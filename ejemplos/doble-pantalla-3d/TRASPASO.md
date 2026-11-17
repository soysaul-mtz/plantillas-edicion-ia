# Traspaso · EJEMPLO DE IA (5 nov 2026)

Saúl pidió que esta edición la termine la sesión "Referencia de edicion.mp4". Formato: **Original vs Editado por Claude** (como C8256).

## Fuente
`<tu disco>/Grabaciones/Casa Nelson/EJEMPLO DE IA/`
- `Crudos/FX30-7544.MP4`: 111 s, chamarra negra, CTA "EDITOR".
- `Crudos/FX30-7545.MP4`: 57.6 s, polo negro, CTA "CLAUDE".
- Los dos crudos son 4K horizontal, de noche, con ventana y ciudad atrás.
- `REFERENCIAS/Referencia C8256 .mp4`: la referencia viral.
  - Arriba va "Original" con el chip "IMG_xxx · SIN TOCAR".
  - Abajo va "Editado por Claude Opus 5.5", en naranja sobre fondo café oscuro.
- `REFERENCIAS/Video editado - C8256.mp4`: el que se hizo el 19 oct con Saúl Pro y doble.mjs. **No repetir ese estilo.**

## Lo que pidió Saúl
1. Analizar la referencia cuadro por cuadro y editar los dos crudos en ese formato de doble pantalla. Arriba y abajo llevan los mismos cortes.
2. Los crudos están MUY desenfocados porque la cámara enfocó la ciudad. Hay que enfocarlo lo más posible antes de editar.
3. La mitad de abajo va en estilo distinto al de C8256, con plantillas nuevas:
   - un video "más editado, con animaciones 3D dentro del video";
   - otro de "puras imágenes" (como los Flujo de FONDO GRIS).

## Lo hecho (en `~/Proyectos/ejemplo-ia/`)
- **`enfoque.py`:** deconvolución Richardson-Lucy.
  - Usa PSF de disco con radio 10 a 1920x1080, 25 iteraciones, torch MPS.
  - Se aplica SOLO sobre la persona (máscara de `estilo-cine/segmentar.swift`). El fondo ya estaba nítido y no se toca.
  - La mejora es clara. CodeFormer/GFPGAN no se pudieron instalar (permiso negado): no intentarlo.
  - Falta pasar `piel.py` encima.
- **`armar_corte.py`:** arma las tomas buenas, medidas por energía del audio. Las transcripciones están en `crudos/7544.json` y `crudos/7545.json`.
  - `7545/corte.mp4` + `corte_enfocado.mp4` (24.08 s): tomas [0.92-3.75] [4.56-7.35] [7.99-17.42] [46.42-55.45].
  - `7544/corte.mp4` + `corte_enfocado.mp4` (24.2 s): tomas [21.95-28.4] [46.2-54.0] [68.95-71.35] [101.85-109.4], ya sin retomas.
- **`logos/`:** `capcut.png`, `premiere.png` y `edits.png`, íconos oficiales de App Store de 1024 px.

## Video 1 · FX30-7545 → plantilla nueva "3D"
Fondo real nocturno con objetos Three.js en luz naranja y aguamarina.

| seg | dice | se ve |
|---|---|---|
| 0–2.8 | "Subir videos a redes sociales es mucho más fácil que nunca" | Celular 3D flotando a su lado; suben 3 tarjetas de video con barra a 100 % |
| 2.8–5.6 | "Y más porque no ocupas saber editar para subir videos" | **Pedido expreso:** logos REALES de CapCut, Premiere y Edits en 3D entran flotando; en "editar" se agrietan y estallan en pedazos que salen volando |
| 5.6–9 | "este video se hizo completamente con IA" | Logo de Claude 3D girando enorme detrás de su cabeza, con "100 % IA" en relieve |
| 9–14 | "Los subtítulos, las imágenes, las transiciones, todo" | Tarjetas 3D en órbita, una por palabra, con palomita; "TODO" gigante en 3D detrás de él |
| 14–15 | "Inclusive la música y los efectos de sonido" | Ecualizador 3D con la envolvente real de su voz y una nota musical girando |
| 15–24 | CTA "coméntame la palabra CLAUDE… te envío gratis la plantilla" | Burbuja de comentario 3D "CLAUDE" con flecha; sobre/archivo "PLANTILLA" volando a la bandeja de DM |

