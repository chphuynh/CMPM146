
from collections import namedtuple, Counter

# As Game does not require any inner manipulation of variables, we can use a namedtuple
# rather than defining a full class.
Game = namedtuple('Game', ['width', 'players', 'dots', 'boxes', 'h_lines', 'v_lines'])


def create_game(width):
    players = ('red', 'blue')  # These must be valid tkinter color names.
    dots = frozenset((i, j) for i in range(width) for j in range(width))
    boxes = frozenset((i, j) for i in range(width - 1) for j in range(width - 1))
    h_lines = frozenset((i, j) for i in range(width - 1) for j in range(width))
    v_lines = frozenset((i, j) for i in range(width) for j in range(width - 1))

    return Game(width, players, dots, boxes, h_lines, v_lines)


class State:
    def __init__(self, game):
        self.game = game
        self.player_turn = game.players[0]
        self.box_owners = {}
        self.h_line_owners = {}
        self.v_line_owners = {}

    def copy(self):
        res = State(self.game)
        res.player_turn = self.player_turn
        res.box_owners = self.box_owners.copy()
        res.h_line_owners = self.h_line_owners.copy()
        res.v_line_owners = self.v_line_owners.copy()
        return res

    def apply_move(self, move):

        orientation, cell = move
        x,y = cell

        if orientation == 'h':
            self.h_line_owners[cell] = self.player_turn
            box_checks = [(x, y-1), (x,y)]
        elif orientation == 'v':
            self.v_line_owners[cell] = self.player_turn
            box_checks = [(x-1, y), (x,y)]

        new_boxes = False
        for box in box_checks:
            (i,j) = box
            if (i, j) not in self.box_owners \
                    and (i, j) in self.h_line_owners \
                    and (i, j) in self.v_line_owners \
                    and (i, j + 1) in self.h_line_owners \
                    and (i + 1, j) in self.v_line_owners:
                new_boxes = True
                self.box_owners[box] = self.player_turn

        if not new_boxes:
            self.player_turn = self.game.players[(self.game.players.index(self.player_turn) + 1) % len(self.game.players)]

    def is_terminal(self):
        return len(self.box_owners) == len(self.game.boxes)
        #return any(score > len(self.game.boxes)/2 for score in self.score.values())

    @property
    def legal_moves(self):
        h_moves = [('h', h) for h in self.game.h_lines if h not in self.h_line_owners]
        v_moves = [('v', v) for v in self.game.v_lines if v not in self.v_line_owners]
        return h_moves + v_moves


    @property
    def score(self):
        return dict(Counter(self.box_owners.values()))

    @property
    def winner(self):
        if len(self.score) == 0:
            return 'tie'
        player, winning_score = max(self.score.items(), key=lambda pair: pair[1])
        if winning_score == len(self.game.boxes)/2:
            return 'tie'
        else:
            return player

