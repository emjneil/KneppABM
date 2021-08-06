# ------ ABM of the Knepp Estate (2005-2046) --------
from mesa import Agent, Model
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd
from random_walk import RandomWalker
from schedule import RandomActivationByBreed
from mesa.space import MultiGrid 
from random import choice as rchoice



# herbivore eating habitat types
def eat_saplings(habitat_patch, eatenSaps):
    # rescale this according to how many shrubs there are 
    eatenSaps_scaled = eatenSaps - int((eatenSaps*(habitat_patch.scrub_here/100)))
    habitat_patch.saplings_here -= eatenSaps_scaled
    # don't let number of saplings go negative
    if habitat_patch.saplings_here < 0:
        habitat_patch.saplings_here = 0

def eat_trees(habitat_patch, eatenTrees):
    # roll dice between 0 and my maximum number I'll eat
    habitat_patch.trees_here -= eatenTrees
    # don't let it go negative
    if habitat_patch.trees_here < 0:
        habitat_patch.trees_here = 0

def eat_scrub(habitat_patch, eatenScrub):
    # roll dice between 0 and my maximum number I'll eat
    habitat_patch.scrub_here -= eatenScrub
    # don't let it go negative
    if habitat_patch.scrub_here < 0:
        habitat_patch.scrub_here = 0

def eat_youngscrub(habitat_patch, eatenYoungScrub):
    # rescale according to number of scrub plants
    eatenYoungScrub_scaled = eatenYoungScrub - int((eatenYoungScrub*(habitat_patch.scrub_here/100)))
    habitat_patch.youngscrub_here -= eatenYoungScrub_scaled
    # don't let it go negative
    if habitat_patch.youngscrub_here < 0:
        habitat_patch.youngscrub_here = 0

def eat_grass(habitat_patch, eatenGrass):
    # roll dice between 0 and my maximum number I'll eat
    habitat_patch.perc_grass_here -= eatenGrass
    habitat_patch.perc_bareground_here += eatenGrass
    # don't let it go negative
    if habitat_patch.perc_grass_here < 0:
        habitat_patch.perc_grass_here = 0
        habitat_patch.perc_bareground_here = 100


                            # # # # ------ Define the agents ------ # # # #
  
class habitatAgent (Agent):
    def __init__(self, unique_id, pos, model, condition, trees_here, saplings_here, scrub_here, youngscrub_here, perc_grass_here, perc_bareground_here):
        super().__init__(unique_id, model)
        self.condition = condition
        self.pos = pos
        self.trees_here = trees_here
        self.saplings_here = saplings_here
        self.scrub_here = scrub_here
        self.youngscrub_here = youngscrub_here
        self.perc_grass_here = perc_grass_here
        self.perc_bareground_here = perc_bareground_here

    def step(self):
        # chance of reproducing saplings to neighboring cell or to my cell
        neighborhood_list = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)
        items_in_neighborhood = list(map(self.model.grid.get_cell_list_contents, neighborhood_list)) 
        # pick one that has less than 1000 saplings
        only_habitat_cells = [obj for obj in items_in_neighborhood if (isinstance(x, habitatAgent) for x in obj)]
        no_herbivores = [item[0] for item in only_habitat_cells]
        available_sapling_cell = [i for i in no_herbivores if i.saplings_here < 1000 and i.trees_here < 100]
        if len(available_sapling_cell) > 0:
            new_patch_sapling = self.random.choice(available_sapling_cell)
            # and put a sapling there
            # newSapling = (int(self.model.chance_reproduceSapling * self.trees_here))
            # it has less chance of surviving if there are lots of trees there
            # new_patch_sapling.saplings_here += (newSapling - int((newSapling*(new_patch_sapling.trees_here/100))))
            new_patch_sapling.saplings_here += int(self.model.chance_reproduceSapling * self.trees_here) # if there are no trees, this'll be zero

        # chance of reproducing young scrub
        neighborhood_list = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)
        items_in_neighborhood = list(map(self.model.grid.get_cell_list_contents, neighborhood_list)) 
        # pick one that has less than 1000 young scrubs
        only_habitat_cells = [obj for obj in items_in_neighborhood if (isinstance(x, habitatAgent) for x in obj)]
        no_herbivores = [item[0] for item in only_habitat_cells]
        available_youngscrub_cell = [i for i in no_herbivores if i.youngscrub_here < 1000 and i.scrub_here < 100]
        if len(available_youngscrub_cell) > 0:
            new_patch_youngscrub = self.random.choice(available_youngscrub_cell) 
            # and put a young scrub there
            new_patch_youngscrub.youngscrub_here += int(self.model.chance_reproduceYoungScrub * self.scrub_here) # if there are no trees, this'll be zero

        # chance of bare ground becoming grassland
        amount_regrown = self.model.chance_regrowGrass * self.perc_bareground_here
        self.perc_grass_here += int(amount_regrown)
        self.perc_bareground_here -= int(amount_regrown)

        # chance of young scrub becoming mature scrub
        scrub_maturing = self.model.chance_youngScrubMatures * self.youngscrub_here
        if self.scrub_here + scrub_maturing > 100: 
            scrub_maturing = 100 - self.scrub_here
        self.scrub_here += int(scrub_maturing)
        self.youngscrub_here -= int(scrub_maturing)

        # chance of sapling becoming tree
        tree_maturing = self.model.chance_saplingBecomingTree * self.saplings_here
        if self.trees_here + tree_maturing > 100: 
            tree_maturing = 100 - self.trees_here
        self.trees_here += int(tree_maturing)
        self.saplings_here -= int(tree_maturing)
   
        # outcompeted by tree - scales depending on number of trees
        outcompeted_grass = self.model.chance_grassOutcompetedByTree * self.perc_grass_here
        self.perc_bareground_here += (int(outcompeted_grass) - int((outcompeted_grass*(self.trees_here/100))))
        self.perc_grass_here -= (int(outcompeted_grass) - int((outcompeted_grass*(self.trees_here/100))))
        outcompeted_scrub = self.model.chance_scrubOutcompetedByTree * self.scrub_here
        self.scrub_here -= (int(outcompeted_scrub) - int((outcompeted_scrub*(self.trees_here/100))))
        outcompeted_saplings = self.model.chance_saplingOutcompetedByTree * self.saplings_here
        self.saplings_here -= (int(outcompeted_saplings) - int((outcompeted_saplings*(self.trees_here/100))))
        outcompeted_youngscrub = self.model.chance_youngScrubOutcompetedByTree * self.youngscrub_here
        self.youngscrub_here -= (int(outcompeted_youngscrub) - int((outcompeted_youngscrub*(self.trees_here/100))))

        # outcompeted by mature scrub
        outcompeted_grass_byScrub = self.model.chance_grassOutcompetedByScrub * self.perc_grass_here
        self.perc_bareground_here += (int(outcompeted_grass_byScrub) - int((outcompeted_grass_byScrub*(self.scrub_here/100))))
        self.perc_grass_here -= (int(outcompeted_grass_byScrub) - int((outcompeted_grass_byScrub*(self.scrub_here/100))))
        outcompeted_saplings_byScrub = self.model.chance_saplingOutcompetedByScrub * self.saplings_here
        self.saplings_here -= (int(outcompeted_saplings_byScrub) - int((outcompeted_saplings_byScrub*(self.scrub_here/100))))
        outcompeted_youngscrub = self.model.chance_youngScrubOutcompetedByScrub * self.youngscrub_here
        self.youngscrub_here -= (int(outcompeted_youngscrub) - int((outcompeted_youngscrub*(self.scrub_here/100))))



        # print(self.unique_id, "trees", self.trees_here, "scrub", self.scrub_here, "saplings", self.saplings_here, "youngScrub", self.youngscrub_here, "grass", self.perc_grass_here, "Bare", self.perc_bareground_here)
        
        # reassess dominant condition
        if self.trees_here < 10 and self.scrub_here < 10 and self.perc_grass_here >= 50:
            self.condition = "grassland"
        if self.trees_here < 10 and self.scrub_here < 10 and self.perc_bareground_here > 50:
            self.condition = "bare_ground"
        if self.trees_here < 10 and self.scrub_here >= 10:
            self.condition = "thorny_scrubland"
        if self.trees_here >= 10:
            self.condition = "woodland"


