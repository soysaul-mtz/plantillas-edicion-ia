"""Audio final de un anuncio del webinar (sobre el video que sacó render.mjs) y entrega.

Uso:  python3 mezcla.py <2038|2040|2041>
- voz: corte/cam.mov con limpieza suave (sin compresor, sin reductor de ruido: Saúl, 4 nov)
- música: Leanin (Slowed) desde el segundo 0, medida contra la voz real: −23 dB al hablar, −12 dB en pausas
- efectos: whoosh en cada cambio de escena (sin pisar la última sílaba), tic en cada chip/notificación, golpe en sellos,
  "listo" cuando aparece la invitación y la flecha
- volumen final −14 LUFS (o menos si subirlo aplastara la voz) → "Video editado - IMG_XXXX.mp4" junto a los crudos
"""
import sys, os, json, re, subprocess, shutil
import numpy as np

n = sys.argv[1]; P = os.path.expanduser(f"./proyectos/web-{n}"); J = lambda f: os.path.join(P, f)
SFX = os.path.expanduser("estilo-cine/sfx")
MUSICA = os.path.expanduser("editor-testimoniales/musica/Leanin (Slowed).wav")
SALIDA = f"<tu disco>/NO BORRAR/ADS/OCTUBRE 2026/WEBINAR/Video editado - IMG_{n}.mp4"
run = lambda *a, **k: subprocess.run(*a, check=True, **k)
dur = lambda f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
VID = J("salida/sin_audio.mp4"); DUR = dur(VID); SR = 48000
C = json.load(open(J("cine.json"))); W = json.load(open(J("voz/palabras.json")))

# ---------- efectos a partir de la escaleta ----------
fx, i = [], 0
fin_antes = lambda t: max([w["b"] for w in W if w["b"] <= t + .05] or [0])
for k, e in enumerate(C["escenas"]):
    ini = W[i]["a"] if i < len(W) else DUR
    if k and e.get("trans"): fx.append([max(ini - .22, fin_antes(ini) + .03), "whoosh_rapido.mp3", .2])
    i += sum(len(l.lstrip("-*~").split()) for gp in e["grupos"] for l in gp["lineas"])
    for it in (e.get("chips") or {}).get("items", []): fx.append([it["en"], "tic.mp3", .32])
    N = e.get("notifs") or {}
    if "impulsar" in N: fx += [[N["impulsar"] + .35, "tic.mp3", .4]]
    for it in N.get("items", []): fx.append([it["en"], "tic.mp3", .32])
    if "cero" in N: fx.append([N["cero"], "boom.mp3", .3])
    O = e.get("orden") or {}
    if "tacha" in O: fx.append([O["tacha"], "glitch_corto.mp3", .2])
    if "swap" in O: fx.append([O["swap"], "whoosh_grave.mp3", .25])
    if "luz2" in O: fx.append([O["luz2"], "listo.mp3", .25])
    for p in (e.get("embudo") or {}).get("pasos", []): fx.append([p["en"], "tic.mp3", .32])
    V = e.get("versus") or {}
    if V: fx += [[V["en"], "boom.mp3", .22], [V["b"], "tic.mp3", .3]]
    if e.get("hoja"): fx.append([e["hoja"]["llena"], "teclear.mp3", .3])
    if e.get("invita"):
        I = e["invita"]
        if not any(f[1] == "listo.mp3" and abs(f[0] - I["en"]) < .1 for f in fx): fx.append([I["en"], "listo.mp3", .3])
        if I.get("flecha"): fx.append([I["flecha"], "rec.mp3", .35])
    if e.get("visual") == "interfaz":
        U = e["ui"]; fx += [[U.get("negocio", 0), "teclear.mp3", .3], [U.get("ideas", 0), "listo.mp3", .25]]
        if U.get("pide"): fx.append([U["pide"], "teclear.mp3", .3])
        if U.get("guion"): fx.append([U["guion"], "listo.mp3", .25])
    if e.get("tel"):  # chat dentro del celular: tecleo al escribir, "listo" cuando responde la IA
        T = e["tel"]; fx += [[T["escribe1"], "teclear.mp3", .25], [T["ideas"], "listo.mp3", .22], [T["escribe2"], "teclear.mp3", .25], [T["guion"], "listo.mp3", .22]]
    if e.get("golpe") is not None: fx.append([e["golpe"], "boom.mp3", .25])
fx = sorted([f for f in fx if 0 <= f[0] < DUR - .3])

# ---------- música medida contra la voz ----------
def pcm(path, sr=SR, ch=2):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", str(ch), "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).copy()
m = pcm(MUSICA); rms = np.sqrt((m[:len(m) // SR * SR, 0].reshape(-1, SR) ** 2).mean(axis=1))
desde = float(np.where(rms >= .7 * np.median(rms))[0][0])
m = m[int(desde * SR):][:int(DUR * SR)]
vz = pcm(J("corte/cam.mov"), 16000, 1)[:, 0]; h = 160
e = np.array([20 * np.log10(np.sqrt((vz[k:k + h] ** 2).mean()) + 1e-9) for k in range(0, len(vz) - h, h)])
voz = e > max(np.percentile(e, 15) + 12, -44)
v_db = 20 * np.log10(np.sqrt(np.mean(10 ** (e[voz] / 10))) + 1e-9)
m_db = 20 * np.log10(np.sqrt((m[len(m) // 4:3 * len(m) // 4] ** 2).mean()) + 1e-9)
VOL, DUCK = 10 ** ((v_db - 12 - m_db) / 20), 10 ** ((-23 + 12) / 20)
g = np.ones(len(m), np.float32)
for k in np.where(voz)[0]: g[max(0, int((k * .01 - .12) * SR)):int((k * .01 + .25) * SR)] = DUCK
q = int(.3 * SR); g = np.convolve(g, np.ones(q) / q, mode="same"); t = np.arange(len(m)) / SR
fin_voz = W[-1]["b"]; g *= np.clip(t / .05, 0, 1) * np.clip((DUR - t) / max(.3, DUR - fin_voz), 0, 1)
m *= (g * VOL)[:, None]
run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", J("_musica.wav")], input=m.tobytes())

VOZ_FX = "highpass=f=80,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.2:g=2,highshelf=f=9000:g=1.5"
ains = ["-i", J("corte/cam.mov"), "-i", J("_musica.wav")]
afc = f"[0:a]aresample={SR},aformat=channel_layouts=stereo,{VOZ_FX},apad=whole_dur={DUR:.3f}[voz];[1:a]anull[mus]"; mix = "[voz][mus]"
for j, (ts, f, vol) in enumerate(fx):
    ains += ["-i", os.path.join(SFX, f)]
    afc += f";[{j + 2}:a]aresample={SR},aformat=channel_layouts=stereo,volume={vol},adelay={round(ts * 1000)}:all=1[s{j}]"; mix += f"[s{j}]"
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
final = J("salida/final.mp4")
run(["ffmpeg", "-v", "error", "-y", *ains, "-i", VID, "-filter_complex", afc + f";[pre]{ln}[a]", "-map", f"{len(ains) // 2}:v", "-map", "[a]",
     "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", final])
shutil.copyfile(final, SALIDA); assert os.path.getsize(SALIDA) == os.path.getsize(final)
print(f"✓ {len(fx)} efectos · música desde {desde:.1f} s · entregado: {SALIDA}")
