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
from mesa.space import MultiGrid # this grid allows multiple agents to be in same cell



# ------ Define the agents: roe deer, grassland ------
  
class grasslandParklandAgent(Agent):
    # grass grows, is eaten by herbivores, [and is outcompeted by trees & scrub]
    def __init__(self, pos, model, condition, countdown):
        # create a new patch of grass
        super().__init__(pos, model)
        self.condition = condition
        self.countdown = countdown
    def step(self):
        # grow grass
        if not self.condition == "fully_grown":
            if self.countdown <= 0:
                # Set as fully grown
                self.condition = "fully_grown"
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1




class roeDeer_agent(RandomWalker):
    def __init__(self, pos, model, moore, energy):
        super().__init__(pos, model, moore=moore)
        self.energy = energy

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        living = True 
        # reduce energy
        self.energy -= 1
        # if grass is available, eat it
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        grass_patch = [obj for obj in this_cell
                        if isinstance(obj, grasslandParklandAgent)][0]
        if grass_patch.condition == "fully_grown":
            self.energy += self.model.roeDeer_gain_from_food
            grass_patch.condition = "bare_ground"
        # if roe deer's energy is less than 0, die 
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False
        # reproduce
        if living and random.random() < self.model.roeDeer_reproduce:
            # Create a new roe deer and divide energy:
            self.energy /= 2
            fawn = roeDeer_agent(self.pos, self.model, self.moore, self.energy)
            self.model.grid.place_agent(fawn, self.pos)
            self.model.schedule.add(fawn)
    


# ------ Define the model ------

class KneppModel(Model):
    def __init__(self, initial_roeDeer, initial_grassland, roeDeer_reproduce, roeDeer_gain_from_food, grass_regrowth_time, width, height):
        
        # set parameters
        self.initial_roeDeer = initial_roeDeer
        self.initial_grassland = initial_grassland
        self.grass_regrowth_time = grass_regrowth_time
        self.roeDeer_gain_from_food = roeDeer_gain_from_food
        self.roeDeer_reproduce = roeDeer_reproduce
        self.height = height
        self.width = width
        # set grid & schedule
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivationByBreed(self)


        # Create roe deer
        for i in range(self.initial_roeDeer):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            energy = np.random.uniform(2 * self.roeDeer_gain_from_food)
            roeDeer = roeDeer_agent((x, y), self, True, energy)
            self.grid.place_agent(roeDeer, (x, y))
            self.schedule.add(roeDeer)


        # Create grassland
        for _, x, y in self.grid.coord_iter():
            condition = np.random.choice(["fully_grown", "bare_ground"], p=[initial_grassland/100, (100-initial_grassland)/100])
            if condition == "fully_grown":
                countdown = self.grass_regrowth_time
            else:
                countdown = random.randrange(self.grass_regrowth_time)
            grasslandParkland = grasslandParklandAgent((x, y), self, condition, countdown)
            self.grid.place_agent(grasslandParkland, (x, y))
            self.schedule.add(grasslandParkland)
        
        self.running = True

        # get data organized
        self.datacollector = DataCollector({
                            "Time": lambda m: m.schedule.time, 
                            "Roe deer": lambda m: m.schedule.get_breed_count(roeDeer_agent),
                            "Grassland": lambda m: self.count_type(m, "fully_grown")
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
number_simulations = 25
# time for first ODE (2005-2009, ~ 48 months)
time_firstModel = 10
# define other parameters 
initial_roeDeer = random.randint(1, 12)
initial_grassland = np.random.uniform(70, 90)
roeDeer_reproduce = np.random.uniform(0,1)
roeDeer_gain_from_food = np.random.uniform(0,100)
grass_regrowth_time = random.randint(1,10)

final_results = []
# run the model for 48 months, 10 times
model = KneppModel(initial_roeDeer, initial_grassland, roeDeer_reproduce, roeDeer_gain_from_food, grass_regrowth_time, width = 10, height = 10)
for i in range(number_simulations):
    for j in range(time_firstModel):
        # run the model
        model.step()

print(model.datacollector.get_model_vars_dataframe())

# results = model.datacollector.collect()
# print(results)
#         result["Roe deer"].append(model.number_roe_deer)
#         result["Grassland"].append(model.number_grassland)
# print(pd.DataFrame(result))
