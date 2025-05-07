from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from login.models import Persona
from .models import Convocatoria, Documento, Contrato, EvaluacionHV
from .forms import DocumentoForm, ConvocatoriaForm, ContratoForm, EvaluacionHVForm
from login.forms import PersonaFormCompleto
import os


@login_required
def registro_documentacion(request):
    persona = get_object_or_404(Persona, usuario=request.user)
    documentos = Documento.objects.filter(contratista=persona)

    if request.method == "POST" and "guardar_datos" in request.POST:
        persona_form = PersonaFormCompleto(request.POST, instance=persona)
        if persona_form.is_valid():
            persona_form.save()
            messages.success(
                request, "✅ Tus datos han sido guardados correctamente.")
            return redirect("contratacion:registro_documentacion")
        else:
            messages.error(
                request, "❌ Error al guardar los datos. Verifica los campos.")
    else:
        persona_form = PersonaFormCompleto(instance=persona)

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
        "persona_form": persona_form,
        "documento_form": documento_form,
        "documentos": documentos,
    })


@login_required
def eliminar_documento(request, id):
    doc = get_object_or_404(Documento, id=id, contratista=request.user.perfil)
    if doc.archivo:
        ruta_archivo = os.path.join(settings.MEDIA_ROOT, str(doc.archivo))
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)
    doc.delete()
    messages.success(request, "✅ Documento eliminado correctamente.")
    return redirect("contratacion:registro_documentacion")


@login_required
def actualizar_datos(request):
    persona = Persona.objects.get(usuario=request.user)
    if request.method == "POST":
        persona.eps = request.POST.get("eps")
        persona.fondo_pensiones = request.POST.get("fondo_pensiones")
        persona.save()
        messages.success(request, "✅ Datos actualizados correctamente.")
    return redirect("contratacion:registro_documentacion")


@login_required
def listado_Hv(request):
    query = request.GET.get("q", "")
    if query:
        contratistas = Persona.objects.filter(
            no_identificacion__icontains=query
        ) | Persona.objects.filter(
            nombre1__icontains=query
        ) | Persona.objects.filter(
            apellido1__icontains=query
        )
    else:
        contratistas = Persona.objects.all()

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
    contratista = get_object_or_404(Persona, id=contratista_id)
    convocatoria = get_object_or_404(Convocatoria, id=convocatoria_id)

    if request.method == "POST":
        evaluacion, created = EvaluacionHV.objects.get_or_create(
            contratista=contratista,
            convocatoria=convocatoria,
            defaults={"fecha_asociacion": timezone.now()}
        )
        if not created and not evaluacion.fecha_asociacion:
            evaluacion.fecha_asociacion = timezone.now()
            evaluacion.save()

        messages.success(
            request,
            f"✅ {contratista.nombre1} ha sido asociado a la convocatoria '{convocatoria.titulo}'."
        )
        return redirect("contratacion:seleccionar_contratista", convocatoria_id=convocatoria.id)

    return redirect("contratacion:lista_convocatorias")


@login_required
def seleccionar_contratista(request, convocatoria_id):
    convocatoria = get_object_or_404(Convocatoria, id=convocatoria_id)
    contratistas = Persona.objects.all()
    evaluaciones = EvaluacionHV.objects.filter(convocatoria=convocatoria)
    evaluaciones_dict = {ev.contratista.id: ev for ev in evaluaciones}

    contratistas_info = []
    for persona in contratistas:
        evaluacion = evaluaciones_dict.get(persona.id)
        contratistas_info.append({
            'persona': persona,
            'evaluacion': evaluacion,
        })

    return render(request, "contratacion/seleccionar_contratista.html", {
        "convocatoria": convocatoria,
        "contratistas_info": contratistas_info,
    })


@login_required
def lista_contratos(request):
    contratos = Contrato.objects.all()
    return render(request, "contratacion/lista_contratos.html", {"contratos": contratos})


@login_required
def crear_contrato(request):
    if request.method == "POST":
        form = ContratoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("contratacion:lista_contratos")
    else:
        form = ContratoForm()
    return render(request, "contratacion/crear_contrato.html", {"form": form})


@login_required
def editar_contrato(request, id):
    contrato = get_object_or_404(Contrato, id=id)
    if request.method == "POST":
        form = ContratoForm(request.POST, instance=contrato)
        if form.is_valid():
            form.save()
            return redirect("contratacion:lista_contratos")
    else:
        form = ContratoForm(instance=contrato)
    return render(request, "contratacion/editar_contrato.html", {"form": form, "contrato": contrato})


@login_required
def eliminar_contrato(request, id):
    contrato = get_object_or_404(Contrato, id=id)
    if request.method == "POST":
        contrato.delete()
        return redirect("contratacion:lista_contratos")
    return render(request, "contratacion/eliminar_contrato.html", {"contrato": contrato})


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
            messages.success(request, "✅ Convocatoria creada con éxito.")
            return redirect('contratacion:crear_convocatoria')
    else:
        form = ConvocatoriaForm()

    convocatorias = Convocatoria.objects.all().order_by('-fecha_creacion')
    return render(request, 'contratacion/crear_convocatoria.html', {'form': form, 'convocatorias': convocatorias})


