from .models import Numerador
from django.db.models import Q
from tabla.filters import paginador
from tabla.forms import FiltroSimple
from perfiles.funcs import get_opcion_paginado


def numerador_filtrar(query_dict):
    buscar = query_dict.POST.get('buscar')
    items = get_opcion_paginado(query_dict)
    modo = query_dict.GET.get('modo')
    filtrado = Numerador.objects.all()

    if buscar != '' and buscar is not None:
        try:
            nvalue = int(buscar)
        except Exception as e:
            nvalue = 0

        filtrado = filtrado.filter(Q(comprobante__icontains=buscar) |
                                   Q(descripcion__icontains=buscar) |
                                   Q(ultimo_valor=nvalue))

    registros = filtrado.count()
    paginado = paginador(query_dict, filtrado)

    form = FiltroSimple(initial={'buscar': buscar,
                                 'items': items,
                                 'modo': modo})
    return {'filter': filtrado,
            'paginado': paginado,
            'registros': registros,
            'filtros_form': form}
