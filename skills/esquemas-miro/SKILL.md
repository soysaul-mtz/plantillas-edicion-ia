---
name: esquemas-miro
description: Crea esquemas paso a paso en Miro con plantillas de estilo guardadas (la principal es "Esquema de empresa", un organigrama con banner lila, áreas numeradas, mascotas y tarjetas TÚ/CLAUDE), más la guía HTML con el prompt, el PDF, la captura puesta en Miro y la imagen agregada a un Word de plantillas. Úsala siempre que el usuario pida un esquema, organigrama, diagrama de sistema o "explicación paso a paso" en Miro, quiera explicar un sistema o un guion de video con un tablero, mencione "Esquema de empresa" o "plantillas de Miro", pida la guía/PDF de un prompt para un reel, o quiera guardar un estilo nuevo de esquema como plantilla, aunque no nombre la skill.
---

# Esquemas en Miro con plantillas

Sirve para convertir un sistema o un guion de video en un tablero de Miro que se entiende en 3 segundos, y empaquetarlo como guía con el prompt exacto (para el CTA "comenta la palabra X"). El estilo sale de los reels de @mate.jimenez sobre Claude + Miro, adaptado por Saúl Martínez: es guía de look, no se copia contenido.

## Qué necesitas
- Conector de **Miro** activo en Claude (herramientas `canvas_*`, `board_*`, `image_*`).
- **Python 3** con `pillow` y `python-docx` (`pip install pillow python-docx`) y **Google Chrome** (para PDF y capturas). En otra ruta de Chrome: variable `CHROME`.
- Lee `references/miro-lecciones.md` antes del primer dibujo de la sesión: ahorra los errores que ya cometimos.

## Plantillas disponibles
Ver `references/catalogo.md`. Por defecto usa **Esquema de empresa** (`references/estilo-esquema-de-empresa.md`).

## Flujo (en este orden; cada paso espera el visto bueno del usuario)

1. **Entender el guion o sistema.** Saca los pasos y quién hace qué. Si hay un reel de referencia, descárgalo (`yt-dlp`), transcríbelo y saca fotogramas: copia la estructura, no el contenido.
2. **Escribir el spec.** Copia `assets/ejemplo-edita-videos.json` y cambia los textos:
   - `titulo1` (línea 1 del banner) y `titulo2` (casi siempre "Automáticamente con"; el script agrega "✱ Claude").
   - `barra`: 3 ideas cortas separadas por `     |     `.
   - `dueno` y `jefe`: barra + texto de la tarjeta. `laterales` (0 a 2): tarjetas a los lados del jefe, p. ej. "El link…" y "El prompt exacto".
   - `areas`: 3 a 5 áreas `"1 · Nombre"`, cada una con `descripcion` y 1 a 3 `agentes` (`nombre`, `quien`: `tu` o `cl`, `texto` ≤ 140 caracteres).
   - `cierre`: CTA o ciclo de retroalimentación. `origen_x`: dónde ponerlo en el tablero.
3. **Dibujar en Miro.** `python3 scripts/generar.py spec.json esquema.svg` → manda el SVG con `canvas_create_from_svg`. Revisa medidas en la respuesta y corrige lo que se parta. Muéstralo con `board_show`.
4. **Guía local con el prompt.** Copia `assets/guia-plantilla/` a la carpeta del proyecto y cambia textos: banner, "Cómo funciona", "Lo que necesitas", el prompt (en `<pre id="p1">`, escapando `<` y `>` como `&lt;` `&gt;`) y "Lo que recibes". Ábrela en el navegador. El prompt se entrega aquí, no se guarda en otras conversaciones.
5. **Solo cuando el usuario confirme:** `python3 scripts/empaquetar.py <carpeta de la guía> [ancho alto de la tarjeta]` → PDF + `captura-completa.png` + `captura-bloques.png`. Sube `captura-bloques.png` a Miro encima de la tarjeta del prompt (ver "Imágenes" en `references/miro-lecciones.md`).
6. **Word de plantillas.** Haz la imagen del esquema con `python3 scripts/capturar.py spec.json esquema.png` y agrégala al documento maestro con `python3 scripts/agregar_a_word.py "<ruta.docx>" "<Nombre>" esquema.png "<leyenda>"` (el Word debe estar cerrado; el script se niega si está abierto). Pregunta la ruta del Word la primera vez. Para verificar cómo se ve: `qlmanage -t -s 1400 -o <carpeta> <archivo.docx>`.

## Guardar un estilo nuevo
Cuando el usuario pase otra plantilla ("guárdala como plantilla"), sigue `references/catalogo.md`: destila el estilo en `estilo-<nombre>.md` + `plantilla-<nombre>.json`, agrégala al catálogo y su imagen al Word.

## Cómo comunicarlo
- Di qué hiciste en Miro y qué no pudiste comprobar (no se puede ver el tablero renderizado; solo medidas).
- Si agregas algo que no estaba en el guion (un paso, una aclaración), dilo y ofrece quitarlo.
- Sé honesto con lo técnico del prompt: si el sistema necesita Claude Code o herramientas instaladas, escríbelo en la guía.
