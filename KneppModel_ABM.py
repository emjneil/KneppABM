# ------ ABM of the Knepp Estate (2005-2046) --------
from mesa import Agent, Model
from mesa.datacollection import DataCollector
import numpy as np
import random
import pandas as pd
from random_walk import RandomWalker
from schedule import RandomActivationByBreed
from mesa.space import MultiGrid 
from random import choice as rchoice
import math
from collections import defaultdict


# herbivore eating habitat types
def eat_saplings(habitat_patch, eatenSaps):
    habitat_patch.edibles["saplings"] -= eatenSaps

def eat_trees(habitat_patch, eatenTrees):
    habitat_patch.edibles["trees"] -= eatenTrees

def eat_scrub(habitat_patch, eatenScrub):
    habitat_patch.edibles["scrub"] -= eatenScrub

def eat_youngscrub(habitat_patch, eatenYoungScrub):
    habitat_patch.edibles["youngScrub"] -= eatenYoungScrub

def eat_grass(habitat_patch, eatenGrass):
    habitat_patch.edibles["grass"] -= eatenGrass
    habitat_patch.edibles["bare_ground"] += eatenGrass


                            # # # # ------ Define the agents ------ # # # #

class habitatAgent (Agent):
    def __init__(self, unique_id, pos, model, condition, trees_here, saplings_here, scrub_here, youngscrub_here, perc_grass_here, perc_bareground_here):
        super().__init__(unique_id, model)

        self.edibles = defaultdict(int)
        self.edibles["trees"] = trees_here
        self.edibles['scrub'] = scrub_here
        self.edibles["saplings"] = saplings_here
        self.edibles["youngScrub"] = youngscrub_here
        self.edibles["grass"] = perc_grass_here
        self.edibles["bare_ground"] = perc_bareground_here
        self.condition = condition
        self.pos = pos

        self.habs_eaten = defaultdict(int)
        self.habs_outcompeted_byTrees= defaultdict(int)
        self.habs_outcompeted_byScrub = defaultdict(int)
        self.habs_grew_up = defaultdict(int)


    def step(self):

        self.habs_eaten.clear()
        self.habs_outcompeted_byTrees.clear()
        self.habs_outcompeted_byScrub.clear()
        self.habs_grew_up.clear()

        # chance of 1 young scrub becoming 1 mature scrub
        number_scrub_maturing = np.random.binomial(n=self.edibles["youngScrub"], p=self.model.chance_youngScrubMatures)
        # don't let it go over 800 mature shrubs
        number_scrub_maturing = min(number_scrub_maturing, 800 - self.edibles['scrub'])
        self.edibles['scrub'] += number_scrub_maturing
        self.edibles["youngScrub"] -= number_scrub_maturing
        self.habs_grew_up["youngScrub"] += number_scrub_maturing

        # chance of sapling becoming tree
        number_saplings_maturing = np.random.binomial(n=self.edibles["saplings"], p=self.model.chance_saplingBecomingTree)
        # don't let it go over 400 trees
        number_saplings_maturing = min(number_saplings_maturing, 400 - self.edibles["trees"])
        self.edibles["trees"] += number_saplings_maturing
        self.edibles["saplings"] -= number_saplings_maturing
        self.habs_grew_up["saplings"] += number_saplings_maturing

        # chance of reproducing saplings or young shrubs
        neighborhood_list = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)
        items_in_neighborhood = list(map(self.model.grid.get_cell_list_contents, neighborhood_list)) 
        only_habitat_cells = [obj for obj in items_in_neighborhood if (isinstance(x, habitatAgent) for x in obj)]
        no_herbivores = [item[0] for item in only_habitat_cells]

        # chance of reproducing saplings
        number_reproduce_trees = np.random.binomial(n=self.edibles["trees"], p=self.model.chance_reproduceSapling)
        # are there any that aren't full of other saplings/trees?
        available_sapling_cell = [i for i in no_herbivores if i.edibles["saplings"] < 5000 and i.edibles["trees"] < 400]
        if len(available_sapling_cell) > 0: 
            list_of_choices = random.choices(available_sapling_cell, k = number_reproduce_trees)
            for i in range(number_reproduce_trees):
                new_patch_sapling = list_of_choices[i]
                new_patch_sapling.edibles["saplings"] += 1 

        list_of_choices = None
        # chance of reproducing scrub
        number_reproduce_shrubs = np.random.binomial(n=self.edibles['scrub'], p=self.model.chance_reproduceYoungScrub)
        # are there any that aren't full of other scrub/young scrub?
        available_youngscrub_cell = [i for i in no_herbivores if i.edibles["youngScrub"] < 5000 and i.edibles['scrub'] < 400]
        if len(available_youngscrub_cell) > 0:
            list_of_choices = random.choices(available_youngscrub_cell, k = number_reproduce_shrubs)
            for i in range(number_reproduce_shrubs):
                new_patch_youngscrub = list_of_choices[i]
                new_patch_youngscrub.edibles["youngScrub"] += 1 
   
        # chance of 1% bare ground becoming 1% grassland
        number_reproduce_bareGround = np.random.binomial(n=self.edibles["bare_ground"], p=self.model.chance_regrowGrass)
        self.edibles["grass"] += number_reproduce_bareGround
        self.edibles["bare_ground"] -= number_reproduce_bareGround

        # chance of grass being outcompeted by mature trees and scrub
        outcompeted_by_trees = ((self.edibles["trees"]/400)*self.model.chance_grassOutcompetedByTree) 
        if outcompeted_by_trees>1: outcompeted_by_trees=1
        outcompeted_grass_byTrees = np.random.binomial(n=self.edibles["grass"], p=outcompeted_by_trees)
        if self.edibles["grass"] - outcompeted_grass_byTrees < 0: outcompeted_grass_byTrees = self.edibles["grass"]
        self.edibles["grass"] -= outcompeted_grass_byTrees
        self.edibles["bare_ground"] += outcompeted_grass_byTrees
        self.habs_outcompeted_byTrees["grass"] += outcompeted_grass_byTrees
        #shrubs
        outcompeted_by_shrubs = ((self.edibles['scrub']/800)*self.model.chance_grassOutcompetedByScrub)
        if outcompeted_by_shrubs>1: outcompeted_by_shrubs=1
        outcompeted_grass_byScrub = np.random.binomial(n=self.edibles["grass"], p=outcompeted_by_shrubs)
        if self.edibles["grass"] - outcompeted_grass_byScrub < 0: outcompeted_grass_byScrub = self.edibles["grass"]
        self.edibles["grass"] -= outcompeted_grass_byScrub
        self.edibles["bare_ground"] += outcompeted_grass_byScrub
        self.habs_outcompeted_byScrub["grass"] += outcompeted_grass_byScrub

        # chance of mature scrub being outcompeted by trees 
        prob=(self.edibles["trees"]/400)*self.model.chance_scrubOutcompetedByTree
        if prob>1: prob=1
        mature_scrub_outcompeted = np.random.binomial(n=self.edibles['scrub'], p=prob)
        self.edibles['scrub'] -= mature_scrub_outcompeted
        self.habs_outcompeted_byTrees["scrub"] += mature_scrub_outcompeted

        # saplings being outcompeted by scrub/trees
        outcompeted_by_trees = ((self.edibles["trees"]/400)*self.model.chance_saplingOutcompetedByTree) 
        if outcompeted_by_trees>1: outcompeted_by_trees=1
        outcompeted_saplings_byTrees = np.random.binomial(n=self.edibles["saplings"], p=outcompeted_by_trees)
        if self.edibles["saplings"] - outcompeted_saplings_byTrees < 0: outcompeted_saplings_byTrees = self.edibles["saplings"]
        self.edibles["saplings"] -= outcompeted_saplings_byTrees
        self.habs_outcompeted_byTrees["saplings"] += outcompeted_saplings_byTrees

        outcompeted_by_shrubs = ((self.edibles['scrub']/800)*self.model.chance_saplingOutcompetedByScrub)
        if outcompeted_by_shrubs>1: outcompeted_by_shrubs=1
        outcompeted_saplings_byScrub = np.random.binomial(n=self.edibles["saplings"], p=outcompeted_by_shrubs)
        if self.edibles["saplings"] - outcompeted_saplings_byScrub < 0: outcompeted_saplings_byScrub = self.edibles["saplings"]
        self.edibles["saplings"] -= outcompeted_saplings_byScrub
        self.habs_outcompeted_byScrub["saplings"] += outcompeted_saplings_byScrub

        # young scrub being outcompeted by scrub/trees
        outcompeted_by_trees = ((self.edibles["trees"]/400)*self.model.chance_youngScrubOutcompetedByTree) 
        if outcompeted_by_trees > 1: outcompeted_by_trees = 1
        outcompeted_youngScrub_byTrees = np.random.binomial(n=self.edibles["youngScrub"], p=outcompeted_by_trees)
        self.edibles["youngScrub"] -= outcompeted_youngScrub_byTrees
        self.habs_outcompeted_byTrees["youngScrub"] += outcompeted_youngScrub_byTrees
        outcompeted_by_shrubs = ((self.edibles['scrub']/800)*self.model.chance_youngScrubOutcompetedByScrub)
        if outcompeted_by_shrubs>1: outcompeted_by_shrubs=1
        outcompeted_youngScrub_byScrub = np.random.binomial(n=self.edibles["youngScrub"], p=outcompeted_by_shrubs)
        self.edibles["youngScrub"] -= outcompeted_youngScrub_byScrub
        self.habs_outcompeted_byScrub["youngScrub"] += outcompeted_youngScrub_byScrub

        # reassess dominant condition
        if self.edibles["trees"] < 50 and self.edibles["scrub"] < 100 and self.edibles["grass"] >= 50:
            self.condition = "grassland"
        elif self.edibles["trees"] < 50 and self.edibles["scrub"] >= 100:
            self.condition = "thorny_scrubland"
        elif self.edibles["trees"] >= 50:
            self.condition = "woodland" 
        elif self.edibles["trees"] < 50 and self.edibles["scrub"] < 100 and self.edibles["bare_ground"] > 50:
            self.condition = "bare_ground"
        

