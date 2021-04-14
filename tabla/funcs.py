from datetime import datetime, date, time
from io import BytesIO
from urllib.parse import urlencode
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from xhtml2pdf import pisa
from tabla.listas import PREPOSICIONES
from crispy_forms.bootstrap import StrictButton


def email_valido(email):
    if es_valido(email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False
    else:
        return False


def list_to_dictionary(lst):
    res_dct = dict((x, y) for x, y in lst)
    return res_dct


# https://xhtml2pdf.readthedocs.io/en/latest/index.html
def render_to_pdf(request, template_src, context_dict={}):
    try:
        descargar = context_dict['descargar']
        nombre_de_archivo = context_dict['nombre_de_archivo']
    except Exception as e:
        descargar = False
        nombre_de_archivo = ''

    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    # ISO-8859-1
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result,
                            default_css=open(settings.BASE_DIR + '/static/css/reporte.css', 'r').read())
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')

        if descargar:
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(nombre_de_archivo)

        return response
    else:
        url = request.META.get('HTTP_REFERRER')
        messages.add_message(request, messages.ERROR, pdf.err)
        return redirect(url)


def es_plural(palabra):
    ultima = palabra[len(palabra) - 1]
    return ultima.lower() == 's'


def plural(singular):
    sufijo = ''
    plural = ''

    if singular in PREPOSICIONES:
        plural = singular

    ultima = singular[len(singular)-1]
    if ultima.lower() == 's':
        plural = singular
    else:
        if ultima.lower() in 'aeiouáéó':
            if ultima.lower() == 's':
                sufijo = 's'
            else:
                sufijo = 'S'
        else:
            if ultima.lower() == 's':
                sufijo = 'es'
            else:
                sufijo = 'ES'
    plural += singular.strip() + sufijo

    return plural


def boton_buscar(name='btn_buscar', caption='', onclick='', helpext=''):
    if helpext == '' or helpext is None:
        if caption == '' or caption is None:
            helpext = 'Buscar'
        else:
            helpext = caption

    caption_aux = '<span class="searchlink"></span>{}'.format(caption)

    if onclick == '':
        boton = StrictButton(caption_aux,
                             name=name,
                             type='submit',
                             title=helpext,
                             css_class='btn btn-outline-info btn-sm')
    else:
        boton = StrictButton(caption_aux,
                             name=name,
                             onclick=onclick,
                             title=helpext,
                             css_class='btn btn-outline-info btn-sm')

    return boton


def custom_redirect(url, parametros):
    try:
        url = reverse(url)
    except Exception as e:
        pass

    parametros = urlencode(parametros)
    url = '{}?{}'.format(url, parametros)
    return redirect(url)


def get_keys_by_value(dictOfElements, valueToFind):
    """"
    Obtiene una lista de claves de un diccionario que contiene el valor buscado
    """
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item in listOfItems:

        if valueToFind.upper() in item[1].upper():
            listOfKeys.append(item[0])
    return listOfKeys


def es_valido(valor):
    if valor is not None:
        if type(valor) is int:
            if valor != 0:
                return True
        else:
            if valor.strip() != '':
                return True
    return False


def normaliza_fechas(fecha_desde_ori, fecha_hasta_ori):
    if es_valido(fecha_desde_ori):
        desde = str_a_date(fecha_desde_ori)
    else:
        desde = datetime.strptime('01/01/2000 00:00:00', '%d/%m/%Y %H:%M:%S')

    if es_valido(fecha_hasta_ori):
        hasta = datetime.strptime(fecha_hasta_ori + ' 23:59:59', '%d/%m/%Y %H:%M:%S')
    else:
        hasta = datetime.strptime('31/12/' + str(date.today().year) + ' 23:59:59', '%d/%m/%Y %H:%M:%S')

    return desde, hasta


def str_a_date(fecha_str):
    if type(fecha_str) == str:
        fecha = fecha_str.split('/')
        fecha_actual = datetime.now()
        if len(fecha) < 3:
            anio = fecha_actual.year
        else:
            anio = fecha[2]
            if es_valido(anio):
                pass
            else:
                anio = str(fecha_actual.year)

        anio = int(anio)

        if len(fecha) < 2:
            mes = fecha_actual.month
        else:
            mes = fecha[1]
            if not es_valido(mes):
                mes = fecha_actual.month
            else:
                if int(mes) > 12:
                    mes = 12
                elif int(mes) < 1:
                    mes = 1
        mes = int(mes)

        dia = fecha[0]
        if not es_valido(dia):
            dia = fecha_actual.day
        dia = int(dia)

        if mes == 2:
            if dia > 29:
                dia = 29
            if dia > 28 and not es_anio_bisiesto(anio):
                dia = 28

        aux = '{}/{}/{} 00:00:00'.format(dia, mes, anio)
        fecha = datetime.strptime(aux, '%d/%m/%Y %H:%M:%S')
    else:
        fecha = fecha_str

    return fecha


def div_separador(titulo, colapsado=False):
    if colapsado:
        colapsado = "collapsible-active"
    else:
        colapsado = ""

    separador = '<button type="button" class="collapsible ' + colapsado + '"> ' + titulo + '</button>'

    return separador


def boton_limpiar_filtros(url='expedientes_listar'):
    boton = """ <div  class="col form-group col-md-2 mb-0 " > """
    boton += """ <div id="div_id_limpliar_filtros" class="form-group"> """
    boton += """ <label for="id_limpliar_filtros" class="">&nbsp;</label> """
    boton += """ <div class=""> """
    boton += """ <a href="{% url '""" + url + """' %}" id="id_limpliar_filtros" """
    boton += """ class="btn btn-outline-danger btn-sm" """
    boton += """title="Borrar todos los valores de los filtros"><span class="eraselink"></span></a> """
    boton += """ </div></div></div> """

    return boton


def es_anio_bisiesto(anio):
    if anio % 4 == 0:
        if anio % 100 == 0:
            if anio % 400 == 0:
                bisiesto = True
            else:
                bisiesto = False
        else:
            bisiesto = True
    else:
        bisiesto = False

    return bisiesto


div_colapsable_ini = """<div class="content-collapsible">"""
div_colapsed_ini = """<div class="content-collapsible" style="display: none;">"""
div_colapsable_fin = """<br></div>"""


def hora_actual():
    hr = datetime.now().strftime("%H")
    mins = datetime.now().strftime("%M")
    hr = int(hr)
    mins = int(mins)
    hora = time(hr, mins, 0)
    return hora


def fecha_actual():
    return datetime.now()


def hora_actual():
    hr = datetime.now().strftime("%H")
    mins = datetime.now().strftime("%M")
    hr = int(hr)
    mins = int(mins)
    hora = time(hr, mins, 0)
    return hora


def procesar_hora(post):
    hr = post['hr']
    mins = post['min']
    if hr == '' or hr is None:
        hr = datetime.now().strftime("%H")
    if mins == '' or mins is None:
        mins = datetime.now().strftime("%M")
    hr = int(hr)
    mins = int(mins)
    hora = time(hr, mins, 0)
    return hora


def minutos_entre_datetimes(dt1, dt2):
    if dt1 is None or dt2 is None:
        minutos = 0
    else:
        if dt1 > dt2:
            dt3 = dt1
            dt1 = dt2
            dt2 = dt3

        fmt = '%d-%m-%Y %H:%M:%S'
        str_dt1 = dt1.strftime(fmt)
        str_dt2 = dt2.strftime(fmt)
        td = datetime.strptime(str_dt2, fmt) - datetime.strptime(str_dt1, fmt)
        minutos = td.total_seconds() / 60
    return round(minutos, 2)