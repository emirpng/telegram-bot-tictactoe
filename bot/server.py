import json
from aiotg import Bot, Chat

from game.tic_tac_toe import TicTacToe
from config import API_TOKEN

bot_server = Bot(api_token=API_TOKEN)

INLINE_KEYBOARD_TYPE = 'InlineKeyboardMarkup'
INLINE_BUTTON_TYPE = 'InlineKeyboardButton'


def dump_board(board):
    return ''.join(str(value) for row in board for value in row)


def dump_cell_coord(i, j):
    return f'{i},{j}'


def parse_callback(data):
    player_value, board_dump, coord_dump = data.split(':')
    n = int(len(board_dump) ** 0.5)
    board = []
    str_index = 0
    for i in range(n):
        board.append([])
        for j in range(n):
            board[i].append(int(board_dump[str_index]))
            str_index += 1

    i, j = (int(coord) for coord in coord_dump.split(','))
    return int(player_value), board, (i, j)



def get_keyboard(game):
    board = game.board
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
                'callback_data': f'{game.player_value}:'
                                 f'{board_dump}:{cell_coord_dump}',
            })
        buttons.append(row_buttons)
    markup = {
        'type': INLINE_KEYBOARD_TYPE,
        'inline_keyboard': buttons
    }

    return markup


def get_choose_player_keyboard():
    buttons = [
        {
            'type': INLINE_BUTTON_TYPE,
            'text': 'As Player 1',
            'callback_data': TicTacToe.PLAYER_ONE,
        },
        {
            'type': INLINE_BUTTON_TYPE,
            'text': 'As Player 2',
            'callback_data': TicTacToe.PLAYER_TWO,
        }
    ]
    markup = {
        'type': INLINE_KEYBOARD_TYPE,
        'inline_keyboard': [buttons],
    }
    return markup


@bot_server.callback
async def handle_callback(chat, update):
    query = update.src
    message = query['message']
    chat_id = message['chat']['id']
    message_id =  message['message_id']
    data = query['data']
    if len(data) == 1:
        human_as_player_two = False
        if int(data) == TicTacToe.PLAYER_TWO:
            human_as_player_two = True
        reply_markup = await first_move(human_as_player_two)
    else:
        reply_markup = await handle_move(data)

    chat.bot.edit_message_text(chat_id=chat_id, text='Game',
                           reply_markup=json.dumps(reply_markup),
                           message_id=message_id)


async def handle_move(data):
    player_value, board, (i, j) = parse_callback(data)
    game = TicTacToe(player_value, board)
    game.make_move((i, j))
    game.switch_player()
    if not game.is_over():
        await game.make_ai_move()
    reply_markup = get_keyboard(game)
    return reply_markup


async def first_move(human_as_player_two):
    if human_as_player_two:
        player_value = TicTacToe.PLAYER_TWO
        game = TicTacToe(player_value)
        game.switch_player()
        await game.make_ai_move()
    else:
        player_value = TicTacToe.PLAYER_ONE
        game = TicTacToe(player_value)
    reply_markup = get_keyboard(game)
    return reply_markup


@bot_server.command('/start')
def start(chat: Chat, match):
    chat.send_text("Choose player number",
                   reply_markup=json.dumps(get_choose_player_keyboard()))

