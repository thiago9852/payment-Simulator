from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

cartoes = {
    "4111111111111111": {"limite": 1000.00, "saldo": 500.00},
    "5500000000000004": {"limite": 2000.00, "saldo": 1500.00}
}

@app.route('/verifica_credito', methods=['POST'])
def verifica_credito():
    dados = request.json  # Recebe os dados enviados por redeCredenciadora.py
    numero_cartao = dados["numero"]
    valor = dados["valor"]
    
    # Verifica se o cartão existe
    if numero_cartao not in cartoes:
        return jsonify({"status": "recusado", "motivo": "Cartão não encontrado"}), 400
    
    # Verifica se o cartão tem limite
    if cartoes[numero_cartao]["saldo"] < valor:
        return jsonify({"status": "recusado", "motivo": "Saldo insuficiente"}), 400

    # Efectua o pagamento
    cartoes[numero_cartao]["saldo"] -= valor  # Atualiza o saldo
    return jsonify({"status": "aprovado", "codigo_autorizacao": "123456"}), 200

@app.route('/consulta_saldo', methods=['POST'])
def consulta_saldo():
    dados = request.json  # Recebe os dados enviados
    numero_cartao = dados["numero"]
    
    if numero_cartao not in cartoes:
        return jsonify({"status": "erro", "motivo": "Cartão não encontrado"}), 400

    return jsonify({
        "status": "sucesso",
        "numero": numero_cartao,
        "saldo": cartoes[numero_cartao]["saldo"],
        "limite": cartoes[numero_cartao]["limite"]
    }), 200


app.run(port=5002)