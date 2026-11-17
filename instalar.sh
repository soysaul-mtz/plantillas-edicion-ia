#!/bin/zsh
# Instalador del sistema de edición. Uso: ./instalar.sh   (se puede correr varias veces; solo instala lo que falte)
# Requisitos: Mac con chip Apple (M1 o más nuevo), macOS 14+. Para lo que necesita tu cuenta (llaves, conexiones),
# sigue INSTALAR.md o pídele a Claude: "instala el sistema siguiendo INSTALAR.md".
set -e
KIT="$(cd "$(dirname "$0")" && pwd)"
cd "$KIT"
ok()   { print -P "%F{green}✓%f $1"; }
paso() { print -P "\n%F{cyan}▸ $1%f"; }
aviso(){ print -P "%F{yellow}⚠ $1%f"; }

[[ "$(uname -m)" == "arm64" ]] || { aviso "Esta Mac no es Apple Silicon: Whisper (mlx) y el recorte con Vision no van a funcionar."; }

paso "1/9 Herramientas de línea de comandos de Apple (swift)"
if xcode-select -p >/dev/null 2>&1; then ok "ya instaladas"; else xcode-select --install || true; aviso "Termina la instalación que se abrió y vuelve a correr ./instalar.sh"; exit 1; fi

paso "2/9 Homebrew"
if ! command -v brew >/dev/null; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi
ok "brew $(brew --version | head -1 | awk '{print $2}')"

paso "3/9 Programas: ffmpeg, Node, Python, GitHub CLI"
for p in ffmpeg ffmpeg-full node python@3.13 gh; do brew list --formula "$p" >/dev/null 2>&1 || brew install "$p"; done
ok "ffmpeg $(ffmpeg -version | head -1 | awk '{print $3}') · node $(node -v) · $(/opt/homebrew/bin/python3.13 --version)"

paso "4/9 Google Chrome (el motor renderiza con Chrome)"
if [[ -d "/Applications/Google Chrome.app" ]]; then ok "ya instalado"; else brew install --cask google-chrome; fi

paso "5/9 Entorno de Python (.venv) + Whisper local"
[[ -d .venv ]] || /opt/homebrew/bin/python3.13 -m venv .venv
.venv/bin/pip install -q --upgrade pip
.venv/bin/pip install -q -r requirements.txt
ok "paquetes de Python listos"
print "   bajando el modelo de Whisper (≈1.6 GB, solo la primera vez)…"
.venv/bin/python -c "from huggingface_hub import snapshot_download as d; d('mlx-community/whisper-large-v3-turbo')" >/dev/null 2>&1 && ok "modelo Whisper listo" || aviso "no se pudo bajar el modelo ahora; se baja solo la primera vez que transcribas"

paso "6/9 Dependencias de Node (motores de render)"
for d in motor editor-anuncios editor-testimoniales/editor skills/render-webpage; do
  [[ -f "$d/package.json" ]] && (cd "$d" && npm install --silent --no-audit --no-fund >/dev/null) && ok "$d"
done

paso "7/9 Recorte de persona con Vision (bin/segmentar)"
mkdir -p bin
swiftc -O estilo-cine/segmentar.swift -o bin/segmentar 2>/dev/null && ok "bin/segmentar compilado"
# editor de testimoniales/anuncios: cara en cada fotograma (bin/caras), HDR → Rec.709 (bin/sdr) y su entorno de Python
T=editor-testimoniales/editor; mkdir -p $T/bin
swiftc -O $T/caras.swift -o $T/bin/caras 2>/dev/null && ok "$T/bin/caras compilado"
swiftc -O $T/sdr.swift -o $T/bin/sdr 2>/dev/null && ok "$T/bin/sdr compilado"
swiftc -O $T/fotogramas.swift -o $T/bin/fotogramas 2>/dev/null && ok "$T/bin/fotogramas compilado (revisión final cuadro por cuadro)"
[[ -e $T/.venv ]] || ln -s ../../.venv $T/.venv

paso "8/9 Efectos de sonido básicos (libres de derechos)"
.venv/bin/python audio/efectos_basicos.py >/dev/null && ok "estilo-cine/sfx (reemplázalos por los de Epidemic si tienes cuenta: audio/LEEME.md)"
W=editor-testimoniales/editor/sfx/whoosh.wav; mkdir -p ${W:h}
[[ -f $W ]] || ffmpeg -v error -y -i estilo-cine/sfx/whoosh_rapido.mp3 $W || aviso "no pude crear $W (la mezcla sigue sin whoosh)"

SK="${SKILLS_DIR:-$HOME/.claude/skills}"   # SKILLS_DIR para probar sin tocar tus skills
paso "9/9 Skills de Claude Code ($SK)"
mkdir -p "$SK"
for s in skills/*/; do
  n=$(basename "$s"); rm -rf "$SK/$n"; cp -R "$s" "$SK/$n"
  # las rutas de las skills son relativas al repositorio: se anota dónde quedó instalado
  print "\n> Repositorio del sistema de edición: \`$KIT\` (todas las rutas relativas de esta skill son relativas a esa carpeta)." >> "$SK/$n/SKILL.md"
  [[ -f "$SK/$n/package.json" && ! -d "$SK/$n/node_modules" ]] && (cd "$SK/$n" && npm install --silent --no-audit --no-fund >/dev/null)
  ok "skill $n"
done

if [[ ! -f config/kit.json && -t 0 ]]; then
  paso "Tus datos (para los videos)"
  read "nom?Tu nombre como sale en los videos: "; read "han?Tu usuario de Instagram (con @): "
  cat > config/kit.json <<EOF
{ "nombre": "${nom:-Tu nombre}", "handle": "${han:-@tu_usuario}", "carpeta_contenido": "", "idioma": "es", "perfil_salida_por_defecto": "redes" }
EOF
  ok "config/kit.json"
fi

print -P "\n%F{green}Listo.%f Sigue con: ./verificar.sh   y luego los pasos de cuenta en INSTALAR.md (Higgsfield, ElevenLabs, Epidemic, Zernio)."
