// node pdf.mjs out.pdf svg...  -> one 16:9 page per slide (fonts embedded), merged with pdfunite
import fs from "node:fs"; import path from "node:path"; import os from "node:os"; import { execFileSync } from "node:child_process"; import { chromium } from "playwright-core";
const here = path.dirname(new URL(import.meta.url).pathname);
const [out, ...files] = process.argv.slice(2);
const noto = p => "file://" + path.join(here, "node_modules/@fontsource", p);
const css = `@font-face{font-family:"Noto Sans Arabic";src:url(${noto("noto-sans-arabic/files/noto-sans-arabic-arabic-400-normal.woff2")})}
@font-face{font-family:"Noto Sans Devanagari";src:url(${noto("noto-sans-devanagari/files/noto-sans-devanagari-devanagari-400-normal.woff2")})}
@font-face{font-family:"Noto Sans Ethiopic";src:url(${noto("noto-sans-ethiopic/files/noto-sans-ethiopic-ethiopic-400-normal.woff2")})}
@page{size:1600px 900px;margin:0} html,body{margin:0} svg{display:block;width:1600px;height:900px}`;
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "deck-"));
const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || "/opt/pw-browsers/chromium" });
const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
const parts = [];
for (const [k, f] of files.entries()) {
  await p.setContent(`<html><head><style>${css}</style></head><body>${fs.readFileSync(f, "utf8")}</body></html>`);
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(100);
  const o = path.join(tmp, String(k).padStart(3, "0") + ".pdf");
  await p.pdf({ path: o, width: "1600px", height: "900px", printBackground: true, pageRanges: "1" });
  parts.push(o);
}
await b.close();
execFileSync("pdfunite", [...parts, out]);
console.log("pdf:", out, parts.length, "pages");
