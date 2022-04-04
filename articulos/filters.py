from articulos.models import Articulo
from django.db.models import Q
from tabla.filters import paginador
from articulos.forms import FiltroArticulo
from perfiles.funcs import get_opcion_paginado


def articulos_filtrar(query_dict):
    buscar = query_dict.GET.get('buscar')
    departamento = query_dict.GET.get('departamento')
    marca = query_dict.GET.get('marca')
    items = get_opcion_paginado(query_dict)
    modo = query_dict.GET.get('modo')
    filtrado = Articulo.objects.all()

    if buscar != '' and buscar is not None:
        filtrado = filtrado.filter(Q(artcod__icontains=buscar) |
                                   Q(descripcion__icontains=buscar)
                                   )
    if departamento != ''and departamento is not None:
        filtrado=filtrado.filter(departamento_id=departamento)

    if marca != '' and marca is not None:
       filtrado=filtrado.filter(marca_id=marca)

    registros = filtrado.count()
    paginado = paginador(query_dict, filtrado)

    form = FiltroArticulo(initial={'buscar': buscar,
                                   'items': items,
                                   'modo': modo,
                                   'marca' : marca,
                                   'departamento' : departamento})
    return {'filter': filtrado,
            'paginado': paginado,
            'registros': registros,
            'filtros_form': form}
