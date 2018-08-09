import json
from aiotg import Bot, Chat

from tic_tac_toe import make_move, get_empty_board
from config import API_TOKEN

bot_server = Bot(api_token=API_TOKEN)

INLINE_KEYBOARD_TYPE = 'InlineKeyboardMarkup'
INLINE_BUTTON_TYPE = 'InlineKeyboardButton'


BOARDS = {}


def get_keyboard(board):
    buttons = [[], [], []]
    move_map = {0: ' ', 1: 'X', 2: 'O'}
    for idx, item in enumerate(board):
        code = f'{idx}'
        mark = move_map[item]
        buttons[idx // 3].append({
            'type': INLINE_BUTTON_TYPE,
            'text': mark,
            'callback_data': code
        })
    markup = {
        'type': INLINE_KEYBOARD_TYPE,
        'inline_keyboard': buttons
    }

    return markup


@bot_server.callback
def handle_move(chat, update):
    query = update.src
    message = query['message']
    chat_id = message['chat']['id']
    message_id =  message['message_id']
    move = int(query['data'])
    try:
        board = BOARDS[chat_id]
    except KeyError:
        return
    board[move] = 1
    board = make_move(board)
    BOARDS[chat_id] = board
    reply_markup = get_keyboard(board)
    chat.bot.edit_message_text(chat_id=chat_id, text='Game',
                           reply_markup=json.dumps(reply_markup),
                           message_id=message_id)


@bot_server.command('/start')
def start(chat: Chat, match):
    empty_board = get_empty_board()
    BOARDS[chat.id] = get_empty_board()
    chat.send_text("Let's the game begin!",
                   reply_markup=json.dumps(get_keyboard(empty_board)))


if __name__ == '__main__':
    bot_server.run()
