import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler,CallbackQueryHandler, Filters, ConversationHandler

from bot_handlers import start, train, train_bayes, train2_bayes, test, test_bayes, accuracy
from bot_handlers import button
from bot_handlers import error

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

WAITING_FOR_TEST, WAITING_FOR_TRAIN, WAITING_FOR_TRAIN2 = range(3)

updater = Updater("373643335:AAGSpALhhKzZdsMkMGxoYI1nh7UPoO4FLvg")


test_handler = ConversationHandler(
    entry_points=[CommandHandler('test', test)],
    states={
        WAITING_FOR_TEST: [MessageHandler(Filters.text, test_bayes)]
    },
    fallbacks=[CommandHandler('start', start)]
)

train_handler = ConversationHandler(
    entry_points=[CommandHandler('train', train)],
    states={
        WAITING_FOR_TRAIN: [MessageHandler(Filters.text, train_bayes)],
        WAITING_FOR_TRAIN2: [MessageHandler(Filters.text, train2_bayes)]
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