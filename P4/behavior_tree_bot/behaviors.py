#behaviors
import sys, logging
sys.path.insert(0, '../')
from planet_wars import issue_order
from random import choice
from math import sqrt, ceil

def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    #if len(state.my_fleets()) >= 1:
        #return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    #if len(state.my_fleets()) >= 1:
    #   return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, weakest_planet.growth_rate + 1)
      
#Want a distance formula, tracker of how many of our forces going where, growth rate tracker
      

#Sort by lowest distance to target planet
def distance(source, destination):
  dx = source.x - destination.x
  dy = source.y - destination.y
  return int(ceil(sqrt(dx * dx + dy * dy)))
  
#Not accounting for distance yet
def spread_to_best_neutral_planet(state):
#  my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships * (1 + 1/p.growth_rate)))

  neutral_planets = [planet for planet in state.neutral_planets()
                     if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
  neutral_planets.sort(key=lambda p: p.num_ships * (1 + 1/p.growth_rate))
  target_planets = iter(neutral_planets)

  try:
      while True:
        target_planet = next(target_planets)
        i = 0
        my_empire = state.my_planets()
        my_empire.sort(key=lambda p: p.num_ships * (1 + 1/p.growth_rate))
        my_top_5 = []
        top_5_ships_available = 0
        while i < 5 and i < len(my_empire):
            my_top_5.append(my_empire[i])
            top_5_ships_available += my_empire[i].num_ships*(1/3) #1/3 of the number of ships from our closest best 5 planets
            i+=1
#            logging.info(i)
        my_top_5.sort(key=lambda p: distance(p, target_planet))
        my_planets = iter(my_top_5)
        my_planet = next(my_planets)
        required_ships = target_planet.num_ships + 5
        j=0
        forces_sent = 0
 
        while j < 5 and j < len(state.my_planets()):
          if top_5_ships_available > required_ships:
            while forces_sent != required_ships and my_planet.num_ships *(2/3) >= 25:
              regiment = my_planet.num_ships * (1/3)
              forces_sent += regiment
              issue_order(state, my_planet.ID, target_planet.ID, regiment)
              my_planet = next(my_planets)
          j+=1


  except StopIteration:
      return False

               
def pester_weakest_enemy_planet(state):
    #Randomly choose a planet
    if len(state.my_planets()) >= 1:
        planet = choice(state.my_planets())
    else:
        return False
    #Find weakest enemy planet
    weakest_planet = min(state.enemy_planets(), key=lambda p: p.num_ships, default=None)
    #Send a random number of ships that does not exceed growth rate
    #ships = choice(range(1, planet.growth_rate - 1))
    if not planet or not weakest_planet:
    #No legal source or destination
        return False
    else:
        return issue_order(state, planet.ID, weakest_planet.ID, max(1,planet.growth_rate - 1))


def spread_to_closest_weakest_planet(state):

    if len(state.my_planets()) >= 1:
        strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    else:
        return False
    
    closest_weak_planet = None
    closest_weak_distance = 999999
    
    for planet in state.not_my_planets():
        dist = distance(strongest_planet, planet) + planet.num_ships

        if dist < closest_weak_distance:
            closest_weak_distance = dist
            closest_weak_planet = planet

    if strongest_planet.num_ships > closest_weak_planet.num_ships + 20:
        issue_order(state, strongest_planet.ID, closest_weak_planet.ID, closest_weak_planet.num_ships + 20)
    return False
