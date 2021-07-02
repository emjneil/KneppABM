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
    def __init__(self, pos, model, condition, trees_here, saplings_here, scrub_here, youngscrub_here, perc_grass_here, perc_bareground_here):
        super().__init__(pos, model)
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
        if self.trees_here < 10 and self.scrub_here < 10 and self.perc_grass_here >= 50:
            self.condition = "grassland"
        if self.trees_here < 10 and self.scrub_here < 10 and self.perc_bareground_here >= 50:
            self.condition = "bare_ground"
        if self.trees_here < 10 and self.scrub_here >= 10:
            self.condition = "thorny_scrubland"
        if self.trees_here >= 10:
            self.condition = "woodland"

class roeDeer_agent(RandomWalker):
    def __init__(self, pos, model, moore, energy, sex):
        super().__init__(pos, model, moore=moore)
        self.energy = energy
        self.sex = sex

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
            
        # if I am female, I reproduce in May & June (assuming model starts in Jan at beginning of year, May & June = time steps 4-6 out of every 12 months)
        if living and self.sex == "female" and random.random() < self.model.roeDeer_reproduce and (4 <= self.model.schedule.time < 6 or 16 <= self.model.schedule.time < 18 or 28 <= self.model.schedule.time < 30 or 40 <= self.model.schedule.time < 42):
            # Create a new roe deer and divide energy:
            self.energy /= 2
            self.sex = np.random.choice(["male","female"])
            fawn = roeDeer_agent(self.pos, self.model, self.moore, self.energy, self.sex)
            self.model.grid.place_agent(fawn, self.pos)
            self.model.schedule.add(fawn)
    




# ------ Define the model ------

class KneppModel(Model):

    def __init__(self, chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
        chance_scrubOutcompetedByTree, chance_grassOutcompetedByTreeScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub,chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
        initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland,
        roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
        roeDeer_impactGrass, roeDeer_saplingsEaten, roeDeer_youngScrubEaten, roeDeer_treesEaten, roeDeer_scrubEaten, width, height):

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
        # other parameters
        self.height = height
        self.width = width
        # set grid & schedule
        self.grid = MultiGrid(width, height, True) # this grid allows for multiple agents on same cell
        self.schedule = RandomActivationByBreed(self)
        self.running = True


        # Create habitat patches
        for _, x, y in self.grid.coord_iter():
            # generate % dominant habitat condition (woodland, scrub, grassland, any remaining = bare ground)
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
            condition = np.random.choice(["grassland", "thorny_scrubland", "woodland", "bare_ground"], p=[prob_grassland, prob_scrubland, prob_woodland, prob_bare_ground])            
            # put a random number of trees, shrubs, etc., depending on dominant condition
            if condition == "grassland": # more than 50% grassland, no more than 10 mature trees/shrubs
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
            patch = habitatAgent((x, y), self, condition, trees_here, saplings_here, scrub_here, youngscrub_here, perc_grass_here, perc_bareground_here)
            self.grid.place_agent(patch, (x, y))
            self.schedule.add(patch)


        # Create roe deer
        for i in range(self.initial_roeDeer):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            energy = np.random.uniform(0, 1)
            sex = np.random.choice(["male","female"])
            roeDeer = roeDeer_agent((x, y), self, True, energy, sex)
            self.grid.place_agent(roeDeer, (x, y))
            self.schedule.add(roeDeer)


        # get data organized
        self.datacollector = DataCollector(model_reporters = {
                            "Time": lambda m: m.schedule.time, 
                            "Roe deer": lambda m: m.schedule.get_breed_count(roeDeer_agent),
                            "Grassland": lambda m: self.count_condition(m, "grassland"),
                            "Woodland": lambda m: self.count_condition(m, "woodland"),
                            "Thorny Scrub": lambda m: self.count_condition(m, "thorny_scrubland"),
                            "Bare ground": lambda m: self.count_condition(m, "bare_ground"),
                            })


    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)


    def count_condition(self, model, habitat_condition):
        # want to count grass, wood, scrub, bare ground in each patch
        count = 0
        for agent in model.schedule.agents_by_breed[habitatAgent]:
            if agent.condition == habitat_condition:
                count += 1
        return count

