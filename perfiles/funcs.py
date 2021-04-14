from django.contrib.auth.models import Group
from perfiles.models import Preferencia, Perfil
from tabla.gets import get_variable
from tabla.models import Tabla
from datetime import date


def debe_cambiar_clave(usuario):
    try:
        perfil = Perfil.objects.get(user=usuario)
        if not perfil.fecha_clave:
            cambiar_clave = True
        else:
            cambiar_clave = False
            v_clave_expira = get_variable('V_CLAVE_EXPIRA', 0)
            if v_clave_expira > 0:
                dif = date.today()-perfil.fecha_clave
                if dif.days >= v_clave_expira:
                    cambiar_clave = True

    except Exception as e:
        cambiar_clave = True

    return cambiar_clave


def actualizar_fecha_de_clave(usuario, fecha):
    if not fecha:
        fecha= date.today()

    try:
        perfil = Perfil.objects.get(user=usuario)
        perfil.fecha_clave = fecha

    except Exception as e:
        perfil = Perfil(user_id=usuario, fecha_clave=fecha)

    perfil.save()

    return fecha


def get_preferencia(usuario, vista, opcion, tipo_dato, default):
    try:
        preferencia = Preferencia.objects.get(usuario=usuario, vista=vista, opcion=opcion)
        fecha = preferencia.fecha
        caracter = preferencia.caracter
        numero = preferencia.numero
        logico = preferencia.logico
    except Exception as e:
        fecha = None
        caracter = None
        numero = None
        logico = None

    if tipo_dato.upper() == 'F':
        valor = fecha
    elif tipo_dato.upper() == 'C':
        valor = caracter
    elif tipo_dato.upper() == 'L':
        valor = logico
    else:
        valor = numero

    if valor is None:
        valor = default
    return valor


def set_preferencia(preferencia):
    usuario = preferencia['usuario']
    vista = preferencia['vista']
    opcion = preferencia['opcion']
    try:
        fecha = preferencia['fecha']
    except Exception as e:
        fecha = None

    try:
        caracter = preferencia['caracter']
    except Exception as e:
        caracter = None

    try:
        numero = preferencia['numero']
    except Exception as e:
        numero = None

    try:
        logico = preferencia['logico']
    except Exception as e:
        logico = None

    try:
        preferencia = Preferencia.objects.get(usuario=usuario, vista=vista, opcion=opcion)
    except Exception as e:
        preferencia = Preferencia.objects.create(usuario=usuario, vista=vista, opcion=opcion)

    try:
        preferencia.fecha = fecha
        preferencia.caracter = caracter
        preferencia.numero = numero
        preferencia.logico = logico
        preferencia.save()
        return True
    except Exception as e:
        return False


def get_dependencia(usuario):

    dependencias_posibles = get_dependencias_posibles(usuario)
    if len(dependencias_posibles) > 0:
        dependencia_x_defecto = dependencias_posibles[0]
    else:
        dependencia_x_defecto = None
    dependencia = get_preferencia(usuario, 'menu', 'dependencia_x_defecto', 'C', dependencia_x_defecto)
    if dependencia is not None:
        if len(dependencias_posibles) > 0:
            if int(dependencia) not in dependencias_posibles:
                if len(dependencias_posibles) > 0:
                    dependencia = dependencias_posibles[0]
                else:
                    dependencia = None

    return dependencia


def get_dependencias_posibles(usuario):
    grupos = Group.objects.filter(user=usuario).exclude(dependencia=None)
    dependencias = []
    for grupo in grupos:
        dependencias.append(grupo.dependencia)
    return dependencias


def get_choices_dependencias_de_usuario(usuario):
    dependencias_posibles = get_dependencias_posibles(usuario)
    if len(dependencias_posibles) == 0:
        dependencias = Tabla.objects.filter(entidad='DEPENDENCIA', activo='S').\
                                     order_by('-valor_preferencial', 'descripcion').\
                                     values('id', 'descripcion', 'codigo')
    else:
        dependencias = Tabla.objects.filter(entidad='DEPENDENCIA', activo='S', id__in=dependencias_posibles). \
                                     order_by('-valor_preferencial', 'descripcion'). \
                                     values('id', 'descripcion', 'codigo')

    choices = [(q['id'], q['descripcion']) for q in dependencias]
    return choices


def get_dependencia_activa(usuario):
    dependencia = get_dependencia(usuario)
    if dependencia == '' or dependencia is None:
        dependencia = None
    else:
        try:
            dependencia = Tabla.objects.get(id=int(dependencia))
        except Exception as e:
            dependencia = None

    return dependencia


def get_opcion_paginado(query_dict):
    usuario = query_dict.user
    default = get_preferencia(usuario, 'filtro', 'paginado', 'N', 10)
    items = query_dict.GET.get('items', default)
    if not items:
        items = 10
    if default != items:
        preferencia = {'usuario': usuario,
                       'vista': 'filtro',
                       'opcion': 'paginado',
                       'numero': int(items)}
        res = set_preferencia(preferencia)

    return int(items)