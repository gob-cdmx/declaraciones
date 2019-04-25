from django.urls import path

from declaracion.views import (RegistroView,PerfilView)

urlpatterns = [

    path('nuevo', RegistroView.as_view(),
         name='nuevo'),
    path('perfil', PerfilView.as_view(),
         name='perfil'),

]
