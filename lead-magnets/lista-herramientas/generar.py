"""Genera index.html (la lista bonita, una hoja por categoría, lista para imprimir a PDF) a partir de datos.json.
Uso: python3 generar.py && open index.html
"""
import json, html, os

AQUI = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(AQUI, 'datos.json')))
e = html.escape

def insignia(t):
    c = 'b-libre' if t.startswith(('Gratis', 'Open source')) else 'b-prueba' if t.startswith('Prueba') else 'b-plan'
    return f'<span class="badge {c}">{e(t)}</span>'

def ficha(nombre, logo, tam=''):
    if os.path.exists(os.path.join(AQUI, 'logos', logo + '.png')):
        return f'<div class="logo {tam}"><img src="logos/{logo}.png" alt=""></div>'
    ini = ''.join(c for c in nombre if c.isupper())[:2] or nombre[:2]
    return f'<div class="logo ini {tam}">{e(ini)}</div>'

total = sum(len(c['items']) for c in D['categorias'])
unicos = []
for c in D['categorias']:
    for it in c['items']:
        if it[1] not in unicos: unicos.append(it[1])

paginas = []
# ---- portada
mosaico = ''.join(ficha(n, n, 'mini') for n in unicos)
indice = ''.join(f'<li><span class="num">{i + 1:02d}</span><span>{e(c["titulo"])}</span><span class="cuantas">{len(c["items"])}</span></li>'
                 for i, c in enumerate(D['categorias']))
paginas.append(f'''
<section class="pagina portada">
  <div class="mosaico">{mosaico}</div>
  <div class="velo"></div>
  <div class="cont">
    <div class="marca">{e(D["handle"])}</div>
    <h1><span class="serif">{total} herramientas</span><br>de IA <mark>gratis</mark></h1>
    <p class="sub">{e(D["subtitulo"])}</p>
    <ol class="indice">{indice}</ol>
    <div class="pie"><span>{e(D["autor"])}</span><span>{e(D["fecha"])}</span></div>
  </div>
</section>''')

# ---- una hoja por categoría
for i, c in enumerate(D['categorias']):
    tarjetas = ''
    for nombre, logo, tipo, desc, link in c['items']:
        tarjetas += f'''
      <a class="tarjeta" href="https://{e(link)}" target="_blank">
        {ficha(nombre, logo)}
        <div class="txt">
          <div class="fila"><h3>{e(nombre)}</h3>{insignia(tipo)}</div>
          <p>{e(desc)}</p>
          <span class="link">{e(link)} ↗</span>
        </div>
      </a>'''
    paginas.append(f'''
<section class="pagina cat" id="{c["id"]}">
  <header>
    <div class="numgrande">{i + 1:02d}</div>
    <div>
      <div class="kicker">Usa estas herramientas gratis para</div>
      <h2 class="serif">{e(c["titulo"])}</h2>
      <p class="intro">{e(c["intro"])}</p>
    </div>
  </header>
  <div class="grid">{tarjetas}
  </div>
  <footer><span>{e(D["handle"])}</span><span>{i + 2} / {len(D["categorias"]) + 2}</span></footer>
</section>''')

# ---- cierre
paginas.append(f'''
<section class="pagina cierre">
  <div class="cont">
    <div class="kicker">Antes de empezar</div>
    <h2 class="serif">Cómo sacarle provecho<br>a esta lista</h2>
    <ol class="pasos">
      <li><b>Escoge una sola categoría.</b> La que hoy te quita más tiempo. No intentes usar las 70 a la vez.</li>
      <li><b>Prueba dos o tres herramientas</b> con un caso real de tu negocio, no con ejemplos.</li>
      <li><b>Quédate con la que se sienta natural</b> y vuélvela parte de tu rutina de cada semana.</li>
      <li><b>Combínalas:</b> idea en Claude → guion → video con tu avatar → clips → anuncio. Así se arma un sistema.</li>
    </ol>
    <div class="cta">
      <div>Si esta lista te sirvió, sígueme para más herramientas y sistemas con IA</div>
      <div class="handle">{e(D["handle"])}</div>
    </div>
    <p class="nota">Los planes gratis, créditos y pruebas cambian seguido. Lista revisada en {e(D["fecha"].lower())}.
    "Gratis (pagas la pauta)" = la herramienta no cuesta, lo que pagas es el anuncio. "Open source" = gratis si lo instalas tú.</p>
  </div>
</section>''')

