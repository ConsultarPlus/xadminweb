from django.core.exceptions import ValidationError


def validar_mayusculas_minusculas_y_especiales(cadena):
    hay_mayusculas = False
    hay_minusculas = False
    hay_numeros = False
    hay_caracteres = False

    for letra in cadena:
        if letra.isupper():
            hay_mayusculas = True
        elif letra.islower():
            hay_minusculas = True
        elif letra.isdigit():
            hay_numeros = True
        else:
            hay_caracteres = True

    if hay_mayusculas and hay_minusculas and hay_caracteres and hay_numeros:
        return True
    else:
        return False


class ValidarClave(object):
    def validate(self, password, user=None):
        if not validar_mayusculas_minusculas_y_especiales(password):
            mensaje = "La nueva contraseña debe tener mayúsculas, minúsculas  y caracteres especiales"
            raise ValidationError(mensaje, code='password_case',)

    def get_help_text(self):
        return "Su contraseña debe tener mayúsculas y minúsculas"
