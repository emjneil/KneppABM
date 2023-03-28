import mesa
import mesa_geo as mg
from shapely.geometry import Point, Polygon, MultiPolygon
import random
from collections import defaultdict
import numpy as np
from movements import browser_move, grazer_move, mixed_diet_move, eat_habitats, random_move
from schedule import RandomActivationByBreed
import uuid

#### --- Define the agents --- ###

class FieldAgent(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs):
        super().__init__(unique_id, model, geometry, crs)
        # set up the dominant habitat condition
        self.condition=np.random.choice(["grassland", "thorny_scrubland", "woodland", "bare_ground"], p=[0.899, 0.043, 0.058, 0])
        # what is the size of my patch? some fields are multipolygons
        if type(self.geometry) == Polygon:
            self.size_of_patch = Polygon(self.geometry).area
        # some of the fields are multipolygons 
        else:
            polygon_list = list([MultiPolygon(self.geometry)])
            self.size_of_patch = sum(polygon.area for polygon in polygon_list)

        # now set number of individual habitat components
        if self.condition == 'grassland': 
            self.trees_here = int(random.randint(0, 749)*(self.size_of_patch/10000))
            self.saplings_here = 0
            self.scrub_here = int(random.randint(0, 749)*(self.size_of_patch/10000))
            self.youngscrub_here = 0
            self.perc_grass_here = random.randint(50, 100)
            self.perc_bareground_here = 100 - self.perc_grass_here
        elif self.condition == "thorny_scrubland": 
            self.trees_here = int(random.randint(0, 749)*(self.size_of_patch/10000))
            self.saplings_here = int(random.randint(0, 5000)*(self.size_of_patch/10000))
            self.scrub_here = int(random.randint(750, 4000)*(self.size_of_patch/10000))
            self.youngscrub_here = int(random.randint(0, 5000)*(self.size_of_patch/10000))
            self.perc_grass_here = random.randint(0, 100)
            self.perc_bareground_here = 100 - self.perc_grass_here
        elif self.condition == "woodland":  
            self.trees_here = int(random.randint(750, 4000)*(self.size_of_patch/10000))
            self.saplings_here = int(random.randint(0, 5000)*(self.size_of_patch/10000))
            self.scrub_here = int(random.randint(0, 4000)*(self.size_of_patch/10000))
            self.youngscrub_here = int(random.randint(0, 5000)*(self.size_of_patch/10000))
            self.perc_grass_here = random.randint(0, 100)
            self.perc_bareground_here = 100 - self.perc_grass_here
        # this is the food available for herbivores in this habitat agent
        self.edibles = defaultdict(int)
        self.edibles["trees"] = self.trees_here
        self.edibles['scrub'] = self.scrub_here
        self.edibles["saplings"] = self.saplings_here
        self.edibles["youngScrub"] = self.youngscrub_here
        self.edibles["grass"] = self.perc_grass_here
        self.edibles["bare_ground"] = self.perc_bareground_here
        # habitat components 'removed' (herbivory, competition, growing to a new type)
        self.habs_eaten = defaultdict(int)
        self.habs_outcompeted_byTrees= defaultdict(int)
        self.habs_outcompeted_byScrub = defaultdict(int)
        self.habs_grew_up = defaultdict(int)


    # define a random point to add herbivores to
    def random_point(self):
        min_x, min_y, max_x, max_y = self.geometry.bounds
        while not self.geometry.contains(
            random_point := Point(
                random.uniform(min_x, max_x), random.uniform(min_y, max_y))):
            continue
        if random_point.is_valid:
            return random_point
        else:
            return Point(min_x, min_y)

    def step(self):
        self.habs_eaten.clear()
        self.habs_outcompeted_byTrees.clear()
        self.habs_outcompeted_byScrub.clear()
        self.habs_grew_up.clear()

        # chance of 1 young scrub becoming 1 mature scrub
        number_scrub_maturing = np.random.binomial(n=self.edibles["youngScrub"], p=self.model.chance_youngScrubMatures)
        # don't let it go over 4000 mature shrubs
        number_scrub_maturing = min(number_scrub_maturing, int((4000*(self.size_of_patch/10000)) - self.edibles['scrub']))
        self.edibles['scrub'] += number_scrub_maturing
        self.edibles["youngScrub"] -= number_scrub_maturing
        self.habs_grew_up["youngScrub"] += number_scrub_maturing

        # chance of sapling becoming tree
        number_saplings_maturing = np.random.binomial(n=self.edibles["saplings"], p=self.model.chance_saplingBecomingTree)
        # don't let it go over 4000 trees
        number_saplings_maturing = min(number_saplings_maturing, int((4000*(self.size_of_patch/10000)) - self.edibles["trees"]))
        self.edibles["trees"] += number_saplings_maturing
        self.edibles["saplings"] -= number_saplings_maturing
        self.habs_grew_up["saplings"] += number_saplings_maturing

        # chance of reproducing saplings or young shrubs
        my_field = self.model.space.get_region_by_id(self.unique_id)
        next_moves = self.model.saved_neighbors[my_field.unique_id]
        neighboring_habitats = [agent for agent in next_moves if (isinstance(agent, FieldAgent))]

        # chance of reproducing saplings
        number_reproduce_trees = np.random.binomial(n=self.edibles["trees"], p=self.model.chance_reproduceSapling)
        # are there any that aren't full of other saplings?
        available_sapling_cell = [i for i in neighboring_habitats if i.edibles["saplings"] < (5000*(self.size_of_patch/10000))]
        if len(available_sapling_cell) > 0: 
            list_of_choices = random.choices(available_sapling_cell, k = number_reproduce_trees)
            for i in range(number_reproduce_trees):
                new_patch_sapling = list_of_choices[i]
                new_patch_sapling.edibles["saplings"] += 1 

        list_of_choices = None
        # chance of reproducing scrub
        number_reproduce_shrubs = np.random.binomial(n=self.edibles['scrub'], p=self.model.chance_reproduceYoungScrub)
        # are there any that aren't full of other scrub/young scrub?
        available_youngscrub_cell = [i for i in neighboring_habitats if i.edibles["youngScrub"] < (5000*(self.size_of_patch/10000))]
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
        outcompeted_by_trees = (self.edibles["trees"]/(4000*(self.size_of_patch/10000)))*self.model.chance_grassOutcompetedByTree
        if outcompeted_by_trees>1: outcompeted_by_trees=1
        outcompeted_grass_byTrees = np.random.binomial(n=self.edibles["grass"], p=outcompeted_by_trees)
        if self.edibles["grass"] - outcompeted_grass_byTrees < 0: outcompeted_grass_byTrees = self.edibles["grass"]
        self.edibles["grass"] -= outcompeted_grass_byTrees
        self.edibles["bare_ground"] += outcompeted_grass_byTrees
        self.habs_outcompeted_byTrees["grass"] += outcompeted_grass_byTrees
        # shrubs
        outcompeted_by_shrubs = ((self.edibles['scrub']/(4000*(self.size_of_patch/10000)))*self.model.chance_grassOutcompetedByScrub)
        if outcompeted_by_shrubs>1: outcompeted_by_shrubs=1
        outcompeted_grass_byScrub = np.random.binomial(n=self.edibles["grass"], p=outcompeted_by_shrubs)
        if self.edibles["grass"] - outcompeted_grass_byScrub < 0: outcompeted_grass_byScrub = self.edibles["grass"]
        self.edibles["grass"] -= outcompeted_grass_byScrub
        self.edibles["bare_ground"] += outcompeted_grass_byScrub
        self.habs_outcompeted_byScrub["grass"] += outcompeted_grass_byScrub

        # chance of mature scrub being outcompeted by trees 
        prob=(self.edibles["trees"]/(4000*(self.size_of_patch/10000)))*self.model.chance_scrubOutcompetedByTree
        if prob>1: prob=1
        mature_scrub_outcompeted = np.random.binomial(n=self.edibles['scrub'], p=prob)
        if self.edibles["scrub"] - mature_scrub_outcompeted < 0: mature_scrub_outcompeted = self.edibles["scrub"]
        self.edibles['scrub'] -= mature_scrub_outcompeted
        self.habs_outcompeted_byTrees["scrub"] += mature_scrub_outcompeted

        # # saplings being outcompeted by scrub/trees
        # outcompeted_by_trees = ((self.edibles["trees"]/(4000*(self.size_of_patch/10000)))*self.model.chance_saplingOutcompetedByTree) 
        # if outcompeted_by_trees>1: outcompeted_by_trees=1
        # outcompeted_saplings_byTrees = np.random.binomial(n=self.edibles["saplings"], p=outcompeted_by_trees)
        # if self.edibles["saplings"] - outcompeted_saplings_byTrees < 0: outcompeted_saplings_byTrees = self.edibles["saplings"]
        # self.edibles["saplings"] -= outcompeted_saplings_byTrees
        # self.habs_outcompeted_byTrees["saplings"] += outcompeted_saplings_byTrees

        # outcompeted_by_shrubs = ((self.edibles['scrub']/(4000*(self.size_of_patch/10000)))*self.model.chance_saplingOutcompetedByScrub)
        # if outcompeted_by_shrubs>1: outcompeted_by_shrubs=1
        # outcompeted_saplings_byScrub = np.random.binomial(n=self.edibles["saplings"], p=outcompeted_by_shrubs)
        # if self.edibles["saplings"] - outcompeted_saplings_byScrub < 0: outcompeted_saplings_byScrub = self.edibles["saplings"]
        # self.edibles["saplings"] -= outcompeted_saplings_byScrub
        # self.habs_outcompeted_byScrub["saplings"] += outcompeted_saplings_byScrub

        # # young scrub being outcompeted by scrub/trees
        # outcompeted_by_trees = ((self.edibles["trees"]/(4000*(self.size_of_patch/10000)))*self.model.chance_youngScrubOutcompetedByTree) 
        # if outcompeted_by_trees > 1: outcompeted_by_trees = 1
        # outcompeted_youngScrub_byTrees = np.random.binomial(n=self.edibles["youngScrub"], p=outcompeted_by_trees)
        # self.edibles["youngScrub"] -= outcompeted_youngScrub_byTrees
        # self.habs_outcompeted_byTrees["youngScrub"] += outcompeted_youngScrub_byTrees
        # outcompeted_by_shrubs = ((self.edibles['scrub']/(4000*(self.size_of_patch/10000)))*self.model.chance_youngScrubOutcompetedByScrub)
        # if outcompeted_by_shrubs>1: outcompeted_by_shrubs=1
        # outcompeted_youngScrub_byScrub = np.random.binomial(n=self.edibles["youngScrub"], p=outcompeted_by_shrubs)
        # self.edibles["youngScrub"] -= outcompeted_youngScrub_byScrub
        # self.habs_outcompeted_byScrub["youngScrub"] += outcompeted_youngScrub_byScrub


        # reassess habitat condition
        if self.edibles["trees"] < 750*(self.size_of_patch/10000) and self.edibles["scrub"] < 750*(self.size_of_patch/10000) and self.edibles["grass"] >= 50*(self.size_of_patch/10000):
            self.condition = "grassland"
        elif self.edibles["trees"] < 750*(self.size_of_patch/10000) and self.edibles["scrub"] >= 750*(self.size_of_patch/10000):
            self.condition = "thorny_scrubland"
        elif self.edibles["trees"] >= 750*(self.size_of_patch/10000):
            self.condition = "woodland" 
        elif self.edibles["trees"] < 750*(self.size_of_patch/10000) and self.edibles["scrub"] < 750*(self.size_of_patch/10000) and self.edibles["bare_ground"] > 50*(self.size_of_patch/10000):
            self.condition = "bare_ground"
        


