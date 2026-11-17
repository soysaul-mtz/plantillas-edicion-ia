"""Ajusta zoom.json para que el panel de pantalla nunca enseñe las pestañas/favoritos del navegador (arriba de y=ARRIBA px).
Uso: python sin_barras.py proyectos/<n> [arriba=148] [izq=88]   (pestañas+URL+favoritos hasta y≈145; barra lateral de Opera hasta x≈85)"""
import sys, json, os
P = sys.argv[1]; ARRIBA = float(sys.argv[2]) if len(sys.argv) > 2 else 148
IZQ = float(sys.argv[3]) if len(sys.argv) > 3 else 88
Z = json.load(open(os.path.join(P, "zoom.json"))); out = []
wmax = (1080 - ARRIBA) * 1080 / 810
for cx, cy, w in Z:
    w = min(w, wmax); h = w * 810 / 1080
    cy = min(max(cy, ARRIBA + h / 2), 1080 - h / 2); cx = min(max(cx, IZQ + w / 2), 1920 - w / 2)
    out.append([round(cx, 1), round(cy, 1), round(w, 1)])
json.dump(out, open(os.path.join(P, "zoom.json"), "w")); print(f"✓ zoom sin barras del navegador (ancho máx {wmax:.0f})")
