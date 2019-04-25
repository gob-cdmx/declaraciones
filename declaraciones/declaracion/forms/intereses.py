from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from declaracion.models import (EmpresasSociedades, Membresias,
                                Representaciones, SociosComerciales,
                                ClientesPrincipales, OtrasPartes,
                                BeneficiosGratuitos, Apoyos)

class EmpresasSociedadesForm(forms.ModelForm):
    class Meta:
        model = EmpresasSociedades
        fields = '__all__'
        exclude = ['declaraciones', 'domicilios', 'observaciones',
                   'empresa_infopersonalvar', 'declarante_infopersonalvar']

class MembresiasForm(forms.ModelForm):
    class Meta:
        model = Membresias
        fields = '__all__'
        exclude = ['declaraciones', 'domicilios', 'observaciones']
        widgets = {'fecha_inicio': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        })}
class ApoyosForm(forms.ModelForm):
    class Meta:
        model = Apoyos
        fields = '__all__'
        exclude = ['declaraciones', 'observaciones', 'beneficiario_infopersonalvar']

class RepresentacionesActivasForm(forms.ModelForm):
    class Meta:
        model = Representaciones
        fields = '__all__'
        exclude = ['declaraciones', 'observaciones', 'info_personal_var']
        widgets = {'fecha_inicio': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        })}
class RepresentacionesPasivasForm(forms.ModelForm):
    class Meta:
        model = Representaciones
        fields = '__all__'
        exclude = ['declaraciones', 'observaciones', 'info_personal_var']
        widgets = {'fecha_inicio': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        })}
class SociosComercialesForm(forms.ModelForm):
    class Meta:
        model = SociosComerciales
        fields = '__all__'
        exclude = ['declaraciones', 'observaciones', 'socio_infopersonalvar']

class ClientesPrincipalesForm(forms.ModelForm):
    class Meta:
        model = ClientesPrincipales
        fields = '__all__'
        exclude = ['declaraciones', 'domicilios', 'observaciones',
                   'info_personal_var']

class OtrasPartesForm(forms.ModelForm):
    class Meta:
        model = OtrasPartes
        fields = '__all__'
        exclude = ['declaraciones', 'observaciones',
                   'declarante_infopersonalvar', 'otraspartes_infopersonalvar']
        widgets = {'fecha_inicio_relacion': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        })}
class BeneficiosGratuitosForm(forms.ModelForm):
    class Meta:
        model = BeneficiosGratuitos
        fields = '__all__'
        exclude = ['declaraciones', 'observaciones']
