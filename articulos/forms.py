from django import forms
from .models import Articulo
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, ButtonHolder
from xadmin.settings import MEDIA_URL, STATIC_URL


class ArticuloForm(forms.ModelForm):

    class Meta:
        model = Articulo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['artcod'].label = 'Código'
        self.fields['descripcion'].label = 'Descripición'
        self.fields['iva'].label = 'Iva %'
        self.fields['precio'].label = 'Precio'
        self.fields['moneda'].label = 'Moneda'
        self.fields['departamento'].label = 'Departamento'
        self.fields['artuniven'].label = 'Unidad'
        self.fields['descextra'].label = 'Descripcion Extra'
        self.fields['ubicacion'].label = 'Ubicación'
        self.fields['artimg'].label = 'Imagen'

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
                Column('departamento', css_class='form-group col-md-5 mb-0'),
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
                css_class='form-row'
                ),
            ButtonHolder(
                Submit('submit', 'Grabar'),
                Button('cancel', 'Volver', css_class='btn-default', onclick="window.history.back()")
            )
        )


