import traceback
import uuid
import sys
import datetime
from django.urls import resolve
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from pip._internal.download import is_file_url
from declaracion.forms import BienesPersonasForm
from declaracion.models import (Declaraciones, Secciones, SeccionDeclaracion, CatCamposObligatorios, Domicilios,
                                BienesInmuebles, BienesMuebles, MueblesNoRegistrables, Fideicomisos, BienesIntangibles,
                                CuentasPorCobrar, BienesPersonas, InfoPersonalVar, Apoyos, ConyugeDependientes,
                                Observaciones)
from django.apps import apps


def validar_declaracion(request, folio_declaracion):
    declaracion = Declaraciones.objects.filter(
        folio = uuid.UUID(folio_declaracion),
        info_personal_fija__usuario = request.user,
        cat_estatus__pk__in = (1, 2, 3)
        ).first()
    if declaracion:
        return declaracion
    else:
        raise ObjectDoesNotExist


def declaracion_datos(kwargs, modelo, declaracion):
    agregar = kwargs.get("agregar", False)
    editar_id = kwargs.get("pk", False)
    tipo = kwargs.get("tipo", False)
    cat_tipos_pasivos = kwargs.get("cat_tipos_pasivos", False)
    es_representacion_activa = kwargs.get("es_representacion_activa", False)
    beneficiario_infopersonalvar = kwargs.get("beneficiario_infopersonalvar", False)

    q = Q(declaraciones=declaracion)

    if beneficiario_infopersonalvar:
        q &= Q(beneficiario_infopersonalvar=beneficiario_infopersonalvar)
    if 'es_representacion_activa' in kwargs:
        q &= Q(es_representacion_activa=es_representacion_activa)
    if cat_tipos_pasivos:
        q &= Q(cat_tipos_pasivos_id=int(cat_tipos_pasivos))
    if tipo:
        q &= Q(cat_tipos_ingresos_varios_id=int(tipo)+1)

    if agregar:
        data = None
    elif editar_id:
        data = modelo.objects.filter(
            Q(pk=editar_id) & q
            ).first()
    else:
        data = modelo.objects.filter(q).last()

    data_todos = modelo.objects.filter(q)

    return agregar, editar_id, data, data_todos

def no_aplica(request):
    try:
        no_aplica = request.POST['no_aplica']
        no_aplica = True
    except KeyError:
        no_aplica = False

    return not no_aplica


def obtiene_rfc(rfc=""):
    try:
        anio = rfc[4:6]
        mes = rfc[6:8]
        dia = rfc[8:10]

        year = datetime.date.today().year

        if int("20" + anio) > year:
            anio = int("19" + anio)
        else:
            anio = int("20" + anio)
        return u"{}-{}-{}".format(anio, mes, dia)
    except Exception as e:
        print (e)
        return ''


def guardar_estatus(request, folio, estatus, parametro=None, aplica=True):
    current_url = resolve(request.path_info).url_name

    if parametro:
        seccion_id = Secciones.objects.filter(url=current_url,
                                              parametro=parametro).first()
    else:
        seccion_id = Secciones.objects.filter(url=current_url).first()
    declaraciones = Declaraciones.objects.filter(folio=folio).first()


    if seccion_id:
        obj, created = SeccionDeclaracion.objects.update_or_create(
            declaraciones=declaraciones,
            seccion=seccion_id,
            defaults={'aplica': aplica, 'estatus': estatus}
        )
        try:
            obtiene_avance(declaraciones)
        except Exception as e:
            print(e)
        return obj, created

def crea_secciones(declaracion):
    todas_secciones = Secciones.objects.filter(parent__isnull=True)
    for s in todas_secciones:
        if SeccionDeclaracion.objects.filter(declaraciones=declaracion,seccion=s).first() is None:

            max=CatCamposObligatorios.objects.filter(seccion__parent=s,es_obligatorio=True,esta_pantalla=True).count()
            print(max)
            observaciones = Observaciones()
            observaciones.save()
            sd = SeccionDeclaracion(estatus=SeccionDeclaracion.PENDIENTE,declaraciones=declaracion,num=0,max=max,seccion=s,aplica=True,observaciones=observaciones)
            sd.save()

def cuenta_campos(objeto,campos,modelos):
    num = 0
    faltas = []
    for cc in campos:

        try:
            if cc.tipo==0:
                cval = getattr(objeto, cc.nombre_columna)
                if callable(cval):
                    cval = cval()
            else:
                if isinstance(objeto,BienesPersonas) or isinstance(objeto,InfoPersonalVar):
                    if objeto.tipo()==cc.tipo:
                        cval = getattr(objeto, cc.nombre_columna)
                        if callable(cval):
                            cval = cval()
                    else:
                        cval=True
                else:
                    cval=True

        except Exception as e:
            print(e)
            traceback.print_exc()

            cval = None
        if cval is  None or str(cval) == "":
            num=num-1
            faltas.append({
                'objeto':objeto,
                'tipo':cc.tipo,
                'nombre':cc.nombre_columna,
                'seccion':cc.seccion
            })
    return (num,faltas)
    #return num