class reindeer(RandomWalker):
    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.count_eaten = defaultdict(int)
        self.energy = energy

    def step(self):
        # move & reduce energy
        self.mixedDiet_move()
        living = True
        self.energy -= 1
        self.count_eaten.clear()
        # Eat what's on my patch: roe deer are broswers, so randomly choose any habitat to eat
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        habitat_choices = ["saplings", "trees", "scrub", "youngScrub", "grass"]
        # pick a habitat type and eat it 
        for _ in range(len(habitat_choices)):
            if self.energy < 1:
                # pick a habitat type
                my_choice = rchoice(habitat_choices)
                habitat_choices.remove(my_choice)
                # if my energy is low enough, eat it 
                if my_choice == "saplings":
                    eatenSaps = math.ceil((1-self.energy)/self.model.reindeer_gain_from_Saplings)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenSaps >= habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800))):
                        eatenSaps = habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800)))
                    eat_saplings(habitat_patch, eatenSaps)
                    self.energy += (self.model.reindeer_gain_from_Saplings * eatenSaps)
                    self.count_eaten[my_choice] += eatenSaps
                elif my_choice == "trees":
                    eatenTrees = math.ceil((1-self.energy)/self.model.reindeer_gain_from_Trees)
                    if eatenTrees >= habitat_patch.edibles["trees"]:
                        eatenTrees = habitat_patch.edibles["trees"]
                    eat_trees(habitat_patch, eatenTrees)
                    self.energy += (self.model.reindeer_gain_from_Trees * eatenTrees)
                    self.count_eaten[my_choice] += eatenTrees
                elif my_choice == "scrub":
                    eatenScrub = math.ceil((1-self.energy)/self.model.reindeer_gain_from_Scrub)
                    if eatenScrub >= habitat_patch.edibles['scrub']:
                        eatenScrub = habitat_patch.edibles['scrub']
                    eat_scrub(habitat_patch, eatenScrub)
                    self.energy += (self.model.reindeer_gain_from_Scrub * eatenScrub)
                    self.count_eaten[my_choice] += eatenScrub
                elif my_choice == "youngScrub":
                    eatenYoungScrub = math.ceil((1-self.energy)/self.model.reindeer_gain_from_YoungScrub)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenYoungScrub >= habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800))):
                        eatenYoungScrub = habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800)))
                    eat_youngscrub(habitat_patch, eatenYoungScrub)
                    self.energy += (self.model.reindeer_gain_from_YoungScrub * eatenYoungScrub)
                    self.count_eaten[my_choice] += eatenYoungScrub
                elif my_choice == "grass":
                    eatenGrass = math.ceil((1-self.energy)/self.model.reindeer_gain_from_grass)
                    if eatenGrass >= habitat_patch.edibles["grass"]:
                        eatenGrass = habitat_patch.edibles["grass"]
                    eat_grass(habitat_patch, eatenGrass)
                    self.energy += (self.model.reindeer_gain_from_grass * eatenGrass)
                    self.count_eaten[my_choice] += eatenGrass
            else:
                break
            # don't let energy be above 1; do a break and >= 1
            if self.energy >= 1:
                self.energy = 1

        # if cow's energy is less than 0, die 
        if self.energy <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        # I reproduce in April, May, and June (assuming model starts in Jan at beginning of year, April, May & June = time steps 4-6 out of every 12 months)
        if living and (random.random() < self.model.reproduce_reindeer/np.log10(self.model.schedule.get_breed_count(reindeer)+ 1)) and (4 <= self.model.get_month() < 7):
            # Create a new cow and divide energy:
            self.energy = np.random.uniform(0, self.energy)
            calf = reindeer(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
            self.model.grid.place_agent(calf, self.pos)
            self.model.schedule.add(calf)







class euroElk(RandomWalker):
    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.count_eaten = defaultdict(int)
        self.energy = energy

    def step(self):
        # move & reduce energy
        self.roe_move()
        living = True
        self.energy -= 1
        self.count_eaten.clear()
        # Eat what's on my patch: roe deer are broswers, so randomly choose any habitat to eat
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        habitat_choices = ["saplings", "trees", "scrub", "youngScrub", "grass"]
        # pick a habitat type and eat it 
        for _ in range(len(habitat_choices)):
            if self.energy < 1:
                # pick a habitat type
                my_choice = rchoice(habitat_choices)
                habitat_choices.remove(my_choice)
                # if my energy is low enough, eat it 
                if my_choice == "saplings":
                    eatenSaps = math.ceil((1-self.energy)/self.model.elk_gain_from_Saplings)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenSaps >= habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800))):
                        eatenSaps = habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800)))
                    eat_saplings(habitat_patch, eatenSaps)
                    self.energy += (self.model.elk_gain_from_Saplings * eatenSaps)
                    self.count_eaten[my_choice] += eatenSaps
                elif my_choice == "trees":
                    eatenTrees = math.ceil((1-self.energy)/self.model.elk_gain_from_Trees)
                    if eatenTrees >= habitat_patch.edibles["trees"]:
                        eatenTrees = habitat_patch.edibles["trees"]
                    eat_trees(habitat_patch, eatenTrees)
                    self.energy += (self.model.elk_gain_from_Trees * eatenTrees)
                    self.count_eaten[my_choice] += eatenTrees
                elif my_choice == "scrub":
                    eatenScrub = math.ceil((1-self.energy)/self.model.elk_gain_from_Scrub)
                    if eatenScrub >= habitat_patch.edibles['scrub']:
                        eatenScrub = habitat_patch.edibles['scrub']
                    eat_scrub(habitat_patch, eatenScrub)
                    self.energy += (self.model.elk_gain_from_Scrub * eatenScrub)
                    self.count_eaten[my_choice] += eatenScrub
                elif my_choice == "youngScrub":
                    eatenYoungScrub = math.ceil((1-self.energy)/self.model.elk_gain_from_YoungScrub)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenYoungScrub >= habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800))):
                        eatenYoungScrub = habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800)))
                    eat_youngscrub(habitat_patch, eatenYoungScrub)
                    self.energy += (self.model.elk_gain_from_YoungScrub * eatenYoungScrub)
                    self.count_eaten[my_choice] += eatenYoungScrub
                elif my_choice == "grass":
                    eatenGrass = math.ceil((1-self.energy)/self.model.elk_gain_from_grass)
                    if eatenGrass >= habitat_patch.edibles["grass"]:
                        eatenGrass = habitat_patch.edibles["grass"]
                    eat_grass(habitat_patch, eatenGrass)
                    self.energy += (self.model.elk_gain_from_grass * eatenGrass)
                    self.count_eaten[my_choice] += eatenGrass
            else:
                break
            # don't let energy be above 1; do a break and >= 1
            if self.energy >= 1:
                self.energy = 1

        # if cow's energy is less than 0, die 
        if self.energy <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        # I reproduce in April, May, and June (assuming model starts in Jan at beginning of year, April, May & June = time steps 4-6 out of every 12 months)
        if living and (random.random() < self.model.reproduce_elk/np.log10(self.model.schedule.get_breed_count(euroElk)+ 1)) and (4 <= self.model.get_month() < 7):
            # Create a new cow and divide energy:
            self.energy = np.random.uniform(0, self.energy)
            calf = euroElk(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
            self.model.grid.place_agent(calf, self.pos)
            self.model.schedule.add(calf)





class euroBison(RandomWalker):
    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.count_eaten = defaultdict(int)
        self.energy = energy

    def step(self):
        # move & reduce energy
        self.mixedDiet_move()
        living = True
        self.energy -= 1

        self.count_eaten.clear()
        # Eat what's on my patch: roe deer are broswers, so randomly choose any habitat to eat
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        habitat_choices = ["saplings", "trees", "scrub", "youngScrub", "grass"]
        # pick a habitat type and eat it 
        for _ in range(len(habitat_choices)):
            if self.energy < 1:
                # pick a habitat type
                my_choice = rchoice(habitat_choices)
                habitat_choices.remove(my_choice)
                # if my energy is low enough, eat it 
                if my_choice == "saplings":
                    eatenSaps = math.ceil((1-self.energy)/self.model.bison_gain_from_Saplings)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenSaps >= habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800))):
                        eatenSaps = habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800)))
                    eat_saplings(habitat_patch, eatenSaps)
                    self.energy += (self.model.bison_gain_from_Saplings * eatenSaps)
                    self.count_eaten[my_choice] += eatenSaps
                elif my_choice == "trees":
                    eatenTrees = math.ceil((1-self.energy)/self.model.bison_gain_from_Trees)
                    if eatenTrees >= habitat_patch.edibles["trees"]:
                        eatenTrees = habitat_patch.edibles["trees"]
                    eat_trees(habitat_patch, eatenTrees)
                    self.energy += (self.model.bison_gain_from_Trees * eatenTrees)
                    self.count_eaten[my_choice] += eatenTrees
                elif my_choice == "scrub":
                    eatenScrub = math.ceil((1-self.energy)/self.model.bison_gain_from_Scrub)
                    if eatenScrub >= habitat_patch.edibles['scrub']:
                        eatenScrub = habitat_patch.edibles['scrub']
                    eat_scrub(habitat_patch, eatenScrub)
                    self.energy += (self.model.bison_gain_from_Scrub * eatenScrub)
                    self.count_eaten[my_choice] += eatenScrub
                elif my_choice == "youngScrub":
                    eatenYoungScrub = math.ceil((1-self.energy)/self.model.bison_gain_from_YoungScrub)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenYoungScrub >= habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800))):
                        eatenYoungScrub = habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800)))
                    eat_youngscrub(habitat_patch, eatenYoungScrub)
                    self.energy += (self.model.bison_gain_from_YoungScrub * eatenYoungScrub)
                    self.count_eaten[my_choice] += eatenYoungScrub
                elif my_choice == "grass":
                    eatenGrass = math.ceil((1-self.energy)/self.model.bison_gain_from_grass)
                    if eatenGrass >= habitat_patch.edibles["grass"]:
                        eatenGrass = habitat_patch.edibles["grass"]
                    eat_grass(habitat_patch, eatenGrass)
                    self.energy += (self.model.bison_gain_from_grass * eatenGrass)
                    self.count_eaten[my_choice] += eatenGrass
            else:
                break
            # don't let energy be above 1; do a break and >= 1
            if self.energy >= 1:
                self.energy = 1

        # if cow's energy is less than 0, die 
        if self.energy <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        # I reproduce in April, May, and June (assuming model starts in Jan at beginning of year, April, May & June = time steps 4-6 out of every 12 months)
        if living and (random.random() < self.model.reproduce_bison/np.log10(self.model.schedule.get_breed_count(euroBison)+ 1)) and (4 <= self.model.get_month() < 7):
            # Create a new cow and divide energy:
            self.energy = np.random.uniform(0, self.energy)
            calf = euroBison(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
            self.model.grid.place_agent(calf, self.pos)
            self.model.schedule.add(calf)



class roeDeer(RandomWalker):
    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.count_eaten = defaultdict(int)
        self.energy = energy

    def step(self):
        # move & reduce energy
        self.roe_move()
        # self.random_move()
        living = True
        self.energy -= 1
        
        # Eat what's on my patch: roe deer are broswers, so randomly choose any habitat to eat
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
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
                    eatenSaps = math.ceil((1-self.energy)/self.model.roeDeer_gain_from_Saplings)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenSaps >= habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800))):
                        eatenSaps = habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800)))
                    eat_saplings(habitat_patch, eatenSaps)
                    self.energy += (self.model.roeDeer_gain_from_Saplings * eatenSaps)
                    self.count_eaten[my_choice] += eatenSaps
                elif my_choice == "trees":
                    eatenTrees = math.ceil((1-self.energy)/self.model.roeDeer_gain_from_Trees)
                    if eatenTrees >= habitat_patch.edibles["trees"]:
                        eatenTrees = habitat_patch.edibles["trees"]
                    eat_trees(habitat_patch, eatenTrees)
                    self.energy += (self.model.roeDeer_gain_from_Trees * eatenTrees)
                    self.count_eaten[my_choice] += eatenTrees
                elif my_choice == "scrub":
                    eatenScrub = math.ceil((1-self.energy)/self.model.roeDeer_gain_from_Scrub)
                    if eatenScrub >= habitat_patch.edibles['scrub']:
                        eatenScrub = habitat_patch.edibles['scrub']
                    eat_scrub(habitat_patch, eatenScrub)
                    self.energy += (self.model.roeDeer_gain_from_Scrub * eatenScrub)
                    self.count_eaten[my_choice] +=eatenScrub
                elif my_choice == "youngScrub":
                    eatenYoungScrub = math.ceil((1-self.energy)/self.model.roeDeer_gain_from_YoungScrub)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenYoungScrub >= habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800))):
                        eatenYoungScrub = habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800)))
                    eat_youngscrub(habitat_patch, eatenYoungScrub)
                    self.energy += (self.model.roeDeer_gain_from_YoungScrub * eatenYoungScrub)
                    self.count_eaten[my_choice] += eatenYoungScrub
                elif my_choice == "grass":
                    eatenGrass = math.ceil((1-self.energy)/self.model.roeDeer_gain_from_grass)
                    if eatenGrass >= habitat_patch.edibles["grass"]:
                        eatenGrass = habitat_patch.edibles["grass"]
                    eat_grass(habitat_patch, eatenGrass)
                    self.energy += (self.model.roeDeer_gain_from_grass * eatenGrass)
                    self.count_eaten[my_choice] += eatenGrass
            else:
                break
            # don't let energy be above 1; do a break and >= 1
            if self.energy >= 1:
                self.energy = 1

        # if roe deer's energy is less than 0 or 1/7yrs (84 months), die 
        if self.energy <= 0 or random.random() < 0.012:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        # I can reproduce in May & June (assuming model starts in Jan at beginning of year, May & June = time steps 5&6 out of every 12 months)
        if living and (random.random() < self.model.roeDeer_reproduce/np.log10(self.model.schedule.get_breed_count(roeDeer)+ 1)) and (5 <= self.model.get_month() < 7):
            # Create a new roe deer and divide energy:
            self.energy = np.random.uniform(0, self.energy)
            fawn = roeDeer(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
            self.model.grid.place_agent(fawn, self.pos)
            self.model.schedule.add(fawn)


class exmoorPony(RandomWalker):
    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.count_eaten = defaultdict(int)
        self.energy = energy

    def step(self):
        # move & reduce energy
        self.grazer_move()
        living = True
        self.energy -= 1
        
        self.count_eaten.clear()
        # Eat what's on my patch: roe deer are broswers, so randomly choose any habitat to eat
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        habitat_choices = ["saplings", "trees", "scrub", "youngScrub", "grass"]
        # pick a habitat type and eat it 
        for _ in range(len(habitat_choices)):
            if self.energy < 1:
                # pick a habitat type
                my_choice = rchoice(habitat_choices)
                habitat_choices.remove(my_choice)
                # if my energy is low enough, eat it 
                if my_choice == "saplings":
                    eatenSaps = math.ceil((1-self.energy)/self.model.ponies_gain_from_Saplings)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenSaps >= habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800))):
                        eatenSaps = habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800)))
                    eat_saplings(habitat_patch, eatenSaps)
                    self.energy += (self.model.ponies_gain_from_Saplings * eatenSaps)
                    self.count_eaten[my_choice] += eatenSaps
                elif my_choice == "trees":
                    eatenTrees = math.ceil((1-self.energy)/self.model.ponies_gain_from_Trees)
                    if eatenTrees >= habitat_patch.edibles["trees"]:
                        eatenTrees = habitat_patch.edibles["trees"]
                    eat_trees(habitat_patch, eatenTrees)
                    self.energy += (self.model.ponies_gain_from_Trees * eatenTrees)
                    self.count_eaten[my_choice] += eatenTrees
                elif my_choice == "scrub":
                    eatenScrub = math.ceil((1-self.energy)/self.model.ponies_gain_from_Scrub)
                    if eatenScrub >= habitat_patch.edibles['scrub']:
                        eatenScrub = habitat_patch.edibles['scrub']
                    eat_scrub(habitat_patch, eatenScrub)
                    self.energy += (self.model.ponies_gain_from_Scrub * eatenScrub)
                    self.count_eaten[my_choice] += eatenScrub
                elif my_choice == "youngScrub":
                    eatenYoungScrub = math.ceil((1-self.energy)/self.model.ponies_gain_from_YoungScrub)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenYoungScrub >= habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800))):
                        eatenYoungScrub = habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800)))
                    eat_youngscrub(habitat_patch, eatenYoungScrub)
                    self.energy += (self.model.ponies_gain_from_YoungScrub * eatenYoungScrub)
                    self.count_eaten[my_choice] += eatenYoungScrub
                elif my_choice == "grass":
                    eatenGrass = math.ceil((1-self.energy)/self.model.ponies_gain_from_grass)
                    if eatenGrass >= habitat_patch.edibles["grass"]:
                        eatenGrass = habitat_patch.edibles["grass"]
                    eat_grass(habitat_patch, eatenGrass)
                    self.energy += (self.model.ponies_gain_from_grass * eatenGrass)
                    self.count_eaten[my_choice] += eatenGrass
            else:
                break
            # don't let energy be above 1; do a break and >= 1
            if self.energy >= 1:
                self.energy = 1
  
        # if pony's energy is less than 0, die 
        if self.energy <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            
    

