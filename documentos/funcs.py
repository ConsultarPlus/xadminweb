from django import forms
from django.template.defaultfilters import filesizeformat
from xadmin import settings
from .models import Documento


def clean_archivo_helper(content):
    try:
        content_type = content.content_type.split('/')[1]
        if content_type in settings.CONTENT_TYPES:
            if content.size > int(settings.MAX_UPLOAD_SIZE):
                maximo = filesizeformat(settings.MAX_UPLOAD_SIZE)
                actual = filesizeformat(content.size)
                mensaje = 'El tamaño de archivo máximo es {}. El seleccionado es de {})'.format(maximo, actual)
                raise forms.ValidationError(mensaje)
        else:
            raise forms.ValidationError('Tipo de archivo no permitido')
    except Exception as e:
        pass
    return content


def guardar_documento(archivo, entidad, entidad_id, descripcion):
    if archivo:
        try:
            documento = Documento.objects.get(entidad=entidad, entidad_id=entidad_id)
            documento.archivo = archivo
            documento.descripcion = descripcion
        except Documento.DoesNotExist:
            documento = Documento(entidad=entidad, entidad_id=entidad_id, descripcion=descripcion, archivo=archivo)

        documento.save()
        return True
    return False
