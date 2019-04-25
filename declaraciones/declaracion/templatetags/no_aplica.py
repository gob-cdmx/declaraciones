import uuid
from django import template
from django.urls import resolve
from declaracion.models import (Secciones, SeccionDeclaracion)

register = template.Library()

@register.simple_tag(takes_context=True)
def no_aplica(context, folio=None, current_url=None, tipo=None):
    if current_url == None and tipo == None:
        request = context['request']
        current_url = resolve(request.path_info).url_name
        parametro = resolve(request.path_info).kwargs

        try:
            tipo = parametro['tipo']
        except Exception as e:
            tipo = None

        try:
            folio = uuid.UUID(context['folio_declaracion'])
        except Exception as e:
            folio = None

    if tipo:
        seccion_id = Secciones.objects.filter(url=current_url,
                                              parametro=tipo).first()
    else:
        seccion_id = Secciones.objects.filter(url=current_url).first()

    if seccion_id:
        seccion = SeccionDeclaracion.objects.filter(
            declaraciones__folio=folio,
            seccion=seccion_id,
        ).first()

        if seccion:
            return not seccion.aplica
        else:
            return False
