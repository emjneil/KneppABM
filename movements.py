import random 
import math
from random import choice as rchoice


def eat_saplings(habitat_patch, eatenSaps):
    habitat_patch.edibles["saplings"] -= eatenSaps

def eat_trees(habitat_patch, eatenTrees):
    habitat_patch.edibles["trees"] -= eatenTrees
    return eatenTrees

def eat_scrub(habitat_patch, eatenScrub):
    habitat_patch.edibles["scrub"] -= eatenScrub

def eat_youngscrub(habitat_patch, eatenYoungScrub):
    habitat_patch.edibles["youngScrub"] -= eatenYoungScrub

def eat_grass(habitat_patch, eatenGrass):
    habitat_patch.edibles["grass"] -= eatenGrass
    habitat_patch.edibles["bare_ground"] += eatenGrass

def eat_habitats(self, habitat_patch, gain_from_saplings, gain_from_trees, gain_from_scrub, gain_from_young_scrub, gain_from_grass):
    habitat_choices = ["saplings", "trees", "scrub", "youngScrub", "grass"]
    # reset count eaten
    self.count_eaten.clear()

    # pick a habitat type and eat it 
    for _ in range(len(habitat_choices)):
        if self.energy < 1:
            # pick a habitat type
            my_choice = rchoice(habitat_choices)
            habitat_choices.remove(my_choice)
            # if my energy is low enough, eat it 
            if my_choice == "saplings":
                eatenSaps = math.ceil((1-self.energy)/gain_from_saplings)
                # scrub facilitates saplings by preventing herbivory
                if eatenSaps >= habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800))):
                    eatenSaps = habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800)))
                eat_saplings(habitat_patch, eatenSaps)
                self.energy += (gain_from_saplings * eatenSaps)
                self.count_eaten[my_choice] += eatenSaps
            elif my_choice == "trees":
                eatenTrees = math.ceil((1-self.energy)/gain_from_trees)
                if eatenTrees >= habitat_patch.edibles["trees"]:
                    eatenTrees = habitat_patch.edibles["trees"]
                self.energy += (gain_from_trees * eatenTrees)
                remove_trees = eat_trees(habitat_patch, eatenTrees)
                self.count_eaten[my_choice] += remove_trees
            elif my_choice == "scrub":
                eatenScrub = math.ceil((1-self.energy)/gain_from_scrub)
                if eatenScrub >= habitat_patch.edibles['scrub']:
                    eatenScrub = habitat_patch.edibles['scrub']
                self.energy += (gain_from_scrub * eatenScrub)
                remove_trees = eat_scrub(habitat_patch, eatenScrub)
                self.count_eaten[my_choice] += eatenScrub
            elif my_choice == "youngScrub":
                eatenYoungScrub = math.ceil((1-self.energy)/gain_from_young_scrub)
                # scrub facilitates saplings by preventing herbivory
                if eatenYoungScrub >= habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800))):
                    eatenYoungScrub = habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800)))
                eat_youngscrub(habitat_patch, eatenYoungScrub)
                self.energy += (gain_from_young_scrub * eatenYoungScrub)
                self.count_eaten[my_choice] += eatenYoungScrub
            elif my_choice == "grass":
                eatenGrass = math.ceil((1-self.energy)/gain_from_grass)
                if eatenGrass >= habitat_patch.edibles["grass"]:
                    eatenGrass = habitat_patch.edibles["grass"]
                eat_grass(habitat_patch, eatenGrass)
                self.energy += (gain_from_grass * eatenGrass)
                self.count_eaten[my_choice] += eatenGrass
        else:
            break
        # don't let energy be above 1; do a break and >= 1
        if self.energy >= 1:
            self.energy = 1
        # what is my energy now?
        return self.energy


def browser_move(self, FieldAgent):
    '''
    move towards areas with most undergrowth (saplings and thorny scrub)
    '''
    # look at neigboring fields - what is the field I am in? And what fields are neighboring it
    my_field = self.model.space.get_region_by_id(self.field_id)
    next_moves = self.model.space.get_neighbors_within_distance(my_field, 1)
    my_choices = [agent for agent in next_moves if (isinstance(agent, FieldAgent))]
    # what are in those fields?
    wood_scrub_areas = [i for i in my_choices if i.condition == "woodland" or i.condition == "thorny_scrubland"]
    
    if len(wood_scrub_areas) > 0:
    # if yes, pick one of those
        next_move = random.choice(wood_scrub_areas)
     # otherwise, pick any one at random
    else:
        next_move = random.choice(my_choices)
    # Now move:
    self.model.space.move_agent(self, next_move)


def grazer_move(self, FieldAgent):
    '''
    move towards grass
    '''
    # look at neigboring fields - what is the field I am in? And what fields are neighboring it
    my_field = self.model.space.get_region_by_id(self.field_id)
    next_moves = self.model.space.get_neighbors_within_distance(my_field, 1)
    my_choices = [agent for agent in next_moves if (isinstance(agent, FieldAgent))]
    # what are in those fields?
    grass_areas = [i for i in my_choices if i.condition == "grassland"]
    
    if len(grass_areas) > 0:
    # if yes, pick one of those
        next_move = random.choice(grass_areas)
     # otherwise, pick any one at random
    else:
        next_move = random.choice(my_choices)
    # Now move:
    self.model.space.move_agent(self, next_move)


def mixed_diet_move(self, FieldAgent):
    '''
    move towards grass in spring/summer, any habitat in autumn/winter
    '''
    # look at neigboring fields - what is the field I am in? And what fields are neighboring it
    my_field = self.model.space.get_region_by_id(self.field_id)
    next_moves = self.model.space.get_neighbors_within_distance(my_field, 1)
    my_choices = [agent for agent in next_moves if (isinstance(agent, FieldAgent))]

    # if it's March-Aug, find grass
    if (1 <= self.model.get_month() < 7):
        # are there any that are not protected? 
        if len(my_choices) > 0:
            grass_areas = [i for i in my_choices if i.condition == "grassland"]
            # are there any that are grassland? 
            if len(grass_areas) > 0:
                next_move = random.choice(grass_areas)
            else:
                next_move = random.choice(my_choices)
        # otherwise, pick any one at random if it's not protected
        else:
            if len(my_choices) > 0:
                next_move = random.choice(my_choices)
            else:
                next_move = random.choice(next_moves)
        # Now move:
        self.model.space.move_agent(self, next_move)



def random_move(self, FieldAgent):
    my_field = self.model.space.get_region_by_id(self.field_id)
    next_moves = self.model.space.get_neighbors_within_distance(my_field, 1)
    my_choices = [agent for agent in next_moves if (isinstance(agent, FieldAgent))]
    next_move = random.choice(my_choices)        
    self.model.space.move_agent(self, next_move)
