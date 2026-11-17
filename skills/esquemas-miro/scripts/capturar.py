#!/usr/bin/env python3
"""Hace una imagen PNG del esquema SIN pasar por Miro (réplica con los mismos datos).

Uso:  python3 capturar.py spec.json salida.png
Genera el SVG con generar.py (origen_x = 0), lo dibuja como HTML con las fuentes de la guía
y le toma una captura con Chrome. Sirve para documentos (Word/PDF) y dashboards.
Las fuentes son parecidas a las de Miro (Space Grotesk en vez de Formular), no idénticas.
"""
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

from PIL import Image, ImageChops

aqui = pathlib.Path(__file__).resolve().parent
CHROME = os.environ.get("CHROME") or next((f for f in ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/local/bin/chromium"] if os.path.exists(f)), "google-chrome")
spec_path, salida = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
tmp = pathlib.Path(tempfile.mkdtemp())
spec = json.loads(spec_path.read_text(encoding="utf-8"))
spec["origen_x"] = 0
(tmp / "spec.json").write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
subprocess.run([sys.executable, str(aqui / "generar.py"), str(tmp / "spec.json"), str(tmp / "e.svg")], check=True, capture_output=True)

root = ET.fromstring((tmp / "e.svg").read_text(encoding="utf-8"))
FAM = {"formular": "SG", "tiempos_text": "IS"}
lineas, solidas, cajas, ancho, alto = [], [], [], 0, 0


def num(e, k, d=0.0):
    return float(e.get(k, d))


for e in root:
    t = e.tag.split("}")[-1]
    if t == "line":
        x1, y1, x2, y2 = num(e, "x1"), num(e, "y1"), num(e, "x2"), num(e, "y2")
        dash = ' stroke-dasharray="9 9"' if e.get("data-line-style") == "dashed" else ""
        (lineas if dash else solidas).append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{e.get("stroke")}" stroke-width="{e.get("stroke-width")}" stroke-linecap="round"{dash}/>')
        ancho, alto = max(ancho, x1, x2), max(alto, y1, y2)
    elif t in ("rect", "circle"):
        if t == "rect":
            x, y, w, h, rx = num(e, "x"), num(e, "y"), num(e, "width"), num(e, "height"), num(e, "rx")
        else:
            r = num(e, "r")
            x, y, w, h, rx = num(e, "cx") - r, num(e, "cy") - r, 2 * r, 2 * r, r
        st = e.get("stroke", "none")
        borde = f"2px {'dashed' if e.get('stroke-dasharray') else 'solid'} {st}" if st != "none" else "none"
        txt = e.get("data-content", "")
        fam = FAM.get(e.get("data-font-family", "formular"), "SG")
        peso = 700 if e.get("data-font-weight") == "bold" else 400
        cajas.append(
            f'<div style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{e.get("fill")};border:{borde};border-radius:{rx}px;'
            f'display:flex;align-items:center;justify-content:center;text-align:center;padding:0 14px;'
            f'color:{e.get("data-text-color", "#1a1a1a")};font:{peso} {e.get("data-font-size", 24)}px/1.25 {fam}">{txt}</div>')
        ancho, alto = max(ancho, x + w), max(alto, y + h)
    elif t == "textArea":
        x, y, w = num(e, "x"), num(e, "y"), num(e, "width")
        fam = FAM.get(e.get("font-family", "formular"), "SG")
        peso = 700 if e.get("font-weight") == "bold" else 400
        cajas.append(
            f'<div style="left:{x}px;top:{y}px;width:{w}px;color:{e.get("fill")};text-align:{e.get("text-align", "left")};'
            f'font:{peso} {e.get("font-size")}px/1.35 {fam}">{e.text}</div>')
        alto = max(alto, y + 120)
        ancho = max(ancho, x + w)   # que el lienzo alcance a los títulos centrados

ancho, alto = int(ancho) + 80, int(alto) + 80
html = f'''<!doctype html><meta charset="utf-8"><style>
@font-face{{font-family:"SG";src:url({aqui.parent}/assets/fonts/space-grotesk.woff2);font-weight:300 700}}
@font-face{{font-family:"IS";src:url({aqui.parent}/assets/fonts/instrument-serif.woff2)}}
body{{margin:0;background:#fff;width:{ancho}px;height:{alto}px;position:relative}}
body>div{{position:absolute;box-sizing:border-box}} svg{{position:absolute;left:0;top:0}}
</style><svg width="{ancho}" height="{alto}">{"".join(lineas)}</svg>{"".join(cajas)}<svg width="{ancho}" height="{alto}">{"".join(solidas)}</svg>'''
(tmp / "e.html").write_text(html, encoding="utf-8")
crudo = tmp / "e.png"
subprocess.run([CHROME, "--headless=new", *(["--no-sandbox"] if sys.platform == "linux" else []), "--disable-gpu", "--hide-scrollbars", f"--window-size={ancho},{alto}", "--virtual-time-budget=3000", f"--screenshot={crudo}", f"file://{tmp / 'e.html'}"], capture_output=True)
im = Image.open(crudo).convert("RGB")
bb = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255))).getbbox()
if os.environ.get("SIN_RECORTE"):
    im = im.crop((0, 0, min(im.width, bb[2] + 30), min(im.height, bb[3] + 30)))   # conserva el origen (0,0) para pegar imágenes por coordenadas
else:
    im = im.crop((max(0, bb[0] - 30), max(0, bb[1] - 30), min(im.width, bb[2] + 30), min(im.height, bb[3] + 30)))
im.save(salida, optimize=True)
print(salida, im.size)
