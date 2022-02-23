from django.db import models
from tabla.models import Tabla
from tabla.listas import MONEDA
from tabla.listas import UNIDADES


# Create your models here.
class Articulo(models.Model):
    artcod = models.CharField(max_length=13, null=False, blank=False)
    descripcion = models.CharField(max_length=60, null=True, blank=True)
    iva = models.FloatField(max_length=6, null=True, blank=True, default=21)
    precio = models.FloatField(max_length=12, null=True, blank=True)
    moneda = models.IntegerField(null=True, blank=True, choices=MONEDA, default= 1)
    departamento = models.ForeignKey(Tabla, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='departamento')
    artuniven = models.CharField(max_length=3, null=True, blank=True, choices=UNIDADES, default="UNI" )
    descextra = models.CharField(max_length=255, null=True, blank=True)
    ubicacion = models.CharField(max_length=15, null=True, blank=True)
    artimg = models.FileField(null=True, blank=True)
