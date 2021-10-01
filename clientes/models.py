from django.db import models


# Create your models here.
class Cliente(models.Model):
    clicod = models.CharField(max_length=5, verbose_name='Código', null=False, blank=False)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    cuit = models.CharField(max_length=13, null=True, blank=True)
    domicilio = models.CharField(max_length=60, null=True, blank=True)
    telefono = models.CharField(verbose_name='Teléfono', max_length=60, null=True, blank=True)
    email = models.EmailField(verbose_name='E-mail', max_length=60, null=True, blank=True)


class Cuentas(models.Model):
    vtacod = models.IntegerField(null=False, blank=False)
    comprobante = models.CharField(max_length=20, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, verbose_name='Cliente', null=False, blank=False, on_delete=models.DO_NOTHING)
    fecha_emision = models.DateField(verbose_name='Fecha Emisión', null=False, blank=False)
    fecha_vencimiento = models.DateField(verbose_name='Vencimiento', null=False, blank=False)
    total = models.IntegerField(null=False, blank=False)
    concepto = models.TextField(null=True, blank=True)
    pdf = models.FileField(null=True, blank=True)
