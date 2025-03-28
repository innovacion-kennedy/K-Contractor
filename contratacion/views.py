from .models import Convocatoria
from .forms import ConvocatoriaForm
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
from django.conf import settings
from .models import Documento, Contrato, Convocatoria, EvaluacionHV
from .forms import DocumentoForm, ConvocatoriaForm, ContratoForm, EvaluacionHVForm
from login.models import Persona
from login.forms import PersonaForm
from django.utils import timezone


@login_required
def registro_documentacion(request):
    """ Vista para gestionar la información del contratista y sus documentos """

    persona = get_object_or_404(Persona, usuario=request.user)
    documentos = Documento.objects.filter(contratista=persona)

    # Guardar datos del contratista
    if request.method == "POST" and "guardar_datos" in request.POST:
        persona_form = PersonaForm(request.POST, instance=persona)
        if persona_form.is_valid():
            persona_form.save()
            messages.success(
                request, "✅ Tus datos han sido guardados correctamente.")
            return redirect("contratacion:registro_documentacion")
        else:
            messages.error(
                request, "❌ Error al guardar los datos. Verifica los campos.")
    else:
        persona_form = PersonaForm(instance=persona)

    # Subida de documentos
    if request.method == "POST" and "subir_documento" in request.POST:
        documento_form = DocumentoForm(request.POST, request.FILES)
        if documento_form.is_valid():
            doc = documento_form.save(commit=False)
            doc.contratista = persona
            doc.estado = "Pendiente"
            doc.save()

            print(f"✅ Archivo guardado en: {doc.archivo.path}")

            messages.success(
                request, f"✅ Documento '{doc.tipo_documento}' subido correctamente.")
            return redirect("contratacion:registro_documentacion")
        else:
            messages.error(
                request, "❌ Error al subir el documento. Inténtalo de nuevo.")

    else:
        documento_form = DocumentoForm()

    return render(request, "contratacion/registro_documentacion.html", {
        "persona_form": persona_form,
        "documento_form": documento_form,
        "documentos": documentos,
    })


@login_required
def eliminar_documento(request, id):
    """✅ Elimina un documento de la base de datos y del sistema de archivos"""
    doc = get_object_or_404(
        # Verifica que sea del usuario actual
        Documento, id=id, contratista=request.user.perfil)

    # 📌 Elimina el archivo del sistema de archivos
    if doc.archivo:
        ruta_archivo = os.path.join(settings.MEDIA_ROOT, str(doc.archivo))
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)  # ✅ Eliminar archivo físicamente

    # 📌 Elimina el registro de la base de datos
    doc.delete()

    messages.success(request, "✅ Documento eliminado correctamente.")
    # 🔄 Recarga la página
    return redirect("contratacion:registro_documentacion")


@login_required
def actualizar_datos(request):
    persona = Persona.objects.get(usuario=request.user)
    if request.method == "POST":
        persona.eps = request.POST.get("eps")
        persona.fondo_pensiones = request.POST.get("fondo_pensiones")
        persona.save()
        messages.success(request, "Datos actualizados correctamente.")
    return redirect("contratacion:registro_documentacion")


@login_required
def eliminar_documento(request, id):
    doc = get_object_or_404(Documento, id=id)
    doc.delete()
    messages.success(request, "Documento eliminado correctamente.")
    return redirect("contratacion:registro_documentacion")


@login_required
def listado_Hv(request):
    query = request.GET.get("q", "")

    # Filtrar contratistas si se ingresó un término de búsqueda
    if query:
        contratistas = Persona.objects.filter(
            no_identificacion__icontains=query
        ) | Persona.objects.filter(
            primer_nombre__icontains=query
        ) | Persona.objects.filter(
            apellido_paterno__icontains=query
        )
    else:
        contratistas = Persona.objects.all()

    # 🔹 Agregamos la fecha de la "Hoja de Vida" a cada contratista
    for persona in contratistas:
        documentos = persona.documentos.filter(
            tipo_documento="Hoja de Vida").order_by("fecha_carga")
        persona.fecha_hoja_vida = documentos.first(
        ).fecha_carga if documentos.exists() else None

    return render(request, "contratacion/listado_Hv.html", {
        "contratistas": contratistas,
        "query": query,
    })


@login_required
def detalle_contratista(request, id):
    persona = get_object_or_404(Persona, id=id)
    return render(request, 'contratacion/detalle_contratista.html', {'persona': persona})


