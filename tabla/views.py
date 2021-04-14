from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.http import JsonResponse
from urllib.parse import urlencode
from .listas import (ENTIDADES,
                     etiquetas_expedientes,
                     etiquetas_cptes,
                     etiquetas_turno,
                     etiquetas_insumidos,
                     etiquetas_instituciones,
                     etiquetas_personas,
                     etiquetas_otros)
from .models import Tabla, Variable, Plantilla
from .forms import TablaForm, VariableForm, PlantillaForm, ImportarCSVForm
from .filters import tabla_filtrar, variable_filtrar, plantilla_filtrar
from .funcs import custom_redirect


@login_required(login_url='ingresar')
@permission_required("tabla.tabla_puede_listar", None, raise_exception=True)
def tablas_cargar_csv(request):
    initial = {'entidades': ENTIDADES}
    errores_lista = []
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
                            codigo = values[0].replace("'", "")
                            codigo = codigo.replace('"', '')
                            if len(codigo) > 10:
                                codigo = codigo[0:10]
                            codigo = codigo.upper()
                            if cnt == 0:
                                print('*values: ', values)
                                print('*codigo: ', codigo)
                            descripcion = ''
                            superior_entidad = ''
                            superior_codigo = ''
                            if len(values) > 1:
                                descripcion = values[1].replace("'", "").strip()
                                if len(descripcion) > 100:
                                    descripcion = descripcion[0:97] + '...'
                                if len(values) > 2:
                                    superior_entidad = values[2].strip()
                                    if len(values) > 3:
                                        superior_codigo = values[3].strip()
                            activo = 'S'
                            valor_preferencial = 'N'
                            try:
                                tabla = Tabla.objects.get(entidad=entidad, codigo=codigo)
                                tabla.entidad = entidad
                                tabla.codigo = codigo
                                if descripcion:
                                    tabla.descripcion = descripcion.upper()
                                if superior_entidad:
                                    tabla.superior_entidad = superior_entidad.upper()
                                if superior_codigo:
                                    tabla.superior_codigo = superior_codigo
                                tabla.valor_preferencial = valor_preferencial
                                tabla.activo = activo
                                tabla.save()
                                actualizados += 1
                                exitos += 1
                            except Tabla.DoesNotExist:
                                tabla = Tabla(entidad=entidad,
                                              codigo=codigo,
                                              descripcion=descripcion.upper(),
                                              superior_entidad=superior_entidad,
                                              superior_codigo=superior_codigo.upper(),
                                              valor_preferencial=valor_preferencial,
                                              activo=activo)
                                tabla.save()
                                nuevos += 1
                                exitos += 1
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
    formato = 'Código C(10) ; Descripción C(100); Entidad superior C(20); Código de entidad superior C(10). ' \
              'Codificación UTF-8'
    titulo = 'Importar CSV'
    contexto = {'form': form, 'formato': formato, 'errores': errores_lista, 'titulo': titulo}
    return render(request, template_name, contexto)


def cargar_localidades(request):
    return cargar_subordinados(request)


def cargar_subordinados(request):
    superior_id = request.GET.get('id')
    if superior_id != '' and superior_id is not None:
        superior = Tabla.objects.filter(id=superior_id).values('codigo', 'entidad')
        codigo = superior[0]['codigo']
        entidad = superior[0]['entidad']
        subordinados = Tabla.objects.filter(superior_codigo=codigo,
                                            superior_entidad=entidad).order_by('-valor_preferencial', 'descripcion')
    else:
        subordinados = Tabla.objects.none()

    return render(request, 'dropdowns/subordinados_dropdown.html', {'subordinados': subordinados})


def cargar_registros_de_entidad(request):
    entidad = request.GET.get('entidad')
    if entidad != '' and entidad is not None:
        registros = Tabla.objects.filter(entidad=entidad).order_by('-valor_preferencial', 'descripcion')
    else:
        registros = Tabla.objects.none()

    return render(request, 'dropdowns/registros_de_entidad_dropdown.html', {'registros': registros})


