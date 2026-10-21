// Usage: node render.mjs <src.json>... ; writes ../../slides/excalidraw/*.excalidraw and ../../slides/svg/*.svg
import http from "node:http"; import fs from "node:fs"; import path from "node:path"; import { chromium } from "playwright-core";
const here = path.dirname(new URL(import.meta.url).pathname);
const root = path.resolve(here, "../..");
const fontsDir = path.join(here, "node_modules/@excalidraw/excalidraw/dist/prod");
const noto = { "arabic.woff2": "@fontsource/noto-sans-arabic/files/noto-sans-arabic-arabic-400-normal.woff2",
  "deva.woff2": "@fontsource/noto-sans-devanagari/files/noto-sans-devanagari-devanagari-400-normal.woff2",
  "ethi.woff2": "@fontsource/noto-sans-ethiopic/files/noto-sans-ethiopic-ethiopic-400-normal.woff2" };
const types = { ".html": "text/html", ".js": "text/javascript", ".woff2": "font/woff2" };
const server = http.createServer((req, res) => {
  const u = decodeURIComponent(req.url.split("?")[0]); let f;
  if (u === "/" ) f = path.join(here, "static/index.html");
  else if (u === "/bundle.js") f = path.join(here, "dist/bundle.js");
  else if (u.startsWith("/noto/")) f = path.join(here, "node_modules", noto[u.slice(6)] || "x");
  else f = path.join(fontsDir, u);
  fs.readFile(f, (err, d) => { if (err) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { "content-type": types[path.extname(f)] || "application/octet-stream" }); res.end(d); });
});
await new Promise(r => server.listen(0, r));
const port = server.address().port;
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || "/opt/pw-browsers/chromium" });
const page = await browser.newPage();
page.on("pageerror", e => console.error("pageerror", e.message));
await page.goto(`http://127.0.0.1:${port}/`);
const outEx = path.join(root, "slides/excalidraw"), outSvg = path.join(root, "slides/svg");
fs.mkdirSync(outEx, { recursive: true }); fs.mkdirSync(outSvg, { recursive: true });
for (const src of process.argv.slice(2)) {
  const skel = JSON.parse(fs.readFileSync(src, "utf8"));
  const { svg, elements } = await page.evaluate(s => window.renderSlide(s), skel);
  const name = path.basename(src, ".json");
  fs.writeFileSync(path.join(outSvg, name + ".svg"), svg);
  fs.writeFileSync(path.join(outEx, name + ".excalidraw"), JSON.stringify({ type: "excalidraw", version: 2, source: "https://excalidraw.com",
    elements, appState: { viewBackgroundColor: "#ffffff", gridSize: 20 }, files: {} }, null, 1));
  console.log("rendered", name);
}
await browser.close(); server.close();
