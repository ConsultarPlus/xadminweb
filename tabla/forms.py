from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, ButtonHolder, HTML
from crispy_forms.bootstrap import FieldWithButtons
from .models import Tabla, Variable, Plantilla
from .gets import list_registros_de_entidad, get_choices
from .listas import ENTIDADES, ITEMS_X_PAG, HOJAS, grupos_de_etiquetas
from .funcs import boton_buscar
from .widgets import SelectLiveSearchInput


class ImportarCSVForm(forms.Form):
    entidad = forms.CharField()
    archivo = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            entidades = kwargs['initial']['entidades']
        except Exception as e:
            entidades = ENTIDADES

        self.fields['entidad'].widget = SelectLiveSearchInput(choices=entidades)
        self.fields['entidad'].initial = kwargs['initial']['entidad']
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control-sm'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('entidad', css_class='form-group col-md-2 mb-0 '),
                Column('archivo', css_class='form-group-sm col-md-4 mb-0'),
                css_class='form-row'
            ),
            HTML('<br>'),
            ButtonHolder(
                Submit('submit', 'Importar'),
                Button('cancel', 'Volver', css_class='btn-default', onclick="window.history.back()")
            )
        )


class TablaForm(forms.ModelForm):

    class Meta:
        model = Tabla
        fields = {'entidad', 'codigo', 'descripcion', 'superior_entidad',
                  'superior_codigo', 'valor_preferencial', 'activo'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        entidades_sup = (('', '----'),) + ENTIDADES
        self.fields['entidad'].widget = SelectLiveSearchInput(choices=ENTIDADES)
        self.fields['superior_entidad'].widget = SelectLiveSearchInput(choices=entidades_sup)
        self.fields['superior_codigo'].widget = SelectLiveSearchInput(choices=())
        self.fields['superior_entidad'].label = 'Entidad superior'
        self.fields['superior_codigo'].label = 'Código de la entidad superior'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control-sm'

        if self.instance.pk:
            self.fields['entidad'].widget.attrs['disabled'] = True
            self.fields['codigo'].widget.attrs['disabled'] = True
            entidad = self.instance.superior_entidad
            if entidad:
                lista = list_registros_de_entidad(entidad)
                self.fields['superior_codigo'].widget = SelectLiveSearchInput(choices=lista)
                self.fields['superior_codigo'].label = entidad
        else:
            if 'superior_entidad' in self.data:
                try:
                    entidad = self.instance.superior_entidad
                    if entidad:
                        self.fields['superior_codigo'].queryset = list_registros_de_entidad(entidad)
                        self.fields['superior_codigo'].label = entidad
                except (ValueError, TypeError):
                    pass
            try:
                entidad = kwargs['initial']['entidad']
                if entidad is not None and entidad != '':
                    self.fields['entidad'].initial = entidad
            except (ValueError, TypeError):
                pass

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('entidad', css_class='form-group col-md-3 mb-0 '),
                Column('codigo', css_class='form-group-sm col-md-2 mb-0 '),
                Column('descripcion', css_class='form-group-sm col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('superior_entidad', css_class='form-group col-md-4 mb-0'),
                Column('superior_codigo', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('valor_preferencial', css_class='form-group col-md-2 mb-0'),
                Column('activo', css_class='form-group col-md-2 mb-0'),
            ),
            ButtonHolder(
                Submit('submit', 'Grabar'),
                Button('cancel', 'Volver', css_class='btn-default', onclick="window.history.back()")
            )
        )


class VariableForm(forms.ModelForm):

    class Meta:
        model = Variable
        fields = {'variable', 'descripcion', 'tipo', 'fecha', 'caracter', 'numero', 'logico'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['fecha'].widget.attrs['disabled'] = True
        self.fields['caracter'].widget.attrs['disabled'] = True
        self.fields['numero'].widget.attrs['disabled'] = True
        self.fields['logico'].widget.attrs['disabled'] = True
        if 'tipo' in self.data or self.instance.pk:
            tipo = self.instance.tipo
            if tipo == "C":
                self.fields['caracter'].widget.attrs['disabled'] = False
            elif tipo == "F":
                self.fields['fecha'].widget.attrs['disabled'] = False
            elif tipo == "N":
                self.fields['numero'].widget.attrs['disabled'] = False
            elif tipo == "L":
                self.fields['logico'].widget.attrs['disabled'] = False
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control-sm'

        self.helper = FormHelper()
        # self.helper.form_action = """ JavaScript:{window.location.replace(window.location)} """
        self.helper.layout = Layout(
            Row(
                Column('variable', css_class='form-group col-md-3 mb-0 '),
                Column('descripcion', css_class='form-group-sm col-md-6 mb-0 '),
                css_class='form-row'
            ),
            Row(
                Column('tipo', css_class='form-group col-md-2 mb-0'),
                Column('fecha', css_class='form-group col-md-2 mb-0'),
                Column('caracter', css_class='form-group col-md-2 mb-0'),
                Column('numero', css_class='form-group col-md-2 mb-0'),
                Column('logico', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Grabar'),
                Button('cancel', 'Volver', css_class='btn-default', onclick="window.history.back()")
            )
        )


class PlantillaForm(forms.ModelForm):
    grupo_etiquetas = forms.CharField(max_length=60,
                                      required=False,
                                      label='Grupo de etiquetas')
    etiqueta = forms.CharField(max_length=60,
                               required=False,
                               help_text='Ctrl+V para pegar la etiqueta seleccionada')

    class Meta:
        model = Plantilla
        fields = {'descripcion', 'activo', 'plantilla', 'tipo_comprobante', 'hoja'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        nada = (('', 'Seleccionar etiqueta'),)
        self.fields['grupo_etiquetas'].widget = SelectLiveSearchInput(choices=grupos_de_etiquetas)
        self.fields['etiqueta'].widget = SelectLiveSearchInput(choices=nada)
        self.fields['tipo_comprobante'].widget = SelectLiveSearchInput(choices=get_choices('COMPROBANTE'))
        self.fields['hoja'].widget = SelectLiveSearchInput(choices=HOJAS)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control-sm'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('descripcion', css_class='form-group-sm col-md-4 mb-0 '),
                Column('activo', css_class='form-group-sm col-md-1 mb-0 '),
                Column('tipo_comprobante', css_class='form-group-sm col-md-2 mb-0 '),
                css_class='form-row'
            ),
            Row(
                Column('grupo_etiquetas', css_class='form-group-sm col-md-2 mb-0 '),
                Column('etiqueta', css_class='form-group-sm col-md-2 mb-0 ', onchange="copiar_etiqueta()"),
                Column('hoja', css_class='form-group-sm col-md-2 mb-0 '),
                css_class='form-row'
            ),
            'plantilla',
            ButtonHolder(
                Submit('submit', 'Grabar'),
                Button('cancel', 'Volver', css_class='btn-default', onclick="window.history.back()")
            )
        )


class FiltroSimple(forms.Form):
    buscar = forms.CharField(max_length=60, required=False)
    modo = forms.CharField(max_length=2, required=False)
    items = forms.IntegerField(max_value=30,
                               min_value=5,
                               required=False,
                               label='ítems x pág.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.disable_csrf = True
        self.fields['buscar'].label = ''
        self.fields['items'].label = ''
        self.fields['items'].widget = SelectLiveSearchInput(choices=ITEMS_X_PAG)
        self.fields['modo'].widget.attrs['hidden'] = True
        self.fields['modo'].label = ""

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control-sm'

        self.helper.layout = Layout(
            Row(
                Column('buscar', css_class='form-group col-md-5 mb-0 '),
                FieldWithButtons('items', boton_buscar(), css_class='form-group col-md-2 mb-0'),
            ),
            'modo',
        )


class FiltroTablas(forms.Form):
    buscar = forms.CharField(max_length=60, required=False)
    entidad = forms.CharField(max_length=60, required=False)
    modo = forms.CharField(max_length=3, required=False)
    superior_entidad = forms.CharField(max_length=60, required=False)
    items = forms.IntegerField(max_value=30,
                               min_value=5,
                               required=False,
                               label='ítems x pág.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            entidad_off = kwargs['initial']['entidad_off']
        except Exception as e:
            entidad_off = 'N'

        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.disable_csrf = True

        entidades_sup = (('', 'TODAS'),) + ENTIDADES
        self.fields['entidad'].widget = SelectLiveSearchInput(choices=sorted(entidades_sup))
        self.fields['items'].widget = SelectLiveSearchInput(choices=ITEMS_X_PAG)
        self.fields['modo'].widget.attrs['hidden'] = True
        self.fields['modo'].label = ""

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control-sm'

        if entidad_off == 'S':
            self.fields['entidad'].widget.attrs['disabled'] = True

        self.helper.layout = Layout(
            Row(
                Column('entidad', css_class='form-group col-md-2 mb-0 '),
                Column('superior_entidad', css_class='form-group col-md-2 mb-0 '),
                Column('buscar', css_class='form-group col-md-2 mb-0 '),
                FieldWithButtons('items', boton_buscar(), css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            'modo',
        )