@login_required(login_url='ingresar')
@permission_required("tabla.tabla_puede_listar", None, raise_exception=True)
def tablas_listar(request):
    contexto = tabla_filtrar(request)
    modo = request.GET.get('modo')
    entidad = request.GET.get('entidad')
    contexto['modo'] = modo
    contexto['entidad'] = entidad
    contexto['url_filtros'] = request.GET.urlencode()
    if modo == 'm' or modo == 's':
        template_name = 'tabla/tablas_list_block.html'
    else:
        template_name = 'tabla/tablas_listar.html'

    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
@permission_required("tabla.tabla_puede_editar", None, raise_exception=True)
def tabla_editar(request, id):
    try:
        tabla = Tabla.objects.get(id=id)
    except Exception as mensaje:
        messages.add_message(request, messages.ERROR, mensaje)
        return redirect('tablas_listar')

    if request.method == 'POST':
        # para poder editar el request hay que copiarlo porque está como sólo lectura
        post = request.POST.copy()
        # En modificación está inhabilitado el codigo y para que al grabar supere
        # las validaciones hay que asignar el valor original de los campos inhabilitados
        # al diccionario del Request
        post['entidad'] = tabla.entidad
        post['codigo'] = tabla.codigo
        form = TablaForm(post, instance=tabla)
        if form.is_valid():
            data = form.cleaned_data
            codigo = data['codigo']
            entidad = data['entidad']
            descripcion = data['descripcion']
            tablas_list = Tabla.objects.filter(Q(entidad=entidad),
                                               Q(codigo=codigo.upper()) |
                                               Q(descripcion=descripcion.upper())) \
                                       .exclude(id=id)
            if len(tablas_list) > 0:
                mensaje = 'Ya existe un registro igual para la entidad {} '.format(entidad)
                messages.add_message(request, messages.WARNING, mensaje)
            else:
                tabla = form.save()
                valor_preferencial = tabla.valor_preferencial
                entidad = tabla.entidad
                url = request.GET.get("next")
                if valor_preferencial == 'S':
                    tabla_id = tabla.id
                    n = set_valor_preferencial(tabla_id, entidad)
                return redirect(url)
    else:
        form = TablaForm(instance=tabla)

    template_name = 'tabla/tabla_form.html'
    return render(request, template_name, {'form': form,
                                           'tabla': tabla})


@login_required(login_url='ingresar')
@permission_required("tabla.tabla_puede_agregar", None, raise_exception=True)
def tabla_agregar(request, entidad=None):
    template_name = 'tabla/tabla_form.html'
    initial = {'entidad': entidad}
    if request.method == 'POST':
        form = TablaForm(request.POST, initial=initial)
        if form.is_valid():
            data = form.cleaned_data
            codigo = data['codigo']
            entidad = data['entidad']
            descripcion = data['descripcion']
            superior_entidad = data['superior_entidad']
            superior_codigo = data['superior_codigo']

            if superior_entidad == '' or superior_entidad is None:
                tablas_list = Tabla.objects.filter(Q(entidad=entidad),
                                                   Q(codigo=codigo.upper())
                                                   )
                if len(tablas_list) > 0:
                    mensaje = 'Ya existe un registro con el mismo código para la entidad {} '.format(entidad)
                    messages.add_message(request, messages.WARNING, mensaje)

            tabla = form.save()
            valor_preferencial = data['valor_preferencial']
            url = request.GET.get("next")
            if url is None:
                url = 'tablas_listar'
            if valor_preferencial == 'S':
                tabla_id = tabla.id
                n = set_valor_preferencial(tabla_id, entidad)
            mensaje = 'Se ha grabado con éxito'
            messages.add_message(request, messages.SUCCESS, mensaje)

            return redirect(url)

    else:
        form = TablaForm(initial=initial)

    return render(request, template_name, {'form': form})


