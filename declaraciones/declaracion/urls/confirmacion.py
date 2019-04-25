from django.urls import re_path

from declaracion.views import (ConfimacionInformacionPersonalView,
                           ConfimacionInteresesView, ConfimacionPasivosView,
                           ConfimacionIngresosView, ConfimacionActivosView,
                           ConfirmarDeclaracionView)

urlpatterns = [
    re_path(r'^informacion-personal/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
         ConfimacionInformacionPersonalView.as_view(),
         name="confirmacion-informacion-personal"),
    re_path(r'^intereses/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
         ConfimacionInteresesView.as_view(),
         name="confirmacion-intereses"),
    re_path(r'^pasivos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
         ConfimacionPasivosView.as_view(),
         name="confirmacion-pasivos"),
    re_path(r'^ingresos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
         ConfimacionIngresosView.as_view(),
         name="confirmacion-ingresos"),
    re_path(r'^activos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
         ConfimacionActivosView.as_view(),
         name="confirmacion-activos"),
    re_path(r'^confirmar-declaracion/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
         ConfirmarDeclaracionView.as_view(),
         name="confirmar-declaracion"),
]
