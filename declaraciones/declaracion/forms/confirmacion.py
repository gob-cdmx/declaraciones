from django import forms
from django.core.validators import FileExtensionValidator


class ConfirmacionForm(forms.Form):
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    key = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['key'])])
    cer = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['cer'])])
