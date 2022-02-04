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

    def step(self):

        # chance of 1 young scrub becoming 1 mature scrub
        number_scrub_maturing = np.random.binomial(n=self.edibles["youngScrub"], p=self.model.chance_youngScrubMatures)
        # don't let it go over 300 mature shrubs
        number_scrub_maturing = min(number_scrub_maturing, 300 - self.edibles['scrub'])
        self.edibles['scrub'] += number_scrub_maturing
        self.edibles["youngScrub"] -= number_scrub_maturing

        # chance of sapling becoming tree
        number_saplings_maturing = np.random.binomial(n=self.edibles["saplings"], p=self.model.chance_saplingBecomingTree)
        # don't let it go over 300 trees
        number_saplings_maturing = min(number_saplings_maturing, 300 - self.edibles["trees"])
        self.edibles["trees"] += number_saplings_maturing
        self.edibles["saplings"] -= number_saplings_maturing

        # chance of reproducing saplings or young shrubs
        neighborhood_list = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)
        items_in_neighborhood = list(map(self.model.grid.get_cell_list_contents, neighborhood_list)) 
        only_habitat_cells = [obj for obj in items_in_neighborhood if (isinstance(x, habitatAgent) for x in obj)]
        no_herbivores = [item[0] for item in only_habitat_cells]

        # chance of reproducing saplings
        number_reproduce_trees = np.random.binomial(n=self.edibles["trees"], p=self.model.chance_reproduceSapling)
        # are there any that aren't full of other saplings/trees?
        available_sapling_cell = [i for i in no_herbivores if i.edibles["saplings"] < 3000 and i.edibles["trees"] < 300]
        if len(available_sapling_cell) > 0: 
            list_of_choices = random.choices(available_sapling_cell, k = number_reproduce_trees)
            for i in range(number_reproduce_trees):
                new_patch_sapling = list_of_choices[i]
                new_patch_sapling.edibles["saplings"] += 1 
            
        list_of_choices = None
        # chance of reproducing scrub
        number_reproduce_shrubs = np.random.binomial(n=self.edibles['scrub'], p=self.model.chance_reproduceYoungScrub)
        # are there any that aren't full of other scrub/young scrub?
        available_youngscrub_cell = [i for i in no_herbivores if i.edibles["youngScrub"] < 3000 and i.edibles['scrub'] < 300]
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
        combined_trees_shrubs = ((self.edibles["trees"]/300)*self.model.chance_grassOutcompetedByTree) + ((self.edibles['scrub']/300)*self.model.chance_grassOutcompetedByScrub)
        if combined_trees_shrubs > 1: combined_trees_shrubs = 1
        outcompeted_grass = np.random.binomial(n=self.edibles["grass"], p=combined_trees_shrubs)
        self.edibles["grass"] -= outcompeted_grass
        self.edibles["bare_ground"] += outcompeted_grass

        # chance of mature scrub being outcompeted by trees 
        mature_scrub_outcompeted = np.random.binomial(n=self.edibles['scrub'], p=(self.edibles["trees"]/300)*self.model.chance_scrubOutcompetedByTree)
        self.edibles['scrub'] -= mature_scrub_outcompeted

        # saplings being outcompeted by scrub/trees
        combined_saplings = ((self.edibles["trees"]/300)*self.model.chance_saplingOutcompetedByTree) + ((self.edibles['scrub']/300)*self.model.chance_saplingOutcompetedByScrub)
        if combined_saplings > 1: combined_saplings = 1
        outcompeted_saplings = np.random.binomial(n=self.edibles["saplings"], p=combined_saplings)
        self.edibles["saplings"] -= outcompeted_saplings

        # young scrub being outcompeted by scrub/trees
        combined_scrub = ((self.edibles["trees"]/300)*self.model.chance_youngScrubOutcompetedByTree) + ((self.edibles['scrub']/300)*self.model.chance_youngScrubOutcompetedByScrub)
        if combined_scrub > 1: combined_scrub = 1
        outcompeted_youngscrub = np.random.binomial(n=self.edibles["youngScrub"], p=combined_scrub)
        self.edibles["youngScrub"] -= outcompeted_youngscrub

        # chance of tree (400) or mature scrub dying (100 yrs). Species informed by this website https://www.kneppestate.co.uk/woodland  
        #   Tree = average of the following: oak = 1000yrs, ash = 350, beech = 350; lime = 400; crab apple = 70; scots pine = 400; hornbeam = 300; sallow = 300; service = 400
        #   Scrub = average of the following: hawthorne = 250yrs; blackthorne 100; blackberry = 40; gorse = 25; elder 60 years; juniper 200; dog-rose 60
        old_trees = np.random.binomial(n=self.edibles["trees"], p=0.0002)
        old_scrub = np.random.binomial(n=self.edibles["scrub"], p=0.008)
        self.edibles["trees"] -= old_trees
        self.edibles["scrub"] -= old_scrub


        # reassess dominant condition
        if self.edibles["trees"] < 50 and self.edibles["scrub"] < 50 and self.edibles["grass"] >= 50:
            self.condition = "grassland"
        elif self.edibles["trees"] < 50 and self.edibles["scrub"] >= 50:
            self.condition = "thorny_scrubland"
        elif self.edibles["trees"] >= 50:
            self.condition = "woodland" 
        elif self.edibles["trees"] < 50 and self.edibles["scrub"] < 50 and self.edibles["bare_ground"] > 50:
            self.condition = "bare_ground"

        # print(self.unique_id, "trees", self.trees_here, "scrub", self.scrub_here, "saplings", self.edibles["saplings"], "youngScrub", self.youngscrub_here, "grass", self.edibles["grass"], "Bare", self.edibles["bare_ground"])



