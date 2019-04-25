from django.urls import path

from declaracion.views import (BusquedaDeclarantesFormView, InfoDeclarantesFormView, InfoDeclaracionFormView,
                               BusquedaDeclaracionesFormView, BusquedaUsuariosFormView, NuevoUsuariosFormView,
                               EliminarUsuarioFormView,InfoUsuarioFormView,EditarUsuarioFormView)

urlpatterns = [

    path('busqueda-declarantes', BusquedaDeclarantesFormView.as_view(),
         name='busqueda-declarantes'),
    path('busqueda-declaraciones', BusquedaDeclaracionesFormView.as_view(),
         name='busqueda-declaraciones'),
    path('busqueda-usuarios', BusquedaUsuariosFormView.as_view(),
         name='busqueda-usuarios'),
    path('info-declarante/<int:pk>/', InfoDeclarantesFormView.as_view(),
         name='info-declarante'),
    path('info-usuario/<int:pk>/', InfoUsuarioFormView.as_view(),
         name='info-usuario'),
    path('eliminar-usuario/<int:pk>/', EliminarUsuarioFormView.as_view(),
         name='eliminar-usuario'),
    path('editar-usuario/<int:pk>/', EditarUsuarioFormView.as_view(),
         name='editar-usuario'),

    path('nuevo-usuario', NuevoUsuariosFormView.as_view(),
         name='nuevo-usuario'),
    path('info-declaracion/<int:pk>/', InfoDeclaracionFormView.as_view(),
         name='info-declaracion'),
]
