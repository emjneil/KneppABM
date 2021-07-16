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


# ------ Define the agents: roe deer & habitat nodes (grassland, woodland, scrub) ------
  
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
        self.energy -= 0.01

        # Eat what's on my patch
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        # are there saplings here? pick how many to eat, gain energy
        if habitat_patch.saplings_here > 0:
            # gain energy
            self.energy += self.model.roeDeer_gain_from_Saplings
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
        # are there trees here?
        if habitat_patch.trees_here > 0:
            self.energy += self.model.roeDeer_gain_from_Trees
            # roll dice between 0 and my maximum number I'll eat
            eatenTrees = random.randint(0,self.model.roeDeer_treesEaten)
            habitat_patch.trees_here -= eatenTrees
            # don't let it go negative
            if habitat_patch.trees_here < 0:
                habitat_patch.trees_here = 0
        # are there shrubs here? pick how many to eat, gain energy'            
        if habitat_patch.scrub_here > 0:
            self.energy += self.model.roeDeer_gain_from_Scrub
                # roll dice between 0 and my maximum number I'll eat
            eatenScrub = random.randint(0,self.model.roeDeer_scrubEaten)
            habitat_patch.scrub_here -= eatenScrub
            # don't let it go negative
            if habitat_patch.scrub_here < 0:
                habitat_patch.scrub_here = 0
        # what about young shrubs?
        if habitat_patch.youngscrub_here > 0:
            self.energy += self.model.roeDeer_gain_from_YoungScrub
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
        # is there grass?
        if habitat_patch.perc_grass_here > 0:
            self.energy += self.model.roeDeer_gain_from_grass
            # roll dice between 0 and my maximum number I'll eat
            eatenGrass = random.randint(0,self.model.roeDeer_impactGrass)
            habitat_patch.perc_grass_here -= eatenGrass
            habitat_patch.perc_bareground_here += eatenGrass
            # don't let it go negative
            if habitat_patch.perc_grass_here < 0:
                habitat_patch.perc_grass_here = 0
                habitat_patch.perc_bareground_here = 100
    
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
        self.energy -= 0.01

        # Eat what's on my patch
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        # are there saplings here? pick how many to eat, gain energy
        if habitat_patch.saplings_here > 0:
            # gain energy
            self.energy += self.model.ponies_gain_from_Saplings
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
        # are there trees here?
        if habitat_patch.trees_here > 0:
            self.energy += self.model.ponies_gain_from_Trees
            # roll dice between 0 and my maximum number I'll eat
            eatenTrees = random.randint(0,self.model.ponies_treesEaten)
            habitat_patch.trees_here -= eatenTrees
            # don't let it go negative
            if habitat_patch.trees_here < 0:
                habitat_patch.trees_here = 0
        # are there shrubs here? pick how many to eat, gain energy           
        if habitat_patch.scrub_here > 0:
            self.energy += self.model.ponies_gain_from_Scrub
                # roll dice between 0 and my maximum number I'll eat
            eatenScrub = random.randint(0,self.model.ponies_scrubEaten)
            habitat_patch.scrub_here -= eatenScrub
            # don't let it go negative
            if habitat_patch.scrub_here < 0:
                habitat_patch.scrub_here = 0
        # what about young shrubs?
        if habitat_patch.youngscrub_here > 0:
            self.energy += self.model.ponies_gain_from_YoungScrub
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
        # is there grass?
        if habitat_patch.perc_grass_here > 0:
            self.energy += self.model.ponies_gain_from_grass
            # roll dice between 0 and my maximum number I'll eat
            eatenGrass = random.randint(0,self.model.ponies_impactGrass)
            habitat_patch.perc_grass_here -= eatenGrass
            habitat_patch.perc_bareground_here += eatenGrass
            # don't let it go negative
            if habitat_patch.perc_grass_here < 0:
                habitat_patch.perc_grass_here = 0
                habitat_patch.perc_bareground_here = 100
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
        self.energy -= 0.01

        # Eat what's on my patch
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        # are there saplings here? pick how many to eat, gain energy
        if habitat_patch.saplings_here > 0:
            # gain energy
            self.energy += self.model.cows_gain_from_Saplings
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
        # are there trees here?
        if habitat_patch.trees_here > 0:
            self.energy += self.model.cows_gain_from_Trees
            # roll dice between 0 and my maximum number I'll eat
            eatenTrees = random.randint(0,self.model.cows_treesEaten)
            habitat_patch.trees_here -= eatenTrees
            # don't let it go negative
            if habitat_patch.trees_here < 0:
                habitat_patch.trees_here = 0
        # are there shrubs here? pick how many to eat, gain energy           
        if habitat_patch.scrub_here > 0:
            self.energy += self.model.cows_gain_from_Scrub
                # roll dice between 0 and my maximum number I'll eat
            eatenScrub = random.randint(0,self.model.cows_scrubEaten)
            habitat_patch.scrub_here -= eatenScrub
            # don't let it go negative
            if habitat_patch.scrub_here < 0:
                habitat_patch.scrub_here = 0
        # what about young shrubs?
        if habitat_patch.youngscrub_here > 0:
            self.energy += self.model.cows_gain_from_YoungScrub
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
        # is there grass?
        if habitat_patch.perc_grass_here > 0:
            self.energy += self.model.cows_gain_from_grass
            # roll dice between 0 and my maximum number I'll eat
            eatenGrass = random.randint(0,self.model.cows_impactGrass)
            habitat_patch.perc_grass_here -= eatenGrass
            habitat_patch.perc_bareground_here += eatenGrass
            # don't let it go negative
            if habitat_patch.perc_grass_here < 0:
                habitat_patch.perc_grass_here = 0
                habitat_patch.perc_bareground_here = 100
    
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
        self.energy -= 0.01

        # Eat what's on my patch
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        # are there saplings here? pick how many to eat, gain energy
        if habitat_patch.saplings_here > 0:
            # gain energy
            self.energy += self.model.fallowDeer_gain_from_Saplings
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
        # are there trees here?
        if habitat_patch.trees_here > 0:
            self.energy += self.model.fallowDeer_gain_from_Trees
            # roll dice between 0 and my maximum number I'll eat
            eatenTrees = random.randint(0,self.model.fallowDeer_treesEaten)
            habitat_patch.trees_here -= eatenTrees
            # don't let it go negative
            if habitat_patch.trees_here < 0:
                habitat_patch.trees_here = 0
        # are there shrubs here? pick how many to eat, gain energy'            
        if habitat_patch.scrub_here > 0:
            self.energy += self.model.fallowDeer_gain_from_Scrub
                # roll dice between 0 and my maximum number I'll eat
            eatenScrub = random.randint(0,self.model.fallowDeer_scrubEaten)
            habitat_patch.scrub_here -= eatenScrub
            # don't let it go negative
            if habitat_patch.scrub_here < 0:
                habitat_patch.scrub_here = 0
        # what about young shrubs?
        if habitat_patch.youngscrub_here > 0:
            self.energy += self.model.fallowDeer_gain_from_YoungScrub
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
        # is there grass?
        if habitat_patch.perc_grass_here > 0:
            self.energy += self.model.fallowDeer_gain_from_grass
            # roll dice between 0 and my maximum number I'll eat
            eatenGrass = random.randint(0,self.model.fallowDeer_impactGrass)
            habitat_patch.perc_grass_here -= eatenGrass
            habitat_patch.perc_bareground_here += eatenGrass
            # don't let it go negative
            if habitat_patch.perc_grass_here < 0:
                habitat_patch.perc_grass_here = 0
                habitat_patch.perc_bareground_here = 100
    
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
        self.energy -= 0.01

        # Eat what's on my patch
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        # are there saplings here? pick how many to eat, gain energy
        if habitat_patch.saplings_here > 0:
            # gain energy
            self.energy += self.model.redDeer_gain_from_Saplings
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
        # are there trees here?
        if habitat_patch.trees_here > 0:
            self.energy += self.model.redDeer_gain_from_Trees
            # roll dice between 0 and my maximum number I'll eat
            eatenTrees = random.randint(0,self.model.redDeer_treesEaten)
            habitat_patch.trees_here -= eatenTrees
            # don't let it go negative
            if habitat_patch.trees_here < 0:
                habitat_patch.trees_here = 0
        # are there shrubs here? pick how many to eat, gain energy'            
        if habitat_patch.scrub_here > 0:
            self.energy += self.model.redDeer_gain_from_Scrub
                # roll dice between 0 and my maximum number I'll eat
            eatenScrub = random.randint(0,self.model.redDeer_scrubEaten)
            habitat_patch.scrub_here -= eatenScrub
            # don't let it go negative
            if habitat_patch.scrub_here < 0:
                habitat_patch.scrub_here = 0
        # what about young shrubs?
        if habitat_patch.youngscrub_here > 0:
            self.energy += self.model.redDeer_gain_from_YoungScrub
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
        # is there grass?
        if habitat_patch.perc_grass_here > 0:
            self.energy += self.model.redDeer_gain_from_grass
            # roll dice between 0 and my maximum number I'll eat
            eatenGrass = random.randint(0,self.model.redDeer_impactGrass)
            habitat_patch.perc_grass_here -= eatenGrass
            habitat_patch.perc_bareground_here += eatenGrass
            # don't let it go negative
            if habitat_patch.perc_grass_here < 0:
                habitat_patch.perc_grass_here = 0
                habitat_patch.perc_bareground_here = 100
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
        self.energy -= 0.01

        # Eat what's on my patch
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        # are there saplings here? pick how many to eat, gain energy
        if habitat_patch.saplings_here > 0:
            # gain energy
            self.energy += self.model.pigs_gain_from_Saplings
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
                piglet = longhornCattle(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
                self.model.grid.place_agent(piglet, self.pos)
                self.model.schedule.add(piglet)



# ------ Define the model ------

class KneppModel(Model):

    def __init__(self,             
            chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
            chance_scrubOutcompetedByTree, chance_grassOutcompetedByTreeScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
            initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland, initial_ponies, initial_cows, initial_fallowDeer, initial_redDeer, initial_pigs,
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
        self.initial_ponies = initial_ponies
        self.initial_cows = initial_cows
        self.initial_fallowDeer = initial_fallowDeer
        self.initial_redDeer = initial_redDeer
        self.initial_pigs = initial_pigs
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
                trees_here = random.randint(0, 25)
                saplings_here = random.randint(0, 1000)
                scrub_here = random.randint(0, 25)
                youngscrub_here = random.randint(0, 1000)
                perc_grass_here = random.randint(50, 100)
                perc_bareground_here = 100 - perc_grass_here
            if condition == "bare_ground": # more than 50% bare ground
                trees_here = random.randint(0, 25)
                saplings_here = random.randint(0, 1000)
                scrub_here = random.randint(0, 25)
                youngscrub_here = random.randint(0, 1000)
                perc_bareground_here = random.randint(50, 100)
                perc_grass_here = 100 - perc_bareground_here
            if condition == "thorny_scrubland":  # at least 10 scrub plants, no more than 10 trees
                trees_here = random.randint(0, 25)
                saplings_here = random.randint(0, 1000)
                scrub_here = random.randint(25, 100)
                youngscrub_here = random.randint(0, 1000)
                perc_grass_here = random.randint(0, 100)
                perc_bareground_here = 100 - perc_grass_here
            if condition == "woodland":  # woodland has 10-100 trees
                trees_here = random.randint(25, 100)
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

        # Create ponies
        for i in range(self.initial_ponies):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            energy = np.random.uniform(0, 1)
            pony = exmoorPony(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(pony, (x, y))
            self.schedule.add(pony)


        # Create cows
        for i in range(self.initial_cows):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            energy = np.random.uniform(0, 1)
            cow = longhornCattle(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(cow, (x, y))
            self.schedule.add(cow)


        # Create fallow deer
        for i in range(self.initial_fallowDeer):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            energy = np.random.uniform(0, 1) 
            fallow = fallowDeer(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(fallow, (x, y))
            self.schedule.add(fallow)


        # Create red deer
        for i in range(self.initial_redDeer):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            energy = np.random.uniform(0, 1)
            red = redDeer(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(red, (x, y))
            self.schedule.add(red)


        # Create pigs
        for i in range(self.initial_pigs):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            energy = np.random.uniform(0, 1)
            pigs = tamworthPigs(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(pigs, (x, y))
            self.schedule.add(pigs)




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
                            # agent_reporters={
                            # "Habitat position": lambda m: self.agent_position(m, habitatAgent) # function that checks if I'm habitat, if so, return number
                            # }
                            )

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)


    def count_condition(self, model, habitat_condition):
        # want to count grass, wood, scrub, bare ground in each patch
        count = 0
        for key, value in model.schedule.agents_by_breed[habitatAgent].items():
            if value.condition == habitat_condition:
                count += 1
        # return percentage of entire area
        return int((count/1800)*100)


    def run_model(self, months):
        
        for i in range(months):
            self.step()
            print("time", self.schedule.time)