#### ---- The Herbivores --- #### 

class roe_deer_agent(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs, field_id, energy):
        super().__init__(unique_id, model, geometry, crs)
        self.field_id = field_id
        self.count_eaten = defaultdict(int)
        self.energy = energy

    def step(self):
        living = True
        # move & reduce energy
        browser_move(self, FieldAgent)
        self.energy -= 1
        # eat
        habitat_patch = self.model.space.get_region_by_id(self.field_id)
        self.energy += eat_habitats(self, habitat_patch, my_dietary_preference="browser", gain_from_saplings = self.model.roe_deer_gain_from_saplings, gain_from_trees=self.model.roe_deer_gain_from_trees, gain_from_scrub=self.model.roe_deer_gain_from_scrub, gain_from_young_scrub=self.model.roe_deer_gain_from_young_scrub, gain_from_grass=self.model.roe_deer_gain_from_grass)
        # if roe deer's energy is less than 0, die 
        if self.energy <= 0:
            self.model.space.remove_herbivore_agent(self)
            self.model.schedule.remove(self)
            living = False
        # I can reproduce in May & June (years run March-March)
        if living and (random.random() < self.model.roe_deer_reproduce/np.log10(self.model.schedule.get_breed_count(roe_deer_agent)+ 1)) and (3 <= self.model.get_month() < 5):
            # Create a new deer and divide energy:
            self.energy = np.random.uniform(0, self.energy)
            fawn = roe_deer_agent(uuid.uuid4().int, self.model, crs=self.crs, geometry=self.geometry, field_id=self.field_id, energy=self.energy)
            self.model.space.add_herbivore_agent(fawn, field_id=self.field_id)
            self.model.schedule.add(fawn)



