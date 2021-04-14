import datetime
from django.db.models import Q
from perfiles.funcs import get_preferencia, set_preferencia, get_opcion_paginado
from tabla.filters import paginador
from tabla.funcs import es_valido, normaliza_fechas
from .forms import FiltroMensajes
from .models import Mensaje, Destinatario


def mensaje_filtrar(query_dict):
    texto = query_dict.GET.get('texto')
    usuario = query_dict.user.id
    items = get_opcion_paginado(query_dict)
    modo = query_dict.GET.get('modo')

    if query_dict.GET:
        fecha_desde = query_dict.GET.get('fecha_desde')
        fecha_hasta = query_dict.GET.get('fecha_hasta')
        bandeja = get_bandeja(query_dict)
    else:
        bandeja = 'rec'
        desde = datetime.datetime.today()
        desde = desde - datetime.timedelta(15)
        fecha_desde = desde.strftime('%d/%m/%Y')
        fecha_hasta = datetime.datetime.today().strftime('%d/%m/%Y')

    if bandeja == 'env':
        filtrado = Mensaje.objects.filter(remitente=usuario).prefetch_related('destinatarios')
    else:
        bandeja = 'rec'
        filtrado = Destinatario.objects.filter(usuario=usuario).select_related()
        filtrado = filtrado.filter(Q(mensaje__hora__lte=datetime.datetime.now().time()) |
                                   Q(mensaje__fecha__lt=datetime.datetime.now()))

    if es_valido(texto):
        if bandeja == 'rec':
            filtrado = filtrado.filter(Q(mensaje__mensaje__icontains=texto))
        else:
            filtrado = filtrado.filter(Q(mensaje__icontains=texto))

    if es_valido(fecha_desde) or es_valido(fecha_hasta):
        fecha_desde_str, fecha_hasta_str = normaliza_fechas(fecha_desde, fecha_hasta)
        fecha_desde = fecha_desde_str
        fecha_hasta = fecha_hasta_str
        if bandeja == 'rec':
            filtrado = filtrado.filter(Q(mensaje__fecha__range=(fecha_desde_str, fecha_hasta_str)))
        else:
            filtrado = filtrado.filter(Q(fecha__range=(fecha_desde_str, fecha_hasta_str)))

    if bandeja == 'rec':
        filtrado = filtrado.order_by('mensaje__fecha')
    else:
        filtrado = filtrado.order_by('fecha')

    filtrado = filtrado.order_by('-id')
    registros = filtrado.count()
    paginado = paginador(query_dict, filtrado)

    form = FiltroMensajes(initial={'texto': texto,
                                   'items': items,
                                   'modo': modo,
                                   'bandeja': bandeja,
                                   'fecha_desde': fecha_desde,
                                   'fecha_hasta': fecha_hasta})
    return {'filter': filtrado,
            'paginado': paginado,
            'registros': registros,
            'bandeja': bandeja,
            'filtros_form': form}


def get_bandeja(query_dict):
    usuario = query_dict.user
    default = get_preferencia(usuario, 'filtro', 'bandeja', 'C', 'rec')
    bandeja = query_dict.GET.get('bandeja', default)
    if not bandeja:
        bandeja = 'rec'
    if default != bandeja:
        preferencia = {'usuario': usuario,
                       'vista': 'filtro',
                       'opcion': 'bandeja',
                       'caracter': bandeja}
        res = set_preferencia(preferencia)

    return bandeja
