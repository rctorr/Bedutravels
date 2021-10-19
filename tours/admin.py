from django.contrib import admin
from .models import Perfil, Zona, Tour

# Personalizando modelos en el admin
class PerfilAdmin(admin.ModelAdmin):
    # Se sobre escribe lo que hace __str__
    list_display = ("id", "user", "fecha_nacimiento", "genero", "tipo")

class ZonaAdmin(admin.ModelAdmin):
    # Se sobre escribe lo que hace __str__
    list_display = ("id", "nombre", "descripcion", "latitud", "longitud")

class TourAdmin(admin.ModelAdmin):
    # Se sobre escribe lo que hace __str__
    list_display = ("id", "nombre", "descripcion", "operador", "user",
                    "img", "zonaSalida", "zonaLlegada")

admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Zona, ZonaAdmin)
admin.site.register(Tour, TourAdmin)
