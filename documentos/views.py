from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from urllib.parse import urlencode
from .forms import DocumentoForm
from .filters import documento_filtrar
from .models import Documento
# from expediente.views.insumido_views import insumido_automatico


@login_required(login_url='ingresar')
@permission_required("documento.puede_listar", None, raise_exception=True)
def documentos_listar(request):
    contexto = documento_filtrar(request)
    template_name = 'documentos_listar.html'
    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
@permission_required("documento.puede_agregar", None, raise_exception=True)
def documento_agregar(request):
    url = reverse('documento_agregar')
    form = DocumentoForm(request.POST or None, request.FILES or None, initial={'redirect': url})
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # url = form.cleaned_data['redirect_url']
            # entidad = form.cleaned_data['entidad']
            # if entidad == 'EXPEDIENTE':
            #     entidad_id = form.cleaned_data['entidad_id']
            #     observacion = 'Archivo adjuntado {}'.format(form.cleaned_data['archivo'])
            #     datos_de_insumido = {'usuario': request.user,
            #                          'observacion': observacion,
            #                          'automatico': True}
            #     insumido_id = insumido_automatico(entidad_id, datos_de_insumido)
            # if len(url) == 0:
            url = reverse('documentos_listar')
            return redirect(url)
        else:
            print(form.errors)

    template_name = 'documento_form.html'
    return render(request, template_name, {'form': form})


@login_required(login_url='ingresar')
@permission_required("documento.puede_agregar", None, raise_exception=True)
def documento_agregar_y_volver(request):
    url = reverse('documento_agregar')
    parametros = urlencode({'volver': True})
    url = '{}?{}'.format(url, parametros)
    return redirect(url)


@login_required(login_url='ingresar')
@permission_required("documento.puede_eliminar", None, raise_exception=True)
def documento_eliminar(request, id):
    try:
        documento = Documento.objects.get(id=id)
        entidad = documento.entidad
        entidad_id = documento.entidad_id
        archivo = documento.archivo
        url = request.META.get('HTTP_REFERER')
        documento.delete()
        exito = 'S'
    except Exception as e:
        exito = 'N'
        mensaje = e
        messages.add_message(request, messages.ERROR, mensaje)

    # if entidad == 'EXPEDIENTE' and exito == 'S':
    #     if respuesta:
    #         respuesta.respuesta = ''
    #         respuesta.save()
        # try:
        #     observacion = 'Archivo eliminado {}'.format(archivo)
        #     datos_de_insumido = {'usuario': request.user,
        #                          'observacion': observacion,
        #                          'automatico': True}
        #     insumido_id = insumido_automatico(entidad_id, datos_de_insumido)
        # except Exception as e:
        #     pass

    return redirect(url)


@login_required(login_url='ingresar')
@permission_required("documento.puede_editar", None, raise_exception=True)
def documento_editar(request, id):
    url = reverse('pagina_anterior')
    try:
        documento = Documento.objects.get(id=id)
        respuesta = documento.respuesta
    except Exception as mensaje:
        messages.add_message(request, messages.ERROR, mensaje)
        return redirect(url)

    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            form.save()
            entidad = form.cleaned_data['entidad']
            # if entidad == 'EXPEDIENTE':
            #     if respuesta:
            #         respuesta.respuesta = form.cleaned_data['archivo']
            #         respuesta.save()

                # entidad_id = form.cleaned_data['entidad_id']
                # observacion = 'Archivo modificado {}'.format(form.cleaned_data['archivo'])
                # datos_de_insumido = {'usuario': request.user,
                #                      'observacion': observacion,
                #                      'automatico': True}
                # insumido_id = insumido_automatico(entidad_id, datos_de_insumido)
            return redirect(url)
    else:
        form = DocumentoForm(instance=documento)

    template_name = 'documento_form.html'
    return render(request, template_name, {'form': form, 'documento': documento})
