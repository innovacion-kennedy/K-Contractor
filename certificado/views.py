from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from .models import Funcionario
from .forms import RegistroForm
from django.contrib.auth import get_user_model 
from login.models import Usuario , Persona
from weasyprint import HTML
import csv
import logging
from datetime import datetime


User = get_user_model() 

@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def gestionar_funcionario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    funcionarios = Funcionario.objects.all()
    
    # Obtener funcionario existente o None si es nuevo
    funcionario = Funcionario.objects.filter(usuario=usuario).first()
    
    if request.method == 'POST':
        # Manejar selección de funcionario existente
        if 'funcionario' in request.POST and request.POST['funcionario']:
            funcionario_id = request.POST['funcionario']
            try:
                funcionario = Funcionario.objects.get(id=funcionario_id)
                # Redirigir para editar el funcionario seleccionado
                return redirect('certificado:gestionar_funcionario', user_id=usuario.id)
            except Funcionario.DoesNotExist:
                messages.error(request, "El funcionario seleccionado no existe")
        
        # Manejar creación/actualización del formulario principal
        form = RegistroForm(request.POST, instance=funcionario)
        if form.is_valid():
            nuevo_funcionario = form.save(commit=False)
            nuevo_funcionario.usuario = usuario
            
            # Asignar valores por defecto para nuevos registros
            if not funcionario:  # Si es un nuevo funcionario
                nuevo_funcionario.estado = 'activo'  # Valor por defecto
                messages.success(request, "Funcionario creado exitosamente")
            else:
                messages.success(request, "Funcionario actualizado exitosamente")
            
            nuevo_funcionario.save()
            return redirect('certificado:generar_certificado', no_identificacion=nuevo_funcionario.no_identificacion)
    else:
        form = RegistroForm(instance=funcionario)
    
    return render(request, 'gestionar_funcionario.html', {
        'form': form,
        'usuario': usuario,
        'funcionarios': funcionarios,
        'funcionario': funcionario  # None si es nuevo
    })

@login_required
def generar_certificado(request, no_identificacion):
    funcionario = get_object_or_404(Funcionario, no_identificacion=no_identificacion)
    rendered = render_to_string('certificado_template.html', {
        'nombre': funcionario.primer_nombre,
        'no_identificacion': funcionario.no_identificacion,
        'sitio_expedicion': funcionario.sitio_expedicion,
        'CPS': funcionario.CPS,
        'objeto': funcionario.objeto,
        'obligaciones': funcionario.obligaciones,
        'vr_inicial_contrato': funcionario.vr_inicial_contrato,
        'valor_mensual_honorarios': funcionario.valor_mensual_honorarios,
        'fecha_inicio': funcionario.fecha_inicio,
        'fecha_terminacion': funcionario.fecha_terminacion,
        'fecha_suscripcion': funcionario.fecha_suscripcion,
        'tiempo_ejecucion_dia': funcionario.tiempo_ejecucion_dia,
        'año_contrato': funcionario.año_contrato,
        'radicado': funcionario.radicado,
        'correo': funcionario.correo,
        'fecha_terminacion_prorrogas': funcionario.fecha_terminacion_prorrogas,
        'plazo_total_ejecucion': funcionario.plazo_total_ejecucion,
        'cesion': funcionario.cesion,
        'suspensiones': funcionario.suspensiones,
        'estado': funcionario.estado
    })
    pdf = HTML(string=rendered, base_url=request.build_absolute_uri('/')).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=\"certificado_{no_identificacion}.pdf\"'
    return response


@login_required
def preview_certificado(request, no_identificacion):
    funcionario = get_object_or_404(Funcionario, no_identificacion=no_identificacion)
    return render(request, 'certificado_template.html', {'funcionario': funcionario})

@login_required
def listar_cedulas(request):
    funcionarios = Funcionario.objects.all()
    datos_funcionarios = [
        {'no_identificacion': funcionario.no_identificacion, 'nombre': funcionario.primer_nombre, 'CPS': funcionario.CPS, 'año_contrato': funcionario.año_contrato, 'usuario': funcionario.usuario}
        for funcionario in funcionarios
    ]
    return render(request, 'listar_cedulas.html', {'datos_usuarios': datos_funcionarios})

@login_required
def buscar_certificado(request):
    if request.method == 'POST':
        no_identificacion = request.POST.get('no_identificacion', '').strip()
        año = request.POST.get('año', '').strip()
        if not no_identificacion or not año:
            return render(request, 'resultado_busqueda.html', {'mensaje': 'Por favor, completa todos los campos.'})
        Funcionario_obj = Funcionario.objects.filter(no_identificacion=no_identificacion, año_contrato=año).first()
        if Funcionario_obj:
            return render(request, 'resultado_busqueda.html', {'Funcionario': Funcionario_obj})
        else:
            return render(request, 'resultado_busqueda.html', {'mensaje': 'Funcionario no encontrado. Por favor, crea un nuevo Funcionario.'})
    return render(request, 'buscar_cert.html')


logger = logging.getLogger(__name__)

