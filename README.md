# py_marketing_advisor: Amazon Product Scraper and Telegram Bot

## Project Overview
This project consists of a Python-based scraper that extracts product details from Amazon product pages and sends this information via a Telegram bot to a specified channel. It is designed to notify followers of the latest deals, product details, and pricing updates. The scraper integrates with the Linkvertise service to generate affiliate links, enhancing monetization through affiliate marketing.

## Features
- **Product Detail Extraction**: Scrapes Amazon product pages for essential details such as title, description, price, star ratings, and top customer reviews.
- **Image Processing**: Downloads product images, adds watermarks, and saves them locally.
- **Affiliate Link Generation**: Generates affiliate links through Linkvertise for monetization.
- **Telegram Integration**: Sends formatted messages to a Telegram channel to update subscribers about new deals and offers.
- **Robust Error Handling**: Includes mechanisms to handle common scraping issues, such as HTTP errors and missing content.
- **User-Agent Rotation**: Utilizes rotating user agents to minimize the risk of being blocked by Amazon.

## Technologies Used
- **Python 3**
- **Beautiful Soup 4**: For web scraping.
- **PIL (Pillow)**: For image processing.
- **Requests**: Library for HTTP requests.
- **Telebot**: Library for interacting with the Telegram API.
- **tqdm**: For progress bar visualization.

## Installation
Clone this repository:
\```bash
git clone https://github.com/yourusername/amazon-scraper-telegram-bot.git
cd amazon-scraper-telegram-bot
\```
Install the required dependencies:
\```bash
pip install -r requirements.txt
\```

## Configuration
- **Environment Variables**: Set up the necessary environment variables or use a `.env` file to store them:
  - `BOT_TOKEN`: Your Telegram bot token.
  - `CHAT_ID`: The chat ID of your Telegram channel.
  - `LINKVERTISE_USER_ID`: Your user ID for Linkvertise.
  - `AMAZON_AFFILIATE_ID`: Your Amazon affiliate ID.
- **Telegram Bot Setup**: Create a bot via [BotFather](https://t.me/botfather) on Telegram and obtain the bot token.
- **Linkvertise Account**: Ensure you have a Linkvertise account and obtain your user ID.

## Usage
Run the script with:
\```bash
python product_scraper.py
\```
You will be prompted to enter the URL of the Amazon product you want to scrape. After the details are scraped, they will automatically be sent to your configured Telegram channel.

## Contributing
Contributions are welcome! Please feel free to submit pull requests, suggest features, or report bugs.

## License
Distributed under the MIT License. See LICENSE for more information.

## Disclaimer
This tool is intended for educational purposes and personal use. Please respect Amazon's Terms of Service regarding scraping and automated access to their site.

