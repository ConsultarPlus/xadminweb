import os
from datetime import datetime
from django.template.defaulttags import register
from django.urls import resolve
from tabla.listas import PRIORIDAD, AMBITO, PREPOSICIONES, ADMISIBLES
from tabla.models import MODELOS, Traduccion, Plantilla
from tabla.listas import UNIDADES, MONEDA


@register.filter
def get_item(dictionary, key):
    item = dictionary.get(key)
    return item


@register.filter
def imagen_si_no(si_no):
    """ Esta etiqueta se puede usar al mostrar campos booleanos o S/N
        con un ícono
        En la plantilla HTML, los bloques que use esta función
        deben estar entre {% autoescape off %} y {% endautoescape %}
    """
    if si_no == 'S' or si_no is True:
        imagen = '<img src="/static/img/icon-yes.svg" alt="True">'
    else:
        imagen = '<img src="/static/img/icon-no.svg" alt="False">'

    return imagen


@register.filter
def texto_si_no(si_no):
    """ Esta etiqueta se puede usar al mostrar campos booleanos o S/N
        con un texto "Sí" o "No"
        En la plantilla HTML, los bloques que use esta función
        deben estar entre {% autoescape off %} y {% endautoescape %}
    """
    if si_no == 'S' or si_no is True:
        texto = 'Sí'
    else:
        texto = 'No'

    return texto


@register.filter
def ambito_descripcion(key):
    AMBITO_TUP = dict(AMBITO)
    return get_item(AMBITO_TUP, key)


@register.filter
def admisible_descripcion(key):
    ADMISIBLE_TUP = dict(ADMISIBLES)
    return get_item(ADMISIBLE_TUP, key)


@register.filter
def prioridad_descripcion(key):
    if key == '' or key is None:
        return '--'
    else:
        PRIORIDAD_TUP = dict(PRIORIDAD)
        return get_item(PRIORIDAD_TUP, key)


@register.filter
def moneda_descripcion(key):
    if key == '' or key is None:
        return '--'
    else:
        PRIORIDAD_TUP = dict(MONEDA)
        return get_item(PRIORIDAD_TUP, key)


@register.filter
def unidad_descripcion(key):
    if key == '' or key is None:
        return '--'
    else:
        PRIORIDAD_TUP = dict(UNIDADES)
        return get_item(PRIORIDAD_TUP, key)



@register.filter
def prioridad_color(prioridad):
    """ Esta etiqueta se puede usar al mostrar campos de prioridad (Alta/Media/Baja)
        con un fondo semaforizado (Verde/Amarillo/Rojo)
        En la plantilla HTML, se llamaría así
        <td bgcolor="{{ item.prioridad|prioridad_color }}" >{{ item.prioridad|prioridad_descripcion }} </td>
    """

    if prioridad == "A":
        bgcolor, fcolor = color_rojo()
    elif prioridad == "M":
        bgcolor, fcolor = color_amarillo()
    else:
        bgcolor, fcolor = color_verde()

    color = 'bgcolor="{}"><font color="{}"'.format(bgcolor, fcolor)
    return color


@register.filter
def prioridad_color_style(prioridad):
    """ Esta etiqueta se puede usar al mostrar campos de prioridad (Alta/Media/Baja)
        con un fondo semaforizado (Verde/Amarillo/Rojo)
        En la plantilla HTML, se llamaría así
        style="{{ item.prioridad|prioridad_color }}"
    """

    if prioridad == "A":
        bgcolor, fcolor = color_rojo()
    elif prioridad == "M":
        bgcolor, fcolor = color_amarillo()
    else:
        bgcolor, fcolor = color_verde()

    color = 'background-color:{};color:{};'.format(bgcolor, fcolor)
    return color


@register.filter
def limpiar_none(valor):
    if valor is None:
        devolver = '--'
    else:
        devolver = valor
    return devolver


@register.filter
def observacion_pop(obs):
    if obs != "" and obs is not None:
        obs_aux = obs.replace('"', '')
        obs_aux = obs_aux.replace("'", '')
        obs_aux = obs_aux.replace(chr(13), '')
        obs_aux = obs_aux.replace(chr(10), '')
        observacion = obs_aux
        if obs_aux != '' and obs_aux is not None:
            if len(obs_aux) > 40:
                observacion = '<a href="#" '
                observacion += """onclick='todo_es_pop("", "{}", "")' >"""
                observacion += '{}</a>'
                observacion = observacion.format(obs_aux, obs_aux[:37] + '...')
    else:
        observacion = ""

    return observacion


