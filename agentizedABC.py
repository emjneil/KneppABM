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



# ------ Define the agents: roe deer, grassland, woodland ------
  
class grasslandParklandAgent(Agent):
    # grass grows, is eaten by herbivores, and can grow in empty patches
    def __init__(self, pos, model, condition, countdown):
        # create a new patch of grass
        super().__init__(pos, model)
        self.condition = condition
        self.countdown = countdown
    
    def step(self):
        if self.condition == "bare_ground":
            if self.countdown <= 0:
                # Set as fully grown
                self.condition = "fully_grown"
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1


class woodlandAgent(Agent):
    # woodland grows, is eaten by herbivores, [and is helped by scrub]
    def __init__(self, pos, model):
        # create a new woodland area
        super().__init__(pos, model)

    def step(self):
        # sprout one new sapling 
        if random.random() < self.model.woodland_regrowth_time:
            # find my neighboring cells, including the one I'm in
            neighborhood_list = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)
            # select those that aren't already full of woodland (number_trees => 100)
            items_in_neighborhood = list(map(self.model.grid.get_cell_list_contents, neighborhood_list))
            no_woodland_alone = [obj for obj in items_in_neighborhood if not any(isinstance(x, woodlandAgent) for x in obj)]
            if len(no_woodland_alone) > 0:
                # pick one randomly
                new_patch_wood = self.random.choice(no_woodland_alone)[0]
                # and put a wood cell there
                sapling = woodlandAgent(self.pos, self.model)
                self.model.grid.place_agent(sapling, new_patch_wood.pos, )
                self.model.schedule.add(sapling)

        # outcompete / "kill" grassland on my patch
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        grass_to_outcompete = [obj for obj in this_cell if isinstance(obj, grasslandParklandAgent)][0]
        if grass_to_outcompete.condition == "fully_grown":
            grass_to_outcompete.condition = "bare_ground"
   


