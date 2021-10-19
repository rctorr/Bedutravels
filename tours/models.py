from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Perfil(models.Model):
    """ Define la tabla User """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    tipo = models.CharField(max_length=45, null=True, blank=True)
    # genero -> ("H", "M")
    GENERO = [
        ("H", "Hombre"),
        ("M", "Mujer"),
        ("O", "Otro"),
        ("N", "Ninguno"),
    ]
    genero = models.CharField(max_length=1, choices=GENERO)

    def __str__(self):
        """ Representación en str para User """
        return self.user

class Zona(models.Model):
    """ Define la tabla Zona """
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=256, null=True, blank=True)
    latitud = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)

    def __str__(self):
        """ Representación en str para Zona """
        return self.nombre

def user_directory_path(tour, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/tour_<id>/<filename>
    return f'user_{tour.user.id}/tour_{tour.id}/{filename}'

class Tour(models.Model):
    """ Define la tabla Tour """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             blank=True)
    nombre = models.CharField(max_length=145)
    slug = models.CharField(max_length=45, null=True, blank=True)
    operador = models.CharField(max_length=45, null=True, blank=True)
    tipoDeTour = models.CharField(max_length=45, null=True, blank=True)
    descripcion = models.CharField(max_length=256)
    img = models.ImageField(upload_to=user_directory_path, null=True,
                            blank=True, max_length=256)
    pais = models.CharField(max_length=45, null=True, blank=True)
    zonaSalida = models.ForeignKey(Zona, on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   related_name="tours_salida")
    zonaLlegada = models.ForeignKey(Zona, on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name="tours_llegada")

    def __str__(self):
        return f"{self.nombre}"

