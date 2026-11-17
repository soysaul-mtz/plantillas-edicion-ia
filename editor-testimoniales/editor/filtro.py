"""Filtro de piel y color de Saúl sobre la cámara del armado en 1080 (antes de poner imágenes y subtítulos).

Uso:  .venv/bin/python filtro.py <proyecto> [--hilos 4]

Toma la cámara sola del armado (_corte_sin_broll.mp4, o corte.mp4 si no hay tomas encima), le aplica estilo-cine/piel.py
(suavizado solo en piel dentro de la silueta + color apenas cálido) y la capa final del look C8253 (viñeta, desenfoque fino,
brillo, grano solo en luz; SIN colorbalance: la pared gris se iba a morado) y la deja en su lugar. El original queda en
_cam_sin_filtro.mp4 (si ya existe, se parte de ahí: correrlo dos veces no filtra doble). Después: stock_encima.py y terminar.
"""
import sys, os, glob, shutil, subprocess
import conf

proj = os.path.abspath(sys.argv[1]); P = lambda f: os.path.join(proj, f)
args = sys.argv[2:]; HILOS = int(args[args.index("--hilos") + 1]) if "--hilos" in args else 4
CINE = os.path.expanduser("."); PIEL_PY = os.path.expanduser(".venv/bin/python")
run = lambda *a, **k: subprocess.run(*a, check=True, **k)
dst = P("_corte_sin_broll.mp4") if os.path.exists(P("_corte_sin_broll.mp4")) else P("corte.mp4")
orig, ok = P("_cam_sin_filtro.mp4"), P("_filtro.ok")
if os.path.exists(ok) and os.path.getmtime(ok) >= os.path.getmtime(dst) and "--otra-vez" not in args:
    sys.exit(print("✓ la cámara ya tiene el filtro (--otra-vez para rehacerlo)"))
# si el armado es nuevo (o nunca se filtró), el original es lo que hay ahora; si ya se filtró, se parte del original guardado
if not os.path.exists(orig) or not os.path.exists(ok) or os.path.getmtime(dst) > os.path.getmtime(ok): shutil.copyfile(dst, orig)
cu, ma, cp = P("cuadros"), P("mascaras"), P("cuadros_pro")
for d in (cu, ma, cp): shutil.rmtree(d, ignore_errors=True)
os.makedirs(cu); os.makedirs(ma)
print("filtro: silueta y cuadros…", flush=True)
p1 = subprocess.Popen([os.path.join(CINE, "bin", "segmentar"), orig, "540", "960"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", "540x960", "-r", "30000/1001", "-i", "-",
     os.path.join(ma, "%05d.jpg")], stdin=p1.stdout); p1.wait()
run(["ffmpeg", "-v", "error", "-y", "-i", orig, "-q:v", "2", os.path.join(cu, "%05d.jpg")])
nc, nm = len(glob.glob(os.path.join(cu, "*.jpg"))), len(glob.glob(os.path.join(ma, "*.jpg")))
for i in range(nm + 1, nc + 1): shutil.copy(os.path.join(ma, f"{nm:05d}.jpg"), os.path.join(ma, f"{i:05d}.jpg"))   # relleno al final
print(f"filtro: piel en {nc} cuadros…", flush=True)
run([PIEL_PY, os.path.join(CINE, "estilo-cine", "piel.py"), proj, "--hilos", str(HILOS)], stdout=subprocess.DEVNULL)
LOOK = "vignette=angle=PI/7,gblur=sigma=0.5,eq=brightness=0.025,format=yuv420p,noise=c0s=6:c0f=t"
run(["ffmpeg", "-v", "error", "-y", "-framerate", "30000/1001", "-i", os.path.join(cp, "%05d.jpg"), "-i", orig, "-map", "0:v", "-map", "1:a",
     "-vf", LOOK, "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "copy", "-shortest", "-movflags", "+faststart", dst])
for d in (cu, ma, cp): shutil.rmtree(d, ignore_errors=True)
open(ok, "w").write("ok")
print(f"✓ filtro aplicado → {os.path.basename(dst)}")