@login_required
def editar_convocatoria(request, id):
    convocatoria = get_object_or_404(Convocatoria, id=id)
    if request.method == 'POST':
        form = ConvocatoriaForm(
            request.POST, request.FILES, instance=convocatoria)
        if form.is_valid():
            form.save()
            messages.success(
                request, "✅ Convocatoria actualizada correctamente.")
            return redirect('contratacion:lista_convocatorias')
    else:
        form = ConvocatoriaForm(instance=convocatoria)

    return render(request, 'contratacion/editar_convocatoria.html', {'form': form, 'convocatoria': convocatoria})


@login_required
def eliminar_convocatoria(request, id):
    convocatoria = get_object_or_404(Convocatoria, id=id)
    if request.method == 'POST':
        convocatoria.delete()
        messages.success(request, "✅ Convocatoria eliminada con éxito.")
        return redirect('contratacion:lista_convocatorias')
    return render(request, 'contratacion/eliminar_convocatoria.html', {'convocatoria': convocatoria})


@login_required
def eliminar_asociacion(request, contratista_id, convocatoria_id):
    evaluacion = get_object_or_404(
        EvaluacionHV, contratista_id=contratista_id, convocatoria_id=convocatoria_id)
    if request.method == "POST":
        evaluacion.delete()
        messages.success(request, "✅ Asociación eliminada correctamente.")
        return redirect("contratacion:seleccionar_contratista", convocatoria_id=convocatoria_id)
    return render(request, "contratacion/confirmar_eliminacion_asociacion.html", {"evaluacion": evaluacion})


@login_required
def evaluar_contratista(request, id):
    persona = get_object_or_404(Persona, id=id)
    convocatoria = Convocatoria.objects.filter(
        evaluaciones__contratista=persona).first()

    if not convocatoria:
        messages.error(
            request, "❌ El contratista no está asociado a ninguna convocatoria.")
        return redirect("contratacion:lista_convocatorias")

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
            messages.error(
                request, "❌ Hubo un error al guardar la evaluación.")

    else:
        form = EvaluacionHVForm(instance=evaluacion)

    return render(request, "contratacion/evaluar_contratista.html", {
        "form": form,
        "persona": persona,
        "convocatoria": convocatoria,
    })


@login_required
def estado_evaluaciones(request):
    convocatoria_id = request.GET.get("convocatoria")
    if convocatoria_id:
        evaluaciones = EvaluacionHV.objects.filter(
            convocatoria_id=convocatoria_id)
    else:
        evaluaciones = EvaluacionHV.objects.all()

    total_pendientes = evaluaciones.filter(estado="Pendiente").count()
    total_aprobados = evaluaciones.filter(estado="Aprobado").count()
    total_finalizados = evaluaciones.filter(estado="Finalizado").count()

    convocatorias = Convocatoria.objects.all()

    return render(request, "contratacion/estado_evaluaciones.html", {
        "evaluaciones": evaluaciones,
        "total_pendientes": total_pendientes,
        "total_aprobados": total_aprobados,
        "total_finalizados": total_finalizados,
        "convocatorias": convocatorias,
    })


@login_required
def detalle_convocatoria(request, id):
    convocatoria = get_object_or_404(Convocatoria, id=id)
    return render(request, 'contratacion/detalle_convocatoria.html', {'convocatoria': convocatoria})


@login_required
def tablero_control(request):
    total_pendientes = EvaluacionHV.objects.filter(estado='Pendiente').count()
    total_aprobados = EvaluacionHV.objects.filter(estado='Aprobado').count()
    total_finalizados = EvaluacionHV.objects.filter(
        estado='Finalizado').count()
    total_personas = Persona.objects.count()
    total_convocatorias = Convocatoria.objects.count()

    convocatorias_con_asociado = Convocatoria.objects.filter(
        evaluaciones__fecha_asociacion__isnull=False
    ).distinct().count()
    convocatorias_sin_asociado = max(
        0, total_convocatorias - convocatorias_con_asociado)

    data_chart = {
        "labels": ["Pendientes", "Aprobados", "Finalizados"],
        "data": [total_pendientes, total_aprobados, total_finalizados]
    }
    data_convocatorias = {
        "labels": ["Asociada", "Sin Asociar"],
        "data": [convocatorias_con_asociado, convocatorias_sin_asociado]
    }

    context = {
        'total_pendientes': total_pendientes,
        'total_aprobados': total_aprobados,
        'total_finalizados': total_finalizados,
        'data_chart': data_chart,
        'data_convocatorias': data_convocatorias,
        'total_personas': total_personas,
    }

    return render(request, 'contratacion/tablero_control.html', context)
