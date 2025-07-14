import os
import json
import logging
import asyncio
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv

# === Load .env credentials ===
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = "session"  # Will save as session.session

# Channels to scrape
CHANNELS = {
    "chemed": "https://t.me/lobelia4cosmetics",
    "tikvah": "https://t.me/tikvahpharma",
    "ChemedTelegramChannel":'https://t.me/ChemedTelegramChannel',
    'tenamereja':"https://t.me/tenamereja",
    'HakimApps_Guideline':"https://t.me/HakimApps_Guideline"
}

# === Logging setup ===
logging.basicConfig(
    filename="scrape.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# === Utilities ===
def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def save_raw_json(messages, channel_name):
    today = datetime.today().strftime("%Y-%m-%d")
    dir_path = os.path.join("data", "raw", "telegram_messages", today)
    ensure_dir(dir_path)
    filepath = os.path.join(dir_path, f"{channel_name}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

# === Main scraping logic ===                                                                                                                                                                                                   
async def scrape_channel(client, channel_name, channel_url, limit=10000):
    try:
        entity = await client.get_entity(channel_url)
        messages = []

        async for message in client.iter_messages(entity, limit=limit):
            msg = {
                "id": message.id,
                "text": message.message,
                "date": message.date.strftime("%Y-%m-%d %H:%M:%S") if message.date else None,
                "media": None
            }

            if isinstance(message.media, MessageMediaPhoto):
                try:
                    img_dir = os.path.join("data", "raw", "telegram_messages", "images", channel_name)
                    ensure_dir(img_dir)
                    image_path = os.path.join(img_dir, f"{message.id}.jpg")
                    await message.download_media(file=image_path)
                    msg["media"] = image_path
                except Exception as e:
                    logging.error(f"Failed to download image for message {message.id} in {channel_name}: {e}")
            
            messages.append(msg)

        save_raw_json(messages, channel_name)
        logging.info(f"✅ Scraped {len(messages)} messages from {channel_name}")

    except FloodWaitError as e:
        logging.warning(f"Rate limited. Sleeping for {e.seconds} seconds.")
        await asyncio.sleep(e.seconds)
        await scrape_channel(client, channel_name, channel_url, limit)
    except Exception as e:
        logging.error(f"❌ Error scraping {channel_name}: {e}")

# === Auth + Main controller ===
async def main():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        if not await client.is_user_authorized():
            phone = input("Enter your phone number (e.g. +2519XXXXXXX): ")
            await client.send_code_request(phone)
            code = input("Enter the OTP code you received: ")
            try:
                await client.sign_in(phone, code)
            except Exception as e:
                logging.error(f"Login failed: {e}")
                return

        logging.info("🚀 Starting scraping...")

        tasks = [scrape_channel(client, name, url) for name, url in CHANNELS.items()]
        await asyncio.gather(*tasks)

        logging.info("✅ All channels scraped successfully.")

# === Run it ===
if __name__ == "__main__":
    asyncio.run(main())


