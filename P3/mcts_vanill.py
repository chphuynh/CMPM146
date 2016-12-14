
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

def traverse_nodes(node, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    if not node.child_nodes:
        node.visits = node.visits + 1
        return node

    bound = None
    selected_child = None
    #selected_child_state = None
    for child in node.child_nodes:
        child = node.child_nodes[child]
        child_bound = child.wins + explore_faction * (sqrt(2*log(node.visits) / (child.visits)))
        if bound is None or child_bound < bound:
            bound = child_bound
            selected_child = child

    #selected_child_state = state.copy()
    state.apply_move(selected_child.parent_action)
            
    return traverse_nodes(selected_child, state, state.player_turn)
    
    # Hint: return leaf_node


def expand_leaf(node, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        state:  The state of the game.

    Returns:    The added child node.

    """
    new_state = state.copy()
    new_move = choice(node.untried_actions)
    new_state.apply_move(new_move)
    new_node = MCTSNode(parent=node, parent_action=new_move, action_list=new_state.legal_moves)
    return new_node
    # Hint: return new_node


def rollout(state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        state:  The state of the game.

    """
    while(state.legal_moves):
        state.apply_move(choice(state.legal_moves))


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    if node.parent == None:
        return
    if won:
        node.wins = node.wins + 1
    node.visits = node.visits + 1

    backpropagate(node.parent, won)


def think(state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = state.player_turn
    root_node = MCTSNode(parent=None, parent_action=None, action_list=state.legal_moves)

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state.copy()

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        node = traverse_nodes(node, sampled_game, identity_of_bot)
        node = expand_leaf(node, sampled_game)
        rollout(sampled_game)
        backpropagate(node, sampled_game.winner == identity_of_bot)
        
    highscore=-1
    bestAction = None
    for child in root_node.child_nodes:
        child = root_node.child_nodes[child]
        if child.wins/child.visits > highscore:
            highscore = child.wins/child.visits
            bestAction = child.parent_action

    
    return bestAction           

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    
