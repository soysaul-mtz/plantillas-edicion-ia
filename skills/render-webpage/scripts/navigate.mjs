import { chromium } from "playwright-core";
import fs from "node:fs";

// Usage: node navigate.mjs <rootUrl> <outPrefix> <executablePath> <folderName1> [folderName2] ...
// Double-clicks through a sequence of folder names in Google Drive's web UI (headless),
// then dumps the resulting view's text, URL, and a screenshot.

const [, , rootUrl, outPrefix, executablePath, ...path] = process.argv;

if (!rootUrl || !executablePath) {
  console.error("Usage: node navigate.mjs <rootUrl> <outPrefix> <executablePath> <folderName1> ...");
  process.exit(1);
}

const browser = await chromium.launch({ executablePath, headless: true });
const page = await browser.newPage({ viewport: { width: 1600, height: 1100 } });

try {
  await page.goto(rootUrl, { waitUntil: "networkidle", timeout: 45000 });
} catch {}
await page.waitForTimeout(2000);

for (const name of path) {
  // Find a row/cell whose text matches the folder name (partial match, case-insensitive)
  const row = page.locator(`[role="row"]:has-text("${name}")`).first();
  try {
    await row.waitFor({ state: "visible", timeout: 10000 });
  } catch (e) {
    console.error(`NOT FOUND: "${name}"`);
    break;
  }
  await row.dblclick();
  try {
    await page.waitForLoadState("networkidle", { timeout: 20000 });
  } catch {}
  await page.waitForTimeout(1500);
}

const text = await page.evaluate(() => document.body.innerText);
fs.writeFileSync(`${outPrefix}.txt`, text);
fs.writeFileSync(`${outPrefix}.url.txt`, page.url());

const height = await page.evaluate(() => document.body.scrollHeight);
await page.setViewportSize({ width: 1600, height: Math.min(height, 20000) });
await page.screenshot({ path: `${outPrefix}.png`, fullPage: true });

console.log("FINAL_URL:", page.url());
console.log("TEXT_LENGTH:", text.length);
console.log("SCREENSHOT:", `${outPrefix}.png`);

await browser.close();
