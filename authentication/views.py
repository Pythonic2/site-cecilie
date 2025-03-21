from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, EventoForm
from django.contrib.auth import logout
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from .models import Usuario, Evento
from django.utils.translation import gettext_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import requests
from carrinho.models import Carrinho,ItemCarrinho
from produto.models import Cidade
from datetime import date
from datetime import datetime, date



User = Usuario

# Create your views here.
def logout_view(request):
    logout(request)
    return redirect("index")


class RegisterUser(CreateView):

    def get(self, request):
        form = SignUpForm()
        return render(request, "register.html", {"form": form, 'title': 'Registrar'})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            # cep = form.cleaned_data.get("cep")
            # url = f"https://viacep.com.br/ws/{cep}/json/"
            # response = requests.get(url)
            # if response.status_code == 200:
            #     data = response.json()
            #     cidades_rm_fortaleza = [cidade.nome for cidade in Cidade.objects.all() ]
                        
            #     if data['localidade'] in cidades_rm_fortaleza:
            #         pass
            #     else:
            #         form.add_error('cep','⚠️ Ainda não atendemos a sua Região, Penas Fortaleza e a Metrópoles')
            #         return render(request, "register.html", {"form": form})
            if get_user_model().objects.filter(username=username).exists():
                form.add_error('username', 'Este nome de usuário já está em uso.')
                return render(request, "register.html", {"form": form})
            
            form.save()
            
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)  # Faz o login automático
                return redirect("produtos")
            else:
                return redirect("register")
        else:
            return render(request, "register.html", {"form": form, "erro": form.errors})


class LoginUsuario(LoginView):
    template_name = 'login.html'
    form_class = LoginForm  # Use o formulário de login personalizado

    def get(self, request):
    
        return render(request, "login.html", {"form": self.form_class,'title':'Login'})
    
    def form_invalid(self, form):
        # Obtem o nome de usuário digitado no formulário
        username = form.cleaned_data.get('username')
        user_exists = User.objects.filter(username=username).exists()

        # Define mensagens de erro personalizadas
        error_messages = {
            'invalid_login': gettext_lazy('Verifique o usuário e senha e tente novamente.'),
            'inactive': gettext_lazy('Usuário inativo.'),
        }
        
        # Atualiza as mensagens de erro no AuthenticationForm
        form.error_messages.update(error_messages)
        
        # Chama o método pai para lidar com a renderização de um formulário inválido
        response = super().form_invalid(form)
        
        # Adiciona o erro ao contexto com base na existência do usuário
        if not user_exists:
            response.context_data['error'] = error_messages['invalid_login']
        else:
            response.context_data['error'] = error_messages['inactive']
        
        return response


