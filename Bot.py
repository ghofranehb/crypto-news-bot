import os
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor


BOT_TOKEN = "7615366315:AAGhaD_NM-7qzsnGClLsf7CGPA9p1bUhrSA"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


CHANNEL_USERNAME = "@HodlHouseNewsBot"

# Function to fetch crypto news
def get_crypto_news():
    url = "https://api.coingecko.com/api/v3/news"
    response = requests.get(url).json()
    articles = response.get("data", [])[:3]  # Get top 3 news articles
    news_text = ""
    for article in articles:
        news_text += f"🔹 *{article['title']}*\n🔗 [Read More]({article['url']})\n\n"
    return news_text if news_text else "No news available now."

@dp.message_handler(commands=['news'])
async def send_news(message: types.Message):
    news = get_crypto_news()
    await bot.send_message(CHANNEL_USERNAME, news, parse_mode="Markdown")

# Function to post news automatically every hour
async def send_news_periodically():
    while True:
        news = get_crypto_news()
        await bot.send_message(CHANNEL_USERNAME, news, parse_mode="Markdown")
        await asyncio.sleep(3600)  # Posts every hour

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(send_news_periodically())
    executor.start_polling(dp)
