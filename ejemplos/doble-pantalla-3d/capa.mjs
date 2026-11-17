// Renderiza la capa de animación (texto, tarjetas, 3D) de una escena HTML cuadro por cuadro, con fondo transparente.
// Uso: node capa.mjs <escena.html> <duración s> <salida.mov> [--desde s] [--hasta s]
// La escena expone window.listo (promesa) y window.pinta(t) (puede ser async). Sale ProRes 4444 con alfa, 1920x1080, 29.97.
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import puppeteer from '../../motor/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? +args[i + 1] : d; };
const [escena, durS, salida] = args;
const FPS = 30000 / 1001, N = Math.ceil(+durS * FPS);
const f0 = Math.floor(opt('--desde', 0) * FPS), f1 = Math.min(N, Math.ceil(opt('--hasta', +durS) * FPS));
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

const browser = await puppeteer.launch({ executablePath: CHROME, headless: true,
  args: ['--force-color-profile=srgb', '--hide-scrollbars', '--allow-file-access-from-files', '--enable-webgl', '--ignore-gpu-blocklist', '--use-angle=metal'] });
const page = await browser.newPage();
page.on('console', m => { if (m.type() === 'error') console.error('escena:', m.text()); });
page.on('pageerror', e => console.error('escena:', e.message));
await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });
await page.goto('file://' + path.resolve(escena.split('?')[0]) + (escena.includes('?') ? '?' + escena.split('?')[1] : ''));
await page.evaluate(() => window.listo);

const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', '30000/1001', '-i', '-',
  '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', '-vendor', 'apl0', salida], { stdio: ['pipe', 'inherit', 'inherit'] });
const t0 = Date.now();
for (let f = f0; f < f1; f++) {
  await page.evaluate(t => window.pinta(t), f / FPS);
  const png = await page.screenshot({ omitBackground: true, type: 'png' });
  if (!ff.stdin.write(png)) await new Promise(r => ff.stdin.once('drain', r));
  if ((f - f0) % 90 === 0) process.stdout.write(`  capa ${f - f0}/${f1 - f0} cuadros (${((Date.now() - t0) / 1000).toFixed(0)} s)\n`);
}
ff.stdin.end();
await new Promise(r => ff.on('close', r));
await browser.close();
console.log(`✓ ${salida}  ${f1 - f0} cuadros`);