class EventoView(TemplateView):
    template_name = 'evento.html'
    form_class = EventoForm

    def get(self, request):
        try:
            usuario = request.user.username
            user = Usuario.objects.get(username=usuario)
            evento = Evento.objects.filter(usuario=user).filter(status='Aguardando Pagamento').last()
            evento.delete()
        except:
            pass
        context = {'form':self.form_class}
        return render(request, self.template_name, context)


    def post(self, request):
        form = EventoForm(request.POST)

        if form.is_valid():
            data_evento_str = form.cleaned_data.get("data_evento")  # Exemplo: "2025-03-20"
            data_evento = data_evento_str
            data_hoje = date.today()

            # Verificação de limite de eventos pagos
            eventos_no_dia = Evento.objects.filter(data_evento=data_evento, status='Pago')

            eventos_com_bomba = eventos_no_dia.filter(chopeiras__tipo='bomba').count()
            eventos_com_eletrica = eventos_no_dia.filter(chopeiras__tipo='eletrica').count()

            # Pegando as chopeiras que o usuário escolheu no formulário
            chopeiras_selecionadas = form.cleaned_data.get("chopeiras")
            tem_bomba = any(chopeira.tipo == 'bomba' for chopeira in chopeiras_selecionadas)
            tem_eletrica = any(chopeira.tipo == 'eletrica' for chopeira in chopeiras_selecionadas)

            # Regras de validação
            if tem_bomba and eventos_com_bomba >= 2:
                form.add_error('chopeiras', "⚠️ Infelizmente não tempos mais Chopeira Bomba disponível para essa data.")
                return render(request, "evento.html", {"form": form, "erro": form.errors})

            if tem_eletrica and eventos_com_eletrica >= 10:
                form.add_error('chopeiras', "⚠️ Infelizmente não tempos mais Chopeira Elétrica disponível para essa data.")
                return render(request, "evento.html", {"form": form, "erro": form.errors})

            # Segue o fluxo normal caso passe na verificação
            diferenca_dias = (data_evento - data_hoje).days
            if diferenca_dias < 10:
                carrinho = Carrinho.objects.filter(usuario=request.user).exclude(status='pago').last()
                itens = ItemCarrinho.objects.filter(carrinho=carrinho)
                chopeiras_formatadas = ", ".join(['Chopeira Bomba' if chopeira.tipo == 'bomba' else 'Chopeira Elétrica' for chopeira in chopeiras_selecionadas])
                
                produtos = [item.produto.nome for item in itens]
                produtos_formatados = ", ".join(produtos)

                mensagem = f"Olá, faltam apenas {diferenca_dias} dias para o evento! Pode me ajudar? Produtos que escolhi: {produtos_formatados}, Chopeiras: {chopeiras_formatadas}."
                link_whatsapp = f"https://wa.me/83998413751?text={mensagem.replace(' ', '%20')}"
                return redirect(link_whatsapp)
            cep = form.cleaned_data.get("cep")
            print(f"**************** CEP {cep} *********************")
            url = f"https://viacep.com.br/ws/{cep}/json/"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                cidades_rm_fortaleza = [cidade.nome for cidade in Cidade.objects.all()]

                if data['localidade'] in cidades_rm_fortaleza:
                    #passa a cidade se tiver no banco como session, para consultar se essa cidade tem frete, se tiver adiciona como item no pagamento
                    request.session['cidade_selecionada'] = data['localidade']
                    evento = form.save(commit=False)
                    evento.usuario = request.user
                    evento.status = 'Aguardando Pagamento'
                    evento.cep = cep
                    evento.save()  # Agora o evento é salvo no banco de dados

                    # Agora podemos associar as chopeiras ao evento
                    evento.chopeiras.set(chopeiras_selecionadas)

                    # Agora podemos redirecionar
                    return redirect('pagina_carrinho')  # Substitua por uma URL válida
                else:
                    form.add_error('cep', '⚠️ Ainda não atendemos a sua Região, apenas Fortaleza e a Metrópole')
                    return render(request, "evento.html", {"form": form, "erro": form.errors})
            
        return render(request, "evento.html", {"form": form, "erro": form.errors})



class PedidosView(TemplateView):
    template_name = 'sucesso.html'
    
    
    def get(self, request):
        usuario = request.user.username
        user = Usuario.objects.get(username=usuario)
        eventos = Evento.objects.filter(usuario=user).order_by('-id')
        print(f'-------------{usuario}---------')
        print(f'-------------{len(eventos)}---------')
        context = {'pagamentos':eventos}
        return render(request, self.template_name, context)


def recovery_password(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        try:
            # Corrige o erro de digitação e remove o uso incorreto de exists()
            user = Usuario.objects.get(username=cpf)
            if user:
                password = request.POST.get('password')
                user.set_password(password)
                user.save()
                return render(request, 'recovery_password.html', {'display_erro':'none','display_sucesso':'block','success': 'Senha alterada com sucesso'})
        except Usuario.DoesNotExist:
            return render(request, 'recovery_password.html', {'display_erro':'block','error': 'Usuario não existe','display_sucesso':'none'})
    return render(request, 'recovery_password.html',{'display_sucesso':'none','display_erro':'none'})