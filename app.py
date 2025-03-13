from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

BANCO_URL = "http://localhost:5002/verifica_credito"

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        numero_cartao = request.form["numero_cartao"]
        valor = float(request.form["valor"])

        dados = {"numero": numero_cartao, "valor": valor}

        resposta = requests.post(BANCO_URL, json=dados)

        resposta_json = resposta.json()
        if resposta.status_code == 200:
            if resposta_json.get("status") == "aprovado":
                resultado = "APROVADO, Código: " + resposta_json.get("codigo_autorizacao", "N/A")
            else:
                resultado = "RECUSADO, Motivo: " + resposta_json.get("motivo", "Motivo desconhecido")
        else:
            resultado = f"RECUSADO, Motivo: {resposta_json.get('motivo', 'Erro ao processar pagamento')}"


    return render_template("index.html", resultado=resultado)

BANCO_URL_CONSULTA = "http://localhost:5002/consulta_saldo"

@app.route("/consulta_saldo", methods=["GET", "POST"])
def consulta_saldo():
    resultado = None

    if request.method == "POST":
        numero_cartao = request.form["numero_cartao"]

        resposta = requests.post(BANCO_URL_CONSULTA, json={"numero": numero_cartao})

        if resposta.status_code == 200:
            dados = resposta.json()
            resultado = f"Cartão: {dados['numero']} | Saldo: R$ {dados['saldo']:.2f} | Limite: R$ {dados['limite']:.2f}"
        else:
            resultado = "Erro: " + resposta.json().get("motivo", "Erro ao consultar saldo")

    return render_template("consulta.html", resultado=resultado)

app.run(port=5003, debug=True)