from django.urls import reverse
from clientes.models import Cliente
from perfiles.funcs import get_preferencia, get_cliente_asociado
from tabla.templatetags.custom_tags import traducir


def menu_processor(request):
    css_version = '?v=1.2'
    usuario = request.user
    if usuario.is_authenticated:
        clicod = get_cliente_asociado(usuario)
        cliente_asociado = []
        try:
            cliente_asociado = Cliente.objects.filter(clicod=clicod).values('encriptado', 'id')[0]
        except Exception as e:
            cliente_asociado = {'encriptado': 0,'id': 0}
        fijar_menu = get_preferencia(usuario, 'menu', 'fijar', 'L', False)
        modo_obscuro = get_preferencia(usuario, 'menu', 'modo_obscuro', 'L', False)
        print('cliente asociado: ', cliente_asociado)
        # CLIENTES
        cuentas_puede_listar = True
        cuenta_corriente = True
        if cliente_asociado['id'] > 0:
            cuentas_puede_listar = request.user.has_perm('clientes.cuentas_listar')
            cuenta_corriente = request.user.has_perm('clientes.cuenta_corriente')
        print('cuenta corriente: ', cuenta_corriente)

        # PROVEEDORES
        # Para Cargar Facturas de Compra ...

        # SOPORTE
        clientes_puede_listar = request.user.has_perm('clientes.puede_listar')
        proveedores_puede_listar = request.user.has_perm('proveedores.puede_listar')
        documento_puede_listar = request.user.has_perm('documentos.puede_listar')
        plantilla_puede_listar = request.user.has_perm('tabla.plantilla_puede_listar')

        # CONFIGURACIÓN
        mostrar_admin = False
        if request.user.is_staff or request.user.is_superuser:
            mostrar_admin = True
        numerador_puede_listar = request.user.has_perm('numeradores.numerador_puede_listar')
        tabla_puede_listar = request.user.has_perm('tablas.tabla_puede_listar')
        variable_puede_listar = request.user.has_perm('tablas.variable_puede_listar')

        grupo_cliente_mostrar = True
        grupo_proveedor_mostrar = True
        grupo_soporte_mostrar = False
        grupo_config_mostrar = False

        if cuentas_puede_listar or cuenta_corriente:
            grupo_cliente_mostrar = True

        if documento_puede_listar or plantilla_puede_listar or clientes_puede_listar:
            grupo_soporte_mostrar = True

        if numerador_puede_listar or tabla_puede_listar or variable_puede_listar or mostrar_admin:
            grupo_config_mostrar = True

        grupos = [
                  {'id': 'CLI', 'descripcion': 'Mis comprobantes',
                   'mostrar': get_preferencia(usuario, 'menu', 'CLI', 'L', True), 'visible': grupo_cliente_mostrar},
                  # {'id': 'PRO', 'descripcion': 'Proveedores',
                  #  'mostrar': get_preferencia(usuario, 'menu', 'PRO', 'L', True), 'visible': grupo_proveedor_mostrar},
                  {'id': 'SOP', 'descripcion': 'Soporte',
                   'mostrar': get_preferencia(usuario, 'menu', 'SOP', 'L', False), 'visible': grupo_soporte_mostrar},
                  {'id': 'CFN', 'descripcion': 'Configuración',
                   'mostrar': get_preferencia(usuario, 'menu', 'CFN', 'L', False), 'visible': grupo_config_mostrar},
                  ]

        menues = [
                  {'id_grupo': 'CLI', 'url': reverse('cuentas_listar', kwargs={'encriptado': cliente_asociado['encriptado']}),
                   'titulo':'Facturas Pendientes', 'modelo': 'CLIENTE', 'visible': True},
                  {'id_grupo': 'CLI', 'url': reverse('cuenta_corriente', kwargs={'encriptado': cliente_asociado['encriptado']}),
                   'titulo': 'Cuenta Corriente', 'modelo': 'CLIENTE', 'visible': True},
                  {'id_grupo': 'SOP', 'url': reverse('clientes_listar'), 'titulo': 'Clientes', 'modelo': 'CLIENTE',
                   'visible': clientes_puede_listar},
                  {'id_grupo': 'SOP', 'url': reverse('cuentas_listar'), 'titulo': 'Comprobantes', 'modelo': 'CUENTAS',
                   'visible': True},
                  {'id_grupo': 'SOP', 'url': reverse('documentos_listar'), 'titulo': 'Documentos',
                   'modelo': 'DOCUMENTO', 'visible': documento_puede_listar},
                  {'id_grupo': 'SOP', 'url': reverse('plantillas_listar'), 'titulo': 'Plantillas',
                   'modelo': 'PLANTILLA', 'visible': plantilla_puede_listar},

                  {'id_grupo': 'CFN', 'url': '/admin/', 'titulo': 'Admin', 'modelo': 'GENERAL',
                   'visible': mostrar_admin},
                  {'id_grupo': 'CFN', 'url': reverse('numeradores_listar'), 'titulo': 'Numeradores',
                   'modelo': 'NUMERADOR',
                   'visible': numerador_puede_listar},
                  {'id_grupo': 'CFN', 'url': reverse('tablas_listar'), 'titulo': 'Tablas', 'modelo': 'TABLA',
                   'visible': tabla_puede_listar},
                  {'id_grupo': 'CFN', 'url': reverse('variables_listar'), 'titulo': 'Variables', 'modelo': 'VARIABLE',
                   'visible': variable_puede_listar},
                  ]

        for menu in menues:
            menu['titulo'] = traducir(menu['titulo'], menu['modelo'])

        carpeta_media = request.build_absolute_uri('/media/')
        return {'menues': menues,
                'grupos': grupos,
                'fijar_menu': fijar_menu,
                'css_version': css_version,
                'modo_obscuro': modo_obscuro,
                'carpeta_media': carpeta_media,
                'titulo': 'XAdmin Web',
                'logo': 'logo.png'}
    else:
        return {'titulo': 'XAdmin Web',
                'logo': 'logo.png'}
