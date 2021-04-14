from django.urls import path
from .views import (mensaje_agregar,
                    mensajes_listar,
                    mensaje_editar,
                    mensaje_ver,
                    mensaje_eliminar,
                    mensaje_responder,
                    contar_mensajes_pendientes,
                    )


urlpatterns = [
    path('mensaje_agregar/', mensaje_agregar, name='mensaje_agregar'),
    path('mensajes_listar/', mensajes_listar, name='mensajes_listar'),
    path('mensaje_editar/<int:id>', mensaje_editar, name='mensaje_editar'),
    path('mensaje_responder/<int:id>', mensaje_responder, name='mensaje_responder'),
    path('mensaje_ver/<int:id>', mensaje_ver, name='mensaje_ver'),
    path('mensaje_eliminar/<int:id>', mensaje_eliminar, name='mensaje_eliminar'),
    path('contar_mensajes_pendientes/', contar_mensajes_pendientes,
         name='contar_mensajes_pendientes'),

]