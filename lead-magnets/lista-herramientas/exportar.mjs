// Capturas de revisión (--png) o PDF final de index.html.  Uso: node exportar.mjs [--png] [--pdf salida.pdf]
import puppeteer from '../../motor/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';
import path from 'path'; import { fileURLToPath } from 'url';
const AQUI = path.dirname(fileURLToPath(import.meta.url));
import fs from 'node:fs';
const CHROME = process.env.CHROME || ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Chromium.app/Contents/MacOS/Chromium', '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/local/bin/chromium'].find(f => fs.existsSync(f)) || 'google-chrome';  // Mac, Linux o Windows (WSL)
const a = process.argv.slice(2), opt = k => { const i = a.indexOf(k); return i >= 0 ? a[i + 1] : null; };
const b = await puppeteer.launch({ executablePath: CHROME, headless: true, args: [...(process.platform === 'linux' ? ['--no-sandbox'] : []), '--force-color-profile=srgb'] });
const p = await b.newPage();
await p.goto('file://' + path.join(AQUI, 'index.html'), { waitUntil: 'networkidle0' });
await p.evaluateHandle('document.fonts.ready');
if (a.includes('--png')) {
  await p.emulateMediaType('print'); await p.setViewport({ width: 794, height: 1123, deviceScaleFactor: 1.5 });
  const hojas = await p.$$('.pagina');
  for (let i = 0; i < hojas.length; i++) await hojas[i].screenshot({ path: path.join(AQUI, `revision_${i + 1}.png`) });
  console.log('✓', hojas.length, 'capturas');
}
const pdf = opt('--pdf');
if (pdf) { await p.pdf({ path: pdf, width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true }); console.log('✓', pdf); }
await b.close();