class exmoor_pony_agent(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs, field_id, energy):
        super().__init__(unique_id, model, geometry, crs)
        self.field_id = field_id
        self.count_eaten = defaultdict(int)
        self.energy = energy

    def step(self):
        # move & reduce energy
        grazer_move(self, FieldAgent)
        self.energy -= 1
        # eat
        habitat_patch = self.model.space.get_region_by_id(self.field_id)
        self.energy += eat_habitats(self, habitat_patch, my_dietary_preference="grazer", gain_from_saplings = self.model.ponies_gain_from_saplings, gain_from_trees=self.model.ponies_gain_from_trees, gain_from_scrub=self.model.ponies_gain_from_scrub, gain_from_young_scrub=self.model.ponies_gain_from_young_scrub, gain_from_grass=self.model.ponies_gain_from_grass)
        # if energy is less than 0, die 
        if self.energy <= 0:
            self.model.space.remove_herbivore_agent(self)
            self.model.schedule.remove(self)
     


class longhorn_cattle_agent(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs, field_id, energy):
        super().__init__(unique_id, model, geometry, crs)
        self.field_id = field_id
        self.count_eaten = defaultdict(int)
        self.energy = energy

    def step(self):
        living = True
        # move & reduce energy
        grazer_move(self, FieldAgent)
        self.energy -= 1
        # eat
        habitat_patch = self.model.space.get_region_by_id(self.field_id)
        self.energy += eat_habitats(self, habitat_patch, my_dietary_preference="grazer", gain_from_saplings = self.model.cows_gain_from_saplings, gain_from_trees=self.model.cows_gain_from_trees, gain_from_scrub=self.model.cows_gain_from_scrub, gain_from_young_scrub=self.model.cows_gain_from_young_scrub, gain_from_grass=self.model.cows_gain_from_grass)
        # if energy is less than 0, die 
        if self.energy <= 0:
            self.model.space.remove_herbivore_agent(self)
            self.model.schedule.remove(self)
            living = False
        # I can reproduce in April, May, June (years run March-March)
        if living and (random.random() < self.model.cattle_reproduce/np.log10(self.model.schedule.get_breed_count(longhorn_cattle_agent)+ 1)) and (2 <= self.model.get_month() < 5):
            # Create a new roe deer and divide energy:
            self.energy = np.random.uniform(0, self.energy)
            calf = longhorn_cattle_agent(uuid.uuid4().int, self.model, crs=self.crs, geometry=self.geometry, field_id=self.field_id, energy=self.energy)
            self.model.space.add_herbivore_agent(calf, field_id=self.field_id)
            self.model.schedule.add(calf)



