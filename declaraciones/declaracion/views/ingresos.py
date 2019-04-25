import uuid
from django.urls import reverse_lazy, resolve
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from declaracion.forms import (ObservacionesForm, DomiciliosForm,
                               SueldosPublicosForm, IngresosVariosForm,
                               InfoPersonalVarForm)
from declaracion.models import (Declaraciones, SeccionDeclaracion,
                                SueldosPublicos, IngresosVarios,
                                SeccionDeclaracion, Secciones)

from .utils import (guardar_estatus, no_aplica, declaracion_datos,
                    validar_declaracion, obtiene_avance)
from .declaracion import (DeclaracionDeleteView)


class SueldosPublicosView(View):
    template_name = 'declaracion/ingresos/sueldos-publicos.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0, None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        sueldos_publicos_data = SueldosPublicos.objects.filter(
            declaraciones=declaracion).first()
        if sueldos_publicos_data:
            observaciones_data = sueldos_publicos_data.observaciones
            sueldos_publicos_data = model_to_dict(sueldos_publicos_data)
            observaciones_data = model_to_dict(observaciones_data)
        else:
            sueldos_publicos_data = {}
            observaciones_data = {}

        sueldos_publicos_form = SueldosPublicosForm(prefix="sueldos_publicos",
                                                    initial=sueldos_publicos_data)
        observaciones_form = ObservacionesForm(prefix="observaciones",
                                               initial=observaciones_data)

        return render(request, self.template_name, {
            'form': sueldos_publicos_form,
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'avance':avance,
            'faltas':faltas,
        })

    @method_decorator(login_required(login_url='/login'))
    def post(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
        except:
            raise Http404()

        sueldos_publicos_data = SueldosPublicos.objects.filter(
            declaraciones=declaracion).first()
        if sueldos_publicos_data:
            observaciones_data = sueldos_publicos_data.observaciones
        else:
            sueldos_publicos_data = None
            observaciones_data = None

        sueldos_publicos_form = SueldosPublicosForm(request.POST,
                                                    prefix="sueldos_publicos",
                                                    instance=sueldos_publicos_data)
        observaciones_form = ObservacionesForm(request.POST,
                                               prefix="observaciones",
                                               instance=observaciones_data)

        sueldos_publicos_is_valid = sueldos_publicos_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()

        if (sueldos_publicos_is_valid and
                observaciones_is_valid):

            sueldos_publicos = sueldos_publicos_form.save(commit=False)
            observaciones = observaciones_form.save()

            sueldos_publicos.declaraciones = declaracion

            sueldos_publicos.observaciones = observaciones
            sueldos_publicos.save()

            status, status_created = guardar_estatus(
                request,
                declaracion.folio,
                SeccionDeclaracion.COMPLETA)

            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')
            #print( request.POST.get("accion"))
            #if request.POST.get("accion")=="gc":
            return redirect('declaracion:ingresos-varios',tipo=0, folio=folio_declaracion)
            #else:
            #    return redirect('declaracion:ingresos-publicos',folio=folio_declaracion)


        return render(request, self.template_name, {
            'form': sueldos_publicos_form,
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance
        })


class IngresosVariosDeleteView(DeclaracionDeleteView):
    model = IngresosVarios


class IngresosVariosView(View):
    template_name = 'declaracion/ingresos/varios.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0,None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        tipo = int(self.kwargs['tipo'])+1
        nombres_tipo = ["","II. Sueldos y salarios por otros empleos","III. Actividad profesional","IV. Actividad empresarial","V. Actividad económica menor","VI. Arrendamiento","VII. Intereses","VIII. Premios","IX. Enajenación de bienes","X. Otros ingresos"]
        siguiente = ["","sueldos y salarios","actividad profesional","actividad empresarial","actividad económica menor","arrendamiento","intereses","premio","enajenación de bienes","otros ingresos"]

        agregar, editar_id, ingresos_varios_data, informacion_registrada = (
            declaracion_datos(kwargs, IngresosVarios, declaracion)
        )

        if ingresos_varios_data:
            observaciones_data = ingresos_varios_data.observaciones
            info_personal_var_data = ingresos_varios_data.info_personal_var
            domicilio_data = info_personal_var_data.domicilios
            if domicilio_data:
                domicilio_data = model_to_dict(domicilio_data)
            else:
                domicilio_data = {}
            info_personal_var_data = model_to_dict(info_personal_var_data)
            observaciones_data = model_to_dict(observaciones_data)
            ingresos_varios_data = model_to_dict(ingresos_varios_data)
        else:
            sueldos_publicos_data = {}
            observaciones_data = {}
            domicilio_data = {}
            info_personal_var_data = {}

        ingresos_varios_form = IngresosVariosForm(
            prefix="ingresos_varios",
            initial=ingresos_varios_data)
        info_personal_var_form = InfoPersonalVarForm(
            prefix="var",
            initial=info_personal_var_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)
        domicilio_form = DomiciliosForm(
            prefix="domicilio",
            initial=domicilio_data)

        return render(request, self.template_name, {
            'form': ingresos_varios_form,
            'domicilio_form': domicilio_form,
            'info_personal_var_form': info_personal_var_form,
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'tipo':tipo-1,
            'nombre':nombres_tipo[tipo],
            'avance':avance,
            'faltas':faltas,
            'siguiente':siguiente[tipo],
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
        tipo = int(self.kwargs['tipo'])+1
        nombres_tipo = ["","II. Sueldos y salarios por otros empleos","III. Actividad profesional","IV. Actividad empresarial","V. Actividad económica menor","VI. Arrendamiento","VII. Intereses","VIII. Premios","IX. Enajenación de bienes","X. Otros ingresos"]

        agregar, editar_id, ingresos_varios_data, informacion_registrada = (
            declaracion_datos(kwargs, IngresosVarios, declaracion)
        )

        if ingresos_varios_data:
            observaciones_data = ingresos_varios_data.observaciones
            info_personal_var_data = ingresos_varios_data.info_personal_var
            domicilio_data = info_personal_var_data.domicilios
        else:
            ingresos_varios_data = None
            observaciones_data = None
            domicilio_data = None
            info_personal_var_data = None

        ingresos_varios_form = IngresosVariosForm(
            request.POST,
            prefix="ingresos_varios",
            instance=ingresos_varios_data)
        info_personal_var_form = InfoPersonalVarForm(
            request.POST,
            prefix="var",
            instance=info_personal_var_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)
        domicilio_form = DomiciliosForm(
            request.POST,
            prefix="domicilio",
            instance=domicilio_data)


        ingresos_varios_is_valid = ingresos_varios_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()
        domicilio_is_valid = domicilio_form.is_valid()
        info_personal_var_is_valid = info_personal_var_form.is_valid()


        if (ingresos_varios_is_valid and
            observaciones_is_valid and
            domicilio_is_valid and
            info_personal_var_is_valid):


            ingresos_varios = ingresos_varios_form.save(commit=False)
            observaciones = observaciones_form.save()
            domicilio = domicilio_form.save()

            info_personal_var = info_personal_var_form.save(commit=False)
            info_personal_var.declaraciones = declaracion
            info_personal_var.domicilios = domicilio
            info_personal_var.save()

            ingresos_varios.info_personal_var = info_personal_var
            ingresos_varios.declaraciones = declaracion
            ingresos_varios.observaciones = observaciones
            ingresos_varios.cat_tipos_ingresos_varios_id = tipo

            ingresos_varios.save()
            if not agregar and not editar_id:
                status, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA,
                    self.kwargs['tipo'],
                    aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:ingresos-varios-agregar',
                                folio=folio_declaracion,
                                tipo=self.kwargs['tipo'])
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            if tipo >8:
                    return redirect('declaracion:ingresos-observaciones', folio=folio_declaracion)
            else:
                    return redirect('declaracion:ingresos-varios',tipo=tipo, folio=folio_declaracion)


        return render(request, self.template_name, {
            'form': ingresos_varios_form,
            'domicilio_form': domicilio_form,
            'info_personal_var_form': info_personal_var_form,
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'tipo':tipo-1,
            'nombre':nombres_tipo[tipo],
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
            'avance':declaracion.avance
        })


class IngresosObservacionesView(View):
    template_name = 'declaracion/ingresos/observaciones.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0,None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        folio = uuid.UUID(folio_declaracion)
        declaracion = Declaraciones.objects.filter(folio=folio).first()

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
            'faltas':faltas,
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

        current_url = resolve(request.path_info).url_name
        seccion_id = Secciones.objects.filter(url=current_url).first()
        seccion = SeccionDeclaracion.objects.filter(declaraciones=declaracion, seccion=seccion_id).first()

        if seccion:
            observaciones_data = seccion.observaciones
        else:
            observaciones_data = None

        observaciones_form = ObservacionesForm(request.POST,
                                               prefix="observaciones",
                                               instance=observaciones_data)

        observaciones_is_valid = observaciones_form.is_valid()

        if observaciones_is_valid:

            status, status_created = guardar_estatus(request,
                                           declaracion.folio,
                                           SeccionDeclaracion.COMPLETA)
            observaciones = observaciones_form.save()
            status.observaciones = observaciones
            status.save()

            return HttpResponseRedirect(
                reverse_lazy('declaracion:bienes-inmuebles',
                             args=[folio_declaracion]))

        return render(request, self.template_name, {
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance
        })