class roeDeer_agent(RandomWalker):
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
                    if eatenSaps >= habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/300))):
                        eatenSaps = habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/300)))
                    eat_saplings(habitat_patch, eatenSaps)
                    self.energy += (self.model.roeDeer_gain_from_Saplings * eatenSaps)
                    self.count_eaten[my_choice] += eatenSaps
                elif my_choice == "trees":
                    eatenTrees = math.ceil((1-self.energy)/self.model.roeDeer_gain_from_Trees)
                    if eatenTrees >= self.model.max_treesScrub_roeDeer: 
                        eatenTrees = self.model.max_treesScrub_roeDeer
                    if eatenTrees >= habitat_patch.edibles["trees"]:
                        eatenTrees = habitat_patch.edibles["trees"]
                    eat_trees(habitat_patch, eatenTrees)
                    self.energy += (self.model.roeDeer_gain_from_Trees * eatenTrees)
                    self.count_eaten[my_choice] += eatenTrees
                elif my_choice == "scrub":
                    eatenScrub = math.ceil((1-self.energy)/self.model.roeDeer_gain_from_Scrub)
                    if eatenScrub >= self.model.max_treesScrub_roeDeer: 
                        eatenScrub = self.model.max_treesScrub_roeDeer
                    if eatenScrub >= habitat_patch.edibles['scrub']:
                        eatenScrub = habitat_patch.edibles['scrub']
                    eat_scrub(habitat_patch, eatenScrub)
                    self.energy += (self.model.roeDeer_gain_from_Scrub * eatenScrub)
                    self.count_eaten[my_choice] +=eatenScrub
                elif my_choice == "youngScrub":
                    eatenYoungScrub = math.ceil((1-self.energy)/self.model.roeDeer_gain_from_YoungScrub)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenYoungScrub >= habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/300))):
                        eatenYoungScrub = habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/300)))
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
        if living and (random.random() < self.model.roeDeer_reproduce/np.log10(self.model.schedule.get_breed_count(roeDeer_agent)+ 1)) and (5 <= self.model.get_month() < 7):
            # Create a new roe deer and divide energy:
            self.energy = np.random.uniform(0, self.energy)
            fawn = roeDeer_agent(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
            self.model.grid.place_agent(fawn, self.pos)
            self.model.schedule.add(fawn)


class exmoorPony(RandomWalker):
    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        # move & reduce energy
        self.grazer_move()
        living = True
        self.energy -= 1
        
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
                    if eatenSaps >= habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/300))):
                        eatenSaps = habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/300)))
                    eat_saplings(habitat_patch, eatenSaps)
                    self.energy += (self.model.ponies_gain_from_Saplings * eatenSaps)
                elif my_choice == "trees":
                    eatenTrees = math.ceil((1-self.energy)/self.model.ponies_gain_from_Trees)
                    if eatenTrees >= self.model.max_treesScrub_largeHerb: 
                        eatenTrees = self.model.max_treesScrub_largeHerb
                    if eatenTrees >= habitat_patch.edibles["trees"]:
                        eatenTrees = habitat_patch.edibles["trees"]
                    eat_trees(habitat_patch, eatenTrees)
                    self.energy += (self.model.ponies_gain_from_Trees * eatenTrees)
                elif my_choice == "scrub":
                    eatenScrub = math.ceil((1-self.energy)/self.model.ponies_gain_from_Scrub)
                    if eatenScrub >= self.model.max_treesScrub_largeHerb: 
                        eatenScrub = self.model.max_treesScrub_largeHerb
                    if eatenScrub >= habitat_patch.edibles['scrub']:
                        eatenScrub = habitat_patch.edibles['scrub']
                    eat_scrub(habitat_patch, eatenScrub)
                    self.energy += (self.model.ponies_gain_from_Scrub * eatenScrub)
                elif my_choice == "youngScrub":
                    eatenYoungScrub = math.ceil((1-self.energy)/self.model.ponies_gain_from_YoungScrub)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenYoungScrub >= habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/300))):
                        eatenYoungScrub = habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/300)))
                    eat_youngscrub(habitat_patch, eatenYoungScrub)
                    self.energy += (self.model.ponies_gain_from_YoungScrub * eatenYoungScrub)
                elif my_choice == "grass":
                    eatenGrass = math.ceil((1-self.energy)/self.model.ponies_gain_from_grass)
                    if eatenGrass >= habitat_patch.edibles["grass"]:
                        eatenGrass = habitat_patch.edibles["grass"]
                    eat_grass(habitat_patch, eatenGrass)
                    self.energy += (self.model.ponies_gain_from_grass * eatenGrass)
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
        self.energy = energy

    def step(self):
        # move & reduce energy
        self.grazer_move()
        living = True
        self.energy -= 1
        
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
                    if eatenSaps >= habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/300))):
                        eatenSaps = habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/300)))
                    eat_saplings(habitat_patch, eatenSaps)
                    self.energy += (self.model.cows_gain_from_Saplings * eatenSaps)
                elif my_choice == "trees":
                    eatenTrees = math.ceil((1-self.energy)/self.model.cows_gain_from_Trees)
                    if eatenTrees >= self.model.max_treesScrub_largeHerb: 
                        eatenTrees = self.model.max_treesScrub_largeHerb
                    if eatenTrees >= habitat_patch.edibles["trees"]:
                        eatenTrees = habitat_patch.edibles["trees"]
                    eat_trees(habitat_patch, eatenTrees)
                    self.energy += (self.model.cows_gain_from_Trees * eatenTrees)
                elif my_choice == "scrub":
                    eatenScrub = math.ceil((1-self.energy)/self.model.cows_gain_from_Scrub)
                    if eatenScrub >= self.model.max_treesScrub_largeHerb: 
                        eatenScrub = self.model.max_treesScrub_largeHerb
                    if eatenScrub >= habitat_patch.edibles['scrub']:
                        eatenScrub = habitat_patch.edibles['scrub']
                    eat_scrub(habitat_patch, eatenScrub)
                    self.energy += (self.model.cows_gain_from_Scrub * eatenScrub)
                elif my_choice == "youngScrub":
                    eatenYoungScrub = math.ceil((1-self.energy)/self.model.cows_gain_from_YoungScrub)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenYoungScrub >= habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/300))):
                        eatenYoungScrub = habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/300)))
                    eat_youngscrub(habitat_patch, eatenYoungScrub)
                    self.energy += (self.model.cows_gain_from_YoungScrub * eatenYoungScrub)
                elif my_choice == "grass":
                    eatenGrass = math.ceil((1-self.energy)/self.model.cows_gain_from_grass)
                    if eatenGrass >= habitat_patch.edibles["grass"]:
                        eatenGrass = habitat_patch.edibles["grass"]
                    eat_grass(habitat_patch, eatenGrass)
                    self.energy += (self.model.cows_gain_from_grass * eatenGrass)
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
        self.energy = energy

    def step(self):
        # move & reduce energy
        self.mixedDiet_move()
        living = True
        self.energy -= 1

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
                    if eatenSaps >= habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/300))):
                        eatenSaps = habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/300)))
                    eat_saplings(habitat_patch, eatenSaps)
                    self.energy += (self.model.fallowDeer_gain_from_Saplings * eatenSaps)
                elif my_choice == "trees":
                    eatenTrees = math.ceil((1-self.energy)/self.model.fallowDeer_gain_from_Trees)
                    if eatenTrees >= self.model.max_treesScrub_largeHerb: 
                        eatenTrees = self.model.max_treesScrub_largeHerb
                    if eatenTrees >= habitat_patch.edibles["trees"]:
                        eatenTrees = habitat_patch.edibles["trees"]
                    eat_trees(habitat_patch, eatenTrees)
                    self.energy += (self.model.fallowDeer_gain_from_Trees * eatenTrees)
                elif my_choice == "scrub":
                    eatenScrub = math.ceil((1-self.energy)/self.model.fallowDeer_gain_from_Scrub)
                    if eatenScrub >= self.model.max_treesScrub_largeHerb: 
                        eatenScrub = self.model.max_treesScrub_largeHerb
                    if eatenScrub >= habitat_patch.edibles['scrub']:
                        eatenScrub = habitat_patch.edibles['scrub']
                    eat_scrub(habitat_patch, eatenScrub)
                    self.energy += (self.model.fallowDeer_gain_from_Scrub * eatenScrub)
                elif my_choice == "youngScrub":
                    eatenYoungScrub = math.ceil((1-self.energy)/self.model.fallowDeer_gain_from_YoungScrub)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenYoungScrub >= habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/300))):
                        eatenYoungScrub = habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/300)))
                    eat_youngscrub(habitat_patch, eatenYoungScrub)
                    self.energy += (self.model.fallowDeer_gain_from_YoungScrub * eatenYoungScrub)
                elif my_choice == "grass":
                    eatenGrass = math.ceil((1-self.energy)/self.model.fallowDeer_gain_from_grass)
                    if eatenGrass >= habitat_patch.edibles["grass"]:
                        eatenGrass = habitat_patch.edibles["grass"]
                    eat_grass(habitat_patch, eatenGrass)
                    self.energy += (self.model.fallowDeer_gain_from_grass * eatenGrass)
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
        self.energy = energy

    def step(self):
        # move & reduce energy
        self.mixedDiet_move()
        living = True
        self.energy -= 1

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
                    if eatenSaps >= habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/300))):
                        eatenSaps = habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/300)))
                    eat_saplings(habitat_patch, eatenSaps)
                    self.energy += (self.model.redDeer_gain_from_Saplings * eatenSaps)
                elif my_choice == "trees":
                    eatenTrees = math.ceil((1-self.energy)/self.model.redDeer_gain_from_Trees)
                    if eatenTrees >= self.model.max_treesScrub_largeHerb: 
                        eatenTrees = self.model.max_treesScrub_largeHerb
                    if eatenTrees >= habitat_patch.edibles["trees"]:
                        eatenTrees = habitat_patch.edibles["trees"]
                    eat_trees(habitat_patch, eatenTrees)
                    self.energy += (self.model.redDeer_gain_from_Trees * eatenTrees)
                elif my_choice == "scrub":
                    eatenScrub = math.ceil((1-self.energy)/self.model.redDeer_gain_from_Scrub)
                    if eatenScrub >= self.model.max_treesScrub_largeHerb: 
                        eatenScrub = self.model.max_treesScrub_largeHerb
                    if eatenScrub >= habitat_patch.edibles['scrub']:
                        eatenScrub = habitat_patch.edibles['scrub']
                    eat_scrub(habitat_patch, eatenScrub)
                    self.energy += (self.model.redDeer_gain_from_Scrub * eatenScrub)
                elif my_choice == "youngScrub":
                    eatenYoungScrub = math.ceil((1-self.energy)/self.model.redDeer_gain_from_YoungScrub)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenYoungScrub >= habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/300))):
                        eatenYoungScrub = habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/300)))
                    eat_youngscrub(habitat_patch, eatenYoungScrub)
                    self.energy += (self.model.redDeer_gain_from_YoungScrub * eatenYoungScrub)
                elif my_choice == "grass":
                    eatenGrass = math.ceil((1-self.energy)/self.model.redDeer_gain_from_grass)
                    if eatenGrass >= habitat_patch.edibles["grass"]:
                        eatenGrass = habitat_patch.edibles["grass"]
                    eat_grass(habitat_patch, eatenGrass)
                    self.energy += (self.model.redDeer_gain_from_grass * eatenGrass)
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
    def __init__(self, unique_id, pos, model, moore, energy, boar):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.pregnancy_timer = None
        self.boar = boar

    def step(self):
        # move & reduce energy
        self.random_move()
        living = True
        self.energy -= 1

        # Eat what's on my patch: roe deer are broswers, so randomly choose any habitat to eat
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        habitat_choices = ["saplings", "youngScrub", "grass", "bare"]
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
                    if eatenSaps >= habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/300))):
                        eatenSaps = habitat_patch.edibles["saplings"] - (round(habitat_patch.edibles["saplings"] * (habitat_patch.edibles['scrub']/300)))
                    eat_saplings(habitat_patch, eatenSaps)
                    self.energy += (self.model.pigs_gain_from_Saplings * eatenSaps)
                elif my_choice == "youngScrub":
                    eatenYoungScrub = math.ceil((1-self.energy)/self.model.pigs_gain_from_YoungScrub)
                    # scrub facilitates saplings by preventing herbivory
                    if eatenYoungScrub >= habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/300))):
                        eatenYoungScrub = habitat_patch.edibles["youngScrub"] - (round(habitat_patch.edibles["youngScrub"] * (habitat_patch.edibles['scrub']/300)))
                    eat_youngscrub(habitat_patch, eatenYoungScrub)
                    self.energy += (self.model.pigs_gain_from_YoungScrub * eatenYoungScrub)
                elif my_choice == "grass":
                    eatenGrass = math.ceil((1-self.energy)/self.model.pigs_gain_from_grass)
                    if eatenGrass >= habitat_patch.edibles["grass"]:
                        eatenGrass = habitat_patch.edibles["grass"]
                    eat_grass(habitat_patch, eatenGrass)
                    self.energy += (self.model.pigs_gain_from_grass * eatenGrass)
                elif my_choice == "bare":
                    eatenSoil = math.ceil((1-self.energy)/self.model.pigs_gain_from_soil)
                    if eatenSoil >= habitat_patch.edibles["bare_ground"]:
                        eatenSoil = habitat_patch.edibles["bare_ground"]
                    self.energy += (self.model.pigs_gain_from_soil * eatenSoil)
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

        # pigs reproduce Jan - July (1 - 7, < 8). 
        # if living and self.pregnancy_timer == None and self.boar == False and (random.random() < self.model.pigs_reproduce/np.log10(self.model.schedule.get_breed_count(tamworthPigs)+ 1)) and (1 <= self.model.get_month() < 8):
        # are there boars here? 
        all_pigs = self.model.schedule.agents_by_breed[tamworthPigs].items()
        boars_here = [i for (k, i) in all_pigs if i.boar == True]
        if len(boars_here) > 0:
            # if there are, set the timer so other pigs reproduce in a few months
            if living and self.pregnancy_timer == None and self.boar == False and (random.random() < self.model.pigs_reproduce/np.log10(self.model.schedule.get_breed_count(tamworthPigs)+ 1)):
                self.pregnancy_timer = random.randint(2,4)
                # divide my energy
                self.energy = np.random.uniform(0, self.energy)

    def giveBirth(self):
        # Pick a number of piglets to have
        for _ in range(random.randint(1,10)):
            piglet = tamworthPigs(self.model.next_id(), self.pos, self.model, self.moore, self.energy, self.boar)
            self.model.grid.place_agent(piglet, self.pos)
            self.model.schedule.add(piglet)



                                # # # # ------ Define the model ------ # # # # 