class fallow_deer_agent(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs, field_id, energy):
        super().__init__(unique_id, model, geometry, crs)
        self.field_id = field_id
        self.count_eaten = defaultdict(int)
        self.energy = energy

    def step(self):
        living = True
        # move & reduce energy
        mixed_diet_move(self, FieldAgent)
        self.energy -= 1
        # eat
        habitat_patch = self.model.space.get_region_by_id(self.field_id)
        self.energy += eat_habitats(self, habitat_patch, my_dietary_preference="intermediate_feeder", gain_from_saplings = self.model.fallow_deer_gain_from_saplings, gain_from_trees=self.model.fallow_deer_gain_from_trees, gain_from_scrub=self.model.fallow_deer_gain_from_scrub, gain_from_young_scrub=self.model.fallow_deer_gain_from_young_scrub, gain_from_grass=self.model.fallow_deer_gain_from_grass)
        # if energy is less than 0, die 
        if self.energy <= 0:
            self.model.space.remove_herbivore_agent(self)
            self.model.schedule.remove(self)
            living = False
        # I can reproduce in May and June (years run March-March)
        # if living and (random.random() < self.model.fallow_deer_reproduce) and (3 <= self.model.get_month() < 5):
        if living and (random.random() < self.model.fallow_deer_reproduce/np.log10(self.model.schedule.get_breed_count(fallow_deer_agent)+ 1)) and (3 <= self.model.get_month() < 5):
            # Create a new deer and divide energy:
            self.energy = np.random.uniform(0, self.energy)
            fawn = fallow_deer_agent(uuid.uuid4().int, self.model, crs=self.crs, geometry=self.geometry, field_id=self.field_id, energy=self.energy)
            self.model.space.add_herbivore_agent(fawn, field_id=self.field_id)
            self.model.schedule.add(fawn)



