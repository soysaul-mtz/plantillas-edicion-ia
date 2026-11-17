"""Compara la calidad de voz de cada toma de cámara vs su grabación de pantalla (SNR y brillo de la voz)."""
import subprocess, numpy as np
B = "<tu disco>/Grabaciones/Casa Nelson/VIDEO DIAGRAMA"
P = [("FX30-7546", "2026-11-01 23-39-20"), ("FX30-7547", "2026-11-01 23-46-26"), ("FX30-7548", "2026-11-01 23-53-09"), ("FX30-7549", "2026-11-01 23-57-10")]
def mide(f):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    h = 800; e = np.array([np.sqrt((x[k:k + h] ** 2).mean()) + 1e-9 for k in range(0, len(x) - h, h)]); db = 20 * np.log10(e)
    voz, piso = np.percentile(db, 95), np.percentile(db, 10)
    seg = x[: len(x) // 1024 * 1024].reshape(-1, 1024); S = np.abs(np.fft.rfft(seg * np.hanning(1024), axis=1)) ** 2
    act = S.sum(1) > np.percentile(S.sum(1), 70); fr = np.fft.rfftfreq(1024, 1 / 16000)
    agudos = S[act][:, fr > 3000].sum() / S[act].sum()
    return voz, piso, agudos
for c, s in P:
    for nom, f in ((c, f"{B}/Crudo/{c}.MP4"), (s, f"{B}/Grabacion pantalla 1-11-26/{s}.mov")):
        v, p, a = mide(f); print(f"{nom:22s} voz {v:6.1f} dB  ruido {p:6.1f} dB  SNR {v - p:5.1f}  agudos {a * 100:4.1f}%")
