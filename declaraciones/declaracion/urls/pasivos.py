from django.urls import path, re_path
from declaracion.views import (DeudasView, DeudasOtrosView,
                               PasivosObservacionesView, DeudasDeleteView,
                               DeudasOtrosDeleteView)

urlpatterns = [
    re_path(r'^deudas/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
            DeudasView.as_view(),
            name='deudas'),
    re_path(r'^deudas/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
            DeudasView.as_view(), {'agregar': True},
            name='deudas-agregar'),
    re_path(r'^deudas/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
            DeudasView.as_view(),
            name='deudas-editar'),
    re_path(r'^deudas/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
            DeudasDeleteView.as_view(),
            name='deudas-borrar'),
    re_path(r'^deudas-otros/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
            DeudasOtrosView.as_view(),
            name='deudas-otros'),
    re_path(r'^deudas-otros/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
            DeudasOtrosView.as_view(), {'agregar': True},
            name='deudas-otros-agregar'),
    re_path(r'^deudas-otros/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
            DeudasOtrosView.as_view(),
            name='deudas-otros-editar'),
    re_path(r'^deudas-otros/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
            DeudasOtrosDeleteView.as_view(),
            name='deudas-otros-borrar'),
    re_path(r'observaciones/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
         PasivosObservacionesView.as_view(),
         name='pasivos-observaciones')
]
