import datetime
from django.core.mail import send_mail
from django.contrib import admin
from django import forms
from django.urls import path
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from simple_history.admin import SimpleHistoryAdmin
from tabla.models import Tabla
from tabla.forms import ImportarCSVForm
from tabla.funcs import es_valido, email_valido
from xadmin import settings
from .models import Perfil, Preferencia
from .forms import CopiarPermisosGrupoForm, CopiarPreferenciasForm


class PerfilAdminForm(forms.ModelForm):
    # En este form se pueden hacer las validaciones de perfil
    pass


class PerfilAdmin(admin.StackedInline):
    form = PerfilAdminForm
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Niveles, foto, fecha de clave, e-mail de recuperación'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "nivel":
            kwargs["queryset"] = Tabla.objects.filter(entidad='NIVEL')
        return super().formfield_for_manytomany(db_field, request, **kwargs)


class UserAdminForm(forms.ModelForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        message = self.cleaned_data['email']
        if email != '' and email is not None:
            otros = User.objects.filter(email=email).exclude(username=username)
            if otros.exists():
                raise ValidationError("El e-mail ya fue usado en otro usuario")
        return message


# Definir un nuevo UserAdmin
class UserAdmin(BaseUserAdmin):
    form = UserAdminForm
    inlines = (PerfilAdmin,)
    change_list_template = "change_list.html"
    actions = ['resetear_clave_y_enviar_mail']

    def grupo(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)

    grupo.short_description = 'Grupos'

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'grupo')

    def resetear_clave_y_enviar_mail(self, request, usuarios):
        # template = Template('aviso_de_reseteo.html')
        template = 'aviso_de_reseteo.html'
        ano = datetime.datetime.today().year
        password = 'Defen_' + str(ano)
        sitio = request.build_absolute_uri('/ingresar/')
        enviados = 0
        errores = 0
        errores_lista = []
        for usuario in usuarios:
            if email_valido(usuario.email):
                perfil = Perfil.objects.get(user=usuario)
                perfil.fecha_clave = None
                perfil.save()
                usuario.set_password(password)
                usuario.save()
                destinatario = [usuario.email]
                contexto = {'por_admin': True,
                            'usuario': usuario.username,
                            'clave': password,
                            'sitio': sitio}
                try:
                    mensaje = render_to_string(template, contexto)
                    exito = send_mail(subject='Defensoria del Pueblo: Nuevas credenciales de acceso',
                                      message='',
                                      from_email=settings.EMAIL_HOST_USER,
                                      recipient_list=destinatario,
                                      html_message=mensaje,
                                      fail_silently=False,)
                except Exception as msj:
                    errores += 1
                    errores_lista.append('Usuario {}, e-mail "{}": {}'.format(usuario.username, usuario.email, msj))

                if exito:
                    enviados += 1
                else:
                    errores += 1
                    errores_lista.append('Usuario {}, e-mail "{}"'.format(usuario.username, usuario.email))
            else:
                errores += 1
                errores_lista.append('Usuario {}, e-mail "{}"'.format(usuario.username, usuario.email))

        tipo = messages.INFO
        if enviados == 0:
            msj = 'No se envió ningún mensaje'
            tipo = messages.WARNING
        elif enviados == 1:
            msj = 'Se envió 1 mensaje'
        else:
            msj = 'Se enviaron {} mensajes'.format(enviados)
        messages.add_message(request, tipo, msj)
        if errores > 0:
            template_name = 'lista_de_errores.html'
            return render(request, template_name, {'enviados': enviados,
                                                   'errores': errores_lista,
                                                   })

    resetear_clave_y_enviar_mail.short_description = "Resetear claves y avisar por correo electrónico"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('importar-csv/', self.importar_csv, name='importar_csv'),
        ]
        return my_urls + urls

    def importar_csv(self, request):
        initial = {'entidades': (('USUARIO', 'Usuario'),),
                   'entidad': 'USUARIO'}
        errores_lista = []
        if request.method == "POST":
            form = ImportarCSVForm(request.POST, request.FILES, initial=initial)
            if form.is_valid():
                csv = request.FILES["archivo"]
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
                                username = values[0].replace("'", "").strip()
                                first_name = None
                                last_name = None
                                email = None
                                email_contacto = None
                                grupo = None
                                password = None
                                nivel = None
                                if len(values) > 1:
                                    if len(username) > 150:
                                        username = username[0:150]
                                    first_name = values[1].replace("'", "").strip()
                                    if len(values) > 2:
                                        last_name = values[2].replace("'", "").strip()
                                        if len(values) > 3:
                                            email = values[3].replace("'", "").strip()
                                            if len(values) > 4:
                                                email_contacto = values[4].replace("'", "").strip()
                                                if len(values) > 5:
                                                    grupo = values[5].replace("'", "").strip()
                                                    if len(grupo) > 150:
                                                        grupo = grupo[0:150]
                                                    if grupo:
                                                        try:
                                                            grupo = Group.objects.get(name=grupo)
                                                        except Exception as e:
                                                            errores += 1
                                                            e = 'El grupo ' + grupo + \
                                                                ' no existe. ' + \
                                                                'Se importa igual, pero sin grupo'
                                                            errores_lista = agregar_a_errores(cnt, errores, e,
                                                                                              errores_lista)
                                                            grupo = None
                                                    if len(values) > 6:
                                                        password = values[6].replace("'", "").strip()
                                                        if len(values) > 7:
                                                            nivel = values[7].replace("'", "").strip()

                                if es_valido(email):
                                    if email_valido(email):
                                        if User.objects.filter(email=email).exclude(username=username).exists():
                                            errores += 1
                                            e = 'El e-mail principal de ' + username + ' "' + email + \
                                                '" ya está asignado a otro usuario. ' + \
                                                'Se deja vacío'
                                            errores_lista = agregar_a_errores(cnt, errores, e, errores_lista)
                                            email = None
                                    else:
                                        errores += 1
                                        e = 'El e-mail principal de ' + username + ' "' + email + \
                                            '" no es válido. Se deja vacío'
                                        errores_lista = agregar_a_errores(cnt, errores, e, errores_lista)
                                        email = None
                                if nivel:
                                    try:
                                        nivel = Tabla.objects.get(codigo=nivel, entidad='NIVEL')
                                    except Tabla.DoesNotExist:
                                        errores += 1
                                        e = 'El código de nivel "' + nivel + \
                                            '" no existe en tabla de niveles. ' + \
                                            'Se importa igual, pero sin nivel.'
                                        errores_lista = agregar_a_errores(cnt, errores, e, errores_lista)
                                        nivel = None

                                try:
                                    user = User.objects.get(username=username)
                                    if first_name:
                                        user.first_name = first_name
                                    if last_name:
                                        user.last_name = last_name
                                    if email:
                                        user.email = email
                                    if password:
                                        user.set_password(password)
                                    user.save()
                                    actualizados += 1
                                    exitos += 1
                                except User.DoesNotExist:
                                    user = User.objects.create_user(username=username,
                                                                    first_name=first_name,
                                                                    last_name=last_name,
                                                                    email=email,
                                                                    is_active=True,
                                                                    )
                                    if password:
                                        user.set_password(password)
                                    user.save()
                                    nuevos += 1
                                    exitos += 1
                                if user:
                                    if es_valido(email_contacto) or nivel:
                                        perfil, creado = Perfil.objects.get_or_create(user_id=user.id)
                                        if es_valido(email_contacto):
                                            perfil.email_contacto = email_contacto
                                        if nivel:
                                            perfil.nivel.add(nivel)
                                        perfil.save()
                                    if grupo:
                                        grupo.user_set.add(user)

                        except Exception as e:
                            errores += 1
                            errores_lista = agregar_a_errores(cnt, errores, e, errores_lista)
                except Exception as e:
                    msj = e

                if msj:
                    messages.add_message(request, messages.ERROR, msj)
                else:
                    msj = 'Carga de usuarios: {} error(es); {} actualizado(s); {} nuevo(s)'.format(errores,
                                                                                             actualizados,
                                                                                             nuevos)
                    if errores_lista:
                        messages.add_message(request, messages.ERROR, msj)
                    else:
                        messages.add_message(request, messages.INFO, msj)
                        return redirect("..")
        else:
            form = ImportarCSVForm(initial=initial)

        formato = 'Nombre de usuario C(150) ; Nombre C(60); Apellido C(150); ' \
                  'E-mail principal (C254); E-mail de contacto C(100); Grupo (C150); ' \
                  'Contraseña (C128); Código de nivel C(10). Codificación UTF-8'
        contexto = {'form': form, 'formato': formato,
                    'errores': errores_lista,
                    'titulo': 'Usuarios',
                    'entidad': 'user'}
        return render(request, "csv_form.html", contexto)


