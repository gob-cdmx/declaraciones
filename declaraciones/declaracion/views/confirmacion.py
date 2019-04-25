import uuid
import base64
import requests
from datetime import datetime
from django.views import View
from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from declaracion.models import (Declaraciones, InfoPersonalVar,
                                InfoPersonalFija, DatosCurriculares, Encargos,
                                ExperienciaLaboral, ConyugeDependientes,
                                Observaciones, SeccionDeclaracion, Secciones)
from declaracion.forms import ConfirmacionForm
from .utils import validar_declaracion
from django.conf import settings

class ConfimacionInformacionPersonalView(View):
    template_name = "declaracion/confirmacion/informacion_personal.html"

    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):
        usuario = request.user

        try:
            folio_declaracion = self.kwargs['folio']
            declaracion = Declaraciones.objects.filter(folio=uuid.UUID(folio_declaracion), info_personal_fija__usuario=request.user).all()[0]
        except Exception as e:
            folio_declaracion = None

        if folio_declaracion:
            info_personal_var = InfoPersonalVar.objects.filter(declaraciones=declaracion).first()
            info_personal_fija = InfoPersonalFija.objects.filter(declaraciones=declaracion).first()
            datos_curriculares = DatosCurriculares.objects.filter(declaraciones=declaracion).first()
            encargos = Encargos.objects.filter(declaraciones=declaracion).first()
            experiecia_laboral = ExperienciaLaboral.objects.filter(declaraciones=declaracion).first()
            conyuge_dependientes = ConyugeDependientes.objects.filter(declaraciones=declaracion).first()

            seccion_id = Secciones.objects.filter(url='informacion-personal-observaciones').first()
            seccion = SeccionDeclaracion.objects.filter(declaraciones=declaracion, seccion=seccion_id).first()
            if seccion:
                observaciones = seccion.observaciones
            else:
                observaciones = ''
        else:
            declaracion = {}
            info_personal_var = {}
            info_personal_fija = {}
            datos_curriculares = {}
            encargos = {}
            experiecia_laboral = {}
            conyuge_dependientes = {}

        return render(request,self.template_name, {
            'declaracion': declaracion,
            'info_personal_var': info_personal_var,
            'info_personal_fija': info_personal_fija,
            'datos_curriculares': datos_curriculares,
            'encargos': encargos,
            'experiecia_laboral': experiecia_laboral,
            'conyuge_dependientes': conyuge_dependientes,
            'observaciones': observaciones,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance
        })


class ConfimacionInteresesView(View):
    template_name = "declaracion/confirmacion/intereses.html"

    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):
        usuario = request.user

        try:
            folio_declaracion = self.kwargs['folio']
            declaracion = Declaraciones.objects.filter(folio=uuid.UUID(folio_declaracion),info_personal_fija__usuario=request.user).all()[0]
            activas = declaracion.representaciones_set.filter(es_representacion_activa=True).all()
            pasivas = declaracion.representaciones_set.filter(es_representacion_activa=False).all()

            seccion_id = Secciones.objects.filter(url='intereses-observaciones').first()
            seccion = SeccionDeclaracion.objects.filter(declaraciones=declaracion, seccion=seccion_id).first()
            if seccion:
                observaciones = seccion.observaciones
            else:
                observaciones = ''

        except Exception as e:
            folio_declaracion = ''
            declaracion = {}

        return render(request,self.template_name, {
            'declaracion': declaracion,
            'activas': activas,
            'pasivas': pasivas,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance,
            'observaciones': observaciones,
        })


class ConfimacionPasivosView(View):
    template_name = "declaracion/confirmacion/pasivos.html"

    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):
        usuario = request.user

        try:
            folio_declaracion = self.kwargs['folio']
            declaracion = Declaraciones.objects.filter(folio=uuid.UUID(folio_declaracion),info_personal_fija__usuario=request.user).all()[0]
            seccion_id = Secciones.objects.filter(url='pasivos-observaciones').first()
            seccion = SeccionDeclaracion.objects.filter(declaraciones=declaracion, seccion=seccion_id).first()
            if seccion:
                observaciones = seccion.observaciones
            else:
                observaciones = ''

        except Exception as e:
            folio_declaracion = ''
            declaracion = {}

        confirmacion = ConfirmacionForm()

        return render(request,self.template_name, {
            'declaracion': declaracion,
            'folio_declaracion': folio_declaracion,
            'observaciones': observaciones,
            'confirmacion': confirmacion,
            'avance':declaracion.avance
        })


