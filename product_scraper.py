import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import re
import urllib.parse
import os
import random
import time
from tqdm import tqdm  # Importing tqdm for the progress bar

print(os.getcwd())


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


def add_watermark_with_icon(image_path, icon_path):
  image = Image.open(image_path)
  icon = Image.open(icon_path)
  icon = icon.resize((50, 50))  # Adjust size as needed
  image.paste(icon, (image.width - 50, image.height - 50), icon)
  image.save(image_path)


def scrape_amazon_product(url, amazon_affiliate_id):
  headers = get_headers()
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, 'html.parser')

  # Extract product details
  title = soup.find('span', id='productTitle').text.strip() if soup.find(
      'span', id='productTitle') else "Title Not Found"
  description = soup.find(
      'div', id='featurebullets_feature_div').text.strip() if soup.find(
          'div', id='featurebullets_feature_div') else "Description Not Found"
  stars = soup.find('span', class_='a-icon-alt').text.strip() if soup.find(
      'span', class_='a-icon-  alt') else "Stars Not Found"
  top_review = soup.find(
      'span', class_='review-text-content').text.strip() if soup.find(
          'span', class_='review-text-content') else "Top Review Not Found"

  # Extract pricing information
  price_block = soup.find('span', id='priceblock_ourprice') or soup.find(
      'span', id='priceblock_dealprice')
  discount_price = price_block.text.strip(
  ) if price_block else "Price Not Found"

  # Extract the image URL
  image_url_element = soup.find('img', id='landingImage')
  image_url = image_url_element['src'] if image_url_element else None
  if image_url:
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    image_path = 'product_image.png'
    image.save(image_path)
    add_watermark_with_icon(image_path, 'watermark.png')
  else:
    image_path = "No image downloaded"

  combined_affiliate_link = generate_affiliate_link(url, amazon_affiliate_id)

  return {
      'title': title,
      'description': description,
      'discount_price': discount_price,
      'stars': stars,
      'top_review': top_review,
      'image_path': image_path,
      'combined_affiliate_link': combined_affiliate_link
  }


def generate_affiliate_link(amazon_url, amazon_affiliate_id):
  import monetization.linkvertise_bot as linkvertise  # Importing the 'linkvertise' module locally
  product_id = extract_product_id_from_url(amazon_url)
  amazon_base_url = "https://www.amazon.it/dp/"
  amazon_affiliate_link = f"{amazon_base_url}{product_id}?tag={amazon_affiliate_id}"
  encoded_amazon_link = urllib.parse.quote_plus(amazon_affiliate_link)
  # Convert the Amazon affiliate link to a Linkvertise link using the linkvertise module
  linkvertise_url = linkvertise.create_linkvertise_link(encoded_amazon_link)
  return linkvertise_url


def extract_product_id_from_url(url):
  match = re.search(r'/dp/(\w+)', url)
  if match:
    return match.group(1)
  else:
    raise ValueError("Invalid URL: Product ID not found.")


# Example usage
try:
  amazon_affiliate_id = os.environ['amazon']
  linkvertise_user_id = os.environ['linkvertise']
  product_info = scrape_amazon_product('https://www.amazon.it/dp/B0CSFYT48V',
                                       amazon_affiliate_id)
  print(product_info)
except Exception as e:
  print(f"An error occurred: {e}")
