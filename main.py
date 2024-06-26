import threading
import signal
import os
import random
from time import sleep
from bots.telegram_bot import send_offer_telegram
from bots.twitter_bot import setup_twitter_api, post_to_twitter
import sys
from pathlib import Path
from offer_scraper import scrape_amazon_offers, escape_markdown_v2
from termcolor import colored
from tqdm import tqdm

sys.path.append(str(Path(__file__).parent))

# Variabili globali
chat_id = os.environ['CHAT_ID']
api = setup_twitter_api()
telegram_bot_running = False
telegram_thread = None
ascii_art = r"""
 /$$      /$$  /$$$$$$  /$$$$$$ /$$   /$$  
| $$$    /$$$ /$$__  $$|_  $$_/| $$$ | $$  
| $$$$  /$$$$| $$  \ $$  | $$  | $$$$| $$  
| $$ $$/$$ $$| $$$$$$$$  | $$  | $$ $$ $$  
| $$  $$$| $$| $$__  $$  | $$  | $$  $$$$  
| $$\  $ | $$| $$  | $$  | $$  | $$\  $$$  
| $$ \/  | $$| $$  | $$ /$$$$$$| $$ \  $$  
|__/     |__/|__/  |__/|______/|__/  \__/  
                                           
                                           
                                           
 /$$      /$$ /$$$$$$$$ /$$   /$$ /$$   /$$
| $$$    /$$$| $$_____/| $$$ | $$| $$  | $$
| $$$$  /$$$$| $$      | $$$$| $$| $$  | $$
| $$ $$/$$ $$| $$$$$   | $$ $$ $$| $$  | $$
| $$  $$$| $$| $$__/   | $$  $$$$| $$  | $$
| $$\  $ | $$| $$      | $$\  $$$| $$  | $$
| $$ \/  | $$| $$$$$$$$| $$ \  $$|  $$$$$$/
|__/     |__/|________/|__/  \__/ \______/ 
"""


def cleanup_and_exit():
  print(colored("Pulizia delle risorse e uscita in corso...", "yellow"))
  if telegram_bot_running:
    stop_telegram_bot()
  print(colored("Chiusura del programma completata.", "yellow"))
  sys.exit(0)  # Uscita pulita dal programma


def signal_handler(sig, frame):
  print(colored('Interrotto!', "red"))
  cleanup_and_exit()


def start_telegram_bot():
  global telegram_bot_running, telegram_thread
  if not telegram_bot_running:
    telegram_bot_running = True
    telegram_thread = threading.Thread(target=start_telegram_bot)
    telegram_thread.start()
    print(colored("Il bot Telegram è stato avviato.", "cyan"))
  else:
    print(colored("Il bot Telegram è già in esecuzione.", "cyan"))


def stop_telegram_bot():
  global telegram_bot_running, telegram_thread
  if telegram_bot_running and telegram_thread is not None:
    print("Fermare il bot di Telegram...")
    # Qui inserisci il codice per fermare effettivamente il bot
    # Ad esempio, potresti avere una variabile di controllo che il thread del bot verifica per decidere se terminare
    telegram_bot_running = False
    telegram_thread.join()  # Attendi che il thread del bot termini
    telegram_thread = None  # Resetta la variabile del thread a None
    print(colored("Il bot Telegram è stato fermato.", "green"))
  else:
    print(
        colored(
            "Il bot Telegram non è attualmente in esecuzione o il thread non è stato avviato correttamente.",
            "red"))


def get_page_url():
  choice = input(
      colored(
          "Vuoi scaricare la prima pagina o una pagina casuale?\n [prima/casuale]:\n ",
          "light_magenta")).lower()
  base_url = 'https://www.amazon.it/s?i=computers&rh=n%3A425916031&fs=true&ref=sr_pg_1'
  if choice == 'casuale':
    page_number = random.randint(
        1, 40)  # Modifica con il numero massimo di pagine se necessario
    return f"{base_url}&page={page_number}"
  else:
    return base_url + "&page=1"


def twitter_action():
  # Esegue lo scraping delle offerte
  offers = scrape_amazon_offers(
      'https://www.amazon.it/s?i=computers&rh=n%3A425916031&fs=true&ref=sr_pg_1',
      chat_id
  )  # Aggiusta con il tuo URL reale e la logica di paginazione se necessario
  # Seleziona un'offerta casuale dalla lista e posta su Twitter
  if offers:
    random_offer = random.choice(offers)
    post_to_twitter(api, random_offer)
  else:
    print(colored("Nessuna offerta trovata.", "red"))


def telegram_action():
  # Avvia il bot di Telegram solo se non è già in esecuzione
  if not telegram_bot_running:
    start_telegram_bot()
  else:
    print(
        colored("Il bot Telegram è già in esecuzione. Invio delle offerte...",
                "cyan"))

  # Ottiene l'URL per lo scraping in base alla scelta dell'utente
  url = get_page_url()
  # Esegue lo scraping delle offerte
  offers = scrape_amazon_offers(
      url, chat_id
  )  # Aggiusta con il tuo URL e la logica di paginazione se necessario

  if offers:
    print(colored(f"Invio di {len(offers)} offerte su Telegram...", "green"))

    # Invia le offerte su Telegram tramite una funzione esterna che gestisce il batch di invio e la logica di retry
    send_offer_telegram(chat_id, offers)

    # Dopo il completamento dell'invio, chiudi la barra di tqdm

    print(colored("Invio offerte completato.", "green"))
  else:
    print(colored("Nessuna offerta trovata.", "red"))


def main():
  while True:
    comando = input(
        f"Inserisci un comando: \n {colored('twitter', 'cyan')} / {colored('telegram', 'blue')} / {colored('both', 'light_yellow')} / {colored('exit', 'red')} :\n\n "
    ).lower()
    if comando == "twitter":
      twitter_action()
    elif comando == "telegram":
      if not telegram_bot_running:
        start_telegram_bot()
      else:
        print("Il bot Telegram è già in esecuzione. Invio delle offerte...")
      telegram_action()
    elif comando == "both":
      if not telegram_bot_running:
        start_telegram_bot()
      twitter_action()
      telegram_action()
    elif comando == "exit":
      if telegram_bot_running:
        stop_telegram_bot()
      print("Chiusura del programma...")
      break
    else:
      print(colored("Comando non riconosciuto. Riprova.", "red"))


if __name__ == "__main__":
  signal.signal(signal.SIGINT, signal_handler)
  print(
      colored("\nMultichannel bot alpha 0.5 developed by TopoDiFogna\n",
              "magenta"))
  print(colored(ascii_art, 'green'))
  try:
    main()

  except KeyboardInterrupt:
    cleanup_and_exit()
