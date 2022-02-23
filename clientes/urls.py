from django.urls import path
from .views import (cliente_agregar,
                    clientes_listar,
                    cliente_editar,
                    cliente_eliminar,
                    clientes_cargar_csv,
                    cliente_agregar_y_volver,
                    cuentas_agregar,
                    cuentas_editar,
                    cuentas_eliminar,
                    facturas_pendientes,
                    cuentas_listar_admin,
                    cuenta_corriente,
                    cuentas_importar,
                    imprimir_png,
                    )


urlpatterns = [
    path('cliente_agregar/', cliente_agregar, name='cliente_agregar'),
    path('cliente_agregar_y_volver/', cliente_agregar_y_volver, name='cliente_agregar_y_volver'),
    path('clientes_listar/', clientes_listar, name='clientes_listar'),
    path('cliente_editar/<slug:encriptado>', cliente_editar, name='cliente_editar'),
    path('cliente_eliminar/<int:id>', cliente_eliminar, name='cliente_eliminar'),
    path('cliente_importar/', clientes_cargar_csv, name='cliente_importar'),
    path('cuentas_agregar/', cuentas_agregar, name='cuentas_agregar'),
    path('cuentas_editar/<int:id>', cuentas_editar, name='cuentas_editar'),
    path('cuentas_eliminar/<int:id>', cuentas_eliminar, name='cuentas_eliminar'),
    path('facturas_pendientes/<slug:encriptado>', facturas_pendientes, name='facturas_pendientes'),
    path('cuentas_listar/', cuentas_listar_admin, name='cuentas_listar_admin'),
    path('cuentas_importar/', cuentas_importar, name='cuentas_importar'),
    path('cuenta_corriente/<slug:encriptado>', cuenta_corriente, name='cuenta_corriente'),
    path('imprimir_png/<int:id>/<slug:encriptado>', imprimir_png, name='imprimir_png'),
]
