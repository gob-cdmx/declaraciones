import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy, resolve
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from declaracion.models import (Declaraciones, InfoPersonalFija,
                                InfoPersonalVar, SeccionDeclaracion,
                                DatosCurriculares, Encargos, ExperienciaLaboral,
                                ConyugeDependientes, Secciones, Apoyos)
from declaracion.forms import (DeclaracionForm, InfoPersonalFijaForm,
                               DomiciliosForm, InfoPersonalVarForm,
                               ObservacionesForm, DatosCurricularesForm,
                               DatosEncargoActualForm, ExperienciaLaboralForm,
                               ConyugeDependientesForm, ApoyosForm)
from .declaracion import (DeclaracionDeleteView)
from .utils import guardar_estatus, declaracion_datos, validar_declaracion, obtiene_avance


class DeclaracionFormView(View):
    template_name="declaracion/informacion_personal/informacion-general.html"

    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):
        usuario = request.user
        info_personal_var_data = {}
        avance,faltas = 0,None
        try:
            cat_tipos_declaracion = self.kwargs['cat_tipos_declaracion']
            info_personal_fija = InfoPersonalFija.objects.filter(usuario=usuario).first()
            info_personal_var_data = {
                'nombres': info_personal_fija.nombres,
                'apellido1': info_personal_fija.apellido1,
                'apellido2': info_personal_fija.apellido2,
                'rfc': info_personal_fija.rfc,
                'fecha_nacimiento': info_personal_fija.fecha_nacimiento,
                'cat_pais': info_personal_fija.cat_pais,
                'cat_entidades_federativas': info_personal_fija.cat_entidades_federativas,
                'curp': info_personal_fija.curp,
            }
        except Exception as e:
            cat_tipos_declaracion = ''

        try:
            folio_declaracion = self.kwargs['folio']
        except Exception as e:
            folio_declaracion = ''

        if folio_declaracion:
            try:
                declaracion_obj = validar_declaracion(request, folio_declaracion)
                avance, faltas = obtiene_avance(declaracion_obj)
            except ObjectDoesNotExist as e:
                raise Http404()


            info_personal_var_data = InfoPersonalVar.objects.filter(
                declaraciones=declaracion_obj).first()
            domicilio_data = info_personal_var_data.domicilios
            observaciones_data = info_personal_var_data.observaciones
            info_personal_var_data = model_to_dict(info_personal_var_data)
            domicilio_data = model_to_dict(domicilio_data)
            observaciones_data = model_to_dict(observaciones_data)
            declaracion_data = {'cat_tipos_declaracion': declaracion_obj.cat_tipos_declaracion}
        else:
            domicilio_data = {}
            observaciones_data = {}
            declaracion_data = {'cat_tipos_declaracion': cat_tipos_declaracion}

        declaracion = DeclaracionForm(prefix="declaracion",
                                      initial=declaracion_data)
        info_personal_var = InfoPersonalVarForm(prefix="var",
                                                initial=info_personal_var_data)
        domicilio = DomiciliosForm(prefix="domicilio",
                                  initial=domicilio_data)
        observaciones = ObservacionesForm(prefix="observaciones",
                                          initial=observaciones_data)



        return render(request,self.template_name, {
            'declaracion': declaracion,
            'info_personal_var': info_personal_var,
            'domicilio': domicilio,
            'observaciones': observaciones,
            'folio_declaracion': folio_declaracion,
            'cat_tipos_declaracion': cat_tipos_declaracion,
            'avance':avance,
            'faltas':faltas
        })

    @method_decorator(login_required(login_url='/login'))
    def post(self,request,*args,**kwargs):

        usuario = request.user
        avance, faltas = 0, None
        try:
            cat_tipos_declaracion = self.kwargs['cat_tipos_declaracion']
        except Exception as e:
            cat_tipos_declaracion = None

        try:
            folio_declaracion = self.kwargs['folio']
        except Exception as e:
            folio_declaracion = None

        if folio_declaracion:
            try:
                declaracion = validar_declaracion(request, folio_declaracion)
            except ObjectDoesNotExist as e:
                raise Http404()

            info_personal_var_data = InfoPersonalVar.objects.filter(
                declaraciones=declaracion).first()
            domicilio_data = info_personal_var_data.domicilios
            observaciones_data = info_personal_var_data.observaciones
        else:
            info_personal_var_data = None
            domicilio_data = None
            observaciones_data = None
            declaracion = None

        declaracion_form = DeclaracionForm(request.POST, prefix="declaracion",
                                           instance=declaracion)

        info_personal_var_form = InfoPersonalVarForm(request.POST, prefix="var",
                                                     instance=info_personal_var_data)
        domicilio_form = DomiciliosForm(request.POST, prefix="domicilio",
                                       instance=domicilio_data)
        observaciones_form = ObservacionesForm(request.POST, prefix="observaciones",
                                               instance=observaciones_data)

        declaracion_is_valid = declaracion_form.is_valid()
        info_personal_var_is_valid = info_personal_var_form.is_valid()
        domicilio_is_valid = domicilio_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()

        if (declaracion_is_valid and
            info_personal_var_is_valid and
            domicilio_is_valid and
            observaciones_is_valid):

            try:
                cat_tipos_declaracion = self.kwargs['cat_tipos_declaracion']
            except Exception as e:
                cat_tipos_declaracion = None

            info_personal_var = info_personal_var_form.save(commit=False)
            domicilio = domicilio_form.save()
            observaciones = observaciones_form.save()

            info_personal_fija = InfoPersonalFija.objects.filter(usuario=usuario).first()
            info_personal_fija.cat_estados_civiles = info_personal_var.cat_estados_civiles
            info_personal_fija.cat_regimenes_matrimoniales = info_personal_var.cat_regimenes_matrimoniales
            info_personal_fija.num_id_identificacion = info_personal_var.num_id_identificacion
            info_personal_fija.email_personal = info_personal_var.email_personal
            info_personal_fija.tel_particular = info_personal_var.tel_particular
            info_personal_fija.tel_movil = info_personal_var.tel_movil
            info_personal_fija.usuario = request.user
            info_personal_fija.save()

            if not declaracion:
                declaraciones = declaracion_form.save(commit=False)
                declaraciones.cat_tipos_declaracion_id = cat_tipos_declaracion
            else:
                declaraciones = declaracion_form.save(commit=False)

            declaraciones.info_personal_fija = info_personal_fija
            declaraciones.save()

            info_personal_var.declaraciones = declaraciones
            info_personal_var.domicilios = domicilio
            info_personal_var.observaciones = observaciones
            info_personal_var.cat_tipo_persona_id = 1
            info_personal_var.save()
            info_personal_var_form.save_m2m()

            status, status_created = guardar_estatus(request,
                                           declaraciones.folio,
                                           SeccionDeclaracion.COMPLETA)

            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return HttpResponseRedirect(
                reverse_lazy('declaracion:datos-curriculares',
                             args=[declaraciones.folio]))

        try:
            avance,faltas = obtiene_avance(declaracion)
        except Exception as e:
            avance = 0

        return render(request,self.template_name, {
            'declaracion': declaracion_form,
            'info_personal_var': info_personal_var_form,
            'domicilio': domicilio_form,
            'observaciones': observaciones_form,
            'avance':avance,
            'folio_declaracion': folio_declaracion,
            'faltas':faltas,
            'cat_tipos_declaracion':cat_tipos_declaracion
        })


