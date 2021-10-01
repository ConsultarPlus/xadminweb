from django.urls import path
from .views import (cliente_agregar,
                    clientes_listar,
                    cliente_editar,
                    cliente_eliminar,
                    cliente_agregar_y_volver,
                    cuentas_listar,
                    cuenta_corriente,
                    cuentas_imprimir,
                    )


urlpatterns = [
    path('cliente_agregar/', cliente_agregar, name='cliente_agregar'),
    path('cliente_agregar_y_volver/', cliente_agregar_y_volver, name='cliente_agregar_y_volver'),
    path('clientes_listar/', clientes_listar, name='clientes_listar'),
    path('cliente_editar/<int:id>', cliente_editar, name='cliente_editar'),
    path('cliente_eliminar/<int:id>', cliente_eliminar, name='cliente_eliminar'),
    path('cuentas_listar/<int:id>', cuentas_listar, name='cuentas_listar'),
    path('cuentas_imprimir/<int:id>', cuentas_imprimir, name='cuentas_imprimir'),
    path('cuenta_corriente/<int:id>', cuenta_corriente, name='cuenta_corriente'),

]
