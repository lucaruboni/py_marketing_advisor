import telebot
from telebot import types
import os
import time
import sys

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from product_scraper import scrape_amazon_product

# Assicurati che l'import sia corretto

# Inizializza il bot con il tuo token
my_secret_BOT_TOKEN = os.environ['BOT_TOKEN']
chat_id = os.environ['CHAT_ID_PRODUCT']
bot = telebot.TeleBot(my_secret_BOT_TOKEN)


def send_product_details_to_telegram(chat_id, product_info):
  title = product_info['title']
  discount_price = product_info['discount_price']
  link = product_info['combined_affiliate_link']
  description = product_info['description']

  message_text = (
      f"😍 Nuovo Coupon! Prezzo ancora più basso!!\n\n"
      f"🔥 *{title}*\n"
      f"{description}\n\n"
      f"💶 *Offerta a soli {discount_price}* 🔥\n"
      f"🚚 Amazon\n"
      f"👉 [Compra ora]({link})\n\n"
      f"ℹ️ Disclaimer: Offerta con commissioni guadagnate sulle vendite #pubblicità"
  )

  bot.send_message(chat_id,
                   message_text,
                   parse_mode='Markdown',
                   disable_web_page_preview=False)


def fetch_and_send_product():
  amazon_affiliate_id = os.environ['amazon']
  product_url = 'https://www.amazon.it/dp/B0CSFYT48V'

  # Scrape product details
  product_info = scrape_amazon_product(product_url, amazon_affiliate_id)
  print("Product info scraped:", product_info)

  # Send product details to Telegram
  send_product_details_to_telegram(chat_id, product_info)


# Chiamata alla funzione fetch_and_send_product() all'avvio del bot
fetch_and_send_product()


# Aggiungi un gestore per il comando '/send_product_info'
@bot.message_handler(commands=['send_product_info'])
def handle_command(message):
  fetch_and_send_product()


# Avvia il polling
bot.polling()
