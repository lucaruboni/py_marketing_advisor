import tweepy
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from monetization.linkvertise_bot import create_linkvertise_link
import random
import time
import telebot  # Import pyTelegramBotAPI as telebot
import os

# Twitter API credentials
my_secret_consumer_key = os.environ['consumer_key']
my_secret_consumer_secret = os.environ['consumer_secret']
my_secret_access_token = os.environ['access_token']
my_secret_access_token_secret = os.environ['access_token_secret']

# Setup Twitter API
auth = tweepy.OAuthHandler(my_secret_consumer_key, my_secret_consumer_secret)
auth.set_access_token(my_secret_access_token, my_secret_access_token_secret)
api = tweepy.API(auth)

my_secret_BOT_TOKEN = os.environ['BOT_TOKEN']
my_secret_CHAT_ID = os.environ['CHAT_ID']
bot = telebot.TeleBot(my_secret_BOT_TOKEN)


def escape_markdown_v2(text):
  escape_chars = '_*[]()~`>#+-=|{}.!\\'
  return ''.join(
      ['\\' + char if char in escape_chars else char for char in text])


def random_sleep(minimum=1, maximum=3):
  time.sleep(random.uniform(minimum, maximum))


def get_headers():
  user_agents = [
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
      "Mozilla/5.0 (iPad; CPU OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
      "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
      "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
      "Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
      "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
      "Mozilla/5.0 (Windows NT 10.0; rv:88.0) Gecko/20100101 Firefox/88.0",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0",
      "Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18",
      "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.177",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.177",
  ]
  return {"User-Agent": random.choice(user_agents)}


def post_to_twitter(offer_title, offer_link, offer_image_url=None):
  try:
    status = f"🔥 Offerta Imperdibile: {offer_title}! Scopri di più qui: {offer_link}"
    if offer_image_url:
      # Se c'è un'immagine, scaricala e poi tweetta con l'immagine
      response = requests.get(offer_image_url, stream=True)
      filename = 'temp.jpg'
      with open(filename, 'wb') as image:
        for chunk in response.iter_content(1024):
          image.write(chunk)

      # Carica l'immagine su Twitter e ottieni un media_id
      media = api.media_upload(filename)
      media_id = [media.media_id_string]

      # Posta il tweet con l'immagine
      api.update_status(status=status, media_id=media_id)
      os.remove(filename)  # Rimuovi il file immagine dopo l'uso
    else:
      # Posta un tweet senza immagine
      api.update_status(status=status)
  except Exception as e:
    print(f"Errore durante la pubblicazione su Twitter: {e}")


def scrape_amazon_offers(base_url, chat_id):
  offers = []  # Inizializza offers come lista vuota all'inizio della funzione
  response = requests.get(base_url, headers=get_headers())
  if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    offers = soup.select('div .s-result-item')
    if not offers:
      bot.send_message(chat_id, "Nessuna offerta trovata.")
      return
    if offers:
      print(f"Offerte trovate: {len(offers)}")
    for offer in offers:
      title_element = offer.select_one("span.a-text-normal")
      if not title_element:
        continue  # Skip offers without title
      title = escape_markdown_v2(title_element.text.strip())

      price_element = offer.select_one("span.a-offscreen")
      if not price_element:
        continue  # Skip offers without price
      price = escape_markdown_v2(price_element.text.strip())

      link_element = offer.select_one("a.a-link-normal")
      if not link_element or "href" not in link_element.attrs:
        continue  # Skip offers without link
      original_link = 'https://www.amazon.it' + str(link_element['href'])

      # Use create_linkvertise_link to generate the Linkvertise link
      linkvertise_url = create_linkvertise_link(original_link)

      image_element = offer.select_one("img.s-image")
      image_url = image_element['src'] if image_element else None
      offer_type = [
          'Offerta Imperdibile', 'Super Offerta', 'Offerta Lampo',
          'Offerta del Giorno', 'Offerta Speciale', 'Offerta Limitata',
          'Offerta Esclusiva'
      ]
      random_offer_type = random.choice(offer_type)
      caption = f"🔥 *{random_offer_type}:* _{title}_ \n\n🚀 a solo {price}\\!\n\n🛒       [Acquista Ora]({linkvertise_url})"
      # Dopo aver processato tutte le pagine, pubblica un unico tweet con un'offerta casuale
      if post_to_twitter and offers:
        random_offer = random.choice(offers)  # Seleziona un'offerta casuale
        tweet_content = f"🔥 *{random_offer.random_offer_type}:* _{random_offer.title}_ \n\n🚀 a solo {random_offer.price}\\!\n\n🛒 [Acquista Ora]({random_offer.linkvertise_url})"
        post_to_twitter(
            tweet_content, None
        )  # Assumi che post_to_twitter prenda il contenuto del tweet e opzionalmente un'immagine
        print(f"\n\n Offerta elaborata: *{title}* \\!\n\nprezzo: {price}\\!"
              )  # Stampa il nome dell'offerta
      # Moved inside the loop to ensure caption is defined before usage
      try:
        bot.send_photo(chat_id,
                       photo=image_url,
                       caption=caption,
                       parse_mode='MarkdownV2')
      except Exception as e:
        print(f"Error sending the photo: {e}")
      # Move this print statement inside the loop
      print(f"HTTP Error: {response.status_code}")


# Funzione per inviare messaggi tramite il bot di Telegram
def send_telegram_message(chat_id, message):
  bot.send_message(chat_id, message)


# Imposta un handler per un comando /start o /search che invoca lo scraping
@bot.message_handler(commands=['search'])
def handle_command(message):
  chat_id = message.chat.id
  bot.send_message(chat_id, "Test: bot attivo e risponde correttamente.")
  scrape_amazon_offers(
      'https://www.amazon.it/s?i=computers&bbn=425916031&rh=n%3A425916031%2Cp_89%3AAmazon%7CApple%7CHP%7CLogitech%7CSAMSUNG&dc&page=1&ref=sr_pg_1',
      chat_id)


def start_bot():
  bot.polling()
