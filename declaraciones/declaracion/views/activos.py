import uuid
from django.urls import resolve
from django.views import View
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, Http404
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from declaracion.models import (Declaraciones, SeccionDeclaracion,
                                BienesMuebles, MueblesNoRegistrables,
                                BienesInmuebles, MueblesNoRegistrables,
                                Inversiones, EfectivoMetales, Fideicomisos,
                                BienesIntangibles, CuentasPorCobrar,
                                BeneficiosEspecie, ActivosBienes,
                                BienesPersonas, InfoPersonalVar,
                                Secciones, SeccionDeclaracion)
from declaracion.forms import (BienesMueblesForm, BienesInmueblesForm,
                               MueblesNoRegistrablesForm, InversionesForm,
                               EfectivoMetalesForm, FideicomisosForm,
                               BienesIntangiblesForm, CuentasPorCobrarForm,
                               BeneficiosEspecieForm, BienesPersonasForm,
                               ActivosBienesForm, InfoPersonalVarForm,
                               DomiciliosForm, ObservacionesForm)

from .declaracion import (DeclaracionDeleteView)
from .utils import (guardar_estatus, no_aplica, declaracion_datos,
                    validar_declaracion,obtiene_avance)


class BienesMueblesDeleteView(DeclaracionDeleteView):
    model = BienesMuebles


class BienesMueblesView(View):
    template_name = 'declaracion/activos/bienes-muebles.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0, None

        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        info_personal_var = InfoPersonalVar.objects.filter(
            declaraciones=declaracion,
            cat_tipo_persona_id=InfoPersonalVar.TIPO_DECLARANTE
        ).first()

        agregar, editar_id, bienes_muebles_data, informacion_registrada = (
            declaracion_datos(kwargs, BienesMuebles, declaracion)
        )

        if bienes_muebles_data:
            activos_bienes = ActivosBienes.objects.filter(
                declaraciones=declaracion,
                cat_activo_bien_id=ActivosBienes.BIENES_MUEBLES,
            ).first()
            observaciones_data = bienes_muebles_data.observaciones
            bienes_muebles_data = model_to_dict(bienes_muebles_data)
            observaciones_data = model_to_dict(observaciones_data)

            declarante_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.DECLARANTE,
            ).first()

            if declarante_bienes_personas:
                bienes_personas_data = model_to_dict(declarante_bienes_personas)
            else:
                bienes_personas_data = {}

            copropietario_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO,
            ).first()
            if copropietario_bienes_personas:
                copropietario_data = copropietario_bienes_personas.otra_persona
                copropietario_data = model_to_dict(copropietario_data)
            else:
                copropietario_data = {}

            propietario_anterior_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.PROPIETARIO_ANTERIOR,
            ).first()
            if propietario_anterior_bienes_personas:
                propietario_anterior_data = propietario_anterior_bienes_personas.otra_persona
                propietario_anterior_data = model_to_dict(propietario_anterior_data)
            else:
                propietario_anterior_data = {}

        else:
            bienes_muebles_data = {}
            observaciones_data = {}
            bienes_personas_data = {}
            copropietario_data = {}
            propietario_anterior_data = {}

        bienes_muebles_form = BienesMueblesForm(
            prefix="bienes_muebles",
            initial=bienes_muebles_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)
        bienes_personas_form = BienesPersonasForm(
            prefix="bienes_personas",
            initial=bienes_personas_data)
        copropietario_form = InfoPersonalVarForm(
            prefix="copropietario",
            initial=copropietario_data)
        propietario_anterior_form = InfoPersonalVarForm(
            prefix="propietario_anterior",
            initial=propietario_anterior_data)

        return render(request, self.template_name, {
            'bienes_muebles_form': bienes_muebles_form,
            'observaciones_form': observaciones_form,
            'bienes_personas_form': bienes_personas_form,
            'copropietario_form': copropietario_form,
            'propietario_anterior_form': propietario_anterior_form,
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

        info_personal_var = InfoPersonalVar.objects.filter(
            declaraciones=declaracion,
            cat_tipo_persona_id=InfoPersonalVar.TIPO_DECLARANTE
        ).first()

        agregar, editar_id, bienes_muebles_data, informacion_registrada = (
            declaracion_datos(kwargs, BienesMuebles, declaracion)
        )

        if bienes_muebles_data:
            activos_bienes = ActivosBienes.objects.filter(
                declaraciones=declaracion,
                cat_activo_bien_id=ActivosBienes.BIENES_MUEBLES,
            ).first()
            observaciones_data = bienes_muebles_data.observaciones
            declarante_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.DECLARANTE,
            ).first()

            if declarante_bienes_personas:
                bienes_personas_data = declarante_bienes_personas
            else:
                bienes_personas_data = None

            copropietario_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO,
            ).first()
            if copropietario_bienes_personas:
                copropietario_data = copropietario_bienes_personas.otra_persona
            else:
                copropietario_data = None

            propietario_anterior_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.PROPIETARIO_ANTERIOR,
            ).first()
            if propietario_anterior_bienes_personas:
                propietario_anterior_data = propietario_anterior_bienes_personas.otra_persona
            else:
                propietario_anterior_data = None
        else:
            bienes_muebles_data = None
            observaciones_data = None
            bienes_personas_data = None
            copropietario_data = None
            propietario_anterior_data = None

        bienes_muebles_form = BienesMueblesForm(
            request.POST,
            prefix="bienes_muebles",
            instance=bienes_muebles_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)
        bienes_personas_form = BienesPersonasForm(
            request.POST,
            prefix="bienes_personas",
            instance=bienes_personas_data)
        copropietario_form = InfoPersonalVarForm(
            request.POST,
            prefix="copropietario",
            instance=copropietario_data)
        propietario_anterior_form = InfoPersonalVarForm(
            request.POST,
            prefix="propietario_anterior",
            instance=propietario_anterior_data)

        if (
            bienes_muebles_form.is_valid() and
            observaciones_form.is_valid() and
            bienes_personas_form.is_valid() and
            copropietario_form.is_valid() and
            propietario_anterior_form.is_valid()
            ):

            activos_bienes, created = ActivosBienes.objects.get_or_create(
                declaraciones=declaracion,
                cat_activo_bien_id=ActivosBienes.BIENES_MUEBLES,
            )

            bienes_muebles = bienes_muebles_form.save(commit=False)
            observaciones = observaciones_form.save()

            propietario_anterior = propietario_anterior_form.save(commit=False)
            propietario_anterior.declaraciones = declaracion
            propietario_anterior.cat_tipo_persona_id = InfoPersonalVar.TIPO_PROPIETARIO_ANTERIOR
            propietario_anterior.save()

            copropietario = copropietario_form.save(commit=False)
            copropietario.declaraciones = declaracion
            copropietario.cat_tipo_persona_id = InfoPersonalVar.TIPO_COPROPIETARIO
            copropietario.save()

            bienes_muebles.declaraciones = declaracion
            bienes_muebles.observaciones = observaciones
            bienes_muebles.activos_bienes = activos_bienes
            bienes_muebles.save()

            activos_bienes.id_activobien = bienes_muebles.id
            activos_bienes.save()

            bienes_personas = bienes_personas_form.save(commit=False)
            bienes_personas.info_personal_var = info_personal_var
            bienes_personas.activos_bienes = activos_bienes
            bienes_personas.cat_tipo_participacion_id = BienesPersonas.DECLARANTE
            bienes_personas.save()

            propietario_anterior_bienes_personas, created = BienesPersonas.objects.update_or_create(
                info_personal_var=info_personal_var,
                otra_persona=propietario_anterior,
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.PROPIETARIO_ANTERIOR,
            )
            copropietario_bienes_personas, created = BienesPersonas.objects.update_or_create(
                info_personal_var=info_personal_var,
                otra_persona=copropietario,
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO,
            )

            if not agregar and not editar_id:
                status_obj, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA,
                    aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:bienes-muebles-agregar', folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return redirect('declaracion:muebles-noregistrables',
                            folio=folio_declaracion)

        return render(request, self.template_name, {
            'bienes_muebles_form': bienes_muebles_form,
            'observaciones_form': observaciones_form,
            'bienes_personas_form': bienes_personas_form,
            'copropietario_form': copropietario_form,
            'propietario_anterior_form': propietario_anterior_form,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id
        })


