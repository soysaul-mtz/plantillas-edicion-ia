#!/usr/bin/env python3
"""PDF + captura "en bloques" de una guía HTML de la plantilla Esquema de empresa.

Uso:  python3 empaquetar.py <carpeta con index.html> [ancho_tarjeta alto_tarjeta]

Deja en esa misma carpeta:
  <nombre-de-la-carpeta>.pdf   páginas de 1280x1810 px (el CSS de la guía ya trae @page)
  captura-completa.png         la página entera en una imagen
  captura-bloques.png          la página partida en secciones y acomodada en 2 columnas,
                               con la proporción de la tarjeta de Miro donde se va a pegar
                               (por defecto 600x670, la tarjeta "El prompt exacto").
Requiere Google Chrome y Pillow (pip install pillow).
"""
import json
import os
import pathlib
import re
import subprocess
import sys

from PIL import Image, ImageChops, ImageDraw

CHROME = os.environ.get("CHROME") or next((f for f in ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/local/bin/chromium"] if os.path.exists(f)), "google-chrome")
carpeta = pathlib.Path(sys.argv[1]).resolve()
tw, th = (float(sys.argv[2]), float(sys.argv[3])) if len(sys.argv) > 3 else (600.0, 670.0)
index = carpeta / "index.html"
url = f"file://{index}"


def chrome(*args):
    return subprocess.run([CHROME, "--headless=new", *(["--no-sandbox"] if sys.platform == "linux" else []), "--disable-gpu", *args], capture_output=True, text=True)


# 1) PDF
pdf = carpeta / f"{carpeta.name}.pdf"
chrome("--no-pdf-header-footer", f"--print-to-pdf={pdf}", url)

# 2) medir las secciones (copia temporal con un script que anota las posiciones)
probe = carpeta / "_probe.html"
html = index.read_text(encoding="utf-8").replace(
    "</body>",
    '<script>addEventListener("load",function(){var o=[];document.querySelectorAll("section").forEach(function(e){'
    'o.push([e.id,e.offsetTop,e.offsetHeight])});document.body.setAttribute("data-pos",JSON.stringify({s:o,t:document.documentElement.scrollHeight}))})</script></body>',
)
probe.write_text(html, encoding="utf-8")
dom = chrome("--window-size=1280,900", "--virtual-time-budget=3000", "--dump-dom", f"file://{probe}").stdout
probe.unlink()
pos = json.loads(re.search(r'data-pos="([^"]*)"', dom).group(1).replace("&quot;", '"'))

# 3) captura completa
raw = carpeta / "_raw.png"
chrome("--hide-scrollbars", f"--window-size=1280,{pos['t'] + 200}", f"--screenshot={raw}", url)
im = Image.open(raw).convert("RGB")
raw.unlink()
bb = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255))).getbbox()
alto = min(im.size[1], bb[3] + 40)
im = im.crop((0, 0, 1280, alto))
im.save(carpeta / "captura-completa.png")

# 4) bloques: cada sección es un bloque (el primero incluye el banner); 2 columnas equilibradas
cortes = [0] + [max(0, t - 12) for _, t, _ in pos["s"][1:]] + [alto]
bloques = [im.crop((0, cortes[i], 1280, cortes[i + 1])) for i in range(len(cortes) - 1)]
cols, g = [[], []], 40
for b in bloques:
    suma = [sum(x.height for x in c) + g * len(c) for c in cols]
    cols[suma.index(min(suma))].append(b)
alto_cols = max(sum(x.height for x in c) + g * (len(c) - 1) for c in cols)
CW = max(2 * 1280 + 3 * g, int((alto_cols + 2 * g) * tw / th))   # si el contenido es muy alto, se ensancha el lienzo
CH = int(CW / (tw / th))
lienzo = Image.new("RGB", (CW, CH), "white")
d = ImageDraw.Draw(lienzo)
top = (lienzo.height - alto_cols) // 2
for ci, c in enumerate(cols):
    x, y = (CW - (2 * 1280 + g)) // 2 + ci * (1280 + g), top
    for b in c:
        lienzo.paste(b, (x, y))
        d.rectangle([x - 1, y - 1, x + b.width, y + b.height], outline=(210, 210, 210), width=2)
        y += b.height + g
lienzo = lienzo.resize((1200, int(1200 * lienzo.height / lienzo.width)), Image.LANCZOS)
lienzo.save(carpeta / "captura-bloques.png", optimize=True)
print("PDF:", pdf.name, "| captura-completa.png", im.size, "| captura-bloques.png", lienzo.size, "| proporción tarjeta", round(tw / th, 3), "→ lienzo", round(lienzo.width / lienzo.height, 3))
