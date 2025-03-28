from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CuentaCobro
from .forms import CuentaCobroForm


@login_required
def lista_cuentas(request):
    cuentas = CuentaCobro.objects.all()
    return render(request, 'cuentas_cobro/lista_cuentas.html', {'cuentas': cuentas})


@login_required
def crear_cuenta(request):
    if request.method == 'POST':
        form = CuentaCobroForm(request.POST)
        if form.is_valid():
            numero = form.cleaned_data['numero_cuenta']
            if CuentaCobro.objects.filter(numero_cuenta=numero).exists():
                messages.error(
                    request, "Error: El número de cuenta ya existe.")
            else:
                form.save()
                messages.success(request, "Cuenta de cobro creada con éxito.")
                return redirect('cuentas_cobro:lista_cuentas')
    else:
        form = CuentaCobroForm()
    return render(request, 'cuentas_cobro/crear_cuenta.html', {'form': form})


@login_required
def editar_cuenta(request, id):
    cuenta = get_object_or_404(CuentaCobro, id=id)
    if request.method == 'POST':
        form = CuentaCobroForm(request.POST, instance=cuenta)
        if form.is_valid():
            numero = form.cleaned_data['numero_cuenta']
            if CuentaCobro.objects.exclude(id=id).filter(numero_cuenta=numero).exists():
                messages.error(
                    request, "Error: El número de cuenta ya existe en otro registro.")
            else:
                form.save()
                messages.success(
                    request, "Cuenta de cobro actualizada con éxito.")
                return redirect('cuentas_cobro:lista_cuentas')
    else:
        form = CuentaCobroForm(instance=cuenta)
    return render(request, 'cuentas_cobro/editar_cuenta.html', {'form': form, 'cuenta': cuenta})


@login_required
def eliminar_cuenta(request, id):
    cuenta = get_object_or_404(CuentaCobro, id=id)
    if request.method == 'POST':
        cuenta.delete()
        messages.success(request, "Cuenta de cobro eliminada correctamente.")
        return redirect('cuentas_cobro:lista_cuentas')
    return render(request, 'cuentas_cobro/eliminar_cuenta.html', {'cuenta': cuenta})
