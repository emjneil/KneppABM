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
import timeit


# time the program
start = timeit.default_timer()

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
        # chance of reproducing a sapling to neighboring cell or to my cell
        if self.trees_here > 0 and random.random() < self.model.chance_reproduceSapling:
            # find my neighboring cells, including the one I'm in
            neighborhood_list = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)
            items_in_neighborhood = list(map(self.model.grid.get_cell_list_contents, neighborhood_list)) 
            # pick one that has less than 1000 saplings
            only_habitat_cells = [obj for obj in items_in_neighborhood if (isinstance(x, habitatAgent) for x in obj)]
            no_herbivores = [item[0] for item in only_habitat_cells]
            available_sapling_cell = [i for i in no_herbivores if i.saplings_here < 1000]
            if len(available_sapling_cell) > 0:
                new_patch_sapling = self.random.choice(available_sapling_cell)
                # and put a sapling there
                new_patch_sapling.saplings_here += 1

        # chance of reproducing young scrub
        if self.scrub_here > 0 and random.random() < self.model.chance_reproduceYoungScrub:
            # find my neighboring cells, including the one I'm in
            neighborhood_list = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)
            items_in_neighborhood = list(map(self.model.grid.get_cell_list_contents, neighborhood_list)) 
            # pick one that has less than 1000 young scrubs
            only_habitat_cells = [obj for obj in items_in_neighborhood if (isinstance(x, habitatAgent) for x in obj)]
            no_herbivores = [item[0] for item in only_habitat_cells]
            available_youngscrub_cell = [i for i in no_herbivores if i.youngscrub_here < 1000]
            if len(available_youngscrub_cell) > 0:
                new_patch_youngscrub = self.random.choice(available_youngscrub_cell) 
                # and put a young scrub there
                new_patch_youngscrub.youngscrub_here += 1


        # chance of bare ground becoming grassland
        if random.random() < self.model.chance_regrowGrass and self.perc_grass_here < 100:
            self.perc_grass_here += 1
            self.perc_bareground_here -= 1

        # chance of young scrub becoming mature scrub
        if self.youngscrub_here > 0:
            if random.random() < self.model.chance_youngScrubMatures:
                self.scrub_here += 1
                self.youngscrub_here -= 1
            # if a mature scrub is added, chance of grassland being outcompeted
                if self.perc_grass_here > 0 and random.random() < self.model.chance_grassOutcompetedByTreeScrub:
                    self.perc_bareground_here += 1
                    self.perc_grass_here -= 1
                # or of scrub/saplings outcompeted
                if self.saplings_here > 0 and random.random() < self.model.chance_saplingOutcompetedByScrub and self.saplings_here >0:
                    self.saplings_here -= 1
                if self.youngscrub_here > 0 and random.random() < self.model.chance_youngScrubOutcompetedByScrub and self.youngscrub_here >0:
                    self.youngscrub_here -= 1

        # chance of sapling becoming tree
        if self.saplings_here > 0:
            if random.random() < self.model.chance_saplingBecomingTree:
                self.trees_here += 1
                self.saplings_here -= 1
                # if a mature tree is added, chance of grassland and scrubland being outcompeted
                if random.random() < self.model.chance_grassOutcompetedByTreeScrub and self.perc_grass_here > 0:
                    self.perc_bareground_here += 1
                    self.perc_grass_here -= 1
                if random.random() < self.model.chance_scrubOutcompetedByTree and self.scrub_here > 0:
                    self.scrub_here -= 1
                    # or saplings/young scrub
                    if random.random() < self.model.chance_saplingOutcompetedByTree and self.saplings_here > 0:
                        self.saplings_here -= 1
                    if random.random() < self.model.chance_youngScrubOutcompetedByTree and self.youngscrub_here > 0:
                        self.youngscrub_here -= 1

        # reassess dominant condition
        if self.trees_here < 25 and self.scrub_here < 25 and self.perc_grass_here >= 50:
            self.condition = "grassland"
        if self.trees_here < 25 and self.scrub_here < 25 and self.perc_bareground_here >= 50:
            self.condition = "bare_ground"
        if self.trees_here < 25 and self.scrub_here >= 25:
            self.condition = "thorny_scrubland"
        if self.trees_here >= 25:
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

        # Eat what's on my patch
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        # are there saplings here? pick how many to eat, gain energy
        if habitat_patch.saplings_here > 0:
            # count scrub and reduce the number of saplings eaten accordingly
            count_scrub = habitat_patch.scrub_here
            # roll dice between 0 and my maximum number I'll eat
            eatenSaps = random.randint(0,self.model.roeDeer_saplingsEaten)
            # rescale this according to how many shrubs there are 
            eatenSaps_scaled = eatenSaps - int((eatenSaps*(count_scrub/100)))
            habitat_patch.saplings_here -= eatenSaps_scaled
            # don't let number of saplings go negative
            if habitat_patch.saplings_here < 0:
                habitat_patch.saplings_here = 0
            if self.energy < 1:
                self.energy += self.model.roeDeer_gain_from_Saplings
                if self.energy > 1:
                    self.energy = 1

        # are there trees here?
        if habitat_patch.trees_here > 0:
            # roll dice between 0 and my maximum number I'll eat
            eatenTrees = random.randint(0,self.model.roeDeer_treesEaten)
            habitat_patch.trees_here -= eatenTrees
            # don't let it go negative
            if habitat_patch.trees_here < 0:
                habitat_patch.trees_here = 0
            if self.energy < 1:
                self.energy += self.model.roeDeer_gain_from_Trees
                if self.energy > 1:
                    self.energy = 1
        # are there shrubs here? pick how many to eat, gain energy'            
        if habitat_patch.scrub_here > 0:
            # roll dice between 0 and my maximum number I'll eat
            eatenScrub = random.randint(0,self.model.roeDeer_scrubEaten)
            habitat_patch.scrub_here -= eatenScrub
            # don't let it go negative
            if habitat_patch.scrub_here < 0:
                habitat_patch.scrub_here = 0
            if self.energy < 1:
                self.energy += self.model.roeDeer_gain_from_Scrub
                if self.energy > 1:
                    self.energy = 1
        # what about young shrubs?
        if habitat_patch.youngscrub_here > 0:
            # count scrub and reduce the number of young scrubs eaten accordingly
            count_scrub = habitat_patch.scrub_here
            # roll dice between 0 and my maximum number I'll eat, and subtract by percentage of scrub (/ total possible # scrub)
            eatenYoungScrub = random.randint(0,self.model.roeDeer_youngScrubEaten)
            # rescale according to number of scrub plants
            eatenYoungScrub_scaled = eatenYoungScrub - int((eatenYoungScrub*(count_scrub/100)))
            habitat_patch.youngscrub_here -= eatenYoungScrub_scaled
            # don't let it go negative
            if habitat_patch.youngscrub_here < 0:
                habitat_patch.youngscrub_here = 0
            if self.energy < 1:
                self.energy += self.model.roeDeer_gain_from_YoungScrub
                if self.energy > 1:
                    self.energy = 1
        # is there grass?
        if habitat_patch.perc_grass_here > 0:
            # roll dice between 0 and my maximum number I'll eat
            eatenGrass = random.randint(0,self.model.roeDeer_impactGrass)
            habitat_patch.perc_grass_here -= eatenGrass
            habitat_patch.perc_bareground_here += eatenGrass
            # don't let it go negative
            if habitat_patch.perc_grass_here < 0:
                habitat_patch.perc_grass_here = 0
                habitat_patch.perc_bareground_here = 100
            if self.energy < 1:
                self.energy += self.model.roeDeer_gain_from_grass
                if self.energy > 1:
                    self.energy = 1
    
        # if roe deer's energy is less than 0, die 
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        # I can reproduce in May & June (assuming model starts in Jan at beginning of year, May & June = time steps 5&6 out of every 12 months)
        if living and random.random() < self.model.roeDeer_reproduce and (5 <= self.model.schedule.time < 7 or 17 <= self.model.schedule.time < 19 or 29 <= self.model.schedule.time < 31 or 41 <= self.model.schedule.time < 43 or 53 <= self.model.schedule.time < 55 or 65 <= self.model.schedule.time < 67 or 77 <= self.model.schedule.time < 79 or 89 <= self.model.schedule.time < 91 or 101 <= self.model.schedule.time < 103 or 113 <= self.model.schedule.time < 115 or 125 <= self.model.schedule.time < 127 or 137 <= self.model.schedule.time < 139 or 149 <= self.model.schedule.time < 151 or 161 <= self.model.schedule.time < 163 or 173 <= self.model.schedule.time < 175 or 185 <= self.model.schedule.time < 187 or 197 <= self.model.schedule.time < 199 or 209 <= self.model.schedule.time < 211 or 221 <= self.model.schedule.time < 223 or 233 <= self.model.schedule.time < 235 or 245 <= self.model.schedule.time < 247 or 257 <= self.model.schedule.time < 259 or 269 <= self.model.schedule.time < 271 or 281 <= self.model.schedule.time < 283 or 293 <= self.model.schedule.time < 295):
            # Create a new roe deer and divide energy:
            self.energy /= 2
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
        # are there saplings here? pick how many to eat, gain energy
        if habitat_patch.saplings_here > 0:
            # count scrub and reduce the number of saplings eaten accordingly
            count_scrub = habitat_patch.scrub_here
            # roll dice between 0 and my maximum number I'll eat
            eatenSaps = random.randint(0,self.model.ponies_saplingsEaten)
            # rescale this according to how many shrubs there are 
            eatenSaps_scaled = eatenSaps - int((eatenSaps*(count_scrub/100)))
            habitat_patch.saplings_here -= eatenSaps_scaled
            # don't let number of saplings go negative
            if habitat_patch.saplings_here < 0:
                habitat_patch.saplings_here = 0
            if self.energy < 1:
                self.energy += self.model.ponies_gain_from_Saplings
                if self.energy > 1:
                    self.energy = 1
        # are there trees here?
        if habitat_patch.trees_here > 0:
            # roll dice between 0 and my maximum number I'll eat
            eatenTrees = random.randint(0,self.model.ponies_treesEaten)
            habitat_patch.trees_here -= eatenTrees
            # don't let it go negative
            if habitat_patch.trees_here < 0:
                habitat_patch.trees_here = 0
            if self.energy < 1:
                self.energy += self.model.ponies_gain_from_Trees
                if self.energy > 1:
                    self.energy = 1
        # are there shrubs here? pick how many to eat, gain energy           
        if habitat_patch.scrub_here > 0:
                # roll dice between 0 and my maximum number I'll eat
            eatenScrub = random.randint(0,self.model.ponies_scrubEaten)
            habitat_patch.scrub_here -= eatenScrub
            # don't let it go negative
            if habitat_patch.scrub_here < 0:
                habitat_patch.scrub_here = 0
            if self.energy < 1:
                self.energy += self.model.ponies_gain_from_Scrub
                if self.energy > 1:
                    self.energy = 1
        # what about young shrubs?
        if habitat_patch.youngscrub_here > 0:
            # count scrub and reduce the number of young scrubs eaten accordingly
            count_scrub = habitat_patch.scrub_here
            # roll dice between 0 and my maximum number I'll eat, and subtract by percentage of scrub (/ total possible # scrub)
            eatenYoungScrub = random.randint(0,self.model.ponies_youngScrubEaten)
            # rescale according to number of scrub plants
            eatenYoungScrub_scaled = eatenYoungScrub - int((eatenYoungScrub*(count_scrub/100)))
            habitat_patch.youngscrub_here -= eatenYoungScrub_scaled
            # don't let it go negative
            if habitat_patch.youngscrub_here < 0:
                habitat_patch.youngscrub_here = 0
            if self.energy < 1:
                self.energy += self.model.ponies_gain_from_YoungScrub
                if self.energy > 1:
                    self.energy = 1
        # is there grass?
        if habitat_patch.perc_grass_here > 0:
            # roll dice between 0 and my maximum number I'll eat
            eatenGrass = random.randint(0,self.model.ponies_impactGrass)
            habitat_patch.perc_grass_here -= eatenGrass
            habitat_patch.perc_bareground_here += eatenGrass
            # don't let it go negative
            if habitat_patch.perc_grass_here < 0:
                habitat_patch.perc_grass_here = 0
                habitat_patch.perc_bareground_here = 100
            if self.energy < 1:
                self.energy += self.model.ponies_gain_from_grass
                if self.energy > 1:
                    self.energy = 1
        # if pony's energy is less than 0, die 
        if self.energy < 0:
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
        # are there saplings here? pick how many to eat, gain energy
        if habitat_patch.saplings_here > 0:
            # count scrub and reduce the number of saplings eaten accordingly
            count_scrub = habitat_patch.scrub_here
            # roll dice between 0 and my maximum number I'll eat
            eatenSaps = random.randint(0,self.model.cows_saplingsEaten)
            # rescale this according to how many shrubs there are 
            eatenSaps_scaled = eatenSaps - int((eatenSaps*(count_scrub/100)))
            habitat_patch.saplings_here -= eatenSaps_scaled
            # don't let number of saplings go negative
            if habitat_patch.saplings_here < 0:
                habitat_patch.saplings_here = 0
            if self.energy < 1:
                self.energy += self.model.cows_gain_from_Saplings
                if self.energy > 1:
                    self.energy = 1
        # are there trees here?
        if habitat_patch.trees_here > 0:
            # roll dice between 0 and my maximum number I'll eat
            eatenTrees = random.randint(0,self.model.cows_treesEaten)
            habitat_patch.trees_here -= eatenTrees
            # don't let it go negative
            if habitat_patch.trees_here < 0:
                habitat_patch.trees_here = 0
            if self.energy < 1:
                self.energy += self.model.cows_gain_from_Trees
                if self.energy > 1:
                    self.energy = 1
        # are there shrubs here? pick how many to eat, gain energy           
        if habitat_patch.scrub_here > 0:
                # roll dice between 0 and my maximum number I'll eat
            eatenScrub = random.randint(0,self.model.cows_scrubEaten)
            habitat_patch.scrub_here -= eatenScrub
            # don't let it go negative
            if habitat_patch.scrub_here < 0:
                habitat_patch.scrub_here = 0
            if self.energy < 1:
                self.energy += self.model.cows_gain_from_Scrub
                if self.energy > 1:
                    self.energy = 1
        # what about young shrubs?
        if habitat_patch.youngscrub_here > 0:
            # count scrub and reduce the number of young scrubs eaten accordingly
            count_scrub = habitat_patch.scrub_here
            # roll dice between 0 and my maximum number I'll eat, and subtract by percentage of scrub (/ total possible # scrub)
            eatenYoungScrub = random.randint(0,self.model.cows_youngScrubEaten)
            # rescale according to number of scrub plants
            eatenYoungScrub_scaled = eatenYoungScrub - int((eatenYoungScrub*(count_scrub/100)))
            habitat_patch.youngscrub_here -= eatenYoungScrub_scaled
            # don't let it go negative
            if habitat_patch.youngscrub_here < 0:
                habitat_patch.youngscrub_here = 0
            if self.energy < 1:
                self.energy += self.model.cows_gain_from_YoungScrub
                if self.energy > 1:
                    self.energy = 1
        # is there grass?
        if habitat_patch.perc_grass_here > 0:
            # roll dice between 0 and my maximum number I'll eat
            eatenGrass = random.randint(0,self.model.cows_impactGrass)
            habitat_patch.perc_grass_here -= eatenGrass
            habitat_patch.perc_bareground_here += eatenGrass
            # don't let it go negative
            if habitat_patch.perc_grass_here < 0:
                habitat_patch.perc_grass_here = 0
                habitat_patch.perc_bareground_here = 100
            if self.energy < 1:
                self.energy += self.model.cows_gain_from_grass
                if self.energy > 1:
                    self.energy = 1
        # if cow's energy is less than 0, die 
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False
            
        # I reproduce in April, May, and June (assuming model starts in Jan at beginning of year, April, May & June = time steps 4-6 out of every 12 months)
        if living and random.random() < self.model.cows_reproduce and (4 <= self.model.schedule.time < 7 or 16 <= self.model.schedule.time < 19 or 28 <= self.model.schedule.time < 31 or 40 <= self.model.schedule.time < 43 or 52 <= self.model.schedule.time < 55 or 64 <= self.model.schedule.time < 67 or 76 <= self.model.schedule.time < 79 or 88 <= self.model.schedule.time < 91 or 100 <= self.model.schedule.time < 103 or 112 <= self.model.schedule.time < 115 or 124 <= self.model.schedule.time < 127 or 136 <= self.model.schedule.time < 139 or 148 <= self.model.schedule.time < 151 or 160 <= self.model.schedule.time < 163 or 172 <= self.model.schedule.time < 175 or 184 <= self.model.schedule.time < 187 or 196 <= self.model.schedule.time < 199 or 208 <= self.model.schedule.time < 211 or 220 <= self.model.schedule.time < 223 or 232 <= self.model.schedule.time < 235 or 244 <= self.model.schedule.time < 247 or 256 <= self.model.schedule.time < 259 or 268 <= self.model.schedule.time < 271 or 280 <= self.model.schedule.time < 283 or 292 <= self.model.schedule.time < 295):
            # Create a new cow and divide energy:
            self.energy /= 2
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
        # are there saplings here? pick how many to eat, gain energy
        if habitat_patch.saplings_here > 0:
            # count scrub and reduce the number of saplings eaten accordingly
            count_scrub = habitat_patch.scrub_here
            # roll dice between 0 and my maximum number I'll eat
            eatenSaps = random.randint(0,self.model.fallowDeer_saplingsEaten)
            # rescale this according to how many shrubs there are 
            eatenSaps_scaled = eatenSaps - int((eatenSaps*(count_scrub/100)))
            habitat_patch.saplings_here -= eatenSaps_scaled
            # don't let number of saplings go negative
            if habitat_patch.saplings_here < 0:
                habitat_patch.saplings_here = 0
            if self.energy < 1:
                self.energy += self.model.fallowDeer_gain_from_Saplings
                if self.energy > 1:
                    self.energy = 1
        # are there trees here?
        if habitat_patch.trees_here > 0:
            # roll dice between 0 and my maximum number I'll eat
            eatenTrees = random.randint(0,self.model.fallowDeer_treesEaten)
            habitat_patch.trees_here -= eatenTrees
            # don't let it go negative
            if habitat_patch.trees_here < 0:
                habitat_patch.trees_here = 0
            if self.energy < 1:
                self.energy += self.model.fallowDeer_gain_from_Trees
                if self.energy > 1:
                    self.energy = 1
        # are there shrubs here? pick how many to eat, gain energy'            
        if habitat_patch.scrub_here > 0:
                # roll dice between 0 and my maximum number I'll eat
            eatenScrub = random.randint(0,self.model.fallowDeer_scrubEaten)
            habitat_patch.scrub_here -= eatenScrub
            # don't let it go negative
            if habitat_patch.scrub_here < 0:
                habitat_patch.scrub_here = 0
            if self.energy < 1:
                self.energy += self.model.fallowDeer_gain_from_Scrub
                if self.energy > 1:
                    self.energy = 1
        # what about young shrubs?
        if habitat_patch.youngscrub_here > 0:
            # count scrub and reduce the number of young scrubs eaten accordingly
            count_scrub = habitat_patch.scrub_here
            # roll dice between 0 and my maximum number I'll eat, and subtract by percentage of scrub (/ total possible # scrub)
            eatenYoungScrub = random.randint(0,self.model.fallowDeer_youngScrubEaten)
            # rescale according to number of scrub plants
            eatenYoungScrub_scaled = eatenYoungScrub - int((eatenYoungScrub*(count_scrub/100)))
            habitat_patch.youngscrub_here -= eatenYoungScrub_scaled
            # don't let it go negative
            if habitat_patch.youngscrub_here < 0:
                habitat_patch.youngscrub_here = 0
            if self.energy < 1:
                self.energy += self.model.fallowDeer_gain_from_YoungScrub
                if self.energy > 1:
                    self.energy = 1
        # is there grass?
        if habitat_patch.perc_grass_here > 0:
            # roll dice between 0 and my maximum number I'll eat
            eatenGrass = random.randint(0,self.model.fallowDeer_impactGrass)
            habitat_patch.perc_grass_here -= eatenGrass
            habitat_patch.perc_bareground_here += eatenGrass
            # don't let it go negative
            if habitat_patch.perc_grass_here < 0:
                habitat_patch.perc_grass_here = 0
                habitat_patch.perc_bareground_here = 100
            if self.energy < 1:
                self.energy += self.model.fallowDeer_gain_from_grass
                if self.energy > 1:
                    self.energy = 1
    
        # if fallow deer's energy is less than 0, die 
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False
            
        # I reproduce in May & June (assuming model starts in Jan at beginning of year, May & June = time steps 5&6 out of every 12 months)
        if living and random.random() < self.model.fallowDeer_reproduce and (5 <= self.model.schedule.time < 7 or 17 <= self.model.schedule.time < 19 or 29 <= self.model.schedule.time < 31 or 41 <= self.model.schedule.time < 43 or 53 <= self.model.schedule.time < 55 or 65 <= self.model.schedule.time < 67 or 77 <= self.model.schedule.time < 79 or 89 <= self.model.schedule.time < 91 or 101 <= self.model.schedule.time < 103 or 113 <= self.model.schedule.time < 115 or 125 <= self.model.schedule.time < 127 or 137 <= self.model.schedule.time < 139 or 149 <= self.model.schedule.time < 151 or 161 <= self.model.schedule.time < 163 or 173 <= self.model.schedule.time < 175 or 185 <= self.model.schedule.time < 187 or 197 <= self.model.schedule.time < 199 or 209 <= self.model.schedule.time < 211 or 221 <= self.model.schedule.time < 223 or 233 <= self.model.schedule.time < 235 or 245 <= self.model.schedule.time < 247 or 257 <= self.model.schedule.time < 259 or 269 <= self.model.schedule.time < 271 or 281 <= self.model.schedule.time < 283 or 293 <= self.model.schedule.time < 295):
            # Create a new fallow deer and divide energy:
            self.energy /= 2
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
        # are there saplings here? pick how many to eat, gain energy
        if habitat_patch.saplings_here > 0:
            # count scrub and reduce the number of saplings eaten accordingly
            count_scrub = habitat_patch.scrub_here
            # roll dice between 0 and my maximum number I'll eat
            eatenSaps = random.randint(0,self.model.redDeer_saplingsEaten)
            # rescale this according to how many shrubs there are 
            eatenSaps_scaled = eatenSaps - int((eatenSaps*(count_scrub/100)))
            habitat_patch.saplings_here -= eatenSaps_scaled
            # don't let number of saplings go negative
            if habitat_patch.saplings_here < 0:
                habitat_patch.saplings_here = 0
            # gain energy up to  1
            if self.energy < 1:
                self.energy += self.model.redDeer_gain_from_Saplings
                if self.energy > 1:
                    self.energy = 1
        # are there trees here?
        if habitat_patch.trees_here > 0:
            # roll dice between 0 and my maximum number I'll eat
            eatenTrees = random.randint(0,self.model.redDeer_treesEaten)
            habitat_patch.trees_here -= eatenTrees
            # don't let it go negative
            if habitat_patch.trees_here < 0:
                habitat_patch.trees_here = 0
            if self.energy < 1:
                self.energy += self.model.redDeer_gain_from_Trees
                if self.energy > 1:
                    self.energy = 1
                
        # are there shrubs here? pick how many to eat, gain energy'            
        if habitat_patch.scrub_here > 0:
                # roll dice between 0 and my maximum number I'll eat
            eatenScrub = random.randint(0,self.model.redDeer_scrubEaten)
            habitat_patch.scrub_here -= eatenScrub
            # don't let it go negative
            if habitat_patch.scrub_here < 0:
                habitat_patch.scrub_here = 0
            if self.energy < 1:
                self.energy += self.model.redDeer_gain_from_Scrub
                if self.energy > 1:
                    self.energy = 1
        # what about young shrubs?
        if habitat_patch.youngscrub_here > 0:
            # count scrub and reduce the number of young scrubs eaten accordingly
            count_scrub = habitat_patch.scrub_here
            # roll dice between 0 and my maximum number I'll eat, and subtract by percentage of scrub (/ total possible # scrub)
            eatenYoungScrub = random.randint(0,self.model.redDeer_youngScrubEaten)
            # rescale according to number of scrub plants
            eatenYoungScrub_scaled = eatenYoungScrub - int((eatenYoungScrub*(count_scrub/100)))
            habitat_patch.youngscrub_here -= eatenYoungScrub_scaled
            # don't let it go negative
            if habitat_patch.youngscrub_here < 0:
                habitat_patch.youngscrub_here = 0
            if self.energy < 1:
                self.energy += self.model.redDeer_gain_from_YoungScrub
                if self.energy > 1:
                    self.energy = 1
        # is there grass?
        if habitat_patch.perc_grass_here > 0:
            # roll dice between 0 and my maximum number I'll eat
            eatenGrass = random.randint(0,self.model.redDeer_impactGrass)
            habitat_patch.perc_grass_here -= eatenGrass
            habitat_patch.perc_bareground_here += eatenGrass
            # don't let it go negative
            if habitat_patch.perc_grass_here < 0:
                habitat_patch.perc_grass_here = 0
                habitat_patch.perc_bareground_here = 100
            if self.energy < 1:
                self.energy += self.model.redDeer_gain_from_grass
                if self.energy > 1:
                    self.energy = 1

        # if red deer's energy is less than 0, die 
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False
        # I reproduce in May & June (assuming model starts in Jan at beginning of year, May & June = time steps 5&6 out of every 12 months)
        if living and random.random() < self.model.redDeer_reproduce and (5 <= self.model.schedule.time < 7 or 17 <= self.model.schedule.time < 19 or 29 <= self.model.schedule.time < 31 or 41 <= self.model.schedule.time < 43 or 53 <= self.model.schedule.time < 55 or 65 <= self.model.schedule.time < 67 or 77 <= self.model.schedule.time < 79 or 89 <= self.model.schedule.time < 91 or 101 <= self.model.schedule.time < 103 or 113 <= self.model.schedule.time < 115 or 125 <= self.model.schedule.time < 127 or 137 <= self.model.schedule.time < 139 or 149 <= self.model.schedule.time < 151 or 161 <= self.model.schedule.time < 163 or 173 <= self.model.schedule.time < 175 or 185 <= self.model.schedule.time < 187 or 197 <= self.model.schedule.time < 199 or 209 <= self.model.schedule.time < 211 or 221 <= self.model.schedule.time < 223 or 233 <= self.model.schedule.time < 235 or 245 <= self.model.schedule.time < 247 or 257 <= self.model.schedule.time < 259 or 269 <= self.model.schedule.time < 271 or 281 <= self.model.schedule.time < 283 or 293 <= self.model.schedule.time < 295):
            # Create a new roe deer and divide energy:
            self.energy /= 2
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
        # are there saplings here? pick how many to eat, gain energy
        if habitat_patch.saplings_here > 0:
            # count scrub and reduce the number of saplings eaten accordingly
            count_scrub = habitat_patch.scrub_here
            # roll dice between 0 and my maximum number I'll eat
            eatenSaps = random.randint(0,self.model.pigs_saplingsEaten)
            # rescale this according to how many shrubs there are 
            eatenSaps_scaled = eatenSaps - int((eatenSaps*(count_scrub/100)))
            habitat_patch.saplings_here -= eatenSaps_scaled
            # don't let number of saplings go negative
            if habitat_patch.saplings_here < 0:
                habitat_patch.saplings_here = 0
            if self.energy < 1:
                self.energy += self.model.pigs_gain_from_Saplings
                if self.energy > 1:
                    self.energy = 1
        # what about young shrubs?
        if habitat_patch.youngscrub_here > 0:
            self.energy += self.model.pigs_gain_from_YoungScrub
            # count scrub and reduce the number of young scrubs eaten accordingly
            count_scrub = habitat_patch.scrub_here
            # roll dice between 0 and my maximum number I'll eat, and subtract by percentage of scrub (/ total possible # scrub)
            eatenYoungScrub = random.randint(0,self.model.pigs_youngScrubEaten)
            # rescale according to number of scrub plants
            eatenYoungScrub_scaled = eatenYoungScrub - int((eatenYoungScrub*(count_scrub/100)))
            habitat_patch.youngscrub_here -= eatenYoungScrub_scaled
            # don't let it go negative
            if habitat_patch.youngscrub_here < 0:
                habitat_patch.youngscrub_here = 0
            if self.energy < 1:
                self.energy += self.model.pigs_gain_from_YoungScrub
                if self.energy > 1:
                    self.energy = 1
        # is there grass?
        if habitat_patch.perc_grass_here > 0:
            self.energy += self.model.pigs_gain_from_grass
            # roll dice between 0 and my maximum number I'll eat
            eatenGrass = random.randint(0,self.model.pigs_impactGrass)
            habitat_patch.perc_grass_here -= eatenGrass
            habitat_patch.perc_bareground_here += eatenGrass
            # don't let it go negative
            if habitat_patch.perc_grass_here < 0:
                habitat_patch.perc_grass_here = 0
                habitat_patch.perc_bareground_here = 100
            if self.energy < 1:
                self.energy += self.model.pigs_gain_from_grass
                if self.energy > 1:
                    self.energy = 1
    
        # if pig's energy is less than 0, die 
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False
            
        # pigs reproduce Jan - July (1 - 7, < 8)
        if living and random.random() < self.model.pigs_reproduce and (1 <= self.model.schedule.time < 8 or 13 <= self.model.schedule.time < 20 or 25 <= self.model.schedule.time < 32 or 37 <= self.model.schedule.time < 44 or 49 <= self.model.schedule.time < 56 or 61 <= self.model.schedule.time < 68 or 73 <= self.model.schedule.time < 80 or 85 <= self.model.schedule.time < 92 or 97 <= self.model.schedule.time < 104 or 109 <= self.model.schedule.time < 116 or 121 <= self.model.schedule.time < 128 or 133 <= self.model.schedule.time < 140 or 145 <= self.model.schedule.time < 152 or 157 <= self.model.schedule.time < 164 or 169 <= self.model.schedule.time < 176 or 181 <= self.model.schedule.time < 188 or 193 <= self.model.schedule.time < 200 or 205 <= self.model.schedule.time < 212 or 217 <= self.model.schedule.time < 224 or 229 <= self.model.schedule.time < 236 or 241 <= self.model.schedule.time < 248 or 253 <= self.model.schedule.time < 260 or 265 <= self.model.schedule.time < 272 or 277 <= self.model.schedule.time < 284 or 289 <= self.model.schedule.time < 296):
            # Pick a number of piglets to have
            for _ in range(random.randint(1,10)):
            # Create a new piglet and divide energy:
                self.energy /= 2
                piglet = tamworthPigs(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
                self.model.grid.place_agent(piglet, self.pos)
                self.model.schedule.add(piglet)










                                # # # # ------ Define the model ------ # # # # 

class KneppModel(Model):
    
    
    def __init__(self,             
            chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
            chance_scrubOutcompetedByTree, chance_grassOutcompetedByTreeScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
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
        self.chance_grassOutcompetedByTreeScrub = chance_grassOutcompetedByTreeScrub
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

    def step(self):
        self.schedule.step()
        # count how many there are, then step
        self.datacollector.collect(self)


    def count_condition(self, model, habitat_condition):
        # want to count grass, wood, scrub, bare ground in each patch
        count = 0
        for key, value in model.schedule.agents_by_breed[habitatAgent].items():
            if value.condition == habitat_condition:
                count += 1
        # return percentage of entire area
        return int((count/1800)*100)


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


    def run_model(self):

        # run pre-reintroduction model: Jan 2005 - March 2009 (50 months)
        for i in range(50):
            self.step()
        # filter these runs; only keep running it if they pass these criteria
        results_preReintro = self.datacollector.get_model_vars_dataframe()

        if ((results_preReintro["Time"] == 50) & (results_preReintro["Roe deer"] <= 40) & (results_preReintro["Roe deer"] >= 12) & (results_preReintro["Grassland"] <= 90) & (results_preReintro["Grassland"] >= 49) & (results_preReintro["Woodland"] <= 27) & (results_preReintro["Woodland"] >= 7) & (results_preReintro["Thorny Scrub"] <= 21) & (results_preReintro["Thorny Scrub"] >= 1)).any():
            # 2009: post-reintro model; add the reintroduced species
            print("made it past 2009")
            # add 23 ponies 
            self.add_herbivores(exmoorPony, 23)
            # add 53 cows 
            self.add_herbivores(longhornCattle, 53)
            # add 20 pigs 
            self.add_herbivores(tamworthPigs, 20)
            for i in range(12):
                self.step()

            # # # # # 2010: add or subtract as many as is needed to get to these values # # # #
            results_2 = self.datacollector.get_model_vars_dataframe()
            # with pd.option_context('display.max_columns',None, 'display.max_rows',None):
            #     print(results_2)
            # Exmoor ponies: 13
            exmoorValue = results_2.iloc[62]['Exmoor pony']
            if exmoorValue >= 13: # randomly choose that many exmoor ponies and delete them
                number_to_subtract = -13 + exmoorValue
                self.remove_herbivores(exmoorPony, number_to_subtract)
            else: # add them
                number_to_add = 13 - exmoorValue
                self.add_herbivores(exmoorPony, number_to_add)
            # Longhorn cattle: 77
            cowValue = results_2.iloc[62]['Longhorn cattle']
            if cowValue >= 77:
                number_to_subtract = -77 + cowValue
                self.remove_herbivores(longhornCattle, number_to_subtract)
            else:
                number_to_add = 77 - cowValue
                self.add_herbivores(longhornCattle, number_to_add)
            # Fallow deer: 42
            fallowValue = results_2.iloc[62]['Fallow deer']
            if fallowValue >= 42:
                number_to_subtract = -42 + fallowValue
                self.remove_herbivores(fallowDeer, number_to_subtract)
            else:
                number_to_add = 42 - fallowValue
                self.add_herbivores(fallowDeer, number_to_add)
            # Pigs: 17
            pigsValue = results_2.iloc[62]['Tamworth pigs']
            if pigsValue >= 17:
                number_to_subtract = -17 + pigsValue
                self.remove_herbivores(tamworthPigs, number_to_subtract)
            else:
                number_to_add = 17 - pigsValue
                self.add_herbivores(tamworthPigs, number_to_add)
            for i in range(12):
                self.step()

                                            # # # # # 2011 # # # # #

            results_3 = self.datacollector.get_model_vars_dataframe()
            # Exmoor ponies: 15
            exmoorValue = results_3.iloc[74]['Exmoor pony']
            if exmoorValue >= 15:
                number_to_subtract = -15 + exmoorValue
                self.remove_herbivores(exmoorPony, number_to_subtract)
            else:
                number_to_add = 15 - exmoorValue
                self.add_herbivores(exmoorPony, number_to_add)
            # Longhorn cattle: 92
            cowValue = results_3.iloc[74]['Longhorn cattle']
            if cowValue >= 92:
                number_to_subtract = -92 + cowValue
                self.remove_herbivores(longhornCattle, number_to_subtract)
            else:
                number_to_add = 92 - cowValue
                self.add_herbivores(longhornCattle, number_to_add)
            # Fallow deer: 81
            fallowValue = results_3.iloc[74]['Fallow deer']
            if fallowValue >= 81:
                number_to_subtract = -81 + fallowValue
                self.remove_herbivores(fallowDeer, number_to_subtract)
            else:
                number_to_add = 81 - fallowValue
                self.add_herbivores(fallowDeer, number_to_add)
            # Pigs: 22
            pigsValue = results_3.iloc[74]['Tamworth pigs']
            if pigsValue >= 22:
                number_to_subtract = -22 + pigsValue
                self.remove_herbivores(tamworthPigs, number_to_subtract)
            else:
                number_to_add = 22 - pigsValue
                self.add_herbivores(tamworthPigs, number_to_add)
            for i in range(12):
                self.step()

                                        # # # # # 2012 # # # # #

            results_4 = self.datacollector.get_model_vars_dataframe()
            # Exmoor ponies: 17
            exmoorValue = results_4.iloc[86]['Exmoor pony']
            if exmoorValue >= 17:
                number_to_subtract = -17 + exmoorValue
                self.remove_herbivores(exmoorPony, number_to_subtract)
            else:
                number_to_add = 17 - exmoorValue
                self.add_herbivores(exmoorPony, number_to_add)
            # Longhorn cattle: 116
            cowValue = results_4.iloc[86]['Longhorn cattle']
            if cowValue >= 116:
                number_to_subtract = -116 + cowValue
                self.remove_herbivores(longhornCattle, number_to_subtract)
            else:
                number_to_add = 116 - cowValue
                self.add_herbivores(longhornCattle, number_to_add)
            # Fallow deer: 100
            fallowValue = results_4.iloc[86]['Fallow deer']
            if fallowValue >= 100:
                number_to_subtract = -100 + fallowValue
                self.remove_herbivores(fallowDeer, number_to_subtract)
            else:
                number_to_add = 100 - fallowValue
                self.add_herbivores(fallowDeer, number_to_add)
            # Pigs: 22
            pigsValue = results_4.iloc[86]['Tamworth pigs']
            if pigsValue >= 33:
                number_to_subtract = -33 + pigsValue
                self.remove_herbivores(tamworthPigs, number_to_subtract)
            else:
                number_to_add = 33 - pigsValue
                self.add_herbivores(tamworthPigs, number_to_add)
            for i in range(12):
                self.step()

                                                    # # # # # 2013 # # # # #

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
            for i in range(12):
                self.step()



                                            # # # # # 2014 # # # # #

            results_6 = self.datacollector.get_model_vars_dataframe()
            # Exmoor ponies: 10
            exmoorValue = results_6.iloc[110]['Exmoor pony']
            if exmoorValue >= 10:
                number_to_subtract = -10 + exmoorValue
                self.remove_herbivores(exmoorPony, number_to_subtract)
            else:
                number_to_add = 10 - exmoorValue
                self.add_herbivores(exmoorPony, number_to_add)
            # Longhorn cattle: 264
            cowValue = results_6.iloc[110]['Longhorn cattle']
            if cowValue >= 264:
                number_to_subtract = -264 + cowValue
                self.remove_herbivores(longhornCattle, number_to_subtract)
            else:
                number_to_add = 264 - cowValue
                self.add_herbivores(longhornCattle, number_to_add)
            # Fallow deer: 100
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
            # Red deer: 13
            redDeerValue = results_6.iloc[110]['Red deer']
            if redDeerValue >= 13:
                number_to_subtract = -13 + redDeerValue
                self.remove_herbivores(redDeer, number_to_subtract)
            else:
                number_to_add = 13 - redDeerValue
                self.add_herbivores(redDeer, number_to_add)
            for i in range(12):
                self.step()




                        # # # # March 2015 # # # #

            results_7 = self.datacollector.get_model_vars_dataframe()
            # Exmoor ponies: 10
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
            self.step()

         # April 2015: one pig culled, 5 born
            print("made it to April 2015")
            self.remove_herbivores(tamworthPigs, 1)
            # add filtering condition: cows & pigs born
            results_April2015 = self.datacollector.get_model_vars_dataframe()
            # with pd.option_context('display.max_columns',None, 'display.max_rows',None):
            #     print(results_April2015)
            if ((results_April2015["Time"] == 123) & (results_April2015["Longhorn cattle"] <= 127) & (results_April2015["Longhorn cattle"] >= 104) & (results_April2015["Tamworth pigs"] <= 24) & (results_April2015["Tamworth pigs"] >= 20)).any():
                self.step()
                print("made it to May 2015")
                # May 2015: 8 pigs culled
                self.remove_herbivores(tamworthPigs, 8)
                # add filtering condition: cows born
                results_May2015 = self.datacollector.get_model_vars_dataframe()
                if ((results_May2015["Time"] == 124) & (results_May2015["Longhorn cattle"] <= 142) & (results_May2015["Longhorn cattle"] >= 116)).any():
                    self.step()
                    print("made it to June 2015")
                    # June & July 2015: 5 cows culled
                    self.remove_herbivores(longhornCattle, 5)
                    # add filtering condition: cows born
                    results_June2015 = self.datacollector.get_model_vars_dataframe()
                    if ((results_June2015["Time"] == 125) & (results_June2015["Longhorn cattle"] <= 142) & (results_June2015["Longhorn cattle"] >= 116)).any():
                        for i in range (2):
                            self.step()
                        # August 2015: cull 2 fallow deer
                        self.remove_herbivores(fallowDeer, 2)
                        self.step()
                        # September 2015: 2 male fallow deer culled; 2 cattle culled and 3 bulls added
                        self.remove_herbivores(fallowDeer, 2)
                        self.remove_herbivores(longhornCattle, 1)
                        self.step()
                        # Oct 2015: 2 female and 1 male fallow deer culled; 38 female cows and 1 bull removed
                        self.remove_herbivores(fallowDeer, 3)
                        self.remove_herbivores(longhornCattle, 39)
                        self.step()
                        # Nov 2015: -7 fallow deer
                        self.remove_herbivores(fallowDeer, 7)       
                        self.step()
                        # Dec 2015: 6 fallow deer culled; 5 cows removed;
                        self.remove_herbivores(fallowDeer, 6)
                        self.remove_herbivores(longhornCattle, 5)
                        self.step()
                        # Jan 2016: 7 fallow deer culled; 4 pigs culled and 1 added
                        self.remove_herbivores(fallowDeer, 7) 
                        self.remove_herbivores(tamworthPigs, 3)
                        self.step()
                        # Feb 2016: 10 fallow deer culled; 2 pigs culled
                        self.remove_herbivores(fallowDeer, 10)
                        self.remove_herbivores(tamworthPigs, 2)
                        results_Feb2016 = self.datacollector.get_model_vars_dataframe()
                        if ((results_Feb2016["Time"] == 133) & (results_Feb2016["Exmoor pony"] == 10)).any():
                            self.step()
                            

                                       # # # # # # # 2016 # # # # # # #

                            print("made it to 2016")
                            # March 2016: 1 pony added; 3 pigs added and 4 culled
                            self.add_herbivores(exmoorPony, 1)
                            # minus 1 pig
                            self.remove_herbivores(tamworthPigs, 1)
                            # filtering conditions: fallow deer, pigs, and red deer
                            results_March2016 = self.datacollector.get_model_vars_dataframe()
                            if ((results_March2016["Time"] == 134) & (results_March2016["Fallow deer"] <= 154) & (results_March2016["Fallow deer"] >= 126) & (results_March2016["Red deer"] >= 23) & (results_March2016["Red deer"] <= 29) & (results_March2016["Tamworth pig"] <= 10) & (results_March2016["Tamworth pig"] >= 8)).any():
                                self.step()
                                # April 2016: 1 cow added & filtering for cows
                                self.add_herbivores(longhornCattle, 1)
                                # filter the cow births
                                results_April2016 = self.datacollector.get_model_vars_dataframe()
                                if ((results_April2016["Time"] == 135) & (results_April2016["Longhorn cattle"] <= 113) & (results_April2016["Longhorn cattle"] >= 93)).any():
                                    self.step()
                                    # May 2016: filtering for cows and pigs, and 2 cows culled
                                    self.remove_herbivores(longhornCattle, 2)
                                    results_May2016 = self.datacollector.get_model_vars_dataframe()
                                    if ((results_May2016["Time"] == 136) & (results_May2016["Longhorn cattle"] <= 119) & (results_May2016["Longhorn cattle"] >= 97) & (results_May2016["Tamworth pigs"] <= 19) & (results_May2016["Tamworth pigs"] >= 15)).any():
                                        self.step()
                                        # June 2016: filtering for cows, 30 cows culled and 4 added 
                                        self.remove_herbivores(longhornCattle, 26)
                                        results_June2016 = self.datacollector.get_model_vars_dataframe()
                                        if ((results_June2016["Time"] == 137) & (results_June2016["Longhorn cattle"] <= 98) & (results_June2016["Longhorn cattle"] >= 80)).any():
                                            self.step()
                                            # July 2016: 2 cows culled
                                            self.remove_herbivores(longhornCattle, 2)
                                            self.step()
                                            # August 2016: -5 fallow deer
                                            self.remove_herbivores(fallowDeer, 5)
                                            self.step()
                                            # September & Oct 2016: -9, +19 cows
                                            self.remove_herbivores(longhornCattle, 10)
                                            for i in range(2):
                                                self.step()
                                            # November 2016: -3 fallow deer; -5 cows
                                            self.remove_herbivores(fallowDeer, 3)
                                            self.remove_herbivores(longhornCattle, 5)
                                            self.step()
                                            # December 2016: -9 fallow; -13 cows; -4 pigs
                                            self.remove_herbivores(fallowDeer, 9)
                                            self.remove_herbivores(longhornCattle, 13)
                                            self.remove_herbivores(tamworthPigs, 4)
                                            self.step()
                                            # January 2017: -4 pigs, +1 pig
                                            self.remove_herbivores(tamworthPigs, 3)
                                            self.step()
                                            # February 2017: -8 fallow deer; -3 pigs; filtering for ponies
                                            self.remove_herbivores(fallowDeer, 8)
                                            self.remove_herbivores(tamworthPigs, 3)
                                            results_Feb2017 = self.datacollector.get_model_vars_dataframe()
                                            if ((results_Feb2017["Time"] == 145) & (results_Feb2017["Exmoor pony"] == 11)).any():
                                                self.step()



                                                    # # # # # # # 2017 # # # # # # #
                                                print("made it to 2017")
                                                # minus 1 exmoor pony, -12 red deer; filtering for cows
                                                self.remove_herbivores(exmoorPony, 1)
                                                self.remove_herbivores(redDeer, 12)
                                                results_March2017 = self.datacollector.get_model_vars_dataframe()
                                                if ((results_March2017["Time"] == 146) & (results_March2017["Fallow deer"] <= 182) & (results_March2017["Fallow deer"] >= 149)).any():
                                                    self.step()
                                                    # April 2017: -3 cows, filtering for cows and pigs
                                                    self.remove_herbivores(longhornCattle, 3)
                                                    results_April2017 = self.datacollector.get_model_vars_dataframe()
                                                    if ((results_April2017["Time"] == 147) & (results_April2017["Longhorn cattle"] <= 110) & (results_April2017["Longhorn cattle"] >= 90) & (results_April2017["Tamworth pigs"] <= 24) & (results_April2017["Tamworth pigs"] >= 20)).any():
                                                        self.step()
                                                        # May 2017: filtering condition for cows
                                                        results_May2017 = self.datacollector.get_model_vars_dataframe()
                                                        if ((results_May2017["Time"] == 148) & (results_May2017["Longhorn cattle"] <= 120) & (results_May2017["Longhorn cattle"] >= 98)).any():
                                                            self.step()
                                                            # June & July 2017: -24 cows, +3 cows, and cow filtering condition
                                                            self.remove_herbivores(longhornCattle, 21)
                                                            results_June2017 = self.datacollector.get_model_vars_dataframe()
                                                            if ((results_June2017["Time"] == 149) & (results_June2017["Longhorn cattle"] <= 103) & (results_June2017["Longhorn cattle"] >= 85)).any():
                                                                for i in range(2):
                                                                    self.step()
                                                                # August 2017: -16 fallow deer 
                                                                self.remove_herbivores(fallowDeer, 16)
                                                                self.step()
                                                                # September 2017: -5 fallow deer; -27, +23 cows
                                                                self.remove_herbivores(fallowDeer, 5)
                                                                self.remove_herbivores(longhornCattle, 4)
                                                                self.step()
                                                                # October 2017: -4 fallow deer; -2 cows
                                                                self.remove_herbivores(fallowDeer, 4)
                                                                self.remove_herbivores(longhornCattle, 2)
                                                                self.step()
                                                                # November 2017: -2 fallow deer
                                                                self.remove_herbivores(fallowDeer, 2)
                                                                self.step()
                                                                # December 2017: -46 fallow deer, -1 red deer; -4 pigs
                                                                self.remove_herbivores(fallowDeer, 46)
                                                                self.remove_herbivores(redDeer, 1)
                                                                self.remove_herbivores(tamworthPigs, 4)
                                                                self.step()
                                                                # January 2018: -9 pigs, +1 pig, and pig filtering conditions
                                                                self.remove_herbivores(tamworthPigs, 8)
                                                                results_June2017 = self.datacollector.get_model_vars_dataframe()
                                                                if ((results_June2017["Time"] == 156) & (results_June2017["Tamworth pigs"] <= 13) & (results_June2017["Tamworth pigs"] >= 11)).any():
                                                                    self.step()
                                                                    # February 2018: -14 fallow; -1 red deer; -1 pig; filtering for pig and exmoor
                                                                    self.remove_herbivores(fallowDeer, 14)
                                                                    self.remove_herbivores(redDeer, 1)
                                                                    self.remove_herbivores(tamworthPigs, 1)
                                                                    results_Feb2018 = self.datacollector.get_model_vars_dataframe()
                                                                    if ((results_Feb2018["Time"] == 157) & (results_Feb2018["Exmoor pony"] == 10) & (results_Feb2018["Tamworth pigs"] <= 18) & (results_Feb2018["Tamworth pigs"] >= 14)).any():
                                                                        self.step()

                                                # # # # # # # 2018 # # # # # # #

                                                                        # March 2018: -1 Exmoor; filtering for red and fallow deer
                                                                        print("made it to 2018")
                                                                        self.remove_herbivores(exmoorPony, 1)
                                                                        results_March2018 = self.datacollector.get_model_vars_dataframe()
                                                                        if ((results_March2018["Time"] == 158) & (results_March2018["Fallow deer"] <= 276) & (results_March2018["Fallow deer"] >= 226) & (results_March2018["Red deer"] <= 26) & (results_March2018["Red deer"] >= 22)).any():
                                                                            self.step()
                                                                            # April 2018: +1 cow and filtering for cow
                                                                            self.add_herbivores(longhornCattle, 1)
                                                                            results_April2018 = self.datacollector.get_model_vars_dataframe()
                                                                            if ((results_April2018["Time"] == 159) & (results_April2018["Longhorn cattle"] <= 111) & (results_April2018["Longhorn cattle"] >= 91)).any():
                                                                                self.step()
                                                                                # May 2018: filtering for cows and pigs
                                                                                results_May2018 = self.datacollector.get_model_vars_dataframe()
                                                                                if ((results_May2018["Time"] == 160) & (results_May2018["Longhorn cattle"] <= 129) & (results_May2018["Longhorn cattle"] >= 105) & (results_May2018["Tamworth pigs"] <= 25) & (results_May2018["Tamworth pigs"] >= 21)).any():
                                                                                    self.step()
                                                                                    # June 2018: -22 cows, +2 cows; filtering for cows
                                                                                    self.remove_herbivores(longhornCattle, 20)
                                                                                    results_June2018 = self.datacollector.get_model_vars_dataframe()
                                                                                    if ((results_June2018["Time"] == 161) & (results_June2018["Longhorn cattle"] <= 113) & (results_June2018["Longhorn cattle"] >= 93)).any():
                                                                                        self.step()
                                                                                        # July 2018: -1 red deer; -1 pig
                                                                                        self.remove_herbivores(redDeer, 1)
                                                                                        self.remove_herbivores(tamworthPigs, 1)
                                                                                        self.step()
                                                                                        # August 2018: -9 ponies; -15 fallow deer; -1 cattle; -1 pig
                                                                                        self.remove_herbivores(exmoorPony, 9)
                                                                                        self.remove_herbivores(fallowDeer, 15)
                                                                                        self.remove_herbivores(tamworthPigs, 1)
                                                                                        self.remove_herbivores(longhornCattle, 1)
                                                                                        self.step()
                                                                                        # September 2018: -19 fallow; -16 and +20 cows
                                                                                        self.remove_herbivores(fallowDeer, 19)
                                                                                        self.add_herbivores(longhornCattle, 4)
                                                                                        self.step()
                                                                                        # October 2018: -4 cows; -4 fallow; -1 pig
                                                                                        self.remove_herbivores(longhornCattle, 4)
                                                                                        self.remove_herbivores(fallowDeer, 4)
                                                                                        self.remove_herbivores(tamworthPigs, 1)
                                                                                        self.step()
                                                                                        # November 2018: -8 cows; -12 pigs
                                                                                        self.remove_herbivores(longhornCattle, 8)
                                                                                        self.remove_herbivores(tamworthPigs, 12)
                                                                                        self.step()
                                                                                        # December & January 2018/2019: -19 fallow; -5 and +1 cow; -1 red deer 
                                                                                        self.remove_herbivores(longhornCattle, 4)
                                                                                        self.remove_herbivores(fallowDeer, 19)
                                                                                        self.remove_herbivores(redDeer, 1)
                                                                                        for i in range(2):
                                                                                            self.step()
                                                                                        # February 2019: +1 pig, -2 cows
                                                                                        self.remove_herbivores(longhornCattle, 2)
                                                                                        self.add_herbivores(tamworthPigs, 1)                                                                       
                                                                                        self.step()
                    

                                                    # # # # # # # 2019 # # # # # # #


                                                                                        # March 2019: -1 pig; fallow and red deer filters
                                                                                        print("made it to 2019")
                                                                                        self.remove_herbivores(tamworthPigs, 1)
                                                                                        results_March2019 = self.datacollector.get_model_vars_dataframe()
                                                                                        if ((results_March2019["Time"] == 169) & (results_March2019["Fallow deer"] <= 306) & (results_March2019["Fallow deer"] >= 250) & (results_March2019["Red deer"] <= 41) & (results_March2019["Red deer"] >= 33)).any():
                                                                                            self.step()
                                                                                            # April 2019: filtering for cows 
                                                                                            results_April2019 = self.datacollector.get_model_vars_dataframe()
                                                                                            if ((results_April2019["Time"] == 170) & (results_April2019["Longhorn cattle"] <= 111) & (results_April2019["Longhorn cattle"] >= 91)).any():
                                                                                                self.step()
                                                                                                # May 2019: filtering for cows 
                                                                                                results_May2019 = self.datacollector.get_model_vars_dataframe()
                                                                                                if ((results_May2019["Time"] == 171) & (results_May2019["Longhorn cattle"] <= 121) & (results_May2019["Longhorn cattle"] >= 99)).any():
                                                                                                    self.step()
                                                                                                    # June 2019: -28 cows and cow filtering condition
                                                                                                    self.remove_herbivores(longhornCattle, 28)
                                                                                                    results_June2019 = self.datacollector.get_model_vars_dataframe()
                                                                                                    if ((results_June2019["Time"] == 172) & (results_June2019["Longhorn cattle"] <= 98) & (results_June2019["Longhorn cattle"] >= 80)).any():
                                                                                                        self.step()
                                                                                                        # July & Aug 2019: -3, +5 cows; -26 pigs; filtering for pigs
                                                                                                        self.remove_herbivores(tamworthPigs, 26)
                                                                                                        self.add_herbivores(longhornCattle, 2)
                                                                                                        results_July2019 = self.datacollector.get_model_vars_dataframe()
                                                                                                        if ((results_July2019["Time"] == 173) & (results_July2019["Tamworth pigs"] <= 10) & (results_July2019["Tamworth pigs"] >= 8)).any():
                                                                                                            for i in range(2):
                                                                                                                self.step()
                                                                                                            # Sept 2019: -15 fallow; -23 and +25 cows
                                                                                                            self.remove_herbivores(fallowDeer, 15)
                                                                                                            self.add_herbivores(longhornCattle, 2)
                                                                                                            self.step()
                                                                                                            # Oct 2019: -5 cows
                                                                                                            self.remove_herbivores(longhornCattle, 5)
                                                                                                            self.step()
                                                                                                            # November 2019: -7 fallow deer; -1 cows; -3 red deer
                                                                                                            self.remove_herbivores(longhornCattle, 1)
                                                                                                            self.remove_herbivores(fallowDeer, 7)
                                                                                                            self.remove_herbivores(redDeer, 3)
                                                                                                            self.step()
                                                                                                            # December 2019: -12 fallow; -7 cows; -4 red; +1 pigs
                                                                                                            self.remove_herbivores(fallowDeer, 12)
                                                                                                            self.remove_herbivores(longhornCattle, 7)
                                                                                                            self.remove_herbivores(redDeer, 4)
                                                                                                            self.add_herbivores(tamworthPigs, 1)
                                                                                                            self.step()
                                                                                                            # January 2020: -24 fallow deer
                                                                                                            self.remove_herbivores(fallowDeer, 24)
                                                                                                            self.step()
                                                                                                            # February 2020: -12 fallow; -1 cow; -2 red; -2 pigs
                                                                                                            self.remove_herbivores(fallowDeer, 12)
                                                                                                            self.remove_herbivores(redDeer, 2)
                                                                                                            self.remove_herbivores(tamworthPigs, 2)
                                                                                                            self.remove_herbivores(longhornCattle, 1)                               
                                                                                                            self.step()
                                                                                                            
                                                                                                                
            #                                     # # # # # 2020 # # # # # #
                                                                                                            # March & April 2020: +15 exmoor; -1 and +3 cows; -1 pig; filtering for red and fallow deer
                                                                                                            print("made it to 2020")
                                                                                                            self.add_herbivores(exmoorPony, 15)
                                                                                                            self.add_herbivores(longhornCattle, 2)
                                                                                                            self.remove_herbivores(tamworthPigs, 1)
                                                                                                            results_March2020 = self.datacollector.get_model_vars_dataframe()
                                                                                                            if ((results_March2020["Time"] == 183) & (results_March2020["Fallow deer"] <= 272) & (results_March2020["Fallow deer"] >= 222) & (results_March2020["Red deer"] <= 39) & (results_March2020["Red deer"] >= 32)).any():
                                                                                                                for i in range(2):
                                                                                                                    self.step()
                                                                                                                # May 2020: filtering for pigs and ponies
                                                                                                                results_May2020 = self.datacollector.get_model_vars_dataframe()
                                                                                                                if ((results_May2020["Time"] == 184) & (results_May2020["Exmoor pony"] == 15) & (results_May2020["Tamworth pigs"] <= 21) & (results_May2020["Tamworth pigs"] >= 17)).any():
                                                                                                                    self.step()

                                                                                                        

                                                    # # # # Run the model # # # # 


def run_model():
    # define number of simulations
    number_simulations = 1000
    # make list of variables
    final_results_list = []
    final_parameters = []
    run_number = 0


    for _ in range(number_simulations):
        # choose my parameters 
        initial_roeDeer = random.randint(6, 18)
        initial_grassland = random.randint(70, 90)
        initial_woodland = random.randint(4, 24)
        initial_scrubland = random.randint(0, 11)
        # habitats
        chance_reproduceSapling = np.random.uniform(0,1)
        chance_reproduceYoungScrub = np.random.uniform(0,1)
        chance_regrowGrass = np.random.uniform(0,1)
        chance_saplingBecomingTree = np.random.uniform(0,1)
        chance_youngScrubMatures = np.random.uniform(0,1)
        chance_scrubOutcompetedByTree = np.random.uniform(0,1) 
        chance_grassOutcompetedByTreeScrub = np.random.uniform(0,1)
        chance_saplingOutcompetedByTree = np.random.uniform(0,1)
        chance_saplingOutcompetedByScrub = np.random.uniform(0,1)
        chance_youngScrubOutcompetedByScrub = np.random.uniform(0,1)
        chance_youngScrubOutcompetedByTree = np.random.uniform(0,1)
        # roe deer
        roeDeer_reproduce = np.random.uniform(0,1)
        roeDeer_gain_from_grass = np.random.uniform(0,1)
        roeDeer_gain_from_Trees = np.random.uniform(0,1)
        roeDeer_gain_from_Scrub = np.random.uniform(0,1)
        roeDeer_gain_from_Saplings = np.random.uniform(0,1)
        roeDeer_gain_from_YoungScrub = np.random.uniform(0,1)
        roeDeer_impactGrass = random.randint(0,100)
        roeDeer_saplingsEaten = random.randint(0,1000)
        roeDeer_youngScrubEaten = random.randint(0,1000)
        roeDeer_treesEaten = random.randint(0,100)
        roeDeer_scrubEaten = random.randint(0,100)
        # Fallow deer
        fallowDeer_reproduce = np.random.uniform(0,1)
        fallowDeer_gain_from_grass = np.random.uniform(0,1)
        fallowDeer_gain_from_Trees = np.random.uniform(0,1)
        fallowDeer_gain_from_Scrub = np.random.uniform(0,1)
        fallowDeer_gain_from_Saplings = np.random.uniform(0,1)
        fallowDeer_gain_from_YoungScrub = np.random.uniform(0,1)
        fallowDeer_impactGrass = random.randint(roeDeer_impactGrass,100)
        fallowDeer_saplingsEaten = random.randint(roeDeer_saplingsEaten,1000)
        fallowDeer_youngScrubEaten = random.randint(roeDeer_youngScrubEaten,1000)
        fallowDeer_treesEaten = random.randint(roeDeer_treesEaten,100)
        fallowDeer_scrubEaten = random.randint(roeDeer_scrubEaten,100)
        # Red deer
        redDeer_reproduce = np.random.uniform(0,1)
        redDeer_gain_from_grass = np.random.uniform(0,1)
        redDeer_gain_from_Trees = np.random.uniform(0,1)
        redDeer_gain_from_Scrub = np.random.uniform(0,1)
        redDeer_gain_from_Saplings = np.random.uniform(0,1)
        redDeer_gain_from_YoungScrub = np.random.uniform(0,1)
        redDeer_impactGrass = random.randint(fallowDeer_impactGrass,100)
        redDeer_saplingsEaten = random.randint(fallowDeer_saplingsEaten,1000)
        redDeer_youngScrubEaten = random.randint(fallowDeer_youngScrubEaten,1000)
        redDeer_treesEaten = random.randint(fallowDeer_treesEaten,100)
        redDeer_scrubEaten = random.randint(fallowDeer_scrubEaten,100)
        # Exmoor ponies
        ponies_gain_from_grass = np.random.uniform(0,1)
        ponies_gain_from_Trees = np.random.uniform(0,1)
        ponies_gain_from_Scrub = np.random.uniform(0,1)
        ponies_gain_from_Saplings = np.random.uniform(0,1)
        ponies_gain_from_YoungScrub = np.random.uniform(0,1)
        ponies_impactGrass = random.randint(redDeer_impactGrass,100)
        ponies_saplingsEaten = random.randint(redDeer_saplingsEaten,1000)
        ponies_youngScrubEaten = random.randint(redDeer_youngScrubEaten,1000)
        ponies_treesEaten = random.randint(redDeer_treesEaten,100)
        ponies_scrubEaten = random.randint(redDeer_scrubEaten,100)
        # Longhorn cattle
        cows_reproduce = np.random.uniform(0,1)
        cows_gain_from_grass = np.random.uniform(0,1)
        cows_gain_from_Trees = np.random.uniform(0,1)
        cows_gain_from_Scrub = np.random.uniform(0,1)
        cows_gain_from_Saplings = np.random.uniform(0,1)
        cows_gain_from_YoungScrub = np.random.uniform(0,1)
        cows_impactGrass = random.randint(ponies_impactGrass,100)
        cows_saplingsEaten = random.randint(ponies_saplingsEaten,1000)
        cows_youngScrubEaten = random.randint(ponies_youngScrubEaten,1000)
        cows_treesEaten = random.randint(ponies_treesEaten,100)
        cows_scrubEaten = random.randint(ponies_scrubEaten,100)
        # Tamworth pigs
        pigs_reproduce = np.random.uniform(0,1)
        pigs_gain_from_grass = np.random.uniform(0,1)
        pigs_gain_from_Saplings = np.random.uniform(0,1)
        pigs_gain_from_YoungScrub = np.random.uniform(0,1)
        pigs_impactGrass = random.randint(cows_impactGrass,100)
        pigs_saplingsEaten = random.randint(cows_saplingsEaten,1000)
        pigs_youngScrubEaten = random.randint(cows_youngScrubEaten,1000)

        # keep track of my parameters
        parameters_used = [
            run_number,
            chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
            chance_scrubOutcompetedByTree, chance_grassOutcompetedByTreeScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
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
            pigs_impactGrass, pigs_saplingsEaten, pigs_youngScrubEaten 
            ]
        # append to dataframe
        final_parameters.append(parameters_used)

        # keep track of the runs
        run_number +=1
        print(run_number)
        model = KneppModel(
            chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
            chance_scrubOutcompetedByTree, chance_grassOutcompetedByTreeScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
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
            width = 50, height = 36)
        model.run_model()

        # remember the results of the model (dominant conditions, # of agents)
        results = model.datacollector.get_model_vars_dataframe()
        results['run_number'] = run_number
        final_results_list.append(results)
        
    # append to dataframe
    final_results = pd.concat(final_results_list)

    variables = [
        # number of runs
        "run_number",
        # habitat variables
        "chance_reproduceSapling", # this is to initialize the initial dominant condition
        "chance_reproduceYoungScrub",  # this is to initialize the initial dominant condition
        "chance_regrowGrass", # this is to initialize the initial dominant condition
        "chance_saplingBecomingTree",
        "chance_youngScrubMatures",
        "chance_scrubOutcompetedByTree", # if tree matures, chance of scrub decreasing
        "chance_grassOutcompetedByTreeScrub",
        "chance_saplingOutcompetedByTree",
        "chance_saplingOutcompetedByScrub",
        "chance_youngScrubOutcompetedByScrub",
        "chance_youngScrubOutcompetedByTree",
        # initial values
        "initial_roeDeer",
        "initial_grassland",
        "initial_woodland",
        "initial_scrubland",
        # roe deer variables
        "roeDeer_reproduce",
        "roeDeer_gain_from_grass",
        "roeDeer_gain_from_Trees",
        "roeDeer_gain_from_Scrub",
        "roeDeer_gain_from_Saplings", 
        "roeDeer_gain_from_YoungScrub", 
        "roeDeer_impactGrass",
        "roeDeer_saplingsEaten",
        "roeDeer_youngScrubEaten",
        "roeDeer_treesEaten",
        "roeDeer_scrubEaten",
        # Exmoor pony variables
        "ponies_gain_from_grass", 
        "ponies_gain_from_Trees", 
        "ponies_gain_from_Scrub", 
        "ponies_gain_from_Saplings", 
        "ponies_gain_from_YoungScrub", 
        "ponies_impactGrass", 
        "ponies_saplingsEaten", 
        "ponies_youngScrubEaten", 
        "ponies_treesEaten", 
        "ponies_scrubEaten", 
        # Cow variables
        "cows_reproduce", 
        "cows_gain_from_grass", 
        "cows_gain_from_Trees", 
        "cows_gain_from_Scrub", 
        "cows_gain_from_Saplings", 
        "cows_gain_from_YoungScrub", 
        "cows_impactGrass", 
        "cows_saplingsEaten", 
        "cows_youngScrubEaten", 
        "cows_treesEaten", 
        "cows_scrubEaten", 
        # Fallow deer variables
        "fallowDeer_reproduce", 
        "fallowDeer_gain_from_grass", 
        "fallowDeer_gain_from_Trees", 
        "fallowDeer_gain_from_Scrub", 
        "fallowDeer_gain_from_Saplings", 
        "fallowDeer_gain_from_YoungScrub", 
        "fallowDeer_impactGrass", 
        "fallowDeer_saplingsEaten", 
        "fallowDeer_youngScrubEaten", 
        "fallowDeer_treesEaten", 
        "fallowDeer_scrubEaten",
        # Red deer variables
        "redDeer_reproduce", 
        "redDeer_gain_from_grass", 
        "redDeer_gain_from_Trees", 
        "redDeer_gain_from_Scrub", 
        "redDeer_gain_from_Saplings", 
        "redDeer_gain_from_YoungScrub", 
        "redDeer_impactGrass", 
        "redDeer_saplingsEaten", 
        "redDeer_youngScrubEaten", 
        "redDeer_treesEaten", 
        "redDeer_scrubEaten", 
        # Pig variables
        "pigs_reproduce", 
        "pigs_gain_from_grass", 
        "pigs_gain_from_Saplings", 
        "pigs_gain_from_YoungScrub", 
        "pigs_impactGrass", 
        "pigs_saplingsEaten", 
        "pigs_youngScrubEaten" 
        ]

    # check out the parameters used
    final_parameters = pd.DataFrame(data=final_parameters, columns=variables)

    # accepted runs are those that made it to year 184, plus this last filtering criteria
    all_accepted_runs = final_results[(final_results["Time"] == 185)
                                # (final_results["Roe deer"] <= 40) & (final_results["Roe deer"] >= 20)
                                # (final_results["Grassland"] <= 69) & (final_results["Grassland"] >= 49) &
                                # (final_results["Woodland"] <= 35) & (final_results["Woodland"] >= 21) &
                                # (final_results["Thorny Scrub"] <= 29) & (final_results["Thorny Scrub"] >= 9)
                                ]

    # accepted parameters
    accepted_parameters = final_parameters[final_parameters['run_number'].isin(all_accepted_runs['run_number'])]

    with pd.option_context('display.max_columns',None):
        print(final_results[(final_results["Time"] == 185)])

    with pd.option_context('display.max_rows',None, 'display.max_columns',None):
        print("accepted_years: \n", all_accepted_runs)
        
    return accepted_parameters, all_accepted_runs, variables

run_model()


# calculate the time it takes to run per node, currently 8.5min for 1k runs
stop = timeit.default_timer()
print('Total time: ', (stop - start))