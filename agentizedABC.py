# ------ ABM of the Knepp Estate (2005-2046) --------

# download packages
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd
from random import randrange
from random_walk import RandomWalker
from schedule import RandomActivationByBreed
from mesa.space import MultiGrid



# ------ Define the agents: roe deer & habitat nodes (grassland, woodland, scrub) ------
  
class habitatAgent (Agent):
    def __init__(self, pos, model, condition, trees_here, saplings_here, scrub_here, youngscrub_here, perc_grass_here, perc_bareground_here):
        super().__init__(pos, model)
        self.condition = condition
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
            only_habitat_cells = [obj for obj in items_in_neighborhood if not any(isinstance(x, roeDeer_agent) for x in obj)]
            available_sapling_cell = [obj for obj in only_habitat_cells if not any(x.saplings_here >= 1000 for x in obj)]
            if len(available_sapling_cell) > 0:
                new_patch_sapling = self.random.choice(available_sapling_cell)[0] 
                # and put a sapling there
                new_patch_sapling.saplings_here += 1

        # chance of reproducing young scrub
        if self.scrub_here > 0 and random.random() < self.model.chance_reproduceYoungScrub:
            # find my neighboring cells, including the one I'm in
            neighborhood_list = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)
            items_in_neighborhood = list(map(self.model.grid.get_cell_list_contents, neighborhood_list)) 
            # pick one that has less than 1000 young scrubs
            only_habitat_cells = [obj for obj in items_in_neighborhood if not any(isinstance(x, roeDeer_agent) for x in obj)]
            available_youngscrub_cell = [obj for obj in only_habitat_cells if not any(x.youngscrub_here >= 1000 for x in obj)]
            if len(available_youngscrub_cell) > 0:
                new_patch_youngscrub = self.random.choice(available_youngscrub_cell)[0] 
                # and put a young scrub there
                new_patch_youngscrub.youngscrub_here += 1

        # chance of bare ground becoming grassland
        if random.random() < self.model.chance_regrowGrass:
            self.perc_grass_here += 1
            self.perc_bareground_here -= 1

        # chance of young scrub becoming mature scrub
        if self.youngscrub_here > 0:
            if random.random() < self.model.chance_youngScrubMatures:
                self.scrub_here += 1
                self.youngscrub_here -= 1
            # if a mature scrub is added, chance of grassland being outcompeted
                if self.perc_grass_here >0 and random.random() < self.model.chance_grassOutcompetedByTreeScrub:
                    self.perc_bareground_here += 1
                    self.perc_grass_here -= 1
                # or of scrub/saplings outcompeted
                if self.saplings_here > 0 and random.random() < self.model.chance_youngScrubOutcompetedByScrub and self.saplings_here >0:
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
                    if random.random() < self.model.chance_saplingOutcompetedByTree and self.youngscrub_here > 0:
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
        self.random_move()
        living = True 
        # reduce energy
        self.energy -= 0.01

        # Look at the patch I'm on
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        habitat_patch = [obj for obj in this_cell if isinstance(obj, habitatAgent)][0]
        # roe deer prefer to eat scrub & woodland
        print("trees:",habitat_patch.trees_here, "shrub:",habitat_patch.scrub_here, "saplings:",habitat_patch.saplings_here)
        if habitat_patch.trees_here > 0 or habitat_patch.scrub_here > 0:
            self.energy += self.model.roeDeer_gain_from_TreesAndScrub
            # trees, scrub, and young plants eaten
            if random.random() < herbivore_impactSaplings_youngScrub and habitat_patch.saplings_here > 0:
                habitat_patch.saplings_here -= 1
            if random.random() < herbivore_impactSaplings_youngScrub and habitat_patch.youngscrub_here > 0:
                habitat_patch.youngscrub_here -= 1
            if random.random() < roeDeer_impactTrees and habitat_patch.trees_here > 0:
                habitat_patch.trees_here -= 1
            if random.random() < roeDeer_impactScrubland and habitat_patch.scrub_here > 0:
                habitat_patch.scrub_here -= 1
        # otherwise eat grass
        elif habitat_patch.perc_grass_here > 0:
            self.energy += self.model.roeDeer_gain_from_grass
            if random.random() < herbivore_impactGrass and habitat_patch.perc_grass_here > 0:
                habitat_patch.perc_bareground_here += 1
                habitat_patch.perc_grass_here -= 1
                # young scrub and saplings could be mixed in with the grass
            if random.random() < herbivore_impactSaplings_youngScrub and habitat_patch.saplings_here > 0:
                habitat_patch.saplings_here -= 1
            if random.random() < herbivore_impactSaplings_youngScrub and habitat_patch.youngscrub_here > 0:
                habitat_patch.youngscrub_here -= 1

        # if roe deer's energy is less than 0, die 
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False
            
        # if I am female, I reproduce in May & June (assuming model starts in Jan at beginning of year, May & June = time steps 4-6 out of every 12 months)
        if living and self.sex == "female" and random.random() < self.model.roeDeer_reproduce and (4 <= model.schedule.time < 6 or 16 <= model.schedule.time < 18 or 28 <= model.schedule.time < 30 or 40 <= model.schedule.time < 42):
            # Create a new roe deer and divide energy:
            self.energy /= 2
            self.sex = np.random.choice(["male","female"])
            fawn = roeDeer_agent(self.pos, self.model, self.moore, self.energy, self.sex)
            self.model.grid.place_agent(fawn, self.pos)
            self.model.schedule.add(fawn)
    




# ------ Define the model ------

