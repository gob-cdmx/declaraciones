from django.db import models
from django.urls import reverse_lazy
from .informacion_personal import(Declaraciones, Observaciones,
                                  InfoPersonalVar)
from .catalogos import (CatEntesPublicos, CatMonedas, CatTiposActividad,
                        CatTiposIngresosVarios, CatTiposMuebles)


class SueldosPublicos(models.Model):
    rfc = models.CharField(max_length=255, blank=True)
    ingreso_bruto_anual = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    duracion_dias = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    duracion_meses = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    duracion_anual = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_entes_publicos = models.ForeignKey(CatEntesPublicos, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_monedas = models.ForeignKey(CatMonedas, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    es_transaccion = models.BooleanField(blank=True, null=True, default=None)
    fecha_transaccion = models.DateField(blank=True, null=True)
    otro_ente = models.CharField(max_length=255, blank=True, null=True)

    def observacion(self):
        return [self.observaciones]


class IngresosVarios(models.Model):
    ingreso_bruto_anual = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    duracion_dias = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    duracion_meses = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    duracion_anual = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_monedas = models.ForeignKey(CatMonedas, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_actividad = models.ForeignKey(CatTiposActividad, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_ingresos_varios = models.ForeignKey(CatTiposIngresosVarios, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    otra_actividad = models.CharField(max_length=255, blank=True)
    es_transaccion = models.DateField(blank=True, null=True)
    info_personal_var = models.ForeignKey(InfoPersonalVar, on_delete=models.DO_NOTHING)
    es_mueble = models.BooleanField(blank=True, null=True, default=None)
    cat_tipos_muebles = models.ForeignKey(CatTiposMuebles, on_delete=models.DO_NOTHING, blank=True, null=True)
    otro_mueble = models.CharField(max_length=255, blank=True, null=True)
    descripcion_actividad = models.CharField(max_length=255, blank=True, null=True)
    def observacion(self):
        return [self.observaciones]

    def persona(self):
        return [self.info_personal_var]
    def domicilio(self):
        return [self.info_personal_var.domicilios]

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
        if self.cat_tipos_actividad:
            return u"{}".format(self.cat_tipos_actividad)
        else:
            return u""

    def columna_tres(self):
        if self.info_personal_var.cat_sectores_industria:
            return u"{}".format(self.info_personal_var.cat_sectores_industria)
        else:
            return u""

    def url_editar(self):
        return reverse_lazy('declaracion:ingresos-varios-editar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'tipo': int(self.cat_tipos_ingresos_varios_id) - 1,
                                    'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:ingresos-varios-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'tipo': int(self.cat_tipos_ingresos_varios_id) - 1,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:ingresos-varios',
                            kwargs={'folio': self.declaraciones.folio,
                                    'tipo': self.cat_tipos_ingresos_varios_id})

    def tipo_actividad(self):
        try:
            if self.cat_tipos_actividad.default:
                return u"{} {}".format(self.cat_tipos_actividad,
                                       self.otra_actividad)
            else:
                return u"{}".format(self.cat_tipos_actividad)
        except Exception as e:
            return u""
