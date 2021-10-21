from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Tour, Zona, Perfil

from .serializers import ZonaSerializer, TourSerializer
from rest_framework import viewsets

# Bedutravels/tours/views.py

# Create your views here.
def registro(request):
   """ Atiende las peticiones GET y POST /registro/ """
   if request.POST:
      username = request.POST.get("username")
      first_name = request.POST.get("first_name", None)
      last_name = request.POST.get("last_name", None)
      email = request.POST.get("email", None)
      fechaNacimiento = request.POST.get("fechaNacimiento", None)
      if fechaNacimiento == "":
         fechaNacimiento = None
      tipo = request.POST.get("tipo", None)
      genero = request.POST.get("genero")
      password1 = request.POST.get("password1")
      password2 = request.POST.get("password2")

      if password1 == password2:
         # User
         user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
         )
         user.set_password(password1)
         user.save()
         # Perfil
         perfil = Perfil(
            user=user,
            fecha_nacimiento=fechaNacimiento,
            tipo=tipo,
            genero=genero
         )
         perfil.save()

         return redirect("/")
      else:
         msg = "Error: Las claves tienen que ser idénticas"
   else:
      # Estamos atendiendo el método GET
      msg = ""

   return render(request, "registration/registro.html",
      {
         "msg":msg,
         "lista_generos":Perfil.GENERO,
      }
   )

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
         if request.FILES:
            img_file = request.FILES["img"]
         else:
            img_file = None
         pais_form = request.POST.get("pais", None)
         zonaSalida_id_form = request.POST.get("zonaSalida", None)
         zonaSalida_obj = Zona.objects.get(pk=zonaSalida_id_form)
         zonaLlegada_id_form = request.POST.get("zonaLlegada", None)
         zonaLlegada_obj = Zona.objects.get(pk=zonaLlegada_id_form)
         tour = Tour(
            user=request.user,
            nombre=nombre_form,
            slug=slug_form,
            tipoDeTour=tipoDeTour_form,
            descripcion=descripcion_form,
            pais=pais_form,
            zonaSalida=zonaSalida_obj,
            zonaLlegada=zonaLlegada_obj,
            operador=request.user.username,
         )
         tour.save()  # genera un id para la instancia del tour
         tour.img=img_file
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

@login_required()
def tour_modificar(request, id_tour):
   """ Atiende las peticiones GET y POST /tour/modificar/id_tour/ """
   tour_obj = Tour.objects.get(pk=id_tour)
   zonas = Zona.objects.all()
   es_operador = request.user.groups.filter(name="operador").exists()
   if es_operador:
      if request.method == "POST":
         nombre_form = request.POST.get("nombre")
         slug_form = request.POST.get("slug", None)
         tipoDeTour_form = request.POST.get("tipoDeTour", None)
         descripcion_form = request.POST.get("descripcion")
         if request.FILES:
            img_file = request.FILES["img"]
         else:
            img_file = None
         pais_form = request.POST.get("pais", None)
         zonaSalida_id_form = request.POST.get("zonaSalida", None)
         zonaSalida_obj = Zona.objects.get(pk=zonaSalida_id_form)
         zonaLlegada_id_form = request.POST.get("zonaLlegada", None)
         zonaLlegada_obj = Zona.objects.get(pk=zonaLlegada_id_form)

         tour_obj.nombre=nombre_form
         tour_obj.slug=slug_form
         tour_obj.tipoDeTour=tipoDeTour_form
         tour_obj.descripcion=descripcion_form
         tour_obj.img=img_file
         tour_obj.pais=pais_form
         tour_obj.zonaSalida=zonaSalida_obj
         tour_obj.zonaLlegada=zonaLlegada_obj
         tour_obj.save()

         msg = "El Tour ha sido modificado exitosamente!"

         return index(request, msg)

      return render(request, "tours/tour_modificar.html",
         {
            "zonas":zonas,
            "tour":tour_obj,
         }
      )
   else:
      raise Http404("El Tour no existe")


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

