"""Filtro de piel y color de Saúl (estilo-cine/piel.py + look C8253) sobre un corte HORIZONTAL 1920x1080.
Igual que testimoniales-mas/editor/filtro.py pero con la silueta en 960x540 y sin tocar proyecto.json.

Uso:  python3 filtro_h.py <entrada.mp4> <salida.mp4> [--hilos 4]
"""
import sys, os, glob, shutil, subprocess, tempfile

src, dst = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
args = sys.argv[3:]; HILOS = int(args[args.index("--hilos") + 1]) if "--hilos" in args else 4
CINE = os.path.expanduser("."); PIEL_PY = os.path.expanduser(".venv/bin/python")
run = lambda *a, **k: subprocess.run(*a, check=True, **k)
tmp = tempfile.mkdtemp(prefix="filtro_h-", dir=os.path.dirname(dst))
cu, ma, cp = (os.path.join(tmp, d) for d in ("cuadros", "mascaras", "cuadros_pro"))
os.makedirs(cu); os.makedirs(ma)
print("filtro: silueta y cuadros…", flush=True)
p1 = subprocess.Popen([os.path.join(CINE, "bin", "segmentar"), src, "960", "540"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", "960x540", "-r", "30000/1001", "-i", "-",
     os.path.join(ma, "%05d.jpg")], stdin=p1.stdout); p1.wait()
run(["ffmpeg", "-v", "error", "-y", "-i", src, "-q:v", "2", os.path.join(cu, "%05d.jpg")])
nc, nm = len(glob.glob(os.path.join(cu, "*.jpg"))), len(glob.glob(os.path.join(ma, "*.jpg")))
for i in range(nm + 1, nc + 1): shutil.copy(os.path.join(ma, f"{nm:05d}.jpg"), os.path.join(ma, f"{i:05d}.jpg"))
print(f"filtro: piel en {nc} cuadros…", flush=True)
run([PIEL_PY, os.path.join(CINE, "estilo-cine", "piel.py"), tmp, "--hilos", str(HILOS)], stdout=subprocess.DEVNULL)
LOOK = "vignette=angle=PI/7,gblur=sigma=0.5,eq=brightness=0.025,format=yuv420p,noise=c0s=6:c0f=t"
run(["ffmpeg", "-v", "error", "-y", "-framerate", "30000/1001", "-i", os.path.join(cp, "%05d.jpg"), "-i", src, "-map", "0:v", "-map", "1:a",
     "-vf", LOOK, "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "copy", "-shortest", "-movflags", "+faststart", dst])
shutil.rmtree(tmp, ignore_errors=True)
print(f"✓ filtro aplicado → {dst}")
