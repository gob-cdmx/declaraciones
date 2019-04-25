import uuid
from django.db import models
from .informacion_personal import(Declaraciones, Observaciones)
from mptt.models import MPTTModel, TreeForeignKey


class SeccionDeclaracion(models.Model):
    PENDIENTE = 0
    COMPLETA = 1
    INCOMPLETA = 2
    STATUS_CHOICES = (
        (PENDIENTE, 'Pendiente'),
        (COMPLETA, 'Completa'),
        (INCOMPLETA, 'Incompleta'),
        )
    declaraciones = models.ForeignKey(Declaraciones,
                                    on_delete=models.CASCADE)
    seccion = models.ForeignKey('Secciones',
                                on_delete=models.CASCADE,
                                related_name='status')
    estatus = models.IntegerField(default=PENDIENTE, choices=STATUS_CHOICES)
    observaciones = models.ForeignKey(Observaciones,
                                      on_delete=models.CASCADE,
                                      verbose_name="",
                                      null=True,
                                      default=None)
    aplica = models.BooleanField()
    max = models.IntegerField(default=1)
    num = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Secciones(MPTTModel):
    seccion = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    parametro = models.CharField(max_length=255, blank=True, default='')
    order = models.IntegerField(default=1)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def get_status(self, folio):

        try:
            folio = uuid.UUID(folio)
        except:
            return ('', '')
        declaracion = Declaraciones.objects.filter(folio=folio).first()

        try:


            status = SeccionDeclaracion.objects.filter(seccion=self).filter(declaraciones=declaracion).first()

            if status is None:
                return ('','')
            if status.num==0:
                return ('','')
            elif status.num == status.max:
                return ('success',"100%")
            elif status.num < status.max:
                return ('in-progress', str(status.num)+"/"+str(status.max) )
            else:
                return ('','')
        except:
            return ('', '')




    def __str__(self):
        return self.seccion

class CatCamposObligatorios(models.Model):
    seccion = models.ForeignKey(Secciones, models.DO_NOTHING, blank=True, null=True)
    nombre_tabla = models.CharField(max_length=255, blank=True, null=True)
    nombre_columna = models.CharField(max_length=255, blank=True, null=True)
    es_obligatorio = models.IntegerField(blank=True, null=True)
    es_principal = models.BooleanField(default=False)
    esta_pantalla = models.BooleanField(default=False)
    tipo = models.IntegerField(default=0)

