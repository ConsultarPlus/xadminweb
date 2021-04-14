from django import forms
from django.urls import reverse
from .models import Documento
from .funcs import clean_archivo_helper
from tabla.listas import APLICACIONES
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, ButtonHolder
# from expediente.models import Persona, Expediente, Comprobante


class DocumentoForm(forms.ModelForm):
    redirect_url = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Documento
        fields = ('entidad', 'entidad_id', 'descripcion', 'archivo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['entidad'].widget = forms.Select(choices=APLICACIONES)

        if self.instance.pk:
            entidad = self.instance.entidad
            entidad_id = self.instance.entidad_id
        else:
            try:
                entidad = kwargs['initial']['entidad']
                entidad_id = kwargs['initial']['entidad_id']
            except Exception as e:
                entidad = 'EXPEDIENTE'
                entidad_id = 0
        url = ''
        if entidad_id > 0:
            # try:
            #     if entidad == 'EXPEDIENTE':
            #     #     qs = Expediente.objects.get(id=entidad_id)
            #     #     descripcion = qs
            #     # elif entidad == 'PERSONA':
            #     #     qs = Persona.objects.get(id=entidad_id)
            #     #     descripcion = qs
            #     # elif entidad == 'COMPROBANTE':
            #     #     qs = Comprobante.objects.get(id=entidad_id)
            #     #     descripcion = qs
            #     else:
            #         descripcion = ''
            #         qs = None
            # except Exception as e:
            descripcion = ''
            qs = None
            url=""
            self.fields['entidad'].label = '%s: %s ' % (entidad, descripcion)
            if qs is not None:
                self.fields['entidad_id'].queryset = qs
                self.fields['entidad_id'].widget.attrs['hidden'] = True
                self.fields['entidad'].widget.attrs['hidden'] = True
                self.fields['entidad_id'].label = ''
                if entidad != 'COMPROBANTE':
                    url = '{}_documento_agregar_y_volver'.format(entidad.lower())
                    url = "cambiar_redirect('" + reverse(url, args=[entidad_id]) + "')"
                else:
                    url = "cambiar_redirect('" + reverse('documento_agregar_y_volver') + "')"
            else:
                url = "cambiar_redirect('" + reverse('documento_agregar_y_volver') + "')"

        self.helper = FormHelper()
        self.helper.form_id = 'id_form'
        self.helper.layout = Layout(
            Row(
                Column('entidad', css_class='form-group col-md-4 mb-0'),
                Column('entidad_id', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('descripcion', css_class='form-group col-md-3 mb-0'),
                Column('archivo', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'redirect_url',
            ButtonHolder(
                Submit('submit1', 'Grabar'),
                # Button('submit2', 'Grabar y agregar otro', css_class='btn-default', onclick=url),
                Button('cancel', 'Volver', css_class='btn-default', onclick="window.history.back()")
            )
        )

    def clean_archivo(self):
        return clean_archivo_helper(self.cleaned_data['archivo'])
