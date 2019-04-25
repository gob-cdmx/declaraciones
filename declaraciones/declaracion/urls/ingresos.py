from django.urls import path, re_path
from declaracion.views import (SueldosPublicosView, IngresosVariosView,
                               IngresosObservacionesView, IngresosVariosDeleteView)
from django.views.generic import TemplateView

urlpatterns = [

    re_path(r'^publicos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
            SueldosPublicosView.as_view(),
            name='ingresos-publicos'),
    re_path(r'^varios/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/(?P<tipo>[0-9])/$',
            IngresosVariosView.as_view(),
            name="ingresos-varios"),
    re_path(r'^varios/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/(?P<tipo>[0-9])/agregar/$',
            IngresosVariosView.as_view(), {'agregar': True},
            name="ingresos-varios-agregar"),
    re_path(r'^varios/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/(?P<tipo>[0-9])/editar/(?P<pk>\d+)/$',
            IngresosVariosView.as_view(),
            name="ingresos-varios-editar"),
    re_path(r'^varios/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/(?P<tipo>[0-9])/borrar/(?P<pk>\d+)/$',
            IngresosVariosDeleteView.as_view(),
            name="ingresos-varios-borrar"),
    re_path(r'observaciones/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
         IngresosObservacionesView.as_view(),
         name='ingresos-observaciones')

]
