import datetime
import uuid
from django import template
from declaracion.models import (Declaraciones, CatTiposDeclaracion)

register = template.Library()

@register.simple_tag(takes_context=True)
def tipo_declaracion(context):
    try:
        tipo_declaracion = context['cat_tipos_declaracion']
    except Exception as e:
        tipo_declaracion = None

    try:
        folio = context['folio_declaracion']
    except Exception as e:
        folio = None

    if tipo_declaracion:
        tipo_declaracion = CatTiposDeclaracion.objects.filter(
            id=tipo_declaracion).first()
        return u"{}".format(tipo_declaracion.tipo_declaracion)

    if folio:
        folio = context['folio_declaracion']
        folio = uuid.UUID(folio)
        declaracion = Declaraciones.objects.filter(folio=folio).first()
        return u'{}'.format(declaracion.cat_tipos_declaracion.tipo_declaracion)
