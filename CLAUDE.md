# Sistema de edición de video con IA · instrucciones para Claude

Este repositorio es un sistema completo para editar reels verticales con Claude Code: corte de tomas, subtítulos
palabra por palabra, filtro de piel, gráficos y escenas 3D hechos con código, interfaces de herramientas emuladas,
render en 1080 o 4K y entrega por DM en Instagram. Lo construyó Saúl Martínez (creador de contenido) con Claude, video
por video, y aquí quedan sus plantillas y todas las reglas que fue corrigiendo.

Si el sistema no está instalado (falta `.venv`, `bin/segmentar` o `config/kit.json`), sigue **INSTALAR.md** antes de nada.
Los datos de la persona (nombre, @usuario, carpeta de videos) están en `config/kit.json`: úsalos en cada `cine.json`
(`"nombre"`, `"handle"`).

## Instalación (con el mensaje de su link personal de compra)
1. Corre `scripts/requisitos.sh`. Por cada ✗ imprime un comando: **enséñaselo y pídele permiso** antes de correrlo (Homebrew pide la contraseña de la Mac en la Terminal, nunca en el chat). Repite hasta «Todo listo».
2. Si falta `config/kit.json`, pregúntale su nombre y su usuario de Instagram y créalo (formato en INSTALAR.md).
3. **Prueba:** `node estilo-cine/render.mjs proyectos/demo` → `proyectos/demo/salida/cine_codigo.mp4`; dile dónde quedó.

## Qué hay aquí
| Carpeta | Para qué |
|---|---|
| `estilo-cine/` | **Motor principal** (plantillas Saúl Pro y Saúl Pro 3D): `cine.js` (escenas, texto, 3D, interfaces), `render.mjs`, `metodo_corte.py`, `transcribir.py`, `quitar_tramos.py`, `preparar.py`, `piel.py`, `prep4k.py`, formatos de reacción (`reac_*.py`), doble pantalla (`doble.mjs`), tutorial cámara+pantalla (`metodo*.{py,mjs}`). Ver su README. |
| `plantillas/` | Fichas de cada estilo: `saul-pro-3d/` (receta + `cine_base.json`), `formatos/editor-NN/ESTILO.md` (51 estilos analizados: "Editor 1…50" + "Dani Pro", agrupados en 26 familias, índice en `formatos/README.md`), `esquema-de-empresa/` (diagramas en Miro), `CATALOGO.md`. |
| `editores/` | Catálogo de editores + `identificar.py` (decide qué editor le toca a un video). |
| `editor-anuncios/` | Editor de anuncios con retomas (prepare → build → cues → render): zoom con cara, subtítulos, transiciones. |
| `editor-testimoniales/` | Editor de testimoniales y anuncios a cámara (horizontal o vertical): `editor/editar.py <proyecto> plan → armar → terminar`, con todas las revisiones automáticas. Ver su README. |
| `editor-cursos/` | **Cursos y clases largas horizontales** (cámara + pantalla, 30 min–2 h por archivo) → un video por capítulo, sin retomas ni plática de grabación, subtítulos solo a cámara, voz limpia. `armar.py capNN.json`. Lee su README, `GUIA_CORTES.md` y `GUIA_PULIDO.md`. |
| `editor-vsl-animado/` | **VSL animado 3D**: la voz real sobre ~190 animaciones 3D/gráficos hechos con código y subtítulos al centro palabra por palabra. Escaleta → stills → render. Ver su README. |
| `editor-vertical/` | Pasar videos horizontales (crudos o ya editados) a **vertical** sin zooms: reencuadre a la cara por cuadro, paneles si hay texto quemado, subtítulos. |
| `editor-testimoniales/EDITOR51.md` | **Editor 51**: persona + imágenes editoriales a pantalla completa cada 2–4 s (`imagenes51.py`, también horizontal). |
| `ejemplos/` | Proyectos reales terminados para copiar la forma de trabajar: doble pantalla con 3D, cámara + diagrama, anuncios en Saúl Pro. Sus rutas a crudos dicen `<tu disco>`: cámbialas. |
| `motor/` + `video` | Motor de reels sin cara con voz de ElevenLabs (`./video nuevo|voz|render|logo|transcribir`). Ver `docs/motor-tutoriales.md`. |
| `lead-magnets/` | Generador de la lista de herramientas en PDF (`datos.json → generar.py → exportar.mjs`) y la guía "Edita tus videos con Claude". |
| `instagram/` | Entrega automática por DM con Zernio: `vigilante-recursos/` (reintentos, corre en GitHub Actions) y `esperar_reel.py` (copia la automatización al siguiente reel). |
| `audio/` | Catálogo de música/efectos de Epidemic y generador de efectos libres. |
| `skills/` | Skills de Claude Code que instala `instalar.sh` en `~/.claude/skills`. |

