from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, PersonaFormCompleto, PersonaForm
from .models import Usuario, Persona
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.middleware.csrf import rotate_token
from django.contrib.auth import update_session_auth_hash
from .forms import CustomPasswordChangeForm

Usuario = get_user_model()

# ===================vista para registro===================== #


def registro_view(request):
    if request.method == 'POST':
        user_form = RegistroForm(request.POST)
        persona_form = PersonaForm(request.POST)

        if user_form.is_valid() and persona_form.is_valid():
            try:
                username = user_form.cleaned_data['username']
                email = user_form.cleaned_data['email']
                documento = persona_form.cleaned_data['no_identificacion']

                # Verificar duplicados antes de guardar
                if Usuario.objects.filter(username=username).exists():
                    messages.error(
                        request, '❌ El nombre de usuario ya está en uso.')
                elif Usuario.objects.filter(email=email).exists():
                    messages.error(
                        request, '❌ El correo electrónico ya está registrado.')
                elif Persona.objects.filter(no_identificacion=documento).exists():
                    messages.error(
                        request, '❌ Ya existe una persona registrada con este número de documento.')
                else:
                    # Guardar usuario
                    user = user_form.save()

                    # Crear persona asociada
                    persona = persona_form.save(commit=False)
                    persona.usuario = user
                    persona.save()

                    messages.success(
                        request, '✅ Registro exitoso. Ahora puedes iniciar sesión.')
                    return redirect('login:login_view')

            except Exception as e:
                messages.error(request, f'❌ Error inesperado: {str(e)}')

        else:
            messages.error(
                request, '❌ El formulario contiene errores. Por favor, revísalo.')

    else:
        user_form = RegistroForm()
        persona_form = PersonaForm()

    return render(request, "login/registro.html", {
        'user_form': user_form,
        'persona_form': persona_form
    })
# ===================vista para login===================== #


def login_view(request):
    if request.user.is_authenticated:
        return redirect("login:dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido, {user.username}!")
            return redirect("login:dashboard")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "login/login.html")


# ===================vista para perfil===================== #

@login_required
def perfil(request):
    persona = get_object_or_404(Persona, usuario=request.user)

    if request.method == 'POST':
        password_form = CustomPasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, '✅ Contraseña actualizada correctamente.')
            return redirect('login:perfil')
    else:
        password_form = CustomPasswordChangeForm(request.user)

    return render(request, "login/perfil.html", {
        "usuario": request.user,
        "persona": persona,
        "password_form": password_form
    })

# ===================vista para Dashboard===================== #


@login_required
def dashboard_view(request):
    try:
        perfil = request.user.perfil
        rol = perfil.rol
    except Persona.DoesNotExist:
        messages.error(request, "⚠️ No se encontró un perfil asociado.")
        return redirect("completar_perfil")

    total_pendientes = Persona.objects.filter(
        evaluaciones__estado="Pendiente").count()
    total_aprobados = Persona.objects.filter(
        evaluaciones__estado="Aprobado").count()
    total_finalizados = Persona.objects.filter(
        evaluaciones__estado="Finalizado").count()

    dashboards_por_rol = {
        'contratista': "login/dashboard_vista.html",
        'alcaldesa': "login/dashboard_alcaldesa.html",
        'juridico': "login/dashboard_juridico.html",
        'contratacion': "login/dashboard_contratacion.html",
        'financiera': "login/dashboard_financiera.html",
        'despacho': "login/dashboard.html",
        'admin': "login/dashboard.html",
    }

    template = dashboards_por_rol.get(rol, "login/dashboard_vista.html")

    return render(request, template, {
        "user": request.user,
        "total_pendientes": total_pendientes,
        "total_aprobados": total_aprobados,
        "total_finalizados": total_finalizados,
    })

# ===================vista para completar perfil===================== #


@login_required
def completar_perfil(request):
    persona = get_object_or_404(Persona, usuario=request.user)

    if request.method == 'POST':
        form = PersonaFormCompleto(request.POST, instance=persona)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('dashboard')
    else:
        form = PersonaFormCompleto(instance=persona)

    return render(request, 'login/completar_perfil.html', {
        'persona_form': form,
        'persona': persona,
    })

# ===================cierre de sesión===================== #


@login_required
def logout_view(request):
    logout(request)
    rotate_token(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("login:login_view")

# ===================lista de usuarios===================== #


@login_required
def lista_usuarios(request):
    if not request.user.is_staff:
        raise PermissionDenied

    User = get_user_model()
    usuarios = User.objects.all()
    return render(request, 'login/lista_usuarios.html', {'usuarios': usuarios})