CSS = '''
@font-face { font-family: "Instrument Serif"; src: url("InstrumentSerif-Regular.ttf"); }
:root { --fondo:#0e0d0b; --tarjeta:#181612; --borde:#2a2620; --texto:#f4efe6; --suave:#a39d91; --amarillo:#ffe11a; }
* { box-sizing:border-box; margin:0; padding:0; }
html { background:#2b2925; }
body { font-family:"Helvetica Neue", Helvetica, Arial, sans-serif; color:var(--texto); -webkit-print-color-adjust:exact; print-color-adjust:exact; }
.serif { font-family:"Instrument Serif", Georgia, serif; font-weight:400; letter-spacing:-.01em; }
.pagina { width:210mm; height:297mm; margin:24px auto; background:var(--fondo); position:relative; overflow:hidden;
  box-shadow:0 20px 60px rgba(0,0,0,.45); padding:16mm 14mm 14mm; display:flex; flex-direction:column; }
mark { background:var(--amarillo); color:#111; padding:0 .18em; border-radius:.12em; box-decoration-break:clone; }
.kicker { text-transform:uppercase; letter-spacing:.18em; font-size:9pt; color:var(--amarillo); font-weight:700; }

/* portada */
.portada { padding:0; }
.mosaico { position:absolute; inset:-10mm; display:grid; grid-template-columns:repeat(9,1fr); gap:5mm; padding:8mm; transform:rotate(-8deg) scale(1.15); opacity:.32; }
.mosaico .logo { width:100%; height:auto; aspect-ratio:1; }
.velo { position:absolute; inset:0; background:linear-gradient(180deg, rgba(14,13,11,.55) 0%, rgba(14,13,11,.92) 38%, var(--fondo) 62%); }
.portada .cont { position:relative; z-index:2; padding:22mm 16mm 14mm; display:flex; flex-direction:column; height:100%; }
.marca { font-weight:700; letter-spacing:.06em; font-size:11pt; color:var(--amarillo); }
.portada h1 { margin-top:46mm; font-size:50pt; line-height:.98; font-weight:800; letter-spacing:-.03em; }
.portada h1 .serif { font-size:62pt; font-weight:400; letter-spacing:-.02em; }
.sub { margin-top:7mm; font-size:13pt; line-height:1.4; color:#d8d2c6; max-width:150mm; }
.indice { list-style:none; margin-top:12mm; border-top:1px solid var(--borde); }
.indice li { display:flex; align-items:baseline; gap:6mm; padding:3.2mm 0; border-bottom:1px solid var(--borde); font-size:13pt; }
.indice .num { color:var(--amarillo); font-weight:800; font-size:10pt; width:8mm; }
.indice .cuantas { margin-left:auto; color:var(--suave); font-size:10pt; }
.pie { margin-top:auto; display:flex; justify-content:space-between; color:var(--suave); font-size:10pt; }

/* categoría */
.cat header { display:flex; gap:7mm; align-items:flex-start; margin-bottom:7mm; }
.numgrande { font-family:"Instrument Serif", Georgia, serif; font-size:78pt; line-height:.8; color:transparent; -webkit-text-stroke:1.2px var(--amarillo); }
.cat h2 { font-size:38pt; line-height:1; margin-top:1.5mm; }
.intro { margin-top:2.5mm; font-size:10.5pt; line-height:1.45; color:#cfc8bb; max-width:140mm; }
.grid { display:grid; grid-template-columns:1fr 1fr; grid-auto-rows:1fr; gap:4mm; flex:1; align-content:stretch; }
.tarjeta { display:flex; gap:4.5mm; align-items:center; padding:5mm; background:var(--tarjeta); border:1px solid var(--borde); border-radius:4mm;
  text-decoration:none; color:inherit; transition:transform .15s, border-color .15s; }
.tarjeta:hover { transform:translateY(-2px); border-color:#5a5140; }
.logo { flex:none; width:17mm; height:17mm; border-radius:3.6mm; background:#fff; display:flex; align-items:center; justify-content:center; overflow:hidden; box-shadow:0 2px 10px rgba(0,0,0,.35); }
.logo img { width:78%; height:78%; object-fit:contain; }
.logo.ini { background:linear-gradient(135deg,#2b2d42,#5a3fd1); color:#fff; font-weight:800; font-size:13pt; }
.logo.mini { border-radius:22%; }
.txt { min-width:0; }
.fila { display:flex; align-items:center; gap:2.5mm; flex-wrap:wrap; }
.tarjeta h3 { font-size:12.5pt; font-weight:700; }
.tarjeta p { margin-top:1.4mm; font-size:10pt; line-height:1.35; color:#cfc8bb; }
.link { display:block; margin-top:2mm; font-size:8pt; color:var(--suave); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.badge { font-size:6.8pt; font-weight:700; text-transform:uppercase; letter-spacing:.06em; padding:.7mm 2mm; border-radius:10mm; white-space:nowrap; }
.b-libre { background:var(--amarillo); color:#151100; }
.b-plan { border:1px solid var(--amarillo); color:var(--amarillo); }
.b-prueba { border:1px solid #6d675c; color:#c9c2b5; }
.cat footer { display:flex; justify-content:space-between; color:var(--suave); font-size:8.5pt; margin-top:5mm; }

/* cierre */
.cierre .cont { display:flex; flex-direction:column; height:100%; padding-top:14mm; }
.cierre h2 { font-size:42pt; line-height:1.02; margin-top:3mm; }
.pasos { margin-top:12mm; counter-reset:p; list-style:none; }
.pasos li { counter-increment:p; position:relative; padding:5mm 0 5mm 16mm; border-bottom:1px solid var(--borde); font-size:12pt; line-height:1.45; color:#d8d2c6; }
.pasos li::before { content:counter(p, decimal-leading-zero); position:absolute; left:0; top:5mm; color:var(--amarillo); font-weight:800; font-size:11pt; }
.pasos b { color:var(--texto); }
.cta { margin-top:auto; background:var(--amarillo); color:#141000; border-radius:5mm; padding:9mm; font-size:13pt; line-height:1.4; font-weight:600; }
.cta .handle { font-size:30pt; font-weight:800; letter-spacing:-.02em; margin-top:2mm; }
.nota { margin-top:6mm; font-size:8pt; line-height:1.5; color:var(--suave); }

@page { size:210mm 297mm; margin:0; }
@media print { html { background:none; } .pagina { margin:0; box-shadow:none; page-break-after:always; } }
'''

doc = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>{e(D["titulo"])} · {e(D["handle"])}</title>
<meta name="viewport" content="width=device-width, initial-scale=1"><style>{CSS}</style></head>
<body>{"".join(paginas)}
</body></html>'''
open(os.path.join(AQUI, 'index.html'), 'w').write(doc)
print('✓ index.html', total, 'herramientas,', len(unicos), 'logos distintos,', len(paginas), 'hojas')
