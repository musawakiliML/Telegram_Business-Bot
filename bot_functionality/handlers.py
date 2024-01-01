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


# Start Command Function
def start(update, context: CallbackContext) -> int:
   bot = context.bot
   chat_id = update.message.chat.id
   bot.send_message(
      chat_id = chat_id,
      text = "Hi fellow, Welcome to SMEbot ,"
        "Please tell me about yourself, "
        "provide your full name, email, and phone number, "
        "separated by comma each e.g: "
        "John Doe, JohnD@gmail.com, +234567897809"
   )
   return CHOOSING

# Get Generic user data from user and store

def choose(update, context):
   bot = context.bot
   chat_id = update.message.chat.id

   # Create new data entry from user input
   data = update.message.text.split(",")

   if len(data) < 3 or len(data) > 3:
      bot.send_message(
         chat_id = chat_id,
         text = "Invalid entry, please make sure to input the details "
            "as requested in the instructions"
      )
      bot.send_message(
         chat_id = chat_id,
         text = "Type /start, to restart bot"
      )
      return ConversationHandler.END
   # Check if user exists before creating a new one

   new_user = fauna_client.query(
      q.create(
         q.collection("User"), {
            "data":{
               "name":data[0],
               "email":data[1],
               "telephone":data[2],
               "is_smeowner":False,
               "preference":"",
               "chat_id": chat_id
            }
         }
      )
   )
   context.user_data["user-id"] = new_user["ref"].id()
   context.user_data["user-name"] = data[0]
   context.user_data["user-data"] = new_user['data']
   reply_keyboard = [
      [
         InlineKeyboardButton(
            text="SME",
            callback_data="SME"
         ),
         InlineKeyboardButton(
            text="Customer",
            callback_data="Customer"
         )
      ]
   ]
   markup = InlineKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
   bot.send_message(
      chat_id = chat_id,
      text = "Collected information succesfully!..🎉🎉 \n"
        "Which of the following do you identify as ?",
      reply_markup = markup
   )
   return CLASS_RATE

# Class 

def classer(update, context):
   bot = context.bot
   chat_id = update.callback_query.message.chat.id
   name = context.user_data["user-name"]
   if update.callback_query.data.lower() == "sme":
      # update user as smeowner
      fauna_client.query(
         q.update(
            q.ref(
               q.collection("User"), context.user_data["user-id"]
            ), {"data": {"is_smeowner":True}}
         )
      )
      bot.send_message(
         chat_id = chat_id,
         text = f"Great! {name}, please tell me about your business, "
            "provide your BrandName, Brand email, Address, and phone number"
            "in that order, each separated by comma(,) each e.g: "
            "JDWears, JDWears@gmail.com, 101-Mike Avenue-Ikeja, +234567897809",
         reply_markup = ReplyKeyboardRemove()
      )
      return SME_DETAILS
   elif update.callback_query.data.lower() == "customer":
      categories = [
         [
            InlineKeyboardButton(
               text="Clothing/Fashion",
               callback_data="Clothing/Fashion"
            ),
            InlineKeyboardButton(
               text="Hardware Accessories",
               callback_data="Hardware Accessories"
            )
         ],
         [
            InlineKeyboardButton(
               text="Food/Kitchen Ware",
               callback_data="Food/Kitchen Ware"
            ),
            InlineKeyboardButton(
               text="Art and Design",
               callback_data="Art and Design"
            )
         ]
      ]
      bot.send_message(
         chat_id=chat_id,
         text="Here's a list of categories available"
         "Choose one that matches your interest",
         reply_markup = InlineKeyboardMarkup(categories)
      )
      return CHOOSE_PREF

# Cancel Control

def cancel(update: Update, context: CallbackContext) -> int:
   update.message.reply_text(
      'Bye! I hope we can talk again some day.',
      reply_markup=ReplyKeyboardRemove()
   )
   return ConversationHandler.END