## Video 2 · FX30-7544 → plantilla "Puras imágenes"
Mundo Flujo en B/N con luz naranja, panel 16:9.

| seg | dice | se ve |
|---|---|---|
| 0–1.43 | "Ya no ocupas saber editar videos…" | Saúl a cámara, enfocado |
| 1.43–2.95 | "…para subir videos a redes sociales" | Chavo abrumado frente a un programa de edición lleno de capas |
| 2.95–6.45 | "porque este video se hizo 100 % con IA" | **Pedido:** un ROBOT en la computadora editando |
| 6.45–10.95 | los subtítulos, las imágenes, las animaciones, la música, los efectos de sonido | Montaje rápido: subtítulos / fotos / animaciones / tocadiscos y bocina / onda de audio |
| 10.95–14.25 | "todo, absolutamente todo se hizo con IA" | **Pedido:** el chavo DE ESPALDAS frente a una pantalla gigante donde el video se arma solo |
| 14.25–16.65 | "sin utilizar una sola herramienta de edición" | Herramientas de edición empolvadas en una vitrina |
| 16.65–22.1 | CTA "comenta la palabra EDITOR…" | Saúl a cámara con caja de comentario "EDITOR" y flecha, hecha en código |
| 22.1–24.2 | "…y te mando la plantilla" | Celular recibiendo un sobre con la plantilla |

**Las 10 imágenes YA están generadas** en `7544/flujo/00–09.png` (16:9, 5 créditos) y `flujo.json` está listo. Cuando se corrió `flujo.py` faltaba `cortes.json`; ya existe. Para armar los clips 1920x1080 (sin regenerar imágenes):

```
cd editor-testimoniales/editor && .venv/bin/python estilo_paleta/flujo.py ~/Proyectos/ejemplo-ia/7544 ~/Proyectos/ejemplo-ia/7544/flujo.json
```

`flujo.py` admite desde hoy `"formato":"16:9"`, `"lugar"` por toma y `"rapido"` (el foco cambia en 0.05 s, para montajes).

## Pendiente
- **Respuesta de Saúl:** el panel de ARRIBA ("Original · SIN TOCAR"), ¿crudo desenfocado o también enfocado? Se le propuso dejarlo crudo para que se note el contraste; abajo va enfocado. Aún no contesta.
- **Tiempo estimado que se le dio:** Video 2 ~30–40 min, Video 1 (3D) ~2–2.5 h. Se ofreció entregar primero el Video 2.
- **Entrega sugerida:** junto a los crudos, como `Video editado - FX30-7545.mp4` y `Video editado - FX30-7544.mp4`.
- **Reglas que aplican:**
  - texto nunca sobre la cara y dentro de la zona segura de IG;
  - música distinta en cada video, que suene desde el segundo 0;
  - sin palabras cortadas;
  - renders uno a la vez, con `nice`.

## Entregado (5 nov 2026)
- `Video editado - FX30-7544.mp4` (puras imágenes) y `Video editado - FX30-7545.mp4` (3D), junto a los crudos en `EJEMPLO DE IA/`.
- Saúl confirmó: arriba va el CRUDO desenfocado ("Original · SIN TOCAR"). Música: Leanin (Slowed) en los dos (lo pidió él).
- Flujo: `filtro_h.py` (piel) → `cam.mp4`; escenas HTML en `escenas/` (7545 = Three.js en dos pasadas, atrás/frente de la silueta `mascara.mp4`);
  `python3 armar_final.py <v>` arma capa + panel + audio + doble pantalla (`doble.mjs`, 29.97) y copia a la salida. `fotos.mjs` = cuadros sueltos para revisar.
