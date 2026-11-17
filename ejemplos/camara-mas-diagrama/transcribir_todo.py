"""Transcribe (palabra por palabra) las tomas de cámara y las grabaciones de pantalla de VIDEO DIAGRAMA → crudos/<nombre>.json"""
import os, sys, json, subprocess, glob
import mlx_whisper as m
BASE = "<tu disco>/Grabaciones/Casa Nelson/VIDEO DIAGRAMA"
fs = [f"{BASE}/Crudo/FX30-75{n}.MP4" for n in (46, 47, 48, 49)] + sorted(glob.glob(f"{BASE}/Grabacion pantalla 1-11-26/2026*.mov"))
out = os.path.expanduser("~/Proyectos/video-diagrama/crudos")
for f in fs:
    nom = os.path.splitext(os.path.basename(f))[0]; j = f"{out}/{nom}.json"
    if os.path.exists(j): continue
    wav = f"{out}/{nom}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    r = m.transcribe(wav, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="es", word_timestamps=True)
    json.dump(r, open(j, "w"), ensure_ascii=False)
    print(nom, len(r["segments"]), "segmentos", flush=True)
