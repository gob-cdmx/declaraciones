from django.urls import path, re_path
from declaracion.views import (DeclaracionFormView, DatosCurricularesView,
                               DatosEncargoActualView, ExperienciaLaboralView,
                               ConyugeDependientesView,
                               InformacionPersonalObservacionesView,
                               DatosCurricularesDelete,
                               ExperienciaLaboralDeleteView,
                               ConyugeDependientesDeleteView)
from django.views.generic import TemplateView

urlpatterns = [
    re_path(r'^informacion-general/(?P<cat_tipos_declaracion>[0-9])/$', DeclaracionFormView.as_view(),
         name='informacion-general'),
    re_path(r'^informacion-general/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
            DeclaracionFormView.as_view(),
            name='informacion-general'),
    re_path(r'^datos-curriculares/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
            DatosCurricularesView.as_view(),
            name='datos-curriculares'),
    re_path(r'^datos-curriculares/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
            DatosCurricularesView.as_view(), {'agregar': True},
            name='datos-curriculares-agregar'),
    re_path(r'^datos-curriculares/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
            DatosCurricularesView.as_view(),
            name='datos-curriculares-editar'),
    re_path(r'^datos-curriculares/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
            DatosCurricularesDelete.as_view(),
            name='datos-curriculares-borrar'),
    re_path(r'^datos-del-encargo-actual/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
            DatosEncargoActualView.as_view(),
            name='datos-del-encargo-actual'),
    re_path(r'^experiencia-laboral/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
            ExperienciaLaboralView.as_view(),
            name='experiencia-laboral'),
    re_path(r'^experiencia-laboral/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
            ExperienciaLaboralView.as_view(), {'agregar': True},
            name='experiencia-laboral-agregar'),
    re_path(r'^experiencia-laboral/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
            ExperienciaLaboralView.as_view(),
            name='experiencia-laboral-editar'),
    re_path(r'^experiencia-laboral/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
            ExperienciaLaboralDeleteView.as_view(),
            name='experiencia-laboral-borrar'),
    re_path(r'^dependientes-economicos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
            ConyugeDependientesView.as_view(),
            name='dependientes-economicos'),
    re_path(r'^dependientes-economicos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/agregar/$',
            ConyugeDependientesView.as_view(), {'agregar': True},
            name='dependientes-economicos-agregar'),
    re_path(r'^dependientes-economicos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/editar/(?P<pk>\d+)/$',
            ConyugeDependientesView.as_view(),
            name='dependientes-economicos-editar'),
    re_path(r'^dependientes-economicos/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/borrar/(?P<pk>\d+)/$',
            ConyugeDependientesDeleteView.as_view(),
            name='dependientes-economicos-borrar'),
    re_path(r'observaciones/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
         InformacionPersonalObservacionesView.as_view(),
         name='informacion-personal-observaciones')
]