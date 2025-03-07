import asyncio
import requests
import logging
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command  

BOT_TOKEN = "7615366315:AAGhaD_NM-7qzsnGClLsf7CGPA9p1bUhrSA"
CHANNEL_USERNAME = "@Hodl_house_news"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()  
router = Router()

def get_crypto_news():
    url = "https://api.coingecko.com/api/v3/news"
    response = requests.get(url).json()
    articles = response.get("data", [])[:3]  
    news_text = ""
    for article in articles:
        news_text += f"🔹 *{article['title']}*\n🔗 [Read More]({article['url']})\n\n"
    return news_text if news_text else "No news available now."

@router.message(Command("news"))  
async def send_news(message: types.Message):
    news = get_crypto_news()
    await bot.send_message(CHANNEL_USERNAME, news, parse_mode="Markdown")

async def send_news_periodically():
    while True:
        news = get_crypto_news()
        await bot.send_message(CHANNEL_USERNAME, news, parse_mode="Markdown")
        await asyncio.sleep(3600)  

async def main():
    dp.include_router(router)
    asyncio.create_task(send_news_periodically())  
    await dp.start_polling(bot)  

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())  