class DatosCurricularesDelete(DeclaracionDeleteView):
    model = DatosCurriculares


class DatosCurricularesView(View):
    template_name = 'declaracion/informacion_personal/datos-curriculares.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args,**kwargs):
        folio_declaracion = self.kwargs['folio']
        avance,faltas=0,None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance,faltas=obtiene_avance(declaracion)
        except ObjectDoesNotExist as e:
            raise Http404()

        agregar, editar_id, datos_curriculares_data, informacion_registrada = (
            declaracion_datos(kwargs, DatosCurriculares, declaracion)
        )

        if datos_curriculares_data:
            observaciones_data = datos_curriculares_data.observaciones
            observaciones_data = model_to_dict(observaciones_data)
            datos_curriculares_data = model_to_dict(datos_curriculares_data)
        else:
            observaciones_data = {}
            datos_curriculares_data = {}

        datos_curriculares_form = DatosCurricularesForm(
            prefix="datos_curriculares",
            initial=datos_curriculares_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)
        return render(request, self.template_name, {
            'datos_curriculares_form': datos_curriculares_form,
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
            'avance':declaracion.avance
        })

    @method_decorator(login_required(login_url='/login'))
    def post(self, request, *args,**kwargs):

        folio_declaracion = self.kwargs['folio']
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
        except ObjectDoesNotExist as e:
            raise Http404()

        agregar, editar_id, datos_curriculares_data, informacion_registrada = (
            declaracion_datos(kwargs, DatosCurriculares, declaracion)
        )

        if datos_curriculares_data:
            observaciones_data = datos_curriculares_data.observaciones
        else:
            observaciones_data = None
            datos_curriculares_data = None

        datos_curriculares_form = DatosCurricularesForm(request.POST,
                                                        prefix="datos_curriculares",
                                                        instance=datos_curriculares_data)
        observaciones_form = ObservacionesForm(request.POST, prefix="observaciones",
                                               instance=observaciones_data)

        datos_curriculares_is_valid = datos_curriculares_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()

        if datos_curriculares_is_valid and observaciones_is_valid:

            datos_curriculares = datos_curriculares_form.save(commit=False)


            observaciones = observaciones_form.save()

            datos_curriculares.declaraciones = declaracion
            datos_curriculares.observaciones = observaciones
            datos_curriculares.save()

            if not agregar and not editar_id:
                status, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA)

            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')
            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:datos-curriculares-agregar', folio=folio_declaracion)

            return HttpResponseRedirect(
                reverse_lazy('declaracion:datos-del-encargo-actual',
                             args=[folio_declaracion]))

        return render(request, self.template_name, {
            'datos_curriculares_form': datos_curriculares_form,
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
            'avance':declaracion.avance
        })

