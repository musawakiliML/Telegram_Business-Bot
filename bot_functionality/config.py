import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["Telegram_Bot_API"]
CLOUDINARY_API_SECRET = os.environ["Cloudinary_API_SECRET"]
CLOUDINARY_API_KEY = os.environ["Cloudinary_API_KEY"]
CLOUDINARY_API_NAME = os.environ["Cloudinary_API_NAME"]
FAUNA_API = os.environ["Fauna_API"]