import bot_functionality.handlers as handlers
from telegram.ext import (
   CommandHandler, CallbackContext,
   ConversationHandler, MessageHandler,
   filters, Updater, CallbackQueryHandler, Application
)

from bot_functionality.config import TELEGRAM_BOT_TOKEN

# Initiating Bot Instance
updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
print(updater)

dispatcher = updater.dispatcher


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
      allow_reentry=True
   )
   dispatcher.add_handler(conversation_handler)
   updater.start_polling()
   updater.idle()

if __name__ == "__main__":
   main()

# from telegram.ext import Application, CommandHandler
# application = Application.builder().token('TOKEN').build()
# application.add_handler(CommandHandler('start', start_callback))
# application.run_polling()