class KneppModel(Model):
    def __init__(self, chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, chance_scrubOutcompetedByTree, chance_grassOutcompetedByTreeScrub, chance_saplingOutcompetedByTree, chance_youngScrubOutcompetedByScrub,
        initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland,
        roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_TreesAndScrub, roeDeer_impactTrees, roeDeer_impactScrubland,
        herbivore_impactGrass, herbivore_impactSaplings_youngScrub, width, height):
        

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
        self.chance_grassOutcompetedByTreeScrub = chance_grassOutcompetedByTreeScrub
        self.chance_saplingOutcompetedByTree = chance_saplingOutcompetedByTree
        self.chance_youngScrubOutcompetedByScrub = chance_youngScrubOutcompetedByScrub
        # roe deer parameters
        self.roeDeer_gain_from_grass = roeDeer_gain_from_grass
        self.roeDeer_gain_from_TreesAndScrub = roeDeer_gain_from_TreesAndScrub
        self.roeDeer_reproduce = roeDeer_reproduce
        self.roeDeer_impactTrees = roeDeer_impactTrees
        self.roeDeer_impactScrubland = roeDeer_impactScrubland
        # all herbivore parameters
        self.herbivore_impactGrass = herbivore_impactGrass
        self.herbivore_impactSaplings_youngScrub = herbivore_impactSaplings_youngScrub
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


# # ----- Create a model with agents and run it for 10 steps -----

# define number of simulations
number_simulations = 1
# time for first ODE (2005-2009, ~ 48 months)
time_firstModel = 12
# make list of variables

variables = [
    # number of runs
    "run_number",
    # habitat variables
    "initial_grassland", # this is to initialize the initial dominant condition
    "initial_woodland",  # this is to initialize the initial dominant condition
    "initial_scrubland", # this is to initialize the initial dominant condition
    "chance_reproduceSapling",
    "chance_reproduceYoungScrub",
    "chance_regrowGrass",
    "chance_saplingBecomingTree",
    "chance_youngScrubMatures",
    "chance_scrubOutcompetedByTree", # if tree matures, chance of scrub decreasing
    "chance_grassOutcompetedByTreeScrub",
    "chance_saplingOutcompetedByTree",
    "chance_youngScrubOutcompetedByScrub",
    # roe deer variables
    "initial_roeDeer",
    "roeDeer_gain_from_grass",
    "roeDeer_gain_from_TreesAndScrub",
    "roeDeer_reproduce", 
    "roeDeer_impactTrees",
    "roeDeer_impactScrubland",
    # overall herbivore impacts
    "herbivore_impactGrass",
    "herbivore_impactSaplings_youngScrub",
    ]

final_results_list = []
final_parameters = []
run_number = 0

# run the model for 48 months, 10 times
for i in range(number_simulations):
    # keep track of the runs
    run_number +=1
    # define parameters
    initial_roeDeer = random.randint(1, 12)
    initial_grassland = random.randint(70, 90)
    initial_woodland = random.randint(9, 19)
    initial_scrubland = random.randint(0, 2)
    # habitats
    chance_reproduceSapling = np.random.uniform(0,1)
    chance_reproduceYoungScrub = np.random.uniform(0,1)
    chance_regrowGrass = np.random.uniform(0,1)
    chance_saplingBecomingTree = np.random.uniform(0,1)
    chance_youngScrubMatures = np.random.uniform(0,1)
    chance_scrubOutcompetedByTree = np.random.uniform(0,1) 
    chance_grassOutcompetedByTreeScrub = np.random.uniform(0,1)
    chance_saplingOutcompetedByTree = np.random.uniform(0,1)
    chance_youngScrubOutcompetedByScrub = np.random.uniform(0,1)
    # roe deer
    roeDeer_reproduce = np.random.uniform(0,1)
    roeDeer_gain_from_grass = np.random.uniform(0,1)
    roeDeer_gain_from_TreesAndScrub = np.random.uniform(0,1)
    roeDeer_impactTrees = np.random.uniform(0,1)
    roeDeer_impactScrubland = np.random.uniform(0,1)
    # all herbivores
    herbivore_impactGrass = np.random.uniform(0,1)
    herbivore_impactSaplings_youngScrub = np.random.uniform(0,1)


    # parameters = generate_parameters()
    parameters_used = [
        run_number,
        chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
        chance_scrubOutcompetedByTree, chance_grassOutcompetedByTreeScrub, chance_saplingOutcompetedByTree, chance_youngScrubOutcompetedByScrub,
        initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland,
        roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_TreesAndScrub, roeDeer_impactTrees, roeDeer_impactScrubland,
        herbivore_impactGrass, herbivore_impactSaplings_youngScrub
        ]
    # remember parameters used 
    final_parameters.append(parameters_used)
    # run the model 
    model = KneppModel(
        chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
        chance_scrubOutcompetedByTree, chance_grassOutcompetedByTreeScrub, chance_saplingOutcompetedByTree, chance_youngScrubOutcompetedByScrub,
        initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland,
        roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_TreesAndScrub, roeDeer_impactTrees, roeDeer_impactScrubland,
        herbivore_impactGrass, herbivore_impactSaplings_youngScrub,
        width = 10, height = 10)
    
    # run for 48 months (2005-2009)
    for j in range(time_firstModel):
        # run the model
        model.step()
    # remember the results
    results = model.datacollector.get_model_vars_dataframe()
    final_results_list.append(results)

# append to dataframe
final_results = pd.concat(final_results_list)


final_parameters = pd.DataFrame(data=final_parameters, columns=variables)

with pd.option_context('display.max_rows',None):
    print(final_results)
# with pd.option_context('display.max_columns',None):
#     print(final_parameters)