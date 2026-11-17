# Catálogo de plantillas de estilo

Plantillas visuales reutilizables de Saúl para explicar sistemas en video. Cada carpeta trae `ESTILO.md`, `plantilla.json` y los scripts para repetirla.

| # | Nombre | Para qué | Carpeta | Estado |
|---|--------|----------|---------|--------|
| 1 | **Esquema de empresa** | Explicar un sistema paso a paso como organigrama (dueño, jefe, áreas y agentes) + guía con prompt | `esquema-de-empresa/` | Guardada (17 oct 2026) |
| 2 | (pendiente: Saúl va a pasar el 2º estilo) | | | |
| 3 | (pendiente: Saúl va a pasar el 3er estilo) | | | |

Para sumar un estilo nuevo: crear su carpeta con `ESTILO.md` + `plantilla.json`, agregarlo a esta tabla y avisarle a Saúl.

## Flujo cuando Saúl pase una plantilla nueva
1. **Guardarla:** crear `plantillas-estilo/<nombre>/` con `ESTILO.md` + `plantilla.json` (y sus scripts) y agregar su fila a la tabla de arriba.
2. **Crearla:** usarla para hacer el esquema que pida (Miro, guía local y, si confirma, PDF y captura en Miro).
3. **Capturarla:** generar la imagen de la plantilla (en "Esquema de empresa": `capturar.py spec.json salida.png`).
4. **Word:** agregarla al documento maestro con
   `.venv/bin/python agregar_a_word.py "~/Documents/Plantillas de Miro.docx" "<Nombre>" <imagen.png> "<leyenda>"`
   (una sección nueva por plantilla, en página aparte; el Word debe estar cerrado).

## Plantillas de edición de video (reels)
| Nombre | Para qué | Carpeta | Word |
|--------|----------|---------|------|
| **Saúl Pro** | Reels estilo cine: tipografía palabra por palabra, tu fondo real con filtro de piel, escenas 3D (19 oct 2026) | `saul-pro/` | `~/Documents/Saúl Pro.docx` |
| **Saúl Pro 3D** | Saúl Pro + intro con la ventana Top N, bloque 3D por herramienta e interfaces en código a pantalla completa, para reels tipo lista (22 oct 2026) | `saul-pro-3d/` (ESTILO.md, cine_base.json) | `~/Documents/Saúl Pro 3D.docx` |

## Plantillas de Formatos/1023 (Editor 1–50 + Dani Pro)
51 plantillas de edición analizadas fotograma por fotograma, agrupadas en 26 familias (Pantalla Filmada, Tutorial con Flechas, Mundo Voxel, Split Explicador, Comercial de Producto, Póster Editorial…). Índice en `formatos/README.md`; Word con todas las plantillas (también las que ya usamos): `~/Documents/Plantillas y Editores.docx`.
