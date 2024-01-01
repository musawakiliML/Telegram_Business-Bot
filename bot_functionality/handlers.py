from telegram import (
   ReplyKeyboardMarkup,
   ReplyKeyboardRemove, Update,
   InlineKeyboardButton, InlineKeyboardMarkup
)

from telegram.ext import (
   CommandHandler, CallbackContext,
   ConversationHandler, MessageHandler,
   filters, Updater, CallbackQueryHandler
)

from config import (
   TELEGRAM_BOT_TOKEN, CLOUDINARY_API_KEY,
   CLOUDINARY_API_NAME, CLOUDINARY_API_SECRET,
   FAUNA_API
)

import cloudinary
from cloudinary.uploader import upload
from faunadb import query as q
from faunadb.client import FaunaClient
from faunadb.errors import NotFound


# Configure Cloudinary API
cloudinary.config(
   cloud_name = CLOUDINARY_API_NAME,
   api_key = CLOUDINARY_API_KEY,
   api_secret = CLOUDINARY_API_SECRET
)

# Creating Fauna Client
fauna_client = FaunaClient(secret=FAUNA_API)

# Define Options for the ChatBot
CHOOSING, CLASS_RATE, SME_DETAILS, CHOOSE_PREF, SME_CAT, ADD_PRODUCTS, SHOW_STOCKS, POST_VIEW_PRODUCTS = range(8)
