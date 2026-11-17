#!/usr/bin/env python3
"""Descarga un video de Instagram (reel o post público) a una carpeta.

Uso:  python3 descargar.py <link> [carpeta]     (por defecto la carpeta es entrada/)
"""
import pathlib
import shutil
import subprocess
import sys


def main():
    if len(sys.argv) < 2:
        sys.exit("Uso: python3 descargar.py <link> [carpeta]")
    link = sys.argv[1].split("?")[0]  # quita los parámetros de seguimiento
    carpeta = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "entrada")
    carpeta.mkdir(parents=True, exist_ok=True)
    if not shutil.which("yt-dlp"):
        sys.exit("Falta yt-dlp. Instálalo y vuelve a intentar (Mac: brew install yt-dlp).")
    cmd = [
        "yt-dlp", "--no-playlist",
        "-f", "bv*[vcodec^=avc1]+ba/b",       # prefiere H.264: lo leen todos los programas
        "--merge-output-format", "mp4",
        "-o", str(carpeta / "%(id)s.%(ext)s"),
        "--print", "after_move:filepath",
        link,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("No se pudo descargar:\n" + r.stderr.strip()[-600:])
    print(r.stdout.strip().splitlines()[-1])  # ruta del video descargado


main()