class BienesInmueblesDeleteView(DeclaracionDeleteView):
    model = BienesInmuebles


class BienesInmueblesView(View):
    template_name = 'declaracion/activos/bienes-inmuebles.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0, None

        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        info_personal_var = InfoPersonalVar.objects.filter(
            declaraciones=declaracion,
            cat_tipo_persona_id=InfoPersonalVar.TIPO_DECLARANTE
        ).first()

        agregar, editar_id, bienes_inmuebles_data, informacion_registrada = (
            declaracion_datos(kwargs, BienesInmuebles, declaracion)
        )

        if bienes_inmuebles_data:
            activos_bienes = ActivosBienes.objects.filter(
                declaraciones=declaracion,
                cat_activo_bien_id=ActivosBienes.BIENES_INMUEBLES,
            ).first()
            if bienes_inmuebles_data:
                observaciones_data = bienes_inmuebles_data.observaciones
                domicilios_data = bienes_inmuebles_data.domicilios
                bienes_inmuebles_data = model_to_dict(bienes_inmuebles_data)
                observaciones_data = model_to_dict(observaciones_data)
                domicilios_data = model_to_dict(domicilios_data)
            else:
                bienes_inmuebles_data = {}
                observaciones_data = {}
                domicilios_data = {}


            declarante_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.DECLARANTE,
            ).first()

            if declarante_bienes_personas:
                bienes_personas_data = model_to_dict(declarante_bienes_personas)
            else:
                bienes_personas_data = {}

            copropietario_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO,
            ).first()
            if copropietario_bienes_personas:
                copropietario_data = copropietario_bienes_personas.otra_persona
                copropietario_data = model_to_dict(copropietario_data)
            else:
                copropietario_data = {}

            propietario_anterior_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.PROPIETARIO_ANTERIOR,
            ).first()
            if propietario_anterior_bienes_personas:
                propietario_anterior_data = propietario_anterior_bienes_personas.otra_persona
                propietario_anterior_data = model_to_dict(propietario_anterior_data)
            else:
                propietario_anterior_data = {}
        else:
            bienes_inmuebles_data = {}
            observaciones_data = {}
            domicilios_data = {}
            bienes_personas_data = {}
            copropietario_data = {}
            propietario_anterior_data = {}

        bienes_inmuebles_form = BienesInmueblesForm(
            prefix="bienes_inmuebles",
            initial=bienes_inmuebles_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)
        domicilio_form = DomiciliosForm(
            prefix="domicilio",
            initial=domicilios_data)
        bienes_personas_form = BienesPersonasForm(
            prefix="bienes_personas",
            initial=bienes_personas_data)
        copropietario_form = InfoPersonalVarForm(
            prefix="copropietario",
            initial=copropietario_data)
        propietario_anterior_form = InfoPersonalVarForm(
            prefix="propietario_anterior",
            initial=propietario_anterior_data)

        return render(request, self.template_name, {
            'bienes_inmuebles_form': bienes_inmuebles_form,
            'observaciones_form': observaciones_form,
            'domicilio_form': domicilio_form,
            'bienes_personas_form': bienes_personas_form,
            'copropietario_form': copropietario_form,
            'propietario_anterior_form': propietario_anterior_form,
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

        info_personal_var = InfoPersonalVar.objects.filter(
            declaraciones=declaracion,
            cat_tipo_persona_id=InfoPersonalVar.TIPO_DECLARANTE
        ).first()

        agregar, editar_id, bienes_inmuebles_data, informacion_registrada = (
            declaracion_datos(kwargs, BienesInmuebles, declaracion)
        )

        if bienes_inmuebles_data:
            activos_bienes = ActivosBienes.objects.filter(
                declaraciones=declaracion,
                cat_activo_bien_id=ActivosBienes.BIENES_INMUEBLES,
            ).first()

            if bienes_inmuebles_data:
                observaciones_data = bienes_inmuebles_data.observaciones
                domicilios_data = bienes_inmuebles_data.domicilios
            else:
                bienes_inmuebles_data = None
                observaciones_data = None
                domicilios_data = None

            declarante_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.DECLARANTE,
            ).first()

            if declarante_bienes_personas:
                bienes_personas_data = declarante_bienes_personas
            else:
                bienes_personas_data = None

            copropietario_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO,
            ).first()
            if copropietario_bienes_personas:
                copropietario_data = copropietario_bienes_personas.otra_persona
            else:
                copropietario_data = None

            propietario_anterior_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.PROPIETARIO_ANTERIOR,
            ).first()
            if propietario_anterior_bienes_personas:
                propietario_anterior_data = propietario_anterior_bienes_personas.otra_persona
            else:
                propietario_anterior_data = None
        else:
            bienes_inmuebles_data = None
            observaciones_data = None
            domicilios_data = None
            bienes_personas_data = None
            copropietario_data = None
            propietario_anterior_data = None

        bienes_inmuebles_form = BienesInmueblesForm(
            request.POST,
            prefix="bienes_inmuebles",
            instance=bienes_inmuebles_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)
        domicilio_form = DomiciliosForm(
            request.POST,
            prefix="domicilio",
            instance=domicilios_data)
        bienes_personas_form = BienesPersonasForm(
            request.POST,
            prefix="bienes_personas",
            instance=bienes_personas_data)
        info_personal_var_form = InfoPersonalVarForm(
            request.POST,
            prefix="info_personal_var",
            instance=None)
        copropietario_form = InfoPersonalVarForm(
            request.POST,
            prefix="copropietario",
            instance=copropietario_data)
        propietario_anterior_form = InfoPersonalVarForm(
            request.POST,
            prefix="propietario_anterior",
            instance=propietario_anterior_data)

        if (
            bienes_inmuebles_form.is_valid() and
            observaciones_form.is_valid() and
            domicilio_form.is_valid() and
            bienes_personas_form.is_valid() and
            info_personal_var_form.is_valid() and
            copropietario_form.is_valid() and
            propietario_anterior_form.is_valid()
            ):

            activos_bienes, created = ActivosBienes.objects.get_or_create(
                declaraciones=declaracion,
                cat_activo_bien_id=ActivosBienes.BIENES_INMUEBLES,
            )

            bienes_inmuebles = bienes_inmuebles_form.save(commit=False)
            observaciones = observaciones_form.save()
            domicilio = domicilio_form.save()

            copropietario = copropietario_form.save(commit=False)
            copropietario.declaraciones = declaracion
            copropietario.cat_tipo_persona_id = InfoPersonalVar.TIPO_COPROPIETARIO
            copropietario.save()
            propietario_anterior = propietario_anterior_form.save(commit=False)
            propietario_anterior.declaraciones = declaracion
            propietario_anterior.cat_tipo_persona_id = InfoPersonalVar.TIPO_PROPIETARIO_ANTERIOR
            propietario_anterior.save()

            bienes_inmuebles.declaraciones = declaracion
            bienes_inmuebles.domicilios = domicilio
            bienes_inmuebles.activos_bienes = activos_bienes
            bienes_inmuebles.observaciones = observaciones
            bienes_inmuebles.save()

            activos_bienes.id_activobien = bienes_inmuebles.id
            activos_bienes.save()

            bienes_personas = bienes_personas_form.save(commit=False)
            bienes_personas.info_personal_var = info_personal_var
            bienes_personas.activos_bienes = activos_bienes
            bienes_personas.cat_tipo_participacion_id = BienesPersonas.DECLARANTE
            bienes_personas.save()

            propietario_anterior_bienes_personas, created = BienesPersonas.objects.update_or_create(
                info_personal_var=info_personal_var,
                otra_persona=propietario_anterior,
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.PROPIETARIO_ANTERIOR,
            )
            copropietario_bienes_personas, created = BienesPersonas.objects.update_or_create(
                info_personal_var=info_personal_var,
                otra_persona=copropietario,
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO,
            )
            if not agregar and not editar_id:
                status_obj, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA,
                    aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:bienes-inmuebles-agregar', folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return redirect('declaracion:bienes-muebles',
                            folio=folio_declaracion)

        return render(request, self.template_name, {
            'bienes_inmuebles_form': bienes_inmuebles_form,
            'observaciones_form': observaciones_form,
            'domicilio_form': domicilio_form,
            'bienes_personas_form': bienes_personas_form,
            'copropietario_form': copropietario_form,
            'propietario_anterior_form': propietario_anterior_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
        })


