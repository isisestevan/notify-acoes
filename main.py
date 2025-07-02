from flask import Flask, jsonify
import yfinance as yf
import os
import requests
from dotenv import load_dotenv

load_dotenv()

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
    if response.status_code == 200:
        print(f"Mensagem enviada: {mensagem}")
    else:
        print(f"Erro ao enviar mensagem: {response.text}")

@app.route('/verificar')
def verificar():
    mensagens = []
    with open('acoes.txt', 'r') as arquivo:
        linhas = arquivo.readlines()

    acoes = [linha.strip() for linha in linhas]

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
            mensagens.append(mensagem)

    if mensagens:
        return jsonify({"alertas": mensagens})
    else:
        return jsonify({"alertas": ["Nenhuma queda significativa detectada."]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
