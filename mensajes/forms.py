from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, ButtonHolder, HTML
from crispy_forms.bootstrap import FieldWithButtons
from xadmin.settings import MEDIA_URL, STATIC_URL
from tabla.widgets import DatePickerInput, SelectLiveSearchInput
from tabla.funcs import boton_buscar
from tabla.templatetags.custom_tags import traducir
from tabla.listas import ITEMS_X_PAG
from perfiles.models import Perfil
from .models import Mensaje


class MensajeForm(forms.ModelForm):
    fecha = forms.DateTimeField(input_formats=['%d/%m/%Y'], widget=DatePickerInput())
    hr = forms.IntegerField(max_value=24,
                            min_value=0,
                            required=False,
                            label='Hora')
    min = forms.IntegerField(max_value=59,
                             min_value=0,
                             required=False,
                             label='Min.')

    class Meta:
        model = Mensaje
        fields = {'fecha', 'mensaje', 'destinatarios', 'hr', 'min', 'hora', 'remitente'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        horas = []
        for x in range(0, 24):
            horas.append((x, x))
        horas = tuple(horas)

        minutos = []
        for x in range(0, 60):
            minutos.append((x, x))
        minutos = tuple(minutos)

        self.fields['hr'].widget = SelectLiveSearchInput(choices=horas)
        self.fields['min'].widget = SelectLiveSearchInput(choices=minutos)
        self.fields['mensaje'].widget.attrs['rows'] = 5
        self.fields['destinatarios'].queryset = User.objects.none()
        self.fields['hora'].widget.attrs['hidden'] = True
        self.fields['hora'].label = ''
        try:
            visualizar = kwargs['initial']['visualizar']
        except Exception as mensaje:
            visualizar = False

        if not visualizar:
            self.fields['remitente'].widget.attrs['hidden'] = True
            self.fields['remitente'].label = ''

        for field_name, field in self.fields.items():
            if field_name == 'fecha':
                field.widget.attrs['class'] = 'form-control-sm js-date'
            else:
                field.widget.attrs['class'] = 'form-control-sm'
            field.label = traducir(field.label, self._meta.model._meta.model_name)

            if visualizar:
                field.widget.attrs['disabled'] = True

        if self.instance.pk:
            destinatarios_list = self.data.getlist('destinatarios')
            if len(destinatarios_list) > 0:
                destinatarios = User.objects.filter(id__in=destinatarios_list)
            else:
                mensaje = Mensaje.objects.get(id=self.instance.pk)
                destinatarios = mensaje.destinatarios.all()
            self.fields['destinatarios'].queryset = destinatarios
        else:
            if 'destinatarios' in self.data:
                try:
                    destinatarios = self.data.getlist('destinatarios')
                    self.fields['destinatarios'].queryset = User.objects.filter(id__in=destinatarios)
                except (ValueError, TypeError):
                    pass

        try:
            destinatarios = kwargs['initial']['destinatarios']
            if destinatarios:
                qs = User.objects.filter(id__in=destinatarios.split(','))
                self.fields['destinatarios'].queryset = qs
        except Exception as e:
            pass

        self.helper = FormHelper()
        btn_buscar = boton_buscar('buscar', '', 'openWin(1)')
        lay_1 = Layout(
                Row(
                    Column('mensaje', css_class='form-group col-md-6 mb-0'),
                    Column('hora', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('fecha', css_class='form-group col-md-2 mb-0 '),
                    Column('hr', css_class='form-group-sm col-md-1 mb-0 '),
                    Column('min', css_class='form-group-sm col-md-1 mb-0 '),
                    css_class='form-row'
                ),
                )
        lay_2 = Layout(
                Row(
                    FieldWithButtons('destinatarios', btn_buscar, css_class='form-group col-md-6 mb-0'),
                ),
                'remitente',
                ButtonHolder(
                    Submit('submit', 'Grabar'),
                    Button('cancel', 'Volver', css_class='btn-default', onclick="window.history.back()")
                )
                )
        if visualizar:
            foto_id = ""
            if self.instance.pk:
                remitente = self.instance.remitente
                try:
                    usuario = Perfil.objects.get(user=remitente.id)
                    if usuario.foto:
                        img = MEDIA_URL+str(usuario.foto)
                    else:
                        img = STATIC_URL + "img/usuario_incognito.png"
                    foto_id = '<div  class="col form-group col-md-1 mb-0 " > ' +\
                              ' <div id="div_foto_preview" class="form-group"> ' +\
                              ' <div <a>' +\
                              ' <img class="preview foto-id-m" src="' + img + '"> ' +\
                              ' </a> ' +\
                              ' </div></div></div> '.format(img)
                except Exception as e:
                    pass
            link_resp = """ <a class="reply" """ +\
                        """ href="{% url 'mensaje_responder' mensaje_interno.id %}?a_todos=N">Responder</a> """
            link_resp_todos = """ <a class="replyall" """ +\
                              """ href="{% url 'mensaje_responder' mensaje_interno.id %}?a_todos=S"> """ +\
                              """ Responder a todos</a> """

            self.helper.layout = Layout(Row(
                                            HTML(foto_id),
                                            Column('remitente', css_class='form-group col-md-2 mb-0'),
                                            css_class='form-row'
                                        ),
                                        lay_1,
                                        Row(
                                            Column('destinatarios', css_class='form-group col-md-4 mb-0'),
                                        ),
                                        ButtonHolder(
                                            Button('cancel', 'Volver', css_class='btn-default',
                                                   onclick="window.history.back()"),
                                            HTML(link_resp),
                                            HTML(link_resp_todos),
                                        )
                                        )
        else:
            self.helper.layout = Layout(lay_1, lay_2)


class FiltroMensajes(forms.Form):
    texto = forms.CharField(max_length=60, required=False)
    fecha_desde = forms.DateField(input_formats=['%d/%m/%y'], widget=DatePickerInput(), required=False)
    fecha_hasta = forms.DateField(input_formats=['%d/%m/%y'], widget=DatePickerInput(), required=False)
    bandeja = forms.CharField()
    modo = forms.CharField(max_length=2, required=False)
    items = forms.IntegerField(max_value=30,
                               min_value=5,
                               required=False,
                               label='ítems x pág.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        env_o_rec = (('rec', 'Recibidos'),
                     ('env', 'Enviados'))
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.disable_csrf = True
        self.fields['items'].label = '&nbsp'
        self.fields['items'].widget = SelectLiveSearchInput(choices=ITEMS_X_PAG)
        self.fields['bandeja'].widget = SelectLiveSearchInput(choices=env_o_rec)
        self.fields['modo'].widget.attrs['hidden'] = True
        self.fields['modo'].label = ""

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control-sm'

        self.helper.layout = Layout(
            Row(
                Column('texto', css_class='form-group col-md-4 mb-0 '),
                FieldWithButtons('items', boton_buscar(), css_class='form-group col-md-2 mb-0'),
            ),
            Row(
                Column('fecha_desde', css_class='form-group col-md-2 mb-0 '),
                Column('fecha_hasta', css_class='form-group col-md-2 mb-0 '),
                Column('bandeja', css_class='form-group col-md-2 mb-0 '),
            ),
            'modo',
        )
