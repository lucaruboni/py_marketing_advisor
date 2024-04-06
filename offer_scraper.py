import requests
from termcolor import colored
import random
import time
from bs4 import BeautifulSoup
from monetization.linkvertise_bot import create_linkvertise_link


def get_headers():
  user_agents = []
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
  user_agents.extend([
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15",
      "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
      "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
      "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
      "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
      "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
      "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
      "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0",
      "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.22 (KHTML, like Gecko) Ubuntu Chromium/25.0.1364.160 Chrome/25.0.1364.160 Safari/537.22",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.28.10 (KHTML, like Gecko) Version/6.0.3 Safari/536.28.10",
      "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
      "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1",
      "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/12.04 Chromium/18.0.1025.168 Chrome/18.0.1025.168 Safari/535.19",
      "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
      "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7",
      "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
  ])

  return {"User-Agent": random.choice(user_agents)}


def escape_markdown_v2(text):
  escape_chars = '_*[]()~`>#+-=|{}.!\\'
  return ''.join(
      ['\\' + char if char in escape_chars else char for char in text])


def random_sleep(minimum=1, maximum=3):
  time.sleep(random.uniform(minimum, maximum))


def make_request_with_retries(url, session, max_attempts=5):
  base_sleep_time = 5  # inizia con 5 secondi
  for attempt in range(max_attempts):
    response = session.get(url)
    if response.status_code == 200:
      return response  # Restituisce la risposta se è riuscita
    elif response.status_code == 503:
      # Gestisce specificamente l'errore 503
      sleep_time = base_sleep_time * (2**attempt)
      print(
          colored(
              f"503 Service Unavailable ricevuto, tentativo {attempt + 1}. Attendo {sleep_time} secondi prima di riprovare.",
              'red'))
      time.sleep(sleep_time)
    else:
      # Gestisce tutti gli altri codici di stato di errore
      sleep_time = base_sleep_time * (2**attempt)
      print(
          colored(
              f"Errore {response.status_code} ricevuto, tentativo {attempt + 1}. Attendo {sleep_time} secondi prima di riprovare.",
              'red'))
      time.sleep(sleep_time)

  print(colored("Massimi tentativi raggiunti. Richiesta fallita.", 'red'))
  return None


# In the offer_scraper.py file, modify the scrape_amazon_offers function
def scrape_amazon_offers(base_url, chat_id, max_pages=10):
  offers = []
  session = requests.Session()  # Crea una sessione
  session.headers.update(get_headers())  # Imposta gli header della sessione

  def random_sleep(minimum=1, maximum=5):
    time.sleep(random.uniform(minimum, maximum))

  session = requests.Session()
  session.headers.update(get_headers())

  # Esempio di utilizzo della funzione make_request_with_retries
  homepage_url = "https://www.amazon.it"
  response = make_request_with_retries(homepage_url, session)
  if response:
    print("Accesso alla homepage riuscito")
    # Prosegui con l'elaborazione della risposta
  else:
    print("Impossibile accedere alla homepage dopo vari tentativi.")

  page = random.randint(1, 40)
  url = f"{base_url}&page={page}"
  print(f"Tentativo di accesso a: {url} ")  # Stampa l'URL
  try:
    # Usa make_request_with_retries anche per questa richiesta
    response = make_request_with_retries(url, session)
    if not response:
      print(f"Impossibile accedere alla pagina {page} dopo vari tentativi.")
      return offers  # Esce dalla funzione se non riesce ad accedere alla pagina desiderata

    # Se la richiesta è riuscita, procedi con lo scraping
    print(f"Scraping pagina {page}, status code: {response.status_code}")
    random_sleep(1, 4)
    soup = BeautifulSoup(response.content, 'html.parser')
    offer_elements = soup.select('div .s-result-item')
    if not offer_elements:
      print(chat_id, "Nessuna offerta trovata.")
      return offers

    print(f"Offerte trovate: {len(offer_elements)}")
    for offer_element in offer_elements:
      random_sleep(1, 5)
      title_element = offer_element.select_one("span.a-text-normal")
      if not title_element:
        continue  # Skip offers without title
      title = escape_markdown_v2(title_element.text.strip())

      price_element = offer_element.select_one("span.a-offscreen")
      if not price_element:
        continue  # Skip offers without price
      price = escape_markdown_v2(price_element.text.strip())

      link_element = offer_element.select_one("a.a-link-normal")
      if not link_element or "href" not in link_element.attrs:
        continue  # Skip offers without link
      original_link = 'https://www.amazon.it' + str(link_element['href'])

      # Use create_linkvertise_link to generate the Linkvertise link
      linkvertise_url = create_linkvertise_link(original_link)

      image_element = offer_element.select_one("img.s-image")
      image_url = image_element['src'] if image_element else None

      offer = {
          'title':
          title,
          'price':
          price,
          'linkvertise_url':
          linkvertise_url,
          'image_url':
          image_url,
          'offer_type': [
              'Offerta Imperdibile', 'Super Offerta', 'Offerta Lampo',
              'Offerta del Giorno', 'Offerta Speciale', 'Offerta Limitata',
              'Offerta Esclusiva',
              '⚠️ __Attenzione__ ⚠️ Possibile *🚀🔥Errore di Prezzo🔥🚀*'
          ]
      }
      offers.append(offer)
  except Exception as e:
    print(f"Errore durante lo scraping della pagina {page}: {e}")

  return offers
