import json
from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time
from heapq import heappop, heappush
from math import inf

Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])


class State(OrderedDict):
    """ This class is a thin wrapper around an OrderedDict, which is simply a dictionary which keeps the order in
        which elements are added (for consistent key-value pair comparisons). Here, we have provided functionality
        for hashing, should you need to use a state as a key in another dictionary, e.g. distance[state] = 5. By
        default, dictionaries are not hashable. Additionally, when the state is converted to a string, it removes
        all items with quantity 0.

        Use of this state representation is optional, should you prefer another.
    """

    def __key(self):
        return tuple(self.items())

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.__key() < other.__key()

    def copy(self):
        new_state = State()
        new_state.update(self)
        return new_state

    def __str__(self):
        return str(dict(item for item in self.items() if item[1] > 0))


def make_checker(rule):
    # Implement a function that returns a function to determine whether a state meets a
    # rule's requirements. This code runs once, when the rules are constructed before
    # the search is attempted.

    def check(state):
        # This code is called by graph(state) and runs millions of times.
        # Tip: Do something with rule['Consumes'] and rule['Requires'].       

        if 'Consumes' in rule:
            for item in rule['Consumes']:
                item_cost = rule['Consumes'][item]
                if not state[item] >= item_cost:
                    return False
        if 'Requires' in rule:
            for item in rule['Requires']:
                if not state[item] > 0:
                    return False
        
        return True

    return check


def make_effector(rule):
    # Implement a function that returns a function which transitions from state to
    # new_state given the rule. This code runs once, when the rules are constructed
    # before the search is attempted.

    def effect(state):
        # This code is called by graph(state) and runs millions of times
        # Tip: Do something with rule['Produces'] and rule['Consumes'].
        next_state = state.copy()

        if 'Produces' in rule:
            for item in rule['Produces']:
                next_state[item] = next_state[item] + rule['Produces'][item]

        if 'Consumes' in rule:
            for item in rule['Consumes']:
                next_state[item] = next_state[item] - rule['Consumes'][item]
        
        return next_state

    return effect


def make_goal_checker(goal):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.

    def is_goal(state):
        # This code is used in the search process and may be called millions of times.

        for item in goal:
            if not state[item] >= goal[item]:
                return False
            
        return True

    return is_goal


def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)


def heuristic(state, action, prev_state, total_list):
    # Implement your heuristic here!
    tools = ['bench', 'wooden_pickaxe', 'wooden_axe', 'stone_axe', 'stone_pickaxe', 'iron_pickaxe', 'iron_axe', 'furnace']
    priority = 0
    cur_state = state.copy()
    
    for tool in tools:
        if state[tool] > 1:
            return inf
        elif tool in action:
            return 0

    for item in total_list:
        if cur_state[item] > total_list[item]:
            return inf

    if state['iron_pickaxe'] == 1:
        if 'stone_pickaxe' in action or 'wooden_pickaxe' in action:
            return inf
    elif state['stone_pickaxe'] == 1:
        if 'wooden_pickaxe' in action:
            return inf
        
    if state['iron_axe'] == 1:
        if 'stone_axe' in action or 'wooden_axe' in action:
            return inf
    elif state['stone_pickaxe'] == 1:
        if 'wooden_axe' in action:
            return inf
        
    for item in prev_state:
        cur_state[item] += prev_state[item]

    for item in total_list:
        priority += cur_state[item]

    return priority

def get_total_list(goal):
    things_needed = State({key: 0 for key in Crafting['Items']})
    tools = ['bench', 'wooden_pickaxe', 'wooden_axe', 'stone_axe', 'stone_pickaxe', 'iron_pickaxe', 'iron_axe', 'furnace']

    queue = []

    for item in goal:
        queue.append((item, goal[item]))

    while queue:
        item, amount = queue.pop()

        if item in tools:
            things_needed[item] = 1
        else:
            things_needed[item] += amount

        for action in Crafting['Recipes']:
            if item in Crafting['Recipes'][action]['Produces']:
                if 'Consumes' in Crafting['Recipes'][action]:
                    for consumable in Crafting['Recipes'][action]['Consumes']:
                        queue.append((consumable, Crafting['Recipes'][action]['Consumes'][consumable]))
                if 'Requires' in Crafting['Recipes'][action]:
                    for requireable in Crafting['Recipes'][action]['Requires']:
                        if things_needed[requireable] == 0:
                            queue.append((requireable, 1))
                
    return things_needed

def search(graph, state, is_goal, limit, heuristic):

    goal_list = get_total_list(Crafting['Goal'])
    print(goal_list)
    start_time = time()
    queue = [(0, state)]
    cost = {}
    cost[state] = 0
    backpointers = {}
    backpointers[state] = None
    actions = {}
    actions[state] = None
    visited_states = set()
    visited_states.add(state)
    
    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state
    while time() - start_time < limit:
        current_cost, current_state = heappop(queue)

        if is_goal(current_state):
            path = [(current_state, actions[current_state])]

            current_back_state = backpointers[current_state]
            while current_back_state is not None:
                path.insert(0,(current_back_state, actions[current_back_state]))
                current_back_state = backpointers[current_back_state]
            print('states visited: ' + str(len(visited_states)))
            print(time() - start_time, "seconds.")
            return path

        for adj_action, adj_state, adj_cost in graph(current_state):
            total_cost = current_cost + adj_cost + heuristic(adj_state, adj_action, current_state, goal_list)
            
            if (adj_state not in cost or total_cost < cost[adj_state]) and adj_state not in visited_states:
                cost[adj_state] =  total_cost
                backpointers[adj_state] = current_state
                actions[adj_state] = adj_action
                visited_states.add(adj_state)
                heappush(queue, (total_cost, adj_state))
            
    # Failed to find a path
    print(queue[0])
    print(actions[queue[0][1]])
    print(time() - start_time, 'seconds.')
    print("Failed to find a path from", state, 'within time limit.')
    return None

if __name__ == '__main__':
    with open('Crafting.json') as f:
        Crafting = json.load(f)

    # List of items that can be in your inventory:
    print('All items:', Crafting['Items'])

    # List of items in your initial inventory with amounts:
    print('Initial inventory:', Crafting['Initial'])

    # List of items needed to be in your inventory at the end of the plan:
    print('Goal:',Crafting['Goal'])

    # Dict of crafting recipes (each is a dict):
    print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

    # Build rules
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)

    # Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])

    # Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})
    state.update(Crafting['Initial'])
    
    # Search for a solution
    resulting_plan = search(graph, state, is_goal, 30, heuristic)

    if resulting_plan:
        # Print resulting plan
        cost = 0
        for state, action in resulting_plan:
            if action:
                cost += Crafting['Recipes'][action]['Time']
            print('\t',state)
            print(action)
        print('[cost=' + str(cost) + ', len=' + str(len(resulting_plan)-1) + ']')
