"""xadmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

handler404 = 'menu.views.handler404'
handler500 = 'menu.views.handler500'
handler403 = 'menu.views.handler403'
handler400 = 'menu.views.handler400'

urlpatterns = [
    path('', include('menu.urls')),
    path('ingresar/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='ingresar'),
    path('salir/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='salir'),
    path('tinymce/', include('tinymce.urls')),
    path('password/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'XAdmin | Gestión WEB'
admin.site.site_title = 'XAdmin | Gestión WEB'
# admin.site.index_title = 'Gestión ON-LINE'