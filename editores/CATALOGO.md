# Catálogo de editores de Saúl

Cuando Saúl manda un video para editar, primero se identifica qué editor le toca:

```
python3 editores/identificar.py "<video>"
```

Da un ranking con razones (ruta, formato, si es entrevista, palabras clave que se oyen en los primeros 2 min).
**RECOMENDADO** = se dice a Saúl qué editor se usará y por qué, y se arranca. **PROBABLE** = preguntarle antes.
Si Saúl nombra el editor ("con el de ORVI", "como los testimoniales"), manda eso sobre el identificador.

| ID | Editor | Para qué | Carpeta | Cómo se usa |
|---|---|---|---|---|
| `orvi99` | **Editor Anuncios** | Anuncios verticales crudos del iPhone (con retomas y plática de grabación) y VSL horizontales de la marca del cliente (seguro de vida, el asesor). Quita silencios/retomas, subtítulos palabra por palabra, zoom con seguimiento de cara, transición en cada corte, gráficos de marca. | `editor-anuncios` | `prepare.py` → `build.py` → `cues.js` → `render.mjs` · memorias `orvi99-editor-v2`, `feedback-ads-edicion-ritmo` |
| `testimoniales-mas` | **Editor Testimoniales MAS** | Entrevistas horizontales (preguntas fuera de cuadro) para testimoniales emotivos que venden el MAS. Mejores partes → armado → subtítulos finish.edits → música Epidemic; subtítulos para tomas de stock del V1. | `editor-testimoniales/editor` | skill `testimoniales-mas` · `README.md` |
| `saul-pro` | **Saúl Pro** | Reels de la marca personal de Saúl (IA + marca personal, CONTENIDO: Dolor/Valor/Autoridad/Objeciones/Metodología). Estilo cine: tipografía palabra por palabra, Saúl recortado sobre papel/negro con texto detrás, escenas 3D, textura de película, sfx y música. Guarda en la misma carpeta como `Video editado - <nombre>.mp4`. | `estilo-cine` | corte con prepare/build de ORVI → `segmentar.swift` → `cine.json` → `node estilo-cine/render.mjs` · Word `~/Documents/Saúl Pro.docx` |
| `saul-pro-3d` | **Saúl Pro 3D** | Reels tipo lista ("las top 5 herramientas…"): Saúl Pro con su fondo real + intro con la ventana naranja Top N y candados, bloque 3D por herramienta (sube, se enciende y gira, con quemado de luz), interfaz de cada herramienta en código a pantalla completa, cierre con la ventana desbloqueada y CTA. Aprobado con C8251 (22 oct 2026). | `estilo-cine` | receta `plantillas/saul-pro-3d/ESTILO.md` + `cine_base.json` · Word `~/Documents/Saúl Pro 3D.docx` |
| `estilo-apple` | **Estilo Apple** | Look de comercial/keynote de Apple: degradado radial de apertura, producto al centro girando en 3D, frases palabra por palabra con blur-in, transiciones con motion blur, fondo marfil. Opcional: dentro de pantalla de MacBook con etiqueta "opus 5.5". | `plantillas/estilo-apple` | `ESTILO.md` (desglose cuadro a cuadro) |
| `editor-51` | **Editor 51** | Persona a cámara vertical + imágenes editoriales a pantalla completa (GPT Image 2.5 en Higgsfield o de internet, look foto real, nada de "gráfico IA") ilustrando cada frase; subtítulos chicos a la izquierda con palabra clave en serif itálica; velo oscuro abajo. Ref. `~/Desktop/editor 51.mp4`. | `editor-testimoniales/editor` | `EDITOR51.md` · `imagenes51.py` · `"estilo51": true` |

Casos frontera conocidos:
- `IMG_0944.MOV` (en la carpeta de ADS de SEGUROS) es un anuncio de **Revolución (la empresa del cliente)**, no de ORVI: el identificador lo marca como PROBABLE ORVI porque no oye palabras de ORVI. El motor de anuncios sirve, pero sin gráficos de marca ORVI — confirmar con Saúl.
- Ana (ejemplo) es agente de seguros, pero su video es testimonial del MAS (entrevista + "Mastermind"): gana Testimoniales MAS.

## Agregar un editor nuevo

Cuando Saúl diga "este es el editor X":
1. Agregar una entrada en `editores.json`: `id`, `nombre`, `alias` (cómo lo llama Saúl), `carpeta`, `para`, `arranque`, `guia`,
   y `señales` → `rutas` (pedazos de ruta típicos), `palabras` (lo que se oye en esos videos), `orientacion`
   (`vertical`/`horizontal`/`null`), `entrevista` (`true`/`false`/`null`).
2. Agregar su renglón a la tabla de arriba.
3. Probar `identificar.py` con 2–3 videos de ese tipo y con uno de cada editor existente (que no se confundan).
4. Anotarlo en la memoria `catalogo-editores`.

## Plantillas de referencia "Editor 1–50" y "Dani Pro"
Saúl las nombra así (videos en `<tu carpeta de contenido>/Formatos/1023/editor N.mp4`). Ficha de cada una en `plantillas/formatos/editor-NN/ESTILO.md`; índice por familia en `plantillas/formatos/README.md`. Si Saúl dice "edítalo con el Editor N", abrir esa ficha y construir el estilo con el motor estilo-cine (la ficha dice cómo). Ojo: el Editor 49 es la referencia de Saúl Pro ("Saul pro.mp4").
