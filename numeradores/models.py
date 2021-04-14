from django.db import models
from simple_history.models import HistoricalRecords
from tabla.listas import ACTIVO
import unidecode


class Numerador(models.Model):
    comprobante = models.CharField(max_length=20, primary_key=True)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción',)
    ultimo_valor = models.IntegerField(null=True, blank=True)
    activo = models.CharField(max_length=1, default="S", choices=ACTIVO)
    history = HistoricalRecords(table_name='historico_numerador')

    def clean(self):
        self.comprobante = self.comprobante.upper().replace(' ', '_')
        self.comprobante = unidecode.unidecode(self.comprobante)
        if self.ultimo_valor is None:
            self.ultimo_valor = 0

    def __str__(self):
        return '%s (%s)' % (self.descripcion, self.ultimo_valor)

    class Meta:
        verbose_name_plural = "numeradores"
