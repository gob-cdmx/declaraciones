from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.core.validators import RegexValidator
from django.forms import  TextInput,Textarea
from declaracion.models import (Declaraciones, InfoPersonalFija, Domicilios,
                                InfoPersonalVar, Observaciones, DatosCurriculares,
                                Encargos, ExperienciaLaboral,
                                ConyugeDependientes)


class DeclaracionForm(forms.ModelForm):
    class Meta:
        model = Declaraciones
        fields = ['cat_tipos_declaracion']
        widgets = {'cat_tipos_declaracion': forms.HiddenInput()}


class InfoPersonalFijaForm(forms.ModelForm):
    class Meta:
        model = InfoPersonalFija
        fields = '__all__'
        widgets = {'fecha_nacimiento': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        }), 'fecha_inicio': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        }) }


class DomiciliosForm(forms.ModelForm):
    cp=forms.CharField(max_length=5,required=False)
    class Meta:
        model = Domicilios
        fields = '__all__'


class InfoPersonalVarForm(forms.ModelForm):
    rfc = forms.CharField(max_length=13, label="RFC con Homoclave", required=False, validators=[
        RegexValidator('^([A-Z,Ñ,&]{3,4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[A-Z|\d]{3})$',
                       message="Introduzca un RFC válido")])
    curp = forms.CharField(max_length=20, label="CURP (si aplica)", required=False, validators=[RegexValidator(
        '^[A-Z]{1}[AEIOU]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]{1}[0-9]{1}$',
        message="Introduzca un CURP válido")])
    tel_particular =  forms.CharField(max_length=15, required=False, label="Teléfono",
                               validators=[RegexValidator('^\d{4,}$', message="Introduzca un Teléfono válido")])
    tel_movil =  forms.CharField(max_length=15, required=False, label="Teléfono",
                               validators=[RegexValidator('^\d{4,}$', message="Introduzca un Teléfono válido")])
    email_personal = forms.EmailField(required=False)

    class Meta:
        model = InfoPersonalVar
        fields = '__all__'
        exclude = ['declaraciones', 'domicilios', 'observaciones',
                   'activos_bienes']
        widgets = {'fecha_nacimiento': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        })}


class ObservacionesForm(forms.ModelForm):
    class Meta:
        model = Observaciones
        fields = '__all__'

        widgets = {
            'observacion': Textarea(attrs={'rows': 4})
        }


class DatosCurricularesForm(forms.ModelForm):
    class Meta:
        model = DatosCurriculares
        fields = '__all__'
        exclude = ['declaraciones', 'observaciones']


class DatosEncargoActualForm(forms.ModelForm):
    telefono_laboral = forms.CharField(max_length=15, required=False, label="Teléfono",
                               validators=[RegexValidator('^\d{8,}$', message="Introduzca un Teléfono válido")])
    telefono_extension = forms.CharField(max_length=10, required=False, label="Teléfono",
                               validators=[RegexValidator('^\d{2,}$', message="Introduzca una Extensión válido")])
    email_laboral = forms.EmailField(required=False)

    class Meta:
        model = Encargos
        fields = '__all__'
        exclude = ['declaraciones', 'domicilios', 'observaciones']
        widgets = {'posesion_conclusion': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        }), 'posesion_inicio': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        })}


class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        fields = '__all__'
        exclude = ['declaraciones', 'domicilios', 'observaciones']
        widgets = {'fecha_ingreso': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        }), 'fecha_salida': DatePickerInput(options={
            "format": 'YYYY-MM-DD',
            "locale": "es",
            "ignoreReadonly": True,
            "maxDate": 'now'
        })}


class ConyugeDependientesForm(forms.ModelForm):
    class Meta:
        model = ConyugeDependientes
        fields = '__all__'
        exclude = ['declaraciones', 'domicilios', 'observaciones',
                   'declarante_infopersonalvar', 'dependiente_infopersonalvar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['cat_tipos_relaciones_personales'].queryset = (
            self.fields['cat_tipos_relaciones_personales'].queryset.filter(
                grupo_familia=1)
        )
