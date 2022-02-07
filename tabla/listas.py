
ENTIDADES = (
    ('DEPENDENCIA', 'Dependencia'),
    ('LOCALIDAD', 'Localidad'),
    ('PROVINCIA', 'Provincia'),
    ('COMPROBANTE', 'Comprobante'),
    ('ESTADO', 'Estado de expediente'),
    ('TIPO_DOCUMENTO', 'Tipo de documento'),
    ('ESTADO_CIVIL', 'Estado Civil'),
    ('SECTOR', 'Sector'),
    ('SUBSECTOR', 'Sub-sector'),
    ('TEMA', 'Tema'),
    ('SUBTEMA', 'Sub-tema'),
    ('GENERO', 'Género'),
    ('NIVEL', 'Nivel'),
    ('ORIGEN', 'Origen'),
    ('ROL', 'Rol de persona '),
    ('ROL_INSTITUCION', 'Rol de institución'),
    ('CIRCUITO', 'Circuito'),
    ('TIPO_DEPENDENCIA', 'Tipo de dependencia'),
    ('ESTADO_TURNO', 'Estado del ticket de turno'),
    ('PAIS', 'País'),
    ('TIPO_NACIONALIDAD', 'Tipo de nacionalidad'),

)

IVAS = (
    ('I', 'INSCRIPTO'),
    ('E', 'EXCENTO'),
    ('M', 'MONOTRIBUTO'),
    ('C', 'CONSUMIDOR FINAL'),
    ('N', 'EXCENTO TIERRA'),
    ('P', 'PUBLICIDAD'),
    ('S', 'SERVICIOS'),
)

ACTIVO = (
    ('S', 'Activo'),
    ('N', 'Inactivo'),
)

SINO = (
    ('S', 'Sí'),
    ('N', 'No'),
)


PRIORIDAD = (
    ('A', 'Alta'),
    ('M', 'Media'),
    ('B', 'Baja'),
)

PRIORIDAD_MAS_VACIO = (('', '---'),) + PRIORIDAD

AMBITO = (
    ('N', 'Nacional'),
    ('P', 'Provincial'),
    ('M', 'Municipal'),
    ('A', 'Particular'),
)

AMBITO_TUP = dict(AMBITO)

APLICACIONES = (
    ('PERSONA', 'Persona'),
    ('EXPEDIENTE', 'Expediente'),
    ('COMPROBANTE', 'Comprobante'),
)


TIPOS_DE_VARIABLE = (
        ('F', 'Fecha'),
        ('C', 'Caracter'),
        ('N', 'Numérico'),
        ('L', 'Lógico'),
    )

ITEMS_X_PAG = (
    ('5', 'ver 5 ítems'),
    ('10', 'ver 10 ítems'),
    ('15', 'ver 15 ítems'),
    ('30', 'ver 30 ítems'),
    )

etiquetas_turno = (
                   ('{{ turno_fecha }}', 'Fecha del turno'),
                   ('{{ turno_hora }}', 'Hora  del turno'),
                   ('{{ turno_tema }}', 'Tema  del turno'),
                   ('{{ turno_numero }}', 'Número  del turno'),
                   ('{{ turno_dependencia }}', 'Dependencia  del turno'),
                   )

