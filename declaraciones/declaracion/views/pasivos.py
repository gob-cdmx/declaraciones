import uuid
from django.urls import reverse_lazy, resolve
from django.views import View
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from declaracion.models import (Declaraciones, SeccionDeclaracion, DeudasOtros,
                                Secciones, SeccionDeclaracion)
from declaracion.forms import (ObservacionesForm, DomiciliosForm, DeudasForm,
                               DeudasOtrosForm, InfoPersonalVarForm)
from .utils import (guardar_estatus, no_aplica, declaracion_datos,
                    validar_declaracion,obtiene_avance)
from .declaracion import (DeclaracionDeleteView)


class DeudasDeleteView(DeclaracionDeleteView):
    model = DeudasOtros


class DeudasView(View):
    template_name = 'declaracion/pasivos/deudas.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0,None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        kwargs['cat_tipos_pasivos'] = 1
        agregar, editar_id, deudas_data, informacion_registrada = (
            declaracion_datos(kwargs, DeudasOtros, declaracion)
        )

        if deudas_data:
            observaciones_data = deudas_data.observaciones
            acreedor_infopersonalvar = deudas_data.acreedor_infopersonalvar
            if acreedor_infopersonalvar.domicilios:
                domicilio_data = acreedor_infopersonalvar.domicilios
                domicilio_data = model_to_dict(domicilio_data)
            else:
                domicilio_data = {}
            acreedor_infopersonalvar = model_to_dict(acreedor_infopersonalvar)
            observaciones_data = model_to_dict(observaciones_data)
            deudas_data = model_to_dict(deudas_data)
        else:
            observaciones_data = {}
            domicilio_data = {}
            deudas_data = {}
            acreedor_infopersonalvar = {}

        deudas_form = DeudasForm(prefix="deudas",
                                 initial=deudas_data)
        observaciones_form = ObservacionesForm(prefix="observaciones",
                                               initial=observaciones_data)
        domicilio_form = DomiciliosForm(prefix="domicilio",
                                       initial=domicilio_data)
        acreedor_infopersonalvar_form = InfoPersonalVarForm(
            prefix="acreedor_infopersonalvar",
            initial=acreedor_infopersonalvar)

        return render(request, self.template_name, {
            'deudas_form': deudas_form,
            'observaciones_form': observaciones_form,
            'domicilio_form': domicilio_form,
            'acreedor_infopersonalvar_form': acreedor_infopersonalvar_form,
            'folio_declaracion': folio_declaracion,
            'avance':avance,
            'faltas':faltas,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id
        })

    @method_decorator(login_required(login_url='/login'))
    def post(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
        except:
            raise Http404()

        kwargs['cat_tipos_pasivos'] = 1
        agregar, editar_id, deudas_data, informacion_registrada = (
            declaracion_datos(kwargs, DeudasOtros, declaracion)
        )
        if deudas_data:
            observaciones_data = deudas_data.observaciones
            acreedor_infopersonalvar = deudas_data.acreedor_infopersonalvar
            if acreedor_infopersonalvar.domicilios:
                domicilio_data = acreedor_infopersonalvar.domicilios
            else:
                domicilio_data = None
        else:
            observaciones_data = None
            domicilio_data = None
            deudas_data = None
            acreedor_infopersonalvar = None

        deudas_form = DeudasForm(request.POST, prefix="deudas",
                                 instance=deudas_data)
        observaciones_form = ObservacionesForm(request.POST,
                                               prefix="observaciones",
                                               instance=observaciones_data)
        domicilio_form = DomiciliosForm(request.POST,
                                       prefix="domicilio",
                                       instance=domicilio_data)
        acreedor_infopersonalvar_form = InfoPersonalVarForm(
            request.POST,
            prefix="acreedor_infopersonalvar",
            instance=acreedor_infopersonalvar)

        deudas_is_valid = deudas_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()
        domicilio_is_valid = domicilio_form.is_valid()
        acreedor_infopersonalvar_is_valid = acreedor_infopersonalvar_form.is_valid()


        if (deudas_is_valid and
            observaciones_is_valid and
            domicilio_is_valid and
            acreedor_infopersonalvar_is_valid):


            deudas = deudas_form.save(commit=False)
            observaciones = observaciones_form.save()
            domicilio = domicilio_form.save()

            acreedor_infopersonalvar = acreedor_infopersonalvar_form.save(commit=False)
            acreedor_infopersonalvar.declaraciones = declaracion
            acreedor_infopersonalvar.domicilios = domicilio
            acreedor_infopersonalvar.save()

            deudas.acreedor_infopersonalvar = acreedor_infopersonalvar
            deudas.declaraciones = declaracion
            deudas.cat_tipos_pasivos_id = 1
            deudas.observaciones = observaciones
            deudas.save()

            if not agregar and not editar_id:
                status_obj, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA,
                    aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:deudas-agregar', folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return redirect('declaracion:deudas-otros',
                            folio=folio_declaracion)

        return render(request, self.template_name, {
            'deudas_form': deudas_form,
            'observaciones_form': observaciones_form,
            'domicilio_form': domicilio_form,
            'folio_declaracion': folio_declaracion,
            'acreedor_infopersonalvar_form': acreedor_infopersonalvar_form,
            'avance':declaracion.avance,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id
        })


class DeudasOtrosDeleteView(DeclaracionDeleteView):
    model = DeudasOtros


