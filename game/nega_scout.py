import asyncio

from config import DEPTH


async def _nega_scout(game, depth, alpha, beta):
    if depth == 0 or game.is_over():
        return game.get_score()

    possible_moves = game.possible_moves()
    result_move = None
    if depth == DEPTH:
        result_move = next(game.possible_moves())
    best_value = -float('inf')

    for move in possible_moves:
        await asyncio.sleep(0)
        game.make_move(move)
        game.switch_player()
        move_alpha = - await _nega_scout(game, depth - 1, -beta, -alpha)
        game.switch_player()
        game.unmake_move(move)

        best_value = max(best_value, move_alpha)
        if  alpha < move_alpha:
            alpha = move_alpha
            if depth == DEPTH:
                result_move = move
            if alpha >= beta:
                break

    return result_move or best_value


async def get_move(game):
    move = await _nega_scout(game, DEPTH, -float('inf'), float('inf'))
    return move
