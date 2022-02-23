from django.urls import path
from django import views as django_views
from perfiles import views


urlpatterns = [
    path('cambiar_clave/', views.cambiar_clave, name='cambiar_clave'),
    path('usuario_modificar/', views.usuario_modificar, name='usuario_modificar'),
    path('usuario_nombre/', views.usuario_nombre, name='usuario_nombre'),
    path('usuarios_listar/', views.usuarios_listar, name='usuarios_listar'),
    path('seleccionar_usuario/', views.seleccionar_usuario, name='seleccionar_usuario'),
    path('seleccionar_usuarios/', views.seleccionar_usuarios, name='seleccionar_usuarios'),
    path('preferencia_grabar_asinc/', views.preferencia_grabar_asinc, name='preferencia_grabar_asinc'),
    path('jsi18n/', django_views.i18n.JavaScriptCatalog.as_view(), name='jsi18n'),
]