class DeudasOtrosView(View):
    template_name = 'declaracion/pasivos/deudas-otros.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0,None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)

        except:
            raise Http404()

        kwargs['cat_tipos_pasivos'] = 2
        agregar, editar_id, deudas_otros_data, informacion_registrada = (
            declaracion_datos(kwargs, DeudasOtros, declaracion)
        )
        if deudas_otros_data:
            observaciones_data = deudas_otros_data.observaciones
            acreedor_infopersonalvar = deudas_otros_data.acreedor_infopersonalvar
            if acreedor_infopersonalvar.domicilios:
                domicilio_data = acreedor_infopersonalvar.domicilios
                domicilio_data = model_to_dict(domicilio_data)
            else:
                domicilio_data = {}
            acreedor_infopersonalvar = model_to_dict(acreedor_infopersonalvar)
            observaciones_data = model_to_dict(observaciones_data)
            deudas_otros_data = model_to_dict(deudas_otros_data)
        else:
            observaciones_data = {}
            domicilio_data = {}
            deudas_otros_data = {}
            acreedor_infopersonalvar = {}

        deudas_otros_form = DeudasOtrosForm(
            prefix="deudas_otros",
            initial=deudas_otros_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)
        domicilio_form = DomiciliosForm(
            prefix="domicilio",
            initial=domicilio_data)
        acreedor_infopersonalvar_form = InfoPersonalVarForm(
            prefix="acreedor_infopersonalvar",
            initial=acreedor_infopersonalvar)


        return render(request, self.template_name, {
            'deudas_otros_form': deudas_otros_form,
            'observaciones_form': observaciones_form,
            'domicilio_form': domicilio_form,
            'acreedor_infopersonalvar_form': acreedor_infopersonalvar_form,
            'folio_declaracion': folio_declaracion,
            'avance':avance,
            'faltas':faltas,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id
        })

    @method_decorator(login_required(login_url='/login'))
    def post(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
        except:
            raise Http404()

        kwargs['cat_tipos_pasivos'] = 2
        agregar, editar_id, deudas_otros_data, informacion_registrada = (
            declaracion_datos(kwargs, DeudasOtros, declaracion)
        )
        if deudas_otros_data:
            observaciones_data = deudas_otros_data.observaciones
            acreedor_infopersonalvar = deudas_otros_data.acreedor_infopersonalvar
            if acreedor_infopersonalvar.domicilios:
                domicilio_data = acreedor_infopersonalvar.domicilios
            else:
                domicilio_data = None
        else:
            observaciones_data = None
            domicilio_data = None
            deudas_otros_data = None
            acreedor_infopersonalvar = None

        deudas_otros_form = DeudasOtrosForm(
            request.POST,
            prefix="deudas_otros",
            instance=deudas_otros_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)
        domicilio_form = DomiciliosForm(
            request.POST,
            prefix="domicilio",
            instance=domicilio_data)
        acreedor_infopersonalvar_form = InfoPersonalVarForm(
            request.POST,
            prefix="acreedor_infopersonalvar",
            instance=acreedor_infopersonalvar)

        deudas_otros_is_valid = deudas_otros_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()
        domicilio_is_valid = domicilio_form.is_valid()
        acreedor_infopersonalvar_is_valid = acreedor_infopersonalvar_form.is_valid()


        if (deudas_otros_is_valid and
            observaciones_is_valid and
            domicilio_is_valid and
            acreedor_infopersonalvar_is_valid):

            deudas = deudas_otros_form.save(commit=False)
            observaciones = observaciones_form.save()
            domicilio = domicilio_form.save()

            acreedor_infopersonalvar = acreedor_infopersonalvar_form.save(commit=False)
            acreedor_infopersonalvar.declaraciones = declaracion
            acreedor_infopersonalvar.domicilios = domicilio
            acreedor_infopersonalvar.save()

            deudas.acreedor_infopersonalvar = acreedor_infopersonalvar
            deudas.declaraciones = declaracion
            deudas.cat_tipos_pasivos_id = 2
            deudas.observaciones = observaciones
            deudas.save()

            if not agregar and not editar_id:
                status_obj, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA,
                    aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:deudas-otros-agregar', folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return redirect('declaracion:pasivos-observaciones',
                            folio=folio_declaracion)

        return render(request, self.template_name, {
            'deudas_otros_form': deudas_otros_form,
            'observaciones_form': observaciones_form,
            'domicilio_form': domicilio_form,
            'acreedor_infopersonalvar_form': acreedor_infopersonalvar_form,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id
        })


class PasivosObservacionesView(View):
    template_name = 'declaracion/pasivos/observaciones.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0,None #obtiene_avance(declaracion)
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        current_url = resolve(request.path_info).url_name
        seccion_id = Secciones.objects.filter(url=current_url).first()
        seccion = SeccionDeclaracion.objects.filter(declaraciones=declaracion, seccion=seccion_id).first()
        if seccion:
            observaciones_data = seccion.observaciones
            observaciones_data = model_to_dict(observaciones_data)
        else:
            observaciones_data = {}

        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)

        return render(request, self.template_name, {
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'avance':avance,
            'faltas':faltas
        })

    @method_decorator(login_required(login_url='/login'))
    def post(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']

        try:
            declaracion = validar_declaracion(request, folio_declaracion)
        except:
            raise Http404()

        current_url = resolve(request.path_info).url_name
        seccion_id = Secciones.objects.filter(url=current_url).first()
        seccion = SeccionDeclaracion.objects.filter(declaraciones=declaracion, seccion=seccion_id).first()

        if seccion:
            observaciones_data = seccion.observaciones
        else:
            observaciones_data = None

        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)

        observaciones_is_valid = observaciones_form.is_valid()

        if observaciones_is_valid:


            status_obj, status_created = guardar_estatus(request,
                                                         declaracion.folio,
                                                         SeccionDeclaracion.COMPLETA,
                                                         aplica=no_aplica(request))
            observaciones = observaciones_form.save()
            status_obj.observaciones = observaciones
            status_obj.save()

            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return redirect('declaracion:confirmacion-informacion-personal',
                            folio=folio_declaracion)

        return render(request, self.template_name, {
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance
        })