def set_valor_preferencial(tabla_id, entidad):
    with connection.cursor() as cursor:
        sql = 'update tabla_tabla ' \
              "set valor_preferencial='N' " \
              "where entidad='{}' " \
              "and id<>{} ".format(entidad, tabla_id)
        cursor.execute(sql)
    return 1


@login_required(login_url='ingresar')
@permission_required("tabla.tabla_puede_eliminar", None, raise_exception=True)
def tabla_eliminar(request, id):
    tabla = Tabla.objects.get(id=id)
    url = request.GET.get("next")

    try:
        tabla.delete()
    except Exception as e:
        mensaje = 'No se puede eliminar porque el ítem está referenciado en ' \
                  'otros registros. Otra opción es desactivarlo'
        messages.add_message(request, messages.ERROR, mensaje)

    return redirect(url)


@login_required(login_url='ingresar')
@permission_required("tabla.variable_puede_listar", None, raise_exception=True)
def variables_listar(request):
    contexto = variable_filtrar(request)
    return render(request, 'variable/variables_listar.html', contexto)


@login_required(login_url='ingresar')
@permission_required("tabla.variable_puede_agregar", None, raise_exception=True)
def variable_agregar(request):
    if request.POST:
        form = VariableForm(request.POST)
        if form.is_valid():
            form.save()
            return custom_redirect('variables_listar', {'buscar': form.cleaned_data['variable']})
    else:
        form = VariableForm()
        template_name = 'variable/variable_form.html'
        return render(request, template_name, {'form': form})


@login_required(login_url='ingresar')
@permission_required("tabla.variable_puede_editar", None, raise_exception=True)
def variable_editar(request, variable_id):
    try:
        variable = Variable.objects.get(variable=variable_id)
    except Exception as mensaje:
        messages.add_message(request, messages.ERROR, mensaje)
        return redirect('variables_listar')

    if request.method == 'POST':
        post = request.POST.copy()
        form = VariableForm(post, instance=variable)
        if form.is_valid():
            form.save()
            return redirect('variables_listar')
    else:
        template_name = 'variable/variable_form.html'
        form = VariableForm(instance=variable)
        return render(request, template_name, {'form': form, 'variable': variable})


# @login_required(login_url='ingresar')
# def variable_eliminar(request, variable_id):
#     variable = Variable.objects.get(variable=variable_id)
#     url = 'variables_listar'
#     try:
#         variable.delete()
#     except Exception as e:
#         mensaje = 'No se puede eliminar porque el ítem está referenciado en ' \
#                   'otros registros. Otra opción es desactivarlo'
#         messages.add_message(request, messages.ERROR, mensaje)
#
#     return redirect(url)

@login_required(login_url='ingresar')
@permission_required("tabla.variable_puede_eliminar", None, raise_exception=True)
def variable_eliminar(request, variable_id):
    url = 'variables_listar'
    try:
        variable = Variable.objects.get(variable=variable_id)
        variable.delete()
    except Exception as e:
        mensaje = 'No se puede eliminar porque el ítem está referenciado en ' \
                  'otros registros. Otra opción es desactivarlo'
        messages.add_message(request, messages.ERROR, mensaje)

    return redirect(url)


@login_required(login_url='ingresar')
@permission_required("tabla.plantilla_puede_listar", None, raise_exception=True)
def plantillas_listar(request):
    contexto = plantilla_filtrar(request)
    modo = request.GET.get('modo')
    contexto['modo'] = modo

    if modo == 'm' or modo == 's':
        template_name = 'plantilla/plantillas_list_block.html'
    else:
        template_name = 'plantilla/plantillas_listar.html'

    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
@permission_required("tabla.plantilla_puede_agregar", None, raise_exception=True)
def plantilla_agregar(request):
    if request.POST:
        form = PlantillaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plantillas_listar')
    else:
        form = PlantillaForm()

    template_name = 'plantilla/plantilla_form.html'
    return render(request, template_name, {'form': form})


