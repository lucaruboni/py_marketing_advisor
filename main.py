from bots.telegram_bot import start_bot
print("Multichannel bot alpha 0.1 developed by TopoDiFogna")
print("Bot is starting...")
if __name__ == '__main__':
    try:
        print("Starting polling...")
        start_bot()
    except Exception as e:
        print(f"Errore nell'avvio del bot: {e}")