class longhornCattle(RandomWalker):
    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.count_eaten = defaultdict(int)
        self.energy = energy

    def step(self):
        # move & reduce energy
        self.grazer_move()
        living = True
        self.energy -= 1

        self.count_eaten.clear()
        # Eat what's on my patch: roe deer are broswers, so randomly choose any habitat to eat
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        habitat_choices = ["saplings", "trees", "scrub", "youngScrub", "grass"]
        # pick a habitat type and eat it 
        for _ in range(len(habitat_choices)):
            if self.energy < 1:
                # pick a habitat type
                my_choice = rchoice(habitat_choices)
                habitat_choices.remove(my_choice)
                # if my energy is low enough, eat it 
                if my_choice == "saplings":
                    eatenSaps = math.ceil((1-self.energy)/self.model.cows_gain_from_Saplings)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenSaps >= habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800))):
                        eatenSaps = habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800)))
                    eat_saplings(habitat_patch, eatenSaps)
                    self.energy += (self.model.cows_gain_from_Saplings * eatenSaps)
                    self.count_eaten[my_choice] += eatenSaps
                elif my_choice == "trees":
                    eatenTrees = math.ceil((1-self.energy)/self.model.cows_gain_from_Trees)
                    if eatenTrees >= habitat_patch.edibles["trees"]:
                        eatenTrees = habitat_patch.edibles["trees"]
                    eat_trees(habitat_patch, eatenTrees)
                    self.energy += (self.model.cows_gain_from_Trees * eatenTrees)
                    self.count_eaten[my_choice] += eatenTrees
                elif my_choice == "scrub":
                    eatenScrub = math.ceil((1-self.energy)/self.model.cows_gain_from_Scrub)
                    if eatenScrub >= habitat_patch.edibles['scrub']:
                        eatenScrub = habitat_patch.edibles['scrub']
                    eat_scrub(habitat_patch, eatenScrub)
                    self.energy += (self.model.cows_gain_from_Scrub * eatenScrub)
                    self.count_eaten[my_choice] += eatenScrub
                elif my_choice == "youngScrub":
                    eatenYoungScrub = math.ceil((1-self.energy)/self.model.cows_gain_from_YoungScrub)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenYoungScrub >= habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800))):
                        eatenYoungScrub = habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800)))
                    eat_youngscrub(habitat_patch, eatenYoungScrub)
                    self.energy += (self.model.cows_gain_from_YoungScrub * eatenYoungScrub)
                    self.count_eaten[my_choice] += eatenYoungScrub
                elif my_choice == "grass":
                    eatenGrass = math.ceil((1-self.energy)/self.model.cows_gain_from_grass)
                    if eatenGrass >= habitat_patch.edibles["grass"]:
                        eatenGrass = habitat_patch.edibles["grass"]
                    eat_grass(habitat_patch, eatenGrass)
                    self.energy += (self.model.cows_gain_from_grass * eatenGrass)
                    self.count_eaten[my_choice] += eatenGrass
            else:
                break
            # don't let energy be above 1; do a break and >= 1
            if self.energy >= 1:
                self.energy = 1

        # if cow's energy is less than 0, die 
        if self.energy <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        # I reproduce in April, May, and June (assuming model starts in Jan at beginning of year, April, May & June = time steps 4-6 out of every 12 months)
        if living and (random.random() < self.model.cows_reproduce/np.log10(self.model.schedule.get_breed_count(longhornCattle)+ 1)) and (4 <= self.model.get_month() < 7):
            # Create a new cow and divide energy:
            self.energy = np.random.uniform(0, self.energy)
            calf = longhornCattle(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
            self.model.grid.place_agent(calf, self.pos)
            self.model.schedule.add(calf)
        

class fallowDeer(RandomWalker):
    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.count_eaten = defaultdict(int)
        self.energy = energy

    def step(self):
        # move & reduce energy
        self.mixedDiet_move()
        living = True
        self.energy -= 1

        self.count_eaten.clear()
        # Eat what's on my patch: roe deer are broswers, so randomly choose any habitat to eat
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        habitat_choices = ["saplings", "trees", "scrub", "youngScrub", "grass"]
        # pick a habitat type and eat it 
        for _ in range(len(habitat_choices)):
            if self.energy < 1:
                # pick a habitat type
                my_choice = rchoice(habitat_choices)
                habitat_choices.remove(my_choice)
                # if my energy is low enough, eat it 
                if my_choice == "saplings":
                    eatenSaps = math.ceil((1-self.energy)/self.model.fallowDeer_gain_from_Saplings)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenSaps >= habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800))):
                        eatenSaps = habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800)))
                    eat_saplings(habitat_patch, eatenSaps)
                    self.energy += (self.model.fallowDeer_gain_from_Saplings * eatenSaps)
                    self.count_eaten[my_choice] += eatenSaps
                elif my_choice == "trees":
                    eatenTrees = math.ceil((1-self.energy)/self.model.fallowDeer_gain_from_Trees)
                    if eatenTrees >= habitat_patch.edibles["trees"]:
                        eatenTrees = habitat_patch.edibles["trees"]
                    eat_trees(habitat_patch, eatenTrees)
                    self.energy += (self.model.fallowDeer_gain_from_Trees * eatenTrees)
                    self.count_eaten[my_choice] += eatenTrees
                elif my_choice == "scrub":
                    eatenScrub = math.ceil((1-self.energy)/self.model.fallowDeer_gain_from_Scrub)
                    if eatenScrub >= habitat_patch.edibles['scrub']:
                        eatenScrub = habitat_patch.edibles['scrub']
                    eat_scrub(habitat_patch, eatenScrub)
                    self.energy += (self.model.fallowDeer_gain_from_Scrub * eatenScrub)
                    self.count_eaten[my_choice] += eatenScrub
                elif my_choice == "youngScrub":
                    eatenYoungScrub = math.ceil((1-self.energy)/self.model.fallowDeer_gain_from_YoungScrub)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenYoungScrub >= habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800))):
                        eatenYoungScrub = habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800)))
                    eat_youngscrub(habitat_patch, eatenYoungScrub)
                    self.energy += (self.model.fallowDeer_gain_from_YoungScrub * eatenYoungScrub)
                    self.count_eaten[my_choice] += eatenYoungScrub
                elif my_choice == "grass":
                    eatenGrass = math.ceil((1-self.energy)/self.model.fallowDeer_gain_from_grass)
                    if eatenGrass >= habitat_patch.edibles["grass"]:
                        eatenGrass = habitat_patch.edibles["grass"]
                    eat_grass(habitat_patch, eatenGrass)
                    self.energy += (self.model.fallowDeer_gain_from_grass * eatenGrass)
                    self.count_eaten[my_choice] += eatenGrass
            else:
                break
            # don't let energy be above 1; do a break and >= 1
            if self.energy >= 1:
                self.energy = 1
    
        # if fallow deer's energy is less than 0, die 
        if self.energy <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False
            
        # I reproduce in May & June (assuming model starts in Jan at beginning of year, May & June = time steps 5&6 out of every 12 months)
        if living and (random.random() < self.model.fallowDeer_reproduce/np.log10(self.model.schedule.get_breed_count(fallowDeer)+ 1)) and (5 <= self.model.get_month() < 7):
            # Create a new fallow deer and divide energy:
            self.energy = np.random.uniform(0, self.energy)
            fawn = fallowDeer(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
            self.model.grid.place_agent(fawn, self.pos)
            self.model.schedule.add(fawn)


class redDeer(RandomWalker):
    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.count_eaten = defaultdict(int)
        self.energy = energy

    def step(self):
        # move & reduce energy
        self.mixedDiet_move()
        living = True
        self.energy -= 1

        self.count_eaten.clear()
        # Eat what's on my patch: roe deer are broswers, so randomly choose any habitat to eat
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        habitat_choices = ["saplings", "trees", "scrub", "youngScrub", "grass"]
        # pick a habitat type and eat it 
        for _ in range(len(habitat_choices)):
            if self.energy < 1:
                # pick a habitat type
                my_choice = rchoice(habitat_choices)
                habitat_choices.remove(my_choice)
                # if my energy is low enough, eat it 
                if my_choice == "saplings":
                    eatenSaps = math.ceil((1-self.energy)/self.model.redDeer_gain_from_Saplings)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenSaps >= habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800))):
                        eatenSaps = habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800)))
                    eat_saplings(habitat_patch, eatenSaps)
                    self.energy += (self.model.redDeer_gain_from_Saplings * eatenSaps)
                    self.count_eaten[my_choice] += eatenSaps
                elif my_choice == "trees":
                    eatenTrees = math.ceil((1-self.energy)/self.model.redDeer_gain_from_Trees)
                    if eatenTrees >= habitat_patch.edibles["trees"]:
                        eatenTrees = habitat_patch.edibles["trees"]
                    eat_trees(habitat_patch, eatenTrees)
                    self.energy += (self.model.redDeer_gain_from_Trees * eatenTrees)
                    self.count_eaten[my_choice] += eatenTrees
                elif my_choice == "scrub":
                    eatenScrub = math.ceil((1-self.energy)/self.model.redDeer_gain_from_Scrub)
                    if eatenScrub >= habitat_patch.edibles['scrub']:
                        eatenScrub = habitat_patch.edibles['scrub']
                    eat_scrub(habitat_patch, eatenScrub)
                    self.energy += (self.model.redDeer_gain_from_Scrub * eatenScrub)
                    self.count_eaten[my_choice] += eatenScrub
                elif my_choice == "youngScrub":
                    eatenYoungScrub = math.ceil((1-self.energy)/self.model.redDeer_gain_from_YoungScrub)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenYoungScrub >= habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800))):
                        eatenYoungScrub = habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800)))
                    eat_youngscrub(habitat_patch, eatenYoungScrub)
                    self.energy += (self.model.redDeer_gain_from_YoungScrub * eatenYoungScrub)
                    self.count_eaten[my_choice] += eatenYoungScrub
                elif my_choice == "grass":
                    eatenGrass = math.ceil((1-self.energy)/self.model.redDeer_gain_from_grass)
                    if eatenGrass >= habitat_patch.edibles["grass"]:
                        eatenGrass = habitat_patch.edibles["grass"]
                    eat_grass(habitat_patch, eatenGrass)
                    self.energy += (self.model.redDeer_gain_from_grass * eatenGrass)
                    self.count_eaten[my_choice] += eatenGrass
            else:
                break
            # don't let energy be above 1; do a break and >= 1
            if self.energy >= 1:
                self.energy = 1

        # if red deer's energy is less than 0, die 
        if self.energy <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        # I reproduce in May & June (assuming model starts in Jan at beginning of year, May & June = time steps 5&6 out of every 12 months)
        if living and (random.random() < self.model.redDeer_reproduce/np.log10(self.model.schedule.get_breed_count(redDeer)+ 1)) and (5 <= self.model.get_month() < 7):
            # Create a new roe deer and divide energy:
            self.energy = np.random.uniform(0, self.energy)
            fawn = redDeer(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
            self.model.grid.place_agent(fawn, self.pos)
            self.model.schedule.add(fawn)



class tamworthPigs(RandomWalker):
    def __init__(self, unique_id, pos, model, moore, energy, condition):
        super().__init__(unique_id, pos, model, moore=moore)
        self.count_eaten = defaultdict(int)
        self.energy = energy
        self.pregnancy_timer = None
        self.condition = condition

    def step(self):
        # move & reduce energy
        self.random_move()
        living = True
        self.energy -= 1

        self.count_eaten.clear()
        # Eat what's on my patch: roe deer are broswers, so randomly choose any habitat to eat
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        habitat_choices = ["saplings", "trees", "scrub", "youngScrub", "grass"]
        # pick a habitat type and eat it 
        for _ in range(len(habitat_choices)):
            if self.energy < 1:
                # pick a habitat type
                my_choice = rchoice(habitat_choices)
                habitat_choices.remove(my_choice)
                # if my energy is low enough, eat it 
                if my_choice == "saplings":
                    eatenSaps = math.ceil((1-self.energy)/self.model.pigs_gain_from_Saplings)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenSaps >= habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800))):
                        eatenSaps = habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/800)))
                    eat_saplings(habitat_patch, eatenSaps)
                    self.energy += (self.model.pigs_gain_from_Saplings * eatenSaps)
                    self.count_eaten[my_choice] += eatenSaps
                elif my_choice == "youngScrub":
                    eatenYoungScrub = math.ceil((1-self.energy)/self.model.pigs_gain_from_YoungScrub)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenYoungScrub >= habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800))):
                        eatenYoungScrub = habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/800)))
                    eat_youngscrub(habitat_patch, eatenYoungScrub)
                    self.energy += (self.model.pigs_gain_from_YoungScrub * eatenYoungScrub)
                    self.count_eaten[my_choice] += eatenYoungScrub
                elif my_choice == "grass":
                    eatenGrass = math.ceil((1-self.energy)/self.model.pigs_gain_from_grass)
                    if eatenGrass >= habitat_patch.edibles["grass"]:
                        eatenGrass = habitat_patch.edibles["grass"]
                    eat_grass(habitat_patch, eatenGrass)
                    self.energy += (self.model.pigs_gain_from_grass * eatenGrass)
                    self.count_eaten[my_choice] += eatenGrass
                elif my_choice == "trees":
                    eatenTrees = math.ceil((1-self.energy)/self.model.pigs_gain_from_Trees)
                    if eatenTrees >= habitat_patch.edibles["trees"]:
                        eatenTrees = habitat_patch.edibles["trees"]
                    eat_trees(habitat_patch, eatenTrees)
                    self.energy += (self.model.pigs_gain_from_Trees * eatenTrees)
                    self.count_eaten[my_choice] += eatenTrees
                elif my_choice == "scrub":
                    eatenScrub = math.ceil((1-self.energy)/self.model.pigs_gain_from_Scrub)
                    if eatenScrub >= habitat_patch.edibles['scrub']:
                        eatenScrub = habitat_patch.edibles['scrub']
                    eat_scrub(habitat_patch, eatenScrub)
                    self.energy += (self.model.pigs_gain_from_Scrub * eatenScrub)
                    self.count_eaten[my_choice] += eatenScrub
            else:
                break
            # don't let energy be above 1; do a break and >= 1
            if self.energy >= 1:
                self.energy = 1
    
        # if pig's energy is less than 0, die 
        if self.energy <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        if self.pregnancy_timer != None: 
            self.pregnancy_timer = self.pregnancy_timer - 1
            if self.pregnancy_timer == 0:
                self.giveBirth()
                self.pregnancy_timer = None

        # are there boars here? 
        all_pigs = self.model.schedule.agents_by_breed[tamworthPigs].items()
        boars_here = [i for (k, i) in all_pigs if i.condition == "boar"]
        # if there are, set the timer so other pigs reproduce in a few months
        if len(boars_here) > 0 and self.condition == "sow" and living and self.pregnancy_timer == None and (random.random() < self.model.pigs_reproduce/np.log10(self.model.schedule.get_breed_count(tamworthPigs)+ 1)):
            self.pregnancy_timer = random.randint(2,4)
            # divide my energy
            self.energy = np.random.uniform(0, self.energy)

    def giveBirth(self):
        # Pick a number of piglets to have
        number_piglets = np.random.binomial(n=10, p=0.5)
        for _ in range(number_piglets):
            piglet = tamworthPigs(self.model.next_id(), self.pos, self.model, self.moore, self.energy, self.condition)
            piglet.condition = "piglet"
            self.model.grid.place_agent(piglet, self.pos)
            self.model.schedule.add(piglet)



                                # # # # ------ Define the model ------ # # # # 

