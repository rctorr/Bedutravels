from django.contrib.auth import views as auth_views
from django.urls import path
from graphene_django.views import GraphQLView

from . import views

urlpatterns = [
	path('', views.index, name="index"),
    path('tour/agregar/', views.tour_agregar, name="tour_agregar"),
    path('tour/eliminar/<int:id_tour>/', views.tour_eliminar, name="tour_eliminar"),
    path('tour/modificar/<int:id_tour>/', views.tour_modificar, name="tour_modificar"),
    path("login/",
    	auth_views.LoginView.as_view(template_name="registration/login.html"),
    	name="login"),
    path("logout/",
        auth_views.LogoutView.as_view(next_page="/"),
        name="logout"),
    path("registro/", views.registro, name="registro"),
    path('api/graphql/', GraphQLView.as_view(graphiql=True)),
]