class red_deer_agent(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs, field_id, energy):
        super().__init__(unique_id, model, geometry, crs)
        self.field_id = field_id
        self.count_eaten = defaultdict(int)
        self.energy = energy

    def step(self):
        living = True
        # move & reduce energy
        mixed_diet_move(self, FieldAgent)
        self.energy -= 1
        # eat
        habitat_patch = self.model.space.get_region_by_id(self.field_id)
        self.energy += eat_habitats(self, habitat_patch, my_dietary_preference="intermediate_feeder", gain_from_saplings = self.model.red_deer_gain_from_saplings, gain_from_trees=self.model.red_deer_gain_from_trees, gain_from_scrub=self.model.red_deer_gain_from_scrub, gain_from_young_scrub=self.model.red_deer_gain_from_young_scrub, gain_from_grass=self.model.red_deer_gain_from_grass)
        # if energy is less than 0, die 
        if self.energy <= 0:
            self.model.space.remove_herbivore_agent(self)
            self.model.schedule.remove(self)
            living = False
        # I can reproduce in May and June (years run March-March)
        if living and (random.random() < self.model.red_deer_reproduce/np.log10(self.model.schedule.get_breed_count(red_deer_agent)+ 1)) and (3 <= self.model.get_month() < 5):
        # if living and (random.random() < self.model.red_deer_reproduce) and (3 <= self.model.get_month() < 5):

            # Create a new roe deer and divide energy:
            self.energy = np.random.uniform(0, self.energy)
            fawn = red_deer_agent(uuid.uuid4().int, self.model, crs=self.crs, geometry=self.geometry, field_id=self.field_id, energy=self.energy)
            self.model.space.add_herbivore_agent(fawn, field_id=self.field_id)
            self.model.schedule.add(fawn)




