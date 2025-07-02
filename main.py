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
    enviar_telegram("Teste direto do servidor - mensagem enviada via /verificar")
    return jsonify({"alerta": "Mensagem teste enviada"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