@login_required
@require_http_methods(["GET", "POST"])
def cargar_csv(request):
    if request.method == 'POST':
        logger.info("Iniciando procesamiento de CSV")
        
        if 'file' not in request.FILES:
            logger.error("No se recibió archivo en la solicitud")
            return JsonResponse({
                'success': False,
                'mensaje': 'No se ha subido ningún archivo'
            }, status=400)
            
        file = request.FILES['file']
        logger.info(f"Archivo recibido: {file.name} ({file.size} bytes)")
        
        if not file.name.endswith('.csv'):
            logger.error("El archivo no es CSV")
            return JsonResponse({
                'success': False,
                'mensaje': 'El archivo debe ser un CSV'
            }, status=400)

        registros_procesados = 0
        errores = []
        
        try:
            # Leer el archivo directamente desde memoria
            content = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(content)
            
            for i, row in enumerate(reader, start=1):
                try:
                    logger.debug(f"Procesando fila {i}: {row}")
                    
                    # Convertir fechas
                    fecha_suscripcion = datetime.strptime(row['fecha_suscripcion'], '%Y-%m-%d').date()
                    fecha_inicio = datetime.strptime(row['fecha_inicio'], '%Y-%m-%d').date()
                    fecha_terminacion = datetime.strptime(row['fecha_terminacion'], '%Y-%m-%d').date()
                    
                    # 1. Crear o obtener usuario asociado
                    usuario, usuario_creado = User.objects.get_or_create(
                        username=row['no_identificacion'],
                        defaults={
                            'first_name': row['primer_nombre'],
                            'email': row.get('correo', ''),
                            'password': make_password(row['no_identificacion'])  # Password = número de identificación
                        }
                    )
                    
                    if usuario_creado:
                        logger.info(f"Usuario creado: {usuario.username} (ID: {usuario.id})")
                    
                    # 2. Crear o actualizar Persona
                    persona, persona_creada = Persona.objects.update_or_create(
                        no_identificacion=row['no_identificacion'],
                        defaults={
                            'usuario': usuario,
                            'primer_nombre': row['primer_nombre'],
                            'correo': row.get('correo', ''),
                            # Agrega aquí otros campos de Persona si son necesarios
                        }
                    )
                    
                    if persona_creada:
                        logger.info(f"Persona creada: {persona.no_identificacion}")
                    
                    # 3. Crear o actualizar Funcionario
                    funcionario, funcionario_creado = Funcionario.objects.update_or_create(
                        no_identificacion=row['no_identificacion'],
                        defaults={
                            'persona': persona,
                            'CPS': row['CPS'],
                            'sitio_expedicion': row['sitio_expedicion'],
                            'objeto': row['objeto'],
                            'obligaciones': row['obligaciones'],
                            'vr_inicial_contrato': float(row['vr_inicial_contrato']),
                            'valor_mensual_honorarios': float(row['valor_mensual_honorarios']),
                            'fecha_suscripcion': fecha_suscripcion,
                            'fecha_inicio': fecha_inicio,
                            'fecha_terminacion': fecha_terminacion,
                            'tiempo_ejecucion_dia': int(row['tiempo_ejecucion_dia']),
                            'año_contrato': row['año_contrato'],
                            'radicado': row.get('radicado', ''),
                            'correo': row.get('correo', '')
                        }
                    )
                    
                    if funcionario_creado:
                        logger.info(f"Funcionario creado: {funcionario.no_identificacion}")
                    else:
                        logger.info(f"Funcionario actualizado: {funcionario.no_identificacion}")
                    
                    registros_procesados += 1
                    
                except Exception as e:
                    error_msg = f"Fila {i}: {str(e)}"
                    errores.append(error_msg)
                    logger.error(error_msg)
                    continue
            
            logger.info(f"Procesamiento completado. {registros_procesados} registros procesados")
            
            return JsonResponse({
                'success': True,
                'mensaje': 'Archivo procesado correctamente',
                'registros_procesados': registros_procesados,
                'errores': errores
            })
            
        except Exception as e:
            logger.exception("Error al procesar el archivo CSV")
            return JsonResponse({
                'success': False,
                'mensaje': f'Error al procesar el archivo: {str(e)}'
            }, status=500)
    
    # Método GET - Mostrar formulario
    return render(request, 'cargar_csv.html')
   

@login_required
def descargar_csv(request):
    funcionarios = Funcionario.objects.all()  # Elimina select_related
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="funcionarios_completo.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'no_identificacion', 'primer_nombre', 'CPS', 'sitio_expedicion',
        'objeto', 'obligaciones', 'vr_inicial_contrato', 'valor_mensual_honorarios',
        'fecha_suscripcion', 'fecha_inicio', 'fecha_terminacion', 'tiempo_ejecucion_dia',
        'año_contrato', 'radicado', 'correo'
    ])
    
    for f in funcionarios:
        # Accede a los campos directamente del Funcionario
        writer.writerow([
            f.no_identificacion,
            f.primer_nombre,  # Asegúrate que este campo exista en Funcionario
            f.CPS,
            f.sitio_expedicion,
            f.objeto,
            f.obligaciones,
            f.vr_inicial_contrato,
            f.valor_mensual_honorarios,
            f.fecha_suscripcion.strftime('%Y-%m-%d'),
            f.fecha_inicio.strftime('%Y-%m-%d'),
            f.fecha_terminacion.strftime('%Y-%m-%d'),
            f.tiempo_ejecucion_dia,
            f.año_contrato,
            f.radicado,
            f.correo
        ])
    
    return response