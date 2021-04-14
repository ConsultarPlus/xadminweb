from django import forms
from .models import Numerador
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, ButtonHolder


class NumeradorForm(forms.ModelForm):

    class Meta:
        model = Numerador
        fields = 'comprobante', 'descripcion', 'ultimo_valor', 'activo'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('comprobante', css_class='form-group col-md-4 mb-0'),
                Column('descripcion', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('ultimo_valor', css_class='form-group col-md-4 mb-0'),
                Column('activo', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Grabar'),
                Button('cancel', 'Volver', css_class='btn-default', onclick="window.history.back()")
            )
        )
