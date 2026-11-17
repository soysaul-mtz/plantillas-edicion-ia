# Plantilla de estilo · Esquema de empresa

**Para qué sirve.** Explicar un sistema paso a paso como si fuera el organigrama de una empresa: quién manda, qué áreas hay y qué hace cada agente. Se usa para grabar un reel con el tablero de Miro y para entregar una guía con el prompt exacto.

**Origen.** Sale de los reels de Mateo Jiménez (@mate.jimenez) sobre Claude y Miro, adaptado por Saúl (oct 2026). Es guía de estilo y de estructura, no se copia su contenido.

## Cómo se ve
- **Banner lila** (#DDE1F9) con el título gigante en azul marino. Línea 1 en negritas; línea 2 dice "Automáticamente con ✱ Claude" (asterisco terracota dibujado con 6 líneas, "Claude" en serif).
- **Barra negra** debajo con 3 ideas cortas separadas por `|`.
- **Nivel 1 · Dueño: Tú** (barra negra + tarjeta rosa con borde terracota). **Nivel 2 · Claude, jefe** (barra negra + tarjeta blanca).
- **Tarjetas laterales** a cada lado del jefe, opcionales (el link que se pega, el prompt que se envía).
- **Áreas numeradas** de izquierda a derecha con barra negra ("1 · Estilo"). Cada una: caja gris que explica el área, círculo punteado con la mascota de cuadritos, círculos grises numerados, chip gris con el nombre del agente y tarjeta blanca.
- **Chips de quién actúa:** TÚ (rosa) o CLAUDE (lila). En sistemas ya construidos se usan chips de estado (HECHO, EN PROCESO, PENDIENTE).
- **Recuadro rosa final** con el CTA ("Comenta la palabra …") o el ciclo de retroalimentación.
- Líneas **punteadas** que bajan desde el título hasta cada tarjeta, como un organigrama.

## Cómo se usa (receta)
1. Copia `ejemplo-edita-videos.json`, cambia los textos (hasta 3 a 4 áreas, 1 a 3 agentes por área) y corre `python3 generar.py mi-spec.json mi.svg`. Con `"origen_x"` lo mueves a una zona libre del tablero.
2. Manda el SVG a Miro (`canvas_create_from_svg`). Revisa las medidas que devuelve y reacomoda lo que se parta en dos líneas (ver reglas en `plantilla.json`).
3. Escribe el prompt y arma la guía local copiando `guia-ejemplo/` (cambia textos; el prompt va en `<pre id="p1">`, escapando `<` y `>`).
4. **Solo cuando Saúl confirme:** `python3 empaquetar.py <carpeta de la guía>` genera el PDF y las capturas. La captura de bloques se sube a Miro encima de la tarjeta del prompt.

## Lecciones aprendidas
- Miro estima mal la altura de los textos largos: da siempre ancho al textArea y revisa `data-rendered-bounds`.
- Las coordenadas de `image_create` son del centro de la imagen; en el SVG son de la esquina.
- Para subir imágenes: `image_get_upload_url` → `curl -X PUT` → `image_create`.
- El PDF necesita `@page{size:1280px 1810px}` y reglas de impresión que fuercen la rejilla de escritorio.
- No se puede ver el tablero renderizado desde aquí: se comprueba con medidas y con la guía HTML.

## Archivos
`plantilla.json` (parámetros) · `generar.py` (Miro) · `empaquetar.py` (PDF + capturas) · `ejemplo-edita-videos.json` (contenido de ejemplo) · `guia-ejemplo/` (guía HTML) · `referencias/` (imágenes de ejemplo).
