from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Evento

class SignUpForm(UserCreationForm):
    cep = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "CEP",
                "class": "form-control border-2 border-secondary w-75 w-md-100 py-3 px-4 rounded-pill mb-3"
            }
        ))
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control border-2 border-secondary w-75 w-md-100 py-3 px-4 rounded-pill mb-3"
            }
        ))
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nome",
                "class": "form-control border-2 border-secondary w-75 w-md-100 py-3 px-4 rounded-pill mb-3"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control border-2 border-secondary w-75 w-md-100 py-3 px-4 rounded-pill mb-3"
            }
        ))
    
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Senha",
                "class": "form-control border-2 border-secondary w-75 w-md-100 py-3 px-4 rounded-pill mb-3"
            }
        ))
    password2 = forms.CharField(
        label="Confirme a Senha",
        widget=forms.PasswordInput(
            attrs={
                "label":"Senha",
                "placeholder": "Confirme a Senha",
                "class": "form-control border-2 border-secondary w-75 w-md-100 py-3 px-4 rounded-pill mb-3"
            }
        ),
        help_text="Digite a mesma senha para confirmação.",
        )
    
    class Meta:
        model = Usuario
        fields = ('cep','nome','username', 'email', 'password1', 'password2')



class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control border-2 border-secondary w-75 w-md-100 py-3 px-4 rounded-pill mb-3"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Senha",
                "class": "form-control border-2 border-secondary w-75 w-md-100 py-3 px-4 rounded-pill mb-3"
            }
        )
    )

    class Meta:
        fields = ['username', 'password']




class EventoForm(forms.ModelForm):
    cep = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Cep",
                "class": "form-control",
                "maxlength":"8",
                "required":"true"
            }
        ),
    )
    celular = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Celular",
                "class": "form-control",
                "maxlength":"11",
                "required":"true"
            }
        ),
    )
    bairro = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Bairro",
                "class": "form-control"
            }
        ),
        required=False
    )
    endereco = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Endereço",
                "class": "form-control"
            }
        ))
    data_evento = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "placeholder": "Data do Evento",
                "class": "form-control",
                "type": "date"
            }
        ),
        required=False
    )
    tipo_evento = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Tipo de Evento",
                "class": "form-control"
            }
        ),
        required=False
    )
    

    class Meta:
        model = Evento
        fields = ('celular', 'bairro', 'endereco', 'data_evento', 'tipo_evento')