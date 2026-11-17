"""Arma el panel "Editado por Claude" y la doble pantalla final.

Uso:  python3 armar_final.py <7544|7545> [--sin-capa]
Lee <v>/final.json:
  {"capa": "escenas/escenaV.html", "broll": true|false, "sfx": [[t, "archivo.mp3", volumen], ...],
   "etiqueta": "FX30-7544.MP4 · SIN TOCAR", "salida": "/ruta/Video editado - FX30-7544.mp4"}
1. capa.mjs → <v>/capa.mov (animación con alfa; se rehace si la escena es más nueva)
2. panel = cam.mp4 (enfocado + piel) + tomas del flujo (proyecto.json → broll) + capa → <v>/panel.mp4
3. audio: voz mejorada (sin compresor) + Leanin (Slowed) medida contra la voz real (−23 dB al hablar, −12 en pausas,
   desde el segundo 0) + efectos → volumen final −14 LUFS (o menos si subir aplastara la voz)
4. doble pantalla 1080x1920: arriba corte.mp4 tal cual (Original · SIN TOCAR), abajo el panel → <v>/final.mp4 y copia a "salida"
"""
import sys, os, json, subprocess, shutil
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__)); v = sys.argv[1]; D = os.path.join(AQUI, v); P = lambda f: os.path.join(D, f)
CF = json.load(open(P("final.json"))); SFX = os.path.expanduser("estilo-cine/sfx")
MUSICA = os.path.expanduser("editor-testimoniales/musica/Leanin (Slowed).wav")
run = lambda *a, **k: subprocess.run(*a, check=True, **k)
dur = lambda f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
DUR = dur(P("corte.mp4")); SR = 48000
nice = ["nice", "-n", "10"]

# 1. capa
# "atras": true → la escena se renderiza en dos pasadas (?capa=atras / ?capa=frente) y lo de atrás queda bajo la silueta de la persona (mascara.mp4)
capa, esc = P("capa.mov"), os.path.join(AQUI, CF["capa"]); atras = P("capa_atras.mov") if CF.get("atras") else None
nuevo = lambda f: not os.path.exists(f) or os.path.getmtime(f) < max(os.path.getmtime(esc), os.path.getmtime(os.path.join(AQUI, "escenas", "comun.js")))
if "--sin-capa" not in sys.argv:
    if nuevo(capa): run(nice + ["node", os.path.join(AQUI, "capa.mjs"), esc + ("?capa=frente" if atras else ""), f"{DUR:.3f}", capa])
    if atras and nuevo(atras): run(nice + ["node", os.path.join(AQUI, "capa.mjs"), esc + "?capa=atras", f"{DUR:.3f}", atras])

# 2. panel
ins, fc, prev = ["-i", P("cam.mp4")], [], "0:v"
br = json.load(open(P("proyecto.json"))).get("broll", []) if CF.get("broll") else []
for k, b in enumerate(br):
    ins += ["-i", b["fuente"]]
    fc.append(f"[{k + 1}:v]setpts=PTS-STARTPTS+{b['a']:.3f}/TB,format=yuv420p[b{k}]")
    fc.append(f"[{prev}][b{k}]overlay=eof_action=pass:enable='between(t,{b['a']:.3f},{b['b']:.3f})'[o{k}]"); prev = f"o{k}"
if atras:
    n_ = len(ins) // 2; ins += ["-i", atras, "-i", P("mascara.mp4")]
    fc.append(f"[{prev}]split[c1][c2];[c1][{n_}:v]overlay=format=auto:shortest=0[ca]")
    fc.append(f"[{n_ + 1}:v]format=gray,gblur=sigma=2,tpad=stop_mode=clone:stop_duration=1[m];[c2][m]alphamerge[pe];[ca][pe]overlay=shortest=0[oa]"); prev = "oa"
if os.path.exists(capa):
    ins += ["-i", capa]; fc.append(f"[{prev}][{len(ins) // 2 - 1}:v]overlay=format=auto:shortest=0[oc]"); prev = "oc"
fc.append(f"[{prev}]format=yuv420p[v]")
run(nice + ["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-t", f"{DUR:.3f}", "-an",
            "-c:v", "libx264", "-crf", "15", "-preset", "medium", P("panel.mp4")])
print("✓ panel.mp4")

