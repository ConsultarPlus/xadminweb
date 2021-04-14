from django.urls import path
from .views import (documento_agregar,
                    documentos_listar,
                    documento_editar,
                    documento_eliminar,
                    documento_agregar_y_volver)


urlpatterns = [
    path('documento_agregar/', documento_agregar, name='documento_agregar'),
    path('documento_agregar_y_volver/', documento_agregar_y_volver, name='documento_agregar_y_volver'),
    path('documentos_listar/', documentos_listar, name='documentos_listar'),
    path('documento_editar/<int:id>', documento_editar, name='documento_editar'),
    path('documento_eliminar/<int:id>', documento_eliminar, name='documento_eliminar'),

]
