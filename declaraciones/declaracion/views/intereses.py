import uuid
from django.urls import reverse_lazy, resolve
from django.views import View
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, Http404
from declaracion.models import (Declaraciones, SeccionDeclaracion,
                                EmpresasSociedades, Membresias, Apoyos,
                                InfoPersonalVar, Representaciones,
                                SociosComerciales, ClientesPrincipales,
                                OtrasPartes, BeneficiosGratuitos,
                                Secciones, SeccionDeclaracion)
from declaracion.forms import (EmpresasSociedadesForm, ObservacionesForm,
                               DomiciliosForm, MembresiasForm,
                               RepresentacionesActivasForm,
                               RepresentacionesPasivasForm,
                               SociosComercialesForm, ClientesPrincipalesForm,
                               OtrasPartesForm, BeneficiosGratuitosForm,
                               ApoyosForm, InfoPersonalVarForm)
from .utils import (guardar_estatus, no_aplica, declaracion_datos,
                    validar_declaracion,obtiene_avance)
from .declaracion import (DeclaracionDeleteView)
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class EmpresasSociedadesDeleteView(DeclaracionDeleteView):
    model = EmpresasSociedades


class EmpresasSociedadesView(View):
    template_name = 'declaracion/intereses/empresas-sociedades-asociaciones.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0,None

        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        agregar, editar_id, empresas_sociedades_data, informacion_registrada = (
            declaracion_datos(kwargs, EmpresasSociedades, declaracion)
        )

        if empresas_sociedades_data:
            observaciones_data = empresas_sociedades_data.observaciones
            info_personal_var_data = empresas_sociedades_data.empresa_infopersonalvar
            domicilio_data = info_personal_var_data.domicilios
            if domicilio_data:
                domicilio_data = model_to_dict(domicilio_data)
            else:
                domicilio_data = {}
            observaciones_data = model_to_dict(observaciones_data)
            empresas_sociedades_data = model_to_dict(empresas_sociedades_data)
            info_personal_var_data = model_to_dict(info_personal_var_data)
        else:
            observaciones_data = {}
            domicilio_data = {}
            empresas_sociedades_data = {}
            info_personal_var_data = {}

        info_personal_var_form = InfoPersonalVarForm(
            prefix="var",
            initial=info_personal_var_data
        )
        empresas_sociedades_form = EmpresasSociedadesForm(
            prefix="empresas_sociedades",
            initial=empresas_sociedades_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)
        domicilio_form = DomiciliosForm(
            prefix="domicilio",
            initial=domicilio_data)

        return render(request, self.template_name, {
            'empresas_sociedades_form': empresas_sociedades_form,
            'observaciones_form': observaciones_form,
            'info_personal_var_form': info_personal_var_form,
            'domicilio_form': domicilio_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
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

        agregar, editar_id, empresas_sociedades_data, informacion_registrada = (
            declaracion_datos(kwargs, EmpresasSociedades, declaracion)
        )

        if empresas_sociedades_data:
            observaciones_data = empresas_sociedades_data.observaciones
            info_personal_var_data = empresas_sociedades_data.empresa_infopersonalvar
            domicilio_data = info_personal_var_data.domicilios
        else:
            observaciones_data = None
            domicilio_data = None
            empresas_sociedades_data = None
            info_personal_var_data = None

        empresas_sociedades_form = EmpresasSociedadesForm(
            request.POST,
            prefix="empresas_sociedades",
            instance=empresas_sociedades_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)
        domicilio_form = DomiciliosForm(
            request.POST,
            prefix="domicilio",
            instance=domicilio_data)
        info_personal_var_form = InfoPersonalVarForm(
            request.POST,
            prefix="var",
            instance=info_personal_var_data
        )

        empresas_sociedades_is_valid = empresas_sociedades_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()
        domicilio_is_valid = domicilio_form.is_valid()
        info_personal_var_is_valid = info_personal_var_form.is_valid()

        if (empresas_sociedades_is_valid and
            observaciones_is_valid and
            domicilio_is_valid and
            info_personal_var_is_valid):

            empresas_sociedades = empresas_sociedades_form.save(commit=False)
            observaciones = observaciones_form.save()
            domicilio = domicilio_form.save()

            info_personal_var = info_personal_var_form.save(commit=False)
            info_personal_var.declaraciones = declaracion
            info_personal_var.domicilios = domicilio
            info_personal_var.cat_tipo_persona_id = 3
            info_personal_var.save()

            empresas_sociedades.declaraciones = declaracion
            empresas_sociedades.observaciones = observaciones

            declarante_infopersonalvar = InfoPersonalVar.objects.filter(
                declaraciones=declaracion).first()

            empresas_sociedades.declarante_infopersonalvar = declarante_infopersonalvar
            empresas_sociedades.empresa_infopersonalvar = info_personal_var

            empresas_sociedades.save()

            if not agregar and not editar_id:
                status, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA,
                    aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:empresas-sociedades-asociaciones-agregar', folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return HttpResponseRedirect(
                reverse_lazy('declaracion:membresias',
                             args=[folio_declaracion]))

        return render(request, self.template_name, {
            'empresas_sociedades_form': empresas_sociedades_form,
            'observaciones_form': observaciones_form,
            'info_personal_var_form': info_personal_var_form,
            'domicilio_form': domicilio_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
            'avance':declaracion.avance
        })


class MembresiaDeleteView(DeclaracionDeleteView):
    model = Membresias


class MembresiaView(View):
    template_name = 'declaracion/intereses/membresias.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0,None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        agregar, editar_id, membresia_data, informacion_registrada = (
            declaracion_datos(kwargs, Membresias, declaracion)
        )

        if membresia_data:
            observaciones_data = membresia_data.observaciones
            domicilio_data = membresia_data.domicilios
            observaciones_data = model_to_dict(observaciones_data)
            domicilio_data = model_to_dict(domicilio_data)
            membresia_data = model_to_dict(membresia_data)
        else:
            observaciones_data = {}
            domicilio_data = {}
            membresia_data = {}

        membresia_form = MembresiasForm(prefix="membresia",
                                       initial=membresia_data)
        observaciones_form = ObservacionesForm(prefix="observaciones",
                                               initial=observaciones_data)
        domicilio_form = DomiciliosForm(prefix="domicilio",
                                       initial=domicilio_data)

        return render(request, self.template_name, {
            'membresia_form': membresia_form,
            'observaciones_form': observaciones_form,
            'domicilio_form': domicilio_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
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

        agregar, editar_id, membresia_data, informacion_registrada = (
            declaracion_datos(kwargs, Membresias, declaracion)
        )

        if membresia_data:
            observaciones_data = membresia_data.observaciones
            domicilio_data = membresia_data.domicilios
        else:
            observaciones_data = None
            domicilio_data = None
            membresia_data = None

        membresia_form = MembresiasForm(request.POST,
                                       prefix="membresia",
                                       instance=membresia_data)
        observaciones_form = ObservacionesForm(request.POST, prefix="observaciones",
                                               instance=observaciones_data)
        domicilio_form = DomiciliosForm(request.POST, prefix="domicilio",
                                       instance=domicilio_data)

        membresia_is_valid = membresia_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()
        domicilio_is_valid = domicilio_form.is_valid()

        if membresia_is_valid and observaciones_is_valid and domicilio_is_valid:

            membresias = membresia_form.save(commit=False)
            observaciones = observaciones_form.save()
            domicilio = domicilio_form.save()

            membresias.declaraciones = declaracion
            membresias.observaciones = observaciones
            membresias.domicilios = domicilio
            membresias.save()

            if not agregar and not editar_id:
                status, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA,
                    aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:membresias-agregar', folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return HttpResponseRedirect(
                reverse_lazy('declaracion:apoyos',
                             args=[folio_declaracion]))

        return render(request, self.template_name, {
            'membresia_form': membresia_form,
            'observaciones_form': observaciones_form,
            'domicilio_form': domicilio_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
            'avance':declaracion.avance
        })


class ApoyosDeleteView(DeclaracionDeleteView):
    model = Apoyos


class ApoyosView(View):
    template_name = 'declaracion/intereses/apoyos.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0,None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        info_persona_var = InfoPersonalVar.objects.filter(declaraciones=declaracion).first()

        kwargs['beneficiario_infopersonalvar'] = info_persona_var
        agregar, editar_id, apoyos_data, informacion_registrada = (
            declaracion_datos(kwargs, Apoyos, declaracion)
        )

        if apoyos_data:
            observaciones_data = apoyos_data.observaciones
            observaciones_data = model_to_dict(observaciones_data)
            apoyos_data = model_to_dict(apoyos_data)
        else:
            observaciones_data = {}
            apoyos_data = {}

        apoyos_form = ApoyosForm(prefix="apoyos", initial=apoyos_data)
        observaciones_form = ObservacionesForm(prefix="observaciones", initial=observaciones_data)

        return render(request, self.template_name, {
            'apoyos_form': apoyos_form,
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'avance':avance,
            'faltas':faltas,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
        })

    @method_decorator(login_required(login_url='/login'))
    def post(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
        except:
            raise Http404()

        info_persona_var = InfoPersonalVar.objects.filter(declaraciones=declaracion).first()

        agregar, editar_id, apoyos_data, informacion_registrada = (
            declaracion_datos(kwargs, Apoyos, declaracion)
        )

        if apoyos_data:
            observaciones_data = apoyos_data.observaciones
        else:
            observaciones_data = None
            apoyos_data = None

        apoyos_form = ApoyosForm(request.POST, prefix="apoyos",
                                 instance=apoyos_data)
        observaciones_form = ObservacionesForm(request.POST,
                                               prefix="observaciones",
                                               instance=observaciones_data)

        apoyos_is_valid = apoyos_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()

        if apoyos_is_valid and observaciones_is_valid:


            apoyos = apoyos_form.save(commit=False)
            observaciones = observaciones_form.save()

            apoyos.beneficiario_infopersonalvar = info_persona_var
            apoyos.declaraciones = declaracion
            apoyos.observaciones = observaciones
            apoyos.save()

            if not agregar and not editar_id:
                status, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA,
                    aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:apoyos-agregar',
                                folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return HttpResponseRedirect(
                reverse_lazy('declaracion:representacion-activa',
                             args=[folio_declaracion]))

        return render(request, self.template_name, {
            'apoyos_form': apoyos_form,
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id
        })


class RepresentacionesActivasDeleteView(DeclaracionDeleteView):
    model = Representaciones


class RepresentacionesActivasView(View):
    template_name = 'declaracion/intereses/representaciones-activas.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0,None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        kwargs['es_representacion_activa'] = 1
        agregar, editar_id, representaciones_activas_data, informacion_registrada = (
            declaracion_datos(kwargs, Representaciones, declaracion)
        )

        if representaciones_activas_data:
            observaciones_data = representaciones_activas_data.observaciones
            info_personal_var_data = representaciones_activas_data.info_personal_var
            observaciones_data = model_to_dict(observaciones_data)
            representaciones_activas_data = model_to_dict(representaciones_activas_data)
            info_personal_var_data = model_to_dict(info_personal_var_data)
        else:
            observaciones_data = {}
            representaciones_activas_data = {}
            info_personal_var_data = {}

        info_personal_var_form = InfoPersonalVarForm(
            prefix="var",
            initial=info_personal_var_data)
        representaciones_activas_form = RepresentacionesActivasForm(
            prefix="representaciones_activas",
            initial=representaciones_activas_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)

        return render(request, self.template_name, {
            'representaciones_activas_form': representaciones_activas_form,
            'observaciones_form': observaciones_form,
            'info_personal_var_form': info_personal_var_form,
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

        kwargs['es_representacion_activa'] = 1
        agregar, editar_id, representaciones_activas_data, informacion_registrada = (
            declaracion_datos(kwargs, Representaciones, declaracion)
        )

        if representaciones_activas_data:
            observaciones_data = representaciones_activas_data.observaciones
            info_personal_var_data = representaciones_activas_data.info_personal_var
        else:
            observaciones_data = None
            representaciones_activas_data = None
            info_personal_var_data = None

        representaciones_activas_form = RepresentacionesActivasForm(
            request.POST,
            prefix="representaciones_activas",
            instance=representaciones_activas_data)
        info_personal_var_form = InfoPersonalVarForm(
            request.POST,
            prefix="var",
            instance=info_personal_var_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)

        representaciones_activas_is_valid = representaciones_activas_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()
        info_personal_var_is_valid = info_personal_var_form.is_valid()

        if (representaciones_activas_is_valid and
            observaciones_is_valid and info_personal_var_is_valid):

            representaciones_activas = representaciones_activas_form.save(commit=False)
            observaciones = observaciones_form.save()
            info_personal_var = info_personal_var_form.save(commit=False)
            info_personal_var.declaraciones = declaracion
            info_personal_var.save()
            representaciones_activas.declaraciones = declaracion
            representaciones_activas.observaciones = observaciones
            representaciones_activas.info_personal_var = info_personal_var
            representaciones_activas.es_representacion_activa = 1

            representaciones_activas.save()

            if not agregar and not editar_id:
                status, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA,
                    aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:representacion-activa-agregar',
                                folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return HttpResponseRedirect(
                reverse_lazy('declaracion:representacion-pasiva',
                             args=[folio_declaracion]))

        return render(request, self.template_name, {
            'representaciones_activas_form': representaciones_activas_form,
            'observaciones_form': observaciones_form,
            'info_personal_var_form': info_personal_var_form,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id
        })


class RepresentacionesPasivasDeleteView(DeclaracionDeleteView):
    model = Representaciones


class RepresentacionesPasivasView(View):
    template_name = 'declaracion/intereses/representaciones-pasivas.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0,None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)  # 0,None
        except:
            raise Http404()

        kwargs['es_representacion_activa'] = 0
        agregar, editar_id, representaciones_pasivas_data, informacion_registrada = (
            declaracion_datos(kwargs, Representaciones, declaracion)
        )

        if representaciones_pasivas_data:
            observaciones_data = representaciones_pasivas_data.observaciones
            info_personal_var = representaciones_pasivas_data.info_personal_var
            observaciones_data = model_to_dict(observaciones_data)
            representaciones_pasivas_data = model_to_dict(representaciones_pasivas_data)
            info_personal_var = model_to_dict(info_personal_var)
        else:
            observaciones_data = {}
            representaciones_pasivas_data = {}
            info_personal_var = {}

        representaciones_pasivas_form = RepresentacionesPasivasForm(
            prefix="representaciones_pasivas",
            initial=representaciones_pasivas_data)
        info_personal_var_form = InfoPersonalVarForm(
            prefix="var",
            initial=info_personal_var)
        observaciones_form = ObservacionesForm(prefix="observaciones",
                                               initial=observaciones_data)

        return render(request, self.template_name, {
            'representaciones_pasivas_form': representaciones_pasivas_form,
            'observaciones_form': observaciones_form,
            'info_personal_var_form': info_personal_var_form,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance,
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

        kwargs['es_representacion_activa'] = 0
        agregar, editar_id, representaciones_pasivas_data, informacion_registrada = (
            declaracion_datos(kwargs, Representaciones, declaracion)
        )

        if representaciones_pasivas_data:
            observaciones_data = representaciones_pasivas_data.observaciones
            info_personal_var_data = representaciones_pasivas_data.info_personal_var
        else:
            observaciones_data = None
            representaciones_pasivas_data = None
            info_personal_var_data = None

        representaciones_pasivas_form = RepresentacionesPasivasForm(
            request.POST,
            prefix="representaciones_pasivas",
            instance=representaciones_pasivas_data)
        info_personal_var_form = InfoPersonalVarForm(
            request.POST,
            prefix="var",
            instance=info_personal_var_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)

        representaciones_pasivas_is_valid = representaciones_pasivas_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()

        if representaciones_pasivas_is_valid and observaciones_is_valid:

            representaciones_pasivas = representaciones_pasivas_form.save(commit=False)
            observaciones = observaciones_form.save()

            info_personal_var = info_personal_var_form.save(commit=False)
            info_personal_var.declaraciones = declaracion
            info_personal_var.save()
            info_personal_var_form.save_m2m()

            representaciones_pasivas.declaraciones = declaracion
            representaciones_pasivas.observaciones = observaciones
            representaciones_pasivas.info_personal_var = info_personal_var
            representaciones_pasivas.es_representacion_activa = 0

            representaciones_pasivas.save()
            if not agregar and not editar_id:
                status, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA,
                    aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:representacion-pasiva-agregar',
                                folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return HttpResponseRedirect(
                reverse_lazy('declaracion:socios-comerciales',
                             args=[folio_declaracion]))

        return render(request, self.template_name, {
            'representaciones_pasivas_form': representaciones_pasivas_form,
            'observaciones_form': observaciones_form,
            'info_personal_var_form': info_personal_var_form,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id
        })


class SociosComercialesDeleteView(DeclaracionDeleteView):
    model = SociosComerciales


class SociosComercialesView(View):
    template_name = 'declaracion/intereses/socios-comerciales.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0,None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)  # 0,None
        except:
            raise Http404()

        agregar, editar_id, socios_comerciales_data, informacion_registrada = (
            declaracion_datos(kwargs, SociosComerciales, declaracion)
        )

        if socios_comerciales_data:
            observaciones_data = socios_comerciales_data.observaciones
            socio_infopersonalvar_data =  socios_comerciales_data.socio_infopersonalvar
            socio_infopersonalvar_data = model_to_dict(socio_infopersonalvar_data)
            observaciones_data = model_to_dict(observaciones_data)
            socios_comerciales_data = model_to_dict(socios_comerciales_data)
        else:
            observaciones_data = {}
            socios_comerciales_data = {}
            socio_infopersonalvar_data = {}

        socios_comerciales_form = SociosComercialesForm(
            prefix="socios_comerciales",
            initial=socios_comerciales_data)
        socio_infopersonalvar_form = InfoPersonalVarForm(
            prefix="var",
            initial=socio_infopersonalvar_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)

        return render(request, self.template_name, {
            'socios_comerciales_form': socios_comerciales_form,
            'observaciones_form': observaciones_form,
            'socio_infopersonalvar_form': socio_infopersonalvar_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
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

        agregar, editar_id, socios_comerciales_data, informacion_registrada = (
            declaracion_datos(kwargs, SociosComerciales, declaracion)
        )

        if socios_comerciales_data:
            observaciones_data = socios_comerciales_data.observaciones
            socio_infopersonalvar_data = socios_comerciales_data.socio_infopersonalvar
        else:
            observaciones_data = None
            socios_comerciales_data = None
            socio_infopersonalvar_data = None

        socios_comerciales_form = SociosComercialesForm(
            request.POST,
            prefix="socios_comerciales",
            instance=socios_comerciales_data)
        socio_infopersonalvar_form = InfoPersonalVarForm(
            request.POST,
            prefix="var",
            instance=socio_infopersonalvar_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)

        socios_comerciales_is_valid = socios_comerciales_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()
        socio_infopersonalvar_is_valid = socio_infopersonalvar_form.is_valid()

        if (socios_comerciales_is_valid and observaciones_is_valid and
            socio_infopersonalvar_is_valid):

            socios_comerciales = socios_comerciales_form.save(commit=False)
            observaciones = observaciones_form.save()

            socio_infopersonalvar = socio_infopersonalvar_form.save(commit=False)
            socio_infopersonalvar.declaraciones = declaracion
            socio_infopersonalvar.save()

            socios_comerciales.socio_infopersonalvar = socio_infopersonalvar
            socios_comerciales.declaraciones = declaracion
            socios_comerciales.observaciones = observaciones

            if not agregar and not editar_id:
                status, status_created = guardar_estatus(request,
                                                             declaracion.folio,
                                                             SeccionDeclaracion.COMPLETA,
                                                             aplica=no_aplica(request))

            socios_comerciales.save()

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:socios-comerciales-agregar', folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return HttpResponseRedirect(
                reverse_lazy('declaracion:clientes-principales',
                             args=[folio_declaracion]))

        return render(request, self.template_name, {
            'socios_comerciales_form': socios_comerciales_form,
            'observaciones_form': observaciones_form,
            'socio_infopersonalvar_form': socio_infopersonalvar_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
            'avance':declaracion.avance
        })


class ClientesPrincipalesDeleteView(DeclaracionDeleteView):
    model = ClientesPrincipales


class ClientesPrincipalesView(View):
    template_name = 'declaracion/intereses/clientes-principales.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas =  0,None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        agregar, editar_id, clientes_principales_data, informacion_registrada = (
            declaracion_datos(kwargs, ClientesPrincipales, declaracion)
        )

        if clientes_principales_data:
            observaciones_data = clientes_principales_data.observaciones
            info_personal_var_data = clientes_principales_data.info_personal_var
            domicilio_data = info_personal_var_data.domicilios
            if domicilio_data:
                domicilio_data = model_to_dict(domicilio_data)
            else:
                domicilio_data = {}
            info_personal_var_data = model_to_dict(info_personal_var_data)
            observaciones_data = model_to_dict(observaciones_data)
            clientes_principales_data = model_to_dict(clientes_principales_data)
        else:
            observaciones_data = {}
            domicilio_data = {}
            clientes_principales_data = {}
            info_personal_var_data = {}

        clientes_principales_form = ClientesPrincipalesForm(
            prefix="clientes_principales",
            initial=clientes_principales_data)
        info_personal_var_form = InfoPersonalVarForm(
            prefix="var",
            initial=info_personal_var_data)
        domicilio_form = DomiciliosForm(
            prefix="domicilio",
            initial=domicilio_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)

        return render(request, self.template_name, {
            'clientes_principales_form': clientes_principales_form,
            'observaciones_form': observaciones_form,
            'info_personal_var_form': info_personal_var_form,
            'domicilio_form': domicilio_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
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

        agregar, editar_id, clientes_principales_data, informacion_registrada = (
            declaracion_datos(kwargs, ClientesPrincipales, declaracion)
        )

        if clientes_principales_data:
            observaciones_data = clientes_principales_data.observaciones
            info_personal_var_data = clientes_principales_data.info_personal_var
            domicilio_data = info_personal_var_data.domicilios
        else:
            observaciones_data = None
            domicilio_data = None
            clientes_principales_data = None
            info_personal_var_data = None

        clientes_principales_form = ClientesPrincipalesForm(
            request.POST,
            prefix="clientes_principales",
            instance=clientes_principales_data)
        info_personal_var_form = InfoPersonalVarForm(
            request.POST,
            prefix="var",
            instance=info_personal_var_data)
        domicilio_form = DomiciliosForm(
            request.POST,
            prefix="domicilio",
            instance=domicilio_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)

        clientes_principales_is_valid = observaciones_form.is_valid()
        domicilio_is_valid = domicilio_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()
        info_personal_var_is_valid = info_personal_var_form.is_valid()

        if (clientes_principales_is_valid and
            domicilio_is_valid and
            observaciones_is_valid and
            info_personal_var_is_valid):

            clientes_principales = clientes_principales_form.save(commit=False)
            observaciones = observaciones_form.save()
            domicilio = domicilio_form.save()

            info_personal_var = info_personal_var_form.save(commit=False)
            info_personal_var.declaraciones = declaracion
            info_personal_var.domicilios = domicilio
            info_personal_var.save()

            clientes_principales.info_personal_var = info_personal_var
            clientes_principales.declaraciones = declaracion
            clientes_principales.observaciones = observaciones

            clientes_principales.save()

            if not agregar and not editar_id:
                status, status_created = guardar_estatus(request,
                                                             declaracion.folio,
                                                             SeccionDeclaracion.COMPLETA,
                                                             aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:clientes-principales-agregar', folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return HttpResponseRedirect(
                reverse_lazy('declaracion:otras-partes-relacionadas',
                             args=[folio_declaracion]))

        return render(request, self.template_name, {
            'clientes_principales_form': clientes_principales_form,
            'observaciones_form': observaciones_form,
            'info_personal_var_form': info_personal_var_form,
            'domicilio_form': domicilio_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
            'avance':declaracion.avance
        })


class OtrasPartesFormDeleteView(DeclaracionDeleteView):
    model = OtrasPartes


class OtrasPartesFormView(View):
    template_name = 'declaracion/intereses/otras-partes.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0,None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        agregar, editar_id, otras_partes_data, informacion_registrada = (
            declaracion_datos(kwargs, OtrasPartes, declaracion)
        )

        if otras_partes_data:
            observaciones_data = otras_partes_data.observaciones
            otraspartes_infopersonalvar_data = otras_partes_data.otraspartes_infopersonalvar
            otraspartes_infopersonalvar_data = model_to_dict(otraspartes_infopersonalvar_data)
            observaciones_data = model_to_dict(observaciones_data)
            otras_partes_data = model_to_dict(otras_partes_data)
        else:
            observaciones_data = {}
            otras_partes_data = {}
            otraspartes_infopersonalvar_data = {}

        otras_partes_form = OtrasPartesForm(
            prefix="otras_partes",
            initial=otras_partes_data)
        otraspartes_infopersonalvar_form = InfoPersonalVarForm(
            prefix="var",
            initial=otraspartes_infopersonalvar_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)

        return render(request, self.template_name, {
            'otras_partes_form': otras_partes_form,
            'observaciones_form': observaciones_form,
            'otraspartes_infopersonalvar_form': otraspartes_infopersonalvar_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
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

        agregar, editar_id, otras_partes_data, informacion_registrada = (
            declaracion_datos(kwargs, OtrasPartes, declaracion)
        )

        if otras_partes_data:
            observaciones_data = otras_partes_data.observaciones
            otraspartes_infopersonalvar_data = otras_partes_data.otraspartes_infopersonalvar
        else:
            observaciones_data = None
            otras_partes_data = None
            otraspartes_infopersonalvar_data = None

        otras_partes_form = OtrasPartesForm(
            request.POST,
            prefix="otras_partes",
            instance=otras_partes_data)
        otraspartes_infopersonalvar_form = InfoPersonalVarForm(
            request.POST,
            prefix="var",
            instance=otraspartes_infopersonalvar_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)

        otras_partes_is_valid = otras_partes_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()
        otraspartes_infopersonalvar_is_valid = otraspartes_infopersonalvar_form.is_valid()

        if (otras_partes_is_valid and
            observaciones_is_valid and
            otraspartes_infopersonalvar_is_valid):


            otras_partes = otras_partes_form.save(commit=False)
            observaciones = observaciones_form.save()

            otraspartes_infopersonalvar = otraspartes_infopersonalvar_form.save(commit=False)
            otraspartes_infopersonalvar.declaraciones = declaracion
            otraspartes_infopersonalvar.save()
            otraspartes_infopersonalvar_form.save_m2m()

            declarante_infopersonalvar = InfoPersonalVar.objects.filter(
                declaraciones=declaracion).first()

            otras_partes.declarante_infopersonalvar = declarante_infopersonalvar
            otras_partes.otraspartes_infopersonalvar = otraspartes_infopersonalvar
            otras_partes.declaraciones = declaracion
            otras_partes.observaciones = observaciones

            otras_partes.save()

            if not agregar and not editar_id:
                status, status_created = guardar_estatus(request,
                                                             declaracion.folio,
                                                             SeccionDeclaracion.COMPLETA,
                                                             aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:otras-partes-relacionadas-agregar', folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return HttpResponseRedirect(
                reverse_lazy('declaracion:beneficios-gratuitos',
                             args=[folio_declaracion]))

        return render(request, self.template_name, {
            'otras_partes_form': otras_partes_form,
            'observaciones_form': observaciones_form,
            'info_personal_var_form': otraspartes_infopersonalvar_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
            'avance':declaracion.avance
        })


class BeneficiosGratuitosDeleteView(DeclaracionDeleteView):
    model = BeneficiosGratuitos


class BeneficiosGratuitosView(View):
    template_name = 'declaracion/intereses/beneficios-gratuitos.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0,None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)  # 0,None
        except:
            raise Http404()

        agregar, editar_id, beneficios_gratuitos_data, informacion_registrada = (
            declaracion_datos(kwargs, BeneficiosGratuitos, declaracion)
        )

        if beneficios_gratuitos_data:
            observaciones_data = beneficios_gratuitos_data.observaciones
            observaciones_data = model_to_dict(observaciones_data)
            beneficios_gratuitos_data = model_to_dict(beneficios_gratuitos_data)
        else:
            observaciones_data = {}
            beneficios_gratuitos_data = {}

        beneficios_gratuitos_form = BeneficiosGratuitosForm(
            prefix="beneficios_gratuitos",
            initial=beneficios_gratuitos_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)

        return render(request, self.template_name, {
            'beneficios_gratuitos_form': beneficios_gratuitos_form,
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
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

        agregar, editar_id, beneficios_gratuitos_data, informacion_registrada = (
            declaracion_datos(kwargs, BeneficiosGratuitos, declaracion)
        )

        if beneficios_gratuitos_data:
            observaciones_data = beneficios_gratuitos_data.observaciones
        else:
            observaciones_data = None
            beneficios_gratuitos_data = None

        beneficios_gratuitos_form = BeneficiosGratuitosForm(
            request.POST,
            prefix="beneficios_gratuitos",
            instance=beneficios_gratuitos_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)

        beneficios_gratuitos_is_valid = beneficios_gratuitos_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()

        if (beneficios_gratuitos_is_valid and
            observaciones_is_valid):


            beneficios_gratuitos = beneficios_gratuitos_form.save(commit=False)
            observaciones = observaciones_form.save()

            beneficios_gratuitos.declaraciones = declaracion
            beneficios_gratuitos.observaciones = observaciones

            beneficios_gratuitos.save()

            if not agregar and not editar_id:
                status, status_created = guardar_estatus(request,
                                                             declaracion.folio,
                                                             SeccionDeclaracion.COMPLETA,
                                                             aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:beneficios-gratuitos-agregar', folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return HttpResponseRedirect(
                reverse_lazy('declaracion:intereses-observaciones',
                             args=[folio_declaracion]))

        return render(request, self.template_name, {
            'beneficios_gratuitos_form': beneficios_gratuitos_form,
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
            'avance':declaracion.avance
        })


class InteresesObservacionesView(View):
    template_name = 'declaracion/intereses/observaciones.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas =  0,None
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


            status, status_created = guardar_estatus(request,
                                                         declaracion.folio,
                                                         SeccionDeclaracion.COMPLETA,
                                                         aplica=no_aplica(request))
            observaciones = observaciones_form.save()
            status.observaciones = observaciones
            status.save()

            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return HttpResponseRedirect(
                reverse_lazy('declaracion:ingresos-publicos',
                             args=[folio_declaracion]))

        return render(request, self.template_name, {
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance
        })
