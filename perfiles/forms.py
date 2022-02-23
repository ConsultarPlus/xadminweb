from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.validators import validate_email
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, ButtonHolder, HTML
from crispy_forms.bootstrap import FieldWithButtons
from xadmin.settings import MEDIA_URL, STATIC_URL
from tabla.widgets import SelectLiveSearchInput
from tabla.funcs import div_separador, boton_buscar, div_colapsable_ini, div_colapsable_fin
from tabla.models import Tabla
from tabla.listas import ITEMS_X_PAG
from tabla.gets import get_choices_mas_vacio, get_group_choices, get_user_groups
from tabla.templatetags.custom_tags import traducir
from .models import Perfil, Preferencia


PANTALLAS = (('documentos_listar', traducir('Documentos')),
             ('/admin', traducir('Admin')),
             ('tablas_listar', traducir('Tablas')),
             ('variables_listar', traducir('Variables')),
             ('plantillas_listar', traducir('Plantillas')),
             ('numeradores_listar', traducir('Numeradores')),
             ('usuario_modificar', traducir('Perfil')),
             ('', traducir('Ninguna')),
             )


class PerfilPantallaForm(forms.ModelForm):
    VISTA_DUMMY_CHOICES = (('menu', 'Menú'),)
    OPCION_DUMMY_CHOICES = (('pantalla_inicial', 'Pantalla inicial'),)

    vista_dummy = forms.ChoiceField(choices=VISTA_DUMMY_CHOICES, required=False, label='Pantalla')
    opcion_dummy = forms.ChoiceField(choices=OPCION_DUMMY_CHOICES, required=False, label='Opción')
    caracter = forms.ChoiceField(choices=sorted(PANTALLAS), required=False, label='Valor')
    vista = forms.CharField(max_length=60, initial='menu', label='')
    # opcion = forms.CharField(max_length=60, initial='pantalla_inicial', label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vista_dummy'].widget.attrs['disabled'] = True
        self.fields['opcion_dummy'].widget.attrs['disabled'] = True
        self.fields['vista'].widget.attrs['hidden'] = True
        self.fields['opcion'].widget.attrs['hidden'] = True