class MueblesNoRegistrablesDeleteView(DeclaracionDeleteView):
    model = MueblesNoRegistrables


class MueblesNoRegistrablesView(View):
    template_name = 'declaracion/activos/muebles-no-registrables.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0, None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        info_personal_var = InfoPersonalVar.objects.filter(
            declaraciones=declaracion,
            cat_tipo_persona_id=InfoPersonalVar.TIPO_DECLARANTE
        ).first()

        agregar, editar_id, muebles_no_registrables_data, informacion_registrada = (
            declaracion_datos(kwargs, MueblesNoRegistrables, declaracion)
        )

        if muebles_no_registrables_data:
            activos_bienes = ActivosBienes.objects.filter(
                declaraciones=declaracion,
                cat_activo_bien_id=ActivosBienes.MUEBLES_NO_REGISTRABLES,
            ).first()

            observaciones_data = muebles_no_registrables_data.observaciones
            muebles_no_registrables_data = model_to_dict(muebles_no_registrables_data)
            observaciones_data = model_to_dict(observaciones_data)

            declarante_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.DECLARANTE,
            ).first()

            if declarante_bienes_personas:
                bienes_personas_data = model_to_dict(declarante_bienes_personas)
            else:
                bienes_personas_data = {}

            copropietario_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO,
            ).first()
            if copropietario_bienes_personas:
                copropietario_data = copropietario_bienes_personas.otra_persona
                copropietario_data = model_to_dict(copropietario_data)
            else:
                copropietario_data = {}

            propietario_anterior_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.PROPIETARIO_ANTERIOR,
            ).first()
            if propietario_anterior_bienes_personas:
                propietario_anterior_data = propietario_anterior_bienes_personas.otra_persona
                propietario_anterior_data = model_to_dict(propietario_anterior_data)
            else:
                propietario_anterior_data = {}
        else:
            muebles_no_registrables_data = {}
            observaciones_data = {}
            bienes_personas_data = {}
            copropietario_data = {}
            propietario_anterior_data = {}


        muebles_no_registrables_form = MueblesNoRegistrablesForm(
            prefix="muebles_no_registrables",
            initial=muebles_no_registrables_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)
        bienes_personas_form = BienesPersonasForm(
            prefix="bienes_personas",
            initial=bienes_personas_data)
        copropietario_form = InfoPersonalVarForm(
            prefix="copropietario",
            initial=copropietario_data)
        propietario_anterior_form = InfoPersonalVarForm(
            prefix="propietario_anterior",
            initial=propietario_anterior_data)


        return render(request, self.template_name, {
            'muebles_no_registrables_form': muebles_no_registrables_form,
            'observaciones_form': observaciones_form,
            'bienes_personas_form': bienes_personas_form,
            'copropietario_form': copropietario_form,
            'propietario_anterior_form': propietario_anterior_form,
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

        info_personal_var = InfoPersonalVar.objects.filter(
            declaraciones=declaracion,
            cat_tipo_persona_id=InfoPersonalVar.TIPO_DECLARANTE
        ).first()

        agregar, editar_id, muebles_no_registrables_data, informacion_registrada = (
            declaracion_datos(kwargs, MueblesNoRegistrables, declaracion)
        )

        if muebles_no_registrables_data:
            activos_bienes = ActivosBienes.objects.filter(
                declaraciones=declaracion,
                cat_activo_bien_id=ActivosBienes.MUEBLES_NO_REGISTRABLES,
            ).first()
            observaciones_data = muebles_no_registrables_data.observaciones
            declarante_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.DECLARANTE,
            ).first()

            if declarante_bienes_personas:
                bienes_personas_data = declarante_bienes_personas
            else:
                bienes_personas_data = None

            copropietario_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO,
            ).first()
            if copropietario_bienes_personas:
                copropietario_data = copropietario_bienes_personas.otra_persona
            else:
                copropietario_data = None

            propietario_anterior_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.PROPIETARIO_ANTERIOR,
            ).first()
            if propietario_anterior_bienes_personas:
                propietario_anterior_data = propietario_anterior_bienes_personas.otra_persona
            else:
                propietario_anterior_data = None
        else:
            muebles_no_registrables_data = None
            observaciones_data = None
            bienes_personas_data = None
            copropietario_data = None
            propietario_anterior_data = None

        muebles_no_registrables_form = MueblesNoRegistrablesForm(
            request.POST,
            prefix="muebles_no_registrables",
            instance=muebles_no_registrables_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)
        bienes_personas_form = BienesPersonasForm(
            request.POST,
            prefix="bienes_personas",
            instance=bienes_personas_data)
        copropietario_form = InfoPersonalVarForm(
            request.POST,
            prefix="copropietario",
            instance=copropietario_data)
        propietario_anterior_form = InfoPersonalVarForm(
            request.POST,
            prefix="propietario_anterior",
            instance=propietario_anterior_data)

        if (
            muebles_no_registrables_form.is_valid() and
            observaciones_form.is_valid() and
            bienes_personas_form.is_valid() and
            copropietario_form.is_valid() and
            propietario_anterior_form.is_valid()
            ):

            activos_bienes, created = ActivosBienes.objects.get_or_create(
                declaraciones=declaracion,
                cat_activo_bien_id=ActivosBienes.MUEBLES_NO_REGISTRABLES,
            )

            muebles_no_registrables = muebles_no_registrables_form.save(commit=False)
            observaciones = observaciones_form.save()

            copropietario = copropietario_form.save(commit=False)
            copropietario.declaraciones = declaracion
            copropietario.cat_tipo_persona_id = InfoPersonalVar.TIPO_COPROPIETARIO
            copropietario.save()
            propietario_anterior = propietario_anterior_form.save(commit=False)
            propietario_anterior.declaraciones = declaracion
            propietario_anterior.cat_tipo_persona_id = InfoPersonalVar.TIPO_PROPIETARIO_ANTERIOR
            propietario_anterior.save()

            muebles_no_registrables.declaraciones = declaracion
            muebles_no_registrables.activos_bienes = activos_bienes
            muebles_no_registrables.observaciones = observaciones
            muebles_no_registrables.save()

            activos_bienes.id_activobien = muebles_no_registrables.id
            activos_bienes.save()

            bienes_personas = bienes_personas_form.save(commit=False)
            bienes_personas.info_personal_var = info_personal_var
            bienes_personas.activos_bienes = activos_bienes
            bienes_personas.cat_tipo_participacion_id = BienesPersonas.DECLARANTE
            bienes_personas.save()

            propietario_anterior_bienes_personas, created = BienesPersonas.objects.update_or_create(
                info_personal_var=info_personal_var,
                otra_persona=propietario_anterior,
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.PROPIETARIO_ANTERIOR,
            )
            copropietario_bienes_personas, created = BienesPersonas.objects.update_or_create(
                info_personal_var=info_personal_var,
                otra_persona=copropietario,
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO,
            )
            if not agregar and not editar_id:
                status_obj, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA,
                    aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:muebles-noregistrables-agregar', folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return redirect('declaracion:inversiones',
                            folio=folio_declaracion)

        return render(request, self.template_name, {
            'form': muebles_no_registrables_form,
            'observaciones_form': observaciones_form,
            'bienes_personas_form': bienes_personas_form,
            'propietario_infopersonalvar_form': propietario_infopersonalvar_form,
            'otra_persona_form': otra_persona_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id
        })