class roeDeer_agent(RandomWalker):
    def __init__(self, pos, model, moore, energy):
        super().__init__(pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        living = True 
        # reduce energy
        self.energy -= 1

        # If there is grass available, eat it
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        grass_patch = [obj for obj in this_cell if isinstance(obj, grasslandParklandAgent)][0]
        if grass_patch.condition == "fully_grown":
            self.energy += self.model.roeDeer_gain_from_grass
            grass_patch.condition = "bare_ground"

        # eat woodland if it's there
        wood_patch = [obj for obj in this_cell if isinstance(obj, woodlandAgent)]
        if len(wood_patch) > 0:
            removed_patch = wood_patch[0]
            self.energy += self.model.roeDeer_gain_from_woodland
            self.model.grid._remove_agent(self.pos, removed_patch)
            self.model.schedule.remove(removed_patch)
        
        # if roe deer's energy is less than 0, die 
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False
            
        # reproduce in May & June (assuming model starts in Jan at beginning of year, May & June = time steps 4-6 out of every 12 months)
        if living and random.random() < self.model.roeDeer_reproduce and (4 <= model.schedule.time < 6 or 16 <= model.schedule.time < 18 or 28 <= model.schedule.time < 30 or 40 <= model.schedule.time < 42):
            # Create a new roe deer and divide energy:
            self.energy /= 2
            fawn = roeDeer_agent(self.pos, self.model, self.moore, self.energy)
            self.model.grid.place_agent(fawn, self.pos)
            self.model.schedule.add(fawn)
    


# ------ Define the model ------

class KneppModel(Model):
    def __init__(self, initial_roeDeer, initial_grassland, initial_woodland, roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_woodland, grass_regrowth_time, woodland_regrowth_time, width, height):
        
        # set parameters
        self.initial_roeDeer = initial_roeDeer
        self.initial_grassland = initial_grassland
        self.initial_woodland = initial_woodland
        self.grass_regrowth_time = grass_regrowth_time
        self.woodland_regrowth_time = woodland_regrowth_time
        self.roeDeer_gain_from_grass = roeDeer_gain_from_grass
        self.roeDeer_gain_from_woodland = roeDeer_gain_from_woodland
        self.roeDeer_reproduce = roeDeer_reproduce
        self.height = height
        self.width = width
        # set grid & schedule
        self.grid = MultiGrid(width, height, True) # this grid allows for multiple agents on same cell
        self.schedule = RandomActivationByBreed(self)
        self.running = True


        # Create grass patches
        for _, x, y in self.grid.coord_iter():
            condition = np.random.choice(["fully_grown", "bare_ground"], p=[initial_grassland/100, 1-(initial_grassland/100)])            
            if condition == "fully_grown":
                countdown = self.grass_regrowth_time
            else:
                countdown = self.random.randrange(self.grass_regrowth_time)
            patch = grasslandParklandAgent((x, y), self, condition, countdown)
            self.grid.place_agent(patch, (x, y))
            self.schedule.add(patch)


        # Create woodland
        x_coords = []
        y_coords = []
        for _, x, y in self.grid.coord_iter():
            x_coords.append(x)
            y_coords.append(y)
        all_coords = list(zip(x_coords,y_coords))
        # pick random cells in range of woodland numbers
        choices = random.sample(all_coords, k=self.initial_woodland)
        for x,y in choices:
            # sprout a certain number of trees
            wood = woodlandAgent((x,y), self)
            self.grid.place_agent(wood, (x,y))
            self.schedule.add(wood)


        # Create roe deer
        for i in range(self.initial_roeDeer):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            energy = np.random.uniform(2 * self.roeDeer_gain_from_grass)
            roeDeer = roeDeer_agent((x, y), self, True, energy)
            self.grid.place_agent(roeDeer, (x, y))
            self.schedule.add(roeDeer)


        # get data organized
        self.datacollector = DataCollector(model_reporters = {
                            "Time": lambda m: m.schedule.time, 
                            "Roe deer": lambda m: m.schedule.get_breed_count(roeDeer_agent),
                            # "Grassland": lambda m: m.schedule.get_breed_count(grasslandParklandAgent),
                            "Grassland": lambda m: self.count_type(m, "fully_grown"),
                            "Woodland": lambda m: m.schedule.get_breed_count(woodlandAgent),
                            "Bare ground": lambda m: self.count_type(m, "bare_ground"),
                            })

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)


    def count_type(self, model, habitat_condition):
        # count grass patches
        count = 0
        for agent in model.schedule.agents_by_breed[grasslandParklandAgent]:
            if agent.condition == habitat_condition:
                count += 1
        return count    




# # ----- Create a model with 10 agents and run it for 10 steps -----

# define number of simulations
number_simulations = 1
# time for first ODE (2005-2009, ~ 48 months)
time_firstModel = 20
# make list of variables
variables = ["initial_roeDeer", "initial_grassland", "initial_woodland", "roeDeer_reproduce", "roeDeer_gain_from_grass", "roeDeer_gain_from_woodland", "grass_regrowth_time", "woodland_regrowth_time", "run_number"]

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

    # make sure the habitat types sum to 100
    # if (initial_grassland + initial_woodland) > 100:
    #     scale_factor = 100/(initial_grassland + initial_woodland)
    #     # scale the initial values, make sure it's an integer
    #     initial_grassland = int(initial_grassland * scale_factor)
    #     initial_woodland = int(initial_woodland * scale_factor)

    roeDeer_reproduce = np.random.uniform(0,1)
    roeDeer_gain_from_grass = np.random.uniform(0,5)
    roeDeer_gain_from_woodland = np.random.uniform(0,5)
    grass_regrowth_time = random.randint(1,3)
    woodland_regrowth_time = np.random.uniform(0,0.1)

    # parameters = generate_parameters()
    parameters_used = [initial_roeDeer, initial_grassland, initial_woodland, roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_woodland, grass_regrowth_time, woodland_regrowth_time, run_number]
    # remember parameters used 
    final_parameters.append(parameters_used)
    # run the model 
    model = KneppModel(initial_roeDeer, initial_grassland, initial_woodland, roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_woodland, grass_regrowth_time, woodland_regrowth_time, width = 10, height = 10)
    
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
with pd.option_context('display.max_columns',None):
    print(final_parameters)