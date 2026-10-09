// Native Excalidraw -> SVG -> vector PDF. Set CHROMIUM_PATH to a Chrome executable.
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { createRequire } from 'node:module';
const here=path.dirname(new URL(import.meta.url).pathname);
const root=path.resolve(here,'..');
const deps=process.env.RENDER_DEPS || here;
const require=createRequire(path.join(deps,'package.json'));
const {build}=require('esbuild');
const {chromium}=require('playwright-core');
const temp=process.env.RENDER_TMP || path.join(here,'.render');
fs.mkdirSync(temp,{recursive:true});
await build({stdin:{contents:'import {exportToSvg,exportToCanvas,convertToExcalidrawElements} from "@excalidraw/excalidraw"; window.L={exportToSvg,exportToCanvas,convertToExcalidrawElements};',resolveDir:deps},bundle:true,format:'iife',outfile:path.join(temp,'bundle.js'),define:{'process.env.NODE_ENV':'"production"'},loader:{'.woff2':'file'}});
const fontRoot=path.join(deps,'node_modules/@excalidraw/excalidraw/dist/prod');
const server=http.createServer((req,res)=>{
 if(req.url==='/'){res.setHeader('content-type','text/html');res.end('<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0}</style><script>window.EXCALIDRAW_ASSET_PATH=location.origin+"/"</script><script src="/bundle.js"></script></head><body></body></html>');return;}
 const f=req.url==='/bundle.js'?path.join(temp,'bundle.js'):path.join(fontRoot,decodeURIComponent(req.url));
 fs.readFile(f,(e,d)=>{if(e){res.writeHead(404);res.end();return;}res.setHeader('content-type',f.endsWith('.js')?'text/javascript':f.endsWith('.woff2')?'font/woff2':'application/octet-stream');res.end(d);});
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
try {
 const page=await browser.newPage();
 await page.goto(`http://127.0.0.1:${server.address().port}/`);
 for(const name of fs.readdirSync(path.join(root,'figures/src')).filter(x=>x.endsWith('.json'))){
  const spec=JSON.parse(fs.readFileSync(path.join(root,'figures/src',name),'utf8'));
  const out=await page.evaluate(async s=>{
   const hash=t=>{let h=2166136261;for(const c of t){h^=c.codePointAt(0);h=Math.imul(h,16777619);}return (h>>>0)%2147483647||1;};
   const sk=s.elements.filter(e=>e.type!=='cameraUpdate');
   let elements=L.convertToExcalidrawElements(sk,{regenerateIds:false});
   const appState={exportBackground:false,viewBackgroundColor:'#ffffff'};
   await L.exportToCanvas({elements,appState,files:null,exportPadding:0});await document.fonts.ready;
   elements=L.convertToExcalidrawElements(sk,{regenerateIds:false}).map(e=>({...e,seed:hash(e.id),versionNonce:hash(e.id+'#'),version:1,updated:1}));
   const svg=await L.exportToSvg({elements,appState,files:null,exportPadding:0});
   return {elements,svg:svg.outerHTML,w:+svg.getAttribute('width'),h:+svg.getAttribute('height')};
  },spec);
  const stem=name.replace(/\.json$/,'');
  for(const d of ['excalidraw','svg','pdf'])fs.mkdirSync(path.join(root,'figures',d),{recursive:true});
  fs.writeFileSync(path.join(root,'figures/excalidraw',stem+'.excalidraw'),JSON.stringify({type:'excalidraw',version:2,source:'https://excalidraw.com',elements:out.elements,appState:{viewBackgroundColor:'#f6efe2',gridSize:null},files:{}},null,2));
  fs.writeFileSync(path.join(root,'figures/svg',stem+'.svg'),out.svg);
  const print=await browser.newPage({viewport:{width:Math.ceil(out.w),height:Math.ceil(out.h)},deviceScaleFactor:2});
  await print.setContent(`<html><head><style>@page{margin:0}body{margin:0}svg{display:block}</style></head><body>${out.svg}</body></html>`);
  await print.evaluate(()=>document.fonts.ready);
  await print.pdf({path:path.join(root,'figures/pdf',stem+'.pdf'),width:out.w+'px',height:out.h+'px',printBackground:true,margin:{top:0,right:0,bottom:0,left:0}});
  await print.screenshot({path:path.join(temp,stem+'.png')});await print.close();
  console.log(`${stem}: ${out.w} × ${out.h}, ${out.elements.length} editable objects`);
 }
} finally {await browser.close();server.close();}
