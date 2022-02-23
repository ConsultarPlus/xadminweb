from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


class Mensaje(models.Model):
    remitente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=User)
    destinatarios = models.ManyToManyField(User, blank=True,
                                           help_text="Para eliminar de la selección Ctrl+Clic sobre el item",
                                           related_name='destinatarios')
    mensaje = models.TextField(verbose_name='Mensaje', null=True)
    fecha = models.DateField()
    hora = models.TimeField(null=True, blank=True)
    history = HistoricalRecords(table_name='historico_mensaje')

    class Meta:
        permissions = (("mensaje_puede_agregar", _("Agregar")),
                       ("mensaje_puede_editar", _("Editar")),
                       ("mensaje_puede_eliminar", _("Eliminar")),
                       ("mensaje_puede_listar", _("Listar")),
                       )

    def __str__(self):
        return "{} {}, {}, {}".format(self.fecha, self.hora, self.remitente, self.mensaje[:37] + '...')


class Destinatario(models.Model):
    mensaje = models.ForeignKey(Mensaje, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=User,
                                related_name='destinatario')
    fecha_visto = models.DateField(null=True, blank=True)
    hora_visto = models.TimeField(null=True, blank=True)

    class Meta:
        permissions = (("destinatario_puede_agregar", _("Agregar")),
                       ("destinatario_puede_eliminar", _("Eliminar")),
                       )

    def __str__(self):
        return '%s, %s %s' % (self.usuario, self.fecha_visto, self.hora_visto)

