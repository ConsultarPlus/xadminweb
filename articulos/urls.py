from django.urls import path
from articulos.views import articulos_listar, articulo_editar, articulos_importar, articulo_agregar


urlpatterns = [
    path('articulos_listar/', articulos_listar, name='articulos_listar'),
    path('articulo_editar/<int:id>', articulo_editar, name='articulo_editar'),
    path('articulos_importar/', articulos_importar, name='articulos_importar'),
    path('articulo_agregar/', articulo_agregar, name='articulo_agregar')
]