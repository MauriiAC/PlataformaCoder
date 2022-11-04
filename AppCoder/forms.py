from django import forms
from .models import Curso
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User



# class CursoFormulario(forms.Form):

#     curso = forms.CharField()
#     camada = forms.IntegerField()

class CursoFormulario(forms.ModelForm):

    class Meta:
        model=Curso
        fields=('__all__')
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'placeholder': "Ingrese nombre...",
                    'class': 'input-curso-name'
                }
            )
        }


class ProfesorFormulario(forms.Form):

    nombre = forms.CharField(max_length=30)
    apellido = forms.CharField(max_length=30)
    email = forms.EmailField()
    profesion = forms.CharField(max_length=30)


class UserEditForm(UserChangeForm):

    password = forms.CharField(
        help_text="",
        widget=forms.HiddenInput(), required=False
    )

    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir Contraseña", widget=forms.PasswordInput)

    class Meta:

        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']


    def clean_password2(self):

        print('self\n',self.cleaned_data)

        password2 = self.cleaned_data["password2"]
        if password2 != self.cleaned_data["password1"]:
            raise forms.ValidationError("Las contraseñas no coinciden!")
        return password2