class InversionesDeleteView(DeclaracionDeleteView):
    model = Inversiones


class InversionesView(View):
    template_name = 'declaracion/activos/inversiones.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0, None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        agregar, editar_id, inversiones_data, informacion_registrada = (
            declaracion_datos(kwargs, Inversiones, declaracion)
        )

        if inversiones_data:
            observaciones_data = inversiones_data.observaciones
            info_personal_var_data = inversiones_data.info_personal_var
            if info_personal_var_data:
                domicilios_data = info_personal_var_data.domicilios
            else:
                domicilios_data = {}
            observaciones_data = model_to_dict(observaciones_data)
            domicilios_data = model_to_dict(domicilios_data)
            inversiones_data = model_to_dict(inversiones_data)
            info_personal_var_data = model_to_dict(info_personal_var_data)
        else:
            observaciones_data = {}
            domicilios_data = {}
            inversiones_data = {}
            info_personal_var_data = {}

        inversiones_form = InversionesForm(
            prefix="inversiones",
            initial=inversiones_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)
        domicilio_form = DomiciliosForm(
            prefix="domicilio",
            initial=domicilios_data)
        info_personal_var_form = InfoPersonalVarForm(
            prefix="var",
            initial=info_personal_var_data)


        return render(request, self.template_name, {
            'form': inversiones_form,
            'domicilio_form': domicilio_form,
            'observaciones_form': observaciones_form,
            'info_personal_var_form': info_personal_var_form,
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
        avance, faltas = 0, None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
        except:
            raise Http404()

        agregar, editar_id, inversiones_data, informacion_registrada = (
            declaracion_datos(kwargs, Inversiones, declaracion)
        )

        if inversiones_data:
            observaciones_data = inversiones_data.observaciones
            info_personal_var_data = inversiones_data.info_personal_var
            domicilios_data = info_personal_var_data.domicilios
        else:
            observaciones_data = None
            domicilios_data = None
            inversiones_data = None
            info_personal_var_data = None

        inversiones_form = InversionesForm(
            request.POST,
            prefix="inversiones",
            instance=inversiones_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)
        domicilio_form = DomiciliosForm(
            request.POST,
            prefix="domicilio",
            instance=domicilios_data)
        info_personal_var_form = InfoPersonalVarForm(
            request.POST,
            prefix="var",
            instance=info_personal_var_data)


        inversiones_is_valid = inversiones_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()
        domicilio_is_valid = domicilio_form.is_valid()
        info_personal_var_is_valid = info_personal_var_form.is_valid()

        if (inversiones_is_valid and
            observaciones_is_valid and
            domicilio_is_valid and
            info_personal_var_is_valid):

            inversiones = inversiones_form.save(commit=False)
            observaciones = observaciones_form.save()
            domicilio = domicilio_form.save()

            info_personal_var = info_personal_var_form.save(commit=False)
            info_personal_var.declaraciones = declaracion
            info_personal_var.domicilios = domicilio
            info_personal_var.cat_tipo_persona_id = 7
            info_personal_var.save()

            inversiones.info_personal_var = info_personal_var
            inversiones.declaraciones = declaracion
            inversiones.observaciones = observaciones
            inversiones.save()

            if not agregar and not editar_id:
                status_obj, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA,
                    aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:inversiones-agregar', folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return redirect('declaracion:efectivo-metales',
                            folio=folio_declaracion)

        return render(request, self.template_name, {
            'form': inversiones_form,
            'observaciones_form': observaciones_form,
            'domicilio_form': domicilio_form,
            'info_personal_var_form': info_personal_var_form,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
        })


class EfectivoMetalesDeleteView(DeclaracionDeleteView):
    model = EfectivoMetales


class EfectivoMetalesView(View):
    template_name = 'declaracion/activos/efectivo-metales.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0, None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        agregar, editar_id, efectivo_metales_data, informacion_registrada = (
            declaracion_datos(kwargs, EfectivoMetales, declaracion)
        )

        if efectivo_metales_data:
            observaciones_data = efectivo_metales_data.observaciones
            observaciones_data = model_to_dict(observaciones_data)
            efectivo_metales_data = model_to_dict(efectivo_metales_data)
        else:
            efectivo_metales_data = {}
            observaciones_data = {}

        efectivo_metales_form = EfectivoMetalesForm(
            prefix="efectivo_metales",
            initial=efectivo_metales_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)

        return render(request, self.template_name, {
            'form': efectivo_metales_form,
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance,
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

        agregar, editar_id, efectivo_metales_data, informacion_registrada = (
            declaracion_datos(kwargs, EfectivoMetales, declaracion)
        )

        if efectivo_metales_data:
            observaciones_data = efectivo_metales_data.observaciones
        else:
            efectivo_metales_data = None
            observaciones_data = None

        efectivo_metales_form = EfectivoMetalesForm(
            request.POST,
            prefix="efectivo_metales",
            instance=efectivo_metales_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)

        efectivo_metales_is_valid = efectivo_metales_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()

        if (efectivo_metales_is_valid and
                observaciones_is_valid):
            efectivo_metales = efectivo_metales_form.save(commit=False)
            observaciones = observaciones_form.save()

            efectivo_metales.declaraciones = declaracion
            efectivo_metales.observaciones = observaciones
            efectivo_metales.save()

            if not agregar and not editar_id:
                status_obj, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA,
                    aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:efectivo-metales-agregar', folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return redirect('declaracion:fideicomisos',
                            folio=folio_declaracion)

        return render(request, self.template_name, {
            'form': efectivo_metales_form,
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
        })


class FideicomisosDeleteView(DeclaracionDeleteView):
    model = Fideicomisos


class FideicomisosView(View):
    template_name = 'declaracion/activos/fideicomisos.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0, None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        info_personal_var = InfoPersonalVar.objects.filter(
            declaraciones=declaracion,
            cat_tipo_persona_id=InfoPersonalVar.TIPO_DECLARANTE
        ).first()

        agregar, editar_id, fideicomisos_data, informacion_registrada = (
            declaracion_datos(kwargs, Fideicomisos, declaracion)
        )

        if fideicomisos_data:
            activos_bienes = ActivosBienes.objects.filter(
                declaraciones=declaracion,
                cat_activo_bien_id=ActivosBienes.FIDEICOMISOS,
            ).first()
            observaciones_data = fideicomisos_data.observaciones
            fideicomisos_data = model_to_dict(fideicomisos_data)
            observaciones_data = model_to_dict(observaciones_data)

            declarante_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.DECLARANTE,
            ).first()

            if declarante_bienes_personas:
                bienes_personas_data = model_to_dict(declarante_bienes_personas)
            else:
                bienes_personas_data = {}

            fideicomisario_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.FIDEICOMISARIO,
            ).first()

            if fideicomisario_bienes_personas:
                fideicomisario_data = fideicomisario_bienes_personas.otra_persona
                domicilio_fideicomisario_data = fideicomisario_data.domicilios
                fideicomisario_data = model_to_dict(fideicomisario_data)
                domicilio_fideicomisario_data = model_to_dict(domicilio_fideicomisario_data)
            else:
                fideicomisario_data = {}
                domicilio_fideicomisario_data = {}

            fideicomitente_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.FIDEICOMITENTE,
            ).first()

            if fideicomitente_bienes_personas:
                fideicomitente_data = fideicomitente_bienes_personas.otra_persona
                domicilio_fideicomitente_data = fideicomitente_data.domicilios
                fideicomitente_data = model_to_dict(fideicomitente_data)
                domicilio_fideicomitente_data = model_to_dict(domicilio_fideicomitente_data)
            else:
                fideicomitente_data = {}
                domicilio_fideicomitente_data = {}


            fiduciario_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.FIDUCIARIO,
            ).first()

            if fiduciario_bienes_personas:
                fiduciario_data = fiduciario_bienes_personas.otra_persona
                domicilio_fiduciario_data = fiduciario_data.domicilios
                fiduciario_data = model_to_dict(fiduciario_data)
                domicilio_fiduciario_data = model_to_dict(domicilio_fiduciario_data)
            else:
                fiduciario_data = {}
                domicilio_fiduciario_data = {}

        else:
            bienes_personas_data = {}
            fideicomisario_data = {}
            fideicomitente_data = {}
            fiduciario_data = {}
            domicilio_fideicomitente_data = {}
            domicilio_fideicomisario_data = {}
            domicilio_fiduciario_data = {}
            fideicomisos_data = {}
            observaciones_data = {}


        bienes_personas_form = BienesPersonasForm(
            prefix="bienes_personas",
            initial=bienes_personas_data)
        fideicomisario_form = InfoPersonalVarForm(
            prefix="fideicomisario",
            initial=fideicomisario_data)
        fideicomitente_form = InfoPersonalVarForm(
            prefix="fideicomitente",
            initial=fideicomitente_data)
        fiduciario_form = InfoPersonalVarForm(
            prefix="fiduciario",
            initial=fiduciario_data)
        domicilio_fideicomitente_form = DomiciliosForm(
            prefix="domicilio_fideicomitente",
            initial=domicilio_fideicomitente_data)
        domicilio_fideicomisario_form = DomiciliosForm(
            prefix="domicilio_fideicomisario",
            initial=domicilio_fideicomisario_data)
        domicilio_fiduciario_form = DomiciliosForm(
            prefix="domicilio_fiduciario",
            initial=domicilio_fiduciario_data)
        fideicomisos_form = FideicomisosForm(
            prefix="fideicomisos",
            initial=fideicomisos_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)

        return render(request, self.template_name, {
            'bienes_personas_form': bienes_personas_form,
            'fideicomisos_form': fideicomisos_form,
            'fideicomisario_form': fideicomisario_form,
            'fideicomitente_form': fideicomitente_form,
            'fiduciario_form': fiduciario_form,
            'domicilio_fideicomitente_form': domicilio_fideicomitente_form,
            'domicilio_fideicomisario_form': domicilio_fideicomisario_form,
            'domicilio_fiduciario_form': domicilio_fiduciario_form,
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

        info_personal_var = InfoPersonalVar.objects.filter(
            declaraciones=declaracion,
            cat_tipo_persona_id=1
        ).first()

        agregar, editar_id, fideicomisos_data, informacion_registrada = (
            declaracion_datos(kwargs, Fideicomisos, declaracion)
        )

        if fideicomisos_data:
            activos_bienes = ActivosBienes.objects.filter(
                declaraciones=declaracion,
                cat_activo_bien_id=ActivosBienes.FIDEICOMISOS,
            ).first()
            observaciones_data = fideicomisos_data.observaciones

            declarante_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.DECLARANTE,
            ).first()

            if declarante_bienes_personas:
                bienes_personas_data = declarante_bienes_personas
            else:
                bienes_personas_data = None

            fideicomisario_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.FIDEICOMISARIO,
            ).first()

            if fideicomisario_bienes_personas:
                fideicomisario_data = fideicomisario_bienes_personas.otra_persona
                domicilio_fideicomisario_data = fideicomisario_data.domicilios
            else:
                fideicomisario_data = None
                domicilio_fideicomisario_data = None

            fideicomitente_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.FIDEICOMITENTE,
            ).first()

            if fideicomitente_bienes_personas:
                fideicomitente_data = fideicomitente_bienes_personas.otra_persona
                domicilio_fideicomitente_data = fideicomitente_data.domicilios
            else:
                fideicomitente_data = None
                domicilio_fideicomitente_data = None

            fiduciario_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.FIDUCIARIO,
            ).first()

            if fiduciario_bienes_personas:
                fiduciario_data = fiduciario_bienes_personas.otra_persona
                domicilio_fiduciario_data = fiduciario_data.domicilios
            else:
                fiduciario_data = None
                domicilio_fiduciario_data = None

        else:
            bienes_personas_data = None
            fideicomisario_data = None
            fideicomitente_data = None
            fiduciario_data = None
            domicilio_fideicomitente_data = None
            domicilio_fideicomisario_data = None
            domicilio_fiduciario_data = None
            fideicomisos_data = None
            observaciones_data = None


        bienes_personas_form = BienesPersonasForm(
            request.POST,
            prefix="bienes_personas",
            instance=bienes_personas_data)
        fideicomisario_form = InfoPersonalVarForm(
            request.POST,
            prefix="fideicomisario",
            instance=fideicomisario_data)
        fideicomitente_form = InfoPersonalVarForm(
            request.POST,
            prefix="fideicomitente",
            instance=fideicomitente_data)
        fiduciario_form = InfoPersonalVarForm(
            request.POST,
            prefix="fiduciario",
            instance=fiduciario_data)
        domicilio_fideicomitente_form = DomiciliosForm(
            request.POST,
            prefix="domicilio_fideicomitente",
            instance=domicilio_fideicomitente_data)
        domicilio_fideicomisario_form = DomiciliosForm(
            request.POST,
            prefix="domicilio_fideicomisario",
            instance=domicilio_fideicomisario_data)
        domicilio_fiduciario_form = DomiciliosForm(
            request.POST,
            prefix="domicilio_fiduciario",
            instance=domicilio_fiduciario_data)
        fideicomisos_form = FideicomisosForm(
            request.POST,
            prefix="fideicomisos",
            instance=fideicomisos_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)

        if (bienes_personas_form.is_valid() and
            fideicomisario_form.is_valid() and
            fideicomitente_form.is_valid() and
            fiduciario_form.is_valid() and
            domicilio_fideicomitente_form.is_valid() and
            domicilio_fideicomisario_form.is_valid() and
            domicilio_fiduciario_form.is_valid() and
            fideicomisos_form.is_valid() and
            observaciones_form.is_valid()):

            fideicomisos = fideicomisos_form.save(commit=False)
            observaciones = observaciones_form.save()

            domicilio_fideicomitente = domicilio_fideicomitente_form.save()
            domicilio_fideicomisario = domicilio_fideicomisario_form.save()
            domicilio_fiduciario = domicilio_fiduciario_form.save()

            fideicomisario = fideicomisario_form.save(commit=False)
            fideicomitente = fideicomitente_form.save(commit=False)
            fiduciario = fiduciario_form.save(commit=False)

            fideicomisario.domicilios = domicilio_fideicomisario
            fideicomisario.cat_tipo_persona_id = 8
            fideicomisario.declaraciones = declaracion
            fideicomisario.save()
            fideicomitente.domicilios = domicilio_fideicomitente
            fideicomitente.cat_tipo_persona_id = 9
            fideicomitente.declaraciones = declaracion
            fideicomitente.save()
            fiduciario.domicilios = domicilio_fiduciario
            fiduciario.cat_tipo_persona_id = 10
            fiduciario.declaraciones = declaracion
            fiduciario.save()


            activos_bienes, created = ActivosBienes.objects.update_or_create(
                declaraciones=declaracion,
                cat_activo_bien_id=ActivosBienes.FIDEICOMISOS,
            )

            fideicomisos.observaciones = observaciones
            fideicomisos.activos_bienes = activos_bienes
            fideicomisos.declaraciones = declaracion
            fideicomisos.save()

            activos_bienes.id_activobien = fideicomisos.id
            activos_bienes.save()

            declarante_bienes_personas, created = BienesPersonas.objects.update_or_create(
                info_personal_var=info_personal_var,
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.DECLARANTE,
                defaults={'porcentaje': bienes_personas_form.cleaned_data['porcentaje']},
            )

            fideicomisario_bienes_personas, created = BienesPersonas.objects.update_or_create(
                info_personal_var=info_personal_var,
                otra_persona=fideicomisario,
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.FIDEICOMISARIO,
            )

            fideicomitente_bienes_personas, created = BienesPersonas.objects.update_or_create(
                info_personal_var=info_personal_var,
                otra_persona=fideicomitente,
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.FIDEICOMITENTE,
            )

            fiduciario_bienes_personas, created = BienesPersonas.objects.update_or_create(
                info_personal_var=info_personal_var,
                otra_persona=fiduciario,
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.FIDUCIARIO,
            )

            if not agregar and not editar_id:
                status_obj, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA,
                    aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:fideicomisos-agregar', folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return redirect('declaracion:bienes-intangibles',
                            folio=folio_declaracion)

        return render(request, self.template_name, {
            'bienes_personas_form': bienes_personas_form,
            'fideicomisos_form': fideicomisos_form,
            'fideicomisario_form': fideicomisario_form,
            'fideicomitente_form': fideicomitente_form,
            'fiduciario_form': fiduciario_form,
            'domicilio_fideicomitente_form': domicilio_fideicomitente_form,
            'domicilio_fideicomisario_form': domicilio_fideicomisario_form,
            'domicilio_fiduciario_form': domicilio_fiduciario_form,
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
        })