## Antes de editar: preguntar (una sola vez, todo junto)
- **Música:** ¿una carpeta con canciones o un MCP de música conectado (p. ej. Epidemic Sound)? Sin música no se entrega, salvo que diga "sin música".
- **Duración máxima** del video: con eso se decide qué partes entran y cuáles no.
- **Formato:** Redes 1080 (por defecto) o 4K.
- **Nombres propios** que Whisper escribe mal (personas, marcas).

## Flujo de trabajo (no saltarse pasos)
1. **Identificar el editor:** `.venv/bin/python editores/identificar.py "<video>"`. Si la persona nombra una plantilla ("Saúl Pro", "Saúl Pro 3D", "Editor 12"…), manda eso.
2. **Transcribir y buscar retomas:** `transcribir.py --tramos`. Whisper de corrido FUSIONA frases repetidas: confirma cada sospecha con la energía del audio (pasos de 10–100 ms) y transcribiendo clips cortos. Separa la voz de la persona (−11 a −23 dB) del audio que suena de fondo en una bocina o celular (−25 a −45 dB): nunca usar esos tramos.
3. **Mostrar el PLAN TAL CUAL a la persona y no editar nada** hasta que diga "sí". Empezar con: "Esto es lo que voy a hacer con tu video, paso a paso. Revísalo y dime si algo está mal antes de que lo arme." El plan lleva: qué partes se usan (tiempo · qué dice · qué se ve · animación · texto en pantalla), retomas que se quitan, duración contra el máximo, música, cada paso de la edición y una lista de **posibles errores** que la persona debe revisar (voz que podría ser de otra persona, palabras que podrían quedar cortadas, licencia de música…). En el editor de testimoniales lo genera `editar.py <p> plan` (PLAN.md). Corregir fila por fila.
4. **Cortar** (`metodo_corte.py` o un `corte.py` del proyecto con ffmpeg), **preparar** (`preparar.py`), armar `cine.json`.
5. **Revisar con stills** (`render.mjs --stills`) con la zona segura encima (`estilo-cine/zona_segura.png`) antes del render completo.
6. **Render** y **verificar**: transcribir el audio final por tramos (con música encima Whisper inventa cosas como "Suscríbete": compara contra la energía), medir volumen (−14 LUFS), ver una hoja de cuadros. Guardar en la misma carpeta del video como `Video editado - <nombre>.mp4` y abrirle la carpeta.
7. **Revisión final cuadro por cuadro (siempre, con cualquier editor):** con el video TERMINADO corre
   `editor-testimoniales/editor/.venv/bin/python editor-testimoniales/editor/revisar_final.py <carpeta_del_proyecto> "<video final>"`.
   Lee con Vision todos los fotogramas (cara y texto real en pantalla) y busca texto sobre la cara, fuera de la zona segura,
   subtítulos que no se ven, destellos de un cuadro, cuadros negros, imagen congelada y audio que satura; deja hojas de
   contacto en `<carpeta>/revision_final/` con marco rojo en los cuadros con problema. **Abre y mira las hojas** antes de entregar.
   En el editor de testimoniales ya viene dentro de `editar.py … terminar` (y solo entrega si todo pasó).
8. Si algo no se pudo verificar (por ejemplo, no se vio de corrido), decirlo.

## Reglas de corte y audio (en TODOS los editores)
- **Palabras cortadas: doble revisión siempre.** Cada inicio y final se lleva al silencio real; cada corte se transcribe exacto y otra vez con medio segundo de más (si cambia la primera o la última palabra, el corte se la come). Al final, transcribir cada unión del video armado con el audio limpio (sin música).
- **Pausas:** ninguna de más de ~0.35 s dentro de una frase (salvo silencios a propósito que la persona quiera).
- **Voz pareja:** nivelar el volumen de cada corte antes de unirlos (que no brinque entre tomas o clips) y dejar el final a −14 LUFS.
- **Voz de otra persona:** el director o quien dicta fuera de cámara suena ~6 dB más bajo: nunca usar esos tramos.
- **Final sin congelar:** el fundido empieza justo cuando la persona termina de hablar (o un poco antes) sobre imagen real; nunca un cuadro congelado.
- **Cambios de escena y tomas de stock:** ninguna toma cruza un cambio de plano del stock (se ve un destello); no dejar rebanadas de 2–4 cuadros de la persona entre una toma y un corte; transición visible en cada corte.
- **Video HDR (HLG/PQ, p. ej. DJI):** convertir a Rec.709 antes de editar o se ve lavado.

