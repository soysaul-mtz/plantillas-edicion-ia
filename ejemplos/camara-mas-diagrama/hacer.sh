#!/bin/zsh
# Arma un reel "Metodología" (cámara arriba + subtítulos serif + pantalla con zoom) de VIDEO DIAGRAMA: hacer.sh diag-7546 [--stills 3,20]
set -e
P=proyectos/$1; PY=.venv/bin/python
cd .
nice python3 estilo-cine/metodo_corte.py $P | tail -2
nice $PY estilo-cine/transcribir.py $P --prompt "Claude, Zernio, Grok, CapCut, Premiere, Edits, Instagram, la empresa del cliente, reels, hooks, bot, DM" | tail -1
nice $PY estilo-cine/preparar.py $P --fuerza 0.75 --suave 1 --color 1 | tail -1
rm -rf ${P:?}/scr && mkdir -p $P/scr && nice ffmpeg -v error -i $P/corte/scr.mov -q:v 3 $P/scr/%05d.jpg
# la pantalla puede acabar unos cuadros antes que la cámara: sin esos cuadros metodo.mjs se queda esperando y deja el mp4 roto
c=$(ls $P/cuadros_pro | wc -l | tr -d ' '); k=$(ls $P/scr | wc -l | tr -d ' '); u=$(printf "$P/scr/%05d.jpg" $k)
while [ $k -lt $c ]; do k=$((k+1)); cp "$u" $(printf "$P/scr/%05d.jpg" $k); done
nice $PY estilo-cine/metodo_zoom.py $P --ancho 1280 | tail -1 && python3 ~/Proyectos/video-diagrama/sin_barras.py $P
shift; nice node estilo-cine/metodo.mjs $P "$@" 2>&1 | tail -2
