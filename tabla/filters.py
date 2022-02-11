from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Tabla, Variable, Plantilla
from .listas import ENTIDADES
from .forms import FiltroSimple, FiltroTablas
from .funcs import get_keys_by_value
from perfiles.funcs import get_opcion_paginado


def tabla_filtrar(query_dict):
    buscar = query_dict.GET.get('buscar')
    entidad = query_dict.GET.get('entidad')
    entidad_off = query_dict.GET.get('entidad_off')
    superior_entidad = query_dict.GET.get('superior_entidad')
    items = get_opcion_paginado(query_dict)
    modo = query_dict.GET.get('modo')
    filtrado = Tabla.objects.all()

    if entidad != '' and entidad is not None:
        filtrado = filtrado.filter(entidad=entidad)
    
    if superior_entidad != '' and superior_entidad is not None:
        filtrado = filtrado.filter(superior_codigo=superior_entidad.upper())

    if buscar != '' and buscar is not None:
        ENTIDADES_TUP = dict(ENTIDADES)
        lista_de_valores = get_keys_by_value(ENTIDADES_TUP, buscar)
        filtrado = filtrado.filter(Q(descripcion__icontains=buscar) |
                                   Q(codigo__icontains=buscar) |
                                   Q(superior_entidad__in=lista_de_valores) |
                                   Q(superior_codigo__icontains=buscar))

    registros = filtrado.count()
    paginado = paginador(query_dict, filtrado)

    form = FiltroTablas(initial={'buscar': buscar,
                                 'entidad': entidad,
                                 'superior_entidad': superior_entidad,
                                 'items': items,
                                 'entidad_off': entidad_off,
                                 'modo': modo})
    return {'filter': filtrado,
            'paginado': paginado,
            'registros': registros,
            'filtros_form': form}


def variable_filtrar(query_dict):
    buscar = query_dict.GET.get('buscar')
    items = get_opcion_paginado(query_dict)
    modo = query_dict.GET.get('modo')
    filtrado = Variable.objects.all()

    if buscar != '' and buscar is not None:
        filtrado = filtrado.filter(Q(variable__icontains=buscar) |
                                   Q(descripcion__icontains=buscar) |
                                   Q(tipo__icontains=buscar) |
                                   Q(fecha__icontains=buscar) |
                                   Q(caracter__icontains=buscar) |
                                   Q(numero__icontains=buscar) |
                                   Q(logico__icontains=buscar))

    registros = filtrado.count()
    paginado = paginador(query_dict, filtrado)

    form = FiltroSimple(initial={'buscar': buscar,
                                 'items': items,
                                 'modo': modo})
    return {'filter': filtrado,
            'paginado': paginado,
            'registros': registros,
            'filtros_form': form}


def plantilla_filtrar(query_dict):
    buscar = query_dict.GET.get('buscar')
    items = get_opcion_paginado(query_dict)
    modo = query_dict.GET.get('modo')
    filtrado = Plantilla.objects.all()

    if buscar != '' and buscar is not None:
        filtrado = filtrado.filter(Q(descripcion__icontains=buscar) |
                                   Q(plantilla__icontains=buscar) |
                                   Q(tipo_comprobante__descripcion__icontains=buscar)
                                   )

    registros = filtrado.count()
    paginado = paginador(query_dict, filtrado)

    form = FiltroSimple(initial={'buscar': buscar,
                                 'items': items,
                                 'modo': modo})
    return {'filter': filtrado,
            'paginado': paginado,
            'registros': registros,
            'filtros_form': form}


def paginador(query_dict, filtrado):
    page = query_dict.GET.get('page', 1)
    items = get_opcion_paginado(query_dict)
    paginator = Paginator(filtrado, items)
    try:
        paginado = paginator.page(page)
    except PageNotAnInteger:
        paginado = paginator.page(1)
    except EmptyPage:
        paginado = paginator.page(paginator.num_pages)
    return paginado