## Cómo se llegó a casi cero errores (checklist que se cumple en CADA video)
Cada punto salió de un error real que la persona vio. No te saltes ninguno.
1. **Plan antes de tocar nada** y la persona dice "sí". Sin plan aprobado no se renderiza.
2. **Stills antes del render completo** (6–10 tiempos: cortes, tomas de apoyo, CTA, cada sección). Míralos con Read.
3. **Revisión final cuadro por cuadro** (`revisar_final.py`) y abrir las hojas `revision_final/hoja_*.jpg`. Solo se entrega si todo pasó.
4. **Transcribir el audio final por uniones** con el audio limpio: así se cazan palabras comidas ("tecnología", "internet") y voces del director.
5. **Arranque:** la voz empieza ≤ 0.15 s después del primer cuadro. **Uniones sin tiempo muerto:** `aire_corte` 0.04, `umbral_bordes_db` −44, `pausa_max` 0.25, transición corta (0.14 s); respiraciones y chasquidos no cuentan como voz.
6. **Color medido en la piel** (`editor/color.py`, no en la pared; verde ≤ 1.02). DJI suele salir azul/magenta. **iPhone en HLG/HDR:** `bin/sdr` antes de editar y SIN corrección de color ni velo claro (se ve lavado).
7. **Filtro de piel suave:** `piel.py --fuerza 0.45 --suave 0.8 --ojeras 0.4` (difuminar ojeras, nunca borrarlas).
8. **Nombres bien escritos** en subtítulos: Whisper escribe "Cloud" por Claude, "conía" por "con IA", "Grok Bot" va en dos palabras. Usa `vocabulario`/`equivalentes` y revisa cada nombre propio; si no se puede confirmar uno, pregúntalo, no lo inventes.
9. **Subtítulo de menos de 0.5–0.9 s no se ve:** únelo con la frase siguiente.
10. **Tomas de apoyo (stock) sin destellos:** nada de 1–2 cuadros de la persona entre tomas (`stock_encima.py`), ninguna cara bajo el texto (`stock_caras.py`), no repetir el mismo plano pegado.
11. **Renders largos en Chrome:** recargar la página cada 2500–3000 cuadros (después de ~12 000 da capturas en blanco y los subtítulos desaparecen).
12. **Three.js:** si cambias `material.transparent` después del primer render pon `material.needsUpdate = true`; prueba colores contra el fondo con stills.
13. **Un proceso pesado a la vez** (render, Whisper) y con `nice`: la persona usa la compu mientras tanto.
14. **Nunca sobrescribir un video ya entregado:** versión nueva con otro nombre o respaldo en `_antes_*`.
15. **Cursos:** sin música, sin zooms ni avance rápido, subtítulos solo a cámara completa, quitar retomas y plática de grabación, y **no censurar de más** (solo lo que la persona pide; pregunta antes de tapar).
16. **Música:** de Epidemic (MCP) o la carpeta que den; una canción distinta por video; voz ≥ 8 dB arriba; final a −14 LUFS (cursos −16).
17. Al entregar di dónde quedó, duración, volumen, qué se revisó solo y qué quedó pendiente de confirmar.

