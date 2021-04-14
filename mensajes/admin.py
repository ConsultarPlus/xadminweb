from django.contrib import admin
from . models import Mensaje
from simple_history.admin import SimpleHistoryAdmin


class MensajeAdmin(SimpleHistoryAdmin):
    list_display = ('fecha', 'hora', 'mensaje', 'remitente')


# admin.site.register(Mensaje, MensajeAdmin)
