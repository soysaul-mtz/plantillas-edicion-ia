---
name: sistema-edicion
description: Sistema de edición de reels con Claude (plantillas Saúl Pro, Saúl Pro 3D, Editor 1–50, reacciones, listas de herramientas, tutoriales, anuncios, testimoniales, cursos/clases largas por capítulo, VSL animado 3D, horizontal a vertical; salida Redes 1080 o 4K; entrega por DM en Instagram). Úsala siempre que la persona pase un video o carpeta para editar, pida una plantilla por nombre, quiera un lead magnet en PDF o una automatización de "comenta la palabra".
---

# Sistema de edición

1. Abre y sigue `CLAUDE.md` de la carpeta del repositorio (ruta al final de este archivo): ahí están el flujo
   (preguntar música [carpeta o MCP], duración máxima y formato → identificar editor → transcribir y cazar retomas →
   PLAN TAL CUAL a la persona, sin editar → cortar → preparar → stills → render → revisiones → entregar)
   y las reglas de estilo que no se deben romper.
2. Si falta algo instalado (`.venv`, `bin/segmentar`, `config/kit.json`), sigue `INSTALAR.md`.
3. Plantillas: `plantillas/` (Saúl Pro 3D: `plantillas/saul-pro-3d/ESTILO.md`). **Formatos (61):** índice `plantillas/formatos/GUIA-FORMATOS.md` y una `GUIA.md` por formato (qué es y cómo hacerlo).
4. Salida por defecto **Redes (1080)**; **4K** solo si la persona lo pide (`prep4k.py` + `render.mjs --perfil 4k`).
5. Cursos o clases largas → `editor-cursos/README.md`; VSL animado 3D → `editor-vsl-animado/README.md`; horizontal a vertical → `editor-vertical/`.
   Antes de entregar cualquier video, cumple la lista «Cómo se llegó a casi cero errores» de `CLAUDE.md`.
6. Primero el plan (mostrado tal cual, con la lista de posibles errores); no se edita ni se publica nada sin aprobación.
6. Testimoniales y anuncios a cámara: `editor-testimoniales/editor/editar.py <proyecto> plan|armar|terminar` (hace las
   revisiones solo: palabras cortadas, pausas, voz pareja, texto fuera de la cara y en zona segura, stock sin destellos, final sin congelar).
