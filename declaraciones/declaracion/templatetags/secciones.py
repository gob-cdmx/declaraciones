import datetime
from django import template
from declaracion.models import (Secciones)

register = template.Library()

@register.simple_tag
def current_time():
    secciones = Secciones.objects.filter(level=0)
    return secciones

@register.simple_tag
def get_status(seccion, folio):
    seccion = Secciones.objects.get(id=seccion.id)
    status = seccion.get_status(folio)
    return status

@register.simple_tag
def show_menu(path, seccion):        
    if "declaracion/informacion-personal" in path and "Información persona" in seccion:        
        return 'show'
    elif "declaracion/intereses" in path and "Intereses" in seccion:        
        return 'show'
    elif "/declaracion/ingresos" in path and "Ingreso" in seccion:        
        return 'show'
    elif "/declaracion/activos" in path and "Activos" in seccion:        
        return 'show'
    elif "/declaracion/pasivos" in path and "Pasivos" in seccion:        
        return 'show'   
    else:
        return 'not-show'
    
