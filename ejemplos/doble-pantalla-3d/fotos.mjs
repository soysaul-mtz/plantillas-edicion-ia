// Fotos sueltas de una escena (para revisar antes de renderizar): node fotos.mjs <escena.html[?capa=..]> <carpeta> t1 t2 ...
import path from 'node:path';
import puppeteer from '../videos-voz-ia/motor/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';
const [escena, dir, ...ts] = process.argv.slice(2);
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true,
  args: ['--force-color-profile=srgb', '--allow-file-access-from-files', '--enable-webgl', '--ignore-gpu-blocklist', '--use-angle=metal'] });
const p = await b.newPage(); p.on('pageerror', e => console.error('escena:', e.message)); p.on('console', m => m.type() === 'error' && console.error('escena:', m.text()));
await p.setViewport({ width: 1920, height: 1080 }); await p.goto('file://' + path.resolve(escena.split('?')[0]) + (escena.includes('?') ? '?' + escena.split('?')[1] : ''));
await p.evaluate(() => window.listo);
for (const t of ts) { await p.evaluate(t => window.pinta(t), +t); await p.screenshot({ path: `${dir}/${t}.png`, omitBackground: true }); }
await b.close(); console.log('✓', ts.length, 'fotos');
