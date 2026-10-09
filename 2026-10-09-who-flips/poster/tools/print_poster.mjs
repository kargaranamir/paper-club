// Render the local HTML artifact; no remote resources are required.
import path from 'node:path';
import fs from 'node:fs';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const here=path.dirname(new URL(import.meta.url).pathname),root=path.resolve(here,'..');
const require=createRequire(path.join(process.env.RENDER_DEPS||here,'package.json'));
const {chromium}=require('playwright-core');
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
try{
 const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});
 const failures=[];page.on('pageerror',e=>failures.push(e.message));
 await page.route('https://**/*',r=>r.abort());await page.route('http://**/*',r=>r.abort());
 await page.goto(pathToFileURL(path.join(root,'who-flips-a0.html')).href);
 await page.evaluate(()=>document.fonts.ready);
 await page.emulateMedia({media:'print'});
 await page.pdf({path:path.join(root,'who-flips-a0.pdf'),preferCSSPageSize:true,printBackground:true,displayHeaderFooter:false,margin:{top:0,right:0,bottom:0,left:0}});
 const geometry=await page.evaluate(()=>{
  const p=document.querySelector('.poster').getBoundingClientRect();
  const cards=Array.from(document.querySelectorAll('.card,.masthead,.footer,.footer-end'));
  return {poster:{width:p.width,height:p.height},fonts:[...document.fonts].map(f=>({family:f.family,weight:f.weight,status:f.status})),cards:cards.map(c=>({class:c.className,overflow:c.scrollHeight>c.clientHeight+1,scroll:c.scrollHeight,height:c.clientHeight,children:Array.from(c.children).filter(e=>!e.classList.contains('tab')).map(e=>{const r=e.getBoundingClientRect(),cr=c.getBoundingClientRect();return {tag:e.tagName,class:e.className,top:r.top-cr.top,bottom:r.bottom-cr.top,outside:r.bottom>cr.bottom+2};})}))};
 });
 console.log(JSON.stringify({failures,...geometry},null,2));
}finally{await browser.close();}