class KneppModel(Model):

    def __init__(self,             
            chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
            chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
            initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland,
            roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
            ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
            cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
            fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
            redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
            pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Trees, pigs_gain_from_Scrub, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
            fallowDeer_stocking, cattle_stocking, redDeer_stocking, tamworthPig_stocking, exmoor_stocking,
            reproduce_bison, bison_gain_from_grass, bison_gain_from_Trees, bison_gain_from_Scrub, bison_gain_from_Saplings, bison_gain_from_YoungScrub,
            reproduce_elk, elk_gain_from_grass, elk_gain_from_Trees, elk_gain_from_Scrub, elk_gain_from_Saplings, elk_gain_from_YoungScrub,
            reproduce_reindeer, reindeer_gain_from_grass, reindeer_gain_from_Trees, reindeer_gain_from_Scrub, reindeer_gain_from_Saplings, reindeer_gain_from_YoungScrub,
            width, height, max_time, reintroduction, introduce_euroBison, introduce_elk, introduce_reindeer):

        self.steps = 0
        # set parameters
        self.initial_roeDeer = round(100*initial_roeDeer)
        self.initial_grassland = round(100*initial_grassland)
        self.initial_woodland = round(100*initial_woodland)
        self.initial_scrubland = round(100*initial_scrubland)
        self.chance_reproduceSapling = chance_reproduceSapling
        self.chance_reproduceYoungScrub = chance_reproduceYoungScrub
        self.chance_regrowGrass = chance_regrowGrass
        self.chance_saplingBecomingTree = chance_saplingBecomingTree
        self.chance_youngScrubMatures = chance_youngScrubMatures
        self.chance_scrubOutcompetedByTree = chance_scrubOutcompetedByTree
        self.chance_saplingOutcompetedByScrub = chance_saplingOutcompetedByScrub
        if self.chance_saplingOutcompetedByScrub > 1: self.chance_saplingOutcompetedByScrub == 1

        self.chance_grassOutcompetedByTree = chance_grassOutcompetedByTree
        if self.chance_grassOutcompetedByTree > 1: self.chance_grassOutcompetedByTree == 1

        self.chance_grassOutcompetedByScrub = chance_grassOutcompetedByScrub
        if self.chance_grassOutcompetedByScrub > 1: self.chance_grassOutcompetedByScrub == 1
        self.chance_saplingOutcompetedByTree = chance_saplingOutcompetedByTree
        if self.chance_saplingOutcompetedByTree > 1: self.chance_saplingOutcompetedByTree == 1
        self.chance_youngScrubOutcompetedByScrub = chance_youngScrubOutcompetedByScrub
        self.chance_youngScrubOutcompetedByTree = chance_youngScrubOutcompetedByTree
        # roe deer parameters
        self.roeDeer_gain_from_grass = roeDeer_gain_from_grass
        self.roeDeer_gain_from_Trees = roeDeer_gain_from_Trees
        self.roeDeer_gain_from_Scrub = roeDeer_gain_from_Scrub
        self.roeDeer_gain_from_Saplings = roeDeer_gain_from_Saplings
        self.roeDeer_gain_from_YoungScrub = roeDeer_gain_from_YoungScrub
        self.roeDeer_reproduce = roeDeer_reproduce
        # exmoor pony parameters
        self.ponies_gain_from_grass = ponies_gain_from_grass
        self.ponies_gain_from_Trees =ponies_gain_from_Trees
        self.ponies_gain_from_Scrub = ponies_gain_from_Scrub
        self.ponies_gain_from_Saplings = ponies_gain_from_Saplings
        self.ponies_gain_from_YoungScrub = ponies_gain_from_YoungScrub
        # cow parameters
        self.cows_reproduce = cows_reproduce
        self.cows_gain_from_grass = cows_gain_from_grass
        self.cows_gain_from_Trees =cows_gain_from_Trees
        self.cows_gain_from_Scrub = cows_gain_from_Scrub
        self.cows_gain_from_Saplings = cows_gain_from_Saplings
        self.cows_gain_from_YoungScrub = cows_gain_from_YoungScrub
        # fallow deer parameters
        self.fallowDeer_reproduce = fallowDeer_reproduce
        self.fallowDeer_gain_from_grass = fallowDeer_gain_from_grass
        self.fallowDeer_gain_from_Trees =fallowDeer_gain_from_Trees
        self.fallowDeer_gain_from_Scrub = fallowDeer_gain_from_Scrub
        self.fallowDeer_gain_from_Saplings = fallowDeer_gain_from_Saplings
        self.fallowDeer_gain_from_YoungScrub = fallowDeer_gain_from_YoungScrub
        # red deer parameters
        self.redDeer_reproduce = redDeer_reproduce
        self.redDeer_gain_from_grass = redDeer_gain_from_grass
        self.redDeer_gain_from_Trees =redDeer_gain_from_Trees
        self.redDeer_gain_from_Scrub = redDeer_gain_from_Scrub
        self.redDeer_gain_from_Saplings = redDeer_gain_from_Saplings
        self.redDeer_gain_from_YoungScrub = redDeer_gain_from_YoungScrub
        # pig parameters
        self.pigs_reproduce = pigs_reproduce
        self.pigs_gain_from_grass = pigs_gain_from_grass
        self.pigs_gain_from_Trees = pigs_gain_from_Trees
        self.pigs_gain_from_Scrub = pigs_gain_from_Scrub
        self.pigs_gain_from_Saplings = pigs_gain_from_Saplings
        self.pigs_gain_from_YoungScrub = pigs_gain_from_YoungScrub
        # other parameters
        self.height = height
        self.width = width
        self.max_time = max_time
        self.reintroduction = reintroduction
        self.introduce_euroBison = introduce_euroBison
        self.introduce_elk = introduce_elk
        self.introduce_reindeer = introduce_reindeer
        # stocking densities
        self.fallowDeer_stocking = fallowDeer_stocking
        self.cattle_stocking = cattle_stocking
        self.redDeer_stocking = redDeer_stocking
        self.tamworthPig_stocking = tamworthPig_stocking
        self.exmoor_stocking = exmoor_stocking
        # euro bison parameters
        self.reproduce_bison = reproduce_bison
        self.bison_gain_from_grass = bison_gain_from_grass
        self.bison_gain_from_Trees = bison_gain_from_Trees 
        self.bison_gain_from_Scrub = bison_gain_from_Scrub
        self.bison_gain_from_Saplings = bison_gain_from_Saplings
        self.bison_gain_from_YoungScrub = bison_gain_from_YoungScrub
        # elk parameters
        self.reproduce_elk = reproduce_elk
        self.elk_gain_from_grass = elk_gain_from_grass
        self.elk_gain_from_Trees = elk_gain_from_Trees
        self.elk_gain_from_Scrub = elk_gain_from_Scrub
        self.elk_gain_from_Saplings = elk_gain_from_Saplings
        self.elk_gain_from_YoungScrub = elk_gain_from_YoungScrub
        # reindeer parameters
        self.reproduce_reindeer = reproduce_reindeer
        self.reindeer_gain_from_grass = reindeer_gain_from_grass
        self.reindeer_gain_from_Trees = reindeer_gain_from_Trees
        self.reindeer_gain_from_Scrub = reindeer_gain_from_Scrub
        self.reindeer_gain_from_Saplings = reindeer_gain_from_Saplings
        self.reindeer_gain_from_YoungScrub = reindeer_gain_from_YoungScrub

        # set grid & schedule
        self.grid = MultiGrid(width, height, False) # this grid allows for multiple agents on same cell
        self.schedule = RandomActivationByBreed(self)
        self.current_id = 0

        
        # Create habitat patches
        if (self.initial_woodland + self.initial_grassland + self.initial_scrubland) > 100:
            # rescale it to 100 and make bare ground 0
            prob_grassland = self.initial_grassland/(self.initial_woodland + self.initial_grassland + self.initial_scrubland)
            prob_scrubland = self.initial_scrubland/(self.initial_woodland + self.initial_grassland + self.initial_scrubland)
            prob_woodland = self.initial_woodland/(self.initial_woodland + self.initial_grassland + self.initial_scrubland)
            prob_bare_ground = 0
        else:
            prob_grassland = initial_grassland
            prob_scrubland = initial_scrubland
            prob_woodland = initial_woodland
            prob_bare_ground = 1-(initial_grassland + initial_scrubland + initial_woodland)
        condition = random.choices(["grassland", "thorny_scrubland", "woodland", "bare_ground"], weights=(prob_grassland, prob_scrubland, prob_woodland, prob_bare_ground), k=self.height*self.width)            
        
        for cell, condit, in zip(self.grid.coord_iter(), condition):
            # put a random number of trees, shrubs, etc., depending on dominant condition
            i, x, y = cell
            my_condition = condit
            if my_condition == 'grassland': # more than 50% grassland, no more than 10 mature trees/shrubs
                trees_here = random.randint(0, 49)
                saplings_here = 0
                scrub_here = random.randint(0, 99)
                youngscrub_here = 0
                perc_grass_here = random.randint(50, 100)
                perc_bareground_here = 100 - perc_grass_here
            elif my_condition == "thorny_scrubland":  # at least 10 scrub plants, no more than 10 trees
                trees_here = random.randint(0, 49)
                saplings_here = random.randint(0, 50)
                scrub_here = random.randint(100, 800)
                youngscrub_here = random.randint(0, 50)
                perc_grass_here = random.randint(0, 100)
                perc_bareground_here = 100 - perc_grass_here
            elif my_condition == "woodland":  # woodland has 10-100 trees
                trees_here = random.randint(50, 400)
                saplings_here = random.randint(0, 50)
                scrub_here = random.randint(0, 80)
                youngscrub_here = random.randint(0, 50)
                perc_grass_here = random.randint(0, 100)
                perc_bareground_here = 100 - perc_grass_here
            elif my_condition == "bare_ground": # more than 50% bare ground
                trees_here = random.randint(0, 49)
                # trees_here = 0
                saplings_here = 0
                scrub_here = random.randint(0, 99)
                # scrub_here = 0
                youngscrub_here = 0
                perc_bareground_here = random.randint(51, 100)
                # perc_bareground_here = 100
                perc_grass_here = 100 - perc_bareground_here
            patch = habitatAgent(self.next_id(), (x, y), self, my_condition, trees_here, saplings_here, scrub_here, youngscrub_here, perc_grass_here, perc_bareground_here)
            self.grid.place_agent(patch, (x, y))
            self.schedule.add(patch)


        # Create roe deer
        for i in range(self.initial_roeDeer):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            energy = np.random.uniform(0, 1)
            roe = roeDeer(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(roe, (x, y))
            self.schedule.add(roe)


        # get data organized
        self.datacollector = DataCollector(
                        model_reporters = {
                        # number and type of habitats
                        "Time": lambda m: m.schedule.time, 
                        "Roe deer": lambda m: m.schedule.get_breed_count(roeDeer),
                        "Exmoor pony": lambda m: m.schedule.get_breed_count(exmoorPony),
                        "Fallow deer": lambda m: m.schedule.get_breed_count(fallowDeer),
                        "Longhorn cattle": lambda m: m.schedule.get_breed_count(longhornCattle),
                        "Red deer": lambda m: m.schedule.get_breed_count(redDeer),
                        "Tamworth pigs": lambda m: m.schedule.get_breed_count(tamworthPigs),
                        "European bison": lambda m: m.schedule.get_breed_count(euroBison),
                        "European elk": lambda m: m.schedule.get_breed_count(euroElk),
                        "Reindeer": lambda m: m.schedule.get_breed_count(reindeer),

                        # number of habitat types
                        "Grass": lambda m: self.count_habitat_numbers(m, "grass"),
                        "Trees": lambda m: self.count_habitat_numbers(m, "trees"),
                        "Mature Scrub": lambda m: self.count_habitat_numbers(m, "scrub"),
                        "Saplings": lambda m: self.count_habitat_numbers(m, "saplings"),
                        "Young Scrub": lambda m: self.count_habitat_numbers(m,"youngScrub"),
                        "Bare Areas": lambda m: self.count_habitat_numbers(m, "bare_ground"),
                        # percentage habitat conditions
                        "Grassland": lambda m: self.count_condition(m, "grassland"),
                        "Woodland": lambda m: self.count_condition(m, "woodland"),
                        "Thorny Scrub": lambda m: self.count_condition(m, "thorny_scrubland"),
                        "Bare ground": lambda m: self.count_condition(m, "bare_ground"),

                        # what's killing saplings? 
                        "Saplings grown up": lambda m: self.count_habitats_grew(m, "saplings"),
                        "Saplings Outcompeted by Trees": lambda m: self.count_habitats_outcompeted_trees(m, "saplings"),
                        "Saplings Outcompeted by Scrub": lambda m: self.count_habitats_outcompeted_scrub(m, "saplings"),
                        "Saplings eaten by roe deer": lambda m: self.count_eaten(m, roeDeer, "saplings"),
                        "Saplings eaten by Exmoor pony": lambda m: self.count_eaten(m, exmoorPony, "saplings"),
                        "Saplings eaten by Fallow deer": lambda m: self.count_eaten(m, fallowDeer, "saplings"),
                        "Saplings eaten by longhorn cattle": lambda m: self.count_eaten(m, longhornCattle, "saplings"),
                        "Saplings eaten by red deer": lambda m: self.count_eaten(m, redDeer, "saplings"),
                        "Saplings eaten by pigs": lambda m: self.count_eaten(m, tamworthPigs, "saplings"),
                        # what about young scrub?
                        "Young scrub grown up": lambda m: self.count_habitats_grew(m, "youngScrub"),
                        "Young Scrub Outcompeted by Trees": lambda m: self.count_habitats_outcompeted_trees(m, "youngScrub"), 
                        "Young Scrub Outcompeted by Scrub": lambda m: self.count_habitats_outcompeted_scrub(m, "youngScrub"), 
                        "Young Scrub eaten by roe deer": lambda m: self.count_eaten(m, roeDeer, "youngScrub"),
                        "Young Scrub eaten by Exmoor pony": lambda m: self.count_eaten(m, exmoorPony, "youngScrub"),
                        "Young Scrub eaten by Fallow deer": lambda m: self.count_eaten(m, fallowDeer, "youngScrub"),
                        "Young Scrub eaten by longhorn cattle": lambda m: self.count_eaten(m, longhornCattle, "youngScrub"),
                        "Young Scrub eaten by red deer": lambda m: self.count_eaten(m, redDeer, "youngScrub"),
                        "Young Scrub eaten by pigs": lambda m: self.count_eaten(m, tamworthPigs, "youngScrub"),
                        # what's eating grass? 
                        "Grass Outcompeted by Trees": lambda m: self.count_habitats_outcompeted_trees(m, "grass"),
                        "Grass Outcompeted by Scrub": lambda m: self.count_habitats_outcompeted_scrub(m, "grass"),
                        "Grass eaten by roe deer": lambda m: self.count_eaten(m, roeDeer, "grass"),
                        "Grass eaten by Exmoor pony": lambda m: self.count_eaten(m, exmoorPony, "grass"),
                        "Grass eaten by Fallow deer": lambda m: self.count_eaten(m, fallowDeer, "grass"),
                        "Grass eaten by longhorn cattle": lambda m: self.count_eaten(m, longhornCattle, "grass"),
                        "Grass eaten by red deer": lambda m: self.count_eaten(m, redDeer, "grass"),
                        "Grass eaten by pigs": lambda m: self.count_eaten(m, tamworthPigs, "grass"),
                        # what's killing scrub? 
                        "Scrub Outcompeted by Trees": lambda m: self.count_habitats_outcompeted_trees(m, "scrub"),
                        "Scrub eaten by roe deer": lambda m: self.count_eaten(m, roeDeer, "scrub"),
                        "Scrub eaten by Exmoor pony": lambda m: self.count_eaten(m, exmoorPony, "scrub"),
                        "Scrub eaten by Fallow deer": lambda m: self.count_eaten(m, fallowDeer, "scrub"),
                        "Scrub eaten by longhorn cattle": lambda m: self.count_eaten(m, longhornCattle, "scrub"),
                        "Scrub eaten by red deer": lambda m: self.count_eaten(m, redDeer, "scrub"),
                        "Scrub eaten by pigs": lambda m: self.count_eaten(m, tamworthPigs, "scrub"),
                        # how many trees are being eaten? 
                        "Trees eaten by roe deer": lambda m: self.count_eaten(m, roeDeer, "trees"),
                        "Trees eaten by Exmoor pony": lambda m: self.count_eaten(m, exmoorPony, "trees"),
                        "Trees eaten by Fallow deer": lambda m: self.count_eaten(m, fallowDeer, "trees"),
                        "Trees eaten by longhorn cattle": lambda m: self.count_eaten(m, longhornCattle, "trees"),                   
                        "Trees eaten by red deer": lambda m: self.count_eaten(m, redDeer, "trees"),
                        "Trees eaten by pigs": lambda m: self.count_eaten(m, tamworthPigs, "trees"),
                        },

                        # where are the animals at each timestep
                        agent_reporters = {
                        "Breed": lambda agent: agent.__class__.__name__ if (agent.__class__.__name__ != "habitatAgent") else agent.condition,
                        "ID": lambda agent: agent.unique_id,
                        "Energy": lambda agent: agent.energy if (agent.__class__.__name__ != "habitatAgent") else None,
                        "X": lambda agent: agent.pos[0],
                        "Y": lambda agent: agent.pos[1],

                        }
                        )

        self.running = True
        self.datacollector.collect(self)


    def track_position(self, model, breed):
        # want to count the xy coords of each animal
        for key, value in model.schedule.agents_by_breed[breed].items():
            return value.pos, value.unique_id

    def count_habitats_outcompeted_scrub(self, model, habitat_type):
        # want to count grass, wood, scrub, bare ground in each patch
        count_item = 0
        for key, value in model.schedule.agents_by_breed[habitatAgent].items():
            count_item += value.habs_outcompeted_byScrub[habitat_type]
        return count_item

    def count_habitats_outcompeted_trees(self, model, habitat_type):
        # want to count grass, wood, scrub, bare ground in each patch
        count_item = 0
        for key, value in model.schedule.agents_by_breed[habitatAgent].items():
            count_item += value.habs_outcompeted_byTrees[habitat_type]
        return count_item

    def count_habitats_grew(self, model, habitat_type):
        # want to count grass, wood, scrub, bare ground in each patch
        count_item = 0
        for key, value in model.schedule.agents_by_breed[habitatAgent].items():
            count_item += value.habs_grew_up[habitat_type]
        return count_item

    def count_eaten(self, model, breed, eaten_thing):
        count_item = 0
        # want to count grass, wood, scrub, bare ground in each patch
        for key, value in model.schedule.agents_by_breed[breed].items():
            count_item += value.count_eaten[eaten_thing]
        return count_item

    def count_condition(self, model, habitat_condition):
        # want to count grass, wood, scrub, bare ground in each patch
        count = 0
        for key, value in model.schedule.agents_by_breed[habitatAgent].items():
            if value.condition == habitat_condition:
                count += 1
        # return percentage of entire area
        return round((count/450)*100)

    def count_habitat_numbers(self, model, habitat_thing):
        # want to count grass, wood, scrub, bare ground in each patch
        count_item = 0
        for key, value in model.schedule.agents_by_breed[habitatAgent].items():
            count_item += value.edibles[habitat_thing]
        # return percentage of entire area
        return count_item

    def count_food(self, model, kind_eaten, habitat_type = None):
        # want to count grass, wood, scrub, bare ground in each patch
        count_item = 0
        for key, value in model.schedule.agents_by_breed[habitatAgent].items():
            if habitat_type == None or habitat_type == value.condition:
                count_item += value.edibles[kind_eaten]
            else:
                count_item += 0
        # return percentage of entire area
        return count_item

    def add_herbivores(self, herbivore, count):
        x = random.randrange(self.width)
        y = random.randrange(self.height)
        energy = np.random.uniform(0, 1)
        for i in range(count):
            to_add = herbivore(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(to_add, (x, y))
            self.schedule.add(to_add)

    def remove_herbivores(self, herbivore, count):
        to_remove = self.schedule.agents_by_breed[herbivore].items()
        my_choices = random.sample(list(to_remove), k = min(count, len(to_remove)))
        for my_choice in my_choices:
            my_choice = my_choice[1]
            self.grid._remove_agent(my_choice.pos, my_choice)
            self.schedule.remove(my_choice)

    def add_pig(self, herbivore, count_piglets, count_sow, count_boar):
        x = random.randrange(self.width)
        y = random.randrange(self.height)
        energy = np.random.uniform(0, 1)
        for i in range(count_piglets):
            condition = "piglet"
            to_add = herbivore(self.next_id(), (x, y), self, True, energy, condition)
            self.grid.place_agent(to_add, (x, y))
            self.schedule.add(to_add)
        for i in range(count_sow):
            condition = "sow"
            to_add = herbivore(self.next_id(), (x, y), self, True, energy, condition)
            self.grid.place_agent(to_add, (x, y))
            self.schedule.add(to_add)
        for i in range(count_boar):
            condition = "boar"
            to_add = herbivore(self.next_id(), (x, y), self, True, energy, condition)
            self.grid.place_agent(to_add, (x, y))
            self.schedule.add(to_add)


    def remove_pig(self, herbivore, count_piglets, count_sow, count_boar):
        to_remove = self.schedule.agents_by_breed[herbivore].items()
        to_remove_piglets = [i for (k, i) in to_remove if i.condition == "piglet"]
        to_remove_sow = [i for (k, i) in to_remove if i.condition == "sow"]
        to_remove_boars = [i for (k, i) in to_remove if i.condition == "boar"]
        my_choice_piglet = random.sample(list(to_remove_piglets), k = min(count_piglets, len(to_remove_piglets)))
        my_choice_sow = random.sample(list(to_remove_sow), k = min(count_sow, len(to_remove_sow)))
        my_choices_boar = random.sample(list(to_remove_boars), k = min(count_boar, len(to_remove_boars)))

        # remove non-boars
        for my_choice in my_choice_piglet:
            my_choice = my_choice
            self.grid._remove_agent(my_choice.pos, my_choice)
            self.schedule.remove(my_choice)
        for my_choice_sows in my_choice_sow:
            my_choice_sow = my_choice_sows
            self.grid._remove_agent(my_choice_sow.pos, my_choice_sow)
            self.schedule.remove(my_choice_sow)
        # remove boars
        for my_choice_boar in my_choices_boar:
            my_choice_boar = my_choice_boar
            self.grid._remove_agent(my_choice_boar.pos, my_choice_boar)
            self.schedule.remove(my_choice_boar)
    
    def get_month(self):
        return (self.schedule.time % 12) + 1


    def step(self):
        self.schedule.step()
        # count how many there are, then step
        self.datacollector.collect(self)
        
        if self.reintroduction == True: 
            # Jan 2005 - March 2009
            if self.schedule.time == 49:
                self.add_herbivores(exmoorPony, 23)
                self.add_herbivores(longhornCattle, 53)
                number_sows = random.randint(4,8)
                number_piglets = 20-number_sows
                self.add_pig(tamworthPigs, number_piglets, number_sows, 0)
            # March 2010
            if self.schedule.time == 61: 
                results_2 = self.datacollector.get_model_vars_dataframe()
                exmoorValue = results_2.iloc[61]['Exmoor pony']
                if exmoorValue >= 13: # randomly choose that many exmoor ponies and delete them
                    number_to_subtract = -13 + exmoorValue
                    self.remove_herbivores(exmoorPony, number_to_subtract)
                else:
                    number_to_add = 13 - exmoorValue
                    self.add_herbivores(exmoorPony, number_to_add)
                cowValue = results_2.iloc[61]['Longhorn cattle']
                if cowValue >= 77:
                    number_to_subtract = -77 + cowValue
                    self.remove_herbivores(longhornCattle, number_to_subtract)
                else:
                    number_to_add = 77 - cowValue
                    self.add_herbivores(longhornCattle, number_to_add)
                fallowValue = results_2.iloc[61]['Fallow deer']
                if fallowValue >= 42:
                    number_to_subtract = -42 + fallowValue
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                else:
                    number_to_add = 42 - fallowValue
                    self.add_herbivores(fallowDeer, number_to_add)

                pigsValue = results_2.iloc[61]['Tamworth pigs']

                if pigsValue >= 17:
                    number_to_subtract = -17 + pigsValue
                    self.remove_pig(tamworthPigs, number_to_subtract, 0, 0)
                else:
                    number_to_add = 17 - pigsValue
                    self.add_pig(tamworthPigs, number_to_add, 0, 0)

            # 2011
            if self.schedule.time == 73:
                results_3 = self.datacollector.get_model_vars_dataframe()
                exmoorValue = results_3.iloc[73]['Exmoor pony']
                if exmoorValue >= 15: # randomly choose that many exmoor ponies and delete them
                    number_to_subtract = -15 + exmoorValue
                    self.remove_herbivores(exmoorPony, number_to_subtract)
                else:
                    number_to_add = 15 - exmoorValue
                    self.add_herbivores(exmoorPony, number_to_add)
                cowValue = results_3.iloc[73]['Longhorn cattle']
                if cowValue >= 92:
                    number_to_subtract = -92 + cowValue
                    self.remove_herbivores(longhornCattle, number_to_subtract)
                else:
                    number_to_add = 92 - cowValue
                    self.add_herbivores(longhornCattle, number_to_add)
                fallowValue = results_3.iloc[73]['Fallow deer']
                if fallowValue >= 81:
                    number_to_subtract = -81 + fallowValue
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                else:
                    number_to_add = 81 - fallowValue
                    self.add_herbivores(fallowDeer, number_to_add)
                pigsValue = results_3.iloc[73]['Tamworth pigs']
                if pigsValue >= 22:
                    number_to_subtract = -22 + pigsValue
                    self.remove_pig(tamworthPigs, number_to_subtract, 0, 0)
                else:
                    number_to_add = 22 - pigsValue
                    self.add_pig(tamworthPigs, number_to_add, 0, 0)
            # 2012
            if self.schedule.time == 85:
                results_4 = self.datacollector.get_model_vars_dataframe()
                exmoorValue = results_4.iloc[85]['Exmoor pony']
                if exmoorValue >= 17: # randomly choose that many exmoor ponies and delete them
                    number_to_subtract = -17 + exmoorValue
                    self.remove_herbivores(exmoorPony, number_to_subtract)
                else:
                    number_to_add = 17 - exmoorValue
                    self.add_herbivores(exmoorPony, number_to_add)
                cowValue = results_4.iloc[85]['Longhorn cattle']
                if cowValue >= 116:
                    number_to_subtract = -116 + cowValue
                    self.remove_herbivores(longhornCattle, number_to_subtract)
                else:
                    number_to_add = 116 - cowValue
                    self.add_herbivores(longhornCattle, number_to_add)
                fallowValue = results_4.iloc[85]['Fallow deer']
                if fallowValue >= 100:
                    number_to_subtract = -100 + fallowValue
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                else:
                    number_to_add = 100 - fallowValue
                    self.add_herbivores(fallowDeer, number_to_add)
                pigsValue = results_4.iloc[85]['Tamworth pigs']
                if pigsValue >= 33:
                    number_to_subtract = -33 + pigsValue
                    self.remove_pig(tamworthPigs, number_to_subtract, 0, 0)
                else:
                    number_to_add = 33 - pigsValue
                    self.add_pig(tamworthPigs, number_to_add, 0, 0)
            # 2013
            if self.schedule.time == 97:
                results_5 = self.datacollector.get_model_vars_dataframe()
                # Exmoor ponies: 10
                exmoorValue = results_5.iloc[97]['Exmoor pony']
                if exmoorValue >= 10: # randomly choose that many exmoor ponies and delete them
                    number_to_subtract = -10 + exmoorValue
                    self.remove_herbivores(exmoorPony, number_to_subtract)
                else:
                    number_to_add = 10 - exmoorValue
                    self.add_herbivores(exmoorPony, number_to_add)
                # Longhorn cattle: 129
                cowValue = results_5.iloc[97]['Longhorn cattle']
                if cowValue >= 129:
                    number_to_subtract = -129 + cowValue
                    self.remove_herbivores(longhornCattle, number_to_subtract)
                else:
                    number_to_add = 129 - cowValue
                    self.add_herbivores(longhornCattle, number_to_add)
                # Fallow deer: 100
                fallowValue = results_5.iloc[97]['Fallow deer']
                if fallowValue >= 100:
                    number_to_subtract = -100 + fallowValue
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                else:
                    number_to_add = 100 - fallowValue
                    self.add_herbivores(fallowDeer, number_to_add)
                # Pigs: 6
                pigsValue = results_5.iloc[97]['Tamworth pigs']
                if pigsValue >= 6:
                    number_to_subtract = -6 + pigsValue
                    self.remove_pig(tamworthPigs, number_to_subtract, 0, 0)
                else:
                    number_to_add = 6 - pigsValue
                    self.add_pig(tamworthPigs, number_to_add, 0, 0)
                # Red deer: add 13
                self.add_herbivores(redDeer, 13)
            # 2014
            if self.schedule.time == 109:
                results_6 = self.datacollector.get_model_vars_dataframe()
                exmoorValue = results_6.iloc[109]['Exmoor pony']
                if exmoorValue >= 10: # randomly choose that many exmoor ponies and delete them
                    number_to_subtract = -10 + exmoorValue
                    self.remove_herbivores(exmoorPony, number_to_subtract)
                else:
                    number_to_add = 10 - exmoorValue
                    self.add_herbivores(exmoorPony, number_to_add)
                cowValue = results_6.iloc[109]['Longhorn cattle']
                if cowValue >= 264:
                    number_to_subtract = -264 + cowValue
                    self.remove_herbivores(longhornCattle, number_to_subtract)
                else:
                    number_to_add = 264 - cowValue
                    self.add_herbivores(longhornCattle, number_to_add)
                fallowValue = results_6.iloc[109]['Fallow deer']
                if fallowValue >= 100:
                    number_to_subtract = -100 + fallowValue
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                else:
                    number_to_add = 100 - fallowValue
                    self.add_herbivores(fallowDeer, number_to_add)
                # Pigs: 18
                pigsValue = results_6.iloc[109]['Tamworth pigs']
                if pigsValue >= 18:
                    number_to_subtract = -18 + pigsValue
                    self.remove_pig(tamworthPigs, number_to_subtract, 0, 0)
                else:
                    number_to_add = 18 - pigsValue
                    self.add_pig(tamworthPigs, number_to_add, 0, 0)
                redDeerValue = results_6.iloc[109]['Red deer']
                if redDeerValue >= 13:
                    number_to_subtract = -13 + redDeerValue
                    self.remove_herbivores(redDeer, number_to_subtract)
                else:
                    number_to_add = 13 - redDeerValue
                    self.add_herbivores(redDeer, number_to_add)
            
            # Jan 2015 - assumed 1 boar added 
            if self.schedule.time == 119:
                self.add_pig(tamworthPigs, 0, 0, 1)
            # Feb 2015 - assumed 1 boar removed, -2 cows
            if self.schedule.time == 120:
                self.remove_pig(tamworthPigs, 0, 0, 1)
            
    
            # March 2015
            if self.schedule.time == 121:
                results_7 = self.datacollector.get_model_vars_dataframe()
                #  Exmoor ponies: 10
                exmoorValue = results_7.iloc[121]['Exmoor pony']
                if exmoorValue >= 10: # randomly choose that many exmoor ponies and delete them
                    number_to_subtract = -10 + exmoorValue
                    self.remove_herbivores(exmoorPony, number_to_subtract)
                else:
                    number_to_add = 10 - exmoorValue
                    self.add_herbivores(exmoorPony, number_to_add)
                # Longhorn cattle: 107
                cowValue = results_7.iloc[121]['Longhorn cattle']
                if cowValue >= 107:
                    number_to_subtract = -107 + cowValue
                    self.remove_herbivores(longhornCattle, number_to_subtract)
                else:
                    number_to_add = 107 - cowValue
                    self.add_herbivores(longhornCattle, number_to_add)
                # Fallow deer: 100
                fallowValue = results_7.iloc[121]['Fallow deer']
                if fallowValue >= 100:
                    number_to_subtract = -100 + fallowValue
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                else:
                    number_to_add = 100 - fallowValue
                    self.add_herbivores(fallowDeer, number_to_add)

                # Pigs: 18, there should be 5 sows and 13 piglets
                total_pigs = self.schedule.agents_by_breed[tamworthPigs].items()
                number_piglets = [i for (k, i) in total_pigs if i.condition == "piglet"]
                number_sows = [i for (k, i) in total_pigs if i.condition == "sow"]

                if len(number_piglets) >= 13:
                    number_to_subtract_piglets = -13 + len(number_piglets)
                    self.remove_pig(tamworthPigs, number_to_subtract_piglets, 0, 0)
                else:
                    number_to_add_piglets = 13 - len(number_piglets)
                    self.add_pig(tamworthPigs, number_to_add_piglets, 0, 0)

                if len(number_sows) >= 5:
                    number_to_subtract_sows = -5 + len(number_sows)
                    self.remove_pig(tamworthPigs, 0, number_to_subtract_sows, 0)
                else:
                    number_to_add_sows = 5 - len(number_sows)
                    self.add_pig(tamworthPigs, 0, number_to_add_sows, 0)

                # Red deer: 13
                redDeerValue = results_7.iloc[121]['Red deer']
                if redDeerValue >= 13:
                    number_to_subtract = -13 + redDeerValue
                    self.remove_herbivores(redDeer, number_to_subtract)
                else:
                    number_to_add = 13 - redDeerValue
                    self.add_herbivores(redDeer, number_to_add)

            # April 2015
            if self.schedule.time == 122:
                # April 2015: one sow culled
                self.remove_pig(tamworthPigs, 0, 1, 0)
            # May 2015
            if self.schedule.time == 123:
                # May 2015: 8 piglets culled
                self.remove_pig(tamworthPigs, 8, 0, 0)
            # June 2015: 5 cows culled
            if self.schedule.time == 124:
                self.remove_herbivores(longhornCattle, 5)
            # August 2015: 2 fallow deer culled
            if self.schedule.time == 126:
                self.remove_herbivores(fallowDeer, 2)
            # September 2015: 2 male fallow deer culled; 2 cattle culled and 3 bulls added
            if self.schedule.time == 128:
                self.remove_herbivores(fallowDeer, 2)
                self.add_herbivores(longhornCattle, 1)
            # Oct 2015: 2 female and 1 male fallow deer culled; 38 female cows and 1 bull removed
            if self.schedule.time == 128:
                self.remove_herbivores(fallowDeer, 3)
                self.remove_herbivores(longhornCattle, 39)
            # Nov 2015: -7 fallow deer, -1 piglet
            if self.schedule.time == 129:
                self.remove_herbivores(fallowDeer, 7)                 
                self.remove_pig(tamworthPigs, 1, 0, 0)       
            # Dec 2015: 6 fallow deer culled; 5 cows removed;
            if self.schedule.time == 130:
                self.remove_herbivores(fallowDeer, 6)
                self.remove_herbivores(longhornCattle, 5)
            # Jan 2016: 7 fallow deer culled; 4 pigs culled and 1 added
            if self.schedule.time == 131:
                self.remove_herbivores(fallowDeer, 7) 
                self.remove_pig(tamworthPigs, 4, 0, 0)
                self.add_pig(tamworthPigs, 0, 0, 1)
            # Feb 2016: 10 fallow deer culled; 2 pigs culled
            if self.schedule.time == 132:
                self.remove_herbivores(fallowDeer, 10)
                self.remove_pig(tamworthPigs, 2, 0, 0)
                                
                                        # # # # # # # 2016 # # # # # # #

            # March 2016: 1 pony added; 3 pigs added and 4 culled incl. 1 boar
            if self.schedule.time == 133:
                self.add_herbivores(exmoorPony, 1)
                self.remove_pig(tamworthPigs, 1, 0, 1)
                self.add_pig(tamworthPigs, 0, 3, 0)

            # April 2016: 1 cow added & filtering for cows;
            if self.schedule.time == 134:
                self.add_herbivores(longhornCattle, 1)
            # May 2016: filtering for cows and pigs, and 2 cows culled
            if self.schedule.time == 135:
                self.remove_herbivores(longhornCattle, 2)
            # June 2016: filtering for cows, 30 cows culled and 4 added 
            if self.schedule.time == 136:
                self.remove_herbivores(longhornCattle, 26)
            # July 2016: 2 cows culled
            if self.schedule.time == 137:
                self.remove_herbivores(longhornCattle, 2)
            # August 2016: -5 fallow deer
            if self.schedule.time == 138:
                self.remove_herbivores(fallowDeer, 5)
            # September & Oct 2016: -9, +19 cows
            if self.schedule.time == 139:
                self.add_herbivores(longhornCattle, 9)
            # November 2016: -3 fallow deer; -5 cows
            if self.schedule.time == 141:
                self.remove_herbivores(fallowDeer, 3)
                self.remove_herbivores(longhornCattle, 5)
            # December 2016: -9 fallow; -13 cows; -4 pigs
            if self.schedule.time == 142:
                self.remove_herbivores(fallowDeer, 9)
                self.remove_herbivores(longhornCattle, 13)
                self.remove_pig(tamworthPigs, 4, 0, 0)
            # January 2017: -4 pigs, +1 boar
            if self.schedule.time == 143:
                self.remove_pig(tamworthPigs, 2, 2, 0)
                self.add_pig(tamworthPigs, 0, 0, 1)
            # February 2017: -8 fallow deer; -3 pigs; filtering for ponies
            if self.schedule.time == 144:
                self.remove_herbivores(fallowDeer, 8)
                self.remove_pig(tamworthPigs, 1, 1, 1)


            # # # # # # # 2017 # # # # # # #
            # minus 1 exmoor pony, - some number of red deer; filtering for cows
            if self.schedule.time == 145:
                self.remove_herbivores(exmoorPony, 1)
                results_71 = self.datacollector.get_model_vars_dataframe()
                redDeerValue = results_71.iloc[145]['Red deer']
                if redDeerValue >= 14:
                    number_to_subtract = -14 + redDeerValue
                    self.remove_herbivores(redDeer, number_to_subtract)
                else:
                    number_to_add = 14 - redDeerValue
                    self.add_herbivores(redDeer, number_to_add)
            # April 2017: -3 cows, filtering for cows and pigs
            if self.schedule.time == 146:
                self.add_herbivores(longhornCattle, 3)
            # June & July 2017: -24 cows, +3 cows, and cow filtering condition
            if self.schedule.time == 148:
                self.remove_herbivores(longhornCattle, 21)
            # August 2017: -16 fallow deer 
            if self.schedule.time == 150:
                self.remove_herbivores(fallowDeer, 16)
            # September 2017: -5 fallow deer; -27, +23 cows
            if self.schedule.time == 151:
                self.remove_herbivores(fallowDeer, 5)
                self.remove_herbivores(longhornCattle, 2)
            # October 2017: -4 fallow deer; -2 cows
            if self.schedule.time == 152:
                self.remove_herbivores(fallowDeer, 4)
                self.remove_herbivores(longhornCattle, 2)
            # November 2017: -2 fallow deer
            if self.schedule.time == 153:
                self.remove_herbivores(fallowDeer, 2)
            # December 2017: -46 fallow deer, -1 red deer; -4 pigs
            if self.schedule.time == 154:
                self.remove_herbivores(fallowDeer, 46)
                self.remove_herbivores(redDeer, 1)
                self.remove_pig(tamworthPigs, 4, 0, 0)
            # January 2018: -9 pigs, +1 pig, and pig filtering conditions
            if self.schedule.time == 155:
                self.remove_pig(tamworthPigs, 9, 0, 0)
                self.add_pig(tamworthPigs, 0, 0, 1)
            # February 2018: -14 fallow; -1 red deer; -1 pig; filtering for pig and exmoor
            if self.schedule.time == 156:
                self.remove_herbivores(fallowDeer, 14)
                self.remove_herbivores(redDeer, 1)
                self.remove_pig(tamworthPigs, 0, 0, 1)

            # # # # # # # 2018 # # # # # # #
                
            # March 2018: -1 Exmoor; filtering for red deer, supplement fallow
            if self.schedule.time == 157:
                self.remove_herbivores(exmoorPony, 1)
                supp_fallow = self.datacollector.get_model_vars_dataframe()
                fallowValue = supp_fallow.iloc[157]['Fallow deer']
                if fallowValue >= 251: 
                    number_to_subtract = -251 + fallowValue
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                else:
                    number_to_add = 251 - fallowValue
                    self.add_herbivores(fallowDeer, number_to_add)
                self.remove_pig(tamworthPigs, 3, 0, 0)
                self.add_pig(tamworthPigs, 0, 3, 0)

            # April 2018: +1 cow and filtering for cow
            if self.schedule.time == 158:
                self.add_herbivores(longhornCattle, 1)
            # June 2018: -22 cows, +2 cows; filtering for cows
            if self.schedule.time == 160:
                self.remove_herbivores(longhornCattle, 18)
            # July 2018: -1 red deer; -1 pig
            if self.schedule.time == 161:
                self.remove_herbivores(redDeer, 1)
                self.remove_pig(tamworthPigs, 0, 1, 0)
            # August 2018: -9 ponies; -15 fallow deer; -1 cattle
            if self.schedule.time == 162:
                self.remove_herbivores(exmoorPony, 9)
                self.remove_herbivores(fallowDeer, 15)
                self.remove_herbivores(longhornCattle, 1)
                self.remove_herbivores(redDeer, 1)
            # September 2018: -19 fallow; -16 and +20 cows
            if self.schedule.time == 163:
                self.remove_herbivores(fallowDeer, 19)
                self.add_herbivores(longhornCattle, 4)
            # October 2018: -4 cows; -4 fallow; -1 pig
            if self.schedule.time == 164:
                self.remove_herbivores(longhornCattle, 5)
                self.remove_herbivores(fallowDeer, 4)
                self.remove_pig(tamworthPigs, 0, 1, 0)
            # November 2018: -8 cows; -12 pigs
            if self.schedule.time == 165:
                self.remove_herbivores(longhornCattle, 7)
                self.remove_pig(tamworthPigs, 11, 1, 0)
            # December & January 2018/2019: -19 fallow; -5 and +1 cow; -1 red deer 
            if self.schedule.time == 166:
                self.remove_herbivores(longhornCattle, 4)
                self.remove_herbivores(fallowDeer, 19)
                self.remove_herbivores(redDeer, 1)
            # February 2019: +1 pig, -2 cows
            if self.schedule.time == 168:
                self.add_pig(tamworthPigs, 0, 0, 1)                                                                                   
                self.remove_herbivores(longhornCattle, 2)
    

            # # # # # # # 2019 # # # # # # #

            # March 2019: -1 pig; fallow and red deer filters
            if self.schedule.time == 169:
                self.remove_herbivores(fallowDeer, 7)
                self.remove_herbivores(redDeer, 7)
                self.remove_pig(tamworthPigs, 5, 0, 0)                                                                                   
                self.add_pig(tamworthPigs, 0, 4, 0)                                                                                   


            if self.schedule.time == 170:
                self.remove_pig(tamworthPigs, 0, 0, 1)
            # June 2019: -28 cows and cow filtering condition
            if self.schedule.time == 172:
                self.remove_herbivores(longhornCattle, 28)
            # July & Aug 2019: -3, +5 cows; -27 pigs; filtering for pigs
            if self.schedule.time == 173:
                self.remove_pig(tamworthPigs, 27, 0, 0)
                self.add_herbivores(longhornCattle, 4)
            # Sept 2019: -15 fallow; -23 and +25 cows
            if self.schedule.time == 175:
                self.remove_herbivores(fallowDeer, 15)
                self.add_herbivores(longhornCattle, 2)
            # Oct 2019: -5 cows
            if self.schedule.time == 176:
                self.remove_herbivores(longhornCattle, 5)
            # November 2019: -7 fallow deer; -1 cows; -3 red deer
            if self.schedule.time == 177:
                self.remove_herbivores(longhornCattle, 1)
                self.remove_herbivores(fallowDeer, 7)
                self.remove_herbivores(redDeer, 3)
            # December 2019: -12 fallow; -7 cows; -4 red; +1 pigs
            if self.schedule.time == 178:
                self.remove_herbivores(fallowDeer, 12)
                self.remove_herbivores(longhornCattle, 7)
                self.remove_herbivores(redDeer, 4)
                self.add_pig(tamworthPigs, 0, 0, 1)
            # January 2020: -24 fallow deer
            if self.schedule.time == 179:
                self.remove_herbivores(fallowDeer, 24)
            # February 2020: -12 fallow; -1 cow; -2 red; -2 pigs
            if self.schedule.time == 180:
                self.remove_herbivores(fallowDeer, 12)
                self.remove_herbivores(redDeer, 2)
                self.remove_pig(tamworthPigs, 0, 1, 1)
                self.remove_herbivores(longhornCattle, 1)                               

            # # # # # 2020 # # # # # #
            # March & April 2020: +15 exmoor; -1 and +3 cows; -1 pig; filtering for red and fallow deer
            if self.schedule.time == 181:
                self.add_herbivores(exmoorPony, 15)
                self.add_herbivores(longhornCattle, 2)
                self.remove_pig(tamworthPigs, 0, 1, 0)





            # # # # # Forecasting (starting at step 185, July 2020) # # #??#??#             
            if self.schedule.time == 185:
                results_2 = self.datacollector.get_model_vars_dataframe()
                # first make sure that exmoor ponies are at their stocking density
                exmoorValue = results_2.iloc[185]['Exmoor pony']
                if exmoorValue > self.exmoor_stocking: # make sure ponies are at their stocking density
                    number_to_subtract = -self.exmoor_stocking + exmoorValue
                    self.remove_herbivores(exmoorPony, number_to_subtract)
                else:
                    number_to_add = self.exmoor_stocking - exmoorValue
                    self.add_herbivores(exmoorPony, number_to_add)
                    # Longhorn cattle can be culled in July
                    cattleValue = results_2.iloc[185]['Longhorn cattle']
                    if cattleValue > self.cattle_stocking:
                        number_to_subtract = random.randint(0,self.cattle_stocking)
                        self.remove_herbivores(longhornCattle, number_to_subtract)
                if self.introduce_euroBison == True:
                    self.add_herbivores(euroBison, 10)
                if self.introduce_elk == True:
                    self.add_herbivores(euroElk, 10)
                if self.introduce_reindeer == True:
                    self.add_herbivores(reindeer, 10)
            # August 2020
            if self.schedule.time == 186:
                results = self.datacollector.get_model_vars_dataframe()
                cattleValue = results.iloc[186]['Longhorn cattle']
                if cattleValue > self.cattle_stocking:
                    number_to_subtract = random.randint(0,self.cattle_stocking)
                    self.remove_herbivores(longhornCattle, number_to_subtract)
                fallowValue = results.iloc[186]['Fallow deer']
                if fallowValue > self.fallowDeer_stocking:
                    number_to_subtract = random.randint(0,self.fallowDeer_stocking)
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                redDeer_value = results.iloc[186]['Red deer']
                if redDeer_value > self.redDeer_stocking:
                    number_to_subtract = random.randint(0,self.redDeer_stocking)
                    self.remove_herbivores(redDeer, number_to_subtract)
            # Sept 2020
            if self.schedule.time == 187:
                results = self.datacollector.get_model_vars_dataframe()
                cattleValue = results.iloc[187]['Longhorn cattle']
                if cattleValue > self.cattle_stocking:
                    number_to_subtract = random.randint(0,self.cattle_stocking)
                    self.remove_herbivores(longhornCattle, number_to_subtract)
                fallowValue = results.iloc[187]['Fallow deer']
                if fallowValue > self.fallowDeer_stocking:
                    number_to_subtract = random.randint(0,self.fallowDeer_stocking)
                    self.remove_herbivores(fallowDeer, number_to_subtract)
            # Oct 2020
            if self.schedule.time == 188:
                results = self.datacollector.get_model_vars_dataframe()
                cattleValue = results.iloc[188]['Longhorn cattle']
                if cattleValue > self.cattle_stocking:
                    number_to_subtract = random.randint(0,self.cattle_stocking)
                    self.remove_herbivores(longhornCattle, number_to_subtract)
            # Nov 2020
            if self.schedule.time == 189:
                results = self.datacollector.get_model_vars_dataframe()
                cattleValue = results.iloc[189]['Longhorn cattle']
                if cattleValue > self.cattle_stocking:
                    number_to_subtract = random.randint(0,self.cattle_stocking)
                    self.remove_herbivores(longhornCattle, number_to_subtract)
                fallowValue = results.iloc[189]['Fallow deer']
                if fallowValue > self.fallowDeer_stocking:
                    number_to_subtract = random.randint(0,self.fallowDeer_stocking)
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                redDeer_value = results.iloc[189]['Red deer']
                if redDeer_value > self.redDeer_stocking:
                    number_to_subtract = random.randint(0,self.redDeer_stocking)
                    self.remove_herbivores(redDeer, number_to_subtract)
            # Dec 2020
            if self.schedule.time == 190:
                results = self.datacollector.get_model_vars_dataframe()
                cattleValue = results.iloc[190]['Longhorn cattle']
                if cattleValue > self.cattle_stocking:
                    number_to_subtract = random.randint(0,self.cattle_stocking)
                    self.remove_herbivores(longhornCattle, number_to_subtract)
                fallowValue = results.iloc[190]['Fallow deer']
                if fallowValue > self.fallowDeer_stocking:
                    number_to_subtract = random.randint(0,self.fallowDeer_stocking)
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                redDeer_value = results.iloc[190]['Red deer']
                if redDeer_value > self.redDeer_stocking:
                    number_to_subtract = random.randint(0,self.redDeer_stocking)
                    self.remove_herbivores(redDeer, number_to_subtract)
                pigValue = results.iloc[190]['Tamworth pigs']
                if pigValue > self.tamworthPig_stocking:
                    number_to_subtract = random.randint(0,self.tamworthPig_stocking)
                    self.remove_pig(tamworthPigs,number_to_subtract,0,0)
            # Jan 2021  
            if self.schedule.time == 191:
                results = self.datacollector.get_model_vars_dataframe()
                cattleValue = results.iloc[191]['Longhorn cattle']
                if cattleValue > self.cattle_stocking:
                    number_to_subtract = random.randint(0,self.cattle_stocking)
                    self.remove_herbivores(longhornCattle, number_to_subtract)
                fallowValue = results.iloc[191]['Fallow deer']
                if fallowValue > self.fallowDeer_stocking:
                    number_to_subtract = random.randint(0,self.fallowDeer_stocking)
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                redDeer_value = results.iloc[191]['Red deer']
                if redDeer_value > self.redDeer_stocking:
                    number_to_subtract = random.randint(0,self.redDeer_stocking)
                    self.remove_herbivores(redDeer, number_to_subtract)
                pigValue = results.iloc[191]['Tamworth pigs']
                if pigValue > self.tamworthPig_stocking:
                    number_to_subtract = random.randint(0,self.tamworthPig_stocking)
                    self.remove_pig(tamworthPigs, number_to_subtract,0,0)
            # Feb 2021: cull them all back to stocking values
            if self.schedule.time == 192:
                results = self.datacollector.get_model_vars_dataframe()
                cattleValue = results.iloc[192]['Longhorn cattle']
                if cattleValue > self.cattle_stocking:
                    number_to_subtract = -self.cattle_stocking + cattleValue
                    self.remove_herbivores(longhornCattle, number_to_subtract)
                fallowValue = results.iloc[192]['Fallow deer']
                if fallowValue > self.fallowDeer_stocking:
                    number_to_subtract = -self.fallowDeer_stocking + fallowValue
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                redDeer_value = results.iloc[192]['Red deer']
                if redDeer_value > self.redDeer_stocking:
                    number_to_subtract = -self.redDeer_stocking + redDeer_value
                    self.remove_herbivores(redDeer, number_to_subtract)
                pigValue = results.iloc[192]['Tamworth pigs']
                if pigValue > self.tamworthPig_stocking:
                    number_to_subtract = -self.tamworthPig_stocking + pigValue
                    self.remove_pig(tamworthPigs,number_to_subtract,0,0)


            # March 2021
            # reset exmoor pony values
            if self.schedule.time >= 193 and ((self.schedule.time % 12) + 1) == 3:
                results = self.datacollector.get_model_vars_dataframe()
                # first make sure that exmoor ponies are at their stocking density
                exmoorValue = results.iloc[-1]['Exmoor pony']
                if exmoorValue < self.exmoor_stocking: # shouldn't have to subtract anything since they don't grow
                    number_to_add = self.exmoor_stocking - exmoorValue
                    self.add_herbivores(exmoorPony, number_to_add)
                # reset fallow deer values (they are culled)
                fallowValue = results.iloc[-1]['Fallow deer']
                if fallowValue > self.fallowDeer_stocking:
                    number_to_subtract = random.randint(0,self.fallowDeer_stocking)
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                else:
                    number_to_add = self.fallowDeer_stocking - fallowValue
                    self.add_herbivores(fallowDeer, number_to_add)
                # reset red deer values  (they are culled)
                redDeer_value = results.iloc[-1]['Red deer']
                if redDeer_value > self.redDeer_stocking:
                    number_to_subtract = random.randint(0,self.redDeer_stocking)
                    self.remove_herbivores(redDeer, number_to_subtract)
                else:
                    number_to_add = self.redDeer_stocking - redDeer_value
                    self.add_herbivores(redDeer, number_to_add)
                # reset longhorn cattle values (they aren't culled this month)
                cattleValue = results.iloc[-1]['Longhorn cattle']
                if cattleValue < self.cattle_stocking:
                    number_to_add = self.cattle_stocking - cattleValue
                    self.add_herbivores(longhornCattle, number_to_add)
                # reset tamworth pig values (they aren't culled this month)
                pigValue = results.iloc[-1]['Tamworth pigs']
                if pigValue < self.tamworthPig_stocking:
                    number_to_add = self.tamworthPig_stocking - pigValue
                    self.add_pig(tamworthPigs, 0,number_to_add,0)
                if self.introduce_euroBison == True:
                    bisonValue = results.iloc[-1]['European bison']
                    if bisonValue > 10:
                        number_to_remove = -10 + bisonValue
                        self.remove_herbivores(euroBison, number_to_remove)
                if self.introduce_elk == True:
                    elkValue = results.iloc[-1]['European elk']
                    if elkValue > 10:
                        number_to_remove = -10 + elkValue
                        self.remove_herbivores(euroElk, number_to_remove)
                if self.introduce_reindeer == True:
                    reindeerValue = results.iloc[-1]['Reindeer']
                    if reindeerValue > 10:
                        number_to_remove = -10 + reindeerValue
                        self.remove_herbivores(reindeer, number_to_remove)
            # April 2021
            if self.schedule.time >= 193 and ((self.schedule.time % 12) + 1) == 4:
                results = self.datacollector.get_model_vars_dataframe()
                fallowValue = results.iloc[-1]['Fallow deer']
                if fallowValue > self.fallowDeer_stocking:
                    number_to_subtract = -self.fallowDeer_stocking + fallowValue
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                redDeer_value = results.iloc[-1]['Red deer']
                if redDeer_value > self.redDeer_stocking:
                    number_to_subtract = -self.redDeer_stocking + redDeer_value
                    self.remove_herbivores(redDeer, number_to_subtract)
            # May 2021
            if self.schedule.time >= 193 and ((self.schedule.time % 12) + 1) == 5:
                results = self.datacollector.get_model_vars_dataframe()
                pigValue = results.iloc[-1]['Tamworth pigs']
                if pigValue > self.tamworthPig_stocking:
                    number_to_subtract = random.randint(0,self.tamworthPig_stocking)
                    self.remove_pig(tamworthPigs, number_to_subtract,0,0)
            # June 2021
            if self.schedule.time >= 193 and ((self.schedule.time % 12) + 1) == 6:
                results = self.datacollector.get_model_vars_dataframe()
                cattleValue = results.iloc[-1]['Longhorn cattle']
                if cattleValue >= self.cattle_stocking:
                    number_to_subtract = random.randint(0,self.cattle_stocking)
                    self.remove_herbivores(self.cattle_stocking, number_to_subtract)
            # July 2021
            if self.schedule.time >= 193 and ((self.schedule.time % 12) + 1) == 7:
                results = self.datacollector.get_model_vars_dataframe()
                cattleValue = results.iloc[-1]['Longhorn cattle']
                if cattleValue >= self.cattle_stocking:
                    number_to_subtract = random.randint(0,self.cattle_stocking)
                    self.remove_herbivores(longhornCattle, number_to_subtract)
            # August 2021
            if self.schedule.time >= 193 and ((self.schedule.time % 12) + 1) == 8:
                results = self.datacollector.get_model_vars_dataframe()
                cattleValue = results.iloc[-1]['Longhorn cattle']
                if cattleValue > self.cattle_stocking:
                    number_to_subtract = random.randint(0,self.cattle_stocking)
                    self.remove_herbivores(longhornCattle, number_to_subtract)
                fallowValue = results.iloc[-1]['Fallow deer']
                if fallowValue > self.fallowDeer_stocking:
                    number_to_subtract = random.randint(0,self.fallowDeer_stocking)
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                redDeer_value = results.iloc[-1]['Red deer']
                if redDeer_value > self.redDeer_stocking:
                    number_to_subtract = random.randint(0,self.redDeer_stocking)
                    self.remove_herbivores(redDeer, number_to_subtract)
            # Sept 2021
            if self.schedule.time >= 193 and ((self.schedule.time % 12) + 1) == 9:
                results = self.datacollector.get_model_vars_dataframe()
                cattleValue = results.iloc[-1]['Longhorn cattle']
                if cattleValue > self.cattle_stocking:
                    number_to_subtract = random.randint(0,self.cattle_stocking)
                    self.remove_herbivores(longhornCattle, number_to_subtract)
                fallowValue = results.iloc[-1]['Fallow deer']
                if fallowValue > self.fallowDeer_stocking:
                    number_to_subtract = random.randint(0,self.fallowDeer_stocking)
                    self.remove_herbivores(fallowDeer, number_to_subtract)
            # Oct 2021
            if self.schedule.time >= 193 and ((self.schedule.time % 12) + 1) == 10:
                results = self.datacollector.get_model_vars_dataframe()
                cattleValue = results.iloc[-1]['Longhorn cattle']
                if cattleValue > self.cattle_stocking:
                    number_to_subtract = random.randint(0,self.cattle_stocking)
                    self.remove_herbivores(longhornCattle, number_to_subtract)
            # Nov 2021
            if self.schedule.time >= 193 and ((self.schedule.time % 12) + 1) == 11:
                results = self.datacollector.get_model_vars_dataframe()
                cattleValue = results.iloc[-1]['Longhorn cattle']
                if cattleValue > self.cattle_stocking:
                    number_to_subtract = random.randint(0,self.cattle_stocking)
                    self.remove_herbivores(longhornCattle, number_to_subtract)
                fallowValue = results.iloc[-1]['Fallow deer']
                if fallowValue > self.fallowDeer_stocking:
                    number_to_subtract = random.randint(0,self.fallowDeer_stocking)
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                redDeer_value = results.iloc[-1]['Red deer']
                if redDeer_value > self.redDeer_stocking:
                    number_to_subtract = random.randint(0,self.redDeer_stocking)
                    self.remove_herbivores(redDeer, number_to_subtract)
            # Dec 2021
            if self.schedule.time >= 193 and ((self.schedule.time % 12) + 1) == 12:
                results = self.datacollector.get_model_vars_dataframe()
                cattleValue = results.iloc[-1]['Longhorn cattle']
                if cattleValue > self.cattle_stocking:
                    number_to_subtract = random.randint(0,self.cattle_stocking)
                    self.remove_herbivores(longhornCattle, number_to_subtract)
                fallowValue = results.iloc[-1]['Fallow deer']
                if fallowValue > self.fallowDeer_stocking:
                    number_to_subtract = random.randint(0,self.fallowDeer_stocking)
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                redDeer_value = results.iloc[-1]['Red deer']
                if redDeer_value > self.redDeer_stocking:
                    number_to_subtract = random.randint(0,self.redDeer_stocking)
                    self.remove_herbivores(redDeer, number_to_subtract)
                pigValue = results.iloc[-1]['Tamworth pigs']
                if pigValue > self.tamworthPig_stocking:
                    number_to_subtract = random.randint(0,self.tamworthPig_stocking)
                    self.remove_pig(tamworthPigs,number_to_subtract,0,0)
                # add boars
                self.add_pig(tamworthPigs, 0, 0, 1)

            # Jan 2022
            if self.schedule.time >= 193 and ((self.schedule.time % 12) + 1) == 1:
                results = self.datacollector.get_model_vars_dataframe()
                cattleValue = results.iloc[-1]['Longhorn cattle']
                if cattleValue >self.cattle_stocking:
                    number_to_subtract = random.randint(0,self.cattle_stocking)
                    self.remove_herbivores(longhornCattle, number_to_subtract)
                fallowValue = results.iloc[-1]['Fallow deer']
                if fallowValue > self.fallowDeer_stocking:
                    number_to_subtract = random.randint(0,self.fallowDeer_stocking)
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                redDeer_value = results.iloc[-1]['Red deer']
                if redDeer_value > self.redDeer_stocking:
                    number_to_subtract = random.randint(0,self.redDeer_stocking)
                    self.remove_herbivores(redDeer, number_to_subtract)
                pigValue = results.iloc[-1]['Tamworth pigs']
                if pigValue > self.tamworthPig_stocking:
                    number_to_subtract = random.randint(0,self.tamworthPig_stocking)
                    # remove boars
                    self.remove_pig(tamworthPigs,number_to_subtract,0,1)

            # Feb 2022: cull them all back to stocking values
            if self.schedule.time >= 193 and ((self.schedule.time % 12) + 1) == 2:
                results = self.datacollector.get_model_vars_dataframe()
                cattleValue = results.iloc[-1]['Longhorn cattle']
                if cattleValue > self.cattle_stocking:
                    number_to_subtract = -self.cattle_stocking + cattleValue
                    self.remove_herbivores(longhornCattle, number_to_subtract)
                fallowValue = results.iloc[-1]['Fallow deer']
                if fallowValue > self.fallowDeer_stocking:
                    number_to_subtract = -self.fallowDeer_stocking + fallowValue
                    self.remove_herbivores(fallowDeer, number_to_subtract)
                redDeer_value = results.iloc[-1]['Red deer']
                if redDeer_value > self.redDeer_stocking:
                    number_to_subtract = -self.redDeer_stocking + redDeer_value
                    self.remove_herbivores(redDeer, number_to_subtract)
                pigValue = results.iloc[-1]['Tamworth pigs']
                if pigValue > self.tamworthPig_stocking:
                    number_to_subtract = -self.tamworthPig_stocking + pigValue
                    self.remove_pig(tamworthPigs,number_to_subtract,0,0)


        # stop running it at the max_time (184 for present day ones)
        if self.schedule.time == self.max_time:
            self.running = False 


    def run_model(self): 
        # run it for 184 steps
        for i in range(self.max_time):
            self.step()
            # print(i)
        results = self.datacollector.get_model_vars_dataframe()
        return results