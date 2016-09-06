#!/usr/bin/env python
import os
import time
import logging
from random import randint

from telegram import Emoji, ForceReply, InlineKeyboardButton, \
            InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from tictactoe import Player, Game


# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

games = dict()


def start(bot, update):
    chat_id = update.message.chat_id
    if chat_id not in games:
        game = Game()
        game.add_player(Player(chat_id))
        game.add_player(Player(0))
        game.start()
        games[chat_id] = game
        reply_markup = get_keyboard(game, False)
        bot.sendMessage(chat_id=chat_id, text="Let's the game begin!",
                        reply_markup=reply_markup)

def get_keyboard(game, won_marks):
    buttons = []
    for i in range(0, 3):
        row = []
        for j in range(0, 3):
            player = game.get_mark(i, j)
            code = str(i) + ',' + str(j)
            mark = ' '
            if player is not None:
                if player == game.get_prev_player() and won_marks and (i, j) in won_marks:
                    mark = player.mark.upper()
                else:
                    mark = player.mark

            row.append(InlineKeyboardButton(mark, callback_data=code))
        buttons.append(row)
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard


def error(bot, update, error):
        logger.warn('Update "%s" caused error "%s"' % (update, error))


def confirm_value(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    user_id = query.from_user.id
    text = query.data
    i, j = text.split(',')
    game = games[chat_id]
    try:
        game.add_mark(chat_id, int(i), int(j))
        won_marks = game.get_won_marks(chat_id)

        if not won_marks and game.next_player.id == 0:
            add_available_mark(game)
            won_marks = game.get_won_marks(0)

        reply_markup = get_keyboard(game, won_marks)
        bot.editMessageText(chat_id=chat_id, text='Game', reply_markup=reply_markup, message_id=query.message.message_id)
        if won_marks or game.get_mark_count() == 9:
            del games[chat_id]
    except Exception as e:
        bot.answerCallbackQuery(query.id, text=str(e))
        raise


def add_available_mark(game):
    for i in range(0, 3):
        for j in range(0, 3):
            player = game.get_mark(i, j)
            if player is None:
                game.add_mark(0, i, j)
                return

    #bot.answerCallbackQuery(query.id, text="Ok!")


TOKEN = os.environ['BATTLESHIP_BOT_TOKEN']


def main():
    updater = Updater(token=TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    #dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CallbackQueryHandler(confirm_value))
    # log all errors
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

def test():
    game = Game()
    game.add_player(Player(15))
    game.add_player(Player(0))
    game.start()
    game.add_mark(15, 0, 0)
    add_available_mark(game)
    game.add_mark(15, 1, 0)
    add_available_mark(game)
    game.add_mark(15, 2, 0)
    print game.get_won_marks(15)


if __name__ == '__main__':
    #test()
    main()