@register.filter
def vista_desde_url(url):
    rm = resolve(url)
    view = rm.url_name
    return view


@register.filter
def donde_estoy(url):
    view = vista_desde_url(url)
    view = humanizar_texto(view)
    modelo = 'GENERAL'
    for modelo_aux in MODELOS:
        if modelo_aux[0].lower() in view.lower():
            modelo = modelo_aux[0]
            break
    donde = traducir(view.capitalize(), modelo)
    donde = donde.replace(' ', ' | ')
    donde = donde.replace('Tipoinsumido ', 'Tipos de insumido ')
    return donde


@register.filter
def humanizar_texto(texto):
    texto = texto.replace('_', ' ')
    texto = texto.capitalize()
    return texto


@register.filter
def trim(cadena):
    return cadena.strip()


@register.filter
def atraso(d1):
    if isinstance(d1, datetime):
        d2 = datetime.today()
        return abs((d2 - d1).days)
    else:
        return 0


@register.filter
def segundos_timpedelta(td):
    return int(td.total_seconds())


@register.filter
def tiene_vista_previa(archivo):
    if archivo != '' and archivo is not None:
        nombre, extension = os.path.splitext(archivo)
        if extension.lower() in {'.jpg', '.jpeg', '.tiff', '.png', '.bmp', '.gif'}:
            return True
    return False


@register.filter
def solo_nombre_de_archivo(archivo):
    if archivo is not None:
        return os.path.basename(archivo)
    else:
        return ''


@register.simple_tag()
def traducir(palabras, modelo="GENERAL"):
    p = False
    if p:
        print('***************************palabras: ', palabras)

    if palabras != '' and palabras is not None:
        vpalabras = palabras.split(' ')
        traduccion_final = ''
        for palabra_aux in vpalabras:
            palabra = palabra_aux
            if p:
                print('****palabra: ', palabra)
                print('****type(palabra): ', type(palabra))

            if palabra not in PREPOSICIONES:
                modelo_aux = modelo
                i = 1
                while i <= 2:
                    try:
                        traduccion = Traduccion.objects.get(modelo=modelo_aux.upper(), palabra=palabra.upper())
                        if palabra == traduccion.traduccion.lower():
                            reemplazo = traduccion.traduccion.lower()
                        elif palabra == traduccion.traduccion.capitalize():
                            reemplazo = traduccion.traduccion.capitalize()
                        elif palabra == traduccion.traduccion.upper():
                            reemplazo = traduccion.traduccion.upper()
                        else:
                            reemplazo = traduccion.traduccion

                        if len(traduccion_final) == 0:
                            traduccion_final = reemplazo
                        else:
                            traduccion_final += ' ' + reemplazo
                        if p:
                            print('***traduccion: ', traduccion)
                            print('***1 traduccion_final: ', traduccion_final)
                            print('***i: ', i)
                        break

                    except Exception as e:
                        if p:
                            print('***modelo_aux: ', modelo_aux)
                        if modelo_aux != "GENERAL" and i == 1:
                            modelo_aux = "GENERAL"
                        else:
                            if len(traduccion_final) == 0:
                                traduccion_final = palabra
                            else:
                                traduccion_final += ' ' + palabra
                            break
                        if p:
                            print('***2 traduccion_final: ', traduccion_final)
                            print('***i: ', i)
                    i += 1

            else:
                if len(traduccion_final) == 0:
                    traduccion_final = palabra
                else:
                    traduccion_final += ' ' + palabra
                if p:
                    print('***3 traduccion_final: ', traduccion_final)

    else:
        traduccion_final = palabras

    return traduccion_final


@register.filter
def uncarajo(averga):
    print('****uncarajo: ', averga)
    return ''


@register.simple_tag
def define(val=None):
    return val



