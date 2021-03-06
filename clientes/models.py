from django.db import models
from django.utils.translation import ugettext as _
from articulos.models import Articulo

# Create your models here.
from tabla.listas import IVAS


class Cliente(models.Model):
    clicod = models.CharField(max_length=5, verbose_name='Código', null=False, blank=False)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    cuit = models.CharField(max_length=13, null=True, blank=True)
    domicilio = models.CharField(max_length=60, null=True, blank=True)
    telefono = models.CharField(verbose_name='Teléfono', max_length=60, null=True, blank=True)
    email = models.EmailField(verbose_name='E-mail', max_length=60, null=True, blank=True)
    encriptado = models.CharField(max_length=10, null=True, blank=True)
    tipoiva = models.CharField(max_length=60, default='I', choices=IVAS)
    saldo_inicial = models.FloatField(max_length=12, null=True, blank=True)
    fecha_saldo = models.DateField(null=True, blank=True)

    def _get_tipocmp(self):
        if self.tipoiva == "A":
            return "01"
        else:
            if self.tipoiva == "B":
                return "06"
            else:
                return "Undefined"

    tipocmp = property(_get_tipocmp)

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
    pdf = models.FileField(null=True, blank=False)
    cae = models.CharField(max_length=20, null=True, blank=True)
    vencimiento_cae = models.DateField(null=True, blank=True)
    pendiente = models.BooleanField(null=False, blank=False, default=False)
    cptedh = models.CharField(max_length=1, null=True, blank=False)

    def _get_numero(self):
        num = self.comprobante.split('-')[3]
        while len(num) < 8:
            num = "0" + num
        return num

    numero = property(_get_numero)

    def _get_sucursal(self):
        suc = self.comprobante.split('-')[2]
        while len(suc) < 4:
            suc = "0" + suc
        return suc

    sucursal = property(_get_sucursal)

    def _get_tipocmp(self):
        return self.comprobante.split('-')[1]

    tipocmp = property(_get_tipocmp)

    def _get_subtotal(self):
        subt = (self.total / 121) * 100
        return "{:.2f}".format(subt)

    subtotal = property(_get_subtotal)

    def _get_iva(self):
        i = (self.total / 121) * 21
        return "{:.2f}".format(i)

    iva = property(_get_iva)

    def _getiva27(self):
        i = (self.total / 121) * 27
        return "{:.2f}".format(i)

    iva27 = property(_getiva27)

    class Meta:
        permissions = (("clientes.cuentas_agregar", _("Agregar")),
                       ("clientes.cuentas_editar", _("Editar")),
                       ("clientes.cuentas_eliminar", _("Eliminar")),
                       ("clientes.cuentas_listar", _("Listar")),
                       ("clientes.cuentas_listar_admin", _("Listar Admin")),
                       ("clientes.cuenta_corriente", _("Cuenta Corriente")),
                       )


class CuentasD(models.Model):
    vtacod = models.IntegerField(null=False, blank=False)
    articulo = models.ForeignKey(Articulo, on_delete=models.DO_NOTHING, null=True, blank=False)
    cantidad = models.FloatField(null=False, blank=False, default=1)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.IntegerField(null=True, blank=True)

    class Meta:
        permissions = (("clientes.cuentas_agregar", _("Agregar")),
                       ("clientes.cuentas_editar", _("Editar")),
                       ("clientes.cuentas_eliminar", _("Eliminar")),
                       ("clientes.cuentas_listar", _("Listar")),
                       ("clientes.cuentas_listar_admin", _("Listar Admin")),
                       ("clientes.cuenta_corriente", _("Cuenta Corriente")),
                       )
