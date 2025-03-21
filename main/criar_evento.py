from authentication.models import Usuario, Evento
from carrinho.models import Carrinho, ItemCarrinho
import os
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta

# Get the current working directory
current_directory = os.getcwd()

# Construct the full path to the credentials file
arquivo_credenciais = os.path.join(current_directory, "/app/main/dona-calendario.json")

def criar_evento(evento_id, produtos):
    # Fetch the Evento instance from the database using the ID
    evento = Evento.objects.get(id=evento_id)

    # Fetch the Usuario (User) associated with the Evento
    usuario = evento.usuario

    # Define the scopes for Google Calendar API
    escopos = ["https://www.googleapis.com/auth/calendar"]

    # Load the service account credentials
    credenciais = Credentials.from_service_account_file(arquivo_credenciais, scopes=escopos)

    # Build the Google Calendar API service
    service = build("calendar", "v3", credentials=credenciais)

    # Format the product list
    produtos_formatados = "\n".join(
        [f"- {item.produto.nome}: {item.quantidade} unidade(s) - R$ {item.valor}" for item in produtos]
    )

    # Combine event date and time into a full datetime object
    start_datetime = datetime.combine(evento.data_evento, evento.hora_evento)
    end_datetime = start_datetime + timedelta(hours=4)  # Event ends 4 hours later

    # Create the event data
    evento_data = {
        "summary": f"Evento {evento.tipo_evento}  {usuario.nome} - email {usuario.email}",
        "location": f"{evento.bairro}, {evento.endereco}, {evento.cep}",
        "description": (
            f"Evento de: {usuario.nome}\n"
            f"Data de Nascimento: {usuario.data_nascimento}\n"
            f"CPF: {usuario.username}\n"
            f"Endereço do Evento: {evento.endereco}, {evento.bairro}\n"
            f"Tipo de Evento: {evento.tipo_evento}\n"
            f"Produtos:\n{produtos_formatados}\n"
            f"Valor Total: R$ {evento.valor}"
        ),
        "start": {
            "dateTime": start_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
            "timeZone": "America/Sao_Paulo",
        },
        "end": {
            "dateTime": end_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
            "timeZone": "America/Sao_Paulo",
        },
    }

    # Insert the event into Google Calendar
    evento_criado = service.events().insert(calendarId='igormarinhosilva@gmail.com', body=evento_data).execute()

    # Print confirmation and the link to the created event
    print(f"Event created successfully! Link: {evento_criado.get('htmlLink')}")
