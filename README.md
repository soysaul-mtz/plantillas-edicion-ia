# Sistema de edición de video con IA

Edita reels verticales con **Claude Code** como lo hace Saúl Martínez: le pasas un video, Claude encuentra las tomas
buenas, te propone una escaleta, y al aprobarla corta, suaviza la piel, pone subtítulos palabra por palabra, gráficos,
escenas 3D, interfaces de herramientas animadas, música y efectos, y te entrega el video listo en 1080 o en 4K.

## Qué incluye
- **Plantillas con nombre:** Saúl Pro, Saúl Pro 3D (Top N de herramientas), Editor 1–50 y Dani Pro (51 estilos de reels
  analizados fotograma por fotograma), video reacción, original vs editado, tutorial cámara + pantalla, lista de
  herramientas, anuncios con retomas, testimoniales, Editor 51, reels sin cara con voz IA.
- **Editores largos:** cursos y clases por capítulo (cámara + pantalla, sin retomas), VSL animado 3D con subtítulos al
  centro, y paso de horizontal a vertical sin zooms.
- **Motor de render** con texto cinético, Three.js, interfaces emuladas (NotebookLM, Higgsfield, Claude Code, Napkin,
  HeyGen, ElevenLabs…), textura de película y salida **Redes (1080)** o **4K de bajo consumo**.
- **Lead magnets:** genera el PDF de "70 herramientas de IA gratis" y la guía para entregar por DM.
- **Instagram:** entrega automática del recurso a quien comenta la palabra (Zernio + GitHub Actions).
- **Skills de Claude Code** y un `CLAUDE.md` con todas las reglas que se fueron afinando video por video, incluida la
  lista de revisión que se cumple en cada entrega (la que dejó los errores casi en cero).

## Cómo trabaja contigo
1. **Te pregunta lo necesario una sola vez:** de dónde sale la música (una **carpeta** con canciones o un **MCP de música**
   conectado, como Epidemic Sound), la **duración máxima** del video, si lo quieres en Redes (1080) o 4K y los nombres
   propios que salen en el video.
2. **Te muestra el plan tal cual, paso a paso, antes de tocar nada:** qué partes usa y en qué orden, qué quita, cuánto dura,
   qué va a hacer en cada paso y una lista de **posibles errores** para que tú los revises (una voz que podría ser de otra
   persona, una palabra que podría quedar cortada…). Edita solo cuando le dices "sí".
3. **Revisa solo antes de entregarte:**
   - **Cortes:** ninguna palabra cortada (doble transcripción en cada corte y en cada unión) y ninguna pausa larga.
   - **Voz y cierre:** volumen de la voz parejo entre cortes y final a −14 LUFS; el final se desvanece justo cuando
     terminas de hablar, sin cuadro congelado.
   - **Textos:** nunca encima de tu cara (detecta tu cara en todos los fotogramas) y siempre dentro de la zona segura
     de Instagram; ningún subtítulo es tan corto que no se alcance a ver.
   - **Tomas de stock:** ninguna cruza un cambio de plano, así que no hay destellos.
   - **Color:** el video HDR (DJI, iPhone) pasa a color normal.
   - **Revisión final cuadro por cuadro:** con el video terminado lee todos los fotogramas (tu cara y el texto que de verdad
     aparece) y te deja hojas con los cuadros; los que tienen algún problema salen con marco rojo.

## Requisitos
Mac con chip Apple (M1 o más nuevo) · macOS 14+ · Claude Code · ~10 GB libres.
Cuentas opcionales (cada quien la suya): Epidemic Sound (música), Higgsfield (imágenes IA), ElevenLabs (voz IA),
Zernio (Instagram), Miro y Google Drive.

## Instalación

En tu **link personal de compra** está un mensaje listo para copiar. Abre Claude (la app de escritorio en la pestaña **Code**, o
Claude Code en Visual Studio Code), pégalo y Claude descarga el sistema, revisa tu compu con `scripts/requisitos.sh`, te pide
permiso antes de instalar cada cosa y al final renderiza un video de prueba. Paso a paso a mano: **INSTALAR.md**.

## Qué NO viene (y por qué)
- **Música y efectos de Epidemic Sound:** su licencia es por cuenta. El repo trae la lista (`audio/catalogo.json`)
  para que tu Claude los descargue con tu cuenta, y un generador de efectos libres para empezar sin ella.
- **Videos, fotos y fotogramas de personas** (incluidas las referencias de otros creadores): solo vienen las fichas
  escritas de cada estilo. Con tus propias referencias, `plantillas/formatos/generar.py` saca las hojas de fotogramas.
- **Llaves y cuentas:** cada quien conecta las suyas; se guardan en el Llavero de macOS, nunca en archivos.

## Actualizar
`git pull && ./instalar.sh`

## Licencia
Uso personal e intransferible para el comprador (una persona o un negocio). Prohibido compartir o revender el paquete.
Los videos que hagas con él son tuyos. Detalle en [LICENCIA.md](LICENCIA.md).
