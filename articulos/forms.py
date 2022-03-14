from django import forms
from .models import Articulo
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, ButtonHolder, HTML
from xadmin.settings import MEDIA_URL, STATIC_URL
from crispy_forms.bootstrap import FieldWithButtons
from tabla.listas import ITEMS_X_PAG
from tabla.widgets import SelectLiveSearchInput
from tabla.funcs import boton_buscar
from tabla.gets import get_choices


class ArticuloForm(forms.ModelForm):

    class Meta:
        model = Articulo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['artcod'].label = 'Código'
        self.fields['descripcion'].label = 'Descripición'
        self.fields['marca'].label = 'Marca'
        self.fields['color'].label = 'Color'
        self.fields['seccion'].label = 'Seccion'
        self.fields['seccion'].enabled = False
        self.fields['rubro'].label = 'Rubro'
        self.fields['rubro'].enabled = False
        self.fields['codbar'].label = 'codbar'
        self.fields['iva'].label = 'Iva %'
        self.fields['precio'].label = 'Precio'
        self.fields['moneda'].label = 'Moneda'
        self.fields['departamento'].label = 'Departamento'
        self.fields['departamento'].widget = SelectLiveSearchInput(choices=get_choices('DEPARTAMENTO'))
        self.fields['artuniven'].label = 'Unidad'
        self.fields['descextra'].label = 'Descripción Extra'
        self.fields['ubicacion'].label = 'Ubicación'
        self.fields['artimg'].label = 'Imagen'

        link = ""
        if self.instance.pk:
            if self.instance.artimg:
                img = MEDIA_URL+str(self.instance.artimg)
            else:
                img = STATIC_URL + "img/usuario_incognito.png"
            link = """ <div  class="col form-group col-md-10 mb-0 " > """
            link += """ <div id="div_foto_preview" class="form-group"> """
            link += """ <div class=""><a>"""
            link += """ <img class ="preview foto-id" src=" """ + img + """"></a>"""
            link += """ </div></div></div> """

        self.helper = FormHelper()
        self.helper.form_id = 'id_form'
        self.helper.layout = Layout(
            Row(
                Column('artcod', css_class='form-group col-md-2 mb-0'),
                Column('descripcion', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('descextra', css_class='form-group col-md-7 mb-0'),
                css_class='form-row'
            ),

            Row(
                Column('departamento', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('rubro', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('seccion', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('marca', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('color', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('codbar', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('iva', css_class='form-group col-md-1     mb-0'),
                Column('%'),
                css_class='form-row'
            ),
            Row(
                Column('precio', css_class='form-group col-md-3 mb-0'),
                Column('moneda', css_class='form-group col-md-2 mb-0'),
                css_class='form-row',
            ),
            Row(
                Column('artuniven', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('ubicacion', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
                ),
            Row(
                Column('artimg', css_class='form-group col-md-5 mb-0'),
                Column(HTML(link), css_class='form-group col-md-7 mb-'),
                css_class='form-row'
                ),
            ButtonHolder(
                Submit('submit', 'Grabar'),
                Button('cancel', 'Volver', css_class='btn-default', onclick="window.history.back()")
            )
        )


class FiltroArticulo(forms.Form):
    departamento = forms.CharField(max_length=30, required=False)
    buscar = forms.CharField(max_length=60, required=False)
    modo = forms.CharField(required=False)
    items = forms.IntegerField(max_value=30,
                             min_value=5,
                              required=False,
                              label='items x pag.')

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
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
            Row(
                Column('departamento', css_class='form-group col-md-3 mb-0 ')
            ),
            'modo'
        )


