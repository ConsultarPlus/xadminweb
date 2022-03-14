from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponse
from urllib.parse import urlencode
import os
from .models import Cliente, Cuentas, CuentasD, Articulo
from .forms import ClienteForm, CuentasForm
from .filters import clientes_filtrar, cuentas_filtrar, cuentasd_filtrar, articulos_filtrar
from tabla.forms import ImportarCSVForm
from tabla.funcs import es_valido, email_valido, saldo_total
from tabla.funcs import get_lett
from tabla.funcs import generar_qr
from perfiles.admin import agregar_a_errores
from perfiles.models import Perfil
import random
import string
from xadmin.settings import MEDIA_URL, DEBUG, BASE_DIR
from xadmin.settings import MEDIA_URL
from reportlab.pdfgen import canvas
import webbrowser
import json
import keyboard
from tabla.listas import IVAS
import csv


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
            encriptado = ''.join(random.choice(string.ascii_lowercase.join(string.digits)) for i in range(10))
            form.save()
            cliente = Cliente.objects.get(clicod=form.cleaned_data['clicod'])
            cliente.encriptado = encriptado
            cliente.save()
            return redirect('clientes_listar')
    else:
        form = ClienteForm()

    template_name = 'cliente_form.html'

    return render(request, template_name, {'form': form})


