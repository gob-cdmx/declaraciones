from django.db import models


class CatActivoBien(models.Model):
    activo_bien = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.activo_bien


class CatAmbitosLaborales(models.Model):
    ambito_laboral = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.ambito_laboral


class CatDocumentosObtenidos(models.Model):
    documento_obtenido = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.documento_obtenido


class CatEntesPublicos(models.Model):
    ente_publico = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.ente_publico


class CatEntidadesFederativas(models.Model):
    entidad_federativa = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.entidad_federativa


class CatEstadosCiviles(models.Model):
    estado_civil = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.estado_civil


class CatEstatusDeclaracion(models.Model):
    estatus_declaracion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.estatus_declaracion


class CatEstatusEstudios(models.Model):
    estatus_estudios = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.estatus_estudios


class CatFormasAdquisiciones(models.Model):
    forma_adquisicion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.forma_adquisicion


class CatFuncionesPrincipales(models.Model):
    funcion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.funcion


class CatGradosAcademicos(models.Model):
    grado_academico = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.grado_academico


class CatMonedas(models.Model):
    moneda = models.CharField(max_length=255)
    moneda_abrev = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    class Meta:
        ordering = ["moneda"]

    def __str__(self):
        return self.moneda


class CatNaturalezaMembresia(models.Model):
    naturaleza_membresia = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    class Meta:
        ordering = ["orden"]

    def __str__(self):
        return self.naturaleza_membresia


class CatOrdenesGobierno(models.Model):
    orden_gobierno = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.orden_gobierno


class CatPaises(models.Model):
    pais = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=3)

    def __str__(self):
        return self.pais


class CatPoderes(models.Model):
    poder = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.poder


class CatRegimenesMatrimoniales(models.Model):
    regimen_matrimonial = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.regimen_matrimonial


class CatSectoresIndustria(models.Model):
    sector_industria = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.sector_industria


class CatTipoParticipacion(models.Model):
    tipo_participacion = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_participacion


class CatTipoPersona(models.Model):
    tipo_persona = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_persona


class CatTipoVia(models.Model):
    tipo_via = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_via


class CatTiposAcreedores(models.Model):
    tipo_acreedor = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_acreedor


class CatTiposActividad(models.Model):
    tipo_actividad = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_actividad


class CatTiposAdeudos(models.Model):
    tipo_adeudo = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_adeudo


class CatTiposApoyos(models.Model):
    tipo_apoyo = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_apoyo


class CatTiposBeneficios(models.Model):
    tipo_beneficio = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_beneficio


class CatTiposBienes(models.Model):
    tipo_bien = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_bien


class CatTiposDeclaracion(models.Model):
    tipo_declaracion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_declaracion


class CatTiposEspecificosInversiones(models.Model):
    tipo_especifico_inversion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_especifico_inversion


class CatTiposFideicomisos(models.Model):
    tipo_fideicomiso = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_fideicomiso


class CatTiposIngresosVarios(models.Model):
    tipo_ingreso_varios = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_ingreso_varios


class CatTiposInmuebles(models.Model):
    tipo_inmueble = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_inmueble


class CatTiposInstituciones(models.Model):
    tipo_institucion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_institucion


class CatTiposInversiones(models.Model):
    tipo_inversion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_inversion


class CatTiposMetales(models.Model):
    tipo_metal = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_metal


class CatTiposMuebles(models.Model):
    tipo_mueble = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_mueble


class CatTiposOperaciones(models.Model):
    tipo_operacion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_operacion


class CatTiposPasivos(models.Model):
    tipo_pasivo = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_pasivo


class CatTiposRelacionesPersonales(models.Model):
    tipo_relacion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    grupo_familia = models.IntegerField(blank=True, null=True)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_relacion


class CatTiposRepresentaciones(models.Model):
    tipo_representacion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_representacion


class CatTiposTitulares(models.Model):
    tipo_titular = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_titular


class CatTitularTiposRelaciones(models.Model):
    tipo_relacion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.tipo_relacion


class CatUnidadesTemporales(models.Model):
    unidad_temporal = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.IntegerField(default=0)
    orden = models.IntegerField(default=1)
    codigo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.unidad_temporal
