"""Sincroniza por LABIOS (cuadro por cuadro): apertura de boca en la cámara (bin/boca, cada 0.04 s) contra el volumen de la voz
en la grabación de pantalla y en el audio de la cámara. Dice el desfase exacto de cada uno respecto al video.
Uso: python sincronia_labios.py   (ventana de 60 s dentro de las frases que se usan)"""
import subprocess, numpy as np, os
B = "<tu disco>/Grabaciones/Casa Nelson/VIDEO DIAGRAMA"; BOCA = os.path.expanduser("./bin/boca")
P = [("FX30-7546", "2026-11-01 23-39-20", 165, 225, 61.67), ("FX30-7547", "2026-11-01 23-46-26", 170, 230, 11.65),
     ("FX30-7548", "2026-11-01 23-53-09", 35, 95, -2.13), ("FX30-7549", "2026-11-01 23-57-10", 149, 209, 14.16)]
PASO = .04
def env(f, ss, dur):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", str(max(0, ss)), "-t", str(dur), "-i", f, "-vn", "-ac", "1", "-ar", "8000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    h = int(8000 * PASO); n = len(x) // h; e = 20 * np.log10(np.sqrt((x[: n * h].reshape(n, h) ** 2).mean(1)) + 1e-9)
    return np.clip(e, -55, 0)
z = lambda v: (v - v.mean()) / (v.std() + 1e-9)
def mejor(m, e, centro_muestras):  # desfase (en muestras) donde la voz sigue mejor a la boca
    best = None
    for d in range(-40, 41):  # ±1.6 s alrededor de lo esperado
        i = centro_muestras + d
        if i < 0 or i + len(m) > len(e): continue
        c = float(np.corrcoef(m, e[i:i + len(m)])[0, 1]); best = max(best or (c, d), (c, d))
    return best
for cam, scr, a, b, lag in P:
    out = subprocess.run([BOCA, f"{B}/Crudo/{cam}.MP4", str(PASO), str(a), str(b)], capture_output=True, text=True).stdout.split("\n")
    m = np.array([float(l.split()[1]) for l in out if l.strip()]); m[m < 0] = np.median(m[m >= 0])
    m = z(np.convolve(m, np.ones(3) / 3, "same"))
    margen = 2.0
    ec = z(env(f"{B}/Crudo/{cam}.MP4", a - margen, b - a + 2 * margen)); es = z(env(f"{B}/Grabacion pantalla 1-11-26/{scr}.mov", a + lag - margen, b - a + 2 * margen))
    c1, d1 = mejor(m, ec, int(margen / PASO)); c2, d2 = mejor(m, es, int(margen / PASO))
    print(f"{cam}: audio de la cámara {d1 * PASO * 1000:+.0f} ms (corr {c1:.2f}) · audio de la pantalla {d2 * PASO * 1000:+.0f} ms vs el desfase por audio (corr {c2:.2f}) → pantalla = cámara {lag + d2 * PASO:+.3f} s")