@login_required(login_url='ingresar')
@permission_required("tabla.plantilla_puede_editar", None, raise_exception=True)
def plantilla_editar(request, id):
    try:
        plantilla = Plantilla.objects.get(id=id)
    except Exception as mensaje:
        messages.add_message(request, messages.ERROR, mensaje)
        return redirect('plantillas_listar')

    if request.method == 'POST':
        post = request.POST.copy()
        form = PlantillaForm(post, instance=plantilla)
        if form.is_valid():
            form.save()
            return redirect('plantillas_listar')
    else:
        form = PlantillaForm(instance=plantilla)

    template_name = 'plantilla/plantilla_form.html'
    return render(request, template_name, {'form': form, 'plantilla': plantilla})


@login_required(login_url='ingresar')
@permission_required("tabla.plantilla_puede_eliminar", None, raise_exception=True)
def plantilla_eliminar(request, id):
    plantilla = Plantilla.objects.get(id=id)
    url = 'plantillas_listar'
    try:
        plantilla.delete()
    except Exception as e:
        mensaje = 'No se puede eliminar porque el ítem está referenciado en ' \
                  'otros registros. Otra opción es desactivarlo'
        messages.add_message(request, messages.ERROR, mensaje)

    return redirect(url)


@login_required(login_url='ingresar')
def plantilla_contenido(request):
    if request.is_ajax and request.method == "GET":
        plantilla_id = request.GET.get('id')
        plantilla = Plantilla.objects.get(id=plantilla_id)
        if not plantilla:
            return JsonResponse('{"contenido": ""', status=200)
        else:
            contenido = plantilla.plantilla
            return JsonResponse({"contenido": contenido}, status=200)

    return JsonResponse({}, status=400)


@login_required(login_url='ingresar')
def seleccionar_plantilla(request):
    url = reverse('plantillas_listar')
    parametros = urlencode({'modo': 's'})
    url = '{}?{}'.format(url, parametros)
    return redirect(url)


@login_required(login_url='ingresar')
def seleccionar_tabla(request):
    entidad = request.GET.get('entidad')
    entidad_off = request.GET.get('entidad_off')
    url = reverse('tablas_listar')
    parametros = urlencode({'modo': 's', 'entidad': entidad, 'entidad_off': entidad_off})
    url = '{}?{}'.format(url, parametros)
    return redirect(url)


def tabla_descripcion(request):
    if request.is_ajax and request.method == "GET":
        tabla_id = request.GET.get('id')
        tabla = Tabla.objects.get(id=tabla_id)
        if not tabla:
            return JsonResponse('{"descripcion": "No existe"', status=200)
        else:
            descripcion = tabla.descripcion
            return JsonResponse({"descripcion": descripcion}, status=200)

    return JsonResponse({}, status=400)


def probar_algo(request):
    import django.apps
    modelos = 'General,'
    for model in django.apps.apps.get_models('expediente'):
        modelos += model._meta.model_name + ','
    print('***modelos: ', modelos)
    return redirect('menu')


@login_required(login_url='ingresar')
def etiquetas_de_grupo(request):
    etiquetas = (('', 'Seleccionar etiqueta'),)
    if request.is_ajax and request.method == "GET":
        grupo = request.GET.get('grupo')
        if grupo == 'EXPEDIENTES':
            etiquetas = etiquetas_expedientes
        elif grupo == 'COMPROBANTES':
            etiquetas = etiquetas_cptes
        elif grupo == 'INSUMIDOS':
            etiquetas = etiquetas_insumidos
        elif grupo == 'TURNOS':
            etiquetas = etiquetas_turno
        elif grupo == 'PERSONAS':
            etiquetas = etiquetas_personas
        elif grupo == 'INSTITUCIONES':
            etiquetas = etiquetas_instituciones
        elif grupo == 'OTROS':
            etiquetas = etiquetas_otros

    return render(request, 'dropdowns/items_de_lista.html', {'lista': list(etiquetas)})
