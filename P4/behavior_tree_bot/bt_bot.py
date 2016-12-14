#bt_bot
#!/usr/bin/env python
#

"""
// The do_turn function is where your code goes. The PlanetWars object contains
// the state of the game, including information about all planets and fleets
// that currently exist.
//
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from timeit import default_timer as time

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check, Repeater, Inverter, Succeeder, RepeatUntilFail

from planet_wars import PlanetWars, finish_turn


def setup_behavior_tree():
    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    offensive_plan = Sequence(name='Offensive Strategy')
    largest_fleet_check = Check(have_largest_fleet)
    no_neutral_check = Check(if_no_neutral_planet_available)
    attack = Action(attack_weakest_enemy_planet)
    offensive_checks = Selector(name='Offensive Check')
    offensive_checks.child_nodes = [largest_fleet_check, no_neutral_check]
    offensive_plan.child_nodes = [offensive_checks, attack]

    spread_sequence = Sequence(name='Spread Strategy')
    neutral_planet_check = Check(if_neutral_planet_available)
    spread_action = Action(spread_to_best_neutral_planet)
    spread_sequence.child_nodes = [neutral_planet_check, spread_action]

    spread_closest = Sequence(name='Spread Closest')
    spread_closest_action = Action(spread_to_closest_weakest_planet)
    spread_closest.child_nodes = [spread_closest_action]

    '''
    pester_plan = Sequence(name='Pester Strategy')
    #pester_repeater = Repeater(name='Pester Repeater')
    have_five_planets_check = Check(have_five_planets)
    pester_action = Action(pester_weakest_enemy_planet)
    #pester_repeater.child_node = pester_action
    pester_plan.child_nodes = [have_five_planets_check, pester_action]
    '''
    
    root.child_nodes = [offensive_plan, spread_closest, spread_sequence]

    logging.info('\n' + root.tree_to_string())
    return root

def do_turn():
    """
    Here is where you have to implement your strategy using the behaviour tree you defined.
    """
    return

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                start = time()
                behavior_tree.execute(planet_wars)
                time_elapsed = time() - start
                logging.info("Time elapsed: " + str(time_elapsed))
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
