from django import forms
from .models import Cliente, Cuentas
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, ButtonHolder


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id_form'
        self.helper.layout = Layout(
            Row(
                Column('clicod', css_class='form-group col-md-3 mb-0'),
                Column('nombre', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('cuit', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('telefono', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('domicilio', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Grabar'),
                Button('cancel', 'Volver', css_class='btn-default', onclick="window.history.back()")
            )
        )


class CuentasForm(forms.ModelForm):

    class Meta:
        model = Cuentas
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id_form'
        self.helper.layout = Layout(
            Row(
                Column('vtacod', css_class='form-group col-md-1 mb-0'),
                Column('comprobante', css_class='form-group col-md-2 mb-0'),
                Column('cliente', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fecha_emision', css_class='form-group col-md-1 mb-0'),
                Column('fecha_vencimiento', css_class='form-group col-md-2 mb-0'),
                Column('total', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('pdf', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('concepto', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Grabar'),
                Button('cancel', 'Volver', css_class='btn-default', onclick="window.history.back()")
            )
        )