# 3. audio
def pcm(path, sr=SR, ch=2):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", str(ch), "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).copy()
m = pcm(MUSICA); rms = np.sqrt((m[:len(m) // SR * SR, 0].reshape(-1, SR) ** 2).mean(axis=1))
desde = CF.get("musica_desde", float(np.where(rms >= .7 * np.median(rms))[0][0]))       # donde la canción ya está llena
m = m[int(desde * SR):][:int(DUR * SR)]
vz = pcm(P("corte.mp4"), 16000, 1)[:, 0]; n = 160
e = np.array([20 * np.log10(np.sqrt((vz[i:i + n] ** 2).mean()) + 1e-9) for i in range(0, len(vz) - n, n)])
voz = e > max(np.percentile(e, 15) + 12, -44)
v_db = 20 * np.log10(np.sqrt(np.mean(10 ** (e[voz] / 10))) + 1e-9)
m_db = 20 * np.log10(np.sqrt((m[len(m) // 4:3 * len(m) // 4] ** 2).mean()) + 1e-9)
V, DUCK = 10 ** ((v_db - 12 - m_db) / 20), 10 ** ((-23 + 12) / 20)
g = np.ones(len(m), np.float32)
for i in np.where(voz)[0]: g[max(0, int((i * .01 - .12) * SR)):int((i * .01 + .25) * SR)] = DUCK
k = int(.3 * SR); g = np.convolve(g, np.ones(k) / k, mode="same"); t = np.arange(len(m)) / SR
g *= np.clip(t / .05, 0, 1) * np.clip((DUR - t) / .6, 0, 1)
m *= (g * V)[:, None]
run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", P("_musica.wav")], input=m.tobytes())
VOZ_FX = "highpass=f=80,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.2:g=2,highshelf=f=9000:g=1.5"
ains = ["-i", P("corte.mp4"), "-i", P("_musica.wav")]
afc = f"[0:a]aresample={SR},{VOZ_FX},apad=whole_dur={DUR:.3f}[voz];[1:a]anull[mus]"; mix = "[voz][mus]"
for j, (ts, f, vol) in enumerate(CF.get("sfx", [])):
    ains += ["-i", os.path.join(SFX, f)]
    afc += f";[{j + 2}:a]aresample={SR},volume={vol},adelay={round(ts * 1000)}:all=1[s{j}]"; mix += f"[s{j}]"
afc += f";{mix}amix=inputs={mix.count('[')}:normalize=0:duration=first,atrim=0:{DUR:.3f}[pre]"
def medir(L):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *ains, "-filter_complex", afc + f";[pre]loudnorm=I={L}:TP=-1.5:LRA=11:print_format=json[a]",
                        "-map", "[a]", "-f", "null", "-"], capture_output=True, text=True).stderr
    return json.loads(o[o.rindex("{"):o.rindex("}") + 1])
L = -14; mj = medir(L)
if float(mj["input_tp"]) + (L - float(mj["input_i"])) > -1.5:
    L = round(max(L - 3, -1.5 - float(mj["input_tp"]) + float(mj["input_i"])), 1); mj = medir(L); print(f"volumen final {L} LUFS (sin comprimir la voz)")
ln = (f"loudnorm=I={L}:TP=-1.5:LRA=11:measured_I={mj['input_i']}:measured_TP={mj['input_tp']}:measured_LRA={mj['input_lra']}:"
      f"measured_thresh={mj['input_thresh']}:offset={mj['target_offset']}:linear=true,aresample={SR}")
run(["ffmpeg", "-v", "error", "-y", *ains, "-filter_complex", afc + f";[pre]{ln}[a]", "-map", "[a]", "-c:a", "pcm_s16le", P("_audio.wav")])
print(f"✓ audio (música desde {desde:.1f} s, {len(CF.get('sfx', []))} efectos)")

# 4. doble pantalla
run(nice + ["node", os.path.join(AQUI, "doble.mjs"), P("corte.mp4"), P("panel.mp4"), P("_audio.wav"), P("final.mp4"), "--etiqueta", CF["etiqueta"]])
if CF.get("salida"):
    shutil.copyfile(P("final.mp4"), CF["salida"])
    assert os.path.getsize(CF["salida"]) == os.path.getsize(P("final.mp4")); print("✓ entregado:", CF["salida"])
