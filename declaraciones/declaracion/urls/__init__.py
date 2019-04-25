from django.urls import include, path
from django.conf.urls import url

app_name = 'declaracion'
urlpatterns = [
    path('', include('declaracion.urls.declaracion')),
    path('informacion-personal/', include('declaracion.urls.informacion_personal')),
    path('intereses/', include('declaracion.urls.intereses')),
    path('pasivos/', include('declaracion.urls.pasivos')),
    path('ingresos/', include('declaracion.urls.ingresos')),
    path('activos/', include('declaracion.urls.activos')),
    path('registro/', include('declaracion.urls.registro')),
    path('api/', include('declaracion.urls.api')),
    path('confirmacion/', include('declaracion.urls.confirmacion')),
    path('admin/', include('declaracion.urls.admin')),
]
