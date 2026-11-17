#!/usr/bin/env python3
"""Genera el SVG de Miro (Canvas Composer) de la plantilla "Esquema de empresa".

Uso:  python3 generar.py spec.json [salida.svg]
El spec describe el contenido (ver ejemplo-edita-videos.json). Opciones de posición:
  "origen_x": desplazamiento horizontal en el tablero (para no encimar otros dibujos)
Después se manda el SVG a Miro con canvas_create_from_svg y se revisan las medidas.
"""
import json
import math
import sys

INK, BODY, TERRA, PALE, NAVY, LAV = "#1a1a1a", "#595959", "#D97757", "#F9DDD5", "#1E2150", "#DDE1F9"
FF = "formular"
WHO = {"tu": ("TÚ", PALE, INK), "cl": ("CLAUDE", LAV, NAVY)}
CWID, GAPI, GGAP, CH = 400, 40, 200, 360          # tarjeta de agente: ancho, hueco, hueco entre áreas, alto
MB, ABY, DESC_Y, DESC_H = 2050, 2200, 2340, 220    # bus, barra de área, descripción
CIRC_Y, R, SB, NUM_Y, CHIP_Y, CARD_Y = 2750, 130, 2980, 3080, 3140, 3230

spec = json.load(open(sys.argv[1], encoding="utf-8"))
WHO["cl"] = (spec.get("ia", "CLAUDE"), LAV, NAVY)   # etiqueta de las tarjetas de IA (p. ej. "GROK")
OX = spec.get("origen_x", 0)
L, S = [], []


def X(v):
    return v + OX


def div(x1, y1, x2, y2):
    L.append(f'<line data-type="divider" x1="{X(x1):g}" y1="{y1:g}" x2="{X(x2):g}" y2="{y2:g}" stroke="#313131" stroke-width="2" data-line-style="dashed"/>')


def rect(x, y, w, h, fill, stroke="none", rx=0, txt=None, tc=INK, fs=24, bold=False):
    a = f' data-content="{txt}" data-text-color="{tc}" data-font-size="{fs}" data-font-family="{FF}"' if txt else ""
    if txt and bold:
        a += ' data-font-weight="bold"'
    st = f'stroke="{stroke}" stroke-width="2"' if stroke != "none" else 'stroke="none"'
    S.append(f'<rect x="{X(x):g}" y="{y:g}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {st}{a}/>')


def ta(x, y, w, txt, fs=26, col=BODY, bold=False, align="left", ff=FF):
    wt = ' font-weight="bold"' if bold else ""
    S.append(f'<textArea x="{X(x):g}" y="{y:g}" width="{w}" font-family="{ff}" font-size="{fs}" fill="{col}" text-align="{align}"{wt}>{txt}</textArea>')


def bar(cx, y, w, txt, size=48):
    rect(cx - w / 2, y, w, 100, INK, rx=6, txt=txt, tc="#ffffff", fs=size, bold=True)


def asterisk(cx, cy, r, sw):
    for k in range(6):
        a = math.radians(k * 30)
        dx, dy = math.cos(a) * r, math.sin(a) * r
        S.append(f'<line data-type="divider" x1="{X(cx - dx):.0f}" y1="{cy - dy:.0f}" x2="{X(cx + dx):.0f}" y2="{cy + dy:.0f}" stroke="{TERRA}" stroke-width="{sw}"/>')   # en S: debe quedar ENCIMA del banner


def mascot(cx, cy, p=12):
    rect(cx - 3.5 * p, cy - 4 * p, 7 * p, 6 * p, TERRA)
    rect(cx - 6.5 * p, cy - p, 3 * p, 2 * p, TERRA)
    rect(cx + 3.5 * p, cy - p, 3 * p, 2 * p, TERRA)
    rect(cx - 2.5 * p, cy + 2 * p, 2 * p, 2 * p, TERRA)
    rect(cx + 0.5 * p, cy + 2 * p, 2 * p, 2 * p, TERRA)
    rect(cx - 2.5 * p, cy - 2 * p, p, p, INK)
    rect(cx + 1.5 * p, cy - 2 * p, p, p, INK)


def circle(cx, cy, r, fill, stroke=None, dash=None):
    st = f'stroke="{stroke}" stroke-width="2"' + (f' stroke-dasharray="{dash}"' if dash else "") if stroke else 'stroke="none"'
    S.append(f'<circle cx="{X(cx):g}" cy="{cy:g}" r="{r}" fill="{fill}" {st}/>')


def numero(cx, cy, n):
    S.append(f'<circle cx="{X(cx):g}" cy="{cy:g}" r="24" fill="{BODY}" stroke="none" data-content="{n}" data-text-color="#ffffff" data-font-size="26" data-font-weight="bold" data-font-family="{FF}"/>')


# ---- geometría ----
areas = spec["areas"]
cursor, gx = 0, []
for a in areas:
    n = len(a["agentes"])
    w = n * CWID + (n - 1) * GAPI
    gx.append((cursor, w))
    cursor += w + GGAP
W = cursor - GGAP
MINW = spec.get("ancho_min", 3900)   # ancho mínimo: el banner (3600) y las dos tarjetas laterales necesitan este espacio
if W < MINW:
    off = (MINW - W) / 2
    gx = [(l + off, w) for l, w in gx]
    W = MINW
CXW = W / 2

# ---- banner ----
if not spec.get("sin_banner"):
    rect(0, 0, W, 850, LAV, stroke="#9AA5D6")   # con "sin_banner": true el título va directo sobre el tablero, sin fondo lila
