import os
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from datetime import datetime

# Get the current working directory
current_directory = os.getcwd()

# Construct the full path to the credentials file
arquivo_credenciais = os.path.join(current_directory, "main\dona-calendario.json")

def criar_evento(endereco, data, cep, nome_cliente):
    # Definição dos escopos necessários para acessar o Google Calendar
    escopos = ["https://www.googleapis.com/auth/calendar"]

    # Carregando as credenciais da conta de serviço
    credenciais = Credentials.from_service_account_file(arquivo_credenciais, scopes=escopos)

    # Construindo o serviço da API do Google Calendar
    service = build("calendar", "v3", credentials=credenciais)

    # Defina o ID do calendário (normalmente é o e-mail da conta associada)
    calendar_id = "igormarinhosilva@gmail.com"

    # Criando um evento de dia inteiro
    evento = {
        "summary": f"Agendamento com {nome_cliente}",
        "location": f"{cep} - {endereco}",
        "description": f"Agendamento com {nome_cliente} no endereço informado.",
        "start": {
            "date": data,  # Apenas a data, sem horário
            "timeZone": "America/Sao_Paulo",
        },
        "end": {
            "date": data,  # Apenas a data, sem horário
            "timeZone": "America/Sao_Paulo",
        },
    }

    # Inserindo o evento no calendário
    evento_criado = service.events().insert(calendarId=calendar_id, body=evento).execute()

    print(f"Evento criado com sucesso! Link: {evento_criado.get('htmlLink')}")

# Chamando a função com dados de teste
criar_evento(
    endereco="Rua Exemplo, 123, Bairro Centro",
    data="2025-03-19",  # Apenas a data, sem horário
    cep="12345-678",
    nome_cliente="João da Silva"
)
