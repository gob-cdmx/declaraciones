from django.urls import path, re_path

from declaracion.views import (BienesMueblesView, BienesInmueblesView,
                               MueblesNoRegistrablesView, InversionesView,
                               EfectivoMetalesView, FideicomisosView,
                               BienesIntangiblesView, CuentasPorCobrarView,
                               BeneficiosEspecieView, ActivosObservacionesView,
                               BienesInmueblesDeleteView, BienesMueblesDeleteView,
                               MueblesNoRegistrablesDeleteView,
                               InversionesDeleteView,
                               EfectivoMetalesDeleteView,
                               FideicomisosDeleteView,
                               BienesIntangiblesDeleteView,
                               CuentasPorCobrarDeleteView,
                               BeneficiosEspecieDeleteView)

urlpatterns = [
    re_path(
        r'^bienes-inmuebles/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
        BienesInmueblesView.as_view(), name='bienes-inmuebles'),
    re_path(
        r'^bienes-inmuebles/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
        BienesInmueblesView.as_view(), {'agregar': True}, name='bienes-inmuebles-agregar'),
    re_path(
        r'^bienes-inmuebles/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
        BienesInmueblesView.as_view(), name='bienes-inmuebles-editar'),
    re_path(
        r'^bienes-inmuebles/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
        BienesInmueblesDeleteView.as_view(), name='bienes-inmuebles-borrar'),
    re_path(
        r'^bienes-muebles/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
        BienesMueblesView.as_view(), name='bienes-muebles'),
    re_path(
        r'^bienes-muebles/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
        BienesMueblesView.as_view(), {'agregar': True}, name='bienes-muebles-agregar'),
    re_path(
        r'^bienes-muebles/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
        BienesMueblesView.as_view(), name='bienes-muebles-editar'),
    re_path(
        r'^bienes-muebles/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
        BienesMueblesDeleteView.as_view(), name='bienes-muebles-borrar'),
    re_path(
        r'^muebles-noregistrables/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
        MueblesNoRegistrablesView.as_view(), name='muebles-noregistrables'),
    re_path(
        r'^muebles-noregistrables/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
        MueblesNoRegistrablesView.as_view(), {'agregar': True}, name='muebles-noregistrables-agregar'),
    re_path(
        r'^muebles-noregistrables/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
        MueblesNoRegistrablesView.as_view(), name='muebles-noregistrables-editar'),
    re_path(
        r'^muebles-noregistrables/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
        MueblesNoRegistrablesDeleteView.as_view(), name='muebles-noregistrables-borrar'),
    re_path(
        r'^inversiones/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
        InversionesView.as_view(), name='inversiones'),
    re_path(
        r'^inversiones/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
        InversionesView.as_view(), {'agregar': True}, name='inversiones-agregar'),
    re_path(
        r'^inversiones/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
        InversionesView.as_view(), name='inversiones-editar'),
    re_path(
        r'^inversiones/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
        InversionesDeleteView.as_view(), name='inversiones-borrar'),
    re_path(
        r'^efectivo-metales/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
        EfectivoMetalesView.as_view(), name='efectivo-metales'),
    re_path(
        r'^efectivo-metales/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
        EfectivoMetalesView.as_view(), {'agregar': True}, name='efectivo-metales-agregar'),
    re_path(
        r'^efectivo-metales/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
        EfectivoMetalesView.as_view(), name='efectivo-metales-editar'),
    re_path(
        r'^efectivo-metales/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
        EfectivoMetalesDeleteView.as_view(), name='efectivo-metales-borrar'),
    re_path(
        r'^fideicomisos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
        FideicomisosView.as_view(), name='fideicomisos'),
    re_path(
        r'^fideicomisos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
        FideicomisosView.as_view(), {'agregar': True}, name='fideicomisos-agregar'),
    re_path(
        r'^fideicomisos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
        FideicomisosView.as_view(), name='fideicomisos-editar'),
    re_path(
        r'^fideicomisos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
        FideicomisosDeleteView.as_view(), name='fideicomisos-borrar'),
    re_path(
        r'^bienes-intangibles/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
        BienesIntangiblesView.as_view(), name='bienes-intangibles'),
    re_path(
        r'^bienes-intangibles/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
        BienesIntangiblesView.as_view(), {'agregar': True}, name='bienes-intangibles-agregar'),
    re_path(
        r'^bienes-intangibles/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
        BienesIntangiblesView.as_view(), name='bienes-intangibles-editar'),
    re_path(
        r'^bienes-intangibles/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
        BienesIntangiblesDeleteView.as_view(), name='bienes-intangibles-borrar'),
    re_path(
        r'^cuentas-por-cobrar/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
        CuentasPorCobrarView.as_view(), name='cuentas-por-cobrar'),
    re_path(
        r'^cuentas-por-cobrar/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
        CuentasPorCobrarView.as_view(), {'agregar': True}, name='cuentas-por-cobrar-agregar'),
    re_path(
        r'^cuentas-por-cobrar/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
        CuentasPorCobrarView.as_view(), name='cuentas-por-cobrar-editar'),
    re_path(
        r'^cuentas-por-cobrar/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
        CuentasPorCobrarDeleteView.as_view(), name='cuentas-por-cobrar-borrar'),
    re_path(
        r'^beneficios-especie/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
        BeneficiosEspecieView.as_view(), name='beneficios-especie'),
    re_path(
        r'^beneficios-especie/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
        BeneficiosEspecieView.as_view(), {'agregar': True}, name='beneficios-especie-agregar'),
    re_path(
        r'^beneficios-especie/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
        BeneficiosEspecieView.as_view(), name='beneficios-especie-editar'),
    re_path(
        r'^beneficios-especie/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
        BeneficiosEspecieDeleteView.as_view(), name='beneficios-especie-borrar'),
    re_path(r'observaciones/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
         ActivosObservacionesView.as_view(),
         name='activos-observaciones')
]
