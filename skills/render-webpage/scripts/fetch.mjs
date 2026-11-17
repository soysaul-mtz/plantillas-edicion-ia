import { chromium } from "playwright-core";
import fs from "node:fs";

const url = process.argv[2];
const outPrefix = process.argv[3] ?? "out";
const executablePath = process.argv[4];

if (!url || !executablePath) {
  console.error("Usage: node fetch.mjs <url> <outPrefix> <executablePath>");
  process.exit(1);
}

const browser = await chromium.launch({ executablePath, headless: true });
const page = await browser.newPage({ viewport: { width: 1400, height: 1000 } });

try {
  await page.goto(url, { waitUntil: "networkidle", timeout: 45000 });
} catch {
  // Some pages never go fully idle (polling widgets, chat bubbles, etc.) --
  // fall back to whatever loaded within the timeout instead of failing outright.
}
await page.waitForTimeout(2000);

const text = await page.evaluate(() => document.body.innerText);
fs.writeFileSync(`${outPrefix}.txt`, text);

const height = await page.evaluate(() => document.body.scrollHeight);
await page.setViewportSize({ width: 1400, height: Math.min(height, 20000) });
await page.screenshot({ path: `${outPrefix}.png`, fullPage: true });

console.log("TEXT_LENGTH:", text.length);
console.log("SCREENSHOT:", `${outPrefix}.png`);

await browser.close();
