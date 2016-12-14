import math
from random import random, randint

class Individual:
    def __init__(self):
        self.danger = random()*random()*.99 + 1
        self.bomb_one = random()*random()
        self.bomb_two = random()*random()
        self.bomb_three = random()*random()
        self.movement_one = random()*random()
        self.movement_two = random()*random()
        self.bomb_throw = random()*random()*20 - 20

    @classmethod
    def modify(cls, mod):
        new = cls()
        new.danger = mod[0]
        new.bomb_one = mod[1]
        new.bomb_two = mod[2]
        new.bomb_three = mod[3]
        new.movement_one = mod[4]
        new.movement_two = mod[5]
        new.bomb_throw = mod[6]
        return new
    
    def generate_mod(self):
        mod = [self.danger, self.bomb_one, self.bomb_two, \
               self.bomb_three, self.movement_one, self.movement_two, \
               self.bomb_throw]

        return mod

    def print_details(self):
        print('Danger = ' + str(self.danger))
        print('Bomb_one = ' + str(self.bomb_one))
        print('Bomb_two = ' + str(self.bomb_two))
        print('Bomb_three = ' + str(self.bomb_three))
        print('Movement_one = ' + str(self.movement_one))
        print('Movement_two = ' + str(self.movement_two))
        print('Bomb_throw = ' + str(self.bomb_throw))


class Population:
    def __init__(self, pop_count):
        self.ai_list = []
        
        for i in range(pop_count):
            self.ai_list.append(Individual())

    def generate_mods(self):
        mods = []

        for i in range(len(self.ai_list)):
            mods.append(self.ai_list[i].generate_mod())

        return mods
    
    def print(self):
        for i in range(len(self.ai_list)):
            print('AI number: ' + str(i))
            self.ai_list[i].print_details()

class Data:
    def __init__(self):
        self.time_alive = None
        self.ai_number = None

#Functions for genetic algorithm
def fitness(ai_data):
    winners = []

    alive_ai = sorted(ai_data, key=lambda ai: ai.time_alive, reverse=True)
        
    winners = alive_ai[:3]

    for i in range(3):
        winners[i] = alive_ai[i].ai_number
    
    return winners

def crossover(winners, population):
    pop_mods = population.generate_mods()

    winner_list = [pop_mods[winners[0]], pop_mods[winners[1]], pop_mods[winners[2]]]
    
    new_pop = Population(len(pop_mods))

    for i in range(len(pop_mods)):
        new_mod = []
        crossover_index = randint(0, len(pop_mods[0]))
        first = randint(0, 2)
        second = 2 - first
    
        first_winner = winner_list[first]
        second_winner = winner_list[second]

        for j in range(len(first_winner)):
            if j < crossover_index:
                new_mod.append(first_winner[j])
            else:
                new_mod.append(second_winner[j])

        new_pop.ai_list[i] = Individual().modify(new_mod)

    return new_pop