class PreferenciaAdmin(SimpleHistoryAdmin):
    list_display = ("usuario", "vista", "opcion", "fecha", "numero", "caracter", "logico")
    search_fields = ["usuario__first_name", "usuario__last_name", "usuario__username",
                     "vista", "opcion", "fecha", "numero", "caracter", "logico"]
    change_list_template = "preferencias_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('copiar_preferencias/', self.copiar_preferencias, name='copiar_preferencias'),
        ]
        return my_urls + urls

    def copiar_preferencias(self, request):
        if request.method == "POST":
            form = CopiarPreferenciasForm(request.POST)
            if form.is_valid():
                usuarios_destino = form.cleaned_data['usuarios_destino']
                usuario_origen = form.cleaned_data['usuario_origen']
                usuario_origen = User.objects.get(id=usuario_origen)
                reemplazar = form.cleaned_data['reemplazar']
                hubo_cambios = False
                usuario_origen_preferencias = Preferencia.objects.filter(usuario=usuario_origen)
                if usuario_origen_preferencias.count() > 0:
                    for usuario_destino in usuarios_destino:
                        if usuario_origen != usuario_destino:
                            usuario_destino_preferencias = Preferencia.objects.filter(usuario=usuario_destino)
                            if reemplazar == 'R' and usuario_destino_preferencias.count() > 0:
                                hubo_cambios = True
                                usuario_destino_preferencias.delete()
                            for preferencia in usuario_origen_preferencias:
                                hubo_cambios = True
                                usuario_destino_pref, creado = Preferencia.objects.\
                                    get_or_create(usuario=usuario_destino,
                                                  vista=preferencia.vista,
                                                  opcion=preferencia.opcion)
                                usuario_destino_pref.fecha = preferencia.fecha
                                usuario_destino_pref.caracter = preferencia.caracter
                                usuario_destino_pref.numero = preferencia.numero
                                usuario_destino_pref.logico = preferencia.logico
                                usuario_destino_pref.save()
                    if hubo_cambios:
                        messages.add_message(request, messages.INFO, 'Preferencias copiadas')
                    else:
                        messages.add_message(request, messages.INFO, 'No se copió ninguna preferencia')
                    return redirect("..")
                else:
                    msj = 'El usuario seleccionado no tiene preferencias para copiar'
                    messages.add_message(request, messages.WARNING, msj)
        else:
            form = CopiarPreferenciasForm()

        contexto = {'form': form,
                    'usuarios_destino': '',
                    }
        return render(request, "usuarios_copiar_preferencias.html", contexto)


class GroupAdminForm(forms.ModelForm):
    pass


# Definir un nuevo GroupAdmin
class GroupAdmin(BaseGroupAdmin):
    list_display = ('name', 'dependencia')
    search_fields = ['name', 'dependencia']
    form = GroupAdminForm
    change_list_template = "grupos_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('importar-csv/', self.importar_csv, name='importar_csv'),
            path('copiar_permisos/', self.copiar_permisos, name='copiar_permisos'),
        ]
        return my_urls + urls

    def copiar_permisos(self, request):
        if request.method == "POST":
            form = CopiarPermisosGrupoForm(request.POST)
            if form.is_valid():
                grupos_destino = form.cleaned_data['grupos_destino']
                grupo_origen = form.cleaned_data['grupo_origen']
                grupo_origen = Group.objects.get(id=grupo_origen)
                reemplazar = form.cleaned_data['reemplazar']
                hubo_cambios = False
                grupo_origen_permisos = grupo_origen.permissions.all()
                if grupo_origen_permisos.count() > 0:
                    for grupo_destino in grupos_destino:
                        if grupo_origen != grupo_destino:
                            if reemplazar == 'R' and grupo_destino.permissions.count() > 0:
                                hubo_cambios = True
                                grupo_destino.permissions.clear()
                            for permiso in grupo_origen_permisos:
                                hubo_cambios = True
                                grupo_destino.permissions.add(permiso)
                    if hubo_cambios:
                        messages.add_message(request, messages.INFO, 'Permisos copiados')
                    else:
                        messages.add_message(request, messages.INFO, 'No se copió ningún permiso')
                    return redirect("..")
                else:
                    msj = 'El grupo seleccionado no tiene permisos para copiar'
                    messages.add_message(request, messages.WARNING, msj)
        else:
            form = CopiarPermisosGrupoForm()

        contexto = {'form': form,
                    'grupos_destino': '',
                    }
        return render(request, "grupos_copiar_permisos.html", contexto)

    def importar_csv(self, request):
        initial = {'entidades': (('GRUPO', 'Grupo'),),
                   'entidad': 'GRUPO'}
        errores_lista = []
        if request.method == "POST":
            form = ImportarCSVForm(request.POST, request.FILES, initial=initial)
            if form.is_valid():
                csv = request.FILES["archivo"]
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
                                name = values[0].replace("'", "").strip()
                                dependencia = None
                                if len(name) > 150:
                                    name = name[0:150]
                                if len(values) > 1:
                                    dependencia = values[1].replace("'", "").strip()
                                    if len(dependencia) > 10:
                                        dependencia = dependencia[0:10]

                                if dependencia:
                                    try:
                                        dependencia = Tabla.objects.get(codigo=dependencia, entidad='DEPENDENCIA')
                                        dependencia = dependencia.id
                                    except Tabla.DoesNotExist:
                                        errores += 1
                                        e = 'No existe la dependencia ' + dependencia + \
                                            '. Se deja vacía'
                                        errores_lista = agregar_a_errores(cnt, errores, e, errores_lista)
                                        dependencia = None

                                try:
                                    group = Group.objects.get(name=name)
                                    if dependencia:
                                        group.dependencia = dependencia
                                    group.save()
                                    actualizados += 1
                                    exitos += 1
                                except Group.DoesNotExist:
                                    group = Group(name=name,
                                                  dependencia=dependencia,
                                                  )
                                    group.save()
                                    nuevos += 1
                                    exitos += 1
                        except Exception as e:
                            errores += 1
                            errores_lista = agregar_a_errores(cnt, errores, e, errores_lista)
                except Exception as e:
                    msj = e

                if msj:
                    messages.add_message(request, messages.ERROR, msj)
                else:
                    msj = 'Carga de grupos: {} errores; {} actualizados; {} nuevos'.format(errores,
                                                                                           actualizados,
                                                                                           nuevos)
                    if errores_lista:
                        messages.add_message(request, messages.ERROR, msj)
                    else:
                        messages.add_message(request, messages.INFO, msj)
                        return redirect("..")
        else:
            form = ImportarCSVForm(initial=initial)

        formato = 'Grupo C(150) ; Código de dependencia C(10). Codificación UTF-8'
        contexto = {'form': form, 'formato': formato,
                    'errores': errores_lista,
                    'titulo': 'Grupos',
                    'entidad': 'group'}
        return render(request, "csv_form.html", contexto)


# Volver a registrar UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# Volver a registrar GroupAdmin
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(Preferencia, PreferenciaAdmin)


def agregar_a_errores(fila, errores, mensaje, errores_lista):
    if errores <= 10:
        if errores == 10:
            errores_lista.append('Hay más errores...')
        else:
            errores_lista.append('Fila {}: {}'.format(fila + 1, mensaje))
    return errores_lista
