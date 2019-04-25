from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms import PasswordInput, DateInput
from django.core import exceptions

from declaracion.models import InfoPersonalVar
from declaracion.models.catalogos import CatPaises, CatEntidadesFederativas, CatEntesPublicos
from bootstrap_datepicker_plus import DatePickerInput
import django.contrib.auth.password_validation as validators


class RegistroForm(forms.Form):

    nombres = forms.CharField(required = True,label="Nombre(s)")
    apellido1 = forms.CharField(required = True,label="Primer apellido")
    apellido2 = forms.CharField(required = False,label="Segundo apellido")
    dependencia = forms.ModelChoiceField(queryset=CatEntesPublicos.objects.all(),required = True,label="Ente público")
    telefono = forms.CharField(max_length=15,required = True,label="Teléfono",validators=[RegexValidator('^\+?1?\d{9,10}$', message="Introduzca un Teléfono válido")])
    puesto = forms.CharField(required = True,label="Empleo, cargo o comisión")
    rfc = forms.CharField(max_length=13, label="RFC con Homoclave", required=True,validators=[RegexValidator('^([A-Z,Ñ,&]{3,4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[A-Z|\d]{3})$', message="Introduzca un RFC válido")])
    curp = forms.CharField(max_length=20, label="CURP (si aplica)", required=False,validators=[RegexValidator('^[A-Z]{1}[AEIOU]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]{1}[0-9]{1}$', message="Introduzca un CURP válido")])
    fecha = forms.DateField(required=True, widget=DatePickerInput(options={
        "format":'YYYY-MM-DD',
        "locale":"es",
        "ignoreReadonly":True,
        "maxDate": 'now'
    }), label="Fecha de ingreso")
    email = forms.EmailField(required=True, label="Correo electrónico")
    contrasena1 = forms.CharField(widget=PasswordInput,required=True, label="Contraseña")
    contrasena2 = forms.CharField(widget=PasswordInput,required=True, label="Confirmar contraseña")

    pais = forms.ModelChoiceField(queryset=CatPaises.objects.all(),required=False,label="País de origen")
    entidad = forms.ModelChoiceField(queryset=CatEntidadesFederativas.objects.all(),required=False,label="Entidad Federativa")

    def clean(self):
        super().clean()
        email = self.cleaned_data.get("email")
        email = str(email).lower()
        if User.objects.filter(email = email).count()>0:
            self.add_error("email","Correo ya registrado")

        rfc = self.cleaned_data.get("rfc")
        rfc = str(rfc).upper()
        if User.objects.filter(username = rfc).count()>0:
            self.add_error("rfc","RFC ya registrado")

        c1 = self.cleaned_data.get('contrasena1')
        c2 = self.cleaned_data.get('contrasena2')



        if c1 != c2:
            self.add_error('contrasena1','Contraseñas no coinciden')
        if c1 is  None or  c1=="":
            self.add_error('contrasena1', 'Debes escribir una contraseña')
        else:
            try:
                 print(self.cleaned_data.get('contrasena1'))
                 validators.validate_password(password=self.cleaned_data.get('contrasena1'), user=User)
            except exceptions.ValidationError as e:

                 self.errors['contrasena1'] = list(e.messages)

class CambioEntePublicoForm(forms.Form):
    dependencia = forms.ModelChoiceField(queryset=CatEntesPublicos.objects.all(), required=True, label="Ente público")