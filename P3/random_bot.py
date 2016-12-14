
from random import choice


def think(state):
    """ Returns a random move. """
    return choice(state.legal_moves)
