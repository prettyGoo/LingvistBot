import os, os.path

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from classifier.bayes import Bayes
from telegram.ext.dispatcher import run_async

bayes = Bayes()


class TrainingHelper():
    def __init__(self):
        self.training_text = ''
        self.training_label = ''

th = TrainingHelper()

for i in range(1, 10):
    file = open('reviews/reviews_0%s.txt' % i)
    words = file.read().replace('\n', ' ').split(' ')
    features = bayes.document_features(words)
    a = bayes.classify(features)
    print(a)


WAITING_FOR_TEST, WAITING_FOR_TRAIN, WAITING_FOR_TRAIN2 = range(3)


def start(bot, update):
    update.message.reply_text("Hello, I am LinvgistBot! "
                              "I can classify texts using different algorithms."
                              "Try me for your fun")


@run_async
def train(bot, update):
    update.message.reply_text('Input some text and its label in two different Telegram messages. '
                              'The length of the text must be at least 500 characters and within one Telegram message')

    return WAITING_FOR_TRAIN


def train_bayes(bot, update):
    th.training_text = update.message.text.lower()
    if len(th.training_text) < 500:
        update.message.reply_text('Your text must contain at least 500 characters.\nTry again with /test')
    else:
        update.message.reply_text('Input label for your text.\n'
                                  'It must be one of these: news, hobbies, government, reviews')

    return WAITING_FOR_TRAIN2


def train2_bayes(bot, update):
    th.training_label = update.message.text.lower()
    if th.training_label not in ['news', 'reviews', 'government', 'hobbies']:
        th.training_label = ''
        update.message.reply_text('Unknown label')
    else:
        files_n = len([name for name in os.listdir('./{}'.format(th.training_label))])
        f = open('./{}/{}_0{}.txt'.format(th.training_label, th.training_label, files_n + 1), 'w')
        f.write(th.training_text)
        f.close()
        bayes.train(th.training_text , th.training_label)

    return ConversationHandler.END


@run_async
def test(bot, update):
    update.message.reply_text('Input some text (it must not exceed one Telegram message)'
                              'Now next label are available: news, government, hobbies, reviews')
    return WAITING_FOR_TEST


def test_bayes(bot, update):
    text = update.message.text.lower()
    if len(text) < 500:
        update.message.reply_text('Your text must contain at least 500 characters.\nTry again with /test')
    else:

    #
    # keyboard = [[InlineKeyboardButton("Bayes", callback_data='bayes'),
    #            InlineKeyboardButton("CNN", callback_data='cnn')],
    #           [InlineKeyboardButton("Назад", callback_data='back')]]
    #
    # reply_markup = InlineKeyboardMarkup(keyboard)
    # update.message.reply_text('Please choose:', reply_markup=reply_markup)
        words = text.replace('\n', ' ').split(' ')
        features = bayes.document_features(words)
        label = bayes.classify(features)
        update.message.reply_text('LingvistBot says that this text is about %s' % label)
    return ConversationHandler.END


@run_async
def accuracy(bot, update):
    acc = round(bayes.get_accuracy() * 100, 2)
    update.message.reply_text('Current accuracy: %s percent' % acc)


def button(bot, update):
    query = update.callback_query
    a = query.data
    bot.editMessageText(text="", chat_id=query.message.chat_id, message_id=query.message.message_id)


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))
