from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from declaracion.models import (DeudasOtros)

class DeudasForm(forms.ModelForm):
    garantia = forms.TypedChoiceField(
                   coerce=lambda x: x == 'True',
                   choices=((False, 'False'), (True, 'True')),
                   widget=forms.RadioSelect
                )

    class Meta:
        model = DeudasOtros
        fields = '__all__'
        exclude = ['declaraciones', 'domicilios', 'observaciones',
                   'cat_tipos_pasivos', 'acreedor_infopersonalvar']
        widgets = {'fecha_generacion': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        })}
class DeudasOtrosForm(forms.ModelForm):
    class Meta:
        model = DeudasOtros
        fields = '__all__'
        exclude = ['declaraciones', 'domicilios', 'observaciones',
                   'cat_tipos_pasivos', 'acreedor_infopersonalvar']
        widgets = {'fecha_generacion': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        })}