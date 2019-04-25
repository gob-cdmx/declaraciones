from django.db import models
from django.urls import reverse_lazy
from .informacion_personal import(Declaraciones, Domicilios, Observaciones,
                                  InfoPersonalVar)
from .catalogos import (CatPaises, CatSectoresIndustria,
                        CatTiposInstituciones, CatNaturalezaMembresia,
                        CatOrdenesGobierno, CatTiposApoyos,
                        CatTitularTiposRelaciones, CatTiposBeneficios,
                        CatEntesPublicos, CatMonedas, CatTiposIngresosVarios,
                        CatTiposActividad, CatTiposMuebles, CatTiposBienes,
                        CatTiposRepresentaciones)


class EmpresasSociedades(models.Model):
    rol_empresa = models.CharField(max_length=255, blank=True)
    actividad_economica = models.BooleanField(blank=True, null=True, default=None)
    porcentaje_participacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    empresa_infopersonalvar = models.ForeignKey(InfoPersonalVar, on_delete=models.DO_NOTHING, related_name="empresa_empresas_sociedades")
    declarante_infopersonalvar = models.ForeignKey(InfoPersonalVar, on_delete=models.DO_NOTHING, related_name="declarante_empresas_sociedades")

    def columna_uno(self):
        if self.empresa_infopersonalvar.razon_social:
            return u"{}".format(
                self.empresa_infopersonalvar.razon_social)
        else:
            return u""

    def columna_dos(self):
        if self.rol_empresa:
            return u"{}".format(self.rol_empresa)
        else:
            return u""

    def columna_tres(self):
        if self.empresa_infopersonalvar.cat_sectores_industria:
            return u"{}".format(self.empresa_infopersonalvar.cat_sectores_industria)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:empresas-sociedades-asociaciones-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:empresas-sociedades-asociaciones-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:empresas-sociedades-asociaciones',
                            kwargs={'folio': self.declaraciones.folio})

    def observacion(self):
        return [self.observaciones]

    def persona(self):
        return [self.empresa_infopersonalvar]

    def domicilio(self):
        return [self.empresa_infopersonalvar.domicilios]