etiquetas_expedientes = (
                         ('{{ expediente_nro }}', 'Número de expediente'),
                         ('{{ expediente_fecha }}', 'Fecha de expediente'),
                         ('{{ quejoso }}', 'Nombre del quejoso'),
                         ('{{ quejoso_calle_nombre }}', 'Domicilio del quejoso (calle)'),
                         ('{{ quejoso_calle_altura }}', 'Domicilio del quejoso (altura)'),
                         ('{{ quejoso_entre_calle_1 }}', 'Entre calle 1 del quejoso'),
                         ('{{ quejoso_entre_calle_2 }}', 'Entre calle 2 del quejoso'),
                         ('{{ quejoso_piso }}', 'Piso del quejoso'),
                         ('{{ quejoso_depto }}', 'Departamento del quejoso'),
                         ('{{ quejoso_telefono }} ', 'Teléfono del quejoso'),
                         ('{{ quejoso_celular }} ', 'Celular del quejoso'),
                         ('{{ quejoso_twitter }} ', 'Twitter del quejoso'),
                         ('{{ quejoso_instagram }} ', 'Instagram del quejoso'),
                         ('{{ quejoso_facebook }} ', 'Facebook del quejoso'),
                         ('{{ quejoso_email }} ', 'E-mail del quejoso'),
                         ('{{ quejoso_fecha_nacimiento }} ', 'Fecha de nacimiento del quejoso'),
                         ('{{ quejoso_edad }} ', 'Edad del quejoso'),
                         ('{{ quejoso_estado_civil }} ', 'Estado civil del quejoso'),
                         ('{{ quejoso_genero }} ', 'Género del quejoso'),
                         # ('{{ quejoso_nacionalidad }} ', 'Nacionalidad del quejoso'),
                         # ('{{ quejoso_tipo_nacionalidad }} ', 'Tipo de nacionalidad del quejoso'),
                         ('{{ quejoso_provincia }} ', 'Provincia del quejoso'),
                         ('{{ quejoso_localidad }} ', 'Localidad del quejoso'),
                         ('{{ expediente_sector }}', 'Sector del expediente'),
                         ('{{ expediente_subsector }}', 'Subsector del expediente'),
                         ('{{ expediente_tema }}', 'Tema del expediente'),
                         ('{{ expediente_subtema }}', 'Subtema del expediente'),
                         ('{{ expediente_queja }}', 'Queja'),
                         ('{{ expediente_usuario }}', 'Usuario/Instructor (código)'),
                         ('{{ expediente_usuario_nombre_y_apellido }}', 'Usuario/Instructor (nombre y apellido)'),
                         ('{{ expediente_es_admisible }}', 'Admisible'),
                         ('{{ expediente_es_interno }}', 'Interno'),
                         ('{{ expediente_estado }}', 'Estado de expediente'),
                         ('{{ expediente_insumidos }}', 'Acciones de expediente', 'EXPEDIENTE'),
                         ('{{ expediente_requerimientos }}', 'Requerimientos de expediente', 'EXPEDIENTE'),
                         ('{{ expediente_vinculados }}', 'Expedientes vinculados', 'EXPEDIENTE'),
                         ('{{ expediente_personas_vinculadas }}', 'Personas vinculadas', 'EXPEDIENTE'),
                         ('{{ expediente_instituciones_vinculadas }}', 'Instituciones vinculadas', 'EXPEDIENTE'),
                         ('{{ expediente_comprobantes }}', 'Comprobantes de expediente', 'EXPEDIENTE'),
                         ('{{ expediente_documentos }}', 'Documentos de expediente', 'EXPEDIENTE'),
                         )

etiquetas_insumidos = (('{{ expediente_nro }}', 'Número de expediente'),
                       ('{{ expediente_estado }}', 'Estado de expediente'),
                       ('{{ insumido_fecha_hora }}', 'Fecha del insumido'),
                       ('{{ insumido_usuario_destino }}', 'Usuario destino'),
                       ('{{ insumido_usuario_origen }}', 'Usuario origen'),
                       ('{{ insumido_grupo_destino }}', 'Grupo destino'),
                       ('{{ insumido_grupo_origen }}', 'Grupo origen'),
                       ('{{ insumido_tipo_insumido }}', 'Tipo de insumido'),
                       ('{{ insumido_comprobante_nro}}', 'Nro. de comprobante'),
                       ('{{ insumido_prioridad }}', 'Prioridad'),
                       ('{{ insumido_observacion }}', 'Observación'),
                       ('{{ insumido_respuesta }}', 'Respuesta'),
                       ('{{ insumido_fecha_respuesta }}', 'Fecha de respuesta'),
                       )


etiquetas_cptes = (('{{ comprobante_nro }}',  'Número  de cpte'),
                   ('{{ comprobante_tipo_comprobante }}',  'Tipo de comprobante'),
                   ('{{ comprobante_institucion }}',  'Institución'),
                   ('{{ comprobante_responsable }}',  'Responsable'),
                   ('{{ comprobante_observacion }}',  'Observación'),
                   ('{{ comprobante_telefono }}',  'Teléfono'),
                   ('{{ comprobante_recepcion }}',  'Recepción'),
                   ('{{ comprobante_nro_tramite }}',  'Nro. trámite'),
                   ('{{ comprobante_respuesta }}',  'Respuesta'),
                   ('{{ comprobante_fecha }}', 'Fecha de cpte.'),
                   ('{{ comprobante_fecha_respuesta }}',  'Fecha de respuesta'),
                   )

