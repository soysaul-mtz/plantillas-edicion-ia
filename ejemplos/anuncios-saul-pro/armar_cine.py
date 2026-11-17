"""Arma cine.json (motor Saúl Pro) de los anuncios del webinar de Jorge a partir de escenas.py.

Uso:  python3 armar_cine.py <2038|2040|2041>
- cortes = uniones reales del corte (corte/mapa.json), para que el zoom alterno tape cada salto de toma
- sin música ni efectos automáticos: el audio final lo arma mezcla.py (voz mejorada sin comprimir + Leanin bajo la voz + efectos)
"""
import sys, os, json, glob
import escenas as ES

n = sys.argv[1]; P = os.path.expanduser(f"./proyectos/web-{n}")
mapa = json.load(open(f"{P}/corte/mapa.json"))["piezas"]; t, cortes = 0, []
for a, b in mapa[:-1]: t += b - a; cortes.append(round(t, 3))
spec = ES.VIDEOS[n]
# nunca hay cortes dentro de una interfaz (meterían barridos en la pantalla del chat)
ui = [(e["ui"]["en"], e["ui"]["fin"] + .3) for e in spec["escenas"] if e["visual"] == "interfaz"]
cortes = [c for c in cortes if not any(a <= c <= b for a, b in ui)]
# nada encima de la cara: chips y sticker abajo de la barbilla; donde hay chips no cabe la tarjeta de la clase (sale y vuelve a
# entrar en el cierre con la flecha) y el texto sube arriba con velo
W = json.load(open(f"{P}/voz/palabras.json")); iw = 0
for e in spec["escenas"]:
    ini = W[iw]["a"]; iw += sum(len(l.lstrip("-*~").split()) for gp in e["grupos"] for l in gp["lineas"])
    if e.get("chips"):
        e["chips"]["y"] = 1070 / 1920
        if e.pop("invita", None):
            for gp in e["grupos"]: gp["y"] = .16  # lo más alto en la zona segura: no tapa el cabello
    if e.get("pregunta"): e["pregunta"]["y"] = 1230
    if e.get("invita", {}).get("flecha"):
        e["invita"]["en"] = round(ini, 2)
        e.pop("textoTema", None)     # cierre: letra oscura con velo claro (se lee igual sobre pared clara o camisa negra)
        for gp in e["grupos"]: gp["velo"] = True
# una escena nunca arranca 0.1–0.3 s antes o después de un corte de toma: si no, se cuela un pedacito de la otra toma (Saúl, 5 nov)
W2 = json.load(open(f"{P}/voz/palabras.json")); iw = 0
for k, e in enumerate(spec["escenas"]):
    ini = W2[iw]["a"]; iw += sum(len(l.lstrip("-*~").split()) for gp in e["grupos"] for l in gp["lineas"])
    cerca = [c for c in cortes if abs(c - ini) <= .3]
    if k and cerca and "inicio" not in e: e["inicio"] = round(min(cerca, key=lambda c: abs(c - ini)), 3)
# letra blanca con sombra en todo el video y velo oscuro detrás del texto (el velo claro lavaba la imagen: Saúl, 5 nov)
for e in spec["escenas"]:
    if e["visual"] == "persona":
        e["textoTema"] = "oscuro"
        for gp in e["grupos"]: gp["velo"] = True
# texto de arriba sobre la pared (hexágonos rojo/negro/blanco): velo claro detrás para que se lea
for e in spec["escenas"]:
    if e["visual"] == "persona":
        for gp in e["grupos"]:
            if gp["y"] <= .3 and not e.get("textoTema"): gp["velo"] = True
        # 2040 y 2041 (sillón y pantalón oscuros): el texto de abajo va blanco con sombra
        if spec.get("abajo_oscuro") and all(gp["y"] > .6 and not gp.get("velo") for gp in e["grupos"]): e["textoTema"] = "oscuro"
# celular rastreado (tel): esquinas por cuadro dentro de cine.json, suavizadas ±2 cuadros sin cruzar huecos (cortes de toma)
import numpy as np
for e in spec["escenas"]:
    T = e.get("tel")
    if not T or "quads" not in T: continue
    Q = {int(k): v for k, v in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), T.pop("quads")))).items() if v}
    T["q"] = {n: np.mean([Q[k] for k in range(n - 2, n + 3) if k in Q and all(j in Q for j in range(min(n, k), max(n, k) + 1))], axis=0).round(1).tolist() for n in Q}
cfg = {
    "handle": "@jorgeapellido", "fps": "24000/1001", "cola": .45, "voz": "corte/cam.mov",
    "salida": f"{P}/salida/sin_audio.mp4",
    "persona": {"cuadros": "cuadros_pro", "mascaras": "mascaras", "crudos": "cuadros", "n": len(glob.glob(f"{P}/cuadros_pro/*.jpg")),
                "fondo": "real", "bajar": 0, "zoomAlt": 1.05},
    "cortes": cortes, "cortesFx": spec.get("cortesFx", True), "marcas": {"impacto": -9, "tap": -9}, "sfx_auto": False, "sfx": [],
    "logos": spec.get("logos", {}), "escenas": spec["escenas"],
}
json.dump(cfg, open(f"{P}/cine.json", "w"), ensure_ascii=False, indent=1)
print(f"✓ web-{n}/cine.json · {len(spec['escenas'])} escenas · {len(cortes)} uniones · {cfg['persona']['n']} cuadros")
