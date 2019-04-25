from django.db import models
from django.urls import reverse_lazy
from .informacion_personal import(Declaraciones, Domicilios, Observaciones, InfoPersonalVar)
from .catalogos import (CatTiposPasivos, CatTiposOperaciones, CatTiposAcreedores,
                        CatTiposAdeudos, CatPaises, CatSectoresIndustria,
                        CatMonedas, CatTiposTitulares, CatUnidadesTemporales)


class DeudasOtros(models.Model):
    otra_operacion = models.CharField(max_length=255, blank=True)
    otro_tipo_acreedor = models.CharField(max_length=255, blank=True)
    otro_tipo_adeudo = models.CharField(max_length=255, blank=True)
    numero_cuenta = models.CharField(max_length=255, blank=True)
    fecha_generacion = models.DateField(null=True, blank=True)
    monto_original = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    saldo_pendiente = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    monto_abonado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    plazo = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    otro_titular = models.CharField(max_length=255, blank=True)
    porcentaje_adeudo = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    garantia = models.BooleanField(blank=True, null=True, default=None)
    nombre_garantes = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cat_monedas = models.ForeignKey(CatMonedas, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_paises = models.ForeignKey(CatPaises, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_acreedores = models.ForeignKey(CatTiposAcreedores, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_adeudos = models.ForeignKey(CatTiposAdeudos, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_operaciones = models.ForeignKey(CatTiposOperaciones, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_pasivos = models.ForeignKey(CatTiposPasivos, on_delete=models.DO_NOTHING, null=True, blank=True)
    cat_tipos_titulares = models.ForeignKey(CatTiposTitulares, on_delete=models.DO_NOTHING, null=True, blank=True)
    declaraciones = models.ForeignKey(Declaraciones, on_delete=models.DO_NOTHING)
    observaciones = models.ForeignKey(Observaciones, on_delete=models.DO_NOTHING)
    acreedor_infopersonalvar = models.ForeignKey(InfoPersonalVar, on_delete=models.DO_NOTHING)
    cat_unidades_temporales = models.ForeignKey(CatUnidadesTemporales, on_delete=models.DO_NOTHING, null=True, blank=True)
    def observacion(self):
        return [self.observaciones]
    def persona(self):
        return [self.acreedor_infopersonalvar]

    def columna_uno(self):
        if self.cat_tipos_operaciones:
            return u"{}".format(self.cat_tipos_operaciones)
        else:
            return u""

    def columna_dos(self):
        if self.cat_tipos_acreedores:
            return u"{}".format(self.cat_tipos_acreedores)
        else:
            return u""

    def columna_tres(self):
        if self.cat_tipos_adeudos:
            return u"{}".format(self.cat_tipos_adeudos)
        else:
            return u""

    def url(self):
        if self.cat_tipos_pasivos_id == 1:
            return u"deudas"
        else:
            return u"deudas-otros"

    def url_editar(self):
            return reverse_lazy('declaracion:' + self.url() + '-editar',
                                kwargs={'folio': self.declaraciones.folio,
                                        'pk': self.id})

    def url_borrar(self):
        return reverse_lazy('declaracion:' + self.url() + '-borrar',
                            kwargs={'folio': self.declaraciones.folio,
                                    'pk': self.id})

    def url_todos(self):
        return reverse_lazy('declaracion:' + self.url() + '',
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

    def tipo_acreedor(self):
        try:
            if self.cat_tipos_acreedores.default:
                return u"{} {}".format(self.cat_tipos_acreedores,
                                       self.otro_tipo_acreedor)
            else:
                return u"{}".format(self.cat_tipos_acreedores)
        except Exception as e:
            return u""

    def tipo_adeudo(self):
        try:
            if self.cat_tipos_adeudos.default:
                return u"{} {}".format(self.cat_tipos_adeudos,
                                       self.otro_tipo_adeudo)
            else:
                return u"{}".format(self.cat_tipos_adeudos)
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