class tamworth_pig_agent(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs, field_id, energy, condition):
        super().__init__(unique_id, model, geometry, crs)
        self.field_id = field_id
        self.count_eaten = defaultdict(int)
        self.energy = energy
        self.pregnancy_timer = None
        self.condition = condition

    def step(self):
        living = True
        # move & reduce energy
        random_move(self, FieldAgent)
        self.energy -= 1
        # eat
        habitat_patch = self.model.space.get_region_by_id(self.field_id)
        self.energy += eat_habitats(self, habitat_patch, my_dietary_preference="random", gain_from_saplings = self.model.tamworth_pig_gain_from_saplings, gain_from_trees=self.model.tamworth_pig_gain_from_trees, gain_from_scrub=self.model.tamworth_pig_gain_from_scrub, gain_from_young_scrub=self.model.tamworth_pig_gain_from_young_scrub, gain_from_grass=self.model.tamworth_pig_gain_from_grass)
        # if energy is less than 0, die 
        if self.energy <= 0:
            self.model.space.remove_herbivore_agent(self)
            self.model.schedule.remove(self)
            living = False

        # I can reproduce a few months after boar were introduced 
        if self.pregnancy_timer != None: 
            self.pregnancy_timer = self.pregnancy_timer - 1
            if self.pregnancy_timer == 0 and living:
                self.giveBirth()
                self.pregnancy_timer = None

        # are there boars here? 
        all_pigs = self.model.schedule.agents_by_breed[tamworth_pig_agent].items()
        boars_here = [i for (k, i) in all_pigs if i.condition == "boar"]
        # if there are, set the timer so other pigs reproduce in a few months
        if len(boars_here) > 0 and self.condition == "sow" and living and self.pregnancy_timer == None and (random.random() < self.model.tamworth_pig_reproduce/np.log10(self.model.schedule.get_breed_count(tamworth_pig_agent)+ 1)):
            self.pregnancy_timer = random.randint(2,4)
            # divide my energy
            self.energy = np.random.uniform(0, self.energy)


    def giveBirth(self):
        # Pick a number of piglets to have
        number_piglets = np.random.binomial(n=10, p=0.5)
        for _ in range(number_piglets):
            piglet = tamworth_pig_agent(uuid.uuid4().int, self.model, crs=self.crs, geometry=self.geometry, field_id=self.field_id, energy=self.energy, condition="piglet")
            self.model.space.add_herbivore_agent(piglet, field_id=self.field_id)
            self.model.schedule.add(piglet)



#### ----- Future potential reintroduced species ----- ####

class reindeer_agent(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs, field_id, energy):
        super().__init__(unique_id, model, geometry, crs)
        self.field_id = field_id
        self.count_eaten = defaultdict(int)
        self.energy = energy

    def step(self):
        living = True
        # move & reduce energy
        mixed_diet_move(self, FieldAgent)
        self.energy -= 1
        # eat
        habitat_patch = self.model.space.get_region_by_id(self.field_id)
        self.energy += eat_habitats(self, habitat_patch, my_dietary_preference="intermediate_feeder", gain_from_saplings = self.model.reindeer_gain_from_saplings, gain_from_trees=self.model.reindeer_gain_from_trees, gain_from_scrub=self.model.reindeer_gain_from_scrub, gain_from_young_scrub=self.model.reindeer_gain_from_young_scrub, gain_from_grass=self.model.reindeer_gain_from_grass)
        # if energy is less than 0, die 
        if self.energy <= 0:
            self.model.space.remove_herbivore_agent(self)
            self.model.schedule.remove(self)
            living = False
        # I can reproduce in April, May and June (years run March-March)
        if living and (random.random() < self.model.reindeer_reproduce/np.log10(self.model.schedule.get_breed_count(reindeer_agent)+ 1)) and (2 <= self.model.get_month() < 5):
            # Create a new roe deer and divide energy:
            self.energy = np.random.uniform(0, self.energy)
            fawn = reindeer_agent(uuid.uuid4().int, self.model, crs=self.crs, geometry=self.geometry, field_id=self.field_id, energy=self.energy)
            self.model.space.add_herbivore_agent(fawn, field_id=self.field_id)
            self.model.schedule.add(fawn)



