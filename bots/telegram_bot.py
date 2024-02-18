import requests


chat_id = "CHAT_ID_DESTINATARIO"
message = "Ciao! Questo è un messaggio dal mio bot Telegram."
bot_token = "IL_TUO_BOT_TOKEN"

def send_telegram_message(chat_id, message, bot_token):
    """
    Invia un messaggio a un chat_id specifico tramite il bot Telegram.

    Parametri:
    - chat_id (str): ID della chat a cui inviare il messaggio.
    - message (str): Testo del messaggio da inviare.
    - bot_token (str): Il token del tuo bot Telegram.
    """
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=data)
    print(f"Message sent to {chat_id}: {response.text}")
