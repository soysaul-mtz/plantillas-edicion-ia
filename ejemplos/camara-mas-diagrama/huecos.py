"""Alinea cada cámara con su grabación de pantalla por audio y busca huecos: segundos donde la pantalla tiene voz y la cámara no."""
import subprocess, numpy as np
B = "<tu disco>/Grabaciones/Casa Nelson/VIDEO DIAGRAMA"
P = [("FX30-7546", "2026-11-01 23-39-20"), ("FX30-7547", "2026-11-01 23-46-26"), ("FX30-7548", "2026-11-01 23-53-09"), ("FX30-7549", "2026-11-01 23-57-10")]
lee = lambda f: np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vn", "-ac", "1", "-ar", "8000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
def env(x):  # dB cada 10 ms
    h = 80; return 20 * np.log10(np.sqrt(np.add.reduceat(x[: len(x) // h * h] ** 2, np.arange(0, len(x) // h * h, h)) / h) + 1e-9)
for c, s in P:
    a, b = env(lee(f"{B}/Crudo/{c}.MP4")), env(lee(f"{B}/Grabacion pantalla 1-11-26/{s}.mov"))
    za, zb = (np.clip(a, -60, 0) + 60), (np.clip(b, -60, 0) + 60); za, zb = (za - za.mean()) / za.std(), (zb - zb.mean()) / zb.std()
    n = len(za) + len(zb); cc = np.fft.irfft(np.fft.rfft(zb, n) * np.conj(np.fft.rfft(za, n)), n); i = int(np.argmax(cc)); lag = (i if i < n // 2 else i - n) / 100
    print(f"{c}: pantalla = cámara {lag:+.2f} s")
    huecos = []
    for t in range(0, len(a) // 100):
        j = int((t + lag) * 100)
        if j < 0 or j + 100 > len(b): continue
        vc, vs = np.percentile(a[t * 100:(t + 1) * 100], 90), np.percentile(b[j:j + 100], 90)
        if vs > -38 and vc < vs - 15: huecos.append(t)
    if huecos:
        rangos, ini = [], huecos[0]
        for x, y in zip(huecos, huecos[1:] + [None]):
            if y != x + 1: rangos.append((ini, x + 1)); ini = y
        print("  sin voz en la cámara:", ", ".join(f"{p}-{q}s" for p, q in rangos))
    else: print("  la cámara tiene la voz completa")