class BienesIntangiblesDeleteView(DeclaracionDeleteView):
    model = BienesIntangibles


class BienesIntangiblesView(View):
    template_name = 'declaracion/activos/bienes-intangibles.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0, None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        info_personal_var = InfoPersonalVar.objects.filter(
            declaraciones=declaracion,
            cat_tipo_persona_id=InfoPersonalVar.TIPO_DECLARANTE
        ).first()

        agregar, editar_id, bienes_intangibles_data, informacion_registrada = (
            declaracion_datos(kwargs, BienesIntangibles, declaracion)
        )

        if bienes_intangibles_data:
            activos_bienes = ActivosBienes.objects.filter(
                declaraciones=declaracion,
                cat_activo_bien_id=ActivosBienes.BIENES_INTANGIBLES,
            ).first()
            observaciones_data = bienes_intangibles_data.observaciones
            bienes_intangibles_data = model_to_dict(bienes_intangibles_data)
            observaciones_data = model_to_dict(observaciones_data)

            declarante_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.DECLARANTE,
            ).first()

            if declarante_bienes_personas:
                bienes_personas_data = model_to_dict(declarante_bienes_personas)
            else:
                bienes_personas_data = {}

            propietario_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                es_propietario=True,
                cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO,
            ).first()
            if propietario_bienes_personas:
                propietario_data = propietario_bienes_personas.otra_persona
                propietario_data = model_to_dict(propietario_data)
            else:
                propietario_data = {}


            copropietario_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO,
            ).first()
            if copropietario_bienes_personas:
                copropietario_data = copropietario_bienes_personas.otra_persona
                copropietario_data = model_to_dict(copropietario_data)
                copropietario_bienes_personas = model_to_dict(copropietario_bienes_personas)
            else:
                copropietario_data = {}
                copropietario_bienes_personas = {}

        else:
            bienes_intangibles_data = {}
            observaciones_data = {}
            propietario_data = {}
            bienes_personas_data = {}
            copropietario_data = {}
            copropietario_bienes_personas = {}
            bienes_personas_data = {}


        bienes_intangibles_form = BienesIntangiblesForm(
            prefix="bienes_intangibles",
            initial=bienes_intangibles_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)
        propietario_form = InfoPersonalVarForm(
            prefix="propietario",
            initial=propietario_data)
        copropietario_form = InfoPersonalVarForm(
            prefix="copropietario",
            initial=copropietario_data)
        copropietario_bienes_personas_form = BienesPersonasForm(
            prefix="copropietario_bienes_personas",
            initial=copropietario_bienes_personas)
        bienes_personas_form = BienesPersonasForm(
            prefix="bienes_personas",
            initial=bienes_personas_data)

        return render(request, self.template_name, {
            'bienes_intangibles_form': bienes_intangibles_form,
            'observaciones_form': observaciones_form,
            'copropietario_form': copropietario_form,
            'copropietario_bienes_personas_form': copropietario_bienes_personas_form,
            'propietario_form': propietario_form,
            'bienes_personas_form': bienes_personas_form,
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

        info_personal_var = InfoPersonalVar.objects.filter(
            declaraciones=declaracion,
            cat_tipo_persona_id=InfoPersonalVar.TIPO_DECLARANTE
        ).first()

        agregar, editar_id, bienes_intangibles_data, informacion_registrada = (
            declaracion_datos(kwargs, BienesIntangibles, declaracion)
        )

        if bienes_intangibles_data:
            activos_bienes = ActivosBienes.objects.filter(
                declaraciones=declaracion,
                cat_activo_bien_id=ActivosBienes.BIENES_INTANGIBLES,
            ).first()
            observaciones_data = bienes_intangibles_data.observaciones
            declarante_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.DECLARANTE,
            ).first()

            if declarante_bienes_personas:
                bienes_personas_data = declarante_bienes_personas
            else:
                bienes_personas_data = None

            propietario_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                es_propietario=True,
                cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO,
            ).first()
            if propietario_bienes_personas:
                propietario_data = propietario_bienes_personas.otra_persona
            else:
                propietario_data = None


            copropietario_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO,
            ).first()
            if copropietario_bienes_personas:
                copropietario_data = copropietario_bienes_personas.otra_persona
            else:
                copropietario_data = None
                copropietario_bienes_personas = None

        else:
            bienes_intangibles_data = None
            observaciones_data = None
            propietario_data = None
            bienes_personas_data = None
            copropietario_data = None
            copropietario_bienes_personas = None
            bienes_personas_data = None


        bienes_intangibles_form = BienesIntangiblesForm(
            request.POST,
            prefix="bienes_intangibles",
            instance=bienes_intangibles_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)
        propietario_form = InfoPersonalVarForm(
            request.POST,
            prefix="propietario",
            instance=propietario_data)
        copropietario_form = InfoPersonalVarForm(
            request.POST,
            prefix="copropietario",
            instance=copropietario_data)
        copropietario_bienes_personas_form = BienesPersonasForm(
            request.POST,
            prefix="copropietario_bienes_personas",
            instance=copropietario_bienes_personas)
        bienes_personas_form = BienesPersonasForm(
            request.POST,
            prefix="bienes_personas",
            instance=bienes_personas_data)

        if (
            bienes_intangibles_form.is_valid() and
            observaciones_form.is_valid() and
            propietario_form.is_valid() and
            copropietario_form.is_valid() and
            copropietario_bienes_personas_form.is_valid() and
            bienes_personas_form.is_valid()
            ):

            activos_bienes, created = ActivosBienes.objects.get_or_create(
                declaraciones=declaracion,
                cat_activo_bien_id=ActivosBienes.BIENES_INTANGIBLES,
            )

            bienes_intangibles = bienes_intangibles_form.save(commit=False)
            observaciones = observaciones_form.save()

            propietario = propietario_form.save(commit=False)
            propietario.declaraciones = declaracion
            propietario.cat_tipo_persona_id = InfoPersonalVar.TIPO_COPROPIETARIO
            propietario.save()

            copropietario = copropietario_form.save(commit=False)
            copropietario.declaraciones = declaracion
            copropietario.cat_tipo_persona_id = InfoPersonalVar.TIPO_COPROPIETARIO
            copropietario.save()

            bienes_intangibles.activos_bienes = activos_bienes
            bienes_intangibles.declaraciones = declaracion
            bienes_intangibles.observaciones = observaciones
            bienes_intangibles.save()

            activos_bienes.id_activobien = bienes_intangibles.id
            activos_bienes.save()

            bienes_personas = bienes_personas_form.save(commit=False)
            bienes_personas.info_personal_var = info_personal_var
            bienes_personas.declaraciones = declaracion
            bienes_personas.activos_bienes = activos_bienes
            bienes_personas.cat_tipo_participacion_id = BienesPersonas.DECLARANTE
            bienes_personas.save()

            copropietario_bienes_personas = copropietario_bienes_personas_form.save(commit=False)
            copropietario_bienes_personas.info_personal_var = info_personal_var
            copropietario_bienes_personas.declaraciones = declaracion
            copropietario_bienes_personas.activos_bienes = activos_bienes
            copropietario_bienes_personas.cat_tipo_participacion_id = BienesPersonas.COPROPIETARIO
            copropietario_bienes_personas.otra_persona = copropietario
            copropietario_bienes_personas.save()

            propietario_bienes_personas, created = BienesPersonas.objects.update_or_create(
                info_personal_var=info_personal_var,
                otra_persona=propietario,
                activos_bienes=activos_bienes,
                es_propietario=True,
                cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO,
            )

            if not agregar and not editar_id:
                status_obj, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA,
                    aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:bienes-intangibles-agregar', folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return redirect('declaracion:cuentas-por-cobrar',
                            folio=folio_declaracion)

        return render(request, self.template_name, {
            'bienes_intangibles_form': bienes_intangibles_form,
            'observaciones_form': observaciones_form,
            'copropietario_form': copropietario_form,
            'copropietario_bienes_personas_form': copropietario_bienes_personas_form,
            'propietario_form': propietario_form,
            'bienes_personas_form': bienes_personas_form,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
        })


