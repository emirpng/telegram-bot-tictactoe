import json
from aiotg import Bot, Chat

from tic_tac_toe import TicTacToe
from config import API_TOKEN

bot_server = Bot(api_token=API_TOKEN)

INLINE_KEYBOARD_TYPE = 'InlineKeyboardMarkup'
INLINE_BUTTON_TYPE = 'InlineKeyboardButton'


def dump_board(board):
    return ''.join(str(value) for row in board for value in row)


def dump_cell_coord(i, j):
    return f'{i},{j}'


def parse_callback(data):
    board_dump, coord_dump = data.split(':')
    n = int(len(board_dump) ** 0.5)
    board = []
    str_index = 0
    for i in range(n):
        board.append([])
        for j in range(n):
            board[i].append(int(board_dump[str_index]))
            str_index += 1

    i, j = (int(coord) for coord in coord_dump.split(','))
    return board, (i, j)



def get_keyboard(board):
    buttons = []
    move_map = {
        TicTacToe.EMPTY_VALUE: ' ',
        TicTacToe.PLAYER_ONE: 'X',
        TicTacToe.PLAYER_TWO: 'O',
    }
    board_dump = dump_board(board)
    for i, row in enumerate(board):
        row_buttons = []
        for j, value in enumerate(row):
            cell_coord_dump = dump_cell_coord(i, j)
            mark = move_map[value]
            row_buttons.append({
                'type': INLINE_BUTTON_TYPE,
                'text': mark,
                'callback_data': f'{board_dump}:{cell_coord_dump}',
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
    board, (i, j) = parse_callback(query['data'])
    board[i][j] = TicTacToe.PLAYER_ONE
    game = TicTacToe(board)
    if not game.is_over():
        await game.make_ai_move()
    reply_markup = get_keyboard(board)
    chat.bot.edit_message_text(chat_id=chat_id, text='Game',
                           reply_markup=json.dumps(reply_markup),
                           message_id=message_id)


@bot_server.command('/start')
def start(chat: Chat, match):
    game = TicTacToe()
    chat.send_text("Let's the game begin!",
                   reply_markup=json.dumps(get_keyboard(game.board)))


if __name__ == '__main__':
    bot_server.run()
