from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from declaracion.models import CatTiposDeclaracion, InfoPersonalVar, InfoPersonalFija
from declaracion.models.catalogos import CatEntesPublicos, CatEstatusDeclaracion


class BusquedaDeclaranteForm(forms.Form):
    nombre = forms.CharField(max_length=128,label="Nombre", required=False )
    apellido1 = forms.CharField(max_length=128,label="Primer Apellido", required=False )
    apellido2 = forms.CharField(max_length=128,label="Segundo Apellido", required=False )
    rfc = forms.CharField(max_length=13,label="RFC", required=False,validators=[RegexValidator('^([A-Z,Ñ,&]{3,4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[A-Z|\d]{3})$', message="Introduzca un RFC válido")] )
    curp = forms.CharField(max_length=18,label="CURP", required=False )
    ente = forms.ModelChoiceField(queryset=CatEntesPublicos.objects.all(),required=False,label="Ente público")
    estatus = forms.ModelChoiceField(queryset=CatEstatusDeclaracion.objects.all(),required=False,label="Estatus")
    page = forms.CharField(widget=forms.HiddenInput(), required=False)
    page_size = forms.CharField(widget=forms.HiddenInput(), required=False,initial="10" )
class BusquedaUsuariosForm(forms.Form):
    TRUE_FALSE_CHOICES = (
        (None,'--------'),
        (True, 'Activo'),
        (False, 'Inactivo')
    )

    nombre = forms.CharField(max_length=128,label="Nombre", required=False )
    apellido1 = forms.CharField(max_length=128,label="Primer Apellido", required=False )
    apellido2 = forms.CharField(max_length=128,label="Segundo Apellido", required=False )
    ente = forms.ModelChoiceField(queryset=CatEntesPublicos.objects.all(),required=False)
    estatus = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Estatus",
                              initial='', widget=forms.Select(), required=False)
    page = forms.CharField(widget=forms.HiddenInput(), required=False)
    page_size = forms.CharField(widget=forms.HiddenInput(), required=False,initial="10")

class BusquedaDeclaracionForm(forms.Form):
    folio = forms.CharField(max_length=128,label="Folio", required=False )
    tipo = forms.ModelChoiceField(queryset=CatTiposDeclaracion.objects.all(),label="Tipo de declaración", required=False )
    ente = forms.ModelChoiceField(queryset=CatEntesPublicos.objects.all(),label="Ente público", required=False )
    ano = forms.IntegerField(label="Año", required=False )
    estatus = forms.ModelChoiceField(queryset=CatEstatusDeclaracion.objects.all(),label="Estatus", required=False )
    page = forms.CharField(widget=forms.HiddenInput(), required=False)
    page_size = forms.CharField(widget=forms.HiddenInput(), required=False,initial="10")


class RegistroUsuarioForm(forms.Form):
    roles = (
        (False, 'Operador'),
        (True, 'Administrador')
    )
    estatus = (
        (True, 'Activo'),
        (False, 'Inactivo')
    )

    nombres = forms.CharField(required = True,label="Nombre(s)")
    apellido1 = forms.CharField(required = True,label="Primer apellido")
    apellido2 = forms.CharField(required = False,label="Segundo apellido")
    dependencia = forms.ModelChoiceField(queryset=CatEntesPublicos.objects.all(),required = True,label="Ente público")
    telefono = forms.CharField(max_length=15,required = True,label="Teléfono",validators=[RegexValidator('^\+?1?\d{9,10}$', message="Introduzca un Teléfono válido")])
    rfc = forms.CharField(max_length=13, label="RFC con Homoclave", required=True,validators=[RegexValidator('^([A-Z,Ñ,&]{3,4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[A-Z|\d]{3})$', message="Introduzca un RFC válido")])
    puesto = forms.CharField(required = True,label="Empleo, cargo o comisión")
    email = forms.EmailField(required=True, label="Correo electrónico")
    rol =  forms.ChoiceField(choices=roles)
    estatus =  forms.ChoiceField(choices=estatus)
    id = forms.CharField(widget=forms.HiddenInput(),required=False)

    def clean(self):
        super().clean()

        try:
            id =int(self.cleaned_data.get("id"))
        except:
            id=None


        email = self.cleaned_data.get("email")
        email = str(email).lower()
        if id is None:
            if User.objects.filter(email = email).count()>0:
                self.add_error("email","Correo ya registrado")
        else:
            if User.objects.filter(email = email).exclude(pk=id).count()>0:
                self.add_error("email","Correo ya registrado")


        rfc = self.cleaned_data.get("rfc")
        rfc = str(rfc).upper()
        if id is None:
            if User.objects.filter(username = rfc).count()>0:
                self.add_error("rfc","RFC ya registrado")
        else:
            if User.objects.filter(username = rfc,pk=id).exclude(pk=id).count()>0:
                self.add_error("rfc","RFC ya registrado")


