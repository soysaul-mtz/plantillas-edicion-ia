# Instalación (guía para Claude)

> Si eres Claude Code y te pidieron instalar este sistema: sigue estos pasos en orden, corre los comandos tú mismo,
> y solo detente para lo que necesita a la persona (contraseñas, iniciar sesión, pegar llaves). Al final corre
> `./verificar.sh` y reporta qué quedó y qué falta. Nunca escribas llaves en archivos ni las pidas en el chat:
> se guardan en el Llavero con los scripts indicados (la persona las pega en la terminal, oculta).

**Requisitos:** Mac con chip Apple (M1 o más nuevo), macOS 14 o más nuevo, ~10 GB libres, Claude Code.
Funciona en cualquier Mac Apple Silicon; en 8 GB de RAM usar perfil Redes (el 4K también funciona, solo es más lento).

## 1. Automático
```
./instalar.sh
```
Instala/verifica: herramientas de Apple (swift), Homebrew, ffmpeg, Node, Python 3.13, GitHub CLI, Google Chrome,
el entorno de Python con Whisper local (y baja el modelo, ~1.6 GB), dependencias de Node, compila el recorte de persona
(`bin/segmentar`, usa Vision de macOS), genera efectos de sonido libres, instala las skills en `~/.claude/skills` y
pregunta nombre y @usuario (→ `config/kit.json`).

Si pide contraseña de la Mac (Homebrew) o abre una ventana de "herramientas de línea de comandos": la persona la
completa y se vuelve a correr `./instalar.sh`.
Notas para Claude:
- Homebrew pide la contraseña de la Mac y Claude no puede escribirla: si falta Homebrew, pídele a la persona que corra
  `./instalar.sh` en su Terminal (o `! ./instalar.sh` dentro de Claude Code) y continúa cuando termine.
- Corrido desde Claude (sin terminal interactiva) no pregunta los datos: pregúntale a la persona su nombre y su
  @usuario y crea `config/kit.json` a partir de `config/kit.ejemplo.json`.

## 2. Cuentas (cada quien con la suya; todas opcionales salvo que se use esa función)

### Música y efectos — Epidemic Sound (recomendado)
Sin esto el sistema funciona con efectos sintetizados; para la música basta con darle a Claude una **carpeta** con tus
canciones (el editor elige una distinta por video). Con Epidemic, Claude busca y baja la música él mismo:
1. Con cuenta de Epidemic Sound, conectar su MCP: en claude.ai → Configuración → Conectores → **Epidemic Sound**
   (queda disponible en Claude Code con la misma cuenta). Alternativa en terminal:
   `claude mcp add --transport http epidemic-sound https://www.epidemicsound.com/a/mcp-service/mcp` y autorizar.
2. Pedirle a Claude: *"Descarga los efectos y la música de audio/catalogo.json con mi Epidemic"* (detalle en `audio/LEEME.md`).

### Imágenes con IA — Higgsfield (opcional)
1. `npm i -g @higgsfield/cli` y luego `higgsfield auth login` (la persona inicia sesión en el navegador).
2. Si algún comando responde "No workspace selected", revisar `higgsfield account --help` y seleccionar el workspace de la cuenta.
3. Skills oficiales de Higgsfield (opcional): instalarlas desde el repositorio oficial `github.com/higgsfield-ai` siguiendo
   su README. Regla del sistema: **solo imágenes**, nunca videos salvo que la persona lo pida.

### Voz con IA — ElevenLabs (solo para reels sin cara del `motor/`)
`./motor/clave.sh` (pega la API key, queda en el Llavero). La voz se configura en `config/voz-elevenlabs.json`.

### Diagramas en Miro y Google Drive (opcional)
Conectar en claude.ai → Configuración → Conectores: **Miro** (plantilla Esquema de empresa) y **Google Drive**
(biblioteca de recursos para los DM). La skill `esquemas-miro` explica el flujo.

### Instagram: entregar el recurso por DM cuando comentan la palabra (opcional)
Usa **Zernio** (zernio.com, gratis hasta 2 cuentas): conecta la cuenta de Instagram allí.
1. Guardar la llave: `security add-generic-password -a "$USER" -s zernio-api-key -w` (la pega oculta).
2. `cp instagram/vigilante-recursos/cuenta.ejemplo.json instagram/vigilante-recursos/cuenta.json` y llenar los IDs
   (Claude los puede leer con la API de Zernio: `GET /v1/accounts`, `GET /v1/comment-automations`).
3. Recursos por reel: `instagram/vigilante-recursos/recursos.ejemplo.json` → `recursos.json`.
4. El vigilante corre gratis en **GitHub Actions** (cada 30 min) con el secreto `ZERNIO_API_KEY`; ver su README.
Reglas de Meta aprendidas: 1 solo DM por comentario; a quien no te sigue, mandar texto plano; después del DM de
"sígueme" no se puede mandar otro mensaje por API hasta que la persona escriba o toque el botón.

### GitHub (para recibir actualizaciones)
`gh auth login`. Actualizar el sistema: `git pull && ./instalar.sh`.

## 3. Verificar
```
./verificar.sh
```
Revisa todo y renderiza `proyectos/demo` (17 s, sin cámara). Si sale el video, el sistema está listo.

## 4. Primer video
Abrir Claude Code en esta carpeta y decir, por ejemplo:
*"Edita este video con Saúl Pro: /ruta/al/video.MOV"* → Claude identifica el editor, transcribe y entrega la escaleta.
