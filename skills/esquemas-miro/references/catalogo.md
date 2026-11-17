# Catálogo de plantillas de esquemas

| Nombre | Para qué | Archivos en esta skill |
|---|---|---|
| **Esquema de empresa** | Explicar un sistema paso a paso como organigrama: dueño, jefe, áreas numeradas y agentes; con guía HTML del prompt | `references/estilo-esquema-de-empresa.md`, `references/plantilla-esquema-de-empresa.json`, `scripts/generar.py`, `assets/ejemplo-edita-videos.json`, `assets/guia-plantilla/` |

## Para sumar una plantilla nueva
1. Destila el estilo (no lo recrees): colores, tipografías, estructura, medidas y reglas → `references/estilo-<nombre>.md` + `references/plantilla-<nombre>.json`.
2. Si se dibuja con código, agrega su generador en `scripts/` y un spec de ejemplo en `assets/`.
3. Agrega su fila a esta tabla.
4. Haz su imagen y agrégala al Word de plantillas del usuario (`scripts/agregar_a_word.py`).
