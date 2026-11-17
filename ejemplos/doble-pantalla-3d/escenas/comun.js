// Piezas comunes de las escenas (panel 1920x1080 de "Editado por Claude"): tiempo, curvas y subtítulos palabra por palabra.
export const cl = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
export const pr = (t, a, d) => cl((t - a) / d);                        // progreso 0→1 de a a a+d
export const sale = x => 1 - Math.pow(1 - x, 3);                       // ease-out
export const rebote = x => { const c = 1.70158 * 1.4; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
// visible de a a b con entrada/salida de d segundos → 0..1
export const ventana = (t, a, b, d = .18) => Math.min(sale(pr(t, a, d)), 1 - sale(pr(t, b - d, d)));

const limpia = w => w.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9%]/g, '');

// subtítulos: páginas de hasta 4 palabras (cortan en coma/punto o pausa > .45 s); cada palabra aparece cuando se dice;
// las palabras clave van en amarillo (como pidió Saúl el 4 nov)
export function subtitulos(raiz, W, claves) {
  const C = new Set(claves.map(limpia)), pags = []; let p = [];
  W.forEach(([t, w], i) => {
    p.push({ t, w, k: C.has(limpia(w)) });
    const sig = W[i + 1];
    if (!sig || /[,.]$/.test(w) || p.length === 4 || sig[0] - t > .9) { pags.push(p); p = []; }
  });
  pags.forEach((p, i) => { p.a = p[0].t - .04; p.b = pags[i + 1] ? pags[i + 1][0].t - .04 : p[p.length - 1].t + .9; });
  const el = document.createElement('div'); el.className = 'subs'; raiz.appendChild(el);
  let actual = null;
  return t => {
    const pag = pags.find(p => t >= p.a && t < p.b);
    if (pag !== actual) {
      actual = pag;
      el.innerHTML = pag ? pag.map(x => `<span class="${x.k ? 'k' : ''}">${x.w.replace(/[,.]$/, '')}</span>`).join(' ') : '';
    }
    if (!pag) return;
    [...el.children].forEach((s, i) => {
      const q = sale(pr(t, pag[i].t - .06, .12));
      s.style.opacity = q; s.style.transform = `translateY(${(1 - q) * 14}px)`;
    });
  };
}
