from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, redirect
from articulos.filters import articulos_filtrar
from articulos.models import Articulo
from articulos.forms import ArticuloForm
from tabla.forms import ImportarCSVForm
from django.urls import reverse


# Create your views here.
@login_required(login_url='ingresar')
@permission_required('clientes.articulos_puede_listar', None, raise_exception=True)
def articulos_listar(request):
    contexto = articulos_filtrar(request)
    modo = request.GET.get('modo')
    contexto['modo'] = modo

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
        Articulo.save()
        return redirect('articulo_agregar')
    else:
        form =ArticuloForm()

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

    if request.method == 'POST':
       post= request.POST.copy()
       form = ArticuloForm(post, request.FILES, instance=articulo)
       if form.is_valid():
            form.save()
            return redirect('articulos_listar')
    else:
        form = ArticuloForm(instance=articulo)
        template_name = 'articulos_form.html'
        contexto = {'form': form, 'MODELO': articulo}
        return render(request, template_name, contexto)


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
                                artcod = values[1].strip()
                                if len(values) > 2:
                                    descripcion = values[2].replace("'", "").strip()
                                    if len(values) > 3:
                                        iva = values[3].strip()
                                        if len(values) > 4:
                                            precio = values[4].strip()
                                            if len(values) > 5:
                                                    moneda = values[5].strip()
                                                    if len(values) > 6:
                                                        departamento = values[6].strip()
                                                        if len(values) > 7:
                                                            artuniven = values[7].strip()
                                                            if len(values) > 8:
                                                                descextra = values[8].strip()
                                                                if len(values) > 9:
                                                                    ubicacion = values[9].strip()
                                                                    if len(values) > 10:
                                                                        artimg = values[10].strip
                            try:
                                articulo = articulo.objects.get(artcod=artcod)
                                if artcod:
                                    articulo = articulo.objects.get(artcod=artcod)
                                    articulo.articulo = articulo
                                if descripcion:
                                    articulo.descripcion = descripcion.upper()
                                if iva:
                                    articulo.iva = iva
                                if precio:
                                    articulo.precio = precio
                                if moneda:
                                    articulo.moneda = moneda
                                if departamento:
                                    articulo.departamento = departamento
                                if artuniven:
                                    articulo.artuniven = artuniven
                                if descextra:
                                    articulo.descextra = descextra
                                    print(cptedh)
                                if artimg:
                                    articulo.artimg = artimg
                                    print(cptedh)
                                if ubicacion:
                                    if ubicacion == 'S':
                                        ubicacion = True
                                    else:
                                        pendiente = False
                                    articulo.pendiente = pendiente
                                articulo.save()
                                actualizados += 1
                                exitos += 1
                            except articulo.DoesNotExist:
                                articulo = articulo.objects.get(artcod=artcod)
                                articulo = articulo(artcod=artcod,
                                                  descripcion=descripcion,
                                                  articulo=articulo,
                                                  iva=iva,
                                                  precio=precio,
                                                  moneda=moneda,
                                                  departamento=departamento,
                                                  artuniven=artuniven,
                                                  artimg=artimg,
                                                  ubicacion=ubicacion,
                                                  descextra =descextra)
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
        form = ImportarCSVForm(initial=initial)

    template_name = 'tabla/tabla_form.html'
    formato = 'ArtCod C(13) ; escripcion C(60); iva N(6); precio N(12); ' \
              'moneda N(2); departamento C(12); artuniven C(3); descextra C(255) ' \
              'ubicacion C(15); artimg C(250); ' \
              'Codificación UTF-8'
    titulo = 'Importar CSV'
    contexto = {'form': form, 'formato': formato, 'errores': errores_lista, 'titulo': titulo}
    return render(request, template_name, contexto)
