"""Paso final opcional — el mismo video en 4K (2160×3840), con filtro de piel y color de Saúl.

Uso:  .venv/bin/python cuatrok.py <proyecto> [--sin-filtro] [--hilos 3]

Se corre DESPUÉS de `editar.py <p> terminar` (todo se edita y se revisa en 1080; esto solo vuelve a sacar la imagen en 4K):
  1. Cámara en 4K con los mismos cortes del armado (_cut_filter.txt con 2160×3840) → _cam4k.mp4
  2. Filtro (proyecto.json → "filtro": true, por defecto): estilo-cine/piel.py (suavizado solo en piel + color apenas cálido)
     y la capa final del look C8253 (viñeta, desenfoque fino, brillo, grano solo en luz; sin colorbalance: la pared gris
     se iba a morado) → _cam4k_pro.mp4
  3. Imágenes del Editor 51 en 4K (imagenes51.py con ESCALA=2 → img4k/) encima, en los mismos tiempos → corte4k.mp4
  4. Subtítulos y transiciones al doble de resolución (ESCALA=2 render.mjs) → _video4k.mp4
  5. Audio de final.mp4 (ya mezclado y revisado) → «salida» de proyecto.json (HEVC por hardware)
Prioridad baja y pocos hilos para que la compu siga usable. Los cuadros 4K se borran al terminar.
"""
import sys, os, json, glob, shutil, subprocess
import conf

proj = os.path.abspath(sys.argv[1]); P = lambda f: os.path.join(proj, f)
args = sys.argv[2:]; HILOS = int(args[args.index("--hilos") + 1]) if "--hilos" in args else 3
C = conf.cargar(proj); FILTRO = C.get("filtro", True) and "--sin-filtro" not in args
HERE = conf.HERE; PY = os.path.join(HERE, ".venv", "bin", "python")
CINE = os.path.expanduser("."); PIEL_PY = os.path.expanduser(".venv/bin/python")
run = lambda *a, **k: subprocess.run(*a, check=True, **k)
try: os.nice(10)
except OSError: pass
for f in ("final.mp4", "_cut_filter.txt", "cortes.json"):
    if not os.path.exists(P(f)): sys.exit(f"✗ falta {f}: primero termina el video en 1080 (editar.py <p> terminar)")
W, H = (2160, 3840) if C.get("vertical") else (3840, 2160)
w0, h0 = conf.dims(C["fuente"])
if min(w0, h0) < 2160: print(f"⚠ la cámara es {w0}×{h0}: el 4K saldrá escalado (sin más detalle que el 1080)")

# 1. cámara 4K con los mismos cortes
cam = P("_cam4k.mp4")
if not os.path.exists(cam):
    print("1/5 cámara en 4K con los mismos cortes…", flush=True)
    fc = open(P("_cut_filter.txt")).read().replace("1080:1920", f"{W}:{H}").replace("1920:1080", f"{W}:{H}")
    open(P("_cut_filter4k.txt"), "w").write(fc)
    FU = [C["fuente"]] + sorted({c[2] for c in C["cortes"] if len(c) > 2} - {C["fuente"]})
    run(["ffmpeg", "-v", "error", "-y", "-threads", "4", *[x for s in FU for x in ("-i", s)], "-/filter_complex", P("_cut_filter4k.txt"),
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-c:a", "aac", cam])

# 2. filtro de piel + look
base = cam
if FILTRO:
    pro = P("_cam4k_pro.mp4")
    if not os.path.exists(pro):
        cu, ma, cp = P("cuadros"), P("mascaras"), P("cuadros_pro")
        n = int(float(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries", "stream=nb_read_packets",
                                       "-of", "csv=p=0", cam], capture_output=True, text=True).stdout))
        if len(glob.glob(os.path.join(cu, "*.jpg"))) < n:
            print("2/5 cuadros 4K y silueta…", flush=True)
            for d in (cu, ma): shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
            p1 = subprocess.Popen([os.path.join(CINE, "bin", "segmentar"), cam, "540", "960"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", "540x960", "-r", "30000/1001", "-i", "-",
                 os.path.join(ma, "%05d.jpg")], stdin=p1.stdout); p1.wait()
            run(["ffmpeg", "-v", "error", "-y", "-threads", "4", "-i", cam, "-q:v", "2", os.path.join(cu, "%05d.jpg")])
        print(f"   filtro de piel ({HILOS} hilos, reanudable)…", flush=True)
        run([PIEL_PY, os.path.join(CINE, "estilo-cine", "piel.py"), proj, "--hilos", str(HILOS), "--calidad", "93", "--reanudar"], stdout=subprocess.DEVNULL)
        LOOK = "vignette=angle=PI/7,gblur=sigma=1,eq=brightness=0.025,format=yuv420p,noise=c0s=6:c0f=t"
        run(["ffmpeg", "-v", "error", "-y", "-framerate", "30000/1001", "-i", os.path.join(cp, "%05d.jpg"), "-i", cam, "-map", "0:v", "-map", "1:a",
             "-vf", LOOK, "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-c:a", "copy", "-shortest", pro])
        for d in (cu, ma, cp): shutil.rmtree(d, ignore_errors=True)
    base = pro

