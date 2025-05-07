import os
import PyPDF2
from docx import Document
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import default_storage
from .models import (
    CuentaCobro, PagoPlanilla, ContratoObligacion, 
    CuentaCobroObligacion, PreguntasFiscales
)
from contratacion.models import Contrato
from login.models import Persona
from django.template.loader import get_template
from weasyprint import HTML
import re

### FUNCIONES AUXILIARES ###

def extraer_obligaciones_especificas(texto):
    texto = re.sub(r"FORMATO\s*ESTUDIOS\s*PREVIOS\s*PRESTACIÓN\s*DE\s*SERVICIOS\s*PROFESIONALES\s*/\s*DE\s*APOYO\s*A\s*LA\s*ALCALDÍA\s*DE\s*KENNEDY", "", texto, flags=re.IGNORECASE)
    inicio = texto.find("10.5 OBLIGACIONES ESPECÍFICAS")
    if inicio == -1:
        return []
    texto = texto[inicio:]
    fin = texto.find("10.6 OBLIGACIONES DE LA SECRETARÍA")
    if fin != -1:
        texto = texto[:fin]
    obligaciones = []
    linea_actual = ""
    for linea in texto.split("\n"):
        linea = linea.strip()
        if linea.startswith("10.5 OBLIGACIONES ESPECÍFICAS"):
            continue
        if "FORMATO ESTUDIOS PREVIOS" in linea:
            linea = linea.replace("FORMATO ESTUDIOS PREVIOS", "").strip()
        if linea:
            if linea[0].isdigit():
                if linea_actual:
                    obligaciones.append(linea_actual.strip())
                linea_actual = linea
            else:
                linea_actual += " " + linea
    if linea_actual:
        obligaciones.append(linea_actual.strip())
    return obligaciones

def extraer_obligaciones_desde_archivo(ruta_archivo, extension):
    try:
        if extension == ".pdf":
            with open(ruta_archivo, "rb") as archivo:
                lector = PyPDF2.PdfReader(archivo)
                texto = "\n".join([pagina.extract_text() for pagina in lector.pages if pagina.extract_text()])
        elif extension == ".docx":
            doc = Document(ruta_archivo)
            texto = "\n".join([p.text for p in doc.paragraphs])
        else:
            return None, "Formato no soportado."
    except Exception as e:
        return None, f"Error al leer el archivo: {e}"
    return extraer_obligaciones_especificas(texto), None

def manejar_subida_archivo(request):
    if request.method == "POST" and request.FILES.get("archivo"):
        archivo = request.FILES["archivo"]
        extension = os.path.splitext(archivo.name)[1].lower()
        ruta_guardada = default_storage.save(f"temp/{archivo.name}", archivo)
        ruta_completa = os.path.join(default_storage.location, ruta_guardada)
        obligaciones, error = extraer_obligaciones_desde_archivo(ruta_completa, extension)
        os.remove(ruta_completa)
        return obligaciones, error
    return None, None

@login_required
def generar_pdf(request):
    templates = ["cuenta_de_cobro.html", "informe_actividades.html", "calidad_tributaria.html"]
    html_content = ""
    for template_name in templates:
        template = get_template(template_name)
        html_content += template.render({"request": request})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=Cuenta_Cobro.pdf"
    pdf_file = HTML(string=html_content).write_pdf()
    response.write(pdf_file)
    return response

@login_required
def visualizar_obligaciones(request):
    obligaciones, error = manejar_subida_archivo(request)
    if obligaciones is None:
        obligaciones = []
    obligaciones_enumeradas = list(enumerate(obligaciones, start=1))
    return render(request, "cuenta_cobro/documento.html", {
        "obligaciones": obligaciones_enumeradas,
        "error": error
    })

@login_required
def subir_obligaciones(request):
    obligaciones, error = manejar_subida_archivo(request)
    if obligaciones:
        contrato = Contrato.objects.first()
        for index, obligacion in enumerate(obligaciones, start=1):
            ContratoObligacion.objects.create(contrato=contrato, descripcion=obligacion, orden=index)
        return render(request, "cuenta_cobro/documento.html", {"mensaje": "Obligaciones procesadas correctamente."})
    return render(request, "cuenta_cobro/documento.html", {"error": error})

@login_required
def ver_cuenta_cobro(request, cuenta_id):
    cuenta = get_object_or_404(CuentaCobro, id=cuenta_id)
    obligaciones = CuentaCobroObligacion.objects.filter(cuenta_cobro=cuenta)
    planilla = PagoPlanilla.objects.filter(cuenta_cobro=cuenta).first()
    return render(request, "cuenta_cobro/detalle.html", {
        "cuenta": cuenta,
        "obligaciones": obligaciones,
        "planilla": planilla
    })

@login_required
def listado_cuentas_cobro(request):
    persona = get_object_or_404(Persona, usuario=request.user)
    cuentas = CuentaCobro.objects.filter(contrato__persona=persona)
    return render(request, "cuenta_cobro/listado.html", {"cuentas": cuentas})

@login_required
def generar_cuenta_cobro(request):
    persona = get_object_or_404(Persona, usuario=request.user)
    contratos = Contrato.objects.filter(persona=persona)
    if request.method == "POST":
        contrato = get_object_or_404(Contrato, id=request.POST.get("contrato"))
        numero_pago = CuentaCobro.objects.filter(contrato=contrato).count() + 1
        nueva_cuenta = CuentaCobro.objects.create(
            contrato=contrato,
            numero_pago=numero_pago,
            estado="supervision",
            valor_total=request.POST.get("valor_total", 0),
        )
        preguntas, _ = PreguntasFiscales.objects.get_or_create(persona=persona)
        preguntas.soy_pensionado = request.POST.get("soy_pensionado") == "True"
        preguntas.devolucion_saldos = request.POST.get("devolucion_saldos") == "True"
        preguntas.declarante_renta = request.POST.get("declarante_renta") == "True"
        preguntas.save()
        obligaciones_ids = request.POST.getlist("obligacion_id[]")
        actividades = request.POST.getlist("actividad[]")
        productos = request.POST.getlist("producto[]")
        metodos = request.POST.getlist("metodo_verificacion[]")
        for i, obligacion_id in enumerate(obligaciones_ids):
            CuentaCobroObligacion.objects.create(
                cuenta_cobro=nueva_cuenta,
                obligacion_id=ContratoObligacion.objects.get(id=obligacion_id),
                actividad=actividades[i] if i < len(actividades) else "",
                producto=productos[i] if i < len(productos) else "",
                metodo_verificacion=metodos[i] if i < len(metodos) else "",
            )
        return redirect("cuenta_cobro:listado_cuentas_cobro")
    return render(request, "cuenta_cobro/generar.html", {"contratos": contratos})

@login_required
def datos_contrato(request, contrato_id):
    contrato = get_object_or_404(Contrato, id=contrato_id)
    datos = {
        "responsable": f"{contrato.persona.primer_nombre} {contrato.persona.apellido_paterno}",
        "valor_total": str(contrato.valor_total_con_adiciones or contrato.valor_inicial_contrato),
        "fecha_inicio": contrato.fecha_inicio.strftime("%d/%m/%Y"),
        "fecha_fin": contrato.fecha_terminacion.strftime("%d/%m/%Y"),
    }
    return JsonResponse(datos)

@login_required
def obtener_obligaciones_por_contrato(request, contrato_id):
    obligaciones = ContratoObligacion.objects.filter(contrato_id=contrato_id).order_by('orden').values("id", "descripcion", "orden")
    return JsonResponse({"obligaciones": list(obligaciones)})