from django.db import models
from django.urls import reverse_lazy
from .informacion_personal import(Declaraciones, Domicilios, Observaciones,
                                  InfoPersonalVar)
from .catalogos import (CatTiposInmuebles, CatTiposTitulares,
                        CatFormasAdquisiciones, CatSectoresIndustria,
                        CatMonedas, CatTiposOperaciones, CatTiposMuebles,
                        CatPaises, CatEntidadesFederativas,
                        CatTiposEspecificosInversiones, CatTiposInversiones,
                        CatTiposMetales, CatTiposFideicomisos,
                        CatTiposRelacionesPersonales, CatUnidadesTemporales, CatActivoBien,
                        CatTipoParticipacion, CatEntesPublicos)


class ActivosBienes(models.Model):
    BIENES_INMUEBLES = 1
    BIENES_INTANGIBLES = 2
    BIENES_MUEBLES = 3
    MUEBLES_NO_REGISTRABLES = 4
    FIDEICOMISOS = 5
    CUENTAS_POR_COBRAR = 6
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    id_activobien = models.IntegerField(null=True)
    cat_activo_bien = models.ForeignKey(CatActivoBien, on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BienesPersonas(models.Model):
    COVENDEDOR = 1
    COPROPIETARIO = 2
    FIDEICOMITENTE = 3
    FIDEICOMISARIO = 4
    FIDUCIARIO = 5
    PRESTATARIO_O_DEUDOR = 6
    DECLARANTE = 7
    COPROPIETARIO = 8
    PROPIETARIO_ANTERIOR = 9
    info_personal_var = models.ForeignKey(InfoPersonalVar, on_delete=models.DO_NOTHING, related_name="bienes_personas_info_personal_var")
    activos_bienes = models.ForeignKey(ActivosBienes, on_delete=models.DO_NOTHING)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    es_propietario = models.BooleanField(blank=True, null=True, default=None)
    precio_adquision = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    el_adquirio = models.BooleanField(blank=True, null=True, default=None)
    cat_tipo_participacion = models.ForeignKey(CatTipoParticipacion, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tipo_relacion = models.ForeignKey(CatTiposRelacionesPersonales, on_delete=models.DO_NOTHING, blank=True, null=True)
    otra_relacion = models.CharField(max_length=255, blank=True, null=True)
    otra_relacion_familiar = models.CharField(max_length=255, blank=True)
    otra_persona = models.ForeignKey(InfoPersonalVar, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="bienes_personas_otra_persona")

    def tipo(self):
        return self.cat_tipo_participacion_id

    def relacion(self):
        try:
            if self.tipo_relacion.default:
                return u"{} {}".format(self.tipo_relacion,
                                       self.otra_relacion)
            else:
                return u"{}".format(self.tipo_relacion)
        except Exception as e:
            return u""


class BienesInmuebles(models.Model):
    superficie_terreno = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    superficie_construccion = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    otro_titular = models.CharField(max_length=255, blank=True)
    num_escritura_publica = models.CharField(max_length=255, blank=True)
    num_registro_publico = models.CharField(max_length=255, blank=True)
    folio_real = models.CharField(max_length=255, blank=True)
    fecha_contrato_compra = models.DateField(null=True, blank=True)
    otra_forma = models.CharField(max_length=255, blank=True)
    fecha_adquisicion = models.DateField(null=True, blank=True)
    precio_adquisicion = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    valor_catastral = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_formas_adquisiciones = models.ForeignKey(CatFormasAdquisiciones, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_monedas = models.ForeignKey(CatMonedas, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_inmuebles = models.ForeignKey(CatTiposInmuebles, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_operaciones = models.ForeignKey(CatTiposOperaciones, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_titulares = models.ForeignKey(CatTiposTitulares, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    domicilios = models.ForeignKey(Domicilios, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    activos_bienes = models.ForeignKey(ActivosBienes, on_delete=models.DO_NOTHING)
    otra_operacion = models.CharField(max_length=255, blank=True, null=True)
    otro_inmueble = models.CharField(max_length=255, blank=True, null=True)

    def persona(self):
        try:
            return BienesPersonas.objects.filter(activos_bienes = self.activos_bienes,cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO).first()
        except Exception as e:
            return None
    def copropietario(self):
        try:
            return BienesPersonas.objects.filter(activos_bienes = self.activos_bienes,cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO)
        except Exception as e:
            return None
    def declarante(self):
        try:
            return [BienesPersonas.objects.filter(activos_bienes = self.activos_bienes,cat_tipo_participacion_id=BienesPersonas.DECLARANTE).first().info_personal_var]
        except Exception as e:
            return None

    def propierario_anterior(self):
        try:
            return BienesPersonas.objects.filter(activos_bienes = self.activos_bienes,cat_tipo_participacion_id=BienesPersonas.PROPIETARIO_ANTERIOR)
        except Exception as e:
            return None

    def observacion(self):
        return [self.observaciones]

    def columna_uno(self):
        if self.cat_tipos_operaciones:
            return u"{}".format(self.cat_tipos_operaciones)
        else:
            return u""

    def columna_dos(self):
        if self.cat_formas_adquisiciones:
            return u"{}".format(self.cat_formas_adquisiciones)
        else:
            return u""

    def columna_tres(self):
        if self.cat_tipos_titulares:
            return u"{}".format(self.cat_tipos_titulares)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:bienes-inmuebles-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:bienes-inmuebles-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:bienes-inmuebles',
                            kwargs={'folio': self.declaraciones.folio})

    def tipo_operacion(self):
        try:
            if self.cat_tipos_operaciones.default:
                return u"{} {}".format(self.cat_tipos_operaciones,
                                       self.otra_operacion)
            else:
                return u"{}".format(self.cat_tipos_operaciones)
        except Exception as e:
            return u""

    def tipo_inmueble(self):
        try:
            if self.cat_tipos_inmuebles.default:
                return u"{} {}".format(self.cat_tipos_inmuebles,
                                       self.otro_inmueble)
            else:
                return u"{}".format(self.cat_tipos_inmuebles)
        except Exception as e:
            return u""

    def titular(self):
        try:
            if self.cat_tipos_titulares.default:
                return u"{} {}".format(self.cat_tipos_titulares,
                                       self.otro_titular)
            else:
                return u"{}".format(self.cat_tipos_titulares)
        except Exception as e:
            return u""

    def forma_adquisicion(self):
        try:
            if self.cat_formas_adquisiciones.default:
                return u"{} {}".format(self.cat_formas_adquisiciones,
                                       self.otra_forma)
            else:
                return u"{}".format(self.cat_formas_adquisiciones)
        except Exception as e:
            return u""


class BienesMuebles(models.Model):
    otra_operacion = models.CharField(max_length=255, blank=True)
    otro_tipo_mueble = models.CharField(max_length=255, blank=True)
    marca = models.CharField(max_length=255, blank=True)
    submarca = models.CharField(max_length=255, blank=True)
    modelo = models.IntegerField(blank=True, null=True)
    num_serie = models.CharField(max_length=255, blank=True)
    otro_titular = models.CharField(max_length=255, blank=True)
    num_registro_vehicular = models.CharField(max_length=255, blank=True)
    otra_forma = models.CharField(max_length=255, blank=True)
    otro_sector = models.CharField(max_length=255, blank=True)
    fecha_adquisicion = models.DateField(null=True, blank=True)
    precio_adquisicion = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_entidades_federativas = models.ForeignKey(CatEntidadesFederativas, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_formas_adquisiciones = models.ForeignKey(CatFormasAdquisiciones, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_monedas = models.ForeignKey(CatMonedas, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_paises = models.ForeignKey(CatPaises, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_muebles = models.ForeignKey(CatTiposMuebles, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_operaciones = models.ForeignKey(CatTiposOperaciones, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_titulares = models.ForeignKey(CatTiposTitulares, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    activos_bienes = models.ForeignKey(ActivosBienes, on_delete=models.DO_NOTHING)
    def declarante(self):
        try:
            return [BienesPersonas.objects.filter(activos_bienes = self.activos_bienes,cat_tipo_participacion_id=BienesPersonas.DECLARANTE).first().info_personal_var]
        except Exception as e:
            return None

    def copropietario(self):
        try:
            return BienesPersonas.objects.filter(activos_bienes = self.activos_bienes,cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO)
        except Exception as e:
            print(e)
            return None

    def propierario_anterior(self):
        try:
            return BienesPersonas.objects.filter(activos_bienes = self.activos_bienes,cat_tipo_participacion_id=BienesPersonas.PROPIETARIO_ANTERIOR)
        except Exception as e:
            return None

    def observacion(self):
        return [self.observaciones]

    def columna_uno(self):
        if self.cat_tipos_operaciones:
            return u"{}".format(self.cat_tipos_operaciones)
        else:
            return u""

    def columna_dos(self):
        if self.cat_formas_adquisiciones:
            return u"{}".format(self.cat_formas_adquisiciones)
        else:
            return u""

    def columna_tres(self):
        if self.cat_tipos_titulares:
            return u"{}".format(self.cat_tipos_titulares)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:bienes-muebles-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:bienes-muebles-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:bienes-muebles',
                            kwargs={'folio': self.declaraciones.folio})

    def tipo_operacion(self):
        try:
            if self.cat_tipos_operaciones.default:
                return u"{} {}".format(self.cat_tipos_operaciones,
                                       self.otra_operacion)
            else:
                return u"{}".format(self.cat_tipos_operaciones)
        except Exception as e:
            return u""

    def tipo_mueble(self):
        try:
            if self.cat_tipos_muebles.default:
                return u"{} {}".format(self.cat_tipos_muebles,
                                       self.otro_tipo_mueble)
            else:
                return u"{}".format(self.cat_tipos_muebles)
        except Exception as e:
            return u""

    def titular(self):
        try:
            if self.cat_tipos_titulares.default:
                return u"{} {}".format(self.cat_tipos_titulares,
                                       self.otro_titular)
            else:
                return u"{}".format(self.cat_tipos_titulares)
        except Exception as e:
            return u""

    def forma_adquisicion(self):
        try:
            if self.cat_formas_adquisiciones.default:
                return u"{} {}".format(self.cat_formas_adquisiciones,
                                       self.otra_forma)
            else:
                return u"{}".format(self.cat_formas_adquisiciones)
        except Exception as e:
            return u""


class MueblesNoRegistrables(models.Model):
    otra_operacion = models.CharField(max_length=255, blank=True)
    otro_bien_mueble = models.CharField(max_length=255, blank=True)
    descripcion_bien = models.CharField(max_length=255, blank=True)
    otro_titular = models.CharField(max_length=255, blank=True)
    otra_forma = models.CharField(max_length=255, blank=True)
    fecha_adquisicion = models.DateField(null=True, blank=True)
    precio_adquisicion = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_formas_adquisiciones = models.ForeignKey(CatFormasAdquisiciones, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_monedas = models.ForeignKey(CatMonedas, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_muebles = models.ForeignKey(CatTiposMuebles, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_operaciones = models.ForeignKey(CatTiposOperaciones, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_titulares = models.ForeignKey(CatTiposTitulares, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    activos_bienes = models.ForeignKey(ActivosBienes, on_delete=models.DO_NOTHING)
    def declarante(self):
        try:
            return [BienesPersonas.objects.filter(activos_bienes = self.activos_bienes,cat_tipo_participacion_id=BienesPersonas.DECLARANTE).first().info_personal_var]
        except Exception as e:
            return None

    def copropietario(self):
        try:
            return BienesPersonas.objects.filter(activos_bienes = self.activos_bienes,cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO)
        except Exception as e:
            return None

    def propierario_anterior(self):
        try:
            return BienesPersonas.objects.filter(activos_bienes = self.activos_bienes,cat_tipo_participacion_id=BienesPersonas.PROPIETARIO_ANTERIOR)
        except Exception as e:
            return None

    def observacion(self):
        return [self.observaciones]

    def columna_uno(self):
        if self.cat_tipos_operaciones:
            return u"{}".format(self.cat_tipos_operaciones)
        else:
            return u""

    def columna_dos(self):
        if self.cat_formas_adquisiciones:
            return u"{}".format(self.cat_formas_adquisiciones)
        else:
            return u""

    def columna_tres(self):
        if self.cat_tipos_titulares:
            return u"{}".format(self.cat_tipos_titulares)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:muebles-noregistrables-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:muebles-noregistrables-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:muebles-noregistrables',
                            kwargs={'folio': self.declaraciones.folio})

    def tipo_operacion(self):
        try:
            if self.cat_tipos_operaciones.default:
                return u"{} {}".format(self.cat_tipos_operaciones,
                                       self.otra_operacion)
            else:
                return u"{}".format(self.cat_tipos_operaciones)
        except Exception as e:
            return u""

    def tipo_mueble(self):
        try:
            if self.cat_tipos_muebles.default:
                return u"{} {}".format(self.cat_tipos_muebles,
                                       self.otro_bien_mueble)
            else:
                return u"{}".format(self.cat_tipos_muebles)
        except Exception as e:
            return u""

    def titular(self):
        try:
            if self.cat_tipos_titulares.default:
                return u"{} {}".format(self.cat_tipos_titulares,
                                       self.otro_titular)
            else:
                return u"{}".format(self.cat_tipos_titulares)
        except Exception as e:
            return u""

    def forma_adquisicion(self):
        try:
            if self.cat_formas_adquisiciones.default:
                return u"{} {}".format(self.cat_formas_adquisiciones,
                                       self.otra_forma)
            else:
                return u"{}".format(self.cat_formas_adquisiciones)
        except Exception as e:
            return u""


class Inversiones(models.Model):
    otra_operacion = models.CharField(max_length=255, blank=True)
    otra_inversion = models.CharField(max_length=255, blank=True)
    otro_tipo_especifico = models.CharField(max_length=255, blank=True)
    num_cuenta = models.CharField(max_length=255, blank=True)
    otra_forma = models.CharField(max_length=255, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    monto_original = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    saldo_actual = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    plazo = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    cat_tipos_titulares = models.ForeignKey(CatTiposTitulares, on_delete=models.DO_NOTHING, null=True, blank=True)
    otro_tipo_titular = models.CharField(max_length=255, blank=True)
    porcentaje_inversion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_formas_adquisiciones = models.ForeignKey(CatFormasAdquisiciones, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_monedas = models.ForeignKey(CatMonedas, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_paises = models.ForeignKey(CatPaises, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_especificos_inversiones = models.ForeignKey(CatTiposEspecificosInversiones, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_inversiones = models.ForeignKey(CatTiposInversiones, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_operaciones = models.ForeignKey(CatTiposOperaciones, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    info_personal_var = models.ForeignKey(InfoPersonalVar, on_delete=models.DO_NOTHING)
    cat_unidades_temporales = models.ForeignKey(CatUnidadesTemporales, on_delete=models.DO_NOTHING, null=True, blank=True)

    def observacion(self):
        return [self.observaciones]

    def columna_uno(self):
        if self.cat_tipos_operaciones:
            return u"{}".format(self.cat_tipos_operaciones)
        else:
            return u""

    def columna_dos(self):
        if self.cat_formas_adquisiciones:
            return u"{}".format(self.cat_formas_adquisiciones)
        else: return u""

    def columna_tres(self):
        if self.cat_tipos_titulares:
            return u"{}".format(self.cat_tipos_titulares)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:inversiones-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:inversiones-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:inversiones',
                            kwargs={'folio': self.declaraciones.folio})

    def persona(self):
        return [self.info_personal_var]

    def tipo_operacion(self):
        try:
            if self.cat_tipos_operaciones.default:
                return u"{} {}".format(self.cat_tipos_operaciones,
                                       self.otra_operacion)
            else:
                return u"{}".format(self.cat_tipos_operaciones)
        except Exception as e:
            return u""

    def titular(self):
        try:
            if self.cat_tipos_titulares.default:
                return u"{} {}".format(self.cat_tipos_titulares,
                                       self.otro_tipo_titular)
            else:
                return u"{}".format(self.cat_tipos_titulares)
        except Exception as e:
            return u""

    def forma_adquisicion(self):
        try:
            if self.cat_formas_adquisiciones.default:
                return u"{} {}".format(self.cat_formas_adquisiciones,
                                       self.otra_forma)
            else:
                return u"{}".format(self.cat_formas_adquisiciones)
        except Exception as e:
            return u""

    def tipo_inversion(self):
        try:
            if self.cat_tipos_inversiones.default:
                return u"{} {}".format(self.cat_tipos_inversiones,
                                       self.otra_inversion)
            else:
                return u"{}".format(self.cat_tipos_inversiones)
        except Exception as e:
            return u""

    def tipo_especifico(self):
        try:
            if self.cat_tipos_especificos_inversiones.default:
                return u"{} {}".format(self.cat_tipos_especificos_inversiones,
                                       self.otro_tipo_especifico)
            else:
                return u"{}".format(self.cat_tipos_especificos_inversiones)
        except Exception as e:
            return u""


class EfectivoMetales(models.Model):
    otro_tipo_operacion = models.CharField(max_length=255, blank=True)
    monto_efectivo = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    otro_metal = models.CharField(max_length=255, blank=True)
    unidades = models.CharField(max_length=255, blank=True)
    monto_metales = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    otra_forma = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_formas_adquisiciones = models.ForeignKey(CatFormasAdquisiciones, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_monedas = models.ForeignKey(CatMonedas, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_metales = models.ForeignKey(CatTiposMetales, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_operaciones = models.ForeignKey(CatTiposOperaciones, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)

    def observacion(self):
        return [self.observaciones]

    def columna_uno(self):
        if self.cat_tipos_operaciones:
            return u"{}".format(self.cat_tipos_operaciones)
        else:
            return u""

    def columna_dos(self):
        if self.cat_formas_adquisiciones:
            return u"{}".format(self.cat_formas_adquisiciones)
        else:
            return u""

    def columna_tres(self):
        if self.cat_tipos_metales:
            return u"{}".format(self.cat_tipos_metales)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:efectivo-metales-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:efectivo-metales-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:efectivo-metales',
                            kwargs={'folio': self.declaraciones.folio})

    def tipo_operacion(self):
        try:
            if self.cat_tipos_operaciones.default:
                return u"{} {}".format(self.cat_tipos_operaciones,
                                       self.otro_tipo_operacion)
            else:
                return u"{}".format(self.cat_tipos_operaciones)
        except Exception as e:
            return u""

    def tipo_metal(self):
        try:
            if self.cat_tipos_metales.default:
                return u"{} {}".format(self.cat_tipos_metales,
                                       self.otro_metal)
            else:
                return u"{}".format(self.cat_tipos_metales)
        except Exception as e:
            return u""

    def forma_adquisicion(self):
        try:
            if self.cat_formas_adquisiciones.default:
                return u"{} {}".format(self.cat_formas_adquisiciones,
                                       self.otra_forma)
            else:
                return u"{}".format(self.cat_formas_adquisiciones)
        except Exception as e:
            return u""


class Fideicomisos(models.Model):
    nombre_fideicomiso = models.CharField(max_length=255, blank=True)
    otra_operacion = models.CharField(max_length=255, blank=True)
    otro_fideicomiso = models.CharField(max_length=255, blank=True)
    objetivo_fideicomiso = models.CharField(max_length=255, blank=True)
    num_registro = models.CharField(max_length=255, blank=True)
    fecha_creacion = models.DateField(null=True, blank=True)
    plazo_vigencia = models.CharField(max_length=255, blank=True)
    valor_fideicomiso = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    ingreso_monetario = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    institucion_fiduciaria = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_monedas = models.ForeignKey(CatMonedas, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_paises = models.ForeignKey(CatPaises, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_fideicomisos = models.ForeignKey(CatTiposFideicomisos, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_operaciones = models.ForeignKey(CatTiposOperaciones, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    activos_bienes = models.ForeignKey(ActivosBienes, on_delete=models.DO_NOTHING)

    def fideicomitente(self):
        try:
            return [o.otra_persona for o in  BienesPersonas.objects.filter(activos_bienes = self.activos_bienes,cat_tipo_participacion_id=BienesPersonas.FIDEICOMITENTE)]
        except Exception as e:
            return None

    def fideicomisario(self):
        try:
            return [o.otra_persona for o in BienesPersonas.objects.filter(activos_bienes = self.activos_bienes,cat_tipo_participacion_id=BienesPersonas.FIDEICOMISARIO)]
        except Exception as e:
            return None

    def fiduciario(self):
        try:
            return [o.otra_persona for o in BienesPersonas.objects.filter(activos_bienes = self.activos_bienes,cat_tipo_participacion_id=BienesPersonas.FIDUCIARIO)]
        except Exception as e:
            return None

    def observacion(self):
        return [self.observaciones]
    def porcentajes(self):
        try:
            return [BienesPersonas.objects.filter(
                activos_bienes=self.activos_bienes,
                cat_tipo_participacion_id=BienesPersonas.DECLARANTE,
            ).first().porcentaje]
        except:
            None

    def columna_uno(self):
        if self.cat_tipos_operaciones:
            return u"{}".format(self.cat_tipos_operaciones)
        else:
            return u""

    def columna_dos(self):
        if self.cat_tipos_fideicomisos:
            return u"{}".format(self.cat_tipos_fideicomisos)
        else:
            return u""

    def columna_tres(self):
        if self.nombre_fideicomiso:
            return u"{}".format(self.nombre_fideicomiso)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:fideicomisos-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:fideicomisos-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:fideicomisos',
                            kwargs={'folio': self.declaraciones.folio})

    def tipo_operacion(self):
        try:
            if self.cat_tipos_operaciones.default:
                return u"{} {}".format(self.cat_tipos_operaciones,
                                       self.otra_operacion)
            else:
                return u"{}".format(self.cat_tipos_operaciones)
        except Exception as e:
            return u""

    def tipo_fideicomiso(self):
        try:
            if self.cat_tipos_fideicomisos.default:
                return u"{} {}".format(self.cat_tipos_fideicomisos,
                                       self.otro_fideicomiso)
            else:
                return u"{}".format(self.cat_tipos_fideicomisos)
        except Exception as e:
            return u""


class BienesIntangibles(models.Model):
    otra_operacion = models.CharField(max_length=255, blank=True)
    descripcion = models.CharField(max_length=255, blank=True)
    otra_dependencia = models.CharField(max_length=255, blank=True)
    num_registro = models.CharField(max_length=255, blank=True)
    fecha_registro = models.DateField(null=True, blank=True)
    otro_sector = models.CharField(max_length=255, blank=True)
    precio_adquisicion = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    otra_forma = models.CharField(max_length=255, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    activos_bienes = models.ForeignKey(ActivosBienes, on_delete=models.DO_NOTHING)
    precio_total_adquisicion = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_formas_adquisiciones = models.ForeignKey(CatFormasAdquisiciones, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_monedas = models.ForeignKey(CatMonedas, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_sectores_industria = models.ForeignKey(CatSectoresIndustria, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_operaciones = models.ForeignKey(CatTiposOperaciones, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    cat_entes_publicos = models.ForeignKey(CatEntesPublicos, on_delete=models.DO_NOTHING, null=True, blank=True)
    otro_ente = models.CharField(max_length=255, blank=True, null=True)

    def observacion(self):
        return [self.observaciones]

    def columna_uno(self):
        if self.cat_tipos_operaciones:
            return u"{}".format(self.cat_tipos_operaciones)
        else:
            return u""

    def columna_dos(self):
        if self.cat_formas_adquisiciones:
            return u"{}".format(self.cat_formas_adquisiciones)
        else:
            return u""

    def columna_tres(self):
        if self.cat_sectores_industria:
            return u"{}".format(self.cat_sectores_industria)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:bienes-intangibles-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:bienes-intangibles-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:bienes-intangibles',
                            kwargs={'folio': self.declaraciones.folio})

    def tipo_operacion(self):
        try:
            if self.cat_tipos_operaciones.default:
                return u"{} {}".format(self.cat_tipos_operaciones,
                                       self.otra_operacion)
            else:
                return u"{}".format(self.cat_tipos_operaciones)
        except Exception as e:
            return u""

    def sectores_industrias(self):
        try:
            if self.cat_sectores_industria.default:
                return u"{} {}".format(self.cat_sectores_industria,
                                       self.otro_sector)
            else:
                return u"{}".format(self.cat_sectores_industria)
        except Exception as e:
            return u""

    def forma_adquisicion(self):
        try:
            if self.cat_formas_adquisiciones.default:
                return u"{} {}".format(self.cat_formas_adquisiciones,
                                       self.otra_forma)
            else:
                return u"{}".format(self.cat_formas_adquisiciones)
        except Exception as e:
            return u""

    def copropietario(self):
        try:
            return BienesPersonas.objects.filter(activos_bienes = self.activos_bienes,cat_tipo_participacion_id=BienesPersonas.COPROPIETARIO)
        except Exception as e:
            return None

class CuentasPorCobrar(models.Model):
    fecha_prestamo = models.DateField(null=True, blank=True)
    monto_original = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    num_registro = models.CharField(max_length=255, blank=True)
    saldo_pendiente = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_monedas = models.ForeignKey(CatMonedas, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    info_personal_var = models.ForeignKey(InfoPersonalVar, on_delete=models.DO_NOTHING, blank=True, null=True)
    activos_bienes = models.ForeignKey(ActivosBienes, on_delete=models.DO_NOTHING, blank=True, null=True)

    def observacion(self):
        return [self.observaciones]

    def columna_uno(self):
        try:
            if self.info_personal_var.es_fisica:
                return u"{} {} {}".format(
                    self.info_personal_var.nombres,
                    self.info_personal_var.apellido1,
                    self.info_personal_var.apellido2,
                    )
            else:
                return u"{}".format(self.info_personal_var.razon_social)
        except Exception as e:
            return u""

    def columna_dos(self):
        if self.monto_original:
            return u"{}".format(self.monto_original)
        else:
            return u""

    def columna_tres(self):
        if self.saldo_pendiente:
            return u"{}".format(self.saldo_pendiente)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:cuentas-por-cobrar-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:cuentas-por-cobrar-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:cuentas-por-cobrar',
                            kwargs={'folio': self.declaraciones.folio})

    def prestatario(self):
        try:
            return BienesPersonas.objects.filter(activos_bienes = self.activos_bienes,cat_tipo_participacion_id=BienesPersonas.PRESTATARIO_O_DEUDOR)
        except Exception as e:
            return None


class BeneficiosEspecie(models.Model):
    tipo_bien_servicio = models.CharField(max_length=255, blank=True)
    valor_mercado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    otro_familiar = models.CharField(max_length=255, blank=True)
    otra_relacion = models.CharField(max_length=255, blank=True)
    otra_relacion_familiar = models.CharField(max_length=255, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_sectores_industria = models.ForeignKey(CatSectoresIndustria, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_relaciones_personales = models.ForeignKey(CatTiposRelacionesPersonales, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    domicilios = models.ForeignKey(Domicilios, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    info_personal_var = models.ForeignKey(InfoPersonalVar, on_delete=models.DO_NOTHING)

    def observacion(self):
        return [self.observaciones]

    def columna_uno(self):
        if self.tipo_bien_servicio:
            return u"{}".format(self.tipo_bien_servicio)
        else:
            return u""

    def columna_dos(self):
        if self.cat_tipos_relaciones_personales:
            return u"{}".format(self.cat_tipos_relaciones_personales)
        else:
            return u""

    def columna_tres(self):
        if self.cat_sectores_industria:
            return u"{}".format(self.cat_sectores_industria)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:beneficios-especie-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:beneficios-especie-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:beneficios-especie',
                            kwargs={'folio': self.declaraciones.folio})

    def sectores_industrias(self):
        try:
            if self.cat_sectores_industria.default:
                return u"{} {}".format(self.cat_sectores_industria,
                                       self.otro_sector)
            else:
                return u"{}".format(self.cat_sectores_industria)
        except Exception as e:
            return u""

    def tipo_relacion(self):
        try:
            if self.cat_tipos_relaciones_personales.default:
                return u"{} {}".format(self.cat_tipos_relaciones_personales,
                                       self.otro_familiar)
            else:
                return u"{}".format(self.cat_tipos_relaciones_personales)
        except Exception as e:
            return u""
