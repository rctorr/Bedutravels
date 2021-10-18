from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Tour, Zona

from .serializers import ZonaSerializer, TourSerializer
from rest_framework import viewsets

# Bedutravels/tours/views.py

# Create your views here.
@login_required()
def index(request, msg=""):
   """ Atiende la petición GET / """
   tours = Tour.objects.all()
   es_operador = request.user.groups.filter(name="operador").exists()

   return render(request, "tours/index.html",
      {
         "tours":tours,
         "es_operador":es_operador,
         "msg":msg,
      }
   )

@login_required()
def tour_agregar(request):
   """ Atiende las peticiones GET y POST /tour/agregar/ """

   zonas = Zona.objects.all()
   es_operador = request.user.groups.filter(name="operador").exists()
   if es_operador:
      if request.method == "POST":
         nombre_form = request.POST.get("nombre")
         slug_form = request.POST.get("slug", None)
         tipoDeTour_form = request.POST.get("tipoDeTour", None)
         descripcion_form = request.POST.get("descripcion")
         img_form = request.POST.get("img", None)
         pais_form = request.POST.get("pais", None)
         zonaSalida_id_form = request.POST.get("zonaSalida", None)
         zonaSalida_obj = Zona.objects.get(pk=zonaSalida_id_form)
         zonaLlegada_id_form = request.POST.get("zonaLlegada", None)
         zonaLlegada_obj = Zona.objects.get(pk=zonaLlegada_id_form)
         tour = Tour(
            nombre=nombre_form,
            slug=slug_form,
            tipoDeTour=tipoDeTour_form,
            descripcion=descripcion_form,
            img=img_form,
            pais=pais_form,
            zonaSalida=zonaSalida_obj,
            zonaLlegada=zonaLlegada_obj,
            operador=request.user.username,
         )
         tour.save()
         msg = "El Tour ha sido guardado exitosamente!"

         return index(request, msg)

      return render(request, "tours/tour_agregar.html",
         {
            "zonas":zonas,
         }
      )
   else:
      raise Http404("El Tour no existe")

@login_required()
def tour_eliminar(request, id_tour):
   """ Atiende las peticiones GET /tour/eliminar/id_tour """
   tour_obj = Tour.objects.get(pk=id_tour)
   tour_obj.delete()

   return redirect("/")


# Vistas basadas en clases para Django Rest
class ZonaViewSet(viewsets.ModelViewSet):
   """
   API que permite realizar operaciones en la tabla Zona
   """
   # Se define el conjunto de datos sobre el que va a operar la vista,
   # en este caso sobre todos las Zonas disponibles.
   queryset = Zona.objects.all().order_by('id')
   # Se define el Serializador encargado de transformar la peticiones
   # en formato JSON a objetos de Django y de Django a JSON.
   serializer_class = ZonaSerializer


class TourViewSet(viewsets.ModelViewSet):
   """
   API que permite realizar operaciones en la tabla Tour
   """
   # Se define el conjunto de datos sobre el que va a operar la vista,
   # en este caso sobre todos los tours disponibles.
   queryset = Tour.objects.all().order_by('id')
   # Se define el Serializador encargado de transformar la peticiones
   # en formato JSON a objetos de Django y de Django a JSON.
   serializer_class = TourSerializer