class ConfimacionIngresosView(View):
    template_name = "declaracion/confirmacion/ingresos.html"

    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):
        usuario = request.user

        try:
            folio_declaracion = self.kwargs['folio']
            declaracion = Declaraciones.objects.filter(folio=uuid.UUID(folio_declaracion),info_personal_fija__usuario=request.user).all()[0]
            sueldos = declaracion.ingresosvarios_set.filter(cat_tipos_ingresos_varios_id=1).all()
            profesional = declaracion.ingresosvarios_set.filter(cat_tipos_ingresos_varios_id=2).all()
            empresarial = declaracion.ingresosvarios_set.filter(cat_tipos_ingresos_varios_id=3).all()
            menor = declaracion.ingresosvarios_set.filter(cat_tipos_ingresos_varios_id=4).all()
            arrendamiento = declaracion.ingresosvarios_set.filter(cat_tipos_ingresos_varios_id=5).all()
            intereses = declaracion.ingresosvarios_set.filter(cat_tipos_ingresos_varios_id=6).all()
            premios = declaracion.ingresosvarios_set.filter(cat_tipos_ingresos_varios_id=7).all()
            bienes = declaracion.ingresosvarios_set.filter(cat_tipos_ingresos_varios_id=8).all()
            otros = declaracion.ingresosvarios_set.filter(cat_tipos_ingresos_varios_id=9).all()

            seccion_id = Secciones.objects.filter(url='ingresos-observaciones').first()
            seccion = SeccionDeclaracion.objects.filter(declaraciones=declaracion, seccion=seccion_id).first()
            if seccion:
                observaciones = seccion.observaciones
            else:
                observaciones = ''

        except Exception as e:
            folio_declaracion = ''
            declaracion = {}

        return render(request,self.template_name, {
            'declaracion': declaracion,
            'folio_declaracion': folio_declaracion,
            'sueldos': sueldos,
            'profesional': profesional,
            'empresarial': empresarial,
            'menor': menor,
            'arrendamiento': arrendamiento,
            'intereses': intereses,
            'premios': premios,
            'bienes': bienes,
            'otros': otros,
            'observaciones': observaciones,
            'avance':declaracion.avance
        })


class ConfimacionActivosView(View):
    template_name = "declaracion/confirmacion/activos.html"

    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):
        usuario = request.user

        try:
            folio_declaracion = self.kwargs['folio']
            declaracion = Declaraciones.objects.filter(folio=uuid.UUID(folio_declaracion),info_personal_fija__usuario=request.user).all()[0]
            seccion_id = Secciones.objects.filter(url='activos-observaciones').first()
            seccion = SeccionDeclaracion.objects.filter(declaraciones=declaracion, seccion=seccion_id).first()
            if seccion:
                observaciones = seccion.observaciones
            else:
                observaciones = ''

        except Exception as e:
            folio_declaracion = ''
            declaracion = {}

        return render(request,self.template_name, {
            'declaracion': declaracion,
            'observaciones': observaciones,
            'folio_declaracion': folio_declaracion,
            'avance':declaracion.avance
        })


class ConfirmarDeclaracionView(View):
    def get(self, request, *args, **kwargs):
        raise Http404()

    @method_decorator(login_required(login_url='/login'))
    def post(self, request, *args, **kwargs):
        try:
            folio_declaracion = self.kwargs['folio']
            declaracion = validar_declaracion(request, folio_declaracion)
        except Exception as e:
            raise Http404()

        try:
            confirmacion = ConfirmacionForm(request.POST, request.FILES)
            if confirmacion.is_valid():
                byteKey = base64.b64encode(
                    request.FILES['key'].read()).decode('utf-8')
                bytecer = base64.b64encode(
                    request.FILES['cer'].read()).decode('utf-8')
                password = base64.b64encode(
                    request.POST['password'].encode('utf-8')).decode('utf-8')

                firma = {
                  "security": {
                    "tokenId": settings.TOKEN_ID
                  },
                  "data": {
                    "password": password,
                    "cadena": str(declaracion.folio),
                    "byteKey": byteKey,
                    "bytecer": bytecer
                  }
                }
                url = settings.FIRMA_URL

                r = requests.post(url, json=firma)
                response = r.json()
                if response['error']['code'] == 0:
                    declaracion.cat_estatus_id = 4
                    declaracion.sello = response['data']['sello']
                    declaracion.fecha_recepcion = response['data']['fechaFirma']
                    declaracion.save()
                    return redirect('declaraciones-previas')
                else:
                    messages.warning(request, u"Error de autenticación")
                    return redirect('declaracion:confirmacion-pasivos', folio=declaracion.folio)
            else:
                for key, error in confirmacion.errors.items():
                    messages.warning(request, error)
            return redirect('declaracion:confirmacion-pasivos', folio=declaracion.folio)
        except Exception as e:
            print (e)
            return redirect('declaracion:confirmacion-pasivos', folio=declaracion.folio)
