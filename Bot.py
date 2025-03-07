import asyncio
import requests
import logging
from aiogram import Bot, Dispatcher, types


BOT_TOKEN = "7615366315:AAGhaD_NM-7qzsnGClLsf7CGPA9p1bUhrSA"
CHANNEL_USERNAME = "@Hodl_house_news"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Fetch crypto news
def get_crypto_news():
    url = "https://api.coingecko.com/api/v3/news"
    response = requests.get(url).json()
    articles = response.get("data", [])[:3]  # Get top 3 news articles
    news_text = ""
    for article in articles:
        news_text += f"🔹 *{article['title']}*\n🔗 [Read More]({article['url']})\n\n"
    return news_text if news_text else "No news available now."

# Command to fetch news manually
@dp.message(commands=['news'])
async def send_news(message: types.Message):
    news = get_crypto_news()
    await bot.send_message(CHANNEL_USERNAME, news, parse_mode="Markdown")

# Auto-post news every hour
async def send_news_periodically():
    while True:
        news = get_crypto_news()
        await bot.send_message(CHANNEL_USERNAME, news, parse_mode="Markdown")
        await asyncio.sleep(3600)  # Wait 1 hour

async def main():
    dp.include_router(dp.router)  # Fix for Aiogram v3
    asyncio.create_task(send_news_periodically())  # Run auto-news function
    await dp.start_polling(bot)  # Start the bot

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())  # Run bot with Aiogram v3
