



# Não está sendo utilizado no momento

import requests

dados_transacao = {
    "numero_cartao": "4111111111111111",
    "valor": 100.00,
    "parcelas": 2
}

resposta = requests.post("http://localhost:5000/processar_pagamento", json=dados_transacao)
print(resposta.json())