class UsuarioForm(forms.ModelForm):
    nick = forms.CharField(max_length=40, required=False, disabled=True, label='Usuario')
    nombre = forms.CharField(max_length=40, required=False)
    apellido = forms.CharField(max_length=40, required=False)
    telefono = forms.CharField(max_length=40, label='Teléfono', required=False)
    email = forms.CharField(max_length=50, required=False, validators=[validate_email],
                            label='E-mail (para recuperar contraseña)')
    grupo = forms.MultipleChoiceField(required=False, label='Grupos')

    class Meta:
        model = Perfil
        fields = 'user', 'foto', 'telefono', 'nivel', 'email_contacto'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nick'].widget.attrs['disabled'] = True
        self.fields['nivel'].widget.attrs['disabled'] = True
        self.fields['grupo'].widget.attrs['disabled'] = True

        for field_name, field in self.fields.items():
            field.label = traducir(field.label, 'USUARIO')
            if field_name != 'foto':
                field.widget.attrs['class'] = 'form-control-sm'

        link = ""
        if self.instance.pk:
            user_id = self.instance.user_id
            foto = self.instance.foto
            telefono = self.instance.telefono
            usuario = User.objects.get(id=user_id)
            niveles_user = Perfil.objects.filter(id=self.instance.pk).values('nivel')
            niveles = Tabla.objects.filter(entidad='NIVEL', id__in=niveles_user)

            self.fields['grupo'].choices = get_user_groups(usuario)
            self.fields['nick'].initial = usuario.username
            self.fields['nombre'].initial = usuario.first_name
            self.fields['apellido'].initial = usuario.last_name
            self.fields['telefono'].initial = telefono
            self.fields['email'].initial = usuario.email
            if foto:
                img = MEDIA_URL+str(foto)
            else:
                img = STATIC_URL + "img/usuario_incognito.png"
            link = """ <div  class="col form-group col-md-10 mb-0 " > """
            link += """ <div id="div_foto_preview" class="form-group"> """
            link += """ <div class=""><a>"""
            link += """ <img class ="preview foto-id" src=" """ + img + """"></a>"""
            link += """ </div></div></div> """

        separador = div_separador('Preferencias operativas')

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nick', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('nombre', css_class='form-group col-md-3 mb-0'),
                Column('apellido', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('telefono', css_class='form-group col-md-3 mb-0'),
                Column('email', css_class='form-group col-md-3 mb-0'),
                Column('email_contacto', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('foto', css_class='form-group col-md-6 mb-0'),
                Column(HTML(link), css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            HTML(separador),
            HTML(div_colapsable_ini),
            Row(
                # Column('nivel', css_class='form-group col-md-3 mb-0'),
                Column('grupo', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            HTML(div_colapsable_fin),
            ButtonHolder(
                Submit('submit', 'Grabar'),
                Button('cancel', 'Volver', css_class='btn-default', onclick="window.history.back()")
            )
        )


class FiltroUsuario(forms.Form):
    buscar = forms.CharField(max_length=60, required=False)
    grupo = forms.IntegerField(required=False)
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
        self.fields['grupo'].widget = SelectLiveSearchInput(choices=get_group_choices())
        self.fields['modo'].widget.attrs['hidden'] = True
        self.fields['modo'].label = ""

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control-sm'

        self.helper.layout = Layout(
            Row(
                Column('buscar', css_class='form-group col-md-4 mb-0 '),
                FieldWithButtons('items', boton_buscar(), css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('grupo', css_class='form-group col-md-5 mb-0 '),
                css_class='form-row'
            ),
            'modo',
        )


class CopiarPreferenciasForm(forms.Form):
    usuarios_origen = User.objects.all().order_by('username').values('id', 'username')
    usuarios_origen = [(q['id'], q['username']) for q in usuarios_origen]
    usuarios_origen.insert(0, ('', '-----'))

    reemplazar_o_agregar = (
        ('R', 'Reemplazar las preferencias que tengan los usuarios'),
        ('A', 'Agregar las preferencias que falten y modificar las existentes en los usuarios'),
    )
    usuario_origen = forms.ChoiceField(choices=usuarios_origen, label='usuario origen de las preferencias')
    reemplazar = forms.ChoiceField(choices=reemplazar_o_agregar, initial='R', label='Reemplazar o agregar y modificar')
    usuarios_destino = forms.ModelMultipleChoiceField(queryset=User.objects.all().order_by('username'),
                                                      label="Usuarios destino",
                                                      widget=FilteredSelectMultiple("usuarios", is_stacked=False),
                                                      required=True)

    class Media:
        css = {
            'all': ('/static/admin/css/widgets.css',),
        }
        js = ('/admin/jsi18n',)

    def clean_usuario_destinoe(self):
        usuarios_destino = self.cleaned_data['usuarios_destino']
        return usuarios_destino

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control-sm'

        self.helper.layout = Layout(
            Row(
                Column('usuario_origen', css_class='form-group col-md-4 mb-0 '),
                Column('reemplazar', css_class='form-group col-md-1 mb-0 '),
                Column('usuarios_destino', css_class='form-group col-md-5 mb-0 '),
                css_class='form-row'
            ),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            ButtonHolder(
                Submit('submit', 'Copiar preferencias'),
                Button('cancel', 'Volver', css_class='btn-default', onclick="window.history.back()")
            )
        )


class CopiarPermisosGrupoForm(forms.Form):
    grupos_origen = Group.objects.all().order_by('name').values('id', 'name')
    grupos_origen = [(q['id'], q['name']) for q in grupos_origen]
    grupos_origen.insert(0, ('', '-----'))

    reemplazar_o_agregar = (
                            ('R', 'Reemplazar los permisos que tengan los grupos'),
                            ('A', 'Agregar los permisos que falten a los permisos ya existentes en los grupos'),
                            )
    grupo_origen = forms.ChoiceField(choices=grupos_origen, label='Grupo origen de los permisos')
    reemplazar = forms.ChoiceField(choices=reemplazar_o_agregar, initial='R', label='Reemplazar o agregar')
    grupos_destino = forms.ModelMultipleChoiceField(queryset=Group.objects.all().order_by('name'),
                                                    label="Grupos destino",
                                                    widget=FilteredSelectMultiple("Grupos", is_stacked=False),
                                                    required=True)

    class Media:
        css = {
            'all': ('/static/admin/css/widgets.css',),
        }
        js = ('/admin/jsi18n',)

    def clean_grupo_destinoe(self):
        grupos_destino = self.cleaned_data['grupos_destino']
        return grupos_destino

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control-sm'

        self.helper.layout = Layout(
            Row(
                Column('grupo_origen', css_class='form-group col-md-4 mb-0 '),
                Column('reemplazar', css_class='form-group col-md-1 mb-0 '),
                Column('grupos_destino', css_class='form-group col-md-5 mb-0 '),
                css_class='form-row'
            ),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            HTML('<br>'),
            ButtonHolder(
                Submit('submit', 'Copiar permisos'),
                Button('cancel', 'Volver', css_class='btn-default', onclick="window.history.back()")
            )
        )
