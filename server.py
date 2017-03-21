import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler,CallbackQueryHandler, Filters, ConversationHandler

from bot_handlers import start, train_bayes, train_bayes__text, train_bayes__label, test_bayes, test_bayes__text, accuracy
from bot_handlers import button
from bot_handlers import error


from token_api import token_api

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

WAITING_FOR_TEST, WAITING_FOR_TEXT, WAITING_FOR_LABEL = range(3)

updater = Updater(token_api())


test_handler = ConversationHandler(
    entry_points=[CommandHandler('test', test_bayes)],
    states={
        WAITING_FOR_TEST: [MessageHandler(Filters.text, test_bayes__text)]
    },
    fallbacks=[CommandHandler('start', start)]
)

train_handler = ConversationHandler(
    entry_points=[CommandHandler('train', train_bayes)],
    states={
        WAITING_FOR_TEXT: [MessageHandler(Filters.text, train_bayes__text)],
        WAITING_FOR_LABEL: [MessageHandler(Filters.text, train_bayes__label)]
    },
    fallbacks=[CommandHandler('start', start)]
)


updater.dispatcher.add_handler(CommandHandler('start', start))
# updater.dispatcher.add_handler(CommandHandler('train', train))
# updater.dispatcher.add_handler(CommandHandler('test', test))
updater.dispatcher.add_handler(test_handler)
updater.dispatcher.add_handler(train_handler)
# updater.dispatcher.add_handler(CommandHandler('restart', restart))
updater.dispatcher.add_handler(CommandHandler('accuracy', accuracy))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_error_handler(error)

updater.start_polling()
updater.idle()