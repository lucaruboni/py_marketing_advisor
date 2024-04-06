import tweepy
from tweepy.errors import TweepyException
import requests
import os
from io import BytesIO
from offer_scraper import escape_markdown_v2


def setup_twitter_api():
  consumer_key = os.environ['consumer_key']
  consumer_secret = os.environ['consumer_secret']
  access_token = os.environ['access_token']
  access_token_secret = os.environ['access_token_secret']

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)
  return api


def post_to_twitter(api, offer):
  # Costruzione dello status del tweet
  status = f"🔥 {offer['offer_type']}: {escape_markdown_v2(offer['title'])} \n🚀 a solo {escape_markdown_v2(offer['price'])}"

  if offer['image_url']:
    try:
      response = requests.get(offer['image_url'])
      if response.status_code == 200:
        image_bytes = BytesIO(response.content)
        filename = 'temp.jpg'
        with open(filename, 'wb') as img_file:
          img_file.write(image_bytes.read())

        # Tentativo di caricamento dell'immagine e pubblicazione del tweet
        media = api.media_upload(filename)
        api.update_status(status=status, media_ids=[media.media_id])
        os.remove(filename)  # Rimozione del file temporaneo
        print("Postato su Twitter con immagine")
    except requests.exceptions.RequestException as e:
      print(f"Errore nella richiesta HTTP dell'immagine: {e}")
    except TweepyException as e:
      print(
          f"Errore di Tweepy durante la pubblicazione su Twitter con immagine: {e}"
      )
    except Exception as e:
      print(
          f"Errore generico durante la pubblicazione su Twitter con immagine: {e}"
      )
  else:
    try:
      # Tentativo di pubblicazione del tweet senza immagine
      api.update_status(status=status)
      print("Postato su Twitter senza immagine")
    except TweepyException as e:
      print(
          f"Errore di Tweepy durante la pubblicazione su Twitter senza immagine: {e}"
      )
      print(e.api_code)
      print(e.response.text)
    except Exception as e:
      print(
          f"Errore generico durante la pubblicazione su Twitter senza immagine: {e}"
      )
