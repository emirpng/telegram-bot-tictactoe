from itertools import groupby, cycle
from random import shuffle

class MarkType:
    X = 'x'
    O = 'o'

class Player(object):
    def __init__(self, id, mark=None):
        self.id = id
        self.mark = mark

    def __eq__(self, other):
        return self.id == other.id

class Game(object):
    def __init__(self):
        self.players = []
        self.marks = dict()
        self.players_iter = None
        self.prev_player = None
        self.next_player = None

    def add_player(self, player):
        self.players.append(player)

    def start(self):
        self.players_iter = cycle(self.players)
        self.shift()
        marks = [MarkType.X, MarkType.O]
        shuffle(marks)
        for i, mark in enumerate(marks):
            self.players[i].mark = mark

    def get_prev_player(self):
        return self.prev_player

    def get_next_player(self):
        return self.next_player

    def shift(self):
        self.prev_player = self.next_player
        self.next_player = self.players_iter.next()

    def add_mark(self, player_id, i, j):
        if self.get_next_player().id != player_id:
            raise Exception("Wait for your turn")
        key = (i, j)
        if key in self.marks:
            raise Exception("Mark already exists")
        self.marks[key] = self.get_next_player()
        self.shift()

    def get_mark(self, i, j):
        return self.marks.get((i, j))

    def get_mark_count(self):
        return len(self.marks)
    
    def get_status(self):
        if self.check_if_win(1):
            return 1
        if self.check_if_win(2):
            return 2
        return 0

    def get_player_marks(self, player_id):
        player_marks = {key:mark for key, mark in self.marks.iteritems() if (mark.id
                                                == player_id)}
        return player_marks

    def get_player_mark_type(self, player_id):
        return [player for player in self.players if player.id == player_id][0].mark

    def get_won_marks(self, player_id):
        count = 3
        p_marks = self.get_player_marks(player_id)

        won_marks = (self.get_vertical(p_marks)
                    or self.get_horizontal(p_marks)
                    or self.get_major_diagonal(p_marks)
                    or self.get_minor_diagonal(p_marks))
        return won_marks

    def get_vertical(self, p_marks):
        for key, group in groupby([k for k in p_marks], lambda m:list(m)[1]):
            marks = list(group)
            if len(marks) == 3:
                return marks
        return None

    def get_horizontal(self, p_marks):
        for key, group in groupby([k for k in p_marks], lambda m:list(m)[0]):
            marks = list(group)
            if len(marks) == 3:
                return marks
        return None


    def get_major_diagonal(self, p_marks):
        marks = [mark for mark in p_marks if list(mark)[0] == list(mark)[1]]
        if len(marks) == 3:
            return marks
        return None

    def get_minor_diagonal(self, p_marks):
        count = 3
        marks = [m for m in p_marks if (count - 1) -  list(m)[0] == list(m)[1]]
        if len(marks) == 3:
            return marks
        return None

