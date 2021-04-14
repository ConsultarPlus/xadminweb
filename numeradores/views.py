from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .funcs import get_numero
from .models import Numerador
from .filters import numerador_filtrar
from .forms import NumeradorForm


def numerador_prueba(request):
    numero = get_numero(9, 'EXPEDIENTE')
    return redirect('menu')


@login_required(login_url='ingresar')
@permission_required("numeradores.numerador_puede_listar", None, raise_exception=True)
def numeradores_listar(request):
    contexto = numerador_filtrar(request)
    return render(request, 'numeradores_listar.html', contexto)


@login_required(login_url='ingresar')
def numerador_agregar(request):
    if request.POST:
        form = NumeradorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('numeradores_listar')
    else:
        form = NumeradorForm()
        template_name = 'numerador_form.html'
        return render(request, template_name, {'form': form})


@login_required(login_url='ingresar')
def numerador_editar(request, comprobante):
    try:
        numerador = Numerador.objects.get(comprobante=comprobante)
    except Exception as mensaje:
        messages.add_message(request, messages.ERROR, mensaje)
        return redirect('numeradores_listar')

    if request.method == 'POST':
        post = request.POST.copy()
        form = NumeradorForm(post, instance=numerador)
        if form.is_valid():
            form.save()
            return redirect('numeradores_listar')
    else:
        template_name = 'numerador_form.html'
        form = NumeradorForm(instance=numerador)
        return render(request, template_name, {'form': form, 'numerador': numerador})


@login_required(login_url='ingresar')
def numerador_eliminar(request, comprobante):
    numerador = Numerador.objects.get(comprobante=comprobante)
    url = 'numeradores_listar'
    try:
        numerador.delete()
    except Exception as e:
        mensaje = 'No se puede eliminar porque el ítem está referenciado en ' \
                  'otros registros. Otra opción es desactivarlo'
        messages.add_message(request, messages.ERROR, mensaje)

    return redirect(url)