class european_elk_agent(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs, field_id, energy):
        super().__init__(unique_id, model, geometry, crs)
        self.field_id = field_id
        self.count_eaten = defaultdict(int)
        self.energy = energy

    def step(self):
        living = True
        # move & reduce energy
        browser_move(self, FieldAgent)
        self.energy -= 1
        # eat
        habitat_patch = self.model.space.get_region_by_id(self.field_id)
        self.energy += eat_habitats(self, habitat_patch, my_dietary_preference="browser", gain_from_saplings = self.model.european_elk_gain_from_saplings, gain_from_trees=self.model.european_elk_gain_from_trees, gain_from_scrub=self.model.european_elk_gain_from_scrub, gain_from_young_scrub=self.model.european_elk_gain_from_young_scrub, gain_from_grass=self.model.european_elk_gain_from_grass)
        # if energy is less than 0, die 
        if self.energy <= 0:
            self.model.space.remove_herbivore_agent(self)
            self.model.schedule.remove(self)
            living = False
        # I can reproduce in April, May and June (years run March-March)
        if living and (random.random() < self.model.european_elk_reproduce/np.log10(self.model.schedule.get_breed_count(european_elk_agent)+ 1)) and (2 <= self.model.get_month() < 5):
            # Create a new roe deer and divide energy:
            self.energy = np.random.uniform(0, self.energy)
            fawn = european_elk_agent(uuid.uuid4().int, self.model, crs=self.crs, geometry=self.geometry, field_id=self.field_id, energy=self.energy)
            self.model.space.add_herbivore_agent(fawn, field_id=self.field_id)
            self.model.schedule.add(fawn)


class european_bison_agent(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs, field_id, energy):
        super().__init__(unique_id, model, geometry, crs)
        self.field_id = field_id
        self.count_eaten = defaultdict(int)
        self.energy = energy

    def step(self):
        living = True
        # move & reduce energy
        mixed_diet_move(self, FieldAgent)
        self.energy -= 1
        # eat
        habitat_patch = self.model.space.get_region_by_id(self.field_id)
        self.energy += eat_habitats(self, habitat_patch, my_dietary_preference="intermediate_feeder", gain_from_saplings = self.model.european_bison_gain_from_saplings, gain_from_trees=self.model.european_bison_gain_from_trees, gain_from_scrub=self.model.european_bison_gain_from_scrub, gain_from_young_scrub=self.model.european_bison_gain_from_young_scrub, gain_from_grass=self.model.european_bison_gain_from_grass)
        # if energy is less than 0, die 
        if self.energy <= 0:
            self.model.space.remove_herbivore_agent(self)
            self.model.schedule.remove(self)
            living = False
        # I can reproduce in April, May and June (years run March-March)
        if living and (random.random() < self.model.european_bison_reproduce/np.log10(self.model.schedule.get_breed_count(european_bison_agent)+ 1)) and (2 <= self.model.get_month() < 5):
            # Create a new roe deer and divide energy:
            self.energy = np.random.uniform(0, self.energy)
            fawn = european_bison_agent(uuid.uuid4().int, self.model, crs=self.crs, geometry=self.geometry, field_id=self.field_id, energy=self.energy)
            self.model.space.add_herbivore_agent(fawn, field_id=self.field_id)
            self.model.schedule.add(fawn)
