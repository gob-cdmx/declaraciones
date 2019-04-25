import uuid
from django import template
from django.urls import reverse, resolve
from declaracion.models import (Secciones)

register = template.Library()

@register.simple_tag(takes_context=True)
def anterior_siguiente(context):
    request = context['request']
    current_url = resolve(request.path_info).url_name
    current_url = current_url.replace('-borrar','')
    current_url = current_url.replace('-editar','')
    current_url = current_url.replace('-agregar','')
    parametro = resolve(request.path_info).kwargs

    try:
        tipo = parametro['tipo']
    except Exception as e:
        tipo = None

    if tipo:
        seccion = Secciones.objects.filter(url=current_url,
                                           parametro=tipo).first()
    else:
        seccion = Secciones.objects.filter(url=current_url).first()

    try:
        folio = uuid.UUID(context['folio_declaracion'])
    except Exception as e:
        return {
            'anterior': '',
            'siguiente': ''
        }

    if seccion:
        try:
            anterior = seccion.get_previous_sibling().url
            tipo = seccion.get_previous_sibling().parametro
        except Exception as e:
            try:
                anterior = seccion.get_root().get_previous_sibling().get_descendants().last().url
                tipo = seccion.get_root().get_previous_sibling().get_descendants().last().parametro
            except Exception as e:
                anterior = None

        if tipo:
            kwargs = {'folio': folio, 'tipo': tipo}
        else:
            kwargs={'folio': folio}

        if anterior:
            anterior = reverse('declaracion:' + anterior, kwargs=kwargs)
        else:
            anterior = ''


        try:
            siguiente = seccion.get_next_sibling().url
            tipo = seccion.get_next_sibling().parametro
        except Exception as e:
            try:
                siguiente = seccion.get_root().get_next_sibling().get_descendants().first().url
                tipo = seccion.get_root().get_next_sibling().get_descendants().first().parametro
            except Exception as e:
                siguiente = None

        if tipo:
            kwargs = {'folio': folio, 'tipo': tipo}
        else:
            kwargs={'folio': folio}

        if siguiente:
            siguiente = reverse('declaracion:' + siguiente, kwargs=kwargs)
        else:
            siguiente = ''

        return {
            'anterior': anterior,
            'siguiente': siguiente
        }