## Reglas de estilo que ya se aprendieron (respetarlas siempre)
- **Fondo real.** No recortar a la persona ni cambiarle el fondo salvo que lo pida: "se ve chafa". Tampoco poner logos u objetos DETRÁS de la persona con su silueta (el borde del recorte se nota). Tampoco bajarla en el cuadro. El recorte (máscara) solo sirve para meter texto gigante entre el fondo y la persona.
- **Filtro de piel sutil**: `piel.py` con valores por defecto. Subirlo se ve "demasiado filtro". Cuidar que no se vea verde (no usar `eq=saturation` ni grano en canales de color). Si la toma se ve muy naranja/cálida: `colorbalance` hacia azul y `piel.py --color 0.5`.
- **Arrancar justo cuando empieza a hablar.** Sin silencios ni miradas al celular a cuadro. Pausas largas dentro de una frase se recortan.
- **Zona segura de Instagram** (video 1080x1920): nada importante con y < 262, y > 1540, ni x > 900 desde y > 700; 42 px de margen a cada lado. Aplica a subtítulos, flechas y gráficos; revisarlo con medidas, no a ojo.
- **Nada encima de la cara:** detectar la cara en TODOS los fotogramas antes de colocar textos o gráficos (en el editor de testimoniales: `bin/caras` + `revisar_texto.py`). Si un subtítulo no cabe, partirlo en dos antes que taparla.
- **Subtítulos cortos:** ninguno dura menos de ~0.9 s en pantalla; si es más corto, aparece antes o se une al siguiente (si no, no se alcanza a ver).
- **Subtítulos** palabra por palabra (línea chica + palabra grande, `*` resalte, `~` contorno). Blancos con sombra si la ropa o el fondo son oscuros (`"textoTema": "oscuro"`); texto "detrás" de la cabeza oscuro sobre pared clara.
- **Cuando menciona una herramienta**, mostrar su interfaz emulada con código (basada en capturas reales) a **pantalla completa**, con interacción (escribir, clic, generar). En escenas de interfaz no poner `cortes` (meten barridos dentro de la UI).
- **Listas de herramientas**: la columna va del lado al que la persona SEÑALA (revisar cuadro por cuadro sus gestos). Solo poner lo que la persona dice.
- **Zoom**: el empuje lento tiene tope (+5 %) y se reinicia en cada corte o escena; nada de acercamientos acumulados.
- **Ritmo**: animaciones encadenadas, sin tiempo muerto (< 5 % del video quieto, pausas ≤ 0.3 s); transición visible en cada corte; nada encima de la cara.
- **Música**: de la carpeta o el MCP que dio la persona; una canción distinta por video, que se escuche desde el segundo 0 (sin intro suave); baja cuando hablan (voz ≥ 8 dB por encima). Los efectos no deben pisar la última sílaba de una frase. Recordarle confirmar que su licencia cubra anuncios pagados si es para un cliente.
- **Imágenes con IA (Higgsfield)**: solo imágenes, nunca videos (son caros) salvo que lo pidan. Animar con código.
- **Referencias de otros creadores** son guía de look, no para copiar su contenido; cuando la persona pide "cópialo literal", replicar estructura y estilo con sus propios textos y marca.
- **CTA**: tarjeta de comentario con la palabra clave + notificación de DM al final (`cta`, `dm`).

## Plantillas con nombre
- **Saúl Pro**: reel estilo cine con la persona y su fondo real, texto palabra por palabra, escenas 3D, textura de película.
- **Saúl Pro 3D**: Saúl Pro + ventana "Top N" naranja con candados, un bloque 3D por herramienta (sube, se enciende, gira) e interfaz de cada herramienta a pantalla completa. Receta: `plantillas/saul-pro-3d/ESTILO.md`.
- **Formatos**: reacción (original arriba, persona abajo, sin música), original vs editado (doble pantalla), metodología (cámara + pantalla con zoom al cursor), lista de herramientas (título amarillo + columna de logos).
- **Formatos (61)**: Editor 1–50, Dani Pro y 10 "Editor N · pantalla" (el video que corre dentro de la laptop en los formatos de Pantalla Filmada). **Cada uno tiene `plantillas/formatos/<carpeta>/GUIA.md`, escrita para ti: qué es y cómo hacerlo paso a paso.** Para elegir o cuando nombren uno ("hazlo como el Editor 26"), abre primero `plantillas/formatos/GUIA-FORMATOS.md`.
  Cada formato trae su `hoja.jpg` y `cuadros/` (referencia visual) cuando la persona descomprimió el zip **"Referencias de formatos (para Claude)"** de su link personal; si faltan, pídeselo y descomprímelo encima del sistema (`unzip -o -q "<zip>" -d <raíz>`) antes de editar.

## Calidad de salida: Redes (1080) o 4K
Por defecto **Redes**. Solo si la persona pide 4K: editar todo en la copia de 1080 y al final `prep4k.py` + `render.mjs --perfil 4k`
(por bloques, HEVC por hardware, prioridad baja: no traba la compu). Si la cámara no es 4K, avisar que saldrá escalado.

## Seguridad
- Las llaves (ElevenLabs, Zernio, Higgsfield) viven en el **Llavero de macOS**, nunca en archivos ni en el chat.
- Nunca publicar ni mandar mensajes por Instagram sin que la persona confirme.
- Antes de compartir algo de este repositorio, no meter videos, cuadros con caras, llaves ni material con licencia (Epidemic).
