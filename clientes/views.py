from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from urllib.parse import urlencode
from .models import Cliente, Cuentas
from .forms import ClienteForm, CuentasForm
from .filters import clientes_filtrar, cuentas_filtrar
from tabla.forms import ImportarCSVForm
from tabla.funcs import es_valido, email_valido
from perfiles.admin import agregar_a_errores
from perfiles.models import Perfil


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
            return redirect('clientes_listar')
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
@permission_required("clientes.cliente_importar", None, raise_exception=True)
def clientes_cargar_csv(request):
    errores_lista = []
    initial = {'entidades': (('CLIENTES', 'Clientes'), ),
               'entidad': 'Clientes'}
    if request.POST:
        form = ImportarCSVForm(request.POST, request.FILES, initial=initial)
        if form.is_valid():
            csv = request.FILES['archivo']
            entidad = form.cleaned_data['entidad']
            actualizados = 0
            nuevos = 0
            errores = 0
            exitos = 0
            msj = ''
            try:
                for cnt, line in enumerate(csv):
                    try:
                        line_aux = line.decode("utf-8-sig")
                        if line_aux:
                            values = line_aux.split(';')
                            clicod = values[0].replace("'", "")
                            clicod = clicod.replace('"', '')
                            if len(clicod) > 10:
                                clicod = clicod[0:10]
                            clicod = clicod.upper()
                            if cnt == 0:
                                print('*values: ', values)
                                print('*clicod: ', clicod)
                            nombre = ''
                            cuit = ''
                            domicilio = ''
                            telefono = ''
                            email = ''
                            if len(values) > 1:
                                nombre = values[1].replace("'", "").strip()
                                if len(nombre) > 100:
                                    nombre = nombre[0:97] + '...'
                                if len(values) > 2:
                                    cuit = values[2].strip()
                                    if len(values) > 3:
                                        domicilio = values[3].strip()
                                        if len(values) > 4:
                                            telefono = values[4].strip()
                                            if len(values) > 5:
                                                email = values[5].strip()
                            activo = 'S'
                            valor_preferencial = 'N'
                            try:
                                cliente = Cliente.objects.get(clicod=clicod)
                                cliente.clicod = clicod
                                if nombre:
                                    cliente.nombre = nombre.upper()
                                if domicilio:
                                    cliente.domicilio = domicilio.upper()
                                if telefono:
                                    cliente.telefono = telefono
                                if email:
                                    cliente.email = email
                                cliente.save()
                                actualizados += 1
                                exitos += 1
                            except Cliente.DoesNotExist:
                                cliente = Cliente(clicod=clicod,
                                                  nombre=nombre.upper(),
                                                  cuit=cuit,
                                                  domicilio=domicilio.upper(),
                                                  telefono=telefono,
                                                  email=email)
                                cliente.save()
                                nuevos += 1
                                exitos += 1

                            ok = True
                            if es_valido(email):
                                if email_valido(email):
                                    if User.objects.filter(email=email).exclude(username=clicod).exists():
                                        errores += 1
                                        e = 'El e-mail principal de ' + clicod + ' "' + email + \
                                            '" ya está asignado a otro usuario. ' + \
                                            'Se deja vacío'
                                        errores_lista = agregar_a_errores(cnt, errores, e, errores_lista)
                                        ok = False
                                else:
                                    errores += 1
                                    e = 'El e-mail principal de ' + clicod + ' "' + email + \
                                        '" no es válido. Se deja vacío'
                                    errores_lista = agregar_a_errores(cnt, errores, e, errores_lista)
                                    ok = False

                            if ok:
                                try:
                                    user = User.objects.get(username=clicod)
                                    user.first_name = nombre
                                    user.email = email
                                    user.save()
                                    actualizados += 1
                                    exitos += 1
                                except User.DoesNotExist:
                                    user = User.objects.create_user(username=clicod,
                                                                    first_name=nombre,
                                                                    email=email,
                                                                    is_active=True,
                                                                    )
                                    user.set_password('xadminweb')
                                    user.save()
                                    nuevos += 1
                                    exitos += 1
                                grupo = Group.objects.get(name='Clientes')
                                grupo.user_set.add(user)
                                perfil, creado = Perfil.objects.get_or_create(user_id=user.id)
                                perfil.clicod = clicod
                                perfil.save()

                    except Exception as e:
                        errores += 1
                        if errores <= 10:
                            if errores == 10:
                                errores_lista.append('Hay más errores...')
                            else:
                                errores_lista.append('Fila {}: {}'.format(cnt+1, e))
            except Exception as e:
                msj = e

            if msj:
                messages.add_message(request, messages.ERROR, msj)
            else:
                msj = 'Carga de {}: {} errores; {} actualizados; {} nuevos'.format(entidad, errores,
                                                                                   actualizados, nuevos)
                if errores_lista:
                    messages.add_message(request, messages.ERROR, msj)
                else:
                    messages.add_message(request, messages.INFO, msj)
                    return redirect('tablas_listar')
    else:
        form = ImportarCSVForm(initial=initial)

    template_name = 'tabla/tabla_form.html'
    formato = 'CliCod C(5) ; Nombre C(100); CUIT C(13); Domicilio C(60); Teléfono C(60); E-mail C(60) ' \
              'Codificación UTF-8'
    titulo = 'Importar CSV'
    contexto = {'form': form, 'formato': formato, 'errores': errores_lista, 'titulo': titulo}
    return render(request, template_name, contexto)


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
@permission_required("clientes.cuenta_corriente", None, raise_exception=True)
def cuenta_corriente(request):
    url = reverse('cuenta_')
    return redirect(url)


@login_required(login_url='ingresar')
@permission_required("clientes.cuentas_agrega", None, raise_exception=True)
def cuentas_agregar(request):
    url = reverse('cuentas_listar')
    if request.POST:
        form = CuentasForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cuentas_listar')
    else:
        form = CuentasForm()

    template_name = 'cuentas_form.html'

    return render(request, template_name, {'form': form})


@login_required(login_url='ingresar')
@permission_required("clientes.cuentas_editar", None, raise_exception=True)
def cuentas_editar(request, id):
    try:
        cuentas = Cuentas.objects.get(id=id)
    except Exception as mensaje:
        messages.add_message(request, messages.ERROR, mensaje)
        return redirect('cuentas_listar')

    if request.method == 'POST':
        post = request.POST.copy()
        form = CuentasForm(post, request.FILES, instance=cuentas)
        if form.is_valid():
            form.save()
            return redirect('cuentas_listar')
    else:
        form = CuentasForm(instance=cuentas)

    template_name = 'cuentas_form.html'
    contexto = {'form': form, 'MODELO': cuentas}
    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
@permission_required("clientes.cuentas_eliminar", None, raise_exception=True)
def cuentas_eliminar(request, id):
    url = 'cuentas_listar'
    try:
        cuentas = Cuentas.objects.get(id=id)
        cuentas.delete()
    except Exception as e:
        mensaje = 'No se puede eliminar porque el ítem está referenciado en ' \
                  'otros registros. Otra opción es desactivarlo'
        messages.add_message(request, messages.ERROR, mensaje)

    return redirect(url)