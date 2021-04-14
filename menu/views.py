from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from perfiles.funcs import debe_cambiar_clave, get_preferencia
from django.contrib.auth.decorators import login_required, permission_required


def handler400(request, *args, **argv):
    response = render(request, '400.html')
    response.status_code = 400
    return response


def handler403(request, *args, **argv):
    mensaje = 'El usuario no tiene permiso para realizar esta tarea'
    messages.add_message(request, messages.ERROR, mensaje)
    try:
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return redirect('ingresar')


def handler404(request, *args, **argv):
    response = render(request, '404.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, '500.html')
    response.status_code = 500
    return response


@login_required(login_url='ingresar')
def menu(request):
    if debe_cambiar_clave(request.user.id):
        mensaje = 'Debe renovar su contraseña. '
        messages.add_message(request, messages.WARNING, mensaje)
        return redirect('cambiar_clave')
    else:
        vista = get_preferencia(request.user, 'menu', 'pantalla_inicial', 'C', 'insumidos_listar')
        try:
            return redirect(vista)
        except Exception as e:
            return render(request, 'vista_vacia.html')


def pagina_anterior(request):
    template_name = 'pagina_anterior.html'
    return render(request, template_name)
