"""Corta las tomas buenas del crudo 4K, las baja a 1920x1080 y las une (fundido de 10 ms en el audio de cada unión).

Uso:  python3 armar_corte.py <video: 7544|7545>   → <video>/corte.mp4 + <video>/cortes.json (fronteras en el armado)
"""
import sys, os, json, subprocess

CRUDO = "<tu disco>/Grabaciones/Casa Nelson/EJEMPLO DE IA/Crudos/FX30-{}.MP4"
TOMAS = {"7545": [(0.92, 3.75), (4.56, 7.35), (7.99, 17.42), (46.42, 55.45)],
         "7544": [(21.95, 28.40), (46.20, 54.00), (68.95, 71.35), (101.85, 109.40)]}
v = sys.argv[1]; T = TOMAS[v]; out = os.path.join(os.path.dirname(os.path.abspath(__file__)), v); os.makedirs(out, exist_ok=True)
fc, F = [], .01
for k, (a, b) in enumerate(T):
    fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,scale=1920:1080:flags=lanczos[v{k}]")
    fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d={F},afade=t=out:st={b - a - F:.3f}:d={F}[a{k}]")
fc.append("".join(f"[v{k}][a{k}]" for k in range(len(T))) + f"concat=n={len(T)}:v=1:a=1[v][a]")
subprocess.run(["nice", "-n", "10", "ffmpeg", "-v", "error", "-y", "-i", CRUDO.format(v), "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", os.path.join(out, "corte.mp4")], check=True)
fr, t = [], 0
for a, b in T: t += b - a; fr.append(round(t, 3))
json.dump({"tomas": T, "fronteras": fr}, open(os.path.join(out, "cortes.json"), "w"))
print(f"✓ {v}/corte.mp4  {t:.2f} s · fronteras {fr}")
