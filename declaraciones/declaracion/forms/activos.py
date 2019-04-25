from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from declaracion.models import (BienesMuebles, BienesInmuebles,
                                MueblesNoRegistrables, Inversiones,
                                EfectivoMetales, Fideicomisos,
                                BienesIntangibles, CuentasPorCobrar,
                                BeneficiosEspecie, ActivosBienes, BienesPersonas)


class ActivosBienesForm(forms.ModelForm):
    class Meta:
        model = ActivosBienes
        exclude = '__all__'


class BienesPersonasForm(forms.ModelForm):
    class Meta:
        model = BienesPersonas
        fields = '__all__'
        exclude = ['info_personal_var', 'activos_bienes',
                   'otra_persona', 'cat_tipo_participacion']


class BienesMueblesForm(forms.ModelForm):
    class Meta:
        model = BienesMuebles
        fields = '__all__'
        exclude = ['declaraciones', 'observaciones', 'activos_bienes']
        widgets = {'fecha_adquisicion': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        })}

class BienesInmueblesForm(forms.ModelForm):
    class Meta:
        model = BienesInmuebles
        fields = '__all__'
        exclude = ['declaraciones', 'domicilios', 'observaciones',
                   'activos_bienes']
        widgets = {'fecha_adquisicion': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        }),'fecha_contrato_compra': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        })}

class MueblesNoRegistrablesForm(forms.ModelForm):
    class Meta:
        model = MueblesNoRegistrables
        fields = '__all__'
        exclude = ['declaraciones', 'observaciones', 'activos_bienes']
        widgets = {'fecha_adquisicion': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        })}

class InversionesForm(forms.ModelForm):
    class Meta:
        model = Inversiones
        fields = '__all__'
        exclude = ['declaraciones', 'domicilios', 'observaciones',
                   'info_personal_var']
        widgets = {'fecha_inicio': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        })}

class EfectivoMetalesForm(forms.ModelForm):
    class Meta:
        model = EfectivoMetales
        fields = '__all__'
        exclude = ['declaraciones', 'observaciones']


class FideicomisosForm(forms.ModelForm):
    class Meta:
        model = Fideicomisos
        fields = '__all__'
        exclude = ['declaraciones', 'observaciones',
                   'domicilio_fideicomisario', 'domicilio_fideicomitente',
                   'domicilio_fiduciario', 'activos_bienes']
        widgets = {'fecha_creacion': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        })}


class BienesIntangiblesForm(forms.ModelForm):
    class Meta:
        model = BienesIntangibles
        fields = '__all__'
        exclude = ['declaraciones', 'observaciones', 'activos_bienes']
        widgets = {'fecha_registro': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        }),'fecha_vencimiento': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        })}


class CuentasPorCobrarForm(forms.ModelForm):
    class Meta:
        model = CuentasPorCobrar
        fields = '__all__'
        exclude = ['declaraciones', 'observaciones', 'domicilios',
                   'info_personal_var']
        widgets = {'fecha_prestamo': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        }),'fecha_vencimiento': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True

        })}


class BeneficiosEspecieForm(forms.ModelForm):
    class Meta:
        model = BeneficiosEspecie
        fields = '__all__'
        exclude = ['declaraciones', 'observaciones','domicilios',
                   'info_personal_var']
        widgets = {'fecha_inicio': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        })}