@login_required
def asociar_contratista(request, contratista_id, convocatoria_id):
    """
    Asocia un contratista a una convocatoria.
    """
    contratista = get_object_or_404(Persona, id=contratista_id)
    convocatoria = get_object_or_404(Convocatoria, id=convocatoria_id)

    if request.method == "POST":
        # 📌 Crear la evaluación si no existe y registrar fecha de asociación
        evaluacion, created = EvaluacionHV.objects.get_or_create(
            contratista=contratista,
            convocatoria=convocatoria,
            # ✅ Guardar fecha de asociación
            defaults={"fecha_asociacion": timezone.now()}
        )

        # 📌 Si ya existía, actualizar la fecha de asociación solo si no tenía una
        if not created and not evaluacion.fecha_asociacion:
            evaluacion.fecha_asociacion = timezone.now()
            evaluacion.save()

        messages.success(
            request, f"✅ {contratista.primer_nombre} ha sido asociado a la convocatoria '{convocatoria.titulo}'."
        )
        return redirect("contratacion:seleccionar_contratista", convocatoria_id=convocatoria.id)

    return redirect("contratacion:lista_convocatorias")


def seleccionar_contratista(request, convocatoria_id):
    convocatoria = get_object_or_404(Convocatoria, id=convocatoria_id)
    contratistas = Persona.objects.all()

    # ✅ Crear un diccionario con las evaluaciones asociadas a la convocatoria
    evaluaciones_dict = {
        ev.contratista.id: ev for ev in EvaluacionHV.objects.filter(convocatoria=convocatoria)
    }

    return render(request, "contratacion/seleccionar_contratista.html", {
        "convocatoria": convocatoria,
        "contratistas": contratistas,
        # 🔹 Pasamos el diccionario a la plantilla
        "evaluaciones_dict": evaluaciones_dict,
    })


def lista_contratos(request):
    contratos = Contrato.objects.all()
    return render(request, "contratacion/lista_contratos.html", {"contratos": contratos})


def crear_contrato(request):
    if request.method == "POST":
        form = ContratoForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirige a la lista de contratos después de crear uno
            return redirect("lista_contratos")
    else:
        form = ContratoForm()

    return render(request, "contratacion/crear_contrato.html", {"form": form})


def editar_contrato(request, id):
    # Busca el contrato o devuelve un 404
    contrato = get_object_or_404(Contrato, id=id)
    if request.method == "POST":
        form = ContratoForm(request.POST, instance=contrato)
        if form.is_valid():
            form.save()
            # Redirige a la lista de contratos
            return redirect("lista_contratos")
    else:
        form = ContratoForm(instance=contrato)

    return render(request, "contratacion/editar_contrato.html", {"form": form, "contrato": contrato})


def eliminar_contrato(request, id):
    # Busca el contrato o devuelve 404
    contrato = get_object_or_404(Contrato, id=id)

    if request.method == "POST":  # Si confirma la eliminación
        contrato.delete()
        return redirect("lista_contratos")  # Redirige a la lista de contratos

    return render(request, "contratacion/eliminar_contrato.html", {"contrato": contrato})


# ✅ Listar Convocatorias
@login_required
def lista_convocatorias(request):
    convocatorias = Convocatoria.objects.all().order_by('-fecha_creacion')
    return render(request, 'contratacion/lista_convocatorias.html', {'convocatorias': convocatorias})


@login_required
def crear_convocatoria(request):
    if request.method == 'POST':
        form = ConvocatoriaForm(request.POST, request.FILES)
        if form.is_valid():
            convocatoria = form.save(commit=False)
            convocatoria.creada_por = request.user
            convocatoria.save()
            messages.success(request, "Convocatoria creada con éxito.")
            # ✅ Redirigir a la misma página
            return redirect('contratacion:crear_convocatoria')
    else:
        form = ConvocatoriaForm()

    # 🔹 Pasar todas las convocatorias a la plantilla
    convocatorias = Convocatoria.objects.all().order_by('-fecha_creacion')

    return render(request, 'contratacion/crear_convocatoria.html', {'form': form, 'convocatorias': convocatorias})

# ✅ Editar Convocatoria


@login_required
def editar_convocatoria(request, id):
    convocatoria = get_object_or_404(Convocatoria, id=id)
    if request.method == 'POST':
        form = ConvocatoriaForm(
            request.POST, request.FILES, instance=convocatoria)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Convocatoria actualizada correctamente.")
            return redirect('contratacion:lista_convocatorias')
    else:
        form = ConvocatoriaForm(instance=convocatoria)
    return render(request, 'contratacion/editar_convocatoria.html', {'form': form, 'convocatoria': convocatoria})

# ✅ Eliminar Convocatoria


@login_required
def eliminar_convocatoria(request, id):
    convocatoria = get_object_or_404(Convocatoria, id=id)
    if request.method == 'POST':
        convocatoria.delete()
        messages.success(request, "Convocatoria eliminada con éxito.")
        return redirect('contratacion:lista_convocatorias')
    return render(request, 'contratacion/eliminar_convocatoria.html', {'convocatoria': convocatoria})


