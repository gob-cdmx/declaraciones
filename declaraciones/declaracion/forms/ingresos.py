from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from declaracion.models import (SueldosPublicos,IngresosVarios)


class SueldosPublicosForm(forms.ModelForm):
    class Meta:
        model = SueldosPublicos
        fields = '__all__'
        exclude = ['declaraciones', 'domicilios', 'observaciones']
        widgets = {'fecha_transaccion': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        })}
class IngresosVariosForm(forms.ModelForm):
    class Meta:
        model = IngresosVarios
        fields = '__all__'
        exclude = ['declaraciones', 'domicilios', 'observaciones',
                   'cat_tipos_ingresos_varios', 'info_personal_var']
        widgets = {'es_transaccion': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        })}

