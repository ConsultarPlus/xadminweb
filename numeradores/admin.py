from django.contrib import admin
from .models import Numerador
from simple_history.admin import SimpleHistoryAdmin


class NumeradorAdmin(SimpleHistoryAdmin):
    list_display = ('comprobante', 'descripcion', 'activo')


# admin.site.register(Numerador, NumeradorAdmin)