def obtiene_avance(declaracion):
    crea_secciones(declaracion)

    todas_secciones = Secciones.objects.filter(parent__isnull=False)
    mapa_objetos = []
    total = 0
    llenados = 0
    SeccionDeclaracion.objects.filter(seccion__parent__isnull=True).update(num=0)
    faltas = {}
    for s in todas_secciones:
        faltas[s.id]=[]
        try:
            campos_compuestos = list(
                CatCamposObligatorios.objects.filter(seccion=s, es_obligatorio=True, es_principal=False))
            campos_principal = list(
                CatCamposObligatorios.objects.filter(seccion=s, es_obligatorio=True, es_principal=True))
            matriz_campos_principales = {}
            models = {}

            matriz_campos_compuestos = {}
            models_s = {}
            aplica = True

            max_num=0
            try:
                seccion_declaracion  = SeccionDeclaracion.objects.filter(seccion=s,declaraciones=declaracion).first()
                aplica=seccion_declaracion.aplica
            except Exception as e:
                seccion_declaracion=None



            for campo_principal in campos_principal:
                if campo_principal.esta_pantalla:
                    max_num=max_num+1
                if not campo_principal.nombre_tabla in matriz_campos_principales:
                    matriz_campos_principales[campo_principal.nombre_tabla] = []
                matriz_campos_principales[campo_principal.nombre_tabla].append(campo_principal)
                if not campo_principal.nombre_tabla in models:
                    model = next((m for m in apps.get_models() if m._meta.db_table == campo_principal.nombre_tabla), None)
                    models[campo_principal.nombre_tabla] = model

            for campo_principal in campos_compuestos:
                if campo_principal.esta_pantalla:
                    max_num=max_num+1
                if not campo_principal.nombre_tabla in matriz_campos_compuestos:
                    matriz_campos_compuestos[campo_principal.nombre_tabla] = []
                matriz_campos_compuestos[campo_principal.nombre_tabla].append(campo_principal)
                if not campo_principal.nombre_tabla in models_s:
                    model = next((m for m in apps.get_models() if m._meta.db_table == campo_principal.nombre_tabla), None)
                    models_s[campo_principal.nombre_tabla] = model

            #print("%d %d" %(len(campos_principal) + len(campos_compuestos),max_num))
            total += max_num
            num=max_num
            if aplica and max_num > 0:
                if seccion_declaracion is None:
                    num=0
                else:
                    try:
                        for k, v in models.items():
                            if k=="declaracion_observaciones":
                                    try:
                                        obc  = seccion_declaracion.observaciones.observacion
                                        if obc is None or str(obc)=="":
                                            num= num - 1
                                            faltas[s.id].append({
                                                'objeto': seccion_declaracion.observaciones,
                                                'tipo':0,
                                                'nombre': 'observacion',
                                                'seccion':s
                                            })


                                    except Exception as e:
                                        print(e)
                                        num= num - 1
                            else:
                                if s.url =='representacion-activa':

                                    o = v.objects.filter(declaraciones=declaracion,es_representacion_activa=True).first()

                                elif s.url=='representacion-pasiva':

                                    o = v.objects.filter(declaraciones=declaracion,es_representacion_activa=False).first()

                                elif s.url=='ingresos-varios':
                                    pid = int(s.parametro)+1
                                    o = v.objects.filter(declaraciones=declaracion,
                                                             cat_tipos_ingresos_varios__id=pid ).first()
                                elif s.url=='deudas':
                                    o = v.objects.filter(declaraciones=declaracion,
                                                             cat_tipos_pasivos = 1 ).first()
                                elif s.url=='deudas-otros':
                                    o = v.objects.filter(declaraciones=declaracion,
                                                             cat_tipos_pasivos = 2).first()
                                else:
                                    o = v.objects.filter(declaraciones=declaracion).first()



                                for campo_principal in matriz_campos_principales[k]:
                                    try:

                                        if campo_principal.nombre_columna=='apoyos':
                                            if isinstance(o,ConyugeDependientes):

                                                if o.tiene_apoyos:
                                                    lst=o.dependiente()
                                                    for dependiente in lst:
                                                        apoyo = Apoyos.objects.filter(
                                                            beneficiario_infopersonalvar=dependiente
                                                        ).first()
                                                        cuenta = cuenta_campos(apoyo,matriz_campos_compuestos['declaracion_apoyos'],models_s)
                                                        num+=cuenta[0]
                                                        faltas[s.id].append(cuenta[1])

                                        else:
                                            bval = getattr(o, campo_principal.nombre_columna)

                                            if callable(bval):
                                                _list = bval()
                                                if _list is None or len(_list) == 0:
                                                    num=num-1
                                                else:
                                                    if s.id==42:
                                                        print(_list)
                                                    for bval in _list:
                                                        if isinstance(bval, BienesPersonas):
                                                            cuenta = cuenta_campos(bval,
                                                                                 matriz_campos_compuestos['declaracion_bienespersonas'],
                                                                                 models_s)
                                                            num += cuenta[0]
                                                            faltas[s.id].extend(cuenta[1])
                                                            bval=bval.otra_persona

                                                        for l, r in models_s.items():
                                                            if isinstance(bval,InfoPersonalVar) and l=='declaracion_domicilios' and ( isinstance(o,BienesMuebles) or isinstance(o,BienesInmuebles)  or isinstance(o,MueblesNoRegistrables) or isinstance(o,Fideicomisos) or isinstance(o,BienesIntangibles) or isinstance(o,CuentasPorCobrar) ):
                                                                for cc in matriz_campos_compuestos[l]:
                                                                    cval = getattr(bval.domicilios, cc.nombre_columna)

                                                                    #print("Valor = %s de %s en %s" % (
                                                                    #cval, cc.nombre_columna, cc.nombre_tabla))
                                                                    if cval is  None or str(cval) == "":
                                                                        num = num - 1
                                                                        faltas[s.id].append({
                                                                            'objeto': bval,
                                                                            'tipo': cc.tipo,
                                                                            'nombre': cc.nombre_columna,
                                                                            'seccion': s
                                                                        })

                                                            elif isinstance(bval, r):
                                                                for cc in matriz_campos_compuestos[l]:
                                                                    try:

                                                                        if cc.tipo==0:

                                                                            cval = getattr(bval, cc.nombre_columna)


                                                                            if  cc.nombre_columna=='razon_social' and isinstance(bval,InfoPersonalVar):
                                                                                cval = bval.nombre_completo()
                                                                        elif isinstance(bval,InfoPersonalVar) or isinstance(bval,BienesPersonas):

                                                                            if bval.tipo() == cc.tipo:
                                                                                cval = getattr(bval, cc.nombre_columna)
                                                                                if callable(cval):
                                                                                    cval = cval()
                                                                                else:
                                                                                    cval = True
                                                                            else:
                                                                                cval = True

                                                                    except Exception as e:
                                                                        print (e)
                                                                        traceback.print_exc()
                                                                        cval = None
                                                                    if cval is None or str(cval) == "":
                                                                            num = num - 1
                                                                            faltas[s.id].append({
                                                                                'objeto': bval,
                                                                                'tipo': cc.tipo,
                                                                                'nombre': cc.nombre_columna,
                                                                                'seccion':s
                                                                            })
                                            else:
                                                if bval is None or str(bval) == "":
                                                    num = num - 1
                                                    if campo_principal.esta_pantalla:
                                                        faltas[s.id].append({
                                                            'objeto': o,
                                                            'tipo': campo_principal.tipo,
                                                            'nombre': campo_principal.nombre_columna
                                                        })
                                    except Exception as e:
                                        print(e)
                                        traceback.print_exc()
                                        if campo_principal.esta_pantalla:
                                            faltas[s.id].append({
                                                'objeto': o,
                                                'tipo': campo_principal.tipo,
                                                'nombre': campo_principal.nombre_columna
                                            })
                    except Exception as e:
                        print(e)
                        traceback.print_exc()
                        if campo_principal.esta_pantalla:
                            faltas[s.id].append({
                                'objeto': o,
                                'tipo': campo_principal.tipo,
                                'nombre': campo_principal.nombre_columna,
                                'seccion':s
                            })

            if 0>num:
                num=0
            try:
                pc = int(float(num) / float(max_num) * 100)
            except:
                pc = 0

            if seccion_declaracion is not None:
                seccion_declaracion.num=num
                seccion_declaracion.max=max_num
                seccion_declaracion.save()
                try:
                    padre = SeccionDeclaracion.objects.filter(seccion=seccion_declaracion.seccion.parent,declaraciones=declaracion).first()
                    padre.num=padre.num+num
                    #padre.max=padre.max+max_num
                    padre.save()
                except Exception as e:
                    print(e)
                    padre = SeccionDeclaracion(seccion=seccion_declaracion.seccion.parent, num=num,
                                                             max=max_num, estatus=SeccionDeclaracion.PENDIENTE,
                                                             declaraciones=declaracion,aplica=True)
                    padre.save()
                #print(padre)


            mapa_objetos.append({
                'nombre': str(s),
                'llenado': num,
                'total': max_num,
                'porcentaje': pc,
                'seccion':s.id
            })
            llenados += num
            #print("Seccion %d %s %d %d"%(s.id,s.seccion,num,max_num))
        except Exception as e:
            print(e)
            traceback.print_exc()

    try:
        declaracion.avance = int(float(llenados) / float(total) * 100)

        declaracion.save()
    except:
        pass
    print(faltas[42])
    return (declaracion.avance,faltas)