class KneppModel(Model):
    
    max_treesScrub_roeDeer = 3 # assume roe deer don't kill more than 3 trees or adult scrub per month
    max_treesScrub_largeHerb = 15 # assume they don't kill more than 15 per month
    
    def __init__(self,             
            chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
            chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
            initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland,
            roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
            ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
            cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
            fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
            redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
            pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, pigs_gain_from_soil,
            max_start_saplings, max_start_youngScrub,
            width, height, max_time, reintroduction, 
            RC1_noFood, RC2_noTreesScrub, RC3_noTrees, RC4_noScrub):

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
        self.chance_grassOutcompetedByTree = chance_grassOutcompetedByTree
        self.chance_grassOutcompetedByScrub = chance_grassOutcompetedByScrub
        self.chance_saplingOutcompetedByTree = chance_saplingOutcompetedByTree
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
        self.pigs_gain_from_Saplings = pigs_gain_from_Saplings
        self.pigs_gain_from_YoungScrub = pigs_gain_from_YoungScrub
        self.pigs_gain_from_soil = pigs_gain_from_soil
        # other parameters
        self.height = height
        self.width = width
        self.max_time = max_time
        self.reintroduction = reintroduction
        # reality checks
        self.RC1_noFood = RC1_noFood
        self.RC2_noTreesScrub = RC2_noTreesScrub
        self.RC3_noTrees = RC3_noTrees
        self.RC4_noScrub = RC4_noScrub
        # set grid & schedule
        self.grid = MultiGrid(width, height, True) # this grid allows for multiple agents on same cell
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
                scrub_here = random.randint(0, 49)
                youngscrub_here = 0
                perc_grass_here = random.randint(50, 100)
                perc_bareground_here = 100 - perc_grass_here
            elif my_condition == "thorny_scrubland" and self.RC3_noTrees == False:  # at least 10 scrub plants, no more than 10 trees
                trees_here = random.randint(0, 49)
                saplings_here = random.randint(0, round(max_start_saplings * 3000))
                scrub_here = random.randint(50, 300)
                youngscrub_here = random.randint(0, round(max_start_youngScrub * 3000))
                perc_grass_here = random.randint(0, 100)
                perc_bareground_here = 100 - perc_grass_here
            elif my_condition == "thorny_scrubland" and self.RC3_noTrees == True:  # at least 10 scrub plants, no more than 10 trees
                trees_here = 0
                saplings_here = 0
                scrub_here = random.randint(50, 300)
                youngscrub_here = random.randint(0, round(max_start_youngScrub * 3000))
                perc_grass_here = random.randint(0, 100)
                perc_bareground_here = 100 - perc_grass_here
            elif my_condition == "woodland" and self.RC4_noScrub == False:  # woodland has 10-100 trees
                trees_here = random.randint(49, 300)
                saplings_here = random.randint(0, round(max_start_saplings * 3000))
                scrub_here = random.randint(0, 300)
                youngscrub_here = random.randint(0, round(max_start_youngScrub * 3000))
                perc_grass_here = random.randint(0, 100)
                perc_bareground_here = 100 - perc_grass_here
            elif my_condition == "woodland" and self.RC4_noScrub == True:  # woodland has 10-100 trees
                trees_here = random.randint(49, 300)
                saplings_here = random.randint(0, round(max_start_saplings * 3000))
                scrub_here = 0
                youngscrub_here = 0
                perc_grass_here = random.randint(0, 100)
                perc_bareground_here = 100 - perc_grass_here
            elif my_condition == "bare_ground": # more than 50% bare ground
                trees_here = 0
                saplings_here = 0
                scrub_here = 0
                youngscrub_here = 0
                perc_bareground_here = random.randint(51, 100)
                perc_grass_here = 100 - perc_bareground_here
            patch = habitatAgent(self.next_id(), (x, y), self, my_condition, trees_here, saplings_here, scrub_here, youngscrub_here, perc_grass_here, perc_bareground_here)
            self.grid.place_agent(patch, (x, y))
            self.schedule.add(patch)


        # Create roe deer
        for i in range(self.initial_roeDeer):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            energy = np.random.uniform(0, 1)
            roeDeer = roeDeer_agent(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(roeDeer, (x, y))
            self.schedule.add(roeDeer)


        # get data organized
        self.datacollector = DataCollector(
                        model_reporters = {
                        "Time": lambda m: m.schedule.time, 
                        "Roe deer": lambda m: m.schedule.get_breed_count(roeDeer_agent),
                        "Exmoor pony": lambda m: m.schedule.get_breed_count(exmoorPony),
                        "Fallow deer": lambda m: m.schedule.get_breed_count(fallowDeer),
                        "Longhorn cattle": lambda m: m.schedule.get_breed_count(longhornCattle),
                        "Red deer": lambda m: m.schedule.get_breed_count(redDeer),
                        "Tamworth pigs": lambda m: m.schedule.get_breed_count(tamworthPigs),
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
                        # what's being eaten
                        "Eaten Grass": lambda m: self.count_eaten(m, "grass"),
                        "Eaten Trees": lambda m: self.count_eaten(m, "trees"),
                        "Eaten Mature Scrub": lambda m: self.count_eaten(m, "scrub"),
                        "Eaten Saplings": lambda m: self.count_eaten(m, "saplings"),
                        "Eaten Young Scrub": lambda m: self.count_eaten(m, "youngScrub")
                        }
                        )

        self.running = True
        self.datacollector.collect(self)

    def count_eaten(self, model, eaten_thing):
        # want to count grass, wood, scrub, bare ground in each patch
        count_item = 0
        for key, value in model.schedule.agents_by_breed[roeDeer_agent].items():
            count_item += value.count_eaten[eaten_thing]
        return count_item

    def count_condition(self, model, habitat_condition):
        # want to count grass, wood, scrub, bare ground in each patch
        count = 0
        for key, value in model.schedule.agents_by_breed[habitatAgent].items():
            if value.condition == habitat_condition:
                count += 1
        # return percentage of entire area
        return round((count/1800)*100)

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


    def add_pig(self, herbivore, count_non_boar, count_boar):
        x = random.randrange(self.width)
        y = random.randrange(self.height)
        energy = np.random.uniform(0, 1)
        for i in range(count_non_boar):
            boar = False
            to_add = herbivore(self.next_id(), (x, y), self, True, energy, boar)
            self.grid.place_agent(to_add, (x, y))
            self.schedule.add(to_add)
        for i in range(count_boar):
            boar = True
            to_add = herbivore(self.next_id(), (x, y), self, True, energy, boar)
            self.grid.place_agent(to_add, (x, y))
            self.schedule.add(to_add)


    def remove_pig(self, herbivore, count_non_boar, count_boar):
        to_remove = self.schedule.agents_by_breed[herbivore].items()
        to_remove_notBoars = [i for (k, i) in to_remove if i.boar == False]
        to_remove_boars = [i for (k, i) in to_remove if i.boar == True]
        my_choices = random.sample(list(to_remove_notBoars), k = min(count_non_boar, len(to_remove_notBoars)))
        my_choices_boar = random.sample(list(to_remove_boars), k = min(count_boar, len(to_remove_boars)))
        # remove non-boars
        for my_choice in my_choices:
            my_choice = my_choice
            self.grid._remove_agent(my_choice.pos, my_choice)
            self.schedule.remove(my_choice)
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
                self.add_pig(tamworthPigs, 20, 0)
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
                    self.remove_pig(tamworthPigs, number_to_subtract, 0)
                else:
                    number_to_add = 17 - pigsValue
                    self.add_pig(tamworthPigs, number_to_add, 0)
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
                    self.remove_pig(tamworthPigs, number_to_subtract, 0)
                else:
                    number_to_add = 22 - pigsValue
                    self.add_pig(tamworthPigs, number_to_add, 0)
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
                    self.remove_pig(tamworthPigs, number_to_subtract, 0)
                else:
                    number_to_add = 33 - pigsValue
                    self.add_pig(tamworthPigs, number_to_add, 0)
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
                    self.remove_pig(tamworthPigs, number_to_subtract, 0)
                else:
                    number_to_add = 6 - pigsValue
                    self.add_pig(tamworthPigs, number_to_add, 0)
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
                    self.remove_pig(tamworthPigs, number_to_subtract, 0)
                else:
                    number_to_add = 18 - pigsValue
                    self.add_pig(tamworthPigs, number_to_add, 0)
                redDeerValue = results_6.iloc[109]['Red deer']
                if redDeerValue >= 13:
                    number_to_subtract = -13 + redDeerValue
                    self.remove_herbivores(redDeer, number_to_subtract)
                else:
                    number_to_add = 13 - redDeerValue
                    self.add_herbivores(redDeer, number_to_add)
            
            # Jan 2015 - assumed 1 boar added 
            if self.schedule.time == 119:
                self.add_pig(tamworthPigs, 0, 1)
            # Feb 2015 - assumed 1 boar removed, -2 cows
            if self.schedule.time == 120:
                self.remove_pig(tamworthPigs, 0, 1)

        
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
                # Pigs: 18
                pigsValue = results_7.iloc[121]['Tamworth pigs']
                if pigsValue >= 18:
                    number_to_subtract = -18 + pigsValue
                    self.remove_pig(tamworthPigs, number_to_subtract, 0)
                else:
                    number_to_add = 18 - pigsValue
                    self.add_pig(tamworthPigs, number_to_add, 0)
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
                # April 2015: one pig culled
                self.remove_pig(tamworthPigs, 1, 0)
            # May 2015
            if self.schedule.time == 123:
                # May 2015: 8 pigs culled
                self.remove_pig(tamworthPigs, 8, 0)
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
            # Nov 2015: -7 fallow deer, -1 pig
            if self.schedule.time == 129:
                self.remove_herbivores(fallowDeer, 7)                 
                self.remove_pig(tamworthPigs, 1, 0)       
            # Dec 2015: 6 fallow deer culled; 5 cows removed;
            if self.schedule.time == 130:
                self.remove_herbivores(fallowDeer, 6)
                self.remove_herbivores(longhornCattle, 5)
            # Jan 2016: 7 fallow deer culled; 4 pigs culled and 1 added
            if self.schedule.time == 131:
                self.remove_herbivores(fallowDeer, 7) 
                self.remove_pig(tamworthPigs, 4, 0)
                self.add_pig(tamworthPigs, 0, 1)
            # Feb 2016: 10 fallow deer culled; 2 pigs culled
            if self.schedule.time == 132:
                self.remove_herbivores(fallowDeer, 10)
                self.remove_pig(tamworthPigs, 2, 0)
                                
                                        # # # # # # # 2016 # # # # # # #

            # March 2016: 1 pony added; 3 pigs added and 4 culled incl. 1 boar
            if self.schedule.time == 133:
                self.add_herbivores(exmoorPony, 1)
                self.remove_pig(tamworthPigs, 0, 1)
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
                self.remove_pig(tamworthPigs, 4, 0)
            # January 2017: -4 pigs, +1 boar
            if self.schedule.time == 143:
                self.remove_pig(tamworthPigs, 4, 0)
                self.add_pig(tamworthPigs, 0, 1)
            # February 2017: -8 fallow deer; -3 pigs; filtering for ponies
            if self.schedule.time == 144:
                self.remove_herbivores(fallowDeer, 8)
                self.remove_pig(tamworthPigs, 2, 1)


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
                self.remove_pig(tamworthPigs, 4, 0)
            # January 2018: -9 pigs, +1 pig, and pig filtering conditions
            if self.schedule.time == 155:
                self.remove_pig(tamworthPigs, 9, 0)
                self.add_pig(tamworthPigs, 0, 1)
            # February 2018: -14 fallow; -1 red deer; -1 pig; filtering for pig and exmoor
            if self.schedule.time == 156:
                self.remove_herbivores(fallowDeer, 14)
                self.remove_herbivores(redDeer, 1)
                self.remove_pig(tamworthPigs, 0, 1)

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
            # April 2018: +1 cow and filtering for cow
            if self.schedule.time == 158:
                self.add_herbivores(longhornCattle, 1)
            # June 2018: -22 cows, +2 cows; filtering for cows
            if self.schedule.time == 160:
                self.remove_herbivores(longhornCattle, 18)
            # July 2018: -1 red deer; -1 pig
            if self.schedule.time == 161:
                self.remove_herbivores(redDeer, 1)
                self.remove_pig(tamworthPigs, 1, 0)
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
                self.remove_pig(tamworthPigs, 1, 0)
            # November 2018: -8 cows; -12 pigs
            if self.schedule.time == 165:
                self.remove_herbivores(longhornCattle, 7)
                self.remove_pig(tamworthPigs, 12, 0)
            # December & January 2018/2019: -19 fallow; -5 and +1 cow; -1 red deer 
            if self.schedule.time == 166:
                self.remove_herbivores(longhornCattle, 4)
                self.remove_herbivores(fallowDeer, 19)
                self.remove_herbivores(redDeer, 1)
            # February 2019: +1 pig, -2 cows
            if self.schedule.time == 168:
                self.add_pig(tamworthPigs, 0, 1)                                                                                   
                self.remove_herbivores(longhornCattle, 2)
    

            # # # # # # # 2019 # # # # # # #

            # March 2019: -1 pig; fallow and red deer filters
            if self.schedule.time == 169:
                self.remove_herbivores(fallowDeer, 7)
                self.remove_herbivores(redDeer, 7)
            if self.schedule.time == 170:
                self.remove_pig(tamworthPigs, 0, 1)
            # June 2019: -28 cows and cow filtering condition
            if self.schedule.time == 172:
                self.remove_herbivores(longhornCattle, 28)
            # July & Aug 2019: -3, +5 cows; -27 pigs; filtering for pigs
            if self.schedule.time == 173:
                self.remove_pig(tamworthPigs, 27, 0)
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
                self.add_pig(tamworthPigs, 0, 1)
            # January 2020: -24 fallow deer
            if self.schedule.time == 179:
                self.remove_herbivores(fallowDeer, 24)
            # February 2020: -12 fallow; -1 cow; -2 red; -2 pigs
            if self.schedule.time == 180:
                self.remove_herbivores(fallowDeer, 12)
                self.remove_herbivores(redDeer, 2)
                self.remove_pig(tamworthPigs, 1, 1)
                self.remove_herbivores(longhornCattle, 1)                               

            # # # # # 2020 # # # # # #
            # March & April 2020: +15 exmoor; -1 and +3 cows; -1 pig; filtering for red and fallow deer
            if self.schedule.time == 181:
                self.add_herbivores(exmoorPony, 15)
                self.add_herbivores(longhornCattle, 2)
                self.remove_pig(tamworthPigs, 1, 0)
        
        # stop running it in May 2021
        if self.schedule.time == self.max_time:
            self.running = False 


    def run_model(self): 
        # run it for 184 steps
        for i in range(self.max_time):
            self.step()
            # print(i)
        results = self.datacollector.get_model_vars_dataframe()
        return results