w1 = max(3600, len(spec["titulo1"]) * 170)      # ancho holgado: si no, Miro parte el título en 2 líneas
ta(CXW - w1 / 2, 70, w1, spec["titulo1"], 240, NAVY, True, "center")
if spec.get("sin_claude"):
    # titulo2 centrado, sin asterisco ni logo de Claude (para sistemas que no usan Claude)
    ta(CXW - 3300, 420, 6600, spec["titulo2"], 240, NAVY, False, "center")
else:
    ancho2 = spec.get("ancho_titulo2", len(spec["titulo2"]) * 145)   # estimación: formular 240 px ≈ 145 px por letra
    inicio = (W - (ancho2 + 40 + 260 + 40 + 910)) / 2
    ta(inicio, 420, ancho2 + 300, spec["titulo2"], 240, NAVY)
    asterisk(inicio + ancho2 + 40 + 130, 588, 130, 16)
    ta(inicio + ancho2 + 40 + 260 + 40, 420, 1000, "Claude", 240, NAVY, True, "left", "tiempos_text")
BW = 3600
rect(CXW - BW / 2, 820, BW, 150, INK, rx=14, txt=spec["barra"], tc="#ffffff", fs=48, bold=True)

# ---- niveles: dueño y jefe ----
d, j = spec["dueno"], spec["jefe"]
div(CXW, 970, CXW, 1100)
bar(CXW, 1100, d.get("ancho", 560), d["barra"])
div(CXW, 1200, CXW, 1230)
rect(CXW - 450, 1230, 900, 200, PALE, stroke=TERRA, rx=16, txt=d["texto"], tc=INK, fs=28, bold=True)
div(CXW, 1430, CXW, 1530)
bar(CXW, 1530, j.get("ancho", 820), j["barra"])
div(CXW, 1630, CXW, 1660)
rect(CXW - 450, 1660, 900, 240, "#ffffff", stroke="#d9d9d9", rx=16)
lab, cf, ct = WHO[j.get("quien", "cl")]
rect(CXW - 450 + 28, 1684, 160, 44, cf, rx=22, txt=lab, tc=ct, fs=20, bold=True)
ta(CXW - 450 + 28, 1744, 844, j["texto"], 28, BODY)

# ---- tarjetas laterales (opcionales): izquierda y derecha del jefe ----
lat = spec.get("laterales", [])
for i, c in enumerate(lat[:2]):
    x = CXW - 1300 if i == 0 else CXW + 700
    rect(x, 1230, 600, 670, "#ffffff", stroke="#d9d9d9", rx=16)
    lab, cf, ct = WHO[c.get("quien", "tu")]
    rect(x + 30, 1262, 130, 44, cf, rx=22, txt=lab, tc=ct, fs=20, bold=True)
    ta(x + 30, 1330, 540, c["titulo"], 40, INK, True)
    ta(x + 30, 1450, 540, c["texto"], 28, BODY)
    if c.get("placeholder"):
        rect(x + 30, 1700, 540, 130, "#f3f3f3", rx=12, txt=c["placeholder"], tc=BODY, fs=28, bold=True)
    if i == 0:
        div(x + 600, 1780, CXW - 450, 1780)
    else:
        div(CXW + 450, 1780, x, 1780)

# ---- bus y áreas ----
div(CXW, 1900, CXW, MB)
c0, cN = gx[0][0] + gx[0][1] / 2, gx[-1][0] + gx[-1][1] / 2
div(c0, MB, cN, MB)
for a, (gl, gw) in zip(areas, gx):
    gc, n = gl + gw / 2, len(a["agentes"])
    div(gc, MB, gc, ABY)
    bar(gc, ABY, a.get("ancho", len(a["nombre"]) * 30 + 40), a["nombre"])
    div(gc, ABY + 100, gc, DESC_Y)
    bw = min(max(gw, 460), 760)
    rect(gc - bw / 2, DESC_Y, bw, DESC_H, "#f3f3f3", rx=12, txt=a["descripcion"], tc=BODY, fs=26)
    div(gc, DESC_Y + DESC_H, gc, CIRC_Y - R)
    circle(gc, CIRC_Y, R, "#ffffff", stroke="#8a8a8a", dash="5,5")
    mascot(gc, CIRC_Y)
    centers = [gl + i * (CWID + GAPI) + CWID / 2 for i in range(n)]
    div(gc, CIRC_Y + R, gc, SB if n > 1 else NUM_Y - 24)
    if n > 1:
        div(centers[0], SB, centers[-1], SB)
        for cx in centers:
            div(cx, SB, cx, NUM_Y - 24)
    for i, ag in enumerate(a["agentes"]):
        cx = centers[i]
        x = cx - CWID / 2
        lab, cf, ct = WHO[ag["quien"]]
        numero(cx, NUM_Y, i + 1)
        rect(x, CHIP_Y, CWID, 64, "#ececec", rx=6, txt=ag["nombre"], tc=BODY, fs=28, bold=True)
        rect(x, CARD_Y, CWID, CH, "#ffffff", stroke="#d9d9d9", rx=16)
        rect(x + 28, CARD_Y + 28, 130, 44, cf, rx=22, txt=lab, tc=ct, fs=20, bold=True)
        ta(x + 28, CARD_Y + 92, CWID - 56, ag["texto"], 26, BODY)

rect(CXW - 1600, CARD_Y + CH + 140, 3200, 150, PALE, rx=24, txt=spec["cierre"], tc=INK, fs=40, bold=True)

svg = '<svg xmlns="http://www.w3.org/2000/svg">\n' + "\n".join(L + S) + "\n</svg>"
out = sys.argv[2] if len(sys.argv) > 2 else "salida.svg"
open(out, "w", encoding="utf-8").write(svg)
print(f"{out}: {len(svg)} caracteres, {len(L) + len(S)} elementos, ancho del esquema {W}")