@register.filter
def vencimiento_color(vencimiento):
    """
        <td bgcolor="{{ item.vencimiento|vencimiento_color }}" >{{ item.vencimiento }} </td>
    """
    d1 = datetime.today().date()
    dias_para_vencer = abs((vencimiento - d1).days)
    if vencimiento < d1: # vencido, en rojo
        bgcolor = "#ff8080"
        fcolor = "#330000"
    else:
        if dias_para_vencer <= 7:
            bgcolor, fcolor = color_rojo()
        elif 7 < dias_para_vencer <= 14:
            bgcolor, fcolor = color_amarillo()
        else:
            bgcolor, fcolor = color_verde()

    color = 'bgcolor="{}"><font color="{}"'.format(bgcolor, fcolor)
    return color


def color_rojo():
    bgcolor = "#ff8080"
    fcolor = "#330000"
    return bgcolor, fcolor


def color_amarillo():
    bgcolor = "#ffff66"
    fcolor = "#333300"
    return bgcolor, fcolor


def color_verde():
    bgcolor = "#8cd98c"
    fcolor = "#0d260d"
    return bgcolor, fcolor


@register.filter
def lista_a_str(lista):
    return ','.join(lista)


@register.filter
def link_de_ayuda(vista):
    manual = 'instructores'
    try:
        pagina = 1
        if vista.find('expediente_') > 0 or vista.find('expedientes_') > 0:
            pagina = 6
        elif vista.find('insumido_') > 0 or vista.find('insumidos_') > 0:
            pagina = 15
        elif vista.find('comprobante_') > 0:
            pagina = 14
        elif vista.find('circuito_') > 0 or vista.find('circuitos_') > 0:
            manual = 'configuracion'
            pagina = 21
        elif vista.find('clasificador_') > 0 or vista.find('clasificadores_') > 0:
            manual = 'configuracion'
            pagina = 22
        elif vista.find('documento_') > 0 or vista.find('documentos_') > 0:
            manual = 'configuracion'
            pagina = 23
        elif vista.find('documento_') > 0 or vista.find('documentos_') > 0:
            manual = 'configuracion'
            pagina = 23
        elif vista.find('institucion_') > 0 or vista.find('instituciones_') > 0:
            manual = 'configuracion'
            pagina = 23
        elif vista.find('persona_') > 0 or vista.find('personas_') > 0:
            manual = 'configuracion'
            pagina = 24
        elif vista.find('plantilla_') > 0 or vista.find('plantillas_') > 0:
            manual = 'configuracion'
            pagina = 26
        elif vista.find('mensaje') > 0:
            pagina = 20
        elif vista.find('requerimiento_') > 0 or vista.find('requerimientos_') > 0:
            manual = 'configuracion'
            pagina = 29
        elif vista.find('responsable_') > 0 or vista.find('responsables_') > 0:
            manual = 'configuracion'
            pagina = 30
        elif vista.find('admin') > 0:
            manual = 'configuracion'
            if vista.find('traduccion') > 0:
                pagina = 13
            elif vista.find('session') > 0:
                pagina = 13
            elif vista.find('axes') > 0:
                pagina = 11
            elif vista.find('auth') > 0:
                pagina = 8
            else:
                pagina = 7
        elif vista.find('numerador_') > 0 or vista.find('numeradores_') > 0:
            manual = 'configuracion'
            pagina = 14
        elif vista.find('tabla_') > 0 or vista.find('tablas_') > 0:
            manual = 'configuracion'
            pagina = 15
        elif vista.find('tipoinsumido_') > 0:
            manual = 'configuracion'
            pagina = 19
        elif vista.find('variable') > 0:
            manual = 'configuracion'
            pagina = 21
        elif vista.find('turno') > 0:
            manual = 'turnos'
            pagina = 3

        link = '/static/pdf/manual_defensoria_{}.pdf#page={}'.format(manual, pagina)
    except Exception as e:
        link = '/static/pdf/manual_defensoria.{}.pdf'.format(manual)
    return link


@register.filter
def encode_utf8(texto_original):
    texto = texto_original.encode(encoding="utf-8", errors="ignore")
    texto = texto.decode()
    return texto


@register.filter(is_safe=False)
def incluir_plantilla(plantilla_id):
    if plantilla_id != '' and plantilla_id is not None:
        plantilla_id = int(plantilla_id)
        try:
            plantilla = Plantilla.objects.get(id=plantilla_id)
            plantilla_html = plantilla.plantilla
        except Exception as e:
            plantilla_html = 'No se encuentra la plantilla {}'.format(plantilla_id)
    else:
        plantilla_html = 'No se indicó el ID de la plantilla a incluir'

    return plantilla_html
