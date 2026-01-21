from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


# =========================
# USUARIO CON EMAIL + VALIDACIONES
# =========================

class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Requerido, 254 caracteres como máximo"
    )

    first_name = forms.CharField(
        required=True,
        max_length=150,
        label="Nombre",
        help_text="Requerido, 150 caracteres como máximo"
    )

    last_name = forms.CharField(
        required=True,
        max_length=10,
        label="Código",
        help_text="Requerido, 10 caracteres como máximo"
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Nombre de usuario'
        })

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Nombre'
        })

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Código',
            'id': 'codigo'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Dirección email'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Contraseña'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Repetir contraseña'
        })

    # 🔒 Email único
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El email ya está registrado.")
        return email

    # 🔒 Código único (last_name)
    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if User.objects.filter(last_name=last_name).exists():
            raise forms.ValidationError("Este código ya está registrado.")
        return last_name


# =========================
# PERFIL
# =========================

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'link']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-control-file mt-3'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control mt-3',
                'rows': 3,
                'placeholder': 'Biografía'
            }),
            'link': forms.URLInput(attrs={
                'class': 'form-control mt-3',
                'placeholder': 'Enlace'
            }),
        }


# =========================
# EMAIL
# =========================

class EmailForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        help_text="Requerido, 254 caracteres máximo"
    )

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if 'email' in self.changed_data:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Email registrado")
        return email


# =========================
# USERNAME
# =========================

class UsernameForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        help_text="Requerido, 150 caracteres máximo"
    )

    class Meta:
        model = User
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if 'username' in self.changed_data:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Nombre de usuario ya está en uso")
        return username
