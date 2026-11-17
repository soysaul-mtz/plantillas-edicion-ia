---
name: testimoniales-mas
description: Edita testimoniales y anuncios de persona a cámara (entrevistas del MAS / Mastermind de el mentor, anuncios verticales con guion, u otras) con la plantilla de Saúl: transcribe por pedazos, propone las mejores partes, muestra un PLAN paso a paso a la persona, arma el corte (voz pareja, sin palabras cortadas ni pausas largas), subtitula estilo finish.edits sin tapar la cara y dentro de la zona segura de Instagram, tomas de stock, flecha al CTA, música de una carpeta o MCP, y revisa todo antes de entregar. Úsala cuando Saúl (u otra persona) pase un video de testimonio/entrevista/anuncio a cámara, pida "las mejores partes", "armarlo y subtitularlo como el otro", o mande un "... PRE SUBS V1.mp4".
---

# Skill: testimoniales MAS (y anuncios a cámara)

Proyecto: `editor-testimoniales` — leer `README.md` (flujo, `pages.txt`, campos de `proyecto.json`) y
`editor/plantilla.json` (valores por defecto: zona segura de IG, `pausa_max`, `min_pagina`, `lufs`, `cola`, transición).
Todo se corre desde `editor/` con `.venv/bin/python` (Whisper mlx ya instalado ahí).

## 0. Antes de editar: preguntar (una sola vez, juntas)
- **Música:** ¿carpeta con canciones o MCP de música conectado (Epidemic Sound…)? Sin música no se entrega salvo que diga "sin música".
- **Duración máxima** del video y **formato** (Redes 1080 por defecto; 4K solo si lo pide).
- Nombres propios que Whisper escribe mal → `vocabulario`.
- Si hay tomas de stock: el video de stock → `broll_auto` (y la palabra después de la que entran).

## 1. Transcribir y elegir partes
`transcribir.py <video> ../proyectos/<n> "Nombres"` → `fuente.txt` por pedazos con dB. La persona a cámara suena más
fuerte que el director (marcado `← ¿director?`); con retomas, la buena suele ser la última y más fuerte. Proponer partes
con minuto:segundo → `proyecto.json.cortes`.

## 2. PLAN para la persona (obligatorio)
`editar.py ../proyectos/<n> plan` → **mostrar el contenido de PLAN.md TAL CUAL** a la persona, empezando con:
"Esto es lo que voy a hacer con tu video, paso a paso. Revísalo y dime si algo está mal antes de que lo arme."
No armar hasta que diga "sí". Si pide cambios, editar `proyecto.json` y volver a correr `plan`.

## 3. Armar y subtitular
`editar.py <p> armar` → escribir `pages.txt` con `corte.txt` (renglones `s:` cortos, un `B:` por frase, sin palabra
suelta al final; corregir nombres) → `editar.py <p> terminar`. Se detiene si algo falla:
- texto encima de la cara / fuera de la zona segura → parte frases solo; si no puede, acortar `pages.txt`;
- toma de stock que cruza un cambio de plano / rebanada → revisar `broll`;
- unión que se come una palabra o subtítulo distinto a lo que se oye → corregir corte o `pages.txt`;
- **revisión final cuadro por cuadro** (`revisar_final.py`, último paso): texto real sobre la cara o fuera de zona segura,
  subtítulos que no se ven, destellos de 1 cuadro, negros, congelados, audio que satura. Solo si todo pasa se copia a "salida".
  **Mirar las hojas `revision_final/hoja_*.jpg` con Read** (marco rojo = problema) antes de decir que quedó.
Para videos de OTROS editores: `revisar_final.py <carpeta> "<video>"` también funciona (sin pages.json).
Después: `render.mjs <p> stills t1,t2,…` (6–10 tiempos, incluir cortes, tomas de stock y CTA) y VERLOS con Read.

## 4. Entregar
Decir a la persona, en corto: dónde quedó el video, duración, volumen, qué se revisó automáticamente y cualquier
aviso que quedó (p. ej. licencia de música). "Súbele a la música" → `mezcla.py <p> <vol>`.

## V1 con stock de la persona
`v1.py <p> "<V1>.mp4"` → ver `tomas_*.jpg` → `render.mjs <p> v1 stills …` → `render.mjs <p> v1`.

Preferencias de Saúl: memorias `feedback_texto-nunca-sobre-persona`, `feedback-ads-edicion-ritmo`,
`feedback-fluidez-animaciones`, `anuncios-dji-video-7-minutos` (sin zooms, sin circulito, flecha en el CTA).
