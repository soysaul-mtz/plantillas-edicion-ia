"""Identifica qué editor usar para un video.

Uso:  python3 identificar.py <video> [<video> ...]

Mira formato (vertical/horizontal, duración), la ruta del archivo y los primeros 2 minutos de audio (Whisper local):
palabras clave de cada editor y si es entrevista (preguntas de alguien fuera de cuadro). Compara contra editores.json
y da un ranking con las razones. Si el mejor no gana con claridad, preguntar a Saúl antes de editar.
"""
import sys, os, json, subprocess, tempfile, unicodedata, re

HERE = os.path.dirname(os.path.abspath(__file__))
EDS = json.load(open(os.path.join(HERE, "editores.json")))
norm = lambda s: "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")

def probe(v):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=width,height:stream_side_data=rotation:format=duration", "-of", "json", v], capture_output=True, text=True).stdout)
    st = j["streams"][0]; w, h = st["width"], st["height"]
    rot = next((int(sd["rotation"]) for sd in st.get("side_data_list", []) or [] if "rotation" in sd), 0)
    if abs(rot) == 90: w, h = h, w
    return w, h, float(j["format"]["duration"])

def oir(v, seg=120):
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, "a.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", v, "-t", str(seg), "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    subprocess.run(["whisper", wav, "--model", "large-v3-turbo", "--language", "es", "--output_format", "json", "--output_dir", tmp, "--verbose", "False"], capture_output=True)
    try: return [s["text"].strip() for s in json.load(open(os.path.join(tmp, "a.json")))["segments"]]
    except Exception: return []

for v in sys.argv[1:]:
    v = os.path.abspath(v)
    if not os.path.exists(v): print(f"\n=== {v}\nNo existe (¿disco desconectado?)"); continue
    w, h, dur = probe(v)
    ori = "vertical" if h > w else "horizontal"
    segs = oir(v); texto = norm(" ".join(segs))
    preguntas = sum(1 for s in segs if "?" in s or "¿" in s)
    entrevista = preguntas >= 3 or any(k in texto for k in ["cual es tu nombre", "a que te dedicas", "que le dirias"])
    print(f"\n=== {os.path.basename(v)}\n{w}x{h} ({ori}) · {dur/60:.1f} min · preguntas en 2 min: {preguntas} -> {'entrevista' if entrevista else 'monólogo a cámara'}")
    print("Oído:", " ".join(segs)[:260] + ("…" if len(" ".join(segs)) > 260 else ""))
    res = []
    for e in EDS:
        s, why = 0, []
        S = e["señales"]
        r = [x for x in S.get("rutas", []) if re.search(r"(?<![a-z])" + re.escape(x.lower()) + r"(?![a-z])", v.lower())]
        if r: s += 2 * len(r); why.append(f"ruta ({', '.join(r)})")
        p = [x for x in S.get("palabras", []) if norm(x) in texto]
        if p: s += 1.5 * len(p); why.append(f"dice: {', '.join(p[:6])}")
        if S.get("orientacion") == ori: s += 3; why.append(ori)
        elif S.get("orientacion"): s -= 2
        if S.get("entrevista") is not None:
            if S["entrevista"] == entrevista: s += 3; why.append("entrevista" if entrevista else "sin entrevistador")
            else: s -= 3
        res.append((s, e, why, bool(p)))
    res.sort(key=lambda x: -x[0])
    for s, e, why, _ in res:
        print(f"  {s:5.1f}  {e['nombre']:28s} {' · '.join(why)}")
    top, seg2 = res[0], (res[1] if len(res) > 1 else (0, None, [], False))
    claro = top[0] >= 6 and top[0] - seg2[0] >= 4 and top[3]   # además debe coincidir lo que se dice, no solo ruta/formato
    if not top[3]: print('   ojo: ninguna palabra clave del editor en lo que se dice (¿otra marca/proyecto?)')
    print(f"-> {'RECOMENDADO' if claro else 'PROBABLE (confirmar con Saúl)'}: {top[1]['nombre']}  [{top[1]['carpeta']}]")
    print(f"   arranque: {top[1]['arranque']}")
