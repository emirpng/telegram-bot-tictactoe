__all__ = ['make_move']

from easyAI import Negamax, TwoPlayersGame

class TicTacToe(TwoPlayersGame):
    """ The board positions are numbered as follows:
            7 8 9
            4 5 6
            1 2 3
    """

    def __init__(self, board=None, n=3):
        if not board:
            self.board = TicTacToe.get_empty_board(n)
        else:
            self.board = board
        self.n = n
        self.nplayer = 2 # player 1 starts.

    def possible_moves(self):
        return [(i, j) for i, row in enumerate(self.board)
                for j, value in enumerate(row) if value == 0]

    def make_move(self, move):
        i, j = move
        self.board[i][j] = self.nplayer

    def unmake_move(self, move):  # optional method (speeds up the AI)
        i, j = move
        self.board[i][j] = 0

    def lose(self):
        for row in self.board:
            if all(value == self.nopponent for value in row):
                return True
        for j in range(self.n):
            column = [row[j] for row in self.board]
            if all(value == self.nopponent for value in column):
                return True

        diagonal = [row[i] for i, row in enumerate(self.board)]
        if all(value == self.nopponent for value in diagonal):
            return True

        counter_diagonal = [row[-i - 1] for i, row in enumerate(self.board)]
        if all(value == self.nopponent for value in counter_diagonal):
            return True
        return False

    def is_over(self):
        return not self.possible_moves() or self.lose()

    def show(self):
        pass

    def scoring(self):
        return -100 if self.lose() else 0

    @staticmethod
    def get_empty_board(n):
        return [[0 for j in range(n)] for i in range(n)]

def make_move(board):
    ai_algorithm = Negamax(6)
    game = TicTacToe(board)
    if not game.is_over():
        move = ai_algorithm(game)
        game.make_move(move)
    return game.board
