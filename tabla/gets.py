from .models import Tabla, Variable
from django.contrib.auth.models import User, Group
import datetime


def get_default(entidad):
    try:
        default = Tabla.objects.get(entidad=entidad, valor_preferencial='S')
    except Exception as e:
        default = Tabla.objects.filter(entidad=entidad).\
            order_by('-valor_preferencial', 'descripcion', 'codigo').first()
    return default


def get_choices(entidad):
    tipos = Tabla.objects.filter(entidad=entidad, activo='S').order_by('-valor_preferencial',
                                                           'descripcion').values('id', 'descripcion', 'codigo')
    if tipos.count() == 0 and entidad == 'ROL_INSTITUCION':
        tipos = Tabla.objects.filter(entidad='ROL').order_by('-valor_preferencial',
                                                             'descripcion').values('id', 'descripcion')
    if entidad == 'LOCALIDAD':
        choices = [(q['id'], q['descripcion'] + ' (' + q['codigo'] + ')') for q in tipos]
    else:
        choices = [(q['id'], q['descripcion']) for q in tipos]
    return choices


def get_user_choices(grupo):
    if grupo != 0 and grupo is not None:
        tipos = User.objects.filter(groups__id=grupo).order_by('-username').values('id', 'username')
    else:
        tipos = User.objects.all().order_by('-username').values('id', 'username')

    choices = [(q['id'], q['username']) for q in tipos]
    choices.insert(0, ('', '-----'))
    return choices


def get_user_groups(user):
    grupos = Group.objects.filter(user=user)
    choices = ()
    # choices += (('', '-----'),)
    for g in grupos:
        choices += ((g.id, g.name),)

    # print('****choices: ', choices)
    # print('****choices: ', type(choices))
    return choices


def get_group_choices():
    tipos = Group.objects.all().order_by('-name').values('id', 'name')
    choices = [(q['id'], q['name']) for q in tipos]
    choices.insert(0, ('', '-----'))
    return choices


def get_choices_mas_vacio(entidad):
    choices = get_choices(entidad)
    choices.insert(0, ('', '-----'))
    return choices


def get_choices_localidades_de_una_provincia(provincia_id):
    provincia = Tabla.objects.filter(id=provincia_id).values('codigo')
    provincia_codigo = provincia[0]['codigo']
    localidades = Tabla.objects.filter(entidad='LOCALIDAD',
                                       superior_codigo=provincia_codigo).order_by('-valor_preferencial', 'descripcion').values('id', 'descripcion', 'codigo')

    choices = [(q['id'], q['descripcion']+' ('+q['codigo']+')') for q in localidades]
    choices.insert(0, ('', '-----'))
    return choices


def list_registros_de_entidad(entidad):
    lista = ()
    registros = Tabla.objects.filter(entidad=entidad).order_by('descripcion')
    for registro in registros:
        lista += (
                    (registro.codigo, registro.descripcion),
                )
    return lista


def qs_provincia_de_una_localidad(localidad_id):
    localidad = Tabla.objects.filter(id=localidad_id).values('superior_codigo')
    provincia_codigo = localidad[0]['superior_codigo']
    provincia = Tabla.objects.filter(entidad='PROVINCIA', codigo=provincia_codigo).values('id', 'codigo')
    return provincia


def qs_localidades_de_una_provincia(provincia_id):
    provincia = Tabla.objects.filter(id=provincia_id, activo='S').values('codigo')
    provincia_codigo = provincia[0]['codigo']
    localidades = Tabla.objects.filter(entidad='LOCALIDAD',
                                       superior_codigo=provincia_codigo).order_by('-valor_preferencial', 'descripcion')
    # choices = localidades.values_list('id', 'descripcion')
    return localidades


def qs_subordinados_de_una_entidad(entidad_id):
    if entidad_id != '' and entidad_id is not None:
        entidad = Tabla.objects.filter(id=entidad_id).values('codigo', 'entidad')
        entidad_codigo = entidad[0]['codigo']
        entidad_entidad = entidad[0]['entidad']
        subordinados = Tabla.objects.filter(superior_entidad=entidad_entidad,
                                            superior_codigo=entidad_codigo,
                                            activo='S').order_by('-valor_preferencial', 'descripcion')
    else:
        subordinados = Tabla.objects.none()

    return subordinados


def qs_entidad_de_un_subordinado(subordinado_id):
    subordinado = Tabla.objects.filter(id=subordinado_id).values('superior_codigo', 'superior_entidad')
    entidad_codigo = subordinado[0]['superior_codigo']
    entidad_entidad = subordinado[0]['superior_entidad']
    entidad = Tabla.objects.filter(entidad=entidad_entidad, codigo=entidad_codigo).values('id', 'codigo')

    return entidad


def get_variable(codigo_variable, valor_por_defecto):
    try:
        valores = Variable.objects.get(variable=codigo_variable.upper())
    except Variable.DoesNotExist:
        valor_logico = False
        valor_numerico = 0
        valor_fecha = None
        valor_caracter = ''
        if type(valor_por_defecto) == bool:
            tipo = 'L'
            valor_logico = valor_por_defecto
        elif type(valor_por_defecto) == int:
            tipo = 'N'
            valor_numerico = valor_por_defecto
        elif type(valor_por_defecto) == datetime.datetime:
            tipo = 'F'
            valor_fecha = valor_por_defecto
        else:
            tipo = 'C'
            valor_caracter = valor_por_defecto

        valores = Variable(variable=codigo_variable.upper(),
                           tipo=tipo,
                           caracter=valor_caracter,
                           logico=valor_logico,
                           numero=valor_numerico,
                           fecha=valor_fecha)
        valores.save()

    if valores:
        tipo = valores.tipo
        if tipo == 'C':
            return valores.caracter
        elif tipo == 'F':
            return valores.fecha
        elif tipo == 'N':
            return valores.numero
        elif tipo == 'L':
            return valores.logico
        else:
            return valor_por_defecto
    else:
        return valor_por_defecto


def set_variable(codigo_variable, valor):
    try:
        variable = Variable.objects.get(variable=codigo_variable.upper())
        if variable.tipo == 'F':
            variable.fecha = valor
        elif variable.tipo == 'N':
            variable.numero = valor
        elif variable.tipo == 'L':
            variable.logico = valor
        else:
            variable.caracter = valor
        variable.save()

    except Variable.DoesNotExist:
        valor = get_variable(codigo_variable, valor)

    return True

