from .models import Cliente, Cuentas
from django.db.models import Q
from tabla.filters import paginador
from tabla.forms import FiltroSimple
from perfiles.funcs import get_opcion_paginado


def clientes_filtrar(query_dict, encriptado=None):
    buscar = query_dict.GET.get('buscar')
    # buscarenc = query_dict.GET.get('encriptado')
    buscarenc = encriptado
    items = get_opcion_paginado(query_dict)
    modo = query_dict.GET.get('modo')
    filtrado = Cliente.objects.all()

    if buscar != '' and buscar is not None:
        filtrado = filtrado.filter(Q(clicod__icontains=buscar) |
                                   Q(nombre__icontains=buscar)
                                   )

    if buscarenc != '' and buscarenc is not None:
        filtrado = filtrado.filter(encriptado=buscarenc)

    registros = filtrado.count()
    paginado = paginador(query_dict, filtrado)

    form = FiltroSimple(initial={'buscar': buscar,
                                 'items': items,
                                 'modo': modo})
    return {'filter': filtrado,
            'paginado': paginado,
            'registros': registros,
            'filtros_form': form}


def cuentas_filtrar(query_dict, encriptado, facturas_pendientes):
    buscar = query_dict.GET.get('buscar')
    items = get_opcion_paginado(query_dict)
    modo = query_dict.GET.get('modo')
    filtrado = Cuentas.objects.all()

    if encriptado != '' and encriptado is not None:
        filtrado = filtrado.filter(cliente__encriptado=encriptado)

    if facturas_pendientes:
        filtrado = filtrado.filter(pendiente=True)

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
