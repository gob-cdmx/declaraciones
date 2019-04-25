from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import View

from declaracion.models import Declaraciones
from datetime import datetime
from django.core.paginator import Paginator
from django.shortcuts import render

class RegistrosView(View):
    template_name = "reportes/publico.json.html"


    def get(self, request, *args, **kwargs):
        api_key = request.GET.get('api_key')
        sort = request.GET.get('sort')
        page = request.GET.get('page')
        page_size = request.GET.get('page_size')
        nombres = request.GET.get('nombres')
        apellido1 = request.GET.get('apellido1')
        apellido2 = request.GET.get('apellido2')
        rfc = request.GET.get('rfc')
        curp = request.GET.get('rfc')

        id = request.GET.get('id')
        actualizacion = request.GET.get('actualizacion')
        rfc_solicitante = request.GET.get('rfc_solicitante')
        filter = False


        declaraciones = Declaraciones.objects
        if id and id != "":
            declaraciones = declaraciones.filter(folio=id)
            filter=True
        if rfc and rfc != "":
            declaraciones = declaraciones.filter(info_personal_fija__rfc=rfc.upper())
            filter=True
        if curp and curp != "":
            declaraciones = declaraciones.filter(info_personal_fija__curp=curp.upper())
            filter = True
        if nombres and nombres != "":
            declaraciones = declaraciones.filter(info_personal_fija__nombres__contains=nombres.upper())
            filter = True
        if apellido1 and apellido1 != "":
            declaraciones = declaraciones.filter(info_personal_fija__apellido1__contains=apellido1.upper())
            filter = True
        if apellido2 and apellido2 != "":
            declaraciones = declaraciones.filter(info_personal_fija__apellido2__contains=apellido2.upper())
            filter = True
        if sort and sort.upper() == "ASC":
            declaraciones = declaraciones.order_by('fecha_declaracion')
            filter = True
        elif sort and sort.upper() == "DESC":
            declaraciones = declaraciones.order_by('-fecha_declaracion')
            filter = True
        if actualizacion and actualizacion != "":
            actualizacion = datetime.strptime(actualizacion, "%Y-%m-%d")
            declaraciones = declaraciones.filter(fecha_declaracion__gte=actualizacion)
            filter = True
        if not filter:
            declaraciones=declaraciones.all()

        if page_size and page:
            paginator = Paginator(declaraciones, int(page_size))
            declaraciones = paginator.get_page(int(page))
        response = render_to_string(self.template_name, {
            'declaraciones': declaraciones
        })
        return HttpResponse(content = response,content_type="application/json")


