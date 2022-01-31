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
import os
import qrcode
import base64
from PIL import Image

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

def get_lett(num):
    nume = str(num)
    largo = len(nume)
    finnum = ' '
    if largo == 1:
        finnum = unidad(nume)
    if largo == 2:
        finnum = dece(nume)
    if largo == 3:
        finnum = cente(nume)
    if largo == 4:
        finnum = mil(nume)
    if largo == 5:
        finnum = decmil(nume)
    if largo == 6:
        finnum = centmil(nume)
    if largo == 7:
        finnum = mill(nume)
    if largo == 8:
        finnum = dece(nume[:-6]) + " MILLONES " + centmil(nume[2:])
    if largo == 9:
        finnum = cente(nume[:-6]) + " MILLONES " + centmil(nume[3:])
    if largo == 10:
        finnum = mil(nume[:-6]) + " MILLONES " + centmil(nume[4:])
    if largo == 11:
        finnum = decmil(nume[:-6]) + " MILLONES " + centmil(nume[5:])
    if largo == 12:
        finnum = centmil(nume[:-6]) + " MILLONES " + centmil(nume[6:])
    return finnum

def mill (x):
    if x[0] == "1":
        a = "UN MILLON " + centmil(x[1:])
    else:
        a = unidad(x[0]) + " MILLONES " + centmil(x[1:])
    return a

def centmil (x):
    if x[0] == "0" and x[1] == "0" and x[2] == "0":
        a = cente(x[3:])
    else:
        a = cente(x[0]+x[1]+x[2]) + " MIL " + cente(x[3:])
    return a

def decmil (x):
    if x[0] == "0" and x[1] == "0":
        cente(x[2:])
    else:
        a = dece(x[0] + x[1]) + " MIL " + cente(x[2:])
    return a

def mil (x):
    if x[0] == "1":
        a = " MIL " + cente(x[1:])
    else:
        if x[0] == "0":
            a = cente(x[1:])
        else:
            a = unidad(x[0]) + " MIL " + cente(x[1:])
    return a

def cente (x):
    if x[0] == "0":
        a = dece(x[1:])
    if x[0] == "1":
        if x[1:] == "00":
            a = "CIEN"
        else:
            a = "CIENTO " + dece(x[1:])
    if x[0] == "2":
        if x[1:] == "00":
            a = "DOSCIENTOS"
        else:
            a = "DOSCIENTOS " + dece(x[1:])
    if x[0] == "3":
        if x[1:] == "00":
            a = "TRESCIENTOS"
        else:
            a = "TRESCIENTOS " + dece(x[1:])
    if x[0] == "4":
        if x[1:] == "00":
            a = "CUATROCIENTOS"
        else:
            a = "CUATROCIENTOS " + dece(x[1:])
    if x[0] == "5":
        if x[1:] == "00":
            a = "QUINIENTOS"
        else:
            a = "QUINIENTOS " + dece(x[1:])
    if x[0] == "6":
        if x[1:] == "00":
            a = "SEISCIENTOS"
        else:
            a = "SEISCIENTOS " + dece(x[1:])
    if x[0] == "7":
        if x[1:] == "00":
            a = "SETECIENTOS"
        else:
            a = "SETECIENTOS " + dece(x[1:])
    if x[0] == "8":
        if x[1:] == "00":
            a = "OCHOCIENTOS"
        else:
            a = "OCHOCIENTOS " + dece(x[1:])
    if x[0] == "9":
        if x[1:] == "00":
            a = "NOVECIENTOS"
        else:
            a = "NOVECIENTOS " + dece(x[1:])
    return a

