import fs from 'node:fs';import path from 'node:path';import http from 'node:http';import {createRequire} from 'node:module';
const OUT=path.resolve(new URL('..',import.meta.url).pathname);
const WORK=path.join(OUT,'.build');
const render=path.join(OUT,'../tools/render');
const require=createRequire(path.join(render,'package.json'));const {chromium}=require('playwright-core');
const fontRoot=path.join(render,'node_modules/@excalidraw/excalidraw/dist/prod');
const scenes=JSON.parse(fs.readFileSync(path.join(OUT,'source/scenes.json'),'utf8'));
for(const d of ['stills','layers','frames'])fs.mkdirSync(path.join(WORK,d),{recursive:true});
for(const d of ['excalidraw','svg'])fs.mkdirSync(path.join(OUT,d),{recursive:true});
const server=http.createServer((req,res)=>{
 const url=decodeURIComponent(req.url.split('?')[0]);
 const f=url==='/'?path.join(render,'static/index.html'):url==='/bundle.js'?path.join(render,'dist/bundle.js'):path.join(fontRoot,url);
 fs.readFile(f,(err,data)=>{if(err){res.writeHead(404);res.end();return;}
 res.setHeader('Content-Type',url.endsWith('.woff2')?'font/woff2':url.endsWith('.js')?'text/javascript':'text/html');res.end(data);});
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || (process.platform==='darwin'?'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome':'/opt/pw-browsers/chromium')});
const page=await browser.newPage();page.on('pageerror',e=>console.error(e.message));
await page.goto(`http://127.0.0.1:${server.address().port}`);
const exports=[];
for(const s of scenes){
 const output=await page.evaluate(async(s)=>{
  const L=window.ExcalidrawLib,state={exportBackground:false,viewBackgroundColor:'#fffaf0'};
  const skeleton=[...s.base,...s.layers.flatMap(x=>x.elements)];
  let els=L.convertToExcalidrawElements(skeleton,{regenerateIds:false});
  await L.exportToCanvas({elements:els,appState:state,files:null,exportPadding:0});await document.fonts.ready;
  els=stable(L.convertToExcalidrawElements(skeleton,{regenerateIds:false}));
  const svg=await L.exportToSvg({elements:els,appState:state,files:null,exportPadding:0});
  const canvas=await L.exportToCanvas({elements:els,appState:state,files:null,exportPadding:0});
  const b=els.find(e=>e.id.endsWith('-base-paper'));
  const bounds={...b,id:s.slug+'-bounds',backgroundColor:'transparent',opacity:0};
  const gs=[{name:'base',ids:s.base.map(e=>e.id)},...s.layers.map(g=>({name:g.name,ids:g.elements.map(e=>e.id)}))];
  const pngs=[];
  for(const g of gs){
   const list=els.filter(e=>g.ids.includes(e.id));
   const c=await L.exportToCanvas({elements:[bounds,...list],appState:state,files:null,exportPadding:0});
   if(c.width!==1080||c.height!==1080)throw Error('Layer wrong size: '+g.name+' '+c.width+'x'+c.height);
   pngs.push({name:g.name,png:c.toDataURL('image/png')});
  }
  return {elements:els,svg:svg.outerHTML,png:canvas.toDataURL('image/png'),layers:pngs};
 },s);
 fs.writeFileSync(path.join(OUT,'excalidraw',s.slug+'.excalidraw'),JSON.stringify({type:'excalidraw',version:2,source:'https://excalidraw.com',elements:output.elements,appState:{viewBackgroundColor:'#fffaf0',gridSize:null},files:{}},null,1));
 fs.writeFileSync(path.join(OUT,'svg',s.slug+'.svg'),output.svg);
 fs.writeFileSync(path.join(WORK,'stills',s.slug+'.png'),Buffer.from(output.png.split(',')[1],'base64'));
 exports.push({slug:s.slug,elements:output.elements,layers:output.layers});
 console.log('Rendered',s.slug,output.elements.length+' native elements');
}
// One editable storyboard, with each scene placed in a named native frame.
const combined=[];
exports.forEach((s,i)=>{
 const fx=(i%3)*1220,fy=Math.floor(i/3)*1220,fid='frame-'+s.slug;
 combined.push({id:fid,type:'frame',x:fx,y:fy,width:1080,height:1080,angle:0,strokeColor:'#142d32',backgroundColor:'transparent',fillStyle:'solid',strokeWidth:1,strokeStyle:'solid',roughness:0,opacity:100,groupIds:[],frameId:null,index:null,roundness:null,seed:100+i,version:1,versionNonce:100+i,isDeleted:false,boundElements:null,updated:1,link:null,locked:false,name:s.slug});
 combined.push(...s.elements.map(e=>({...e,x:e.x+fx,y:e.y+fy,frameId:fid})));
});
fs.writeFileSync(path.join(OUT,'storyboard.excalidraw'),JSON.stringify({type:'excalidraw',version:2,source:'https://excalidraw.com',elements:combined,appState:{viewBackgroundColor:'#e7ece8',gridSize:null},files:{}},null,1));

