from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def valida_numero_cartao(numero_cartao):
    soma = 0
    alternar = False
    for digito in reversed(numero_cartao):
        n = int(digito)
        if alternar:
            n *= 2
            if n > 9:
                n -= 9
        soma += n
        alternar = not alternar
    return soma % 10 == 0

@app.route('/validar_cartao', methods=['POST'])
def validar_cartao():
    dados = request.json #pega os dados de banco.py
    if not valida_numero_cartao(dados["numero"]):
        return jsonify({"status": "recusado", "motivo": "Cartão inválido"}), 400
    
    resposta = requests.post("http://localhost:5002/verifica_credito", json=dados)
    return resposta.json()
app.run(port=5001)
