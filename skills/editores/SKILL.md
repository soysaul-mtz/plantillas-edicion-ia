---
name: editores
description: Decide qué editor de video usar cuando Saúl manda un video para editar (Editor Anuncios, Editor Testimoniales MAS y los que se vayan agregando). Úsala siempre que Saúl pase un video o ruta de video para editar/subtitular/armar sin decir con qué editor, cuando pregunte "¿qué editor usamos?", o cuando diga que un nuevo flujo/editor tiene nombre ("este es el editor X") para registrarlo.
---

# Skill: catálogo de editores

Registro en `editores/` — `CATALOGO.md` (tabla y cómo agregar editores) y `editores.json` (señales).

## Video nuevo
1. `python3 editores/identificar.py "<video>"` (formato, ruta, ¿entrevista?, palabras de los primeros 2 min).
2. Decirle a Saúl en una línea: **"Este va con el Editor X"** + por qué (p. ej. "vertical, crudo con retomas, habla de seguro de vida").
   - RECOMENDADO → seguir directo con el flujo de ese editor.
   - PROBABLE o empate → preguntarle cuál usar antes de tocar nada.
   - Si Saúl ya nombró el editor, usar ese (alias en `editores.json`: "Orbi 99" = la marca del cliente, "testimoniales" = Testimoniales MAS).
3. Cargar la guía de ese editor: Testimoniales MAS → skill `testimoniales-mas`; la marca del cliente → memorias `orvi99-editor-v2`, `feedback-ads-edicion-ritmo`, `feedback-fluidez-animaciones` y `editor-anuncios`.
   Saúl Pro → memorias `estilo-cine-3d`, `feedback-saul-pro-fondo-real-piel`. **Saúl Pro 3D** (reels tipo lista "top 5 herramientas") → `plantillas/saul-pro-3d/ESTILO.md` + `cine_base.json` y memoria `saul-pro-3d`.

## Editor nuevo
Cuando Saúl bautice un flujo como editor ("este es el editor de X"), registrarlo siguiendo `CATALOGO.md → Agregar un editor nuevo`
(entrada en `editores.json`, renglón en la tabla, prueba de `identificar.py` con videos de cada editor, memoria `catalogo-editores`).
