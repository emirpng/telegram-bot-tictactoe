from algorithms.nega_scout import get_move

class TicTacToe:
    EMPTY_VALUE = 0
    PLAYER_ONE = 1
    PLAYER_TWO = 2
    WIN_POINTS = 100

    def __init__(self, player_value, board=None, n=3):
        if not board:
            self.board = TicTacToe.get_empty_board(n)
        else:
            self.board = board
        self.n = n
        self.player_value = player_value
        self.current_player_value = player_value

    def possible_moves(self):
        for i, row in enumerate(self.board):
            for j, value in enumerate(row):
                if value == TicTacToe.EMPTY_VALUE:
                    yield i, j

    def make_move(self, move):
        i, j = move
        self.board[i][j] = self.current_player_value

    def unmake_move(self, move):
        i, j = move
        self.board[i][j] = TicTacToe.EMPTY_VALUE

    def is_over(self):
        return not next(self.possible_moves(), None) or \
               any(abs(self.get_line_score(line)) == self.WIN_POINTS
                   for line in self.get_lines())

    def get_lines(self):
        for row in self.board:
            yield row
        for j in range(self.n):
            column = [row[j] for row in self.board]
            yield column
        diagonal = [row[i] for i, row in enumerate(self.board)]
        yield diagonal
        counter_diagonal = [row[-i - 1] for i, row in enumerate(self.board)]
        yield counter_diagonal

    def get_line_score(self, line):
        opponent_points = 0
        player_points = 0
        prev_value = None
        for value in line:
            if value == self.opponent_value:
                if value == prev_value:
                    opponent_points *= 10
                else:
                    opponent_points += 1
            elif value == self.current_player_value:
                if value == prev_value:
                    player_points *= 10
                else:
                    player_points += 1
            prev_value = value
        return player_points - opponent_points

    def get_score(self):
        return sum(self.get_line_score(line) for line in self.get_lines())

    def switch_player(self):
        self.current_player_value = self.opponent_value

    async def make_ai_move(self):
        move = await get_move(self)
        self.make_move(move)

    @classmethod
    def get_empty_board(cls, n):
        return [[cls.EMPTY_VALUE for j in range(n)] for i in range(n)]

    @property
    def opponent_value(self):
        if self.current_player_value == TicTacToe.PLAYER_ONE:
            return TicTacToe.PLAYER_TWO
        return TicTacToe.PLAYER_ONE
