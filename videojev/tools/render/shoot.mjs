// node shoot.mjs out_dir svg...  -> PNG screenshots (for checking)
import fs from "node:fs"; import path from "node:path"; import { chromium } from "playwright-core";
const here = path.dirname(new URL(import.meta.url).pathname);
const [out, ...files] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
const noto = p => "file://" + path.join(here, "node_modules/@fontsource", p);
const css = `@font-face{font-family:"Noto Sans Arabic";src:url(${noto("noto-sans-arabic/files/noto-sans-arabic-arabic-400-normal.woff2")})}
@font-face{font-family:"Noto Sans Devanagari";src:url(${noto("noto-sans-devanagari/files/noto-sans-devanagari-devanagari-400-normal.woff2")})}
@font-face{font-family:"Noto Sans Ethiopic";src:url(${noto("noto-sans-ethiopic/files/noto-sans-ethiopic-ethiopic-400-normal.woff2")})}
body{margin:0} svg{display:block}`;
const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || "/opt/pw-browsers/chromium" });
const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
for (const f of files) {
  await p.setContent(`<html><head><style>${css}</style></head><body>${fs.readFileSync(f, "utf8")}</body></html>`);
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(150);
  await p.screenshot({ path: path.join(out, path.basename(f, ".svg") + ".png") });
}
await b.close();
