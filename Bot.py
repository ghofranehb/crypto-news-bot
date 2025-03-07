import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import aiohttp

# Configuration (TEMPORARY TESTING ONLY)
BOT_TOKEN = "7615366315:AAGhaD_NM-7qzsnGClLsf7CGPA9p1bUhrSA"
CHANNEL_USERNAME = "@Hodl_house_news"
CRYPTO_PANIC_TOKEN = "989061952399bf3c79f6970617e153e6fcb646cc"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def get_crypto_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_PANIC_TOKEN}&public=true"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                return data.get("results", [])[:3]
    except Exception as e:
        logging.error(f"News error: {e}")
        return []

async def send_news():
    articles = await get_crypto_news()
    for article in articles:
        try:
            news_text = f"🔹 *{article['title']}*\n🔗 [Read More]({article['url']})"
            await bot.send_message(CHANNEL_USERNAME, news_text, parse_mode="Markdown")
            await asyncio.sleep(2)
        except Exception as e:
            logging.error(f"Send error: {e}")

@dp.message(Command("news"))
async def news_handler(message: Message):
    await message.answer("🔄 Fetching news...")
    await send_news()

async def periodic_news():
    while True:
        await send_news()
        await asyncio.sleep(3600)

async def main():
    asyncio.create_task(periodic_news())
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