if(process.argv.includes('--animate')){
 await page.evaluate(async(data)=>{
  const cache=[];
  for(const scene of data){
   const layers={};
   for(const g of scene.layers){const im=new Image();im.src=g.png;await im.decode();layers[g.name]=im;}
   cache.push(layers);
  }
  window.images=cache;window.screen=document.createElement('canvas');window.screen.width=1080;window.screen.height=1080;
  window.renderFrame=(i,t,scene)=>{
   const c=window.screen,ctx=c.getContext('2d');ctx.clearRect(0,0,1080,1080);
   ctx.drawImage(window.images[i].base,0,0);
   for(const l of scene.layers){
    const p=Math.min(1,Math.max(0,(t-l.at)/l.duration));if(!p)continue;
    const ease=1-Math.pow(1-p,3);ctx.save();
    if(l.kind==='wipe'){
     const lo=Math.min(...l.elements.map(e=>e.y)),hi=Math.max(...l.elements.map(e=>e.y+(e.height||0)));
     ctx.beginPath();ctx.rect(0,lo-15,1080,(hi-lo+30)*ease);ctx.clip();
    }
    else if(l.kind==='flip'){
     const lo=Math.min(...l.elements.map(e=>e.x)),hi=Math.max(...l.elements.map(e=>e.x+(e.width||0))),cx=(lo+hi)/2;
     ctx.translate(cx,0);ctx.scale(Math.sin(ease*Math.PI/2),1);ctx.translate(-cx,0);ctx.globalAlpha=ease;
    }
    else{ctx.globalAlpha=ease;ctx.translate(l.kind==='slide'?(1-ease)*-48:0,l.kind==='rise'?(1-ease)*22:0);}
    ctx.drawImage(window.images[i][l.name],0,0);ctx.restore();
   }
   return c.toDataURL('image/png');
  };
 },exports);
 const frames=[];let count=0;
 for(let i=0;i<scenes.length;i++){
  const s=scenes[i],boundaries=new Set([0,s.duration]);
  for(const l of s.layers){for(let t=l.at;t<l.at+l.duration+.001;t+=.08)if(t>=0)boundaries.add(Math.min(s.duration,+t.toFixed(3)));}
  const ts=[...boundaries].sort((a,b)=>a-b);
  for(let j=0;j<ts.length-1;j++){
   const t=ts[j],dur=Math.max(10,Math.round((ts[j+1]-t)*1000/10)*10);
   const png=await page.evaluate(({i,t,s})=>window.renderFrame(i,t,s),{i,t:t+.02,s});
   const filename=`${String(count++).padStart(4,'0')}.png`;
   fs.writeFileSync(path.join(WORK,'frames',filename),Buffer.from(png.split(',')[1],'base64'));
   frames.push({file:filename,duration:dur,scene:s.slug,time:t});
  }
  console.log('Animated',s.slug);
 }
 fs.writeFileSync(path.join(WORK,'frames.json'),JSON.stringify(frames,null,1));
 console.log('Frames',count,'Duration ms',frames.reduce((a,b)=>a+b.duration,0));
}
await browser.close();server.close();
