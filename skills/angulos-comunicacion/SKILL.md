---
name: angulos-comunicacion
description: Escribe guiones de video/ads persuasivos usando el catálogo de 61 ángulos de comunicación (organizados en 6 familias) y la librería de formatos/esqueletos probados (fórmula CVDirecto, lista numerada tipo "5 leyes", confesión íntima "en secreto", reveal con corte brusco "crítica", caminata/walk&talk, diálogo a dos voces, objeciones validadas, carta abierta, POV). Úsala cuando el usuario pida guion(es) o guiones de ads/video para una persona o marca, mencione "ángulos de comunicación", pida variar o diversificar creativos (p. ej. para Meta/Andrómeda), o pida un formato ya conocido por nombre ("estilo CVDirecto", "leyes del universo", "en secreto", "walk and talk", "diálogo"). Incluye el flujo de investigación previa del protagonista (Instagram + Drive) antes de escribir.
---

# Ángulos de comunicación — guiones persuasivos

Sistema para escribir guiones de video (ads y orgánico) a partir de dos piezas separadas que
casi siempre se confunden: el **ángulo** (el argumento — por qué le importa esto a esta persona)
y el **formato/esqueleto** (el contenedor — cómo se estructura la pieza). El mismo formato
relleno con ángulos distintos produce piezas que se sienten completamente diferentes; el mismo
ángulo en formatos distintos también. Para diversidad real de creativo (relevante si el usuario
menciona Meta/Andrómeda), variar ambos ejes, no solo el gancho de apertura.

## Antes de escribir: investiga al protagonista

No escribas genérico si se puede evitar. Antes del primer guion:

1. **Instagram** (u otra red que tenga): usa el skill `render-webpage` para leer bio, highlights
   y grid — de ahí sale el posicionamiento real, los pilares de contenido y a veces frases
   propias reutilizables.
2. **Drive u otros archivos del proyecto**: busca decks de speaker, testimoniales, guiones
   previos, transcripciones de eventos — con frecuencia hay frases/quotes reales de la persona
   que valen más que cualquier línea inventada. Si hay video/audio largo (ej. un seminario) y
   se necesita el contenido real, transcribir con whisper.cpp (más rápido con aceleración Metal
   en Mac que openai-whisper puro CPU) en vez de resumir de oídas.
3. Si la persona tiene un rol/autoridad concreta (ej. "directora de eventos presenciales", no
   solo "directora"), úsalo como el beat de autoridad/secreto técnico del guion — da más peso
   real que una credencial genérica.

## Flujo para escribir

1. **Define avatar + dolor central** con el usuario si no es obvio (a quién le habla, qué tanto
   sabe ya del problema).
2. **Elige ángulo(s)** de `references/catalogo-angulos.md` — para un solo guion, uno o dos
   ángulos combinados; para un *set* de varios guiones, ángulos de familias distintas para que
   no se sientan variaciones del mismo.
3. **Elige formato(s)** de `references/formatos.md` — combina con el ángulo elegido (un ángulo
   de miedo/pérdida rara vez pide formato "caminata" reflexivo; un ángulo narrativo de origen sí).
4. **Escribe** siguiendo las reglas generales al final de `references/formatos.md` (duración,
   CTA/fecha, voz real de la persona, no declarar jerarquías en voz alta).
5. Si el usuario pide un lote grande para diversidad de Andrómeda, generar **sets**: cada set
   trae su propio ángulo+formato, y dentro de un set 2 variantes de gancho está bien — pero no
   confundir "2 ganchos del mismo set" con "2 sets distintos".

## Referencias

- `references/catalogo-angulos.md` — los 61 ángulos, la cadena avatar→consciencia→ángulo→
  gancho→claim→oferta, la distinción ángulo/formato/gancho, qué familias pesan más en ads
  pagados vs. orgánico, y la regla de secuenciación "Opción C" (gancho universal → nicho).
- `references/lentes-de-contenido.md` — cómo sacar muchos ángulos de un tema (creencia, hábito,
  error, duda, objeción, mito, comparación, proceso, costo) y la fórmula tema × lente × motor ×
  formato; incluye la estructura de carrusel de referencia. Úsalo antes del catálogo cuando se
  pidan ideas o temas para carruseles.
- `references/formatos.md` — los 9 esqueletos documentados con su estructura exacta, más las
  reglas generales de escritura aprendidas en la práctica.
