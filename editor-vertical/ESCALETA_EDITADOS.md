# Escaleta · VSL editados → vertical (Reencuadre + Saúl Pro)

Aplica a **Chuy**, **Mati** y **Legendaria**. Legendaria V1 y V2 son el mismo corte; V2 solo trae subtítulos chiquitos quemados. Como en vertical van subtítulos Saúl Pro, sale **una sola** versión desde V1 (limpia).

## Qué se hace en todos (sin tocar el corte original)
1. **Análisis cuadro por cuadro** (ya hecho): Vision leyó 1 de cada 2 fotogramas (cara + todo el texto quemado) y se detectaron todos los cortes de toma.
2. **Encuadre por tramo, sin zoom:**
   - **Persona a pantalla completa:** recorte 9:16 a la cara. Si la persona se mueve mucho, la cámara la sigue suave, sin acercarse nunca.
   - **Toma o gráfico sin texto:** recorte 9:16 a pantalla completa.
   - **Toma con texto quemado que no cabe en 9:16** ("MENTIRA", "internet / redes sociales", las tarjetas de Legendaria): panel con el recorte más angosto que deja ver el texto completo, y detrás el mismo cuadro desenfocado y oscurecido. Así nunca queda un texto cortado.
   - Si el encuadre cambia sin corte de toma: fundido de 6 cuadros.
3. **Subtítulos viejos** (Mati): la franja de abajo se difumina y oscurece; queda debajo de la interfaz de Instagram.
4. **Subtítulos Saúl Pro:** palabra por palabra, línea chica + palabra gigante (Helvetica Neue), con la entrada de desenfoque y estela de Saúl Pro, sin zoom del texto.
   - En persona van justo debajo de la barbilla. En panel, debajo del panel.
   - Nunca encima de la cara ni del texto que ya trae el video. Si el video ya muestra esa misma frase a todo lo ancho, no se duplica.
   - Color según el fondo de cada página: oscuro con halo claro sobre fondo claro, blanco sobre oscuro. Todo dentro de la zona segura de IG.
5. **Look Saúl Pro:** grano fino solo en luz + viñeta. No se cambia el color del original, que ya viene etalonado.
6. **Audio:** el original tal cual (voz, música y efectos ya mezclados).
7. **Revisión final cuadro por cuadro** (`revisar_final.py`) + re-transcripción por tramos antes de entregar.

Nombres corregidos en subtítulos: Jorge **Apellido**, **la empresa del cliente**, **programa del cliente** (Whisper oía "Club Sinergé" / "Club Cidercú"), **Janeth** (como sale en el video de Chuy, "kamilaJaneth"), **Synergy** Education, **ChatGPT**, **Claude**, **Legendaria**, Alonzo Lozano.

---

## 1 · programa del cliente · Chuy — `VSL CHUY v3.mov` (6:53, 1920×1080)
- 179 tramos: **144 s persona a pantalla completa**, **269 s panel o toma**. Es el más cargado de texto cinético: casi cada frase trae palabras animadas al lado de Jorge, y por eso hay más paneles.
- CTA final: "Toca el botón de aquí abajo" → **flecha animada hacia abajo** en zona segura (6:42–6:53).

| Reel | Tramo | Gancho | Idea |
|---|---|---|---|
| CH-1 · "Atrapado en el mundo físico" | 0:41.8–1:18 (36 s) | "Muchos de nosotros crecimos con la idea que para ganar más dinero hay que echarle más ganas" | si te detienes, el dinero se detiene → tu entrada al mundo digital |
| CH-2 · "El caso de Janeth" | 4:42–5:30 (48 s) | "Quiero que veas el caso de Janeth" | uñas en CDMX → ceros en EE. UU. → "fue mi salvación" |
| CH-3 · "El sistema de 3 pasos" | 2:01–2:36 (35 s) | "Todo se basa en un sistema muy simple y sencillo" | oferta → audiencia → sistema de ventas; "lo puedes copiar" |

## 2 · programa del cliente · Mati — `VSL 1 MATIASH.mov` (9:51, 2560×1440)
- 175 tramos: **385 s persona a pantalla completa**, **206 s panel o toma**. Trae subtítulos quemados abajo: se tapan.
- CTA final: "presiona el botón de aquí abajo" → **flecha animada** (9:24–9:51).

| Reel | Tramo | Gancho | Idea |
|---|---|---|---|
| MA-1 · "Solo tienes 24 horas" | 1:28–2:22 (54 s) | "Estás jugando en un juego donde solamente tienes 24 horas" | el mundo físico → "Ese es el mundo digital" |
| MA-2 · "No es tu culpa" | 3:02–4:10 (67 s) | "Yo ya sé lo que probablemente hoy ya intentaste" | piezas sueltas del rompecabezas → sistema completo |
| MA-3 · "Son las 3 de la mañana" | 6:57–7:32 (35 s) | "Son las 3 de la mañana y tú estás dormido" | venta mientras duermes → "el sistema vende por ti" |

## 3 · Legendaria — `VSL_V1.mp4` (11:41, 1920×1080)
- 84 tramos: **456 s persona a pantalla completa**, **246 s panel** (piedra y palanca 3D, mapa de oficinas, tarjetas de los 4 programas, testimonios en celular).
- CTA final: "bajar dentro de este sitio… agendar mi diagnóstico" → **flecha hacia abajo** (10:57–11:41).

| Reel | Tramo | Gancho | Idea |
|---|---|---|---|
| LE-1 · "La piedra y la palanca" | 0:30–1:31 (61 s) | "Quiero que veas cómo tenemos una tabla y tenemos una piedra" | la IA es la palanca; te falta el punto de apoyo (el método) |
| LE-2 · "La pregunta incómoda" | 2:37–3:20 (43 s) | "¿Por qué la IA, si es tan buena y ya la usas, tu negocio sigue igual?" | razón 1: nada de lo que has visto está hecho para ti |
| LE-3 · "No sé nada de tecnología" | 5:03–5:46 (43 s) | "Oye, Manuel, yo no sé nada de tecnología" | objeción → "este método es para ti" |

## Salidas (junto a cada original en `~/Downloads/lote-vertical/<carpeta>/`)
- `Video editado - VSL Chuy vertical.mp4`, `Video editado - VSL Mati vertical.mp4`, `Video editado - VSL Legendaria vertical.mp4`
- `Reel CH-1 - ….mp4` … (9 reels) — 1080×1920, perfil Redes.

## Preguntas
1. En los reels, ¿cómo cierro? (a) sin CTA, termina en la idea · (b) tarjeta final "Agenda tu sesión ↓" · (c) "comenta PALABRA" (¿cuál?).
   Los reels conservan el audio original: la música ya viene mezclada con la voz y otra canción encima chocaría.