etiquetas_personas = (('{{ persona_nombre_y_apellido }}', 'Nombre y apellido'),
                      ('{{ persona_calle_nombre }}', 'Calle'),
                      ('{{ persona_calle_altura }}', 'Altura de calle'),
                      ('{{ persona_piso }}', 'Piso'),
                      ('{{ persona_depto }}', 'Depto.'),
                      ('{{ persona_telefono }}', 'Teléfono'),
                      ('{{ persona_provincia }}', 'Provincia'),
                      ('{{ persona_localidad }}', 'Localidad'),
                      ('{{ persona_entre_calle_1 }}', 'Entre calle #1'),
                      ('{{ persona_entre_calle_2 }}', 'Entre calle #2'),
                      ('{{ persona_celular }}', 'Celular'),
                      ('{{ persona_twitter }}', 'Tweeter'),
                      ('{{ persona_instagram }}', 'Instagram'),
                      ('{{ persona_facebook }}', 'Facebook'),
                      ('{{ persona_email }}', 'E-mail'),
                      ('{{ persona_fecha_nacimiento }}', 'Fecha de nacimiento'),
                      ('{{ persona_edad }}', 'Edad'),
                      ('{{ persona_estado_civil }}', 'Estado civil'),
                      ('{{ persona_genero }}', 'Género'),
                      ('{{ persona_nacionalidad }}', 'Nacionalidad'),
                      ('{{ persona_tipo_documento }}', 'Tipo de documento'),
                      ('{{ persona_nro_documento }}', 'Nro. de documento'),
                      ('{{ persona_rol }}', 'Rol'),
                      )


etiquetas_instituciones = (('{{ institucion_vinculada }}', 'Institución'),
                           ('{{ institucion_vinculada_rol }}', 'Rol'),
                           ('{{ institucion_vinculada_sucursal }}', 'Sucursal'),
                           ('{{ institucion_vinculada_cuit }}', 'CUIT'),
                           ('{{ institucion_vinculada_calle }}', 'Calle'),
                           ('{{ institucion_vinculada_altura }}', 'Altura'),
                           ('{{ institucion_vinculada_localidad }}', 'Localidad'),
                           ('{{ institucion_vinculada_telefono }}', 'Teléfono'),
                           ('{{ institucion_vinculada_celular }}', 'Celular'),
                           ('{{ institucion_vinculada_e_mail }}', 'E-mail'),
                           ('{{ institucion_vinculada_ambito }}', 'Ámbito'),
                           ('{{ institucion_vinculada_observacion }}', 'Observación'),
                           ('{{ institucion_vinculada_responsable }}', 'Responsable'),
                           ('{{ institucion_vinculada_responsable_seccion }}', 'Responsable: Sección'),
                           ('{{ institucion_vinculada_responsable_telefono }}', 'Responsable: Teléfono'),
                           ('{{ institucion_vinculada_responsable_celular }}', 'Responsable: Celular'),
                           ('{{ institucion_vinculada_responsable_email }}', 'Responsable: E-mail'),
                           ('{{ institucion_vinculada_responsable_observacion }}', 'Responsable: Observación'),
                           )

etiquetas_otros = (('{{ salto_de_pagina }}', 'Salto de página'),
                   ('{{ip <ID de plantilla>|incluir_plantilla ip}}', 'Incluir plantilla'))

grupos_de_etiquetas = (
    ('', 'Seleccionar tipo de etiquetas'),
    ('COMPROBANTES', 'Comprobantes'),
    ('EXPEDIENTES', 'Expedientes'),
    ('INSUMIDOS', 'Insumidos'),
    ('INSTITUCIONES', 'Instituciones'),
    ('PERSONAS', 'Personas'),
    ('TURNOS', 'Turnos'),
    ('OTROS', 'Otros'),
)


HOJAS = (('A4', 'A4'),
         ('A5', 'A5'),
         ('CARTA', 'CARTA'),
         ('OFICIO', 'OFICIO'),
         ('LEGAL', 'LEGAL'),
         ('1/2 CARTA', '1/2 CARTA'),
         )


PREPOSICIONES = ('a', 'ante', 'bajo', 'cabe', 'con', 'contra', 'de', 'desde', '' +
                 'en', 'entre', 'hacia', 'hasta', 'para', 'por', 'según', 'segun', 'sin', '' +
                 'so', 'sobre', 'tras', 'durante', 'mediante', 'versus', 'vía', 'via', '' +
                 'y', 'o', 'u', 'ó', 'e', 'ni', 'no', 'si', 'sí')  # Estas últimas no son preposiciones, son nexos


MODELOS = (('EXPEDIENTE', 'Expedientes'),
           ('VARIABLE', 'Variables'),
           ('PLANTILLA', 'Plantillas'),
           ('TABLA', 'Tablas'),
           ('INSUMIDO', 'Insumidos'),
           ('TIPO_INSUMIDO', 'Tipos de insumidos'),
           ('COMPROBANTES', 'Comprobantes'),
           ('NUMERADORES', 'Numeradores'),
           ('GENERAL', 'General'),
           )

ADMISIBLES = (
    ('S', 'Admisible'),
    ('NO', 'No Admisible'),
    ('ADMISIBLE_OFICIO', 'Admisible Gestión Oficiosa'),
    ('ADMISIBLE_TELEFONICO', 'Admisible Gestión Telefónica'),
)