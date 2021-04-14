from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.conf import settings
from django.contrib.auth import user_logged_in
from django.contrib.sessions.models import Session
from simple_history.models import HistoricalRecords
from tabla.models import Tabla
from tabla.gets import get_choices
from django.contrib.auth.models import Group


dependencias = get_choices('DEPENDENCIA')
Group.add_to_class('dependencia', models.IntegerField(null=True, blank=True,
                                                      choices=dependencias))


def get_image_filename(instance, filename):
    primaryKey = instance.pk
    return "Users/ %s/ %s" % (str(primaryKey), filename)


class Perfil(models.Model):
    """Estos son atributos extras que se le pueden dar a los usuarios del sistema"""

    """El Nivel es una clasificación que puede servir para emparejar dos entidades"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil', verbose_name='Usuario')
    nivel = models.ManyToManyField(Tabla, related_name='nivel', blank=True)
    telefono = models.CharField(max_length=40, null=True, blank=True)
    foto = models.ImageField(upload_to=get_image_filename, null=True, blank=True)
    fecha_clave = models.DateField(null=True, blank=True,  verbose_name='Última actualización de clave')
    email_contacto = models.EmailField(max_length=100, null=True, blank=True,
                                       validators=[validate_email], verbose_name='E-mail de contacto')
    history = HistoricalRecords(table_name='historico_perfil')

    class Meta:
        verbose_name_plural = "perfiles"

    def __str__(self):

        return "Usuario {}".format(self.user)


class Preferencia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,  default=User)
    vista = models.CharField(max_length=60)
    opcion = models.CharField(max_length=60)
    fecha = models.DateField(null=True, blank=True)
    caracter = models.CharField(max_length=100, null=True, blank=True)
    numero = models.DecimalField(decimal_places=4, max_digits=14, null=True, blank=True)
    logico = models.BooleanField(default=False, null=True)
    history = HistoricalRecords(table_name='historico_preferencia')

    class Meta:
        unique_together = (("usuario", "vista", "opcion"),)

    def __str__(self):

        return "{} en {} del usuario {}".format(self.opcion, self.vista, self.usuario)


class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)


# ----------------------------------------------
# Este código se dispara cuando el usuario inicia sesión y previene que un mismo usuario
# tenga más de una sesión activa simultánea.
def eliminar_sesiones_anteriores(sender, user, request, **kwargs):
    # Eliminar sessiones anteriores
    Session.objects.filter(usersession__user=user).delete()
    # guardar la nueva sesión
    request.session.save()
    # Crear el vínculo entre la sesión y el usuario, para poder eliminarlos cuando se vuelva a ejecutar esta señal
    UserSession.objects.get_or_create(user=user, session=Session.objects.get(pk=request.session.session_key))


user_logged_in.connect(eliminar_sesiones_anteriores)
# ---------------------------------------------