class Membresias(models.Model):
    otras_instituciones = models.CharField(max_length=255, blank=True)
    nombre_institucion = models.CharField(max_length=255, blank=True)
    otro_sector = models.CharField(max_length=255, blank=True)
    puesto_rol = models.CharField(max_length=255, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    pagado = models.BooleanField(blank=True, null=True, default=None)
    monto = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_naturaleza_membresia = models.ForeignKey(CatNaturalezaMembresia, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_sectores_industria = models.ForeignKey(CatSectoresIndustria, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_instituciones = models.ForeignKey(CatTiposInstituciones, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    domicilios = models.ForeignKey(Domicilios, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    otra_naturaleza = models.CharField(max_length=255, blank=True, null=True)

    def columna_uno(self):
        if self.nombre_institucion:
            return u"{}".format(
                self.nombre_institucion)
        else:
            return u""

    def columna_dos(self):
        if self.cat_tipos_instituciones:
            return u"{}".format(self.cat_tipos_instituciones)
        else:
            return u""

    def columna_tres(self):
        if self.cat_sectores_industria:
            return u"{}".format(self.cat_sectores_industria)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:membresias-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:membresias-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:membresias',
                            kwargs={'folio': self.declaraciones.folio})

    def observacion(self):
        return [self.observaciones]

    def domicilio(self):
        return [self.domicilios]

    def tipos_instituciones(self):
        try:
            if self.cat_tipos_instituciones.default:
                return u"{} {}".format(self.cat_tipos_instituciones,
                                    self.otras_instituciones)
            else:
                return u"{}".format(self.cat_tipos_instituciones)
        except Exception as e:
            return u""

    def naturaleza(self):
        try:
            if self.cat_naturaleza_membresia.default:
                return u"{} {}".format(self.cat_naturaleza_membresia,
                                    self.otra_naturaleza)
            else:
                return u"{}".format(self.cat_naturaleza_membresia)
        except Exception as e:
            return u""

    def tipo_sector(self):
        try:
            if self.cat_sectores_industria.default:
                return u"{} {}".format(self.cat_sectores_industria,
                                    self.otro_sector)
            else:
                return u"{}".format(self.cat_sectores_industria)
        except Exception as e:
            return u""


class Apoyos(models.Model):
    nombre_programa = models.CharField(max_length=255, blank=True)
    institucion_otorgante = models.CharField(max_length=255, blank=True)
    otro_apoyo = models.CharField(max_length=255, blank=True)
    valor_anual = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    cat_ordenes_gobierno = models.ForeignKey(CatOrdenesGobierno, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_apoyos = models.ForeignKey(CatTiposApoyos, on_delete=models.DO_NOTHING, null=True, blank=True)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    beneficiario_infopersonalvar = models.ForeignKey(InfoPersonalVar, on_delete=models.DO_NOTHING)

    def columna_uno(self):
        if self.nombre_programa:
            return u"{}".format(
                self.nombre_programa)
        else:
            return u""

    def columna_dos(self):
        if self.institucion_otorgante:
            return u"{}".format(self.institucion_otorgante)
        else:
            return u""

    def columna_tres(self):
        if self.cat_tipos_apoyos:
            return u"{}".format(self.cat_tipos_apoyos)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:apoyos-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:apoyos-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:apoyos',
                            kwargs={'folio': self.declaraciones.folio})

    def observacion(self):
        return [self.observaciones]

    def tipos_apoyos(self):
        try:
            if self.cat_tipos_apoyos.default:
                return u"{} {}".format(self.cat_tipos_apoyos,
                                       self.otro_apoyo)
            else:
                return u"{}".format(self.cat_tipos_apoyos)
        except Exception as e:
            return u""


class Representaciones(models.Model):
    cat_tipos_representaciones = models.ForeignKey(CatTiposRepresentaciones, on_delete=models.DO_NOTHING, null=True, blank=True)
    otra_representacion = models.CharField(max_length=255, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    pagado = models.BooleanField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    es_representacion_activa = models.BooleanField(blank=True, null=True, default=None)
    monto = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    info_personal_var = models.ForeignKey(InfoPersonalVar, on_delete=models.DO_NOTHING)
    es_mueble = models.BooleanField(blank=True, null=True, default=None)
    cat_tipos_muebles = models.ForeignKey(CatTiposMuebles, on_delete=models.DO_NOTHING, null=True, blank=True)
    otro_mueble = models.CharField(max_length=255, blank=True, null=True)

    def observacion(self):
        return [self.observaciones]

    def persona(self):
        return [self.info_personal_var]

    def nacionalidad(self):
        return self.info_personal_var.nacionalidad()

    def url(self):
        if self.es_representacion_activa == True:
            return u"activa"
        else:
            return u"pasiva"

    def columna_uno(self):
        return u"{}".format(self.cat_tipos_representaciones)

    def columna_dos(self):
        if self.info_personal_var:
            return u"{}".format(self.info_personal_var.cat_sectores_industria)
        else:
            return u""

    def columna_tres(self):
        if self.info_personal_var:
            return u"{}".format(self.info_personal_var.nombres)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:representacion-' + self.url() + '-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:representacion-' + self.url() + '-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:representacion-' + self.url() + '',
                            kwargs={'folio': self.declaraciones.folio})

    def representaciones(self):
        try:
            if self.cat_tipos_representaciones.default:
                return u"{} {}".format(self.cat_tipos_representaciones,
                                       self.otra_representacion)
            else:
                return u"{}".format(self.cat_tipos_representaciones)
        except Exception as e:
            return u""


class SociosComerciales(models.Model):
    actividad_vinculante = models.CharField(max_length=255, blank=True)
    tipo_vinculo = models.CharField(max_length=255, blank=True)
    antiguedad_vinculo = models.CharField(max_length=255, blank=True)
    rfc_entidad_vinculante = models.CharField(max_length=255, blank=True)
    porcentaje_participacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    socio_infopersonalvar = models.ForeignKey(InfoPersonalVar, on_delete=models.DO_NOTHING)

    def columna_uno(self):
        if self.actividad_vinculante:
            return u"{}".format(
                self.actividad_vinculante)
        else:
            return u""


    def columna_dos(self):
        if self.tipo_vinculo:
            return u"{}".format(self.tipo_vinculo)
        else:
            return u""

    def columna_tres(self):
        if self.socio_infopersonalvar.cat_sectores_industria:
            return u"{}".format(self.socio_infopersonalvar.cat_sectores_industria)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:socios-comerciales-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:socios-comerciales-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:socios-comerciales',
                            kwargs={'folio': self.declaraciones.folio})
    def observacion(self):
        return [self.observaciones]

    def persona(self):
        return [self.socio_infopersonalvar]


class ClientesPrincipales(models.Model):
    porcentaje_facturacion_cliente = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    info_personal_var = models.ForeignKey(InfoPersonalVar, on_delete=models.DO_NOTHING)
    nombre_encargado = models.CharField(max_length=255, blank=True, null=True)

    def columna_uno(self):
        if self.info_personal_var.nombre_negocio:
            return u"{}".format(
                self.info_personal_var.nombre_negocio)
        else:
            return u""

    def columna_dos(self):
        if self.info_personal_var.num_id_identificacion:
            return u"{}".format(self.info_personal_var.num_id_identificacion)
        else:
            return u""

    def columna_tres(self):
        if self.info_personal_var.cat_sectores_industria:
            return u"{}".format(self.info_personal_var.cat_sectores_industria)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:clientes-principales-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:clientes-principales-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:clientes-principales',
                            kwargs={'folio': self.declaraciones.folio})
    def observacion(self):
        return [self.observaciones]

    def persona(self):
        return [self.info_personal_var]


class OtrasPartes(models.Model):
    fecha_inicio_relacion = models.DateField(null=True, blank=True)
    otra_relacion = models.CharField(max_length=255, blank=True)
    otra_relacion_familiar = models.CharField(max_length=255, blank=True)
    ocupacion_profesion = models.CharField(max_length=255, blank=True)
    intereses_comunes = models.BooleanField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_titular_tipos_relaciones = models.ForeignKey(CatTitularTiposRelaciones, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    declarante_infopersonalvar = models.ForeignKey(InfoPersonalVar, on_delete=models.DO_NOTHING, related_name="declarante_otras_partes")
    otraspartes_infopersonalvar = models.ForeignKey(InfoPersonalVar, on_delete=models.DO_NOTHING, related_name="otraspartes_otras_partes")

    def columna_uno(self):
        return u"{} {} {}{}".format(
            self.otraspartes_infopersonalvar.nombres,
            self.otraspartes_infopersonalvar.apellido1,
            self.otraspartes_infopersonalvar.apellido2,
            self.otraspartes_infopersonalvar.razon_social)

    def columna_dos(self):
        if self.cat_titular_tipos_relaciones:
            return u"{}".format(self.cat_titular_tipos_relaciones)
        else:
            return u""

    def columna_tres(self):
        if self.otraspartes_infopersonalvar.cat_sectores_industria:
            return u"{}".format(self.otraspartes_infopersonalvar.cat_sectores_industria)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:otras-partes-relacionadas-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:otras-partes-relacionadas-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:otras-partes-relacionadas',
                            kwargs={'folio': self.declaraciones.folio})

    def observacion(self):
        return [self.observaciones]


    def persona(self):
        return [self.otraspartes_infopersonalvar]

    def nacionalidad(self):
        return self.otraspartes_infopersonalvar.nacionalidad()

    def tipos_relaciones(self):
        try:
            if self.cat_titular_tipos_relaciones.default:
                return u"{} {}".format(self.cat_titular_tipos_relaciones,
                                       self.otra_relacion)
            else:
                return u"{}".format(self.cat_titular_tipos_relaciones)
        except Exception as e:
            return u""


class BeneficiosGratuitos(models.Model):
    otros_beneficios = models.CharField(max_length=255, blank=True)
    origen_beneficio = models.CharField(max_length=255, blank=True)
    otro_sector = models.CharField(max_length=255, blank=True)
    valor_beneficio = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_sectores_industria = models.ForeignKey(CatSectoresIndustria, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_beneficios = models.ForeignKey(CatTiposBeneficios, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)

    def columna_uno(self):
        if self.cat_tipos_beneficios:
            return u"{}".format(
                self.cat_tipos_beneficios)
        else:
            return u""

    def columna_dos(self):
        if self.origen_beneficio:
            return u"{}".format(self.origen_beneficio)
        else:
            return u""

    def columna_tres(self):
        if self.cat_sectores_industria:
            return u"{}".format(self.cat_sectores_industria)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:beneficios-gratuitos-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:beneficios-gratuitos-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:beneficios-gratuitos',
                            kwargs={'folio': self.declaraciones.folio})
    def observacion(self):
        return [self.observaciones]

    def sectores_industrias(self):
        try:
            if self.cat_sectores_industria.default:
                return u"{} {}".format(self.cat_sectores_industria,
                                       self.otro_sector)
            else:
                return u"{}".format(self.cat_sectores_industria)
        except Exception as e:
            return u""


    def tipo_beneficio(self):
        try:
            if self.cat_tipos_beneficios.default:
                return u"{} {}".format(self.cat_tipos_beneficios,
                                       self.otros_beneficios)
            else:
                return u"{}".format(self.cat_tipos_beneficios)
        except Exception as e:
            return u""