class CuentasPorCobrarDeleteView(DeclaracionDeleteView):
    model = CuentasPorCobrar


class CuentasPorCobrarView(View):
    template_name = 'declaracion/activos/cuentas-porcobrar.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0, None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        info_personal_var = InfoPersonalVar.objects.filter(
            declaraciones=declaracion,
            cat_tipo_persona_id=InfoPersonalVar.TIPO_DECLARANTE
        ).first()

        agregar, editar_id, cuentas_porcobrar_data, informacion_registrada = (
            declaracion_datos(kwargs, CuentasPorCobrar, declaracion)
        )
        if cuentas_porcobrar_data:
            activos_bienes = ActivosBienes.objects.filter(
                declaraciones=declaracion,
                cat_activo_bien_id=ActivosBienes.CUENTAS_POR_COBRAR,
            ).first()
            observaciones_data = cuentas_porcobrar_data.observaciones
            cuentas_porcobrar_data = model_to_dict(cuentas_porcobrar_data)
            observaciones_data = model_to_dict(observaciones_data)

            declarante_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.DECLARANTE,
            ).first()

            if declarante_bienes_personas:
                bienes_personas_data = model_to_dict(declarante_bienes_personas)
            else:
                bienes_personas_data = {}

            copropietario_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO,
            ).first()
            if copropietario_bienes_personas:
                copropietario_data = copropietario_bienes_personas.otra_persona
                copropietario_data = model_to_dict(copropietario_data)
            else:
                copropietario_data = {}

            prestatario_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.PRESTATARIO_O_DEUDOR,
            ).first()
            if prestatario_bienes_personas:
                prestatario_data = prestatario_bienes_personas.otra_persona
                prestatario_domicilio_data = prestatario_data.domicilios
                prestatario_data = model_to_dict(prestatario_data)
                domicilios_data = model_to_dict(prestatario_domicilio_data)
            else:
                prestatario_data = {}
                domicilios_data = {}
        else:
            cuentas_porcobrar_data = {}
            observaciones_data = {}
            domicilios_data = {}
            bienes_personas_data = {}
            copropietario_data = {}
            prestatario_data = {}


        cuentas_porcobrar_form = CuentasPorCobrarForm(
            prefix="cuentas_porcobrar",
            initial=cuentas_porcobrar_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)
        domicilio_form = DomiciliosForm(
            prefix="domicilio",
            initial=domicilios_data)
        bienes_personas_form = BienesPersonasForm(
            prefix="bienes_personas",
            initial=bienes_personas_data)
        copropietario_form = InfoPersonalVarForm(
            prefix="copropietario",
            initial=copropietario_data)
        prestatario_form = InfoPersonalVarForm(
            prefix="prestatario",
            initial=prestatario_data)

        return render(request, self.template_name, {
            'cuentas_porcobrar_form': cuentas_porcobrar_form,
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'bienes_personas_form': bienes_personas_form,
            'copropietario_form': copropietario_form,
            'prestatario_form': prestatario_form,
            'domicilio_form':domicilio_form,
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

        info_personal_var = InfoPersonalVar.objects.filter(
            declaraciones=declaracion,
            cat_tipo_persona_id=InfoPersonalVar.TIPO_DECLARANTE
        ).first()

        agregar, editar_id, cuentas_porcobrar_data, informacion_registrada = (
            declaracion_datos(kwargs, CuentasPorCobrar, declaracion)
        )
        if cuentas_porcobrar_data:
            activos_bienes = ActivosBienes.objects.filter(
                declaraciones=declaracion,
                cat_activo_bien_id=ActivosBienes.CUENTAS_POR_COBRAR,
            ).first()
            observaciones_data = cuentas_porcobrar_data.observaciones

            declarante_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.DECLARANTE,
            ).first()

            if declarante_bienes_personas:
                bienes_personas_data = declarante_bienes_personas
            else:
                bienes_personas_data = None

            copropietario_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO,
            ).first()
            if copropietario_bienes_personas:
                copropietario_data = copropietario_bienes_personas.otra_persona
            else:
                copropietario_data = None

            prestatario_bienes_personas = BienesPersonas.objects.filter(
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.PRESTATARIO_O_DEUDOR,
            ).first()
            if prestatario_bienes_personas:
                prestatario_data = prestatario_bienes_personas.otra_persona
                domicilios_data = prestatario_data.domicilios
            else:
                prestatario_data = None
                domicilios_data = None
        else:
            cuentas_porcobrar_data = None
            observaciones_data = None
            domicilios_data = None
            bienes_personas_data = None
            copropietario_data = None
            prestatario_data = None


        cuentas_porcobrar_form = CuentasPorCobrarForm(
            request.POST,
            prefix="cuentas_porcobrar",
            instance=cuentas_porcobrar_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)
        domicilio_form = DomiciliosForm(
            request.POST,
            prefix="domicilio",
            instance=domicilios_data)
        bienes_personas_form = BienesPersonasForm(
            request.POST,
            prefix="bienes_personas",
            instance=bienes_personas_data)
        copropietario_form = InfoPersonalVarForm(
            request.POST,
            prefix="copropietario",
            instance=copropietario_data)
        prestatario_form = InfoPersonalVarForm(
            request.POST,
            prefix="prestatario",
            instance=prestatario_data)


        if (
            cuentas_porcobrar_form.is_valid() and
            observaciones_form.is_valid() and
            domicilio_form.is_valid() and
            bienes_personas_form.is_valid() and
            copropietario_form.is_valid() and
            prestatario_form.is_valid()
            ):

            activos_bienes, created = ActivosBienes.objects.get_or_create(
                declaraciones=declaracion,
                cat_activo_bien_id=ActivosBienes.CUENTAS_POR_COBRAR,
            )

            cuentas_porcobrar = cuentas_porcobrar_form.save(commit=False)
            observaciones = observaciones_form.save()

            copropietario = copropietario_form.save(commit=False)
            copropietario.declaraciones = declaracion
            copropietario.cat_tipo_persona_id = InfoPersonalVar.TIPO_COPROPIETARIO
            copropietario.save()

            domicilio = domicilio_form.save()
            prestatario = prestatario_form.save(commit=False)
            prestatario.declaraciones = declaracion
            prestatario.domicilios = domicilio
            prestatario.cat_tipo_persona_id = InfoPersonalVar.TIPO_PRESTATARIO
            prestatario.save()

            cuentas_porcobrar.declaraciones = declaracion
            cuentas_porcobrar.activos_bienes = activos_bienes
            cuentas_porcobrar.observaciones = observaciones
            cuentas_porcobrar.save()

            activos_bienes.id_activobien = cuentas_porcobrar.id
            activos_bienes.save()

            bienes_personas = bienes_personas_form.save(commit=False)
            bienes_personas.info_personal_var = info_personal_var
            bienes_personas.activos_bienes = activos_bienes
            bienes_personas.cat_tipo_participacion_id = BienesPersonas.DECLARANTE
            bienes_personas.save()

            prestatario_bienes_personas, created = BienesPersonas.objects.update_or_create(
                info_personal_var=info_personal_var,
                otra_persona=prestatario,
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.PRESTATARIO_O_DEUDOR,
            )
            copropietario_bienes_personas, created = BienesPersonas.objects.update_or_create(
                info_personal_var=info_personal_var,
                otra_persona=copropietario,
                activos_bienes=activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO,
            )

            if not agregar and not editar_id:
                status_obj, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA,
                    aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:cuentas-por-cobrar-agregar', folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return redirect('declaracion:beneficios-especie',
                            folio=folio_declaracion)

        return render(request, self.template_name, {
            'cuentas_porcobrar_form': cuentas_porcobrar_form,
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'bienes_personas_form': bienes_personas_form,
            'copropietario_form': copropietario_form,
            'prestatario_form': prestatario_form,
            'domicilio_form':domicilio_form,
            'avance':declaracion.avance,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
        })


