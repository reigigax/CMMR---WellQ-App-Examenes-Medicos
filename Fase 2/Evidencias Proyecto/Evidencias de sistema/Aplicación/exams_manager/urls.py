from django.urls import path
from . import views

# Aqui se defina la ubicacion de cada pagina
urlpatterns = [
    path('', views.base, name="base"),
    path("", views.home, name="home"),
    path("clinico/", views.clinico, name="clinico"),
    path('login/', views.login, name="login"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('upload/', views.upload, name="upload"),
    path("paciente/", views.paciente, name="paciente"),
]