class roeDeer_agent(RandomWalker):
    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        # move & reduce energy
        self.roe_move()
        living = True
        self.energy -= 1

        # Eat what's on my patch: roe deer are broswers, so randomly choose any habitat to eat
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        habitat_choices = ["saplings", "trees", "scrub", "youngScrub", "grass"]
        # pick a habitat type and eat it 
        for habitat_types in habitat_choices:
            # pick a habitat type
            my_choice = rchoice(habitat_choices)
            habitat_choices.remove(my_choice)
            # if my energy is low enough, eat it 
            if self.energy < 1 and my_choice == "saplings" and habitat_patch.saplings_here > 0:
                eatenSaps = random.randint(0,self.model.roeDeer_saplingsEaten)
                eat_saplings(habitat_patch, eatenSaps)
                self.energy += (self.model.roeDeer_gain_from_Saplings * eatenSaps)
            elif self.energy < 1 and my_choice== "trees" and habitat_patch.trees_here > 0:
                eatenTrees = random.randint(0,self.model.roeDeer_treesEaten)
                eat_trees(habitat_patch, eatenTrees)
                self.energy += (self.model.roeDeer_gain_from_Trees * eatenTrees)
            elif self.energy < 1 and my_choice == "scrub" and habitat_patch.scrub_here > 0:
                eatenScrub = random.randint(0,self.model.roeDeer_scrubEaten)
                eat_scrub(habitat_patch, eatenScrub)
                self.energy += (self.model.roeDeer_gain_from_Scrub * eatenScrub)
            elif self.energy < 1 and my_choice == "youngscrub" and habitat_patch.youngscrub_here > 0:
                eatenYoungScrub = random.randint(0,self.model.roeDeer_youngScrubEaten)
                eat_youngscrub(habitat_patch, eatenYoungScrub)
                self.energy += (self.model.roeDeer_gain_from_YoungScrub * eatenYoungScrub)

            elif self.energy < 1 and my_choice == "grass" and habitat_patch.perc_grass_here > 0:
                eatenGrass = random.randint(0,self.model.roeDeer_impactGrass)
                eat_grass(habitat_patch, eatenGrass)
                self.energy += (self.model.roeDeer_gain_from_grass * eatenGrass)
        # don't let energy be above 1
        if self.energy > 1:
            self.energy = 1
        
        # if roe deer's energy is less than 0, die 
        if self.energy <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        # I can reproduce in May & June (assuming model starts in Jan at beginning of year, May & June = time steps 5&6 out of every 12 months)
        if living and (random.random() < self.model.roeDeer_reproduce) and (5 <= self.model.schedule.time < 7 or 17 <= self.model.schedule.time < 19 or 29 <= self.model.schedule.time < 31 or 41 <= self.model.schedule.time < 43 or 53 <= self.model.schedule.time < 55 or 65 <= self.model.schedule.time < 67 or 77 <= self.model.schedule.time < 79 or 89 <= self.model.schedule.time < 91 or 101 <= self.model.schedule.time < 103 or 113 <= self.model.schedule.time < 115 or 125 <= self.model.schedule.time < 127 or 137 <= self.model.schedule.time < 139 or 149 <= self.model.schedule.time < 151 or 161 <= self.model.schedule.time < 163 or 173 <= self.model.schedule.time < 175 or 185 <= self.model.schedule.time < 187 or 197 <= self.model.schedule.time < 199 or 209 <= self.model.schedule.time < 211 or 221 <= self.model.schedule.time < 223 or 233 <= self.model.schedule.time < 235 or 245 <= self.model.schedule.time < 247 or 257 <= self.model.schedule.time < 259 or 269 <= self.model.schedule.time < 271 or 281 <= self.model.schedule.time < 283 or 293 <= self.model.schedule.time < 295):
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
        self.energy -= 1

        # Eat what's on my patch
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        habitat_choices = ["saplings", "trees", "scrub", "youngScrub", "grass"]
        # pick a habitat type and eat it 
        for habitat_types in habitat_choices:
            # pick a habitat type
            my_choice = rchoice(habitat_choices)
            habitat_choices.remove(my_choice)
            # if my energy is low enough, eat it 
            if self.energy < 1 and my_choice == "saplings" and habitat_patch.saplings_here > 0:
                eatenSaps = random.randint(0,self.model.ponies_saplingsEaten)
                eat_saplings(habitat_patch, eatenSaps)
                self.energy += (self.model.ponies_gain_from_Saplings * eatenSaps)
            elif self.energy < 1 and my_choice== "trees" and habitat_patch.trees_here > 0:
                eatenTrees = random.randint(0,self.model.ponies_treesEaten)
                eat_trees(habitat_patch, eatenTrees)
                self.energy += (self.model.ponies_gain_from_Trees * eatenTrees)
            elif self.energy < 1 and my_choice == "scrub" and habitat_patch.scrub_here > 0:
                eatenScrub = random.randint(0,self.model.ponies_scrubEaten)
                eat_scrub(habitat_patch, eatenScrub)
                self.energy += (self.model.ponies_gain_from_Scrub*eatenScrub)
            elif self.energy < 1 and my_choice == "youngscrub" and habitat_patch.youngscrub_here > 0:
                eatenYoungScrub = random.randint(0,self.model.ponies_youngScrubEaten)
                eat_youngscrub(habitat_patch, eatenYoungScrub)
                self.energy += (self.model.ponies_gain_from_YoungScrub*eatenYoungScrub)
            elif self.energy < 1 and my_choice == "grass" and habitat_patch.perc_grass_here > 0:
                eatenGrass = random.randint(0,self.model.ponies_impactGrass)
                eat_grass(habitat_patch, eatenGrass)
                self.energy += (self.model.ponies_gain_from_grass*eatenGrass)

        if self.energy > 1:
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

        # Eat what's on my patch
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        habitat_choices = ["saplings", "trees", "scrub", "youngscrub", "grass"]

        # pick a habitat type and eat it 
        for habitat_types in habitat_choices:
            # pick a habitat type
            my_choice = rchoice(habitat_choices)
            habitat_choices.remove(my_choice)
            # if my energy is low enough, eat it 
            if self.energy < 1 and my_choice == "saplings" and habitat_patch.saplings_here > 0:
                eatenSaps = random.randint(0,self.model.cows_saplingsEaten)
                eat_saplings(habitat_patch, eatenSaps)
                self.energy += (self.model.cows_gain_from_Saplings*eatenSaps)
            elif self.energy < 1 and my_choice== "trees" and habitat_patch.trees_here > 0:
                eatenTrees = random.randint(0,self.model.cows_treesEaten)
                eat_trees(habitat_patch, eatenTrees)
                self.energy += (self.model.cows_gain_from_Trees*eatenTrees)
            elif self.energy < 1 and my_choice == "scrub" and habitat_patch.scrub_here > 0:
                eatenScrub = random.randint(0,self.model.cows_scrubEaten)
                eat_scrub(habitat_patch, eatenScrub)
                self.energy += (self.model.cows_gain_from_Scrub*eatenScrub)
            elif self.energy < 1 and my_choice == "youngscrub" and habitat_patch.youngscrub_here > 0:
                eatenYoungScrub = random.randint(0,self.model.cows_youngScrubEaten)
                eat_youngscrub(habitat_patch, eatenYoungScrub)
                self.energy += (self.model.cows_gain_from_YoungScrub*eatenYoungScrub)
            elif self.energy < 1 and my_choice == "grass" and habitat_patch.perc_grass_here > 0:
                eatenGrass = random.randint(0,self.model.cows_impactGrass)
                eat_grass(habitat_patch, eatenGrass)
                self.energy += (self.model.cows_gain_from_grass*eatenGrass)
        if self.energy > 1:
            self.energy = 1

        # if cow's energy is less than 0, die 
        if self.energy <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        # I reproduce in April, May, and June (assuming model starts in Jan at beginning of year, April, May & June = time steps 4-6 out of every 12 months)
        if living and (random.random() < self.model.cows_reproduce) and (4 <= self.model.schedule.time < 7 or 16 <= self.model.schedule.time < 19 or 28 <= self.model.schedule.time < 31 or 40 <= self.model.schedule.time < 43 or 52 <= self.model.schedule.time < 55 or 64 <= self.model.schedule.time < 67 or 76 <= self.model.schedule.time < 79 or 88 <= self.model.schedule.time < 91 or 100 <= self.model.schedule.time < 103 or 112 <= self.model.schedule.time < 115 or 124 <= self.model.schedule.time < 127 or 136 <= self.model.schedule.time < 139 or 148 <= self.model.schedule.time < 151 or 160 <= self.model.schedule.time < 163 or 172 <= self.model.schedule.time < 175 or 184 <= self.model.schedule.time < 187 or 196 <= self.model.schedule.time < 199 or 208 <= self.model.schedule.time < 211 or 220 <= self.model.schedule.time < 223 or 232 <= self.model.schedule.time < 235 or 244 <= self.model.schedule.time < 247 or 256 <= self.model.schedule.time < 259 or 268 <= self.model.schedule.time < 271 or 280 <= self.model.schedule.time < 283 or 292 <= self.model.schedule.time < 295):
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

        # Eat what's on my patch
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        habitat_choices = ["saplings", "trees", "scrub", "youngscrub", "grass"]

        # pick a habitat type and eat it 
        for habitat_types in habitat_choices:
            # pick a habitat type
            my_choice = rchoice(habitat_choices)
            habitat_choices.remove(my_choice)
            # if my energy is low enough, eat it 
            if self.energy < 1 and my_choice == "saplings" and habitat_patch.saplings_here > 0:
                eatenSaps = random.randint(0,self.model.fallowDeer_saplingsEaten)
                eat_saplings(habitat_patch, eatenSaps)
                self.energy += (self.model.fallowDeer_gain_from_Saplings*eatenSaps)
            elif self.energy < 1 and my_choice== "trees" and habitat_patch.trees_here > 0:
                eatenTrees = random.randint(0,self.model.fallowDeer_treesEaten)
                eat_trees(habitat_patch, eatenTrees)
                self.energy += (self.model.fallowDeer_gain_from_Trees*eatenTrees)
            elif self.energy < 1 and my_choice == "scrub" and habitat_patch.scrub_here > 0:
                eatenScrub = random.randint(0,self.model.fallowDeer_scrubEaten)
                eat_scrub(habitat_patch, eatenScrub)
                self.energy += (self.model.fallowDeer_gain_from_Scrub*eatenScrub)
            elif self.energy < 1 and my_choice == "youngscrub" and habitat_patch.youngscrub_here > 0:
                eatenYoungScrub = random.randint(0,self.model.fallowDeer_youngScrubEaten)
                eat_youngscrub(habitat_patch, eatenYoungScrub)
                self.energy += (self.model.fallowDeer_gain_from_YoungScrub *eatenYoungScrub)
            elif self.energy < 1 and my_choice == "grass" and habitat_patch.perc_grass_here > 0:
                eatenGrass = random.randint(0,self.model.fallowDeer_impactGrass)
                eat_grass(habitat_patch, eatenGrass)
                self.energy += (self.model.fallowDeer_gain_from_grass*eatenGrass)
        if self.energy > 1:
            self.energy = 1
    
        # if fallow deer's energy is less than 0, die 
        if self.energy <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False
            
        # I reproduce in May & June (assuming model starts in Jan at beginning of year, May & June = time steps 5&6 out of every 12 months)
        if living and (random.random() < self.model.fallowDeer_reproduce) and (5 <= self.model.schedule.time < 7 or 17 <= self.model.schedule.time < 19 or 29 <= self.model.schedule.time < 31 or 41 <= self.model.schedule.time < 43 or 53 <= self.model.schedule.time < 55 or 65 <= self.model.schedule.time < 67 or 77 <= self.model.schedule.time < 79 or 89 <= self.model.schedule.time < 91 or 101 <= self.model.schedule.time < 103 or 113 <= self.model.schedule.time < 115 or 125 <= self.model.schedule.time < 127 or 137 <= self.model.schedule.time < 139 or 149 <= self.model.schedule.time < 151 or 161 <= self.model.schedule.time < 163 or 173 <= self.model.schedule.time < 175 or 185 <= self.model.schedule.time < 187 or 197 <= self.model.schedule.time < 199 or 209 <= self.model.schedule.time < 211 or 221 <= self.model.schedule.time < 223 or 233 <= self.model.schedule.time < 235 or 245 <= self.model.schedule.time < 247 or 257 <= self.model.schedule.time < 259 or 269 <= self.model.schedule.time < 271 or 281 <= self.model.schedule.time < 283 or 293 <= self.model.schedule.time < 295):
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

        # Eat what's on my patch
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        habitat_choices = ["saplings", "trees", "scrub", "youngscrub", "grass"]
        # pick a habitat type and eat it 
        for habitat_types in habitat_choices:
            # pick a habitat type
            my_choice = rchoice(habitat_choices)
            habitat_choices.remove(my_choice)
            # if my energy is low enough, eat it 
            if self.energy < 1 and my_choice == "saplings" and habitat_patch.saplings_here > 0:
                eatenSaps = random.randint(0,self.model.redDeer_saplingsEaten)
                eat_saplings(habitat_patch, eatenSaps)
                self.energy += (self.model.redDeer_gain_from_Saplings*eatenSaps)
            elif self.energy < 1 and my_choice== "trees" and habitat_patch.trees_here > 0:
                eatenTrees = random.randint(0,self.model.redDeer_treesEaten)
                eat_trees(habitat_patch, eatenTrees)
                self.energy += (self.model.redDeer_gain_from_Trees*eatenTrees)
            elif self.energy < 1 and my_choice == "scrub" and habitat_patch.scrub_here > 0:
                eatenScrub = random.randint(0,self.model.redDeer_scrubEaten)
                eat_scrub(habitat_patch, eatenScrub)
                self.energy += (self.model.redDeer_gain_from_Scrub*eatenScrub)
            elif self.energy < 1 and my_choice == "youngscrub" and habitat_patch.youngscrub_here > 0:
                eatenYoungScrub = random.randint(0,self.model.redDeer_youngScrubEaten)
                eat_youngscrub(habitat_patch, eatenYoungScrub)
                self.energy += (self.model.redDeer_gain_from_YoungScrub*eatenYoungScrub)
            elif self.energy < 1 and my_choice == "grass" and habitat_patch.perc_grass_here > 0:
                eatenGrass = random.randint(0,self.model.redDeer_impactGrass)
                eat_grass(habitat_patch, eatenGrass)
                self.energy += (self.model.redDeer_gain_from_grass*eatenGrass)
        if self.energy > 1:
            self.energy = 1

        # if red deer's energy is less than 0, die 
        if self.energy <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        # I reproduce in May & June (assuming model starts in Jan at beginning of year, May & June = time steps 5&6 out of every 12 months)
        if living and (random.random() < self.model.redDeer_reproduce) and (5 <= self.model.schedule.time < 7 or 17 <= self.model.schedule.time < 19 or 29 <= self.model.schedule.time < 31 or 41 <= self.model.schedule.time < 43 or 53 <= self.model.schedule.time < 55 or 65 <= self.model.schedule.time < 67 or 77 <= self.model.schedule.time < 79 or 89 <= self.model.schedule.time < 91 or 101 <= self.model.schedule.time < 103 or 113 <= self.model.schedule.time < 115 or 125 <= self.model.schedule.time < 127 or 137 <= self.model.schedule.time < 139 or 149 <= self.model.schedule.time < 151 or 161 <= self.model.schedule.time < 163 or 173 <= self.model.schedule.time < 175 or 185 <= self.model.schedule.time < 187 or 197 <= self.model.schedule.time < 199 or 209 <= self.model.schedule.time < 211 or 221 <= self.model.schedule.time < 223 or 233 <= self.model.schedule.time < 235 or 245 <= self.model.schedule.time < 247 or 257 <= self.model.schedule.time < 259 or 269 <= self.model.schedule.time < 271 or 281 <= self.model.schedule.time < 283 or 293 <= self.model.schedule.time < 295):
            # Create a new roe deer and divide energy:
            self.energy = np.random.uniform(0, self.energy)
            fawn = redDeer(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
            self.model.grid.place_agent(fawn, self.pos)
            self.model.schedule.add(fawn)



class tamworthPigs(RandomWalker):
    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        # move & reduce energy
        self.random_move()
        living = True
        self.energy -= 1
        # Eat what's on my patch
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        habitat_choices = ["saplings", "youngscrub", "grass"]
        # pick a habitat type and eat it 
        for habitat_types in habitat_choices:
            # pick a habitat type
            my_choice = rchoice(habitat_choices)
            habitat_choices.remove(my_choice)
            # if my energy is low enough, eat it 
            if self.energy < 1 and my_choice == "saplings" and habitat_patch.saplings_here > 0:
                eatenSaps = random.randint(0,self.model.pigs_saplingsEaten)
                eat_saplings(habitat_patch, eatenSaps)
                self.energy += (self.model.pigs_gain_from_Saplings*eatenSaps)
            elif self.energy < 1 and my_choice == "youngscrub" and habitat_patch.youngscrub_here > 0:
                eatenYoungScrub = random.randint(0,self.model.pigs_youngScrubEaten)
                eat_youngscrub(habitat_patch, eatenYoungScrub)
                self.energy += (self.model.pigs_gain_from_YoungScrub*eatenYoungScrub)
            elif self.energy < 1 and my_choice == "grass" and habitat_patch.perc_grass_here > 0:
                eatenGrass = random.randint(0,self.model.pigs_impactGrass)
                eat_grass(habitat_patch, eatenGrass)
                self.energy += (self.model.pigs_gain_from_grass*eatenGrass)
 
        if self.energy > 1:
            self.energy = 1
    
        # if pig's energy is less than 0, die 
        if self.energy <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False
            
        # pigs reproduce Jan - July (1 - 7, < 8)
        if living and (random.random() < self.model.pigs_reproduce) and (1 <= self.model.schedule.time < 8 or 13 <= self.model.schedule.time < 20 or 25 <= self.model.schedule.time < 32 or 37 <= self.model.schedule.time < 44 or 49 <= self.model.schedule.time < 56 or 61 <= self.model.schedule.time < 68 or 73 <= self.model.schedule.time < 80 or 85 <= self.model.schedule.time < 92 or 97 <= self.model.schedule.time < 104 or 109 <= self.model.schedule.time < 116 or 121 <= self.model.schedule.time < 128 or 133 <= self.model.schedule.time < 140 or 145 <= self.model.schedule.time < 152 or 157 <= self.model.schedule.time < 164 or 169 <= self.model.schedule.time < 176 or 181 <= self.model.schedule.time < 188 or 193 <= self.model.schedule.time < 200 or 205 <= self.model.schedule.time < 212 or 217 <= self.model.schedule.time < 224 or 229 <= self.model.schedule.time < 236 or 241 <= self.model.schedule.time < 248 or 253 <= self.model.schedule.time < 260 or 265 <= self.model.schedule.time < 272 or 277 <= self.model.schedule.time < 284 or 289 <= self.model.schedule.time < 296):
            # divide my energy
            self.energy = np.random.uniform(0, self.energy)
            # Pick a number of piglets to have
            for _ in range(random.randint(1,10)):
                piglet = tamworthPigs(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
                self.model.grid.place_agent(piglet, self.pos)
                self.model.schedule.add(piglet)






                                # # # # ------ Define the model ------ # # # # 

class KneppModel(Model):
    
    
    def __init__(self,             
            chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
            chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
            initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland,
            roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
            roeDeer_impactGrass, roeDeer_saplingsEaten, roeDeer_youngScrubEaten, roeDeer_treesEaten, roeDeer_scrubEaten,
            ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
            ponies_impactGrass, ponies_saplingsEaten, ponies_youngScrubEaten, ponies_treesEaten, ponies_scrubEaten, 
            cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
            cows_impactGrass, cows_saplingsEaten, cows_youngScrubEaten, cows_treesEaten, cows_scrubEaten, 
            fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
            fallowDeer_impactGrass, fallowDeer_saplingsEaten, fallowDeer_youngScrubEaten, fallowDeer_treesEaten, fallowDeer_scrubEaten,
            redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
            redDeer_impactGrass, redDeer_saplingsEaten, redDeer_youngScrubEaten, redDeer_treesEaten, redDeer_scrubEaten, 
            pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
            pigs_impactGrass, pigs_saplingsEaten, pigs_youngScrubEaten, 
            width, height):

        # set parameters
        self.initial_roeDeer = initial_roeDeer
        self.initial_grassland = initial_grassland
        self.initial_woodland = initial_woodland
        self.initial_scrubland = initial_scrubland
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
        self.roeDeer_treesEaten = roeDeer_treesEaten
        self.roeDeer_scrubEaten = roeDeer_scrubEaten
        self.roeDeer_impactGrass = roeDeer_impactGrass
        self.roeDeer_saplingsEaten = roeDeer_saplingsEaten
        self.roeDeer_youngScrubEaten = roeDeer_youngScrubEaten
        # exmoor pony parameters
        self.ponies_gain_from_grass = ponies_gain_from_grass
        self.ponies_gain_from_Trees =ponies_gain_from_Trees
        self.ponies_gain_from_Scrub = ponies_gain_from_Scrub
        self.ponies_gain_from_Saplings = ponies_gain_from_Saplings
        self.ponies_gain_from_YoungScrub = ponies_gain_from_YoungScrub
        self.ponies_impactGrass = ponies_impactGrass
        self.ponies_saplingsEaten = ponies_saplingsEaten
        self.ponies_youngScrubEaten = ponies_youngScrubEaten
        self.ponies_treesEaten = ponies_treesEaten
        self.ponies_scrubEaten = ponies_scrubEaten
        # cow parameters
        self.cows_reproduce = cows_reproduce
        self.cows_gain_from_grass = cows_gain_from_grass
        self.cows_gain_from_Trees =cows_gain_from_Trees
        self.cows_gain_from_Scrub = cows_gain_from_Scrub
        self.cows_gain_from_Saplings = cows_gain_from_Saplings
        self.cows_gain_from_YoungScrub = cows_gain_from_YoungScrub
        self.cows_impactGrass = cows_impactGrass
        self.cows_saplingsEaten = cows_saplingsEaten
        self.cows_youngScrubEaten = cows_youngScrubEaten
        self.cows_treesEaten = cows_treesEaten
        self.cows_scrubEaten = cows_scrubEaten
        # fallow deer parameters
        self.fallowDeer_reproduce = fallowDeer_reproduce
        self.fallowDeer_gain_from_grass = fallowDeer_gain_from_grass
        self.fallowDeer_gain_from_Trees =fallowDeer_gain_from_Trees
        self.fallowDeer_gain_from_Scrub = fallowDeer_gain_from_Scrub
        self.fallowDeer_gain_from_Saplings = fallowDeer_gain_from_Saplings
        self.fallowDeer_gain_from_YoungScrub = fallowDeer_gain_from_YoungScrub
        self.fallowDeer_impactGrass = fallowDeer_impactGrass
        self.fallowDeer_saplingsEaten = fallowDeer_saplingsEaten
        self.fallowDeer_youngScrubEaten = fallowDeer_youngScrubEaten
        self.fallowDeer_treesEaten = fallowDeer_treesEaten
        self.fallowDeer_scrubEaten = fallowDeer_scrubEaten
        # red deer parameters
        self.redDeer_reproduce = redDeer_reproduce
        self.redDeer_gain_from_grass = redDeer_gain_from_grass
        self.redDeer_gain_from_Trees =redDeer_gain_from_Trees
        self.redDeer_gain_from_Scrub = redDeer_gain_from_Scrub
        self.redDeer_gain_from_Saplings = redDeer_gain_from_Saplings
        self.redDeer_gain_from_YoungScrub = redDeer_gain_from_YoungScrub
        self.redDeer_impactGrass = redDeer_impactGrass
        self.redDeer_saplingsEaten = redDeer_saplingsEaten
        self.redDeer_youngScrubEaten = redDeer_youngScrubEaten
        self.redDeer_treesEaten = redDeer_treesEaten
        self.redDeer_scrubEaten = redDeer_scrubEaten
        # pig parameters
        self.pigs_reproduce = pigs_reproduce
        self.pigs_gain_from_grass = pigs_gain_from_grass
        self.pigs_gain_from_Saplings = pigs_gain_from_Saplings
        self.pigs_gain_from_YoungScrub = pigs_gain_from_YoungScrub
        self.pigs_impactGrass = pigs_impactGrass
        self.pigs_saplingsEaten = pigs_saplingsEaten
        self.pigs_youngScrubEaten = pigs_youngScrubEaten
        # other parameters
        self.height = height
        self.width = width
        # set grid & schedule
        self.grid = MultiGrid(width, height, True) # this grid allows for multiple agents on same cell
        self.schedule = RandomActivationByBreed(self)
        self.running = True
        self.current_id = 0

        
        # Create habitat patches
        if (initial_woodland + initial_grassland + initial_scrubland) >= 100:
            # rescale it to 100
            prob_grassland = initial_grassland/(initial_woodland + initial_grassland + initial_scrubland)
            prob_scrubland = initial_scrubland/(initial_woodland + initial_grassland + initial_scrubland)
            prob_woodland = initial_woodland/(initial_woodland + initial_grassland + initial_scrubland)
            # make bare ground = 0 
            prob_bare_ground = 0
        else:
            prob_grassland = initial_grassland/100
            prob_scrubland = initial_scrubland/100
            prob_woodland = initial_woodland/100
            prob_bare_ground = 1-((initial_grassland + initial_scrubland + initial_woodland)/100)
        count = 0
        for _, x, y in self.grid.coord_iter():
            condition = np.random.choice(["grassland", "thorny_scrubland", "woodland", "bare_ground"], p=[prob_grassland, prob_scrubland, prob_woodland, prob_bare_ground])            
            # put a random number of trees, shrubs, etc., depending on dominant condition
            if condition == "grassland": # more than 50% grassland, no more than 10 mature trees/shrubs
                count +=1
                trees_here = random.randint(0, 10)
                saplings_here = random.randint(0, 1000)
                scrub_here = random.randint(0, 10)
                youngscrub_here = random.randint(0, 1000)
                perc_grass_here = random.randint(50, 100)
                perc_bareground_here = 100 - perc_grass_here
            if condition == "bare_ground": # more than 50% bare ground
                trees_here = random.randint(0, 10)
                saplings_here = random.randint(0, 1000)
                scrub_here = random.randint(0, 10)
                youngscrub_here = random.randint(0, 1000)
                perc_bareground_here = random.randint(50, 100)
                perc_grass_here = 100 - perc_bareground_here
            if condition == "thorny_scrubland":  # at least 10 scrub plants, no more than 10 trees
                trees_here = random.randint(0, 10)
                saplings_here = random.randint(0, 1000)
                scrub_here = random.randint(10, 100)
                youngscrub_here = random.randint(0, 1000)
                perc_grass_here = random.randint(0, 100)
                perc_bareground_here = 100 - perc_grass_here
            if condition == "woodland":  # woodland has 10-100 trees
                trees_here = random.randint(10, 100)
                saplings_here = random.randint(0, 1000)
                scrub_here = random.randint(0, 100)
                youngscrub_here = random.randint(0, 1000)
                perc_grass_here = random.randint(0, 100)
                perc_bareground_here = 100 - perc_grass_here
            patch = habitatAgent(self.next_id(), (x, y), self, condition, trees_here, saplings_here, scrub_here, youngscrub_here, perc_grass_here, perc_bareground_here)
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
                            "Grassland": lambda m: self.count_condition(m, "grassland"),
                            "Woodland": lambda m: self.count_condition(m, "woodland"),
                            "Thorny Scrub": lambda m: self.count_condition(m, "thorny_scrubland"),
                            "Bare ground": lambda m: self.count_condition(m, "bare_ground")
                            }
                            )


        self.running = True
        self.datacollector.collect(self)



    def add_herbivores(self, herbivore, count):
        x = random.randrange(self.width)
        y = random.randrange(self.height)
        energy = np.random.uniform(0, 1)
        for i in range(count):
            to_add = herbivore(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(to_add, (x, y))
            self.schedule.add(to_add)


    def remove_herbivores(self, herbivore, count):
        for i in range (count):
            to_remove = self.schedule.agents_by_breed[herbivore].items()
            if len(to_remove) > 0:
                my_choice = random.choice(list(to_remove))[1]
                self.grid._remove_agent(my_choice.pos, my_choice)
                self.schedule.remove(my_choice)



    def count_condition(self, model, habitat_condition):
        # want to count grass, wood, scrub, bare ground in each patch
        count = 0
        for key, value in model.schedule.agents_by_breed[habitatAgent].items():
            if value.condition == habitat_condition:
                count += 1
        # return percentage of entire area
        return int((count/1800)*100)


    def step(self):
        self.schedule.step()
        # count how many there are, then step
        self.datacollector.collect(self)
        # Jan 2005 - March 2009
        if self.schedule.time == 50:
            self.add_herbivores(exmoorPony, 23)
            self.add_herbivores(longhornCattle, 53)
            self.add_herbivores(tamworthPigs, 20)
        # March 2010
        if self.schedule.time == 62: 
            results_2 = self.datacollector.get_model_vars_dataframe()
            exmoorValue = results_2.iloc[62]['Exmoor pony']
            if exmoorValue >= 13: # randomly choose that many exmoor ponies and delete them
                number_to_subtract = -13 + exmoorValue
                self.remove_herbivores(exmoorPony, number_to_subtract)
            else: # add them
                number_to_add = 13 - exmoorValue
                self.add_herbivores(exmoorPony, number_to_add)
            cowValue = results_2.iloc[62]['Longhorn cattle']
            if cowValue >= 77:
                number_to_subtract = -77 + cowValue
                self.remove_herbivores(longhornCattle, number_to_subtract)
            else:
                number_to_add = 77 - cowValue
                self.add_herbivores(longhornCattle, number_to_add)
            fallowValue = results_2.iloc[62]['Fallow deer']
            if fallowValue >= 42:
                number_to_subtract = -42 + fallowValue
                self.remove_herbivores(fallowDeer, number_to_subtract)
            else:
                number_to_add = 42 - fallowValue
                self.add_herbivores(fallowDeer, number_to_add)
            pigsValue = results_2.iloc[62]['Tamworth pigs']
            if pigsValue >= 17:
                number_to_subtract = -17 + pigsValue
                self.remove_herbivores(tamworthPigs, number_to_subtract)
            else:
                number_to_add = 17 - pigsValue
                self.add_herbivores(tamworthPigs, number_to_add)
        # 2011
        if self.schedule.time == 74:
            results_3 = self.datacollector.get_model_vars_dataframe()
            exmoorValue = results_3.iloc[74]['Exmoor pony']
            if exmoorValue >= 15:
                number_to_subtract = -15 + exmoorValue
                self.remove_herbivores(exmoorPony, number_to_subtract)
            else:
                number_to_add = 15 - exmoorValue
                self.add_herbivores(exmoorPony, number_to_add)
            cowValue = results_3.iloc[74]['Longhorn cattle']
            if cowValue >= 92:
                number_to_subtract = -92 + cowValue
                self.remove_herbivores(longhornCattle, number_to_subtract)
            else:
                number_to_add = 92 - cowValue
                self.add_herbivores(longhornCattle, number_to_add)
            fallowValue = results_3.iloc[74]['Fallow deer']
            if fallowValue >= 81:
                number_to_subtract = -81 + fallowValue
                self.remove_herbivores(fallowDeer, number_to_subtract)
            else:
                number_to_add = 81 - fallowValue
                self.add_herbivores(fallowDeer, number_to_add)
            pigsValue = results_3.iloc[74]['Tamworth pigs']
            if pigsValue >= 22:
                number_to_subtract = -22 + pigsValue
                self.remove_herbivores(tamworthPigs, number_to_subtract)
            else:
                number_to_add = 22 - pigsValue
                self.add_herbivores(tamworthPigs, number_to_add)
        # 2012
        if self.schedule.time == 86:
            results_4 = self.datacollector.get_model_vars_dataframe()
            exmoorValue = results_4.iloc[86]['Exmoor pony']
            if exmoorValue >= 17:
                number_to_subtract = -17 + exmoorValue
                self.remove_herbivores(exmoorPony, number_to_subtract)
            else:
                number_to_add = 17 - exmoorValue
                self.add_herbivores(exmoorPony, number_to_add)
            cowValue = results_4.iloc[86]['Longhorn cattle']
            if cowValue >= 116:
                number_to_subtract = -116 + cowValue
                self.remove_herbivores(longhornCattle, number_to_subtract)
            else:
                number_to_add = 116 - cowValue
                self.add_herbivores(longhornCattle, number_to_add)
            fallowValue = results_4.iloc[86]['Fallow deer']
            if fallowValue >= 100:
                number_to_subtract = -100 + fallowValue
                self.remove_herbivores(fallowDeer, number_to_subtract)
            else:
                number_to_add = 100 - fallowValue
                self.add_herbivores(fallowDeer, number_to_add)
            pigsValue = results_4.iloc[86]['Tamworth pigs']
            if pigsValue >= 33:
                number_to_subtract = -33 + pigsValue
                self.remove_herbivores(tamworthPigs, number_to_subtract)
            else:
                number_to_add = 33 - pigsValue
                self.add_herbivores(tamworthPigs, number_to_add)
        # 2013
        if self.schedule.time == 98:
            results_5 = self.datacollector.get_model_vars_dataframe()
            # Exmoor ponies: 10
            exmoorValue = results_5.iloc[98]['Exmoor pony']
            if exmoorValue >= 10:
                number_to_subtract = -10 + exmoorValue
                self.remove_herbivores(exmoorPony, number_to_subtract)
            else:
                number_to_add = 10 - exmoorValue
                self.add_herbivores(exmoorPony, number_to_add)
            # Longhorn cattle: 129
            cowValue = results_5.iloc[98]['Longhorn cattle']
            if cowValue >= 129:
                number_to_subtract = -129 + cowValue
                self.remove_herbivores(longhornCattle, number_to_subtract)
            else:
                number_to_add = 129 - cowValue
                self.add_herbivores(longhornCattle, number_to_add)
            # Fallow deer: 100
            fallowValue = results_5.iloc[98]['Fallow deer']
            if fallowValue >= 100:
                number_to_subtract = -100 + fallowValue
                self.remove_herbivores(fallowDeer, number_to_subtract)
            else:
                number_to_add = 100 - fallowValue
                self.add_herbivores(fallowDeer, number_to_add)
            # Pigs: 6
            pigsValue = results_5.iloc[98]['Tamworth pigs']
            if pigsValue >= 6:
                number_to_subtract = -6 + pigsValue
                self.remove_herbivores(tamworthPigs, number_to_subtract)
            else:
                number_to_add = 6 - pigsValue
                self.add_herbivores(tamworthPigs, number_to_add)
            # Red deer: add 13
            self.add_herbivores(redDeer, 13)
        # 2014
        if self.schedule.time == 110:
            results_6 = self.datacollector.get_model_vars_dataframe()
            exmoorValue = results_6.iloc[110]['Exmoor pony']
            if exmoorValue >= 10:
                number_to_subtract = -10 + exmoorValue
                self.remove_herbivores(exmoorPony, number_to_subtract)
            else:
                number_to_add = 10 - exmoorValue
                self.add_herbivores(exmoorPony, number_to_add)
            cowValue = results_6.iloc[110]['Longhorn cattle']
            if cowValue >= 264:
                number_to_subtract = -264 + cowValue
                self.remove_herbivores(longhornCattle, number_to_subtract)
            else:
                number_to_add = 264 - cowValue
                self.add_herbivores(longhornCattle, number_to_add)
            fallowValue = results_6.iloc[110]['Fallow deer']
            if fallowValue >= 100:
                number_to_subtract = -100 + fallowValue
                self.remove_herbivores(fallowDeer, number_to_subtract)
            else:
                number_to_add = 100 - fallowValue
                self.add_herbivores(fallowDeer, number_to_add)
            # Pigs: 18
            pigsValue = results_6.iloc[110]['Tamworth pigs']
            if pigsValue >= 18:
                number_to_subtract = -18 + pigsValue
                self.remove_herbivores(tamworthPigs, number_to_subtract)
            else:
                number_to_add = 18 - pigsValue
                self.add_herbivores(tamworthPigs, number_to_add)
            redDeerValue = results_6.iloc[110]['Red deer']
            if redDeerValue >= 13:
                number_to_subtract = -13 + redDeerValue
                self.remove_herbivores(redDeer, number_to_subtract)
            else:
                number_to_add = 13 - redDeerValue
                self.add_herbivores(redDeer, number_to_add)
        
        # March 2015
        if self.schedule.time == 122:
            results_7 = self.datacollector.get_model_vars_dataframe()
            #  Exmoor ponies: 10
            exmoorValue = results_7.iloc[122]['Exmoor pony']
            if exmoorValue >= 10:
                number_to_subtract = -10 + exmoorValue
                self.remove_herbivores(exmoorPony, number_to_subtract)
            else:
                number_to_add = 10 - exmoorValue
                self.add_herbivores(exmoorPony, number_to_add)
            # Longhorn cattle: 107
            cowValue = results_7.iloc[122]['Longhorn cattle']
            if cowValue >= 107:
                number_to_subtract = -107 + cowValue
                self.remove_herbivores(longhornCattle, number_to_subtract)
            else:
                number_to_add = 107 - cowValue
                self.add_herbivores(longhornCattle, number_to_add)
            # Fallow deer: 100
            fallowValue = results_7.iloc[122]['Fallow deer']
            if fallowValue >= 100:
                number_to_subtract = -100 + fallowValue
                self.remove_herbivores(fallowDeer, number_to_subtract)
            else:
                number_to_add = 100 - fallowValue
                self.add_herbivores(fallowDeer, number_to_add)
            # Pigs: 18
            pigsValue = results_7.iloc[122]['Tamworth pigs']
            if pigsValue >= 18:
                number_to_subtract = -18 + pigsValue
                self.remove_herbivores(tamworthPigs, number_to_subtract)
            else:
                number_to_add = 18 - pigsValue
                self.add_herbivores(tamworthPigs, number_to_add)
            # Red deer: 13
            redDeerValue = results_7.iloc[122]['Red deer']
            if redDeerValue >= 13:
                number_to_subtract = -13 + redDeerValue
                self.remove_herbivores(redDeer, number_to_subtract)
            else:
                number_to_add = 13 - redDeerValue
                self.add_herbivores(redDeer, number_to_add)
        # April 2015
        if self.schedule.time == 123:
            # April 2015: one pig culled, 5 born
            self.remove_herbivores(tamworthPigs, 1)
        # May 2015
        if self.schedule.time == 124:
            # May 2015: 8 pigs culled
            self.remove_herbivores(tamworthPigs, 8)
        # June 2015: 5 cows culled
        if self.schedule.time == 125:
            self.remove_herbivores(longhornCattle, 5)
        # August 2015: 2 fallow deer culled
        if self.schedule.time == 127:
            self.remove_herbivores(fallowDeer, 2)
        # September 2015: 2 male fallow deer culled; 2 cattle culled and 3 bulls added
        if self.schedule.time == 128:
            self.remove_herbivores(fallowDeer, 2)
            self.remove_herbivores(longhornCattle, 1)
        # Oct 2015: 2 female and 1 male fallow deer culled; 38 female cows and 1 bull removed
        if self.schedule.time == 129:
            self.remove_herbivores(fallowDeer, 3)
            self.remove_herbivores(longhornCattle, 39)
        # Nov 2015: -7 fallow deer
        if self.schedule.time == 130:
            self.remove_herbivores(fallowDeer, 7)       
        # Dec 2015: 6 fallow deer culled; 5 cows removed;
        if self.schedule.time == 131:
            self.remove_herbivores(fallowDeer, 6)
            self.remove_herbivores(longhornCattle, 5)
        # Jan 2016: 7 fallow deer culled; 4 pigs culled and 1 added
        if self.schedule.time == 132:
            self.remove_herbivores(fallowDeer, 7) 
            self.remove_herbivores(tamworthPigs, 3)
        # Feb 2016: 10 fallow deer culled; 2 pigs culled
        if self.schedule.time == 133:
            self.remove_herbivores(fallowDeer, 10)
            self.remove_herbivores(tamworthPigs, 2)
                            
                                       # # # # # # # 2016 # # # # # # #

        # March 2016: 1 pony added; 3 pigs added and 4 culled
        if self.schedule.time == 134:
            self.add_herbivores(exmoorPony, 1)
            self.remove_herbivores(tamworthPigs, 1)
        # April 2016: 1 cow added & filtering for cows
        if self.schedule.time == 135:
            self.add_herbivores(longhornCattle, 1)
        # May 2016: filtering for cows and pigs, and 2 cows culled
        if self.schedule.time == 136:
            self.remove_herbivores(longhornCattle, 2)
        # June 2016: filtering for cows, 30 cows culled and 4 added 
        if self.schedule.time == 137:
            self.remove_herbivores(longhornCattle, 26)
        # July 2016: 2 cows culled
        if self.schedule.time == 138:
            self.remove_herbivores(longhornCattle, 2)
        # August 2016: -5 fallow deer
        if self.schedule.time == 139:
            self.remove_herbivores(fallowDeer, 5)
        # September & Oct 2016: -9, +19 cows
        if self.schedule.time == 140:
            self.remove_herbivores(longhornCattle, 10)
        # November 2016: -3 fallow deer; -5 cows
        if self.schedule.time == 142:
            self.remove_herbivores(fallowDeer, 3)
            self.remove_herbivores(longhornCattle, 5)
        # December 2016: -9 fallow; -13 cows; -4 pigs
        if self.schedule.time == 143:
            self.remove_herbivores(fallowDeer, 9)
            self.remove_herbivores(longhornCattle, 13)
            self.remove_herbivores(tamworthPigs, 4)
        # January 2017: -4 pigs, +1 pig
        if self.schedule.time == 144:
            self.remove_herbivores(tamworthPigs, 3)
        # February 2017: -8 fallow deer; -3 pigs; filtering for ponies
        if self.schedule.time == 145:
            self.remove_herbivores(fallowDeer, 8)
            self.remove_herbivores(tamworthPigs, 3)



        # # # # # # # 2017 # # # # # # #
        # minus 1 exmoor pony, -12 red deer; filtering for cows
        if self.schedule.time == 146:
            self.remove_herbivores(exmoorPony, 1)
            self.remove_herbivores(redDeer, 12)
        # April 2017: -3 cows, filtering for cows and pigs
        if self.schedule.time == 147:
            self.remove_herbivores(longhornCattle, 3)
        # June & July 2017: -24 cows, +3 cows, and cow filtering condition
        if self.schedule.time == 149:
            self.remove_herbivores(longhornCattle, 21)
        # August 2017: -16 fallow deer 
        if self.schedule.time == 151:
            self.remove_herbivores(fallowDeer, 16)
        # September 2017: -5 fallow deer; -27, +23 cows
        if self.schedule.time == 152:
            self.remove_herbivores(fallowDeer, 5)
            self.remove_herbivores(longhornCattle, 4)
        # October 2017: -4 fallow deer; -2 cows
        if self.schedule.time == 153:
            self.remove_herbivores(fallowDeer, 4)
            self.remove_herbivores(longhornCattle, 2)
        # November 2017: -2 fallow deer
        if self.schedule.time == 154:
            self.remove_herbivores(fallowDeer, 2)
        # December 2017: -46 fallow deer, -1 red deer; -4 pigs
        if self.schedule.time == 155:
            self.remove_herbivores(fallowDeer, 46)
            self.remove_herbivores(redDeer, 1)
            self.remove_herbivores(tamworthPigs, 4)
        # January 2018: -9 pigs, +1 pig, and pig filtering conditions
        if self.schedule.time == 156:
            self.remove_herbivores(tamworthPigs, 8)
        # February 2018: -14 fallow; -1 red deer; -1 pig; filtering for pig and exmoor
        if self.schedule.time == 157:
            self.remove_herbivores(fallowDeer, 14)
            self.remove_herbivores(redDeer, 1)
            self.remove_herbivores(tamworthPigs, 1)

        # # # # # # # 2018 # # # # # # #
            
        # March 2018: -1 Exmoor; filtering for red and fallow deer
        if self.schedule.time == 158:
            self.remove_herbivores(exmoorPony, 1)
        # April 2018: +1 cow and filtering for cow
        if self.schedule.time == 159:
            self.add_herbivores(longhornCattle, 1)
        # June 2018: -22 cows, +2 cows; filtering for cows
        if self.schedule.time == 161:
            self.remove_herbivores(longhornCattle, 20)
        # July 2018: -1 red deer; -1 pig
        if self.schedule.time == 162:
            self.remove_herbivores(redDeer, 1)
            self.remove_herbivores(tamworthPigs, 1)
        # August 2018: -9 ponies; -15 fallow deer; -1 cattle; -1 pig
        if self.schedule.time == 163:
            self.remove_herbivores(exmoorPony, 9)
            self.remove_herbivores(fallowDeer, 15)
            self.remove_herbivores(tamworthPigs, 1)
            self.remove_herbivores(longhornCattle, 1)
        # September 2018: -19 fallow; -16 and +20 cows
        if self.schedule.time == 164:
            self.remove_herbivores(fallowDeer, 19)
            self.add_herbivores(longhornCattle, 4)
        # October 2018: -4 cows; -4 fallow; -1 pig
        if self.schedule.time == 165:
            self.remove_herbivores(longhornCattle, 4)
            self.remove_herbivores(fallowDeer, 4)
            self.remove_herbivores(tamworthPigs, 1)
        # November 2018: -8 cows; -12 pigs
        if self.schedule.time == 166:
            self.remove_herbivores(longhornCattle, 8)
            self.remove_herbivores(tamworthPigs, 12)
        # December & January 2018/2019: -19 fallow; -5 and +1 cow; -1 red deer 
        if self.schedule.time == 167:
            self.remove_herbivores(longhornCattle, 4)
            self.remove_herbivores(fallowDeer, 19)
            self.remove_herbivores(redDeer, 1)
        # February 2019: +1 pig, -2 cows
        if self.schedule.time == 169:
            self.remove_herbivores(longhornCattle, 2)
            self.add_herbivores(tamworthPigs, 1)                                                                       
                            

        # # # # # # # 2019 # # # # # # #


        # March 2019: -1 pig; fallow and red deer filters
        if self.schedule.time == 170:
            self.remove_herbivores(tamworthPigs, 1)
        # June 2019: -28 cows and cow filtering condition
        if self.schedule.time == 173:
            self.remove_herbivores(longhornCattle, 28)
        # July & Aug 2019: -3, +5 cows; -26 pigs; filtering for pigs
        if self.schedule.time == 174:
            self.remove_herbivores(tamworthPigs, 26)
            self.add_herbivores(longhornCattle, 2)
        # Sept 2019: -15 fallow; -23 and +25 cows
        if self.schedule.time == 176:
            self.remove_herbivores(fallowDeer, 15)
            self.add_herbivores(longhornCattle, 2)
        # Oct 2019: -5 cows
        if self.schedule.time == 177:
            self.remove_herbivores(longhornCattle, 5)
        # November 2019: -7 fallow deer; -1 cows; -3 red deer
        if self.schedule.time == 178:
            self.remove_herbivores(longhornCattle, 1)
            self.remove_herbivores(fallowDeer, 7)
            self.remove_herbivores(redDeer, 3)
        # December 2019: -12 fallow; -7 cows; -4 red; +1 pigs
        if self.schedule.time == 179:
            self.remove_herbivores(fallowDeer, 12)
            self.remove_herbivores(longhornCattle, 7)
            self.remove_herbivores(redDeer, 4)
            self.add_herbivores(tamworthPigs, 1)
        # January 2020: -24 fallow deer
        if self.schedule.time == 180:
            self.remove_herbivores(fallowDeer, 24)
        # February 2020: -12 fallow; -1 cow; -2 red; -2 pigs
        if self.schedule.time == 181:
            self.remove_herbivores(fallowDeer, 12)
            self.remove_herbivores(redDeer, 2)
            self.remove_herbivores(tamworthPigs, 2)
            self.remove_herbivores(longhornCattle, 1)                               

        # # # # # 2020 # # # # # #
        # March & April 2020: +15 exmoor; -1 and +3 cows; -1 pig; filtering for red and fallow deer
        if self.schedule.time == 182:
            self.add_herbivores(exmoorPony, 15)
            self.add_herbivores(longhornCattle, 2)
            self.remove_herbivores(tamworthPigs, 1)
        
        # stop running it in May 2021
        if self.schedule.time == 184:
            self.running = False 




    def run_model(self): 
        # run it for 184 steps
        for i in range(184):
            self.step()
            # print(i)
            # results_step = self.datacollector.get_model_vars_dataframe()
            # with pd.option_context('display.max_columns',None):
            #     print(results_step)
        results = self.datacollector.get_model_vars_dataframe()
        # with pd.option_context('display.max_columns',None, 'display.max_rows',None):
        #     print(results)
        return results
