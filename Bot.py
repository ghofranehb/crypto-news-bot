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
    url = "https://cryptopanic.com/api/v1/posts/?auth_token=989061952399bf3c79f6970617e153e6fcb646cc&public=true"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()

        if "results" not in data or len(data["results"]) == 0:
            return "⚠ No crypto news available at the moment."

        articles = data["results"][:3]  
        news_text = ""
        for article in articles:
            title = article.get("title", "No title")
            url = article.get("url", "#")
            news_text += f"🔹 *{title}*\n🔗 [Read More]({url})\n\n"

        return news_text

    except requests.exceptions.RequestException as e:
        return f"⚠ Error fetching news: {str(e)}"


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