class DatosEncargoActualView(View):
    template_name = 'declaracion/informacion_personal/datos-del-encargo-actual.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0, None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except ObjectDoesNotExist as e:
            raise Http404()

        datos_encargo_actual_data = Encargos.objects.filter(declaraciones=declaracion).first()
        if datos_encargo_actual_data:
            observaciones_data = datos_encargo_actual_data.observaciones
            domicilio_data = datos_encargo_actual_data.domicilios
            observaciones_data = model_to_dict(observaciones_data)
            datos_encargo_actual_data = model_to_dict(datos_encargo_actual_data)
            domicilio_data = model_to_dict(domicilio_data)
        else:
            observaciones_data = {}
            datos_encargo_actual_data = {}
            domicilio_data = {}

        datos_encargo_actual_form = DatosEncargoActualForm(
            prefix="datos_encargo_actual",
            initial=datos_encargo_actual_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)
        domicilio_form = DomiciliosForm(
            prefix="domicilio",
            initial=domicilio_data)

        return render(request, self.template_name, {
            'datos_encargo_actual_form': datos_encargo_actual_form,
            'observaciones_form': observaciones_form,
            'domicilio_form': domicilio_form,
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

        folio = uuid.UUID(folio_declaracion)
        declaracion = Declaraciones.objects.filter(folio=folio).first()
        datos_encargo_actual_data = Encargos.objects.filter(declaraciones=declaracion).first()
        if datos_encargo_actual_data:
            observaciones_data = datos_encargo_actual_data.observaciones
            domicilio_data = datos_encargo_actual_data.domicilios
        else:
            observaciones_data = None
            datos_encargo_actual_data = None
            domicilio_data = None

        datos_encargo_actual_form = DatosEncargoActualForm(
            request.POST,
            prefix="datos_encargo_actual",
            instance=datos_encargo_actual_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)
        domicilio_form = DomiciliosForm(
            request.POST,
            prefix="domicilio",
            instance=domicilio_data)

        if (datos_encargo_actual_form.is_valid() and
            observaciones_form.is_valid() and
            domicilio_form.is_valid()):

            datos_encargo_actual = datos_encargo_actual_form.save(commit=False)

            observaciones = observaciones_form.save()
            domicilio = domicilio_form.save()

            datos_encargo_actual.declaraciones = declaracion
            datos_encargo_actual.observaciones = observaciones
            datos_encargo_actual.domicilios = domicilio
            datos_encargo_actual.save()

            status, status_created = guardar_estatus(
                request,
                declaracion.folio,
                SeccionDeclaracion.COMPLETA)

            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return HttpResponseRedirect(
                reverse_lazy('declaracion:experiencia-laboral',
                             args=[folio_declaracion]))


        return render(request, self.template_name, {
            'datos_encargo_actual_form': datos_encargo_actual_form,
            'observaciones_form': observaciones_form,
            'domicilio_form': domicilio_form,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance
        })


class ExperienciaLaboralDeleteView(DeclaracionDeleteView):
    model = ExperienciaLaboral


class ExperienciaLaboralView(View):
    template_name = 'declaracion/informacion_personal/experiencia_laboral.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0, None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except ObjectDoesNotExist as e:
            raise Http404()

        agregar, editar_id, experiencia_laboral_data, informacion_registrada = (
            declaracion_datos(kwargs, ExperienciaLaboral, declaracion)
        )

        if experiencia_laboral_data:
            observaciones_data = experiencia_laboral_data.observaciones
            domicilio_data = experiencia_laboral_data.domicilios
            experiencia_laboral_data = model_to_dict(experiencia_laboral_data)
            observaciones_data = model_to_dict(observaciones_data)
            domicilio_data = model_to_dict(domicilio_data)
        else:
            experiencia_laboral_data = {}
            observaciones_data = {}
            domicilio_data = {}

        experiencia_laboral_form = ExperienciaLaboralForm(
            prefix="experiencia_laboral",
            initial=experiencia_laboral_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)
        domicilio_form = DomiciliosForm(
            prefix="domicilio",
            initial=domicilio_data)

        return render(request, self.template_name, {
            'experiencia_laboral_form': experiencia_laboral_form,
            'observaciones_form': observaciones_form,
            'domicilio_form': domicilio_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
            'avance':declaracion.avance
        })

    @method_decorator(login_required(login_url='/login'))
    def post(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']

        try:
            declaracion = validar_declaracion(request, folio_declaracion)
        except:
            raise Http404()

        agregar, editar_id, experiencia_laboral_data, informacion_registrada = (
            declaracion_datos(kwargs, ExperienciaLaboral, declaracion)
        )

        if experiencia_laboral_data:
            observaciones_data = experiencia_laboral_data.observaciones
            domicilio_data = experiencia_laboral_data.domicilios
        else:
            experiencia_laboral_data = None
            observaciones_data = None
            domicilio_data = None

        experiencia_laboral_form = ExperienciaLaboralForm(
            request.POST,
            prefix="experiencia_laboral",
            instance=experiencia_laboral_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)
        domicilio_form = DomiciliosForm(
            request.POST,
            prefix="domicilio",
            instance=domicilio_data)

        experiencia_laboral_is_valid = experiencia_laboral_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()
        domicilio_is_valid = domicilio_form.is_valid()

        if (experiencia_laboral_is_valid and observaciones_is_valid and
            domicilio_is_valid):

            experiencia_laboral = experiencia_laboral_form.save(commit=False)
            observaciones = observaciones_form.save()
            domicilio = domicilio_form.save()

            experiencia_laboral.declaraciones = declaracion
            experiencia_laboral.observaciones = observaciones
            experiencia_laboral.domicilios = domicilio
            experiencia_laboral.save()

            if not agregar and not editar_id:
                status, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA)

            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')
            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:experiencia-laboral-agregar', folio=folio_declaracion)

            return HttpResponseRedirect(
                reverse_lazy('declaracion:dependientes-economicos',
                             args=[folio_declaracion]))


        return render(request, self.template_name, {
            'experiencia_laboral_form': experiencia_laboral_form,
            'observaciones_form': observaciones_form,
            'domicilio_form': domicilio_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
            'avance':declaracion.avance
        })


class ConyugeDependientesDeleteView(DeclaracionDeleteView):
    model = ConyugeDependientes


class ConyugeDependientesView(View):
    template_name = 'declaracion/informacion_personal/conyuge-dependiente.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0,None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas =obtiene_avance(declaracion)
        except:
            raise Http404()

        agregar, editar_id, conyuge_dependiente_data, informacion_registrada = (
            declaracion_datos(kwargs, ConyugeDependientes, declaracion)
        )

        if conyuge_dependiente_data:
            observaciones_data = conyuge_dependiente_data.observaciones
            info_personal_var_data = conyuge_dependiente_data.dependiente_infopersonalvar
            apoyos_data = Apoyos.objects.filter(
                beneficiario_infopersonalvar=info_personal_var_data
                ).first()
            if apoyos_data:
                observaciones_apoyos_data = apoyos_data.observaciones
                apoyos_data = model_to_dict(apoyos_data)
                observaciones_apoyos_data = model_to_dict(observaciones_apoyos_data)
            else:
                apoyos_data = {}
                observaciones_apoyos_data = {}
            domiclios_data = info_personal_var_data.domicilios
            if domiclios_data:
                domiclios_data = model_to_dict(domiclios_data)
            else:
                domiclios_data = {}
            observaciones_data = model_to_dict(observaciones_data)
            info_personal_var_data = model_to_dict(info_personal_var_data)
            conyuge_dependiente_data = model_to_dict(conyuge_dependiente_data)
        else:
            domiclios_data = {}
            observaciones_data = {}
            conyuge_dependiente_data = {}
            info_personal_var_data = {}
            apoyos_data = {}
            observaciones_apoyos_data = {}

        apoyos_form = ApoyosForm(
            prefix="apoyos",
            initial=apoyos_data)
        observaciones_apoyos_form = ObservacionesForm(
            prefix="observaciones_apoyos",
            initial=observaciones_apoyos_data)
        conyuge_dependiente_form = ConyugeDependientesForm(
            prefix="conyuge_dependiente",
            initial=conyuge_dependiente_data)
        info_personal_var_form = InfoPersonalVarForm(
            prefix="var",
            initial=info_personal_var_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)
        domicilio_form = DomiciliosForm(prefix="domicilio",
                                       initial=domiclios_data)

        return render(request, self.template_name, {
            'conyuge_dependiente_form': conyuge_dependiente_form,
            'observaciones_form': observaciones_form,
            'info_personal_var_form': info_personal_var_form,
            'domicilio_form': domicilio_form,
            'apoyos_form': apoyos_form,
            'observaciones_apoyos_form': observaciones_apoyos_form,
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

        agregar, editar_id, conyuge_dependiente_data, informacion_registrada = (
            declaracion_datos(kwargs, ConyugeDependientes, declaracion)
        )

        if conyuge_dependiente_data:
            observaciones_data = conyuge_dependiente_data.observaciones
            info_personal_var_data = conyuge_dependiente_data.dependiente_infopersonalvar
            domiclios_data = info_personal_var_data.domicilios
            apoyos_data = Apoyos.objects.filter(
                beneficiario_infopersonalvar=info_personal_var_data
                ).first()
            if apoyos_data:
                observaciones_apoyos_data = apoyos_data.observaciones
            else:
                observaciones_apoyos_data = None
        else:
            domiclios_data = None
            observaciones_data = None
            conyuge_dependiente_data = None
            info_personal_var_data = None
            apoyos_data = None
            observaciones_apoyos_data = None

        apoyos_form = ApoyosForm(
            request.POST,
            prefix="apoyos",
            instance=apoyos_data)
        observaciones_apoyos_form = ObservacionesForm(
            request.POST,
            prefix="observaciones_apoyos",
            instance=observaciones_apoyos_data)
        conyuge_dependiente_form = ConyugeDependientesForm(
            request.POST,
            prefix="conyuge_dependiente",
            instance=conyuge_dependiente_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)
        info_personal_var_form = InfoPersonalVarForm(
            request.POST,
            prefix="var",
            instance=info_personal_var_data)
        domicilio_form = DomiciliosForm(
            request.POST,
            prefix="domicilio",
            instance=domiclios_data)


        if (apoyos_form.is_valid() and
            observaciones_apoyos_form.is_valid() and
            conyuge_dependiente_form.is_valid() and
            observaciones_form.is_valid() and
            info_personal_var_form.is_valid() and
            domicilio_form.is_valid()
            ):

            conyuge_dependiente = conyuge_dependiente_form.save(commit=False)
            observaciones = observaciones_form.save()
            domicilio = domicilio_form.save()

            info_personal_var = info_personal_var_form.save(commit=False)
            info_personal_var.declaraciones = declaracion
            info_personal_var.domicilios = domicilio
            info_personal_var.cat_tipo_persona_id = 2
            info_personal_var.save()
            info_personal_var_form.save_m2m()

            conyuge_dependiente.declaraciones = declaracion
            conyuge_dependiente.observaciones = observaciones

            declarante_infopersonalvar = InfoPersonalVar.objects.filter(
                declaraciones=declaracion).first()

            conyuge_dependiente.declarante_infopersonalvar = declarante_infopersonalvar
            conyuge_dependiente.dependiente_infopersonalvar = info_personal_var
            conyuge_dependiente.save()

            observaciones_apoyos = observaciones_apoyos_form.save()
            apoyos = apoyos_form.save(commit=False)
            apoyos.beneficiario_infopersonalvar = info_personal_var
            apoyos.declaraciones = declaracion
            apoyos.observaciones = observaciones_apoyos
            apoyos.save()

            if not agregar and not editar_id:
                status, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA)

            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')
            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:dependientes-economicos-agregar',
                                folio=folio_declaracion)

            return HttpResponseRedirect(
                reverse_lazy('declaracion:informacion-personal-observaciones',
                             args=[folio_declaracion]))


        return render(request, self.template_name, {
            'conyuge_dependiente_form': conyuge_dependiente_form,
            'observaciones_form': observaciones_form,
            'info_personal_var_form': info_personal_var_form,
            'domicilio_form': domicilio_form,
            'apoyos_form': apoyos_form,
            'observaciones_apoyos_form': observaciones_apoyos_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
            'avance':declaracion.avance
        })


class InformacionPersonalObservacionesView(View):
    template_name = 'declaracion/informacion_personal/observaciones.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0, None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except ObjectDoesNotExist as e:
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

        if observaciones_form.is_valid():
            status, status_created = guardar_estatus(request,
                                           declaracion.folio,
                                           SeccionDeclaracion.COMPLETA)
            observaciones = observaciones_form.save()
            status.observaciones = observaciones
            status.save()

            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return HttpResponseRedirect(
                reverse_lazy('declaracion:empresas-sociedades-asociaciones',
                             args=[folio_declaracion]))

        return render(request, self.template_name, {
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance
        })
