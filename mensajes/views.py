from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from urllib.parse import urlencode
from tabla.funcs import procesar_hora
from .forms import MensajeForm
from .filters import mensaje_filtrar
from .models import Mensaje, Destinatario
import datetime


@login_required(login_url='ingresar')
@permission_required("mensajes.mensaje_puede_listar", None, raise_exception=True)
def mensajes_listar(request):
    contexto = mensaje_filtrar(request)
    modo = request.GET.get('modo')
    contexto['modo'] = modo

    if modo == 'm' or modo == 's':
        template_name = 'mensajes_list_block.html'
    else:
        template_name = 'mensajes_listar.html'

    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
@permission_required("mensajes.mensaje_puede_agregar", None, raise_exception=True)
def mensaje_agregar(request):
    initial = {'fecha': datetime.date.today(),
               'destinatarios': request.GET.get('destinatarios')}
    if request.POST:
        post = request.POST.copy()
        post['remitente'] = request.user.id
        post['hora'] = procesar_hora(post)
        form = MensajeForm(post)
        if form.is_valid():
            mensaje = form.save()
            ok = enviar_mensaje_interno(mensaje)
            return redirect('mensajes_listar')
    else:
        form = MensajeForm(initial=initial)

    template_name = 'mensaje_form.html'
    contexto = {'form': form}
    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
@permission_required("mensajes.mensaje_puede_editar", None, raise_exception=True)
def mensaje_editar(request, id):
    try:
        mensaje = Mensaje.objects.get(id=id)
        hr = mensaje.hora.strftime("%H")
        mins = mensaje.hora.strftime("%M")
        if mensaje.remitente != request.user:
            messages.add_message(request, messages.ERROR, 'El mensaje fue creado por otro usuario')
            return redirect('mensajes_listar')
    except Exception as mensaje:
        messages.add_message(request, messages.ERROR, mensaje)
        return redirect('mensajes_listar')

    if request.method == 'POST':
        post = request.POST.copy()
        post['hora'] = procesar_hora(post)
        form = MensajeForm(post, instance=mensaje)
        if form.is_valid():
            mensaje = form.save()
            ok = enviar_mensaje_interno(mensaje)
            return redirect('mensajes_listar')
    else:
        initial = {'hr': hr, 'min': mins}
        form = MensajeForm(instance=mensaje, initial=initial)

    template_name = 'mensaje_form.html'
    contexto = {'form': form, 'mensaje_interno': Mensaje}
    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
@permission_required("mensajes.view_mensaje", None, raise_exception=True)
def mensaje_ver(request, id):
    try:
        mensaje = Mensaje.objects.get(id=id)
        hr = mensaje.hora.strftime("%H")
        mins = mensaje.hora.strftime("%M")
    except Exception as mensaje:
        messages.add_message(request, messages.ERROR, mensaje)
        return redirect('mensajes_listar')

    ok = marcar_mensaje_como_leido(id, request.user.id)

    initial = {'hr': hr, 'min': mins, 'visualizar': True}
    form = MensajeForm(instance=mensaje, initial=initial)
    template_name = 'mensaje_form.html'
    contexto = {'form': form, 'mensaje_interno': mensaje}
    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
@permission_required("expediente.mensaje_puede_eliminar", None, raise_exception=True)
def mensaje_eliminar(request, id):
    url = 'mensajes_listar'
    try:
        mensaje = Mensaje.objects.get(id=id)
        if mensaje.remitente != request.user:
            messages.add_message(request, messages.ERROR, 'El mensaje fue creado por otro usuario')
            return redirect('mensajes_listar')
        else:
            mensaje.delete()
            try:
                pendientes = Destinatario.objects.get(mensaje_id=id)
                pendientes.delete()
            except Exception as e:
                pass
    except Exception as e:
        msj = 'No se puede eliminar porque el ítem está referenciado en ' \
              'otros registros. Otra opción es desactivarlo'
        messages.add_message(request, messages.ERROR, msj)

    return redirect(url)


@login_required(login_url='ingresar')
def mensaje_responder(request, id):
    try:
        a_todos = request.GET.get('a_todos')
        mensaje = Mensaje.objects.get(id=id)
        destinatarios = str(mensaje.remitente.id)
        if a_todos == 'S':
            otros = mensaje.destinatarios.all()
            for otro in otros:
                destinatarios += ',' + str(otro.id)
        url = reverse('mensaje_agregar')
        parametros = urlencode({'destinatarios': destinatarios})
        url = '{}?{}'.format(url, parametros)
    except Exception as e:
        url = 'mensajes_listar'
        messages.add_message(request, messages.ERROR, e)

    return redirect(url)


def contar_mensajes_pendientes(request):
    if request.is_ajax and request.method == "GET":
        usuario = request.user.id
        pendientes = Destinatario.objects.filter(usuario=usuario, fecha_visto=None).values('mensaje_id')
        if not pendientes:
            return JsonResponse({"pendientes": 0}, status=200)
        else:
            mensajes = Mensaje.objects.filter(Q(id__in=pendientes),
                                              Q(hora__lte=datetime.datetime.now().time()) |
                                              Q(fecha__lt=datetime.datetime.now())
                                              )
            return JsonResponse({"pendientes": mensajes.count()}, status=200)
    return JsonResponse({"pendientes": 0}, status=400)


# def procesar_hora(post):
#     hr = post['hr']
#     mins = post['min']
#     if hr == '' or hr is None:
#         hr = datetime.datetime.now().strftime("%H")
#     if mins == '' or mins is None:
#         mins = datetime.datetime.now().strftime("%M")
#     hr = int(hr)
#     mins = int(mins)
#     hora = datetime.time(hr, mins, 0)  # datetime.time()
#     return hora


def enviar_mensaje_interno(mensaje):
    Destinatario.objects.filter(mensaje=mensaje).delete()
    destinatarios = mensaje.destinatarios.all()
    for usuario in destinatarios:
        destinatario = Destinatario.objects.create(mensaje=mensaje,
                                                   usuario=usuario)
    return True


def marcar_mensaje_como_leido(mensaje_id, usuario_id):
    try:
        pendiente = Destinatario.objects.get(mensaje_id=mensaje_id, usuario_id=usuario_id)
        pendiente.fecha_visto = datetime.datetime.now()

        hr = datetime.datetime.now().strftime("%H")
        mins = datetime.datetime.now().strftime("%M")
        hr = int(hr)
        mins = int(mins)
        hora = datetime.time(hr, mins, 0)

        pendiente.hora_visto = hora
        pendiente.save()
        exito = True
    except Exception as e:
        exito = False

    return exito
