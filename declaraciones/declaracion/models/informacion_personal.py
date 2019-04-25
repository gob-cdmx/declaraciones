import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE
from django.urls import reverse_lazy

from .catalogos import CatEstatusDeclaracion
from .catalogos import (CatPaises, CatEstadosCiviles,
                        CatTiposDeclaracion, CatRegimenesMatrimoniales,
                        CatGradosAcademicos, CatEstatusEstudios,
                        CatDocumentosObtenidos, CatEntesPublicos,
                        CatOrdenesGobierno,CatSectoresIndustria,
                        CatFuncionesPrincipales, CatAmbitosLaborales,
                        CatTiposRelacionesPersonales, CatPoderes,
                        CatTipoPersona, CatEntidadesFederativas, CatTipoVia)


class InfoPersonalFija(models.Model):
    nombres = models.CharField(max_length=255, blank=True)
    apellido1 = models.CharField(max_length=255, blank=True)
    apellido2 = models.CharField(max_length=255, blank=True)
    curp = models.CharField(max_length=255, blank=True)
    puesto = models.CharField(max_length=255, blank=True)
    rfc = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=14, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    cat_ente_publico = models.ForeignKey(CatEntesPublicos, on_delete=models.DO_NOTHING, blank=True, null=True)
    cat_entidades_federativas = models.ForeignKey(CatEntidadesFederativas, on_delete=models.DO_NOTHING, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    cat_pais = models.ForeignKey(CatPaises, on_delete=models.DO_NOTHING, null=True, blank=True)
    otro_ente = models.CharField(max_length=255, blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)


class Declaraciones(models.Model):
    folio = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    fecha_recepcion = models.DateTimeField(blank=True, null=True)
    fecha_declaracion = models.DateField(null=True, auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_tipos_declaracion = models.ForeignKey(CatTiposDeclaracion, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_estatus = models.ForeignKey(CatEstatusDeclaracion, on_delete=models.DO_NOTHING, default=1)
    avance = models.IntegerField(blank=True,default=0)
    info_personal_fija = models.ForeignKey(InfoPersonalFija, on_delete=models.DO_NOTHING)
    sello = models.TextField(blank=True)

class Domicilios(models.Model):
    municipio = models.CharField(max_length=255, blank=True)
    cp = models.CharField(max_length=255, blank=True)
    colonia = models.CharField(max_length=255, blank=True)
    nombre_via = models.CharField(max_length=255, blank=True)
    num_exterior = models.CharField(max_length=255, blank=True)
    num_interior = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_entidades_federativas = models.ForeignKey(CatEntidadesFederativas, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_pais = models.ForeignKey(CatPaises, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipo_via = models.ForeignKey(CatTipoVia, on_delete=models.DO_NOTHING, null=True, blank=True)


class Observaciones(models.Model):
    observacion = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.observacion


class InfoPersonalVar(models.Model):
    TIPO_DECLARANTE = 1
    TIPO_DEPENDIENTE = 2
    TIPO_EMPRESA = 3
    TIPO_SOCIO = 4
    TIPO_CLIENTE = 5
    TIPO_SOCIEDAD = 6
    TIPO_INSTITUCION = 7
    TIPO_FIDEICOMISARIO = 8
    TIPO_FIDEICOMITENTE = 9
    TIPO_FIDUCIARIO = 10
    TIPO_COPROPIETARIO = 11
    TIPO_PROPIETARIO_ANTERIOR = 12
    TIPO_PRESTATARIO = 13
    es_fisica = models.BooleanField(blank=True, null=True, default=None)
    razon_social = models.CharField(max_length=255, blank=True, null=True)
    nombres = models.CharField(max_length=255, blank=True)
    apellido1 = models.CharField(max_length=255, blank=True)
    apellido2 = models.CharField(max_length=255, blank=True)
    curp = models.CharField(max_length=255, blank=True)
    rfc = models.CharField(max_length=255, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    num_id_identificacion = models.CharField(max_length=255, blank=True)
    email_personal = models.CharField(max_length=255, blank=True)
    tel_particular = models.CharField(max_length=255, blank=True)
    tel_movil = models.CharField(max_length=255, blank=True)
    cat_entidades_federativas = models.ForeignKey(CatEntidadesFederativas, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_estados_civiles = models.ForeignKey(CatEstadosCiviles, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_pais = models.ForeignKey(CatPaises, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_regimenes_matrimoniales = models.ForeignKey(CatRegimenesMatrimoniales, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    domicilios = models.ForeignKey(Domicilios, on_delete=models.DO_NOTHING, blank=True, null=True)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING, blank=True, null=True)
    cat_tipo_persona = models.ForeignKey(CatTipoPersona, on_delete=models.DO_NOTHING, blank=True, null=True)
    cat_sectores_industria = models.ForeignKey(CatSectoresIndustria, on_delete=models.DO_NOTHING, blank=True, null=True)
    otro_sector = models.CharField(max_length=255, blank=True, null=True)
    otro_estado_civil = models.CharField(max_length=255, blank=True, null=True)
    actividad_economica = models.CharField(max_length=255, blank=True, null=True)
    ocupacion_girocomercial = models.CharField(max_length=255, blank=True, null=True)
    nombre_negocio = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nacionalidades = models.ManyToManyField(CatPaises, through='Nacionalidades', related_name="info_personal_var_nacionalidaes", blank=True)
    activos_bienes = models.ManyToManyField(
        'ActivosBienes',
        through='BienesPersonas',
        through_fields=('info_personal_var', 'activos_bienes'),
        related_name="info_personal_var_activos_bienes")


    class Meta:
        ordering=('pk',)


    def nombre_completo(self):
        if self.es_fisica:
            return ("%s %s %s")%(self.nombres ,self.apellido1,self.apellido2)
        else:
            return self.razon_social

    def domicilio(self):
        return [self.domicilios]

    def observacion(self):
        return [self.observaciones]

    def nacionalidad(self):
        try:
            return self.nacionalidades.all()
        except:
            return None

    def tipo(self):
        return self.cat_tipo_persona_id

    def sectores_industrias(self):
        try:
            if self.cat_sectores_industria.default:
                return u"{} {}".format(self.cat_sectores_industria,
                                       self.otro_sector)
            else:
                return u"{}".format(self.cat_sectores_industria)
        except Exception as e:
            return u""


class Nacionalidades(models.Model):
    cat_paises = models.ForeignKey(CatPaises, models.DO_NOTHING, null=True, blank=True, related_name="nacionalidades_cat_paises")
    info_personal_var = models.ForeignKey(InfoPersonalVar, models.DO_NOTHING, related_name="nacionalidades_info_personal_var")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DatosCurriculares(models.Model):
    institucion_educativa = models.CharField(max_length=255, blank=True)
    municipio = models.CharField(max_length=255, blank=True)
    carrera_o_area = models.CharField(max_length=255, blank=True)
    conclusion = models.CharField(max_length=255, blank=True)
    cedula_profesional = models.CharField(max_length=255, blank=True)
    diploma = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_documentos_obtenidos = models.ForeignKey(CatDocumentosObtenidos, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_entidades_federativas = models.ForeignKey(CatEntidadesFederativas, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_estatus_estudios = models.ForeignKey(CatEstatusEstudios, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_grados_academicos = models.ForeignKey(CatGradosAcademicos, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_pais = models.ForeignKey(CatPaises, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)


    def columna_uno(self):
        if self.cat_grados_academicos:
            return u"{}".format(self.cat_grados_academicos)
        else:
            return u""

    def columna_dos(self):
        if self.institucion_educativa:
            return u"{}".format(self.institucion_educativa)
        else:
            return u""

    def columna_tres(self):
        if self.carrera_o_area:
            return u"{}".format(self.carrera_o_area)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:datos-curriculares-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:datos-curriculares-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:datos-curriculares',
                            kwargs={'folio': self.declaraciones.folio})

    def observacion(self):
        return [self.observaciones]


class Encargos(models.Model):
    empleo_cargo_comision = models.CharField(max_length=255, blank=True)
    honorarios = models.BooleanField(blank=True, null=True, default=None)
    nivel_encargo = models.CharField(max_length=255, blank=True)
    area_adscripcion = models.CharField(max_length=255, blank=True)
    posesion_conclusion = models.DateField(blank=True, null=True)
    telefono_laboral = models.CharField(max_length=255, blank=True)
    email_laboral = models.CharField(max_length=255, blank=True)
    otro_sector = models.CharField(max_length=255, blank=True)
    otra_funcion = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_entes_publicos = models.ForeignKey(CatEntesPublicos, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_funciones_principales = models.ForeignKey(CatFuncionesPrincipales, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_ordenes_gobierno = models.ForeignKey(CatOrdenesGobierno, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_paises = models.ForeignKey(CatPaises, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_sectores_industria = models.ForeignKey(CatSectoresIndustria, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    domicilios = models.ForeignKey(Domicilios, on_delete=models.DO_NOTHING)
    posesion_inicio = models.DateField(blank=True, null=True)
    telefono_extension = models.CharField(max_length=255, blank=True)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    otro_naturalezas_juridicas = models.CharField(max_length=255, blank=True)
    cat_poderes = models.ForeignKey(CatPoderes, on_delete=models.DO_NOTHING, blank=True, null=True)
    otro_ente = models.CharField(max_length=255, blank=True, null=True)

    def observacion(self):
        return [self.observaciones]

    def poderes(self):
        try:
            if self.cat_poderes.default:
                return u"{} {}".format(self.cat_poderes, self.otro_naturalezas_juridicas)
            else:
                return u"{}".format(self.cat_poderes)
        except Exception as e:
            return u""


class ExperienciaLaboral(models.Model):
    otro_poder = models.CharField(max_length=255, blank=True)
    nombre_institucion = models.CharField(max_length=255, blank=True)
    unidad_area_administrativa = models.CharField(max_length=255, blank=True)
    otro_sector = models.CharField(max_length=255, blank=True)
    jerarquia_rango = models.CharField(max_length=255, blank=True)
    cargo_puesto = models.CharField(max_length=255, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)
    fecha_salida = models.DateField(null=True, blank=True)
    otra_funcion = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_ambitos_laborales = models.ForeignKey(CatAmbitosLaborales, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_funciones_principales = models.ForeignKey(CatFuncionesPrincipales, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_ordenes_gobierno = models.ForeignKey(CatOrdenesGobierno, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_poderes = models.ForeignKey(CatPoderes, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_sectores_industria = models.ForeignKey(CatSectoresIndustria, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    domicilios = models.ForeignKey(Domicilios, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    otro_ambitos_laborales = models.CharField(max_length=255, blank=True)

    def columna_uno(self):
        if self.nombre_institucion:
            return u"{}".format(self.nombre_institucion)
        else:
            return u""

    def columna_dos(self):
        if self.jerarquia_rango:
            return u"{}".format(self.jerarquia_rango)
        else:
            return u""

    def columna_tres(self):
        if self.cargo_puesto:
            return u"{}".format(self.cargo_puesto)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:experiencia-laboral-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:experiencia-laboral-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:experiencia-laboral',
                            kwargs={'folio': self.declaraciones.folio})

    def observacion(self):
        return [self.observaciones]

    def funciones_principales(self):
        try:
            if self.cat_funciones_principales.default:
                return u"{} {}".format(self.cat_funciones_principales,
                                       self.otra_funcion)
            else:
                return u"{}".format(self.cat_funciones_principales)
        except Exception as e:
            return u""

class ConyugeDependientes(models.Model):
    habita_domicilio = models.BooleanField(blank=True, null=True, default=None)
    medio_contacto = models.CharField(max_length=255, blank=True)
    ingresos_propios = models.BooleanField(blank=True, null=True, default=None)
    ocupacion_profesion = models.CharField(max_length=255, blank=True)
    otro_sector = models.CharField(max_length=255, blank=True)
    tiene_apoyos = models.BooleanField(blank=True, null=True, default=None)
    proveedor_contratista = models.BooleanField(blank=True, null=True, default=None)
    intereses_comunes = models.BooleanField(blank=True, null=True, default=None)
    cabildeo_sector = models.BooleanField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_tipos_relaciones_personales = models.ForeignKey(CatTiposRelacionesPersonales, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    otra_relacion = models.CharField(max_length=255, blank=True)
    otra_relacion_familiar = models.CharField(max_length=255, blank=True)
    declarante_infopersonalvar = models.ForeignKey(InfoPersonalVar, on_delete=models.DO_NOTHING, related_name="declarante_conyugue_dependientes")
    dependiente_infopersonalvar = models.ForeignKey(InfoPersonalVar, on_delete=models.DO_NOTHING, related_name="dependiente_conyugue_dependientes")

    def columna_uno(self):
        return u"{} {} {}".format(
            self.dependiente_infopersonalvar.nombres,
            self.dependiente_infopersonalvar.apellido1,
            self.dependiente_infopersonalvar.apellido2,
            )

    def columna_dos(self):
        if self.cat_tipos_relaciones_personales:
            return u"{}".format(self.cat_tipos_relaciones_personales)
        else:
            return u""

    def columna_tres(self):
        if self.dependiente_infopersonalvar.fecha_nacimiento:
            return u"{}".format(self.dependiente_infopersonalvar.fecha_nacimiento)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:dependientes-economicos-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:dependientes-economicos-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:dependientes-economicos',
                            kwargs={'folio': self.declaraciones.folio})
    def observacion(self):

        return [self.observaciones]

    def dependiente(self):
        return [self.dependiente_infopersonalvar]

    def nacionalidad(self):
        return self.dependiente_infopersonalvar.nacionalidad()

    def domicilio(self):
        return [self.declarante_infopersonalvar.domicilios]

    def tipo_relacion_personal(self):
        try:
            if self.cat_tipos_relaciones_personales.default:
                return u"{} {}".format(self.cat_tipos_relaciones_personales,
                                  self.otra_relacion)
            else:
                return u"{}".format(self.cat_tipos_relaciones_personales)
        except Exception as e:
            return u""
