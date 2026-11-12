from django.urls import path
from . import views

# Aqui se defina la ubicacion de cada pagina
urlpatterns = [
    #path('', views.base, name="base"),
    #path('', views.home, name="home"),
    path('', views.login, name="login"),
    path('logout/', views.logout_view, name='logout'),

    path('clinico/', views.clinico, name='clinico'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('upload/', views.upload, name='upload'),
    path('paciente/', views.paciente, name='paciente'),
    path('examenes/deshabilitar/<int:examen_id>/', views.deshabilitar_examen, name='deshabilitar_examen'),
    path('examenes/habilitar/<int:examen_id>/', views.habilitar_examen, name='habilitar_examen'),
]