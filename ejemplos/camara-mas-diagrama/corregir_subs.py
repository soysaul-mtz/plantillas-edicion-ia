"""Corrige lo que Whisper oyó mal en voz/palabras.json (solo el texto que se ve; los tiempos no cambian).
Cada regla: secuencia de palabras oídas → texto correcto. Si cambia el número de palabras, el texto va en la primera y las demás quedan vacías."""
import json, re, sys, os
P = os.path.expanduser("./proyectos")
R = {
 "diag-7546": [("carlos", "Claude"), ("cloud", "Claude")],
 "diag-7547": [("videos de reels", "videos a redes sociales"), ("poner el subtil", "poner subtítulos"), ("una plana", "una plantilla"), ("cloud", "Claude"), ("te tomaba", "me tomaba"), ("lo puede editar", "lo puedo editar")],
 "diag-7548": [("zernie", "Zernio"), ("cernio", "Zernio"), ("inmarca", "mi marca", "min"), ("sinergente", "la empresa del cliente"), ("sinergia", "la empresa del cliente"), ("muchísimos marcas", "muchísimas marcas"), ("la habías pegado", "la pases pegado"), ("cloud", "Claude"), ("estudias en", "esto ya sea en"),
               ("que ella responde", "que haya respuestas"), ("claud lo pere", "Claude lo opere"), ("escriba", "escribe")],
 "diag-7549": [("perspectivas atacando el orden", "perspectiva estás atacando el dolor"), ("grock", "Grok")],
}
norm = lambda t: re.sub(r"[^\wáéíóúñü]", "", t.lower())
for n, reglas in R.items():
    f = f"{P}/{n}/voz/palabras.json"; W = json.load(open(f)); toks = [norm(w["t"]) for w in W]; hechos = 0
    for regla in reglas:
        oido, bien = regla[0], regla[1]; minus = len(regla) > 2
        o = oido.split()
        for i in range(len(W) - len(o) + 1):
            if toks[i:i + len(o)] == o:
                fin = re.search(r"[.,;:?!]+$", W[i + len(o) - 1]["t"]); fin = fin.group(0) if fin else ""
                cap = W[i]["t"][:1].isupper()
                txt = (bien[:1].upper() + bien[1:]) if cap else bien
                if minus: txt = txt[:1].lower() + txt[1:]
                nb = bien.split()
                if len(nb) == len(o):      # mismo número de palabras: se cambia palabra por palabra (cada una sale en su momento)
                    for k, pb in enumerate(nb):
                        keep = re.search(r"[.,;:?!]+$", W[i + k]["t"]); keep = keep.group(0) if keep else ""
                        pb = (pb[:1].upper() + pb[1:]) if (k == 0 and cap and not minus) else pb
                        W[i + k]["t"] = pb + keep
                else:
                    W[i]["t"] = txt + fin
                    for k in range(1, len(o)): W[i + k]["t"] = ""
                toks[i:i + len(o)] = ["#"] * len(o); hechos += 1
    json.dump(W, open(f, "w"), ensure_ascii=False); print(n, hechos, "correcciones")
