import asyncio
import requests
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN = "7615366315:AAGhaD_NM-7qzsnGClLsf7CGPA9p1bUhrSA"
CHANNEL_USERNAME = "@Hodl_house_news"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_crypto_news():
    url = "https://cryptopanic.com/api/v1/posts/?auth_token=989061952399bf3c79f6970617e153e6fcb646cc&public=true"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "results" not in data or len(data["results"]) == 0:
            return []  

        return data["results"][:3]  

    except Exception as e:
        logging.error(f"Error fetching news: {e}")
        return []

async def send_news():
    articles = get_crypto_news()
    if not articles:
        return  # Do nothing if no news

    for article in articles:
        title = article.get("title", "No title")
        url = article.get("url", "#")
        news_text = f"🔹 *{title}*\n🔗 [Read More]({url})"
        await bot.send_message(CHANNEL_USERNAME, news_text, parse_mode="Markdown")
        await asyncio.sleep(5)  

@dp.message(Command("news"))
async def send_news_command(message: Message):
    await send_news()

async def send_news_periodically():
    while True:
        await send_news()
        await asyncio.sleep(3600)  

async def main():
    dp.include_router(dp)  # Fix router issue
    asyncio.create_task(send_news_periodically())  
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
