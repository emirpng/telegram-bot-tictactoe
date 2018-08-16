import json
from aiotg import Bot, Chat

from tic_tac_toe import TicTacToe
from config import API_TOKEN

bot_server = Bot(api_token=API_TOKEN)

INLINE_KEYBOARD_TYPE = 'InlineKeyboardMarkup'
INLINE_BUTTON_TYPE = 'InlineKeyboardButton'


BOARDS = {}


def get_keyboard(board):
    buttons = []
    move_map = {
        TicTacToe.EMPTY_VALUE:' ',
        TicTacToe.PLAYER_ONE: 'X',
        TicTacToe.PLAYER_TWO: 'O'}
    for i, row in enumerate(board):
        row_buttons = []
        for j, value in enumerate(row):
            mark = move_map[value]
            row_buttons.append({
                'type': INLINE_BUTTON_TYPE,
                'text': mark,
                'callback_data': f'{i},{j}',
            })
        buttons.append(row_buttons)
    markup = {
        'type': INLINE_KEYBOARD_TYPE,
        'inline_keyboard': buttons
    }

    return markup


@bot_server.callback
async def handle_move(chat, update):
    query = update.src
    message = query['message']
    chat_id = message['chat']['id']
    message_id =  message['message_id']
    i, j = (int(coord) for coord in query['data'].split(','))
    try:
        board = BOARDS[chat_id]
    except KeyError:
        return
    board[i][j] = TicTacToe.PLAYER_ONE
    game = TicTacToe(board)
    if not game.is_over():
        await game.make_ai_move()
    BOARDS[chat_id] = board
    reply_markup = get_keyboard(board)
    chat.bot.edit_message_text(chat_id=chat_id, text='Game',
                           reply_markup=json.dumps(reply_markup),
                           message_id=message_id)


@bot_server.command('/start')
def start(chat: Chat, match):
    game = TicTacToe()
    BOARDS[chat.id] = game.board
    chat.send_text("Let's the game begin!",
                   reply_markup=json.dumps(get_keyboard(game.board)))


if __name__ == '__main__':
    bot_server.run()
