from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Evento
from .models import Evento, Chopeira
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label="CPF",
        widget=forms.TextInput(
            attrs={
                "placeholder": "CPF",
                "class": "form-control border-2 border-secondary w-75 w-md-100 py-3 px-4 rounded-pill mb-3",
                "label":"CPF"
            }
        )
    )
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nome",
                "class": "form-control border-2 border-secondary w-75 w-md-100 py-3 px-4 rounded-pill mb-3"
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control border-2 border-secondary w-75 w-md-100 py-3 px-4 rounded-pill mb-3"
            }
        )
    )
    data_nascimento = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "placeholder": "Data de Nascimento (YYYY-MM-DD)",
                "class": "form-control border-2 border-secondary w-75 w-md-100 py-3 px-4 rounded-pill mb-3",
                "type": "date"
            }
        ),
        required=True,
        label="Data de Nascimento"
    )
    
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Senha",
                "class": "form-control border-2 border-secondary w-75 w-md-100 py-3 px-4 rounded-pill mb-3"
            }
        )
    )
    password2 = forms.CharField(
        label="Confirme a Senha",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirme a Senha",
                "class": "form-control border-2 border-secondary w-75 w-md-100 py-3 px-4 rounded-pill mb-3"
            }
        ),
        help_text="Digite a mesma senha para confirmação."
    )

    class Meta:
        model = Usuario
        fields = ('nome', 'username', 'email', 'data_nascimento', 'password1', 'password2')


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
        widget=forms.TextInput(attrs={
            "placeholder": "Cep",
            "class": "form-control",
            "maxlength": "8",
        }),
        required=True
    )
    celular = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Celular",
            "class": "form-control",
            "maxlength": "11",
        }),
        required=True
    )
    bairro = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Bairro",
            "class": "form-control"
        }),
        required=False
    )
    endereco = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Endereço",
            "class": "form-control"
        }),
        required=True
    )
    data_evento = forms.DateField(
        widget=forms.DateInput(attrs={
            "placeholder": "Data do Evento",
            "class": "form-control",
            "type": "date"
        }),
        required=True
    )
    hora_evento = forms.TimeField(
        widget=forms.TimeInput(attrs={
            "placeholder": "Hora do Evento",
            "class": "form-control",
            "type": "time"
        }),
        required=True
    )
    tipo_evento = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Tipo de Evento",
            "class": "form-control"
        }),
        required=False
    )
    chopeiras = forms.ModelMultipleChoiceField(
        queryset=Chopeira.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True,
        label="Escolha pelo menos uma chopeira"
    )

    class Meta:
        model = Evento
        fields = ("cep", "celular", "bairro", "endereco", "data_evento", "hora_evento", "tipo_evento", "chopeiras")

    def clean_chopeiras(self):
        """Ensure at least one chopeira is selected."""
        chopeiras_selected = self.cleaned_data.get("chopeiras")
        if not chopeiras_selected:
            raise forms.ValidationError("You must select at least one chopeira.")
        return chopeiras_selected