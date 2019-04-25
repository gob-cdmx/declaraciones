from django.urls import path, re_path

from declaracion.views import  RegistrosView
urlpatterns = [

    path('', RegistrosView.as_view(),
         name='api'),
]