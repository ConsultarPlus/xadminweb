from django.db import models
from django.utils.translation import ugettext as _
from tabla.listas import APLICACIONES
from simple_history.models import HistoricalRecords


class Documento(models.Model):
    entidad = models.CharField(max_length=20, choices=APLICACIONES)
    entidad_id = models.IntegerField()
    descripcion = models.CharField(max_length=60, blank=True, verbose_name='Descripción',
                                   help_text='Aclare el contenido del archivo si el nombre del archivo es difuso')
    archivo = models.FileField(upload_to='documentos/')
    history = HistoricalRecords(table_name='historico_documento')

    class Meta:
        permissions = (("documento_puede_agregar", _("Agregar")),
                       ("documento_puede_editar", _("Editar")),
                       ("documento_puede_eliminar", _("Eliminar")),
                       ("documento_puede_listar", _("Listar")),
                       )

    def __str__(self):
        return "{}, {}, {}".format(self.entidad, self.entidad_id, self.archivo)

