import random
import threading
import time
import telebot
from telebot import types
from offer_scraper import escape_markdown_v2
import os
from tqdm import tqdm
from termcolor import colored


def send_promo_message(chat_id):
  """
  Invia una serie di messaggi promozionali su Telegram.
  """
  promo_caption_premium = (
      "⚡️*Offerta Limitata!*⚡️\n"
      "🌟 *Iscriviti a Linkvertise Premium ora* e sblocca accesso immediato a offerte esclusive.\n"
      "✅ *Nessuna Pubblicità*\n"
      "✅ *Contenuti Premium Illimitati*\n"
      "👉 *Agisci ora!* Questa offerta scade a mezzanotte!")
  markup_premium = types.InlineKeyboardMarkup()
  button_premium = types.InlineKeyboardButton(
      text="Iscriviti Subito",
      url="https://linkvertise.com/premium?affid=1131101")
  markup_premium.add(button_premium)
  bot.send_message(chat_id,
                   promo_caption_premium,
                   reply_markup=markup_premium,
                   parse_mode='Markdown')

  # Breve pausa tra i messaggi
  time.sleep(2)  # Regola la durata della pausa a tuo piacimento

  # Messaggio per il canale a pagamento senza pubblicità
  promo_caption_exclusive = (
      "🔥 *Accedi a Offerte Segrete!* 🔥\n"
      "Unisciti al nostro canale VIP per scoprire offerte che non pubblichiamo altrove!\n"
      "⏳ *Le offerte sono limitate e aggiornate quotidianamente!*")
  markup_exclusive = types.InlineKeyboardMarkup()
  button_exclusive = types.InlineKeyboardButton(
      text="Unisciti al Canale VIP", url="https://t.me/your_paid_channel")
  markup_exclusive.add(button_exclusive)
  bot.send_message(chat_id,
                   promo_caption_exclusive,
                   reply_markup=markup_exclusive,
                   parse_mode='Markdown')

  # Messaggio con invito a compilare il form per offerte a tempo
  promo_caption_form = (
      "⌛ *Offerte Flash Disponibili Ora!* ⌛\n"
      "Compila il form esclusivo nel nostro canale VIP e ricevi offerte lampo direttamente nella tua inbox.\n"
      "🚀 *Agisci Velocemente!* Le offerte sono disponibili fino ad esaurimento scorte!"
  )
  markup_form = types.InlineKeyboardMarkup()
  button_form = types.InlineKeyboardButton(text="Compila il Form Ora",
                                           url="https://link.to/form")
  markup_form.add(button_form)
  bot.send_message(chat_id,
                   promo_caption_form,
                   reply_markup=markup_form,
                   parse_mode='Markdown')

  # Messaggio per incoraggiare la condivisione del canale
  promo_caption_share = (
      "📢 *Aiutaci a Crescere!* 📢\n"
      "Condividi il nostro canale con i tuoi amici e ottieni accesso a un *coupon esclusivo* per il tuo prossimo acquisto!\n"
      "👥 *Più siamo, migliori sono le offerte che possiamo offrire!*")
  markup_share = types.InlineKeyboardMarkup()
  button_share = types.InlineKeyboardButton(
      text="Condividi Ora", url="https://t.me/amazon_gratis_prodotti")
  markup_share.add(button_share)
  bot.send_message(chat_id,
                   promo_caption_share,
                   reply_markup=markup_share,
                   parse_mode='Markdown')


my_secret_BOT_TOKEN = os.environ['BOT_TOKEN']
chat_id = os.environ['CHAT_ID']
bot = telebot.TeleBot(my_secret_BOT_TOKEN)

# Variabile per controllare il thread di polling
polling_thread = None
stop_polling = threading.Event()


def random_sleep(minimum=1, maximum=3):
  time.sleep(random.uniform(minimum, maximum))


def send_offer_telegram(chat_id, offers):
  # Crea la barra di tqdm
  pbar = tqdm(
      total=len(offers),
      desc=colored("Invio offerte", "magenta"),
      bar_format=
      "{l_bar}%s{bar}%s| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
      % ('\x1b[1;34m', '\x1b[0m'))
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
      pbar.update(1)
      if i == promo_position:
        send_promo_message(chat_id)
    except Exception as e:
      print(f"Error sending the photo: {e}")
      if 'retry_after' in str(e):
        retry_after = int(str(e).split('retry after ')[1])
        print(f"Waiting {retry_after} seconds due to Telegram rate limits...")
        time.sleep(retry_after)  # Attendi il periodo di tempo suggerito
        pbar.update(1)  # Aggiorna comunque la barra per mantenere la coerenza
        continue
      pbar.update(1)  # Aggiorna la barra anche in caso di altri errori
  pbar.close()  # Chiudi la barra alla fine del ciclo
