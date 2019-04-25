import uuid
import json
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView
from django.http import Http404, JsonResponse
from declaracion.models import Declaraciones,InfoPersonalFija
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q

class DeclaracionView(TemplateView):
    template_name = "declaracion/index.html"
    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):
        try:
            declaracion = Declaraciones.objects.filter(
                info_personal_fija=InfoPersonalFija.objects.filter(usuario=request.user).first()).filter(
                Q(cat_estatus__isnull=True) | Q(cat_estatus__pk__in=(1, 2, 3))).first()

        except:
            declaracion = None

        return render(request,self.template_name,{'declaracion':declaracion})


class DeclaracionDeleteView(DeleteView):
    def get(self, request, *args,**kwargs):
        raise Http404("")

    def get_object(self, queryset=None):
        try:
            folio_declaracion = self.kwargs['folio']
            pk = self.kwargs['pk']
            declaracion_obj = Declaraciones.objects.filter(
                folio=uuid.UUID(folio_declaracion),
                info_personal_fija__usuario=self.request.user
                ).first()
            registros = self.model.objects.filter(
                pk=pk,
                declaraciones=declaracion_obj
                ).first()
        except Exception as e:
            print (e)
            raise Http404("")
        return registros

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return JsonResponse({'delete': 'ok'})
