from twilio.rest import Client

# Inizializza il client Twilio con le tue credenziali
account_sid = 'YOUR_ACCOUNT_SID'
auth_token = 'YOUR_AUTH_TOKEN'
client = Client(account_sid, auth_token)

def send_whatsapp_message(to, message):
    message = client.messages.create(
        body=message,
        from_='whatsapp:+14155238886',  # Numero Twilio per WhatsApp
        to=f'whatsapp:{to}'
    )
    print(f'Message sent to {to}: {message.sid}')
