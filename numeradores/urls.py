from django.urls import path, include
from .views import numerador_prueba, numerador_agregar, numerador_editar, numerador_eliminar, numeradores_listar
from django.urls import path


urlpatterns = [
    path('numerador_prueba/', numerador_prueba, name='numerador_prueba'),
    path('numerador_agregar/', numerador_agregar, name='numerador_agregar'),
    path('numerador_editar/<slug:comprobante>', numerador_editar, name='numerador_editar'),
    path('numerador_eliminar/<slug:comprobante>', numerador_eliminar, name='numerador_eliminar'),
    path('numeradores_listar/', numeradores_listar, name='numeradores_listar'),
]