@login_required(login_url='ingresar')
# @permission_required("clientes.cliente_editar", None, raise_exception=True)
def cliente_editar(request, encriptado=None):
    try:
        cliente = Cliente.objects.get(encriptado=encriptado)
    except Exception as mensaje:
        messages.add_message(request, messages.ERROR, mensaje)
        return redirect('menu')

    if request.method == 'POST':
        post = request.POST.copy()
        form = ClienteForm(post, instance=cliente)
        post["encriptado"] = encriptado
        if form.is_valid():
            form.save()
            return redirect('menu')
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return redirect('menu')
    else:
        form = ClienteForm(instance=cliente)

    template_name = 'cliente_form.html'
    contexto = {'form': form, 'cliente': cliente}
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
    initial = {'entidades': (('CLIENTES', 'Clientes'),),
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
                            nombre = ''
                            cuit = ''
                            domicilio = ''
                            telefono = ''
                            email = ''
                            saldo_inicial = ''
                            fecha_saldo = ''
                            encriptado = ''
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
                                                if len(values) > 6:
                                                    saldo_inicial = values[6].strip()
                                                    if len(values) > 7:
                                                        fecha_saldo = values[7].strip()
                            activo = 'S'
                            valor_preferencial = 'N'
                            try:
                                cliente = Cliente.objects.get(clicod=clicod)
                                cliente.clicod = clicod
                                cliente.encriptado = ''.join(
                                    random.choice(string.ascii_lowercase.join(string.digits)) for i in range(10))
                                if nombre:
                                    cliente.nombre = nombre.upper()
                                if domicilio:
                                    cliente.domicilio = domicilio.upper()
                                if telefono:
                                    cliente.telefono = telefono
                                if email:
                                    cliente.email = email
                                if saldo_inicial:
                                    cliente.saldo_inicial = saldo_inicial
                                if fecha_saldo:
                                    cliente.fecha_saldo = fecha_saldo
                                if encriptado:
                                    encriptado = ''.join(
                                        random.choice(string.ascii_lowercase.join(string.digits)) for i in range(10))
                                cliente.save()
                                actualizados += 1
                                exitos += 1
                            except Cliente.DoesNotExist:
                                encriptado = ''.join(
                                    random.choice(string.ascii_lowercase.join(string.digits)) for i in range(10))
                                cliente = Cliente(clicod=clicod,
                                                  nombre=nombre.upper(),
                                                  cuit=cuit,
                                                  domicilio=domicilio.upper(),
                                                  telefono=telefono,
                                                  email=email,
                                                  saldo_inicial=saldo_inicial,
                                                  fecha_saldo=fecha_saldo,
                                                  encriptado=encriptado)
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
                                try:
                                    grupo = Group.objects.get(name='Clientes')
                                    grupo.user_set.add(user)
                                    perfil, creado = Perfil.objects.get_or_create(user_id=user.id)
                                    perfil.clicod = clicod
                                    perfil.save()
                                except Exception as e:
                                    e = 'Problemas con el grupo o el perfil.'
                                    errores_lista = agregar_a_errores(cnt, errores, e, errores_lista)

                    except Exception as e:
                        errores += 1
                        if errores <= 10:
                            if errores == 10:
                                errores_lista.append('Hay más errores...')
                            else:
                                errores_lista.append('Fila {}: {}'.format(cnt + 1, e))
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
    formato = 'CliCod C(5) ; Nombre C(100); CUIT C(13); Domicilio C(60); Teléfono C(60); E-mail C(60); Saldo N(12.2) ' \
              'Codificación UTF-8'
    titulo = 'Importar CSV'
    contexto = {'form': form, 'formato': formato, 'errores': errores_lista, 'titulo': titulo}
    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
def facturas_pendientes(request, encriptado=None):
    contexto = cuentas_filtrar(request, encriptado, True)
    modo = request.GET.get('modo')
    contexto['modo'] = modo
    contexto['facturas_pendientes'] = True

    if encriptado is None:
        return redirect('menu')

    if modo == 'm' or modo == 's':
        template_name = 'cuentas_list_block.html'
    else:
        template_name = 'cuentas_listar.html'

    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
@permission_required("expediente.expediente_exportar", None, raise_exception=True)
def cuentas_exportar(request):
    output = []
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Cuentas.csv"'
    writer = csv.writer(response, delimiter=";")
    filtrado = Cliente.objects.all()
    # CSV Data
    I = 0
    while I < len(filtrado):
        obj = filtrado[I]
        output.append([obj.clicod,
                       obj.nombre,
                       obj.cuit,
                       obj.domicilio,
                       obj.telefono,
                       obj.email,
                       obj.encriptado,
                       obj.tipoiva,
                       obj.fecha_saldo,
                       obj.saldo_inicial,
                       ])
        I = I + 1
    writer.writerows(output)
    return response


@login_required(login_url='ingresar')
@permission_required("expediente.expediente_exportar", None, raise_exception=True)
def cuentasd_exportar(request):
    output = []
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Cuentas_Detalle.csv"'
    writer = csv.writer(response, delimiter=";")
    filtrado = CuentasD.objects.all()
    # CSV Data
    I = 0
    while I < len(filtrado):
        obj = filtrado[I]
        output.append([obj.vtacod,
                       obj.articulo_id,
                       obj.cantidad,
                       obj.descripcion,
                       obj.precio])
        I = I + 1
    writer.writerows(output)
    return response


@login_required(login_url='ingresar')
@permission_required("expediente.expediente_exportar", None, raise_exception=True)
def facturas_exportar(request):
    output = []
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="facturas.csv"'
    writer = csv.writer(response, delimiter=";")
    filtrado = Cuentas.objects.all()
    # CSV Data
    I = 0
    while I < len(filtrado):
        obj = filtrado[I]
        output.append([obj.vtacod,
                       obj.comprobante,
                       obj.fecha_emision,
                       obj.fecha_vencimiento,
                       obj.total,
                       obj.concepto,
                       obj.pdf,
                       obj.cliente,
                       obj.cae,
                       obj.vencimiento_cae,
                       obj.cptedh,
                       obj.pendiente,
                       ])
        I = I + 1
    writer.writerows(output)
    return response


@login_required(login_url='ingresar')
def cuentas_listar(request, encriptado=None):
    contexto = cuentas_filtrar(request, encriptado)
    modo = request.GET.get('modo')
    contexto['modo'] = modo
    contexto['facturas_pendientes'] = True

    if encriptado is None:
        return redirect('menu')

    if modo == 'm' or modo == 's':
        template_name = 'cuentas_list_block.html'
    else:
        template_name = 'cuentas_listar.html'

    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
@permission_required("clientes.cuentas_listar_admin", None, raise_exception=True)
def cuentas_listar_admin(request):
    contexto = cuentas_filtrar(request, None, False)
    modo = request.GET.get('modo')
    contexto['modo'] = modo

    if modo == 'm' or modo == 's':
        template_name = 'cuentas_list_block.html'
    else:
        template_name = 'cuentas_listar.html'

    contexto['subir_cuentas'] = True
    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
def cuenta_corriente(request, encriptado=None):
    contexto = cuentas_filtrar(request, encriptado, False)
    modo = request.GET.get('modo')
    contexto['modo'] = modo
    contexto['cuenta_corriente'] = True

    if encriptado is None:
        return redirect('menu')

    if modo == 'm' or modo == 's':
        template_name = 'cuentas_list_block.html'
    else:
        template_name = 'cuentas_listar.html'

    cliente = Cliente.objects.get(encriptado=encriptado)

    if cliente.saldo_inicial is None:
        si = 0
    else:
        si = cliente.saldo_inicial

    contexto['saldo_inicial'] = si

    contexto['saldo_actual'] = saldo_total(si, cliente)

    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
def cuenta_detalle(request, id=None, encriptado=None):
    cuentas = Cuentas.objects.get(id=id)
    contexto = cuentasd_filtrar(request, cuentas.vtacod, False)
    modo = request.GET.get('modo')
    contexto['modo'] = modo

    comprobante = Cuentas.objects.get(id=id)

    contexto['comprobante'] = comprobante

    # contexto['fijar_imagen'] = get_preferencia(request.user, 'clientes', 'fijar_i', 'L', True)

    if encriptado is None:
        return redirect('menu')

    if modo == 'm' or modo == 's':
        template_name = 'cuentasD_list_block.html'
    else:
        template_name = 'cuentasD_listar.html'

    return render(request, template_name, contexto)


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
@permission_required("clientes.cuentas_agrega", None, raise_exception=True)
def cuentasd_importar(request):
    errores_lista = []
    initial = {'entidades': (('CUENTASD', 'CuentasD'),),
               'entidad': 'CuentasD'}
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
            listadecods = []
            try:
                for cnt, line in enumerate(csv):
                    line_aux = line.decode("utf-8-sig")
                    if line_aux:
                        values = line_aux.split(';')
                        vtacod = values[0].replace("'", "")
                        vtacod = vtacod.replace('"', '')
                        listadecods.append(vtacod)

                listadecods = list(dict.fromkeys(listadecods))
                for cod in listadecods:
                    cuentas = CuentasD.objects.filter(vtacod=cod)
                    for item in cuentas:
                        item.delete()

                for cnt, line in enumerate(csv):
                    line_aux = line.decode("utf-8-sig")
                    try:
                        values = line_aux.split(';')
                        vtacod = values[0].replace("'", "").replace('"', '')

                        if len(values) > 1:
                            artcod = values[1].strip()
                            try:
                                articulo = Articulo.objects.get(artcod=artcod)
                            except Exception as e:
                                articulo = Articulo(artcod=artcod)
                                articulo.save()
                            if len(values) > 2:
                                cantidad = values[2].strip()
                                if len(values) > 3:
                                    descripcion = values[3].strip()
                                    if len(values) > 4:
                                        precio = values[4].strip()

                        cuentasd = CuentasD(vtacod=vtacod,
                                            articulo=articulo,
                                            cantidad=cantidad,
                                            descripcion=descripcion,
                                            precio=precio)
                        cuentasd.save()
                        nuevos += 1
                        exitos += 1
                    except Exception as e:
                        errores += 1
                        if errores <= 10:
                            if errores == 10:
                                errores_lista.append('Hay más errores...')
                            else:
                                errores_lista.append('Fila {}: {}'.format(cnt + 1, e))
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
                    return redirect('cuentas_listar')
    else:
        form = ImportarCSVForm(initial=initial)

    template_name = 'tabla/tabla_form.html'
    formato = 'VtaCod N(8) ; Articulo C(20); Cantidad N(2); Precio N(10); ' \
              'Codificación UTF-8'
    titulo = 'Importar CSV'
    contexto = {'form': form, 'formato': formato, 'errores': errores_lista, 'titulo': titulo}
    return render(request, template_name, contexto)


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


@login_required(login_url='ingresar')
@permission_required("clientes.cuentas_importar", None, raise_exception=True)
def cuentas_importar(request):
    errores_lista = []
    initial = {'entidades': (('CUENTAS', 'Cuentas'),),
               'entidad': 'Cuentas'}
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
                            vtacod = values[0].replace("'", "")
                            vtacod = vtacod.replace('"', '')

                            comprobante = ''
                            pdf = ''
                            if len(values) > 1:
                                comprobante = values[1].strip()
                                if len(values) > 2:
                                    clicod = values[2].replace("'", "").strip()
                                    if len(values) > 3:
                                        fecha_emision = values[3].strip()
                                        if len(values) > 4:
                                            fecha_vencimiento = values[4].strip()
                                            if len(values) > 5:
                                                t = values[5].replace("'", "")
                                                total = float(t) / 10000
                                                if len(values) > 6:
                                                    concepto = values[6].strip()
                                                    if len(values) > 7:
                                                        cae = values[7].strip()
                                                        if len(values) > 8:
                                                            vto_cae = values[8].strip()
                                                            if len(values) > 9:
                                                                pdf = values[9].strip()
                                                                if len(values) > 10:
                                                                    cptedh = values[10].strip()
                                                                    if len(values) > 11:
                                                                        pendiente = values[11].strip()
                            try:
                                cuentas = Cuentas.objects.get(vtacod=vtacod)
                                if clicod:
                                    cliente = Cliente.objects.get(clicod=clicod)
                                    cuentas.cliente = cliente
                                if comprobante:
                                    cuentas.comprobante = comprobante.upper()
                                if fecha_emision:
                                    cuentas.fecha_emision = fecha_emision
                                if fecha_vencimiento:
                                    cuentas.fecha_vencimiento = fecha_vencimiento
                                if total:
                                    cuentas.total = total
                                if concepto:
                                    cuentas.concepto = concepto
                                if cae:
                                    cuentas.cae = cae
                                if vto_cae:
                                    if vto_cae == "":
                                        vto_cae = None
                                    cuentas.vencimiento_cae = vto_cae
                                if pdf:
                                    cuentas.pdf = pdf
                                if cptedh:
                                    cuentas.cptedh = cptedh
                                if pendiente:
                                    if pendiente == 'N':
                                        pendiente = False
                                    if pendiente == 'S':
                                        pendiente = True
                                    cuentas.pendiente = pendiente
                                cuentas.save()
                                actualizados += 1
                                exitos += 1
                            except Cuentas.DoesNotExist:
                                cliente = Cliente.objects.get(clicod=clicod)
                                if vto_cae == "":
                                    vto_cae = None
                                if pendiente == 'N':
                                    pendiente = False
                                if pendiente == 'S':
                                    pendiente = True
                                cuentas = Cuentas(vtacod=vtacod,
                                                  comprobante=comprobante,
                                                  cliente=cliente,
                                                  fecha_emision=fecha_emision,
                                                  fecha_vencimiento=fecha_vencimiento,
                                                  total=total,
                                                  concepto=concepto,
                                                  cae=cae,
                                                  vencimiento_cae=vto_cae,
                                                  pdf=pdf,
                                                  cptedh=cptedh,
                                                  pendiente=pendiente)
                                cuentas.save()
                                nuevos += 1
                                exitos += 1

                    except Exception as e:
                        errores += 1
                        if errores <= 10:
                            if errores == 10:
                                errores_lista.append('Hay más errores...')
                            else:
                                errores_lista.append('Fila {}: {}'.format(cnt + 1, e))
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
                    return redirect('cuentas_listar')
    else:
        form = ImportarCSVForm(initial=initial)

    template_name = 'tabla/tabla_form.html'
    formato = 'VtaCod N(8) ; Comprobante C(20); CliCod C(5); Emisión D(10); ' \
              'Vencimiento D(10); VtaTotal N(14.4); VtaConce C(255); VtaCAI C(20); Vto CAE D(10); PDF C(200); CpteCV C(1); Pendiente Boolean ' \
              'Codificación UTF-8'
    titulo = 'Importar CSV'
    contexto = {'form': form, 'formato': formato, 'errores': errores_lista, 'titulo': titulo}
    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
def imprimir_png(request, id, encriptado=None):
    print("Dir:" + BASE_DIR)
    comprobante = Cuentas.objects.get(id=id)
    validacion = Cliente.objects.get(clicod=comprobante.cliente)
    cliente = Cliente.objects.get(encriptado=encriptado)
    if validacion != cliente:
        keyboard.press_and_release('ctrl+w')
        return redirect("menu")
    else:
        dat = encriptado + format(id)
        nombre_de_archivo = dat + '.pdf'
        if DEBUG:
            carpeta_media = BASE_DIR + '\media\ '.strip()
            print("Funca:" + carpeta_media)
        else:
            carpeta_media = '/home/consultar/xadminweb/media/'

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="' + nombre_de_archivo + '"'
        doc = canvas.Canvas(response)

        fondo_factura = carpeta_media + "fondo_factura.png"
        doc.drawImage('{}'.format(fondo_factura), 0, -30, width=630, height=891)

        doc.setFontSize(16)
        doc.drawString(420, 753, '{}'.format(comprobante.fecha_emision))
        doc.drawString(400, 783, "Nº " + '{}'.format(comprobante.sucursal) + "-" + '{}'.format(comprobante.numero))
        doc.setFontSize(60)
        doc.drawString(280, 780, '{}'.format(comprobante.tipocmp), 2)
        doc.setFontSize(12)
        doc.drawString(50, 170, '{}'.format(comprobante.subtotal))

        tiva = cliente.tipoiva
        if tiva == "I" or tiva == "M" or tiva == "C":
            doc.drawString(275, 170, '{}'.format(comprobante.iva))
        else:
            if tiva == "S":
                doc.drawString(275, 170, '{}'.format(comprobante.iva27))
            else:
                doc.drawString(275, 170, "0")

        doc.drawString(500, 170, "{:.2f}".format(comprobante.total))
        doc.drawString(50, 200, "SUBTOTAL", 1)
        doc.drawString(275, 200, "IVA", 1)
        doc.drawString(500, 200, "TOTAL", 1)
        doc.drawString(50, 660, "Nombre: ", 1)
        doc.drawString(100, 660, '{}'.format(cliente.nombre))
        doc.drawString(45, 640, "Domicilio: ", 1)
        doc.drawString(100, 640, '{}'.format(cliente.domicilio))
        doc.drawString(75, 620, "IVA: ", 1)

        CAN = len(IVAS)
        x = 0
        while x < CAN:
            if IVAS[x][0] == cliente.tipoiva:
                doc.drawString(100, 620, '{}'.format(IVAS[x][1]))
                break
            x += 1

        doc.drawString(300, 620, "CUIT: ", 1)
        doc.drawString(335, 620, '{}'.format(cliente.cuit))
        doc.drawString(450, 100, "VTO: ", 1)
        doc.drawString(480, 100, '{}'.format(comprobante.fecha_vencimiento))
        doc.drawString(433, 120, "CAE Nº: ", 1)
        doc.drawString(480, 120, '{}'.format(comprobante.cae))
        doc.drawString(75, 550, "SON PESOS:")
        doc.drawString(75, 530, get_lett(comprobante.total))
        doc.drawString(75, 510, comprobante.concepto)
        alt = 510
        articulos = CuentasD.objects.filter(vtacod=comprobante.vtacod)
        for item in articulos:
            producto = item.articulo.artcod + " - "

            if item.precio is None:
                producto = producto + '{}'.format(item.articulo.precio)
            else:
                producto = producto + '{}'.format(item.precio)

            if item.articulo.moneda == 1:
                producto = producto + " pesos "
            else:
                if item.articulo.moneda == 2:
                    producto = producto + " dolares "
                else:
                    producto = producto + ""

            producto = producto + "(Con IVA del " + '{}'.format(item.articulo.iva) + "%)"
            alt -= 20
            doc.drawString(75, alt, producto)

        doc.setFontSize(9)
        doc.drawString(150, 25, "https://serviciosweb.afip.gob.ar/genericos/comprobantes/cae.aspx")
        doc.setFontSize(12)

        jsonqr = {
            "ver": 1,
            "fecha": '{}'.format(comprobante.fecha_emision),
            "cuit": 20124040311,
            "ptoVta": comprobante.sucursal,
            "tipoCmp": comprobante.tipocmp,
            "nroCmp": comprobante.numero,
            "importe": "{:.2f}".format(comprobante.total),
            "moneda": "PES",
            "ctz": 1,
            "tipoDocRec": 80,
            "nroDocRec": cliente.cuit,
            "tipoCodAut": "E",
            "codAut": comprobante.cae
        }

        nombrejson = carpeta_media + "jsonqr.json"
        jsonqra = json.dumps(jsonqr)
        jsonFile = open('{}'.format(nombrejson), "w")
        jsonFile.write(jsonqra)
        jsonFile.close()

        qr = carpeta_media + comprobante.comprobante + ".jpg"
        generar_qr(nombrejson, qr, "S", 5, 'https://www.afip.gob.ar/fe/qr/?p=')
        doc.drawImage(qr, 15, 23, width=120, height=120)

        logo_afip = carpeta_media + "Logo_afip.jpg"
        doc.drawImage('{}'.format(logo_afip), 150, 95)
        doc.drawString(150, 75, "Comprobante Autorizado", 1)

        doc.showPage()
        doc.save()
        return response


@login_required(login_url='ingresar')
def hacer_pedido(request, encriptado=None):
    contexto = articulos_filtrar(request)
    modo = request.GET.get('modo')
    contexto['modo'] = modo
    contexto['facturas_pendientes'] = True
    contexto['encriptado'] = encriptado

    if modo == 'm' or modo == 's':
        template_name = 'articulos_list_block.html'
    else:
        template_name = 'articulos_listar.html'

    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
def subir_pedido(request, encriptado=None):
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
@permission_required("expediente.expediente_vincular", None, raise_exception=True)
def grabar_cuentasd(request):
    print("grabar_cuentasd")
    if request.is_ajax and request.method == "GET":
        articulos_ids = request.GET.get('seleccion')
        articulos_ids = articulos_ids.split(';')
        items = 0
        print('aca')
        """Generar vtacod"""
        vtacod = 99999
        for articulo_id in articulos_ids:
            if int(articulo_id):
                """Alta de cuentasD"""
                cuentasd = CuentasD(vtacod=vtacod,
                                    articulo_id=articulo_id
                                    )
                cuentasd.save()
                items += 1
        mensaje = 'Se generaron {} items en detalle de pedido'.format(items)
        return JsonResponse({"mensaje": mensaje}, status=200)

    return JsonResponse({}, status=400)