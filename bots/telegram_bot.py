import random
import threading
import time
import telebot
from telebot import types
from offer_scraper import escape_markdown_v2
import os

my_secret_BOT_TOKEN = os.environ['BOT_TOKEN']
chat_id = os.environ['CHAT_ID']
bot = telebot.TeleBot(my_secret_BOT_TOKEN)

# Variabile per controllare il thread di polling
polling_thread = None
stop_polling = threading.Event()


def random_sleep(minimum=1, maximum=3):
  time.sleep(random.uniform(minimum, maximum))


def send_offer_telegram(
    chat_id, offers
):  # Nota che ora è `offers`, indicando che ci si aspetta una lista di offerte
  # Determina casualmente dopo quante offerte inviare il messaggio promozionale
  promo_position = random.randint(1, len(offers))

  for i, offer in enumerate(offers, start=1):
    title = escape_markdown_v2(offer['title'])
    price = escape_markdown_v2(offer['price'])
    linkvertise_url = offer['linkvertise_url']
    selected_offer_type = random.choice(offer['offer_type'])
    caption = f"🔥 *{selected_offer_type}:* _{title}_ \n\n🚀 a solo {price}\\! "
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Acquista Ora",
                                        url=linkvertise_url)
    markup.add(button)
    try:
      bot.send_photo(chat_id,
                     offer['image_url'],
                     caption=caption,
                     parse_mode='MarkdownV2',
                     reply_markup=markup)
      # Dopo promo_position offerte, invia il messaggio promozionale
      if i == promo_position:
        send_promo_message(chat_id)
    except Exception as e:
      print(f"Error sending the photo: {e}")


def send_promo_message(chat_id):
  """
  Invia un messaggio promozionale su Telegram.
  """
  promo_caption = "🌟 Vuoi ancora più offerte esclusive? Passa a Linkvertise Premium oggi stesso! 🌟"
  markup = types.InlineKeyboardMarkup()
  promo_button = types.InlineKeyboardButton(
      text="Scopri di più", url="https://linkvertise.com/premium")
  markup.add(promo_button)
  bot.send_message(chat_id, promo_caption, reply_markup=markup)
