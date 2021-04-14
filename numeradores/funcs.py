from tabla.models import Tabla
from .models import Numerador


def get_numero(id, entidad):
    comprobante = entidad
    """
        Una vez determinado el contador para la entidad, se obtiene el último valor
        Si el contador no existe, se crea, sino se adelanta el número        
    """
    if comprobante:
        numerador = Numerador.objects.filter(comprobante=comprobante).values('ultimo_valor')
        if numerador:
            ultimo_valor = numerador[0]['ultimo_valor'] + 1
        else:
            ultimo_valor = 1

        numerador=Numerador(comprobante=comprobante, descripcion=entidad,
                            ultimo_valor=ultimo_valor, activo='S')
        numerador.save()
    else:
        ultimo_valor = 1

    return ultimo_valor
