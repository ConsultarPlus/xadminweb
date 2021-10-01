from .models import Cliente, Cuentas
from django.db.models import Q
from tabla.filters import paginador
from tabla.forms import FiltroSimple
from perfiles.funcs import get_opcion_paginado


def clientes_filtrar(query_dict):
    buscar = query_dict.GET.get('buscar')
    items = get_opcion_paginado(query_dict)
    modo = query_dict.GET.get('modo')
    filtrado = Cliente.objects.all()

    if buscar != '' and buscar is not None:
        filtrado = filtrado.filter(Q(clicod__icontains=buscar) |
                                   Q(nombre__icontains=buscar)
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


def cuentas_filtrar(query_dict):
    buscar = query_dict.GET.get('buscar')
    cliente_id = query_dict.GET.get('id')
    items = get_opcion_paginado(query_dict)
    modo = query_dict.GET.get('modo')
    filtrado = Cuentas.objects.all()

    if cliente_id != '' and cliente_id is not None:
        filtrado = filtrado.filter(cliente=cliente_id)

    if buscar != '' and buscar is not None:
        filtrado = filtrado.filter(concepto__icontains=buscar)

    registros = filtrado.count()
    paginado = paginador(query_dict, filtrado)

    form = FiltroSimple(initial={'buscar': buscar,
                                 'items': items,
                                 'modo': modo})
    return {'filter': filtrado,
            'paginado': paginado,
            'registros': registros,
            'filtros_form': form}
