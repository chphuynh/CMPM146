import random

ROLLOUTS = 10
MAX_DEPTH = 5


def think(state):
    """ For each possible move, this bot plays ROLLOUTS random games to depth MAX_DEPTH then averages the
    score as an estimate of how good the move is.

    Args:
        state:  The state of the game.

    Returns:    The action with the maximal score given the rollouts.

    """
    moves = state.legal_moves

    best_move = moves[0]
    best_expectation = float('-inf')

    me = state.player_turn

    # Define a helper function to calculate the difference between the bot's score and the opponent's.
    def outcome(score):
        red_score = score.get('red', 0)
        blue_score = score.get('blue', 0)
        return red_score - blue_score if me == 'red' else blue_score - red_score

    for move in moves:
        total_score = 0.0

        # Sample a set number of games where the target move is immediately applied.
        for r in range(ROLLOUTS):
            rollout_state = state.copy()
            rollout_state.apply_move(move)

            # Only play to the specified depth.
            for i in range(MAX_DEPTH):
                if rollout_state.is_terminal():
                    break
                rollout_move = random.choice(rollout_state.legal_moves)
                rollout_state.apply_move(rollout_move)

            total_score += outcome(rollout_state.score)

        expectation = float(total_score) / ROLLOUTS

        # If the current move has a better average score, replace best_move and best_expectation
        if expectation > best_expectation:
            best_expectation = expectation
            best_move = move

    print("Rollout bot picking %s with expected score %f" % (str(best_move), best_expectation))
    return best_move
