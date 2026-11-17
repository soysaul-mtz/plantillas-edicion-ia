#!/bin/zsh
# Descarga los videos de ejemplo de cada plantilla (Google Drive público) a videos-de-ejemplo/<carpeta>/.
# Uso: scripts/bajar_ejemplos.sh           (se puede volver a correr: salta lo que ya está completo)
#      scripts/bajar_ejemplos.sh Saúl       (solo las carpetas que contengan ese texto)
cd "$(dirname "$0")/.."; DEST=videos-de-ejemplo; ok=0; mal=0
tail -n +2 scripts/videos_ejemplo.tsv | while IFS=$'\t' read -r carpeta archivo id bytes; do
  [[ -n "$1" && "$carpeta" != *"$1"* ]] && continue
  mkdir -p "$DEST/$carpeta"; f="$DEST/$carpeta/$archivo"
  if [[ -f "$f" && $(stat -f%z "$f") -eq $bytes ]]; then ok=$((ok+1)); continue; fi
  print "↓ $carpeta / $archivo ($((bytes/1048576)) MB)"
  curl -sL --retry 3 -o "$f.part" "https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t"
  if [[ -f "$f.part" && $(stat -f%z "$f.part") -eq $bytes ]]; then mv "$f.part" "$f"; ok=$((ok+1))
  else print -P "%F{red}✗ no bajó bien: $archivo (vuelve a correr el script)%f"; mv -f "$f.part" "$f.fallo" 2>/dev/null; mal=$((mal+1)); fi
  sleep 1
done
print "\n✓ Videos de ejemplo en $DEST/ · listos: $ok · con error: $mal"
