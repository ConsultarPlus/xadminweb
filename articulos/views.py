from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, redirect
from articulos.filters import articulos_filtrar
from articulos.models import Articulo
from articulos.forms import ArticuloForm
from tabla.forms import ImportarCSVForm
from tabla.models import Tabla
from django.urls import reverse


# Create your views here.
@login_required(login_url='ingresar')
@permission_required('clientes.articulos_puede_listar', None, raise_exception=True)
def articulos_listar(request):
    contexto = articulos_filtrar(request)
    modo = request.GET.get('modo')
    contexto['modo'] = modo
    contexto['subir_cuentas'] = True
    if modo == 'm' or modo == 's':
        template_name = 'articulos_list_block.html'
    else:
        template_name = 'articulos_listar.html'

    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
@permission_required("clientes.articulo_agregar", None, raise_exception=True)
def articulo_agregar(request):
    url = reverse('articulo_agregar')
    if request.POST:
        form = ArticuloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articulos_listar')
    else:
        form = ArticuloForm()

    template_name = "articulos_form.html"

    return render(request, template_name, {'form': form})


@login_required(login_url='ingresar')
@permission_required("articulo_editar", None, raise_exception=True)
def articulo_editar(request, id):
    try:
        articulo = Articulo.objects.get(id=id)
    except Exception as mensaje:
        messages.add_message(request, messages.ERROR, mensaje)
        return redirect('articulos_listar')

    template_name = 'articulos_form.html'

    if request.method == 'POST':
       post= request.POST.copy()
       form = ArticuloForm(post, request.FILES, instance=articulo)
       contexto = {'form': form, 'MODELO': articulo}
       if form.is_valid():
            form.save()
            return redirect('articulos_listar')
    else:
        departamento = Tabla.objects.get(id=articulo.departamento.id)
        rubro = Tabla.objects.get(codigo=departamento.superior_codigo, entidad=departamento.superior_entidad)
        seccion = Tabla.objects.get(codigo=rubro.superior_codigo, entidad=rubro.superior_entidad)
        initial = {'rubro': rubro.descripcion, 'seccion':seccion.descripcion}
        form = ArticuloForm(instance=articulo, initial=initial)
        contexto = {'form': form, 'articulo': articulo}

    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
@permission_required("articulos.articulo_eliminar", None, raise_exception=True)
def articulo_eliminar(request, id):
    url = 'articulos_listar'
    try:
        articulo = Articulo.objects.get(id=id)
        articulo.delete()
    except Exception as e:
        mensaje = 'No se puede eliminar porque el ítem está referenciado en ' \
                  'otros registros. Otra opción es desactivarlo'
        messages.add_message(request, messages.ERROR, mensaje)

    return redirect(url)


@login_required(login_url='ingresar')
@permission_required("articulos.articulos_importar", None, raise_exception=True)
def articulos_importar(request):
    errores_lista = []
    initial = {'entidades': (('Articulo', 'Articulo'),),
               'entidad': 'Articulo'}
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
                            artcod = values[0].replace("'", "")
                            artcod = artcod.replace('"', '')
                            descripcion = ''
                            iva = 0
                            precio = 0
                            moneda = 0
                            departamento = ''
                            artuniven = ''
                            descextra = ''
                            ubicacion = ''
                            artimg = ''

                            if len(values) > 1:
                                descripcion = values[1].replace("'", "").strip()
                                if len(values) > 2:
                                    aux = values[2].replace("'", "")
                                    aux = values[2].replace(",", ".")
                                    iva = int(float(aux.strip()))
                                    if len(values) > 3:
                                        aux = values[3].replace("'", "")
                                        aux = values[3].replace(",", ".")
                                        precio = float(aux.strip())
                                        if len(values) > 4:
                                                aux = values[4].replace("'", "")
                                                aux = values[4].replace(",", ".")
                                                moneda = int(float(aux.strip()))
                                                if len(values) > 5:
                                                    departamento = values[5].replace("'", "").strip()
                                                    if len(values) > 6:
                                                        artuniven = values[6].replace("'", "").strip()
                                                        if len(values) > 7:
                                                            descextra = values[7].replace("'", "").strip()
                                                            if len(values) > 8:
                                                                ubicacion = values[8].replace("'", "").strip()
                                                                if len(values) > 9:
                                                                    artimg = values[9].replace("'", "").strip()
                            try:
                                articulo = Articulo.objects.get(artcod=artcod)
                                if descripcion:
                                    articulo.descripcion = descripcion.upper()
                                if iva:
                                    articulo.iva = iva
                                if precio:
                                    articulo.precio = precio
                                if moneda:
                                    articulo.moneda = moneda
                                if departamento:
                                    try:
                                        depto = Tabla.objects.get(codigo=departamento, entidad='DEPARTAMENTO')
                                    except Tabla.DoesNotExist:
                                        depto = Tabla(entidad='DEPARTAMENTO',
                                                      codigo=departamento,
                                                      descripcion=departamento)
                                        depto.save()
                                    articulo.departamento = depto
                                if artuniven:
                                    articulo.artuniven = artuniven
                                if descextra:
                                    articulo.descextra = descextra
                                if artimg:
                                    articulo.artimg = artimg
                                if ubicacion:
                                    articulo.ubicacion = ubicacion
                                articulo.save()
                                actualizados += 1
                                exitos += 1
                            except Articulo.DoesNotExist:
                                try:
                                    depto = Tabla.objects.get(codigo=departamento, entidad='DEPARTAMENTO')
                                except Tabla.DoesNotExist:
                                    depto = Tabla(entidad='DEPARTAMENTO',
                                                  codigo=departamento,
                                                  descripcion=departamento)
                                    depto.save()
                                articulo = Articulo(artcod=artcod,
                                                    descripcion=descripcion,
                                                    iva=iva,
                                                    precio=precio,
                                                    moneda=moneda,
                                                    departamento=depto,
                                                    artuniven=artuniven,
                                                    artimg=artimg,
                                                    ubicacion=ubicacion,
                                                    descextra=descextra)
                                articulo.save()
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
                    return redirect('articulo_listar')
        else:
            messages.add_message(request, messages.ERROR, 'error')
    else:
        form = ImportarCSVForm(initial=initial)

    template_name = 'tabla/tabla_form.html'
    formato = 'ArtCod C(13) ; Descripcion C(60); iva N(6); Precio N(12); ' \
              'moneda N(2); departamento C(12); artuniven C(3); descextra C(255) ' \
              'ubicación C(15); artimg C(250); ' \
              'Codificación UTF-8'
    titulo = 'Importar CSV'
    contexto = {'form': form, 'formato': formato, 'errores': errores_lista, 'titulo': titulo}
    return render(request, template_name, contexto)


def cargar_rubro(request):
    departamento_id = request.GET.get('id_depto')
    departamento = Tabla.objects.get(id=departamento_id)
    rubro = Tabla.objects.get(codigo=departamento.superior_codigo, entidad=departamento.superior_entidad)
    return render(request,  'dropdowns/rubros_dropdown.html', {'rubro': rubro})


def cargar_seccion(request):
    departamento_id = request.GET.get('id_depto')
    departamento = Tabla.objects.get(id=departamento_id)
    rubro = Tabla.objects.get(codigo=departamento.superior_codigo, entidad=departamento.superior_entidad)
    seccion = Tabla.objects.get(codigo=rubro.superior_codigo, entidad=rubro.superior_entidad)
    return render(request,  'dropdowns/seccion_dropdown.html', {'seccion': seccion})

