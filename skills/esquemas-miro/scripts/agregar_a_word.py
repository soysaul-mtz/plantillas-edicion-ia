#!/usr/bin/env python3
"""Agrega la captura de una plantilla nueva al Word "Plantillas de Miro" (si no existe, lo crea).

Uso:
  .venv/bin/python agregar_a_word.py "<archivo.docx>" "<Nombre de la plantilla>" <imagen.png> ["leyenda"] [--reemplazar]

Agrega una sección nueva al final (en página aparte): título (Encabezado 1) con el nombre,
la imagen centrada a 6.5" y una leyenda en cursiva. Si ya existe una sección con ese nombre
no la duplica (usa --reemplazar para sustituir su imagen y su leyenda).
Se niega a escribir si el documento está abierto en Word (para no pisar tus cambios).
"""
import pathlib
import subprocess
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor

args = [a for a in sys.argv[1:] if not a.startswith("--")]
reemplazar = "--reemplazar" in sys.argv
if len(args) < 3:
    sys.exit(__doc__)
ruta, nombre, imagen = pathlib.Path(args[0]).expanduser(), args[1], pathlib.Path(args[2]).expanduser()
leyenda = args[3] if len(args) > 3 else ""
if not imagen.exists():
    sys.exit(f"No existe la imagen: {imagen}")
if not ruta.exists():                      # primera vez: crea el Word con su título
    nuevo = Document()
    nuevo.add_paragraph("Plantillas de esquemas en Miro", style="Title")
    ruta.parent.mkdir(parents=True, exist_ok=True)
    nuevo.save(str(ruta))
    print(f"Creé el documento nuevo: {ruta}")

# ¿está abierto en Word?
if (ruta.parent / f"~${ruta.name[2:]}").exists() or (ruta.parent / f"~${ruta.name}").exists():
    sys.exit("El documento parece estar abierto en Word. Guárdalo y ciérralo, y vuelve a intentarlo.")
try:
    abiertos = subprocess.run(["osascript", "-e", 'tell application "Microsoft Word" to get name of every document'], capture_output=True, text=True, timeout=10).stdout
    if ruta.name in abiertos:
        sys.exit("El documento está abierto en Word. Guárdalo y ciérralo, y vuelve a intentarlo.")
except Exception:
    pass

doc = Document(str(ruta))
parrafos = doc.paragraphs
idx = next((i for i, p in enumerate(parrafos) if p.style.name == "Heading 1" and p.text.strip() == nombre), None)

def poner_imagen(p):
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(imagen), width=Inches(6.5))

def poner_leyenda(p, texto):
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(texto)
    r.italic = True
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

if idx is not None:
    if not reemplazar:
        sys.exit(f'Ya existe la sección "{nombre}". Usa --reemplazar para cambiar su imagen.')
    img_p = parrafos[idx + 1]
    for r in list(img_p.runs):
        r._element.getparent().remove(r._element)
    poner_imagen(img_p)
    if leyenda and idx + 2 < len(parrafos):
        cap = parrafos[idx + 2]
        for r in list(cap.runs):
            r._element.getparent().remove(r._element)
        poner_leyenda(cap, leyenda)
    accion = "reemplazada"
else:
    h = doc.add_paragraph(nombre, style="Heading 1")
    if any(p.style.name == "Heading 1" for p in parrafos[:-1] if p is not h):
        h.paragraph_format.page_break_before = True  # cada plantilla en su página (la primera no)
    poner_imagen(doc.add_paragraph())
    if leyenda:
        poner_leyenda(doc.add_paragraph(), leyenda)
    accion = "agregada"

doc.save(str(ruta))
print(f'Sección "{nombre}" {accion} en {ruta}')
