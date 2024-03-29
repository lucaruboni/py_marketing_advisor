import tweepy
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from monetization.linkvertise import create_linkvertise_link
import random
import time
import telebot  # Import pyTelegramBotAPI as telebot
import os

# Twitter API credentials
consumer_key = 'glcJYziW99lhskKQSyobDiYno'
consumer_secret = 'q6Ex5k8UpFXFnMi0osPPb7P4Sdkp5T621mpc6j8QruZUehGtFU'
access_token = '1767993419350130688-XeJAgQplsKUI5McI4ADUkKcIqQdBry'
access_token_secret = '0ux22GQUDmQ4gZ0grZbquEAqXJzSGyKk3c05Ig9auLvVy'

# Setup Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

BOT_TOKEN = '6989199727:AAFKeuXw1j3ZzNtdmbmKLIUg7ZuuU5Sxjkg'
CHAT_ID = '-1002117648510'
bot = telebot.TeleBot(BOT_TOKEN)

def escape_markdown_v2(text):
    escape_chars = '_*[]()~`>#+-=|{}.!\\'
    return ''.join(['\\' + char if char in escape_chars else char for char in text])

def random_sleep(minimum=1, maximum=3):
    time.sleep(random.uniform(minimum, maximum))

def get_headers():
    user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
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
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.177",]
    return {
        "User-Agent": random.choice(user_agents)
    }

# All'inizio del file, assicurati di avere l'import corretto
from monetization.linkvertise import create_linkvertise_link

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
            media_ids = [media.media_id_string]
            
            # Posta il tweet con l'immagine
            api.update_status(status=status, media_ids=media_ids)
            os.remove(filename)  # Rimuovi il file immagine dopo l'uso
        else:
            # Posta un tweet senza immagine
            api.update_status(status=status)
    except Exception as e:
        print(f"Errore durante la pubblicazione su Twitter: {e}")

def scrape_amazon_offers(base_url, chat_id, max_pages=5):
    for page in range(1, max_pages + 1):
        url = f"{base_url}&page={page}"
        response = requests.get(url, headers=get_headers())
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            offers = soup.select('.s-result-item')
        if not offers:
            bot.send_message(chat_id, "Nessuna offerta trovata.")
            return
        for offer in offers:
            title_element = offer.select_one("span.a-text-normal")
            if not title_element:
                continue  # Salta offerte senza titolo
            title = escape_markdown_v2(title_element.text.strip())
            
            price_element = offer.select_one("span.a-offscreen")
            if not price_element:
                continue  # Salta offerte senza prezzo
            price = escape_markdown_v2(price_element.text.strip())
            
            link_element = offer.select_one("a.a-link-normal")
            if not link_element or "href" not in link_element.attrs:
                continue  # Salta offerte senza link
            original_link = 'https://www.amazon.it' + link_element['href']
            
            # Usa create_linkvertise_link per generare il link di Linkvertise
            linkvertise_url = create_linkvertise_link(original_link)
            
            image_element = offer.select_one("img.s-image")
            image_url = image_element['src'] if image_element else None
            offer_type= ['Offerta Imperdibile', 'Super Offerta', 'Offerta Lampo','Offerta del Giorno', 'Offerta Speciale', 'Offerta Limitata', 'Offerta Esclusiva']
            random_offer_type = random.choice(offer_type)
            caption = f"🔥 *{random_offer_type}:* _{title}_ \n\n🚀 a solo {price}\\!\n\n🛒 [Acquista Ora]({linkvertise_url})"
            twitter_status = f"🔥 Offerta Imperdibile: {title} a solo {price}! Scopri di più qui: {linkvertise_url}"

            try:
                
                bot.send_photo(chat_id, photo=image_url, caption=caption, parse_mode='MarkdownV2')
                 # Postare l'offerta su Twitter
                post_to_twitter(twitter_status, linkvertise_url, image_url)  # Assicurati che questa funzione sia definita correttamente
            except Exception as e:
                print(f"Errore nell'invio della foto: {e}")
    else:
        print(f"Errore HTTP: {response.status_code}")



# Funzione per inviare messaggi tramite il bot di Telegram
def send_telegram_message(chat_id, message):
    bot.send_message(chat_id, message)

# Imposta un handler per un comando /start o /search che invoca lo scraping
@bot.message_handler(commands=['search'])
def handle_command(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Test: bot attivo e risponde correttamente.")
    scrape_amazon_offers('https://www.amazon.it/s?i=computers&bbn=425916031&rh=n%3A425916031%2Cp_89%3AAmazon%7CApple%7CHP%7CLogitech%7CSAMSUNG&dc&page=11&ref=sr_pg_11', chat_id)

def start_bot():
    bot.polling()
