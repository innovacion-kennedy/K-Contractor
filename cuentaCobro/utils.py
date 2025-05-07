import pandas as pd
import os
from django.conf import settings
import PyPDF2
from docx import Document  # ✅ Asegura que está importado correctamente

def extraer_obligaciones_pdf(ruta_pdf):
    obligaciones = []
    with open(ruta_pdf, "rb") as archivo:
        lector = PyPDF2.PdfReader(archivo)
        for pagina in lector.pages:
            texto = pagina.extract_text()
            if "Obligaciones Específicas" in texto:
                partes = texto.split("Obligaciones Específicas")[1].split("\n")
                obligaciones.extend([linea.strip() for linea in partes if linea.strip()])
    return obligaciones

def extraer_obligaciones_word(ruta_docx):
    doc = Document(ruta_docx)
    obligaciones = []
    capturando = False
    for parrafo in doc.paragraphs:
        if "Obligaciones Específicas" in parrafo.text:
            capturando = True  # Empezar a capturar texto después de encontrar el título
        elif capturando:
            if parrafo.text.strip():  # Evita agregar líneas vacías
                obligaciones.append(parrafo.text.strip())
    return obligaciones


