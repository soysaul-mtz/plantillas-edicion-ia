"""Enfoque de tomas desenfocadas (la cámara enfocó la ciudad del fondo): deconvolución Richardson-Lucy con PSF de disco,
SOLO sobre la persona (máscara de Vision, borde suave); el fondo, que ya está nítido, se queda igual. Torch en MPS.

Uso:  python enfoque.py entrada.mp4 salida.mp4 [--radio 10] [--iter 25] [--fuerza 1] [--hasta s] [--cuadro t salida.png]
La entrada ya debe venir a la resolución final del panel (p. ej. 1920x1080); el radio está en px de esa escala.
"""
import sys, os, subprocess, json
import numpy as np, torch, torch.nn.functional as F

a = sys.argv; src, dst = a[1], a[2]
op = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
R, IT, FZ, HASTA = op("--radio", 10.0), op("--iter", 25), op("--fuerza", 1.0), op("--hasta", 0.0)
SEG = os.path.expanduser("estilo-cine/segmentar.swift")
dev = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate",
                                  "-of", "json", src], capture_output=True, text=True).stdout)["streams"][0]
W, H, FPS = info["width"], info["height"], info["r_frame_rate"]


def disco(r):
    n = int(np.ceil(r)) * 2 + 1; yy, xx = np.mgrid[:n, :n] - n // 2
    k = np.clip(r + .5 - np.hypot(xx, yy), 0, 1); k /= k.sum()
    return torch.tensor(k, dtype=torch.float32, device=dev)[None, None]


PSF = disco(R); PSFm = torch.flip(PSF, [2, 3]); PAD = PSF.shape[-1] // 2
conv = lambda x, k: F.conv2d(F.pad(x, (PAD,) * 4, mode="reflect"), k)


def rl(y):
    est = torch.full_like(y, float(y.mean()))
    for _ in range(IT):
        est = (est * conv(y / conv(est, PSF).clamp_min(1e-4), PSFm)).clamp(0, 1.2)
    return est


def enfocar(rgb, m):
    """rgb uint8 HxWx3, m float HxW (0..1) → uint8"""
    x = torch.tensor(rgb, dtype=torch.float32, device=dev) / 255
    Y = (.299 * x[..., 0] + .587 * x[..., 1] + .114 * x[..., 2])[None, None]
    d = (rl(Y) - Y)[0, 0] * FZ                                       # detalle recuperado (solo luminancia: sin halos de color)
    mm = torch.tensor(m, dtype=torch.float32, device=dev)
    out = (x + (d * mm)[..., None]).clamp(0, 1)
    return (out * 255 + .5).byte().cpu().numpy()


def mascaras():
    """máscara de persona por cuadro (Vision), dilatada y suavizada para que el borde no deje aro"""
    p = subprocess.Popen(["swift", SEG, src, str(W), str(H)], stdout=subprocess.PIPE)
    k = torch.ones(1, 1, 15, 15, device=dev) / 225
    while True:
        b = p.stdout.read(W * H)
        if len(b) < W * H: return
        m = torch.tensor(np.frombuffer(b, np.uint8).reshape(H, W).astype(np.float32) / 255, device=dev)[None, None]
        m = F.max_pool2d(m, 9, 1, 4)                                  # crecer un poco: el pelo y la ropa desenfocados salen del borde
        for _ in range(3): m = F.conv2d(F.pad(m, (7,) * 4, mode="replicate"), k)
        yield m[0, 0].cpu().numpy()


if "--cuadro" in a:                                                   # prueba: un solo cuadro (antes|después lado a lado)
    t, png = float(a[a.index("--cuadro") + 1]), a[a.index("--cuadro") + 2]
    fr = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", src, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                      capture_output=True).stdout, np.uint8).reshape(H, W, 3)
    n = round(t * eval(FPS)); m = None
    for i, mk in enumerate(mascaras()):
        if i >= n: m = mk; break
    o = enfocar(fr, m)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W * 2}x{H}", "-i", "-", "-frames:v", "1", png],
                   input=np.concatenate([fr, o], 1).tobytes(), check=True)
    sys.exit(print("✓", png))

lee = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, *(["-t", str(HASTA)] if HASTA else []), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
esc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", FPS, "-i", "-", "-i", src,
                        "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", dst],
                       stdin=subprocess.PIPE)
n = 0
for m in mascaras():
    b = lee.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    esc.stdin.write(enfocar(np.frombuffer(b, np.uint8).reshape(H, W, 3), m).tobytes()); n += 1
    if n % 150 == 0: print(f"  {n} cuadros", flush=True)
esc.stdin.close(); esc.wait(); print(f"✓ {n} cuadros enfocados → {dst}")
