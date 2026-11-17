import { chromium } from "playwright-core";
import fs from "node:fs";

const url = process.argv[2];
const outDir = process.argv[3] ?? "/tmp/render-webpage/frames";
const executablePath = process.argv[4];

fs.mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch({ executablePath, headless: true });
const page = await browser.newPage({ viewport: { width: 1400, height: 1000 } });

try {
  await page.goto(url, { waitUntil: "networkidle", timeout: 45000 });
} catch {}
await page.waitForTimeout(2000);

// dismiss any login overlay if present by pressing Escape
await page.keyboard.press("Escape").catch(() => {});
await page.waitForTimeout(500);

const info = await page.evaluate(() => {
  const v = document.querySelector("video");
  if (!v) return null;
  const r = v.getBoundingClientRect();
  return { duration: v.duration, rect: { x: r.x, y: r.y, width: r.width, height: r.height } };
});

console.log("VIDEO_INFO:", JSON.stringify(info));

if (!info) {
  console.error("NO_VIDEO_FOUND");
  await browser.close();
  process.exit(1);
}

const duration = info.duration && isFinite(info.duration) ? info.duration : 45;
const step = 1.0;

await page.evaluate(() => {
  const v = document.querySelector("video");
  v.pause();
  v.muted = true;
});

let n = 0;
for (let t = 0; t < duration; t += step) {
  await page.evaluate((time) => {
    const v = document.querySelector("video");
    v.currentTime = time;
  }, t);
  await page.evaluate(() => {
    document.querySelectorAll('[role="dialog"], [role="presentation"]').forEach((el) => el.remove());
  }).catch(() => {});
  await page.waitForTimeout(250);
  const clip = { x: Math.max(info.rect.x, 0), y: Math.max(info.rect.y, 0), width: info.rect.width, height: info.rect.height };
  await page.screenshot({ path: `${outDir}/frame_${String(n).padStart(3, "0")}_t${t.toFixed(1)}.png`, clip });
  n++;
}

console.log("FRAMES:", n, "DURATION:", duration);
await browser.close();
