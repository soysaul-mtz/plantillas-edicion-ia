# Miro: lo que aprendimos dibujando con Canvas Composer

Léelo antes de mandar el primer SVG a Miro. Son errores reales que ya pasaron.

## Antes de dibujar
- Carga las herramientas de Miro (`canvas_create_from_svg`, `canvas_update_from_svg`, `canvas_read_as_svg`, `board_create`, `board_show`, `image_get_upload_url`, `image_create`) y lee `canvas_get_canvas_composer_skill` (pasos `design` y `dsl`) la primera vez en la sesión.
- Pregunta en qué tablero dibujar. Crear un tablero nuevo requiere confirmación del usuario.
- Dibuja en una zona libre: `"origen_x"` en el spec mueve todo el esquema (ej. 15000 para ponerlo a la derecha de lo que ya existe).

## Texto
- Usa siempre `textArea` con `width` explícito. Los `<text>` sueltos se convierten en textArea con un ancho estimado y a veces se parten en dos líneas.
- No metas `<b>` ni `<br>` dentro de un textArea: Miro los guarda raros y el texto puede salir con etiquetas visibles o todo en negritas. Un párrafo = un textArea sin etiquetas. Si necesitas negritas, pon el textArea entero en `font-weight="bold"`.
- Texto dentro de una forma (barra, chip, tarjeta de un solo texto): `data-content` en la forma, no un texto encima.
- Después de crear, revisa `data-rendered-bounds` y las alturas: si un texto de una línea sale con el doble de alto, se partió. Corrígelo con `canvas_update_from_svg` (más ancho o letra más chica).

## Orden (z-order)
- Lo que se crea después queda encima. Las líneas punteadas van primero (debajo). El asterisco de Claude va **después** del banner lila, si no queda tapado. `generar.py` ya lo hace bien.
- `canvas_update_from_svg` no cambia el orden de lo existente: para traer algo al frente hay que crearlo de nuevo.

## Imágenes
- Subir: `image_get_upload_url` (con x, y, width) → `curl -X PUT -H 'Content-Type: image/png' --data-binary @archivo.png '<upload_url>'` → `image_create` con el token.
- En `image_get_upload_url`/`image_create` las coordenadas son del **centro** de la imagen; en el SVG son de la esquina superior izquierda.
- Para poner una captura encima de una tarjeta, hazla con la misma proporción que la tarjeta (`empaquetar.py` ya lo hace) y céntrala en la tarjeta.
- Capturas de perfiles públicos de Instagram: `https://www.instagram.com/<usuario>/embed/` con Chrome sin pantalla (`--window-size=900,540`).

## Actualizar y borrar
- Para editar: el `data-miro-id` que devolvió el último `result_svg` + solo los atributos que cambian.
- Borrar es irreversible: confirma con el usuario antes de mandar `data-deleted="true"` (salvo algo que acabas de crear por error, y avísale).
- Si la respuesta es enorme, Miro la guarda en un archivo: léela con `jq` (`.success`, `.created_count`, `.result_svg`).

## Lo que no se puede
- No puedes ver el tablero renderizado: la vista previa de Miro solo devuelve un widget suelto. Comprueba con medidas y, para documentos, haz la imagen con `capturar.py` (réplica con los mismos datos, fuente parecida). Díselo al usuario con claridad.
