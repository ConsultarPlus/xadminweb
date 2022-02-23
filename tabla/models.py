from django.db import models
from .listas import ENTIDADES, ACTIVO, SINO, TIPOS_DE_VARIABLE, MODELOS
from tinymce import models as tinymce_models
from django.utils.translation import ugettext as _
from simple_history.models import HistoricalRecords
import unidecode


class Tabla(models.Model):
    entidad = models.CharField(max_length=20, choices=sorted(ENTIDADES))
    codigo = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción',)
    superior_id = models.IntegerField(null=True, blank=True)
    superior_entidad = models.CharField(max_length=20, blank=True, choices=sorted(ENTIDADES))
    superior_codigo = models.CharField(max_length=10, blank=True)
    valor_preferencial = models.CharField(max_length=1, default="N", choices=SINO)
    activo = models.CharField(max_length=1, default="S", choices=ACTIVO)
    history = HistoricalRecords(table_name='historico_tabla')

    def clean(self):
        self.codigo = self.codigo.upper()
        self.descripcion = self.descripcion.upper()

    class Meta:
        ordering = ["entidad", 'codigo']
        permissions = (("tabla_puede_agregar", _("Agregar")),
                       ("tabla_puede_editar", _("Editar")),
                       ("tabla_puede_eliminar", _("Eliminar")),
                       ("tabla_puede_listar", _("Listar")),
                       )

    def __str__(self):
        tabla = '%s' % self.descripcion
        if self.entidad == 'LOCALIDAD':
            tabla += ' (' + self.codigo + ')'
        return tabla


class Variable(models.Model):
    variable = models.CharField(max_length=20, primary_key=True)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción',)
    tipo = models.CharField(max_length=20, choices=TIPOS_DE_VARIABLE)
    fecha = models.DateField(null=True, blank=True)
    caracter = models.CharField(max_length=100, null=True, blank=True)
    numero = models.DecimalField(decimal_places=4, max_digits=14, null=True, blank=True)
    logico = models.BooleanField(default=False)
    history = HistoricalRecords(table_name='historico_variable')

    def clean(self):
        self.variable = self.variable.upper().replace(' ', '_')
        self.variable = unidecode.unidecode(self.variable)

    class Meta:
        permissions = (("variable_puede_agregar", _("Agregar")),
                       ("variable_puede_editar", _("Editar")),
                       ("variable_puede_eliminar", _("Eliminar")),
                       ("variable_puede_listar", _("Listar")),
                       )


class Plantilla(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name='Descripción')
    plantilla = tinymce_models.HTMLField(blank=True)
    activo = models.CharField(max_length=1, default="S", choices=ACTIVO)
    tipo_comprobante = models.ForeignKey(Tabla, on_delete=models.DO_NOTHING, null=True, blank=True)
    hoja = models.CharField(max_length=10, verbose_name='Tamaño de hoja', default="A4")
    history = HistoricalRecords(table_name='historico_plantilla')

    def clean(self):
        self.descripcion = self.descripcion.upper()

    class Meta:
        permissions = (("plantilla_puede_agregar", _("Agregar")),
                       ("plantilla_puede_editar", _("Editar")),
                       ("plantilla_puede_eliminar", _("Eliminar")),
                       ("plantilla_puede_listar", _("Listar")),
                       )

    def __str__(self):
        return '%s' % self.descripcion


class Traduccion(models.Model):
    modelo = models.CharField(max_length=60, verbose_name='Pantalla', choices=MODELOS, default='GENERAL')
    palabra = models.CharField(max_length=60)
    traduccion = models.CharField(max_length=60)
    history = HistoricalRecords(table_name='historico_traduccion')

    def __str__(self):
        return 'En {}, {} se traduce como {}'.format(self.modelo, self.palabra, self.traduccion)

    class Meta:
        permissions = (("traduccion_puede_agregar", _("Agregar")),
                       ("traduccion_puede_editar", _("Editar")),
                       ("traduccion_puede_eliminar", _("Eliminar")),
                       ("traduccion_puede_listar", _("Listar")),
                       )
        verbose_name_plural = "Traducciones"
        verbose_name = "Traducción"

    def clean(self):
        self.modelo = self.modelo.upper().replace(' ', '_')
        self.palabra = self.palabra.upper()