# 3. imágenes en 4K encima
print("3/5 imágenes en 4K…", flush=True)
br = C.get("broll", [])
if os.path.exists(P("imagenes.json")):
    run([PY, os.path.join(HERE, "imagenes51.py"), proj, "--solo-clips"], env={**os.environ, "ESCALA": "2"})
ins, fb, prev = ["-i", base], [], "0:v"
for k, r_ in enumerate(br):
    f4 = r_["fuente"].replace(f"{os.sep}img{os.sep}", f"{os.sep}img4k{os.sep}")
    src = f4 if os.path.exists(f4) else r_["fuente"]
    ins += ["-ss", str(r_.get("desde", 0)), "-i", src]
    fb.append(f"[{k + 1}:v]trim=0:{r_['b'] - r_['a'] + .1:.3f},setpts=PTS-STARTPTS+{r_['a']:.3f}/TB,fps=30000/1001,"
              f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},format=yuv420p[b{k}]")
    fb.append(f"[{prev}][b{k}]overlay=eof_action=repeat:enable='between(t,{r_['a']:.3f},{r_['b']:.3f})'[o{k}]"); prev = f"o{k}"
if br:
    open(P("_broll4k.txt"), "w").write(";".join(fb))
    run(["ffmpeg", "-v", "error", "-y", "-threads", "4", *ins, "-/filter_complex", P("_broll4k.txt"), "-map", f"[{prev}]", "-map", "0:a",
         "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-c:a", "copy", P("corte4k.mp4")])
else: shutil.copyfile(base, P("corte4k.mp4"))

# 4. subtítulos y transiciones al doble
print("4/5 subtítulos y transiciones en 4K…", flush=True)
run(["node", os.path.join(HERE, "render.mjs"), proj], env={**os.environ, "ESCALA": "2"})

# 5. audio ya mezclado y revisado del 1080
print("5/5 audio y entrega…", flush=True)
out = C.get("salida") or P("final4k.mp4")
os.makedirs(os.path.dirname(out), exist_ok=True); tmp = P("final4k.mp4")
run(["ffmpeg", "-v", "error", "-y", "-i", P("_video4k.mp4"), "-i", P("final.mp4"), "-map", "0:v", "-map", "1:a", "-c", "copy", "-shortest",
     "-movflags", "+faststart", tmp])
d1, d4 = (float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
          for f in (P("final.mp4"), tmp))
if abs(d1 - d4) > .1: sys.exit(f"✗ el 4K dura {d4:.2f}s y el 1080 {d1:.2f}s: revisa")
shutil.copyfile(tmp, out + ".parcial"); os.replace(out + ".parcial", out)
for f in ("_cam4k.mp4", "corte4k.mp4"):
    if os.path.exists(P(f)): os.remove(P(f))
print(f"✓ 4K listo: {out}")