class BeneficiosEspecieDeleteView(DeclaracionDeleteView):
    model = BeneficiosEspecie


class BeneficiosEspecieView(View):
    template_name = 'declaracion/activos/beneficios-especie.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0, None
        try:
            declaracion = validar_declaracion(request, folio_declaracion)
            avance, faltas = obtiene_avance(declaracion)
        except:
            raise Http404()

        agregar, editar_id, beneficios_especie_data, informacion_registrada = (
            declaracion_datos(kwargs, BeneficiosEspecie, declaracion)
        )

        if beneficios_especie_data:
            observaciones_data = beneficios_especie_data.observaciones
            domicilios_data = beneficios_especie_data.domicilios
            info_personal_var = beneficios_especie_data.info_personal_var
            observaciones_data = model_to_dict(observaciones_data)
            domicilios_data = model_to_dict(domicilios_data)
            beneficios_especie_data = model_to_dict(beneficios_especie_data)
            info_personal_var_data = model_to_dict(info_personal_var)
        else:
            observaciones_data = {}
            domicilios_data = {}
            beneficios_especie_data = {}
            info_personal_var_data = {}

        beneficios_especie_form = BeneficiosEspecieForm(
            prefix="beneficios_especie",
            initial=beneficios_especie_data)
        observaciones_form = ObservacionesForm(
            prefix="observaciones",
            initial=observaciones_data)
        domicilio_form = DomiciliosForm(
            prefix="domicilio",
            initial=domicilios_data)
        info_personal_var_form = InfoPersonalVarForm(
            prefix="var",
            initial=info_personal_var_data)

        return render(request, self.template_name, {
            'form': beneficios_especie_form,
            'domicilio_form': domicilio_form,
            'observaciones_form': observaciones_form,
            'info_personal_var_form': info_personal_var_form,
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

        agregar, editar_id, beneficios_especie_data, informacion_registrada = (
            declaracion_datos(kwargs, BeneficiosEspecie, declaracion)
        )
        if beneficios_especie_data:
            observaciones_data = beneficios_especie_data.observaciones
            domicilios_data = beneficios_especie_data.domicilios
            info_personal_var_data = beneficios_especie_data.info_personal_var
        else:
            observaciones_data = None
            domicilios_data = None
            beneficios_especie_data = None
            info_personal_var_data = None

        beneficios_especie_form = BeneficiosEspecieForm(
            request.POST,
            prefix="beneficios_especie",
            instance=beneficios_especie_data)
        observaciones_form = ObservacionesForm(
            request.POST,
            prefix="observaciones",
            instance=observaciones_data)
        domicilio_form = DomiciliosForm(
            request.POST,
            prefix="domicilio",
            instance=domicilios_data)
        info_personal_var_form = InfoPersonalVarForm(
            request.POST,
            prefix="var",
            instance=info_personal_var_data)

        beneficios_especie_is_valid = beneficios_especie_form.is_valid()
        observaciones_is_valid = observaciones_form.is_valid()
        domicilio_is_valid = domicilio_form.is_valid()
        info_personal_var_is_valid = info_personal_var_form.is_valid()

        if (beneficios_especie_is_valid and
            observaciones_is_valid and
            domicilio_is_valid and
            info_personal_var_is_valid):

            beneficios_especie = beneficios_especie_form.save(commit=False)
            observaciones = observaciones_form.save()
            domicilio = domicilio_form.save()
            info_personal_var = info_personal_var_form.save(commit=False)
            info_personal_var.declaraciones = declaracion
            info_personal_var.save()
            beneficios_especie.info_personal_var = info_personal_var
            beneficios_especie.declaraciones = declaracion
            beneficios_especie.domicilios = domicilio
            beneficios_especie.observaciones = observaciones
            beneficios_especie.save()

            if not agregar and not editar_id:
                status_obj, status_created = guardar_estatus(
                    request,
                    declaracion.folio,
                    SeccionDeclaracion.COMPLETA,
                    aplica=no_aplica(request))

            if request.POST.get("accion") == "guardar_otro":
                return redirect('declaracion:beneficios-especie-agregar', folio=folio_declaracion)
            if request.POST.get("accion") == "guardar_salir":
                return redirect('declaracion:perfil')

            return redirect('declaracion:activos-observaciones',
                            folio=folio_declaracion)

        return render(request, self.template_name, {
            'form': beneficios_especie_form,
            'observaciones_form': observaciones_form,
            'domicilio_form': domicilio_form,
            'info_personal_var_form': info_personal_var_form,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance,
            'informacion_registrada': informacion_registrada,
            'agregar': agregar,
            'editar_id': editar_id,
        })


class ActivosObservacionesView(View):
    template_name = 'declaracion/activos/observaciones.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        folio_declaracion = self.kwargs['folio']
        avance, faltas = 0, None
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
            'faltas':faltas,
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

        observaciones_form = ObservacionesForm(request.POST,
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

            return redirect('declaracion:deudas', folio=folio_declaracion)

        return render(request, self.template_name, {
            'observaciones_form': observaciones_form,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance
        })
