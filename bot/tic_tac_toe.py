__all__ = ['get_empty_board', 'make_move']

from easyAI import Negamax, TwoPlayersGame

class TicTacToe(TwoPlayersGame):
    """ The board positions are numbered as follows:
            7 8 9
            4 5 6
            1 2 3
    """

    def __init__(self, board=None):
        if not board:
            self.board = TicTacToe.get_empty_board()
        else:
            self.board = board
        self.nplayer = 2 # player 1 starts.

    def possible_moves(self):
        return [i + 1 for i, e in enumerate(self.board) if e == 0]

    def make_move(self, move):
        self.board[int(move) - 1] = self.nplayer

    def unmake_move(self, move):  # optional method (speeds up the AI)
        self.board[int(move) - 1] = 0

    def lose(self):
        """ Has the opponent "three in line ?" """
        return any([all([(self.board[c - 1] == self.nopponent)
                         for c in line])
                    for line in [[1, 2, 3], [4, 5, 6], [7, 8, 9],  # horiz.
                                 [1, 4, 7], [2, 5, 8], [3, 6, 9],  # vertical
                                 [1, 5, 9], [3, 5, 7]]])  # diagonal

    def is_over(self):
        return not self.possible_moves() or self.lose()

    def show(self):
        pass

    def scoring(self):
        return -100 if self.lose() else 0

    @staticmethod
    def get_empty_board():
        return [0 for i in range(9)]


def get_empty_board():
    return TicTacToe.get_empty_board()


def make_move(board):
    ai_algorithm = Negamax(6)
    game = TicTacToe(board)
    if not game.is_over():
        move = ai_algorithm(game)
        game.make_move(move)
    return game.board
