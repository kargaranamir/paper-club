// Print slide.html to a one-page 16:9 PDF (Nafiseh_Nikeghbal.pdf) and a PNG preview.
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const here = path.dirname(new URL(import.meta.url).pathname);
const require = createRequire(path.join(process.env.RENDER_DEPS || here, 'package.json'));
const {chromium} = require('playwright-core');
const browser = await chromium.launch({executablePath: process.env.CHROMIUM_PATH, headless: true});
try {
  const page = await browser.newPage({viewport: {width: 1280, height: 720}, deviceScaleFactor: 2});
  await page.goto(pathToFileURL(path.join(here, 'slide.html')).href);
  await page.evaluate(() => document.fonts.ready);
  const over = await page.evaluate(() => [...document.querySelectorAll('.card,.bottom')].filter(e => e.scrollHeight > e.clientHeight + 1 || e.scrollWidth > e.clientWidth + 1).map(e => e.className));
  console.log('overflow:', JSON.stringify(over));
  await page.pdf({path: path.join(here, 'Nafiseh_Nikeghbal.pdf'), width: '1280px', height: '720px', printBackground: true, preferCSSPageSize: true, margin: {top: 0, right: 0, bottom: 0, left: 0}});
  await page.screenshot({path: path.join(here, 'preview.png')});
} finally { await browser.close(); }
