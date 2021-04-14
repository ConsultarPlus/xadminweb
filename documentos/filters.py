from .models import Documento
from django.db.models import Q
from tabla.filters import paginador
from tabla.forms import FiltroSimple
from perfiles.funcs import get_opcion_paginado


def documento_filtrar(query_dict):
    buscar = query_dict.GET.get('buscar')
    items = get_opcion_paginado(query_dict)
    modo = query_dict.GET.get('modo')
    filtrado = Documento.objects.all()

    if buscar != '' and buscar is not None:
        filtrado = filtrado.filter(Q(entidad__icontains=buscar) |
                                   Q(entidad_id__icontains=buscar) |
                                   Q(descripcion__icontains=buscar) |
                                   Q(archivo__icontains=buscar))

    registros = filtrado.count()
    paginado = paginador(query_dict, filtrado)

    form = FiltroSimple(initial={'buscar': buscar,
                                 'items': items,
                                 'modo': modo})
    return {'filter': filtrado,
            'paginado': paginado,
            'registros': registros,
            'filtros_form': form}