def dece (x):
    v = int(x)
    if x[0] == "0":
        a = unidad(x[1])
    if x[0] == "1":
        if v < 16:
            if x == "10":
                a = "DIEZ"
            if x == "11":
                a = "ONCE"
            if x == "12":
                a = "DOCE"
            if x == "13":
                a = "TRECE"
            if x == "14":
                a = "CATORCE"
            if x == "15":
                a = "QUINCE"
        else:
            a = "DIECI" + unidad(x[1])
    if x[0] == "2":
        if x[1] == "0":
            a = "VEINTE"
        else:
            a = "VEINTI" + unidad(x[1])
    if x[0] == "3":
        if x[1] == "0":
            a = "TREINTA"
        else:
            a = "TERINTAI" + unidad(x[1])
    if x[0] == "4":
        if x[1] == "0":
            a = "CUARENTA"
        else:
            a = "CUARENTAI" + unidad(x[1])
    if x[0] == "5":
        if x[1] == "0":
            a = "CINCUENTA"
        else:
            a = "CINCUENTAI" + unidad(x[1])
    if x[0] == "6":
        if x[1] == "0":
            a = "SESENTA"
        else:
            a = "SESENTAI" + unidad(x[1])
    if x[0] == "7":
        if x[1] == "0":
            a = "SETENTA"
        else:
            a = "SETENTAI" + unidad(x[1])
    if x[0] == "8":
        if x[1] == "0":
            a = "OCHENTA"
        else:
            a = "OCHENTAI" + unidad(x[1])
    if x[0] == "9":
        if x[1] == "0":
            a = "NOVENTA"
        else:
            a = "NOVENTAI" + unidad(x[1])
    return a

def unidad(x):
    if x == "1":
        a = "UN"
    if x == "2":
        a = "DOS"
    if x == "3":
        a = "TRES"
    if x == "4":
        a = "CUATRO"
    if x == "5":
        a = "CINCO"
    if x == "6":
        a = "SEIS"
    if x == "7":
        a = "SIETE"
    if x == "8":
        a = "OCHO"
    if x == "9":
        a = "NUEVE"
    if x == "0":
        a = ""
    return a

def generar_qr(archivo_input, archivo_output, encriptar='N', box_size='5', prefijo_no_enriptado=''):
    try:
        print(archivo_input)
        if os.path.exists(archivo_input):
            archivo_nombre, archivo_extension = os.path.splitext(archivo_input)
            archivo_dir = os.path.dirname(archivo_input)
            texto = open(archivo_input, 'r').read()



            if archivo_output == '' or archivo_output is None:
                output_dir = archivo_dir
            else:
                output_dir = os.path.dirname(archivo_output)
                if not os.path.isdir(output_dir):
                    os.mkdir(output_dir)
                else:
                    if os.path.exists(archivo_output):
                        os.remove(archivo_output)

            output_nombre, output_extension = os.path.splitext(archivo_output)
            if output_nombre == ''  or output_nombre is None:
                output_nombre = archivo_nombre

            output = '{}.png'.format(output_nombre)

            if encriptar == 'S':
                texto = codificar_en_base64(texto)

            if prefijo_no_enriptado != '' and prefijo_no_enriptado is not None:
                texto = prefijo_no_enriptado + texto

            if box_size == '' or box_size is None:
                box_size = 5
            else:
                box_size = int(box_size)

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=box_size,
                border=4,
            )

            qr.add_data(texto)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img.save(output)
            if not png_a_jpg(output):
                msj = 'Generar QR: No se pudo generar el jpg'
                print(msj)
        else:
            msj = 'Generar QR: No se encuentra el archivo {}'.format(archivo_input)
            print(msj)
    except Exception as msj:
        msj = 'Generar QR: {}'.format(msj)
        print(msj)

def codificar_en_base64(texto):
    message_bytes = texto.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode('ascii')

def png_a_jpg(png):
    try:
        im = Image.open(png)
        rgb_im = im.convert('RGB')
        png_nombre, png_extension = os.path.splitext(png)
        jpg = '{}.jpg'.format(png_nombre)
        if os.path.exists(jpg):
            os.remove(jpg)
        rgb_im.save(jpg)
        return True
    except Exception as e:
        return False