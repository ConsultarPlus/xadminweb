from django.urls import path
from articulos.views import articulos_listar, articulo_editar, articulos_importar, articulo_agregar, articulo_eliminar, cargar_rubro,cargar_seccion

urlpatterns = [
    path('articulos_listar/', articulos_listar, name='articulos_listar'),
    path('articulo_editar/<int:id>', articulo_editar, name='articulo_editar'),
    path('articulos_importar/', articulos_importar, name='articulos_importar'),
    path('articulo_agregar/', articulo_agregar, name='articulo_agregar'),
    path('articulo_eliminar/<int:id>', articulo_eliminar, name='articulo_eliminar'),
    path('cargar_rubro/', cargar_rubro, name='cargar_rubro'),
    path('cargar_seccion/', cargar_seccion, name='cargar_seccion')
]
