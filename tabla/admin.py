from django.contrib import admin, messages
from django.contrib.sessions.models import Session
from django.contrib.auth.models import Permission, User
from django.core.exceptions import ObjectDoesNotExist
from simple_history.admin import SimpleHistoryAdmin
from xadmin.settings import SESSION_COOKIE_AGE
from datetime import timedelta
from .models import Traduccion
from .funcs import fecha_actual


class TablaAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'entidad', 'codigo', 'descripcion', 'activo', 'superior_entidad', 'superior_codigo')
    search_fields = list_display
    history_list_display = ["status"]

    list_filter = ('entidad', 'superior_codigo', 'activo')
    ordering = ('entidad',)
    # filter_horizontal = ('entidad', 'superior_entidad') debe ser many to many field


class VariableAdmin(SimpleHistoryAdmin):
    list_display = ('variable', 'descripcion', 'tipo', 'fecha', 'numero', 'caracter', 'logico')
    search_fields = list_display


class TraduccionAdmin(SimpleHistoryAdmin):
    list_display = ('modelo', 'palabra', 'traduccion')
    search_fields = list_display


class PermisosAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'name', 'codename')
    search_fields = ['name', 'codename']


class SessionAdmin(admin.ModelAdmin):
    actions = ['eliminar_sesiones_caducadas']

    def eliminar_sesiones_caducadas(self, request, sessions):
        hoy = fecha_actual()
        eliminados = 0
        for session in sessions:
            if session.expire_date < hoy:
                eliminados += 1
                session.delete()

        if eliminados == 0:
            msj = 'No hay sesiones caducadas'
        elif eliminados == 1:
            msj = 'Se eliminó una sesión caducada'
        else:
            msj = 'Se eliminaron {} sesiones caducadas'.format(eliminados)

        messages.add_message(request, messages.INFO, msj)

    def _session_data(self, obj):
        return obj.get_decoded()

    def user_name(self, obj):
        session = Session.objects.get(session_key=obj.session_key)
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')
        try:
            user = User.objects.get(id=user_id)
            user_name = user.username
        except ObjectDoesNotExist:
            user_name = 'Sesión caducada sin reingreso'

        return user_name

    def fecha(self, obj):
        session = Session.objects.get(session_key=obj.session_key)
        dias = ((SESSION_COOKIE_AGE/60)/60)/24
        fecha = session.expire_date - timedelta(days=dias)

        return fecha

    user_name.short_description = 'Usuario'

    list_display = ['session_key', 'user_name', 'fecha', 'expire_date']
    search_fields = ['session_key', 'expire_date']
    ordering = ('-expire_date',)


admin.site.register(Session, SessionAdmin)
admin.site.register(Permission, PermisosAdmin)
# admin.site.register(Tabla, TablaAdmin)
# admin.site.register(Variable, VariableAdmin)
admin.site.register(Traduccion, TraduccionAdmin)
