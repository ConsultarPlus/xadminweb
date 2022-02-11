from django.db.models import Q
from django.contrib.auth.models import User
from tabla.filters import paginador
from .forms import FiltroUsuario
from .funcs import get_opcion_paginado


def usuario_filtrar(query_dict):
    buscar = query_dict.GET.get('buscar')
    grupo = query_dict.GET.get('grupo')
    items = get_opcion_paginado(query_dict)
    modo = query_dict.GET.get('modo')
    filtrado = User.objects.select_related('perfil').filter(is_active=True).order_by('username')
    if buscar != '' and buscar is not None:
        filtrado = filtrado.filter(Q(username__icontains=buscar) |
                                   Q(first_name__icontains=buscar) |
                                   Q(last_name__icontains=buscar))
    if grupo != '' and grupo is not None:
        filtrado = filtrado.filter(Q(groups__id=grupo))

    registros = filtrado.count()
    paginado = paginador(query_dict, filtrado)

    form = FiltroUsuario(initial={'buscar': buscar,
                                  'items': items,
                                  'grupo': grupo,
                                  'modo': modo})
    return {'filter': filtrado,
            'paginado': paginado,
            'registros': registros,
            'filtros_form': form}
