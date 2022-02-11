from django.contrib import admin
from . models import Documento
from simple_history.admin import SimpleHistoryAdmin


class DocumentoAdmin(SimpleHistoryAdmin):
    list_display = ('entidad', 'descripcion', 'archivo')


# admin.site.register(Documento, DocumentoAdmin)

