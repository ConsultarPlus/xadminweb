from django.db import models
from django.utils.translation import ugettext as _


# Create your models here.
class Cliente(models.Model):
    clicod = models.CharField(max_length=5, verbose_name='Código', null=False, blank=False)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    cuit = models.CharField(max_length=13, null=True, blank=True)
    domicilio = models.CharField(max_length=60, null=True, blank=True)
    telefono = models.CharField(verbose_name='Teléfono', max_length=60, null=True, blank=True)
    email = models.EmailField(verbose_name='E-mail', max_length=60, null=True, blank=True)
    encriptado = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return "{}".format(self.clicod)

    class Meta:
        permissions = (("clientes.cliente_agregar", _("Agregar")),
                       ("clientes.cliente_editar", _("Editar")),
                       ("clientes.cliente_eliminar", _("Eliminar")),
                       ("clientes.puede_listar", _("Listar")),
                       )


class Cuentas(models.Model):
    vtacod = models.IntegerField(null=False, blank=False)
    comprobante = models.CharField(max_length=20, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, verbose_name='Cliente', null=False, blank=False, on_delete=models.DO_NOTHING)
    fecha_emision = models.DateField(verbose_name='Fecha Emisión', null=False, blank=False)
    fecha_vencimiento = models.DateField(verbose_name='Vencimiento', null=False, blank=False)
    total = models.IntegerField(null=False, blank=False)
    concepto = models.TextField(null=True, blank=True)
    pdf = models.FileField(null=True, blank=True)

    class Meta:
        permissions = (("clientes.cuentas_agregar", _("Agregar")),
                       ("clientes.cuentas_editar", _("Editar")),
                       ("clientes.cuentas_eliminar", _("Eliminar")),
                       ("clientes.cuentas_listar", _("Listar")),
                       ("clientes.cuenta_corriente", _("Cuenta Corriente")),
                       )