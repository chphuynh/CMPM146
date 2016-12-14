
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

    highscore=0
    best=node

    #Go through all child nodes of selected node
    for x in node.child_nodes:
        temp=node.child_nodes[x]

        #Uses Upper Confidence Bound to find best node
        if temp.visits!=0:
            score=(temp.wins/temp.visits) + explore_faction*sqrt(2*log(node.visits)/temp.visits)
        else:
            score=0
        #If Upper Confidence Bound is highest, set it to selected node.
        if score>highscore:
            highscore=score
            best=temp
    
    return best 
    
     
def expand_leaf(node, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        state:  The state of the game.

    Returns:    The added child node.

    """
    #Chooses a random move from the action list
    new_state = state.copy()
    new_move = choice(node.untried_actions)
    new_state.apply_move(new_move)
    
    #Creates new node with selected move
    new_node = MCTSNode(parent=node, parent_action=new_move, action_list=new_state.legal_moves)
    node.child_nodes[new_move] = new_node
    return new_node
    


def rollout(state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        state:  The state of the game.

    """

    #Plays through the game choosing a random choice
    me = state.player_turn
    while(state.legal_moves!=[]):
        current_score = state.score.get(me,0)
        move = choice(state.legal_moves)

        #Applies move to cloned state
        rollout_state = state.copy()
        rollout_state.apply_move(move)

        #If move profits the bot, apply move
        if rollout_state.score.get(me, 0) > current_score:
            state.apply_move(move)
        #Else make another random choice and apply
        else:
            move = choice(state.legal_moves)
            state.apply_move(move)
        
    


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    #Returns from leaf node through root
    current_node = node
    while current_node != None:
        if won:
            current_node.wins+=1
        current_node.visits+=1
        #repeats loop with parent
        current_node =current_node.parent    
    
    
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

        #Selection
        while node.untried_actions==[] and node.child_nodes!={}:
            node.visits+=1
            node=traverse_nodes(node,sampled_game,identity_of_bot)
            if node.parent_action!=None:
                sampled_game.apply_move(node.parent_action)

        #Expansion     
        if ( node.untried_actions !=[]):      
            node=expand_leaf(node,sampled_game)
            node=traverse_nodes(node,sampled_game,identity_of_bot)
            sampled_game.apply_move(node.parent_action)

        #Simulation
        rollout(sampled_game)
        if sampled_game.winner == identity_of_bot:
            vic=True
        else:
            vic=False

        #Backpropogate
        backpropagate(node,vic)
    
    #find the best action
    highscore=-1
    for x in root_node.child_nodes:
        temp=root_node.child_nodes[x]
        if ((temp.wins/temp.visits)>highscore) and x!=None:
            highscore=(temp.wins/temp.visits)
            bestAction=x

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    print("Modified bot picking %s with expected score %f" % (str(bestAction), highscore))
    return bestAction        
    