@login_required
def eliminar_asociacion(request, contratista_id, convocatoria_id):
    """
    Elimina la asociación de un contratista con una convocatoria.
    """
    evaluacion = get_object_or_404(
        EvaluacionHV, contratista_id=contratista_id, convocatoria_id=convocatoria_id
    )

    if request.method == "POST":
        evaluacion.delete()
        messages.success(request, "❌ Asociación eliminada correctamente.")

    return redirect("contratacion:seleccionar_contratista", convocatoria_id=convocatoria_id)


@login_required
def detalle_convocatoria(request, id):
    convocatoria = get_object_or_404(Convocatoria, id=id)
    return render(request, 'contratacion/detalle_convocatoria.html', {'convocatoria': convocatoria})


@login_required
def evaluar_contratista(request, id):
    persona = get_object_or_404(Persona, id=id)

    # ✅ Verificar si el contratista tiene una convocatoria asociada
    convocatoria = Convocatoria.objects.filter(
        evaluaciones__contratista=persona).first()

    if not convocatoria:
        messages.error(
            request, "❌ El contratista no está asociado a ninguna convocatoria. Primero debe asignarlo a una convocatoria antes de evaluarlo.")
        # 🔄 Redirige a la lista de convocatorias
        return redirect("contratacion:lista_convocatorias")

    # ✅ Obtener evaluación existente o crearla
    evaluacion, created = EvaluacionHV.objects.get_or_create(
        contratista=persona, defaults={"convocatoria": convocatoria}
    )

    if request.method == "POST":
        form = EvaluacionHVForm(request.POST, instance=evaluacion)
        if form.is_valid():
            evaluacion = form.save(commit=False)
            evaluacion.evaluador = request.user
            evaluacion.save()
            messages.success(request, "✅ Evaluación guardada con éxito.")
            return redirect("contratacion:listado_Hv")
        else:
            messages.error(request, "❌ Error al guardar la evaluación.")
    else:
        form = EvaluacionHVForm(instance=evaluacion)

    return render(request, "contratacion/evaluar_contratista.html", {
        "form": form,
        "persona": persona,
        "convocatoria": convocatoria
    })


@login_required
def registro_documentacion(request):
    """ Vista para gestionar la información del contratista y sus documentos """

    persona = get_object_or_404(Persona, usuario=request.user)
    documentos = Documento.objects.filter(contratista=persona)

    # Obtener la evaluación si existe
    evaluacion = EvaluacionHV.objects.filter(contratista=persona).first()

    # Formulario de datos personales
    if request.method == "POST" and "guardar_datos" in request.POST:
        persona_form = PersonaForm(request.POST, instance=persona)
        if persona_form.is_valid():
            persona_form.save()
            messages.success(
                request, "✅ Tus datos han sido guardados correctamente.")
            return redirect("contratacion:registro_documentacion")
        else:
            messages.error(
                request, "❌ Error al guardar los datos. Verifica los campos.")
    else:
        # Asegurar que el formulario se inicialice correctamente
        persona_form = PersonaForm(instance=persona)

    # Subida de documentos
    if request.method == "POST" and "subir_documento" in request.POST:
        documento_form = DocumentoForm(request.POST, request.FILES)
        if documento_form.is_valid():
            doc = documento_form.save(commit=False)
            doc.contratista = persona
            doc.estado = "Pendiente"
            doc.save()
            messages.success(
                request, f"✅ Documento '{doc.tipo_documento}' subido correctamente.")
            return redirect("contratacion:registro_documentacion")
        else:
            messages.error(
                request, "❌ Error al subir el documento. Inténtalo de nuevo.")
    else:
        documento_form = DocumentoForm()

    return render(request, "contratacion/registro_documentacion.html", {
        "persona": persona,
        "persona_form": persona_form,
        "documento_form": documento_form,
        "documentos": documentos,
        "evaluacion": evaluacion,  # Pasamos la evaluación al template
    })


@login_required
def estado_evaluaciones(request):
    convocatorias = Convocatoria.objects.all()
    convocatoria_id = request.GET.get("convocatoria")

    if convocatoria_id:
        evaluaciones = EvaluacionHV.objects.filter(
            convocatoria_id=convocatoria_id)
    else:
        evaluaciones = EvaluacionHV.objects.all()

    total_pendientes = evaluaciones.filter(estado="Pendiente").count()
    total_aprobados = evaluaciones.filter(estado="Aprobado").count()
    total_finalizados = evaluaciones.filter(estado="Finalizado").count()

    return render(request, "contratacion/estado_evaluaciones.html", {
        "total_pendientes": total_pendientes,
        "total_aprobados": total_aprobados,
        "total_finalizados": total_finalizados,
        "evaluaciones": evaluaciones,
        "convocatorias": convocatorias,
    })
