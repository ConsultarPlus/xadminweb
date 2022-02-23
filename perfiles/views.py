from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from urllib.parse import urlencode
from perfiles.funcs import actualizar_fecha_de_clave, set_preferencia, get_preferencia
from perfiles.forms import UsuarioForm
from perfiles.models import Perfil, Preferencia
from perfiles.filters import usuario_filtrar
from tabla.templatetags.custom_tags import traducir


@login_required(login_url='ingresar')
def cambiar_clave(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            if check_password(form.cleaned_data['new_password1'], request.user.password):
                messages.add_message(request, messages.ERROR, 'La nueva contraseña debe ser distinta a la actual')
            else:
                user = form.save()
                update_session_auth_hash(request, user)  # ¡Importante!
                f = actualizar_fecha_de_clave(request.user.id, None)
                messages.add_message(request, messages.SUCCESS, 'La clave fue actualizada')
                # logout(request) # Esto desloguea al usuario
                return redirect('menu')
        else:
            messages.add_message(request, messages.ERROR, 'Se debe revisar lo señalado abajo')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'cambiar_clave.html', {'form': form})


@login_required(login_url='ingresar')
def preferencia_grabar_asinc(request):
    if request.is_ajax and request.method == "GET":
        try:
            usuario_id = request.GET.get('usuario')
            usuario = User.objects.get(id=usuario_id)
            vista = request.GET.get('vista')
            opcion = request.GET.get('opcion')
        except Exception as e:
            return JsonResponse({"resultado": False}, status=200)

        try:
            fecha = request.GET.get('fecha')
        except Exception as e:
            fecha = None
        try:
            caracter = request.GET.get('caracter')
        except Exception as e:
            caracter = None
        try:
            numero = request.GET.get('numero')
        except Exception as e:
            numero = None
        try:
            if request.GET.get('logico') == 'true':
                logico = True
            else:
                logico = False
        except Exception as e:
            logico = None
        preferencia = {'usuario': usuario,
                       'vista': vista,
                       'opcion': opcion,
                       'fecha': fecha,
                       'caracter': caracter,
                       'numero': numero,
                       'logico': logico}
        resultado = set_preferencia(preferencia)

        return JsonResponse({"resultado": resultado}, status=200)

    return JsonResponse({}, status=400)


@login_required(login_url='ingresar')
def usuario_modificar(request):
    user = request.user.id
    usuario = User.objects.get(id=user)
    perfil, created = Perfil.objects.get_or_create(user_id=user)
    if request.method == 'POST':
        post = request.POST.copy()
        post['user'] = user
        form = UsuarioForm(post, request.FILES, instance=perfil)
        if form.is_valid():
            email = form['email'].value()
            usuario_con_mismo_mail = User.objects.filter(email=email).exclude(id=usuario.id)
            if usuario_con_mismo_mail.count() == 0:
                """Grabo datos de la tabla User"""
                usuario.first_name = form['nombre'].value()
                usuario.last_name = form['apellido'].value()
                usuario.email = email
                usuario.save()
                """Se graba la tabla Perfil"""
                form.save()
                return render(request, 'vista_vacia.html')
            else:
                messages.add_message(request, messages.ERROR, 'El correo indicado ya está usado')
    else:
        form = UsuarioForm(instance=perfil)

    template_name = 'usuario_form.html'
    contexto = {'form': form, 'usuario': usuario}
    return render(request, template_name, contexto)


def usuario_nombre(request):
    if request.is_ajax and request.method == "GET":
        usuarios_id = request.GET.get('id')
        usuarios_id = usuarios_id.split(';')

        nombres = {}
        for usuario_id in usuarios_id:
            try:
                usuario = User.objects.get(id=usuario_id)
                nombres.update({usuario_id: usuario.username})
            except Exception as e:
                pass
        if nombres:
            return JsonResponse(nombres, status=200)

    return JsonResponse({}, status=400)


@login_required(login_url='ingresar')
def usuarios_listar(request):
    contexto = usuario_filtrar(request)
    modo = request.GET.get('modo')
    contexto['modo'] = modo

    if modo == 'm' or modo == 's':
        template_name = 'usuarios_list_block.html'
    else:
        template_name = 'usuarios_listar.html'

    return render(request, template_name, contexto)


@login_required(login_url='ingresar')
def seleccionar_usuario(request):
    url = reverse('usuarios_listar')
    parametros = urlencode({'modo': 's'})
    url = '{}?{}'.format(url, parametros)
    return redirect(url)


@login_required(login_url='ingresar')
def seleccionar_usuarios(request):
    url = reverse('usuarios_listar')
    parametros = urlencode({'modo': 'm'})
    url = '{}?{}'.format(url, parametros)
    return redirect(url)

