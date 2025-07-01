from flask import Flask, jsonify
import yfinance as yf
from dotenv import load_dotenv
import os
import requests

load_dotenv(override=True)

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_telegram(mensagem: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        # Você pode logar o erro aqui, se quiser
        pass

@app.route('/verificar')
def verificar_acoes():
    with open('acoes.txt', 'r') as arquivo:
        linhas = arquivo.readlines()

    acoes = [linha.strip() for linha in linhas]

    alertas = []
    for acao in acoes:
        codigo = acao.replace('$', '').strip()
        if not codigo.endswith('.SA'):
            codigo += '.SA'

        ticker = yf.Ticker(codigo)
        dados = ticker.history(period="6mo")

        if dados.empty:
            continue

        preco_atual = dados['Close'].iloc[-1]
        media_90d = dados['Close'].tail(90).mean()

        if preco_atual < media_90d * 0.95:
            mensagem = f"⚠️ Alerta: {codigo} caiu para R${preco_atual:.2f}, abaixo da média de 90 dias (R${media_90d:.2f})"
            enviar_telegram(mensagem)
            alertas.append(mensagem)

    return jsonify({"alertas_enviados": alertas})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
