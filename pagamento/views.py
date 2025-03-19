from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
from .models import Transacao, Usuario, Produto
from carrinho.models import Carrinho
from authentication.models import Evento
import mercadopago
import pandas as pd
from .busca_pagameto import buscar_pagamento_mercado_pago
from notifications import send_email
from dotenv import load_dotenv
import os
from datetime import datetime
import logging
from main.criar_evento import criar_evento
load_dotenv()
# Configurando o logger no início do arquivo
logging.basicConfig(
    level=logging.DEBUG,  # Nível de log
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato da mensagem de log
    handlers=[logging.FileHandler('transacoes.log', mode='a'),  # Salvar no arquivo transacoes.log
              logging.StreamHandler()]  # Exibir no console também
)


@csrf_exempt
def simple_test(request):
    logging.debug("Recebendo requisição POST")

    if request.method == "POST":
        if not request.body:
            logging.warning("Corpo da requisição vazio")
            return JsonResponse({'error': 'Corpo da requisição vazio'}, status=400)

        try:
            # Decodificar o corpo da requisição em JSON
            webhook_data = json.loads(request.body.decode('utf-8'))
            logging.debug(f"Dados recebidos no webhook: {webhook_data}")

            # Capturar o pagamento_id e outras informações do webhook
            pagamento_id = str(webhook_data.get('data', {}).get('id', ''))
            tipo = webhook_data.get('type', {})
            logging.debug(f"Pagamento ID: {pagamento_id}, Tipo: {tipo}")


            logging.info("Dados do webhook salvos em recibo.csv")

            # Buscar pagamento usando a função definida anteriormente
            pag = buscar_pagamento_mercado_pago(pagamento_id)
            print("################## IFOR PAG ##################")
            print(pag)
            print("####################################")
            logging.debug(f"Informações do pagamento: {pag}")
            logging.debug(f"Informações do tipo do Pagamento: {tipo}, tam {len(tipo)}")
            pd_id = tipo
            status = pag['status']
            try:
                print(f'-----------------{pd_id}-----------------')
                if status == 'approved' and tipo == 'payment':
                    logging.debug("Pagamento aprovado, processando transação...")
                    user = Usuario.objects.get(id=pag['usuario'])
                    transacao = Transacao(
                    transacao_id=pag['id'],
                    usuario=user,
                    data_transacao=pag['data'],
                    valor_total=pag['valor'],
                    status=pag['status']
                )
                    transacao.save()  # Salvar a transação
                    logging.info(f"Transação salva: {transacao.transacao_id}")

                    produtos = pag['items']
                    for produto_data in produtos:
                        produto = Produto.objects.get(nome=produto_data)
                        transacao.produtos.add(produto.id)
                    logging.debug(f"Produtos associados à transação: {produtos}")
                    logging.debug(f"id evento: {pag['evento']}")
                    #carrinho = Carrinho.objects.get(usuario=user, id=int(pag['evento']))
                    #print(f"----cart: {carrinho}")
                    id_evento = pag['evento']
                    criar_evento(evento_id=id_evento, produtos=produtos)
                    evento = Evento.objects.get(usuario=user, id=id_evento)
                    print(f'---------{evento}------------EVENTO')
                    logging.debug(f"consulta evento: {evento}")


                    print(f'status ----------------------{status}')

                    #carrinho.status = 'Pago'
                    evento.status = 'Pago'
                    evento.save()
                    carrinho = Carrinho.objects.get(usuario=user, id=int(pag['carrinho_id']))
                    #carrinho.save()
                    carrinho.delete()
                    logging.info(f"Carrinho e evento atualizados para 'Pago': {carrinho.id}, {evento.id}")

                    send_email(
                        subject=f"Nova Compra Realizada",
                        body=f"Evento: {evento.tipo_evento}\nData: {evento.data_evento}\nBairro: {evento.bairro}\nRua: {evento.endereco}\nValor da Compra: {evento.valor}\nCliente: {user.nome}\nContato: {evento.celular}\nProdutos: {produtos}",
                        sender_email="noticacoes@gmail.com",
                        sender_password=os.getenv('SENHA'),
                        recipient_emails=["choppitinerante@gmail.com", "igormarinhosilva@gmail.com"]
                    )
                    logging.info(f"E-mail enviado para notificações")
                    return JsonResponse({'status': 'success'})
                else:
                    print(status)
                    logging.warning("Tipo de pagamento diferente de 'payment' ou ID não encontrado.")
                    return JsonResponse({'status': 'Order Generate'})
            except Exception as e:
                logging.warning(f"Erro ao processar transação: {str(e)}")
                return JsonResponse({'status': 'Order Generate'})

        except json.JSONDecodeError:
            logging.error("Falha ao decodificar JSON")
            return JsonResponse({'error': 'Falha ao decodificar JSON'}, status=400)
        except Usuario.DoesNotExist:
            logging.error("Usuário não encontrado")
            return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
        except Produto.DoesNotExist:
            logging.error("Produto não encontrado")
            return JsonResponse({'error': 'Produto não encontrado'}, status=404)

    logging.warning("Método HTTP não permitido")
    return JsonResponse({'status': 'method_not_allowed'}, status=405)
import mercadopago
import os
import logging

def gerar_pagamento(cliente_id: int, produtos: list, evento: int, carrinho_id: int):
    # Inicializar o SDK do Mercado Pago
    sdk = mercadopago.SDK("TEST-3488797328851277-091614-dbbff0af2658e101ee7f9413497c16fd-162016798")

    # Construir a lista de itens dinamicamente
    items = []
    for produto, quantidade, valor in produtos:
        item = {
            "id": produto.id,
            "title": produto.nome,
            "quantity": quantidade,
            "currency_id": "BRL",
            "unit_price": float(valor)
        }
        items.append(item)
    print(f"items -------------{items}")
    # Configurar os dados da preferência
    preference_data = {
        "items": items,
        "back_urls": {
            "success": "https://plataforma-donadochopp.cloudboosterlab.org/minhas-compras/",
            "failure": "https://plataforma-donadochopp.cloudboosterlab.org/minhas-compras/",
            "pending": "https://plataforma-donadochopp.cloudboosterlab.org/minhas-compras/",
        },
        "external_reference": f'{cliente_id}',
        "auto_return": "approved",
        "notification_url": "https://plataforma-donadochopp.cloudboosterlab.org/pag/",
        "metadata": {
            "evento_id": evento,
            "carrinho_id": carrinho_id
        }
    }

    try:
        result = sdk.preference().create(preference_data)
        logging.debug(f"{os.getenv('API_TOKEN')}")
        logging.debug(f"Resposta da criação da preferência: {result}")
        preference = result['response']
        logging.info("Preferência criada com sucesso.")
        return preference['init_point'], carrinho_id
    except Exception as e:
        logging.error(f"Erro ao criar a preferência: {str(e)}")
        return None, None