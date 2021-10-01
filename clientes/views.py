from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from urllib.parse import urlencode
from .models import Cliente, Cuentas
from .forms import ClienteForm
from .filters import clientes_filtrar, cuentas_filtrar


# Create your views here.
@login_required(login_url='ingresar')
@permission_required('clientes.puede_listar', None, raise_exception=True)
def clientes_listar(request):
    contexto = clientes_filtrar(request)
    modo = request.GET.get('modo')
    contexto['modo'] = modo

    if modo == 'm' or modo == 's':
        template_name = 'clientes_list_block.html'
    else:
        template_name = 'clientes_listar.html'

    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
@permission_required("clientes.cliente_agregar", None, raise_exception=True)
def cliente_agregar(request):
    url = reverse('cliente_agregar')
    if request.POST:
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes_listar')
    else:
        form = ClienteForm()

    template_name = 'cliente_form.html'

    return render(request, template_name, {'form': form})


@login_required(login_url='ingresar')
@permission_required("clientes.cliente_editar", None, raise_exception=True)
def cliente_editar(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Exception as mensaje:
        messages.add_message(request, messages.ERROR, mensaje)
        return redirect('clientes_listar')

    if request.method == 'POST':
        post = request.POST.copy()
        form = ClienteForm(post, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('MODELOs_listar')
    else:
        form = ClienteForm(instance=cliente)

    template_name = 'cliente_form.html'
    contexto = {'form': form, 'MODELO': cliente}
    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
@permission_required("clientes.cliente_eliminar", None, raise_exception=True)
def cliente_eliminar(request, id):
    url = 'clientes_listar'
    try:
        cliente = Cliente.objects.get(id=id)
        cliente.delete()
    except Exception as e:
        mensaje = 'No se puede eliminar porque el ítem está referenciado en ' \
                  'otros registros. Otra opción es desactivarlo'
        messages.add_message(request, messages.ERROR, mensaje)

    return redirect(url)


@login_required(login_url='ingresar')
@permission_required("clientes.cliente_agregar", None, raise_exception=True)
def cliente_agregar_y_volver(request):
    url = reverse('cliente_agregar')
    parametros = urlencode({'volver': True})
    url = '{}?{}'.format(url, parametros)
    return redirect(url)


@login_required(login_url='ingresar')
@permission_required("clientes.cuentas_listar", None, raise_exception=True)
def cuentas_listar(request, id=None):
    contexto = cuentas_filtrar(request)
    modo = request.GET.get('modo')
    contexto['modo'] = modo

    if modo == 'm' or modo == 's':
        template_name = 'cuentas_list_block.html'
    else:
        template_name = 'cuentas_listar.html'

    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
def cuentas_imprimir(request, id=None):
    contexto = cuentas_filtrar(request)
    modo = request.GET.get('modo')
    contexto['modo'] = modo

    if modo == 'm' or modo == 's':
        template_name = 'cuentas_list_block.html'
    else:
        template_name = 'cuentas_listar.html'

    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
@permission_required("clientes.cuenta_corriente", None, raise_exception=True)
def cuenta_corriente(request):
    url = reverse('cuenta_')
    return redirect(url)