import bot_functionality.handlers as handlers
from telegram.ext import (
   CommandHandler, CallbackContext,
   ConversationHandler, MessageHandler,
   filters, Updater, CallbackQueryHandler, Application
)
from telegram import Update

from bot_functionality.config import TELEGRAM_BOT_TOKEN

# Initiating Bot Instance
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# Start application

def main():
   conversation_handler = ConversationHandler(
      entry_points=[CommandHandler('start', handlers.start)],
      states={
         handlers.CHOOSING:[
            MessageHandler(
               filters.ALL, handlers.choose
            )
         ],
         handlers.CLASS_RATE:[
            CallbackQueryHandler(handlers.classer)
         ]
      },
      fallbacks=[CommandHandler('cancel', handlers.cancel)],
      allow_reentry=True,
   )
   application.add_handler(conversation_handler)
   application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
   main()