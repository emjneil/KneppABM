import random 
import math
from random import choice as rchoice
from shapely.geometry import Polygon, MultiPolygon

def eat_saplings(habitat_patch, eatenSaps):
    habitat_patch.edibles["saplings"] -= eatenSaps

def eat_trees(self, habitat_patch, eatenTrees):
    # not all trees will die
    # how_many_die = eatenTrees - int(eatenTrees*self.model.chance_tree_survival)
    habitat_patch.edibles["trees"] -= eatenTrees
    return eatenTrees


def eat_scrub(self, habitat_patch, eatenScrub):
    # not all mature scrub will die
    # how_many_die = eatenScrub - int(eatenScrub*self.model.chance_scrub_survival)
    habitat_patch.edibles["scrub"] -= eatenScrub
    return eatenScrub

def eat_youngscrub(habitat_patch, eatenYoungScrub):
    habitat_patch.edibles["youngScrub"] -= eatenYoungScrub

def eat_grass(habitat_patch, eatenGrass):
    habitat_patch.edibles["grass"] -= eatenGrass
    habitat_patch.edibles["bare_ground"] += eatenGrass


def eat_habitats(self, habitat_patch, my_dietary_preference, gain_from_saplings, gain_from_trees, gain_from_scrub, gain_from_young_scrub, gain_from_grass):
    habitat_choices = ["saplings", "trees", "scrub", "youngScrub", "grass"]

    # reset count eaten
    self.count_eaten.clear()
    # find size of my field
    my_field = self.model.space.get_region_by_id(self.field_id)
    if type(my_field.geometry) == Polygon:
        size_of_patch = Polygon(my_field.geometry).area
    else:
        polygon_list = list([MultiPolygon(my_field.geometry)])
        size_of_patch = sum(polygon.area for polygon in polygon_list)

    # # browsers prefer woody veg (saplings, young scrub, trees, scrub) to grass
    # if my_dietary_preference == "browser":
    #     my_preference = ["saplings", "trees", "scrub", "youngScrub"]
    #     not_my_preference = ["grass"]
    
    # if my_dietary_preference == "grazer":
    #     my_preference = ["grass"]
    #     not_my_preference = ["saplings", "trees", "scrub", "youngScrub"]

    # # I prefer grass in spring/summer
    # if my_dietary_preference == "intermediate_feeder": 
    #     if (1 <= self.model.get_month() < 7):
    #         my_preference = ["grass"]
    #         not_my_preference = ["saplings", "trees", "scrub", "youngScrub"]
    #     else:
    #         my_preference = ["saplings", "trees", "scrub", "youngScrub", "grass"]
    #         not_my_preference = []

    # if my_dietary_preference == "random":
    #     my_preference = ["saplings", "trees", "scrub", "youngScrub", "grass"]
    #     not_my_preference = []

          
    for _ in range(len(habitat_choices)):
        if self.energy < 1:
            # pick a habitat type
            my_choice = rchoice(habitat_choices)
            habitat_choices.remove(my_choice)
            # if my energy is low enough, eat it 
            # if my_choice == "saplings":
            #     eatenSaps = math.ceil((1-self.energy)/gain_from_saplings)
            #     # scrub facilitates saplings by preventing herbivory
            #     if eatenSaps >= habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/(800*(size_of_patch/10000))))):
            #         eatenSaps = habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/(800*(size_of_patch/10000)))))
            #     eat_saplings(habitat_patch, eatenSaps)
            #     self.energy += (gain_from_saplings * eatenSaps)
            #     self.count_eaten[my_choice] += eatenSaps

            if my_choice == "saplings":
                eatenSaps = math.ceil((1-self.energy)/gain_from_saplings)
                # scale by the protection factor of scrub
                # eatenSaps = eatenSaps - (round(eatenSaps*(self.model.chance_scrub_saves_saplings*((habitat_patch.edibles["scrub"])/(4000*(size_of_patch/10000))))))
                # if random.random() < ((habitat_patch.edibles["scrub"])/(4000*(size_of_patch/10000))): 
                #     eatenSaps = 0
                if random.random() < (self.model.chance_scrub_saves_saplings*100*((habitat_patch.edibles["scrub"])/(4000*(size_of_patch/10000)))): 
                    eatenSaps = 0
                if eatenSaps > habitat_patch.edibles["saplings"]:
                    eatenSaps = habitat_patch.edibles["saplings"]
                eat_saplings(habitat_patch, eatenSaps)
                self.energy += (gain_from_saplings * eatenSaps)
                self.count_eaten[my_choice] += eatenSaps
            elif my_choice == "trees":
                eatenTrees = math.ceil((1-self.energy)/gain_from_trees)
                if eatenTrees > habitat_patch.edibles["trees"]:
                    eatenTrees = habitat_patch.edibles["trees"]
                self.energy += (gain_from_trees * eatenTrees)
                trees_removed = eat_trees(self, habitat_patch, eatenTrees)
                self.count_eaten[my_choice] += trees_removed # this is how many die/are removed
            elif my_choice == "scrub":
                eatenScrub = math.ceil((1-self.energy)/gain_from_scrub)
                if eatenScrub > habitat_patch.edibles['scrub']:
                    eatenScrub = habitat_patch.edibles['scrub']
                self.energy += (gain_from_scrub * eatenScrub)
                scrub_removed = eat_scrub(self, habitat_patch, eatenScrub)
                self.count_eaten[my_choice] += scrub_removed # this is how many die/are removed
            elif my_choice == "youngScrub":
                eatenYoungScrub = math.ceil((1-self.energy)/gain_from_young_scrub)
                # if random.random() < ((habitat_patch.edibles["scrub"])/(4000*(size_of_patch/10000))): 
                #     eatenYoungScrub = 0
                if eatenYoungScrub > habitat_patch.edibles["youngScrub"]:
                    eatenYoungScrub = habitat_patch.edibles["youngScrub"]
                eat_youngscrub(habitat_patch, eatenYoungScrub)
                self.energy += (gain_from_young_scrub * eatenYoungScrub)
                self.count_eaten[my_choice] += eatenYoungScrub
            # elif my_choice == "youngScrub":
            #     eatenYoungScrub = math.ceil((1-self.energy)/gain_from_young_scrub)
            #     # scrub facilitates saplings by preventing herbivory
            #     if eatenYoungScrub >= habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/(800*(size_of_patch/10000))))):
            #         eatenYoungScrub = habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/(800*(size_of_patch/10000)))))
            #     eat_youngscrub(habitat_patch, eatenYoungScrub)
            #     self.energy += (gain_from_young_scrub * eatenYoungScrub)
            #     self.count_eaten[my_choice] += eatenYoungScrub

            elif my_choice == "grass":
                eatenGrass = math.ceil((1-self.energy)/gain_from_grass)
                if eatenGrass >= habitat_patch.edibles["grass"]:
                    eatenGrass = habitat_patch.edibles["grass"]
                eat_grass(habitat_patch, eatenGrass)
                self.energy += (gain_from_grass * eatenGrass)
                self.count_eaten[my_choice] += eatenGrass
        else:
            break
    
    # # is energy still <1? 
    # if self.energy < 1:
    #     # otherwise go to my non-preferences 
    #     for _ in range(len(not_my_preference)):
    #         if self.energy < 1:
    #             # pick a habitat type
    #             my_choice = rchoice(not_my_preference)
    #             not_my_preference.remove(my_choice)
    #             # if my energy is low enough, eat it 
    #             if my_choice == "saplings":
    #                 eatenSaps = math.ceil((1-self.energy)/gain_from_saplings)
    #                 if random.random() < ((habitat_patch.edibles["scrub"])/(800*(size_of_patch/10000))): 
    #                     eatenSaps = 0
    #                 if eatenSaps > habitat_patch.edibles["saplings"]:
    #                     eatenSaps = habitat_patch.edibles["saplings"]
    #                 eat_saplings(habitat_patch, eatenSaps)
    #                 self.energy += (gain_from_saplings * eatenSaps)
    #                 self.count_eaten[my_choice] += eatenSaps
    #             elif my_choice == "trees":
    #                 eatenTrees = math.ceil((1-self.energy)/gain_from_trees)
    #                 if eatenTrees >= habitat_patch.edibles["trees"]:
    #                     eatenTrees = habitat_patch.edibles["trees"]
    #                 self.energy += (gain_from_trees * eatenTrees)
    #                 trees_removed = eat_trees(self, habitat_patch, eatenTrees)
    #                 self.count_eaten[my_choice] += trees_removed # this is how many die/are removed
    #             elif my_choice == "scrub":
    #                 eatenScrub = math.ceil((1-self.energy)/gain_from_scrub)
    #                 if eatenScrub >= habitat_patch.edibles['scrub']:
    #                     eatenScrub = habitat_patch.edibles['scrub']
    #                 self.energy += (gain_from_scrub * eatenScrub)
    #                 scrub_removed = eat_scrub(self, habitat_patch, eatenScrub)
    #                 self.count_eaten[my_choice] += scrub_removed # this is how many die/are removed
    #             elif my_choice == "youngScrub":
    #                 eatenYoungScrub = math.ceil((1-self.energy)/gain_from_young_scrub)
    #                 if random.random() < ((habitat_patch.edibles["scrub"])/(800*(size_of_patch/10000))): 
    #                     eatenYoungScrub = 0
    #                 if eatenYoungScrub > habitat_patch.edibles["youngScrub"]:
    #                     eatenYoungScrub = habitat_patch.edibles["youngScrub"]
    #                 eat_youngscrub(habitat_patch, eatenYoungScrub)
    #                 self.energy += (gain_from_young_scrub * eatenYoungScrub)
    #                 self.count_eaten[my_choice] += eatenYoungScrub
    #             elif my_choice == "grass":
    #                 eatenGrass = math.ceil((1-self.energy)/gain_from_grass)
    #                 if eatenGrass >= habitat_patch.edibles["grass"]:
    #                     eatenGrass = habitat_patch.edibles["grass"]
    #                 eat_grass(habitat_patch, eatenGrass)
    #                 self.energy += (gain_from_grass * eatenGrass)
    #                 self.count_eaten[my_choice] += eatenGrass
    #         else:
    #             break    
        
    # don't let energy be above 1; do a break and >= 1
    if self.energy > 1:
        self.energy = 1
    # what is my energy now?
    return self.energy


def browser_move(self, FieldAgent):
    '''
    move towards areas with most undergrowth (saplings and thorny scrub)
    '''
    # look at neigboring fields - what is the field I am in? And what fields are neighboring it
    my_field = self.model.space.get_region_by_id(self.field_id)
    next_moves = self.model.saved_neighbors[my_field.unique_id]
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
    next_moves = self.model.saved_neighbors[my_field.unique_id]
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
    next_moves = self.model.saved_neighbors[my_field.unique_id]
    my_choices = [agent for agent in next_moves if (isinstance(agent, FieldAgent))]

    # if it's March-Aug, find grasslands
    if (1 <= self.model.get_month() < 7):
        grass_areas = [i for i in my_choices if i.condition == "grassland"]
        # are there any that are grassland? 
        if len(grass_areas) > 0:
            next_move = random.choice(grass_areas)
        else:
            next_move = random.choice(my_choices)
    else:
        next_move = random.choice(my_choices)
        # Now move:
    self.model.space.move_agent(self, next_move)



def random_move(self, FieldAgent):
    my_field = self.model.space.get_region_by_id(self.field_id)
    next_moves = self.model.saved_neighbors[my_field.unique_id]
    my_choices = [agent for agent in next_moves if (isinstance(agent, FieldAgent))]
    next_move = random.choice(my_choices)        
    self.model.space.move_agent(self, next_move)
