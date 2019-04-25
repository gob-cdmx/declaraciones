from django.urls import path, re_path
from declaracion.views import (EmpresasSociedadesView, MembresiaView,
                               RepresentacionesActivasView,
                               RepresentacionesPasivasView,
                               SociosComercialesView, ClientesPrincipalesView,
                               OtrasPartesFormView, BeneficiosGratuitosView,
                               ApoyosView, InteresesObservacionesView,
                               EmpresasSociedadesDeleteView,
                               MembresiaDeleteView,
                               SociosComercialesDeleteView,
                               ClientesPrincipalesDeleteView,
                               OtrasPartesFormDeleteView,
                               BeneficiosGratuitosDeleteView,
                               ApoyosDeleteView,
                               RepresentacionesActivasDeleteView,
                               RepresentacionesPasivasDeleteView)
from django.views.generic import TemplateView

urlpatterns = [
    re_path(r'^empresas-sociedades-asociaciones/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
            EmpresasSociedadesView.as_view(),
            name='empresas-sociedades-asociaciones'),
    re_path(r'^empresas-sociedades-asociaciones/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
            EmpresasSociedadesView.as_view(), {'agregar': True},
            name='empresas-sociedades-asociaciones-agregar'),
    re_path(r'^empresas-sociedades-asociaciones/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
            EmpresasSociedadesView.as_view(),
            name='empresas-sociedades-asociaciones-editar'),
    re_path(r'^empresas-sociedades-asociaciones/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
            EmpresasSociedadesDeleteView.as_view(),
            name='empresas-sociedades-asociaciones-borrar'),
    re_path(r'^membresias/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
            MembresiaView.as_view(),
            name='membresias'),
    re_path(r'^membresias/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
            MembresiaView.as_view(), {'agregar': True},
            name='membresias-agregar'),
    re_path(r'^membresias/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
            MembresiaView.as_view(),
            name='membresias-editar'),
    re_path(r'^membresias/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
            MembresiaDeleteView.as_view(),
            name='membresias-borrar'),
    re_path(r'^apoyos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
            ApoyosView.as_view(),
            name='apoyos'),
    re_path(r'^apoyos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
            ApoyosView.as_view(), {'agregar': True},
            name='apoyos-agregar'),
    re_path(r'^apoyos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
            ApoyosView.as_view(),
            name='apoyos-editar'),
    re_path(r'^apoyos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
            ApoyosDeleteView.as_view(),
            name='apoyos-borrar'),
    re_path(r'^representacion-activa/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
            RepresentacionesActivasView.as_view(),
            name='representacion-activa'),
    re_path(r'^representacion-activa/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
            RepresentacionesActivasView.as_view(), {'agregar': True},
            name='representacion-activa-agregar'),
    re_path(r'^representacion-activa/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
            RepresentacionesActivasView.as_view(),
            name='representacion-activa-editar'),
    re_path(r'^representacion-activa/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
            RepresentacionesActivasDeleteView.as_view(),
            name='representacion-activa-borrar'),
    re_path(r'^representacion-pasiva/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
            RepresentacionesPasivasView.as_view(),
            name='representacion-pasiva'),
    re_path(r'^representacion-pasiva/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
            RepresentacionesPasivasView.as_view(), {'agregar': True},
            name='representacion-pasiva-agregar'),
    re_path(r'^representacion-pasiva/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
            RepresentacionesPasivasView.as_view(),
            name='representacion-pasiva-editar'),
    re_path(r'^representacion-pasiva/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
            RepresentacionesPasivasDeleteView.as_view(),
            name='representacion-pasiva-borrar'),
    re_path(r'^socios-comerciales/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
            SociosComercialesView.as_view(),
            name='socios-comerciales'),
    re_path(r'^socios-comerciales/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
            SociosComercialesView.as_view(), {'agregar': True},
            name='socios-comerciales-agregar'),
    re_path(r'^socios-comerciales/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
            SociosComercialesView.as_view(),
            name='socios-comerciales-editar'),
    re_path(r'^socios-comerciales/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
            SociosComercialesDeleteView.as_view(),
            name='socios-comerciales-borrar'),
    re_path(r'^clientes-principales/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
            ClientesPrincipalesView.as_view(),
            name='clientes-principales'),
    re_path(r'^clientes-principales/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
            ClientesPrincipalesView.as_view(), {'agregar': True},
            name='clientes-principales-agregar'),
    re_path(r'^clientes-principales/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
            ClientesPrincipalesView.as_view(),
            name='clientes-principales-editar'),
    re_path(r'^clientes-principales/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
            ClientesPrincipalesDeleteView.as_view(),
            name='clientes-principales-borrar'),
    re_path(r'^otras-partes-relacionadas/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
            OtrasPartesFormView.as_view(),
            name='otras-partes-relacionadas'),
    re_path(r'^otras-partes-relacionadas/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
            OtrasPartesFormView.as_view(), {'agregar': True},
            name='otras-partes-relacionadas-agregar'),
    re_path(r'^otras-partes-relacionadas/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
            OtrasPartesFormView.as_view(),
            name='otras-partes-relacionadas-editar'),
    re_path(r'^otras-partes-relacionadas/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
            OtrasPartesFormDeleteView.as_view(),
            name='otras-partes-relacionadas-borrar'),
    re_path(r'^beneficios-gratuitos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
            BeneficiosGratuitosView.as_view(),
            name='beneficios-gratuitos'),
    re_path(r'^beneficios-gratuitos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
            BeneficiosGratuitosView.as_view(), {'agregar': True},
            name='beneficios-gratuitos-agregar'),
    re_path(r'^beneficios-gratuitos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
            BeneficiosGratuitosView.as_view(),
            name='beneficios-gratuitos-editar'),
    re_path(r'^beneficios-gratuitos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
            BeneficiosGratuitosDeleteView.as_view(),
            name='beneficios-gratuitos-borrar'),
    re_path(r'observaciones/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
         InteresesObservacionesView.as_view(),
         name='intereses-observaciones')
]
