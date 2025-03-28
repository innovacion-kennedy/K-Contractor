from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, PersonaForm
from .models import Usuario, Persona


def registro_view(request):
    """
    Vista para registrar nuevos usuarios y crear su perfil automáticamente.
    """
    if request.method == "POST":
        user_form = RegistroForm(request.POST)
        persona_form = PersonaForm(request.POST)

        if user_form.is_valid() and persona_form.is_valid():
            # 🔹 Guardar el usuario
            user = user_form.save()

            # 🔹 Crear la persona y asignarla al usuario
            persona = persona_form.save(commit=False)
            persona.usuario = user
            persona.solicita_permiso_especial = request.POST.get(
                "solicita_permiso_especial") == "on"
            persona.save()

            print(f"✅ Perfil creado para {user.username}")

            # 🔹 Mensaje si solicitó permiso especial
            if persona.solicita_permiso_especial:
                messages.info(
                    request, "Solicitud enviada, pendiente de autorización del administrador."
                )

            # 🔹 Redirigir al login después del registro
            return redirect("login")

    else:
        user_form = RegistroForm()
        persona_form = PersonaForm()

    return render(request, "login/registro.html", {"user_form": user_form, "persona_form": persona_form})


def login_view(request):
    """
    Vista para manejar el inicio de sesión.
    """
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido, {user.username}!")

            # 🔹 Verifica si el usuario tiene permiso especial aprobado
            if user.perfil.solicita_permiso_especial:
                if user.perfil.permiso_aprobado:
                    # ✅ Si el admin aprobó, va a `dashboard.html`
                    return redirect("dashboard")
                else:
                    messages.info(
                        request, "Tu solicitud de permiso está pendiente de aprobación por el administrador.")
                    # ✅ Si no ha sido aprobado, sigue en `dashboard_vista.html`
                    return redirect("dashboard_vista")
            else:
                # ✅ Usuarios sin solicitud van a `dashboard_vista.html`
                return redirect("dashboard_vista")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "login/login.html")


@login_required
def perfil(request):
    try:
        persona = Persona.objects.get(usuario=request.user)
    except Persona.DoesNotExist:
        persona = None  # Si no existe, asignamos None

    # 🚀 IMPRIMIR LOS DATOS PARA DEPURACIÓN
    print("📌 DEBUG: Verificando usuario en la vista")
    print(f"🔹 Usuario: {request.user.username}, Email: {request.user.email}")

    if persona:
        print(
            f"🔹 Persona: {persona.primer_nombre} {persona.apellido_paterno} - ID: {persona.no_identificacion}")
    else:
        print("❌ No se encontró una Persona asociada a este usuario.")

    return render(request, "login/perfil.html", {
        "usuario": request.user,
        "persona": persona,
    })


@login_required
def dashboard_view(request):
    """
    Redirige al usuario al dashboard correcto según su permiso especial
    y muestra el conteo de contratistas en cada estado.
    """
    # Contar estados desde el modelo Evaluacion si allí se guarda el estado
    total_pendientes = Persona.objects.filter(
        evaluaciones__estado="Pendiente").count()
    total_aprobados = Persona.objects.filter(
        evaluaciones__estado="Aprobado").count()
    total_finalizados = Persona.objects.filter(
        evaluaciones__estado="Finalizado").count()

    # Verifica si el usuario tiene permisos especiales
    if request.user.perfil.solicita_permiso_especial:
        template = "login/dashboard.html"
    else:
        template = "login/dashboard_vista.html"

    return render(request, template, {
        "user": request.user,
        "total_pendientes": total_pendientes,
        "total_aprobados": total_aprobados,
        "total_finalizados": total_finalizados,
    })


@login_required
def logout_view(request):
    """
    Cierra la sesión del usuario y redirige al login.
    """
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("login")


@login_required
def perfil_view(request):
    """
    Muestra el perfil del usuario.
    """
    return render(request, "login/perfil.html", {"user": request.user})
