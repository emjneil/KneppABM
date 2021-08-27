# run experiments on the accepted parameter sets 
from run_model import run_all_models
from KneppModel_ABM import roeDeer_agent, habitatAgent, exmoorPony, redDeer, fallowDeer, longhornCattle, tamworthPigs
from mesa import Model
from mesa.datacollection import DataCollector
import numpy as np
import random
import pandas as pd
from schedule import RandomActivationByBreed
from mesa.space import MultiGrid 



                                # # # # ------ Define the model ------ # # # # 

class KneppModel_counterfactual(Model):
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
        # run till 2021 with no large herbivore reintroductions
        if self.schedule.time == 50:
            self.running = False



    def run_model(self): 
        # run it for 184 steps
        for i in range(50):
            self.step()
        results = self.datacollector.get_model_vars_dataframe()
        return results
  



def run_counterfactual():
    number_simulations, final_results, accepted_parameters = run_all_models()
    # run the counterfactual: what would have happened if rewilding hadn't occurred? 
    final_results_list = []
    run_number = 0

    # take the accepted parameters, and go row by row, running the model
    for _, row in accepted_parameters.iterrows():
        chance_reproduceSapling = row[1]
        chance_reproduceYoungScrub =  row[2]
        chance_regrowGrass =  row[3]
        chance_saplingBecomingTree =  row[4]
        chance_youngScrubMatures =  row[5]
        chance_scrubOutcompetedByTree =  row[6]
        chance_grassOutcompetedByTree =  row[7]
        chance_grassOutcompetedByScrub = row[8]
        chance_saplingOutcompetedByTree =  row[9]
        chance_saplingOutcompetedByScrub =  row[10]
        chance_youngScrubOutcompetedByScrub =  row[11]
        chance_youngScrubOutcompetedByTree =  row[12]
        initial_roeDeer = int(row[13])
        initial_grassland =  int(row[14])
        initial_woodland =  int(row[15])
        initial_scrubland =  int(row[16])
        roeDeer_reproduce =  row[17]
        roeDeer_gain_from_grass =  row[18]
        roeDeer_gain_from_Trees =  row[19]
        roeDeer_gain_from_Scrub =  row[20]
        roeDeer_gain_from_Saplings =  row[21]
        roeDeer_gain_from_YoungScrub =  row[22]
        roeDeer_impactGrass =  row[23]
        roeDeer_saplingsEaten =  row[24]
        roeDeer_youngScrubEaten =  row[25]
        roeDeer_treesEaten =  row[26]
        roeDeer_scrubEaten =  row[27]
        ponies_gain_from_grass =  row[28]
        ponies_gain_from_Trees =  row[29]
        ponies_gain_from_Scrub =  row[30]
        ponies_gain_from_Saplings =  row[31]
        ponies_gain_from_YoungScrub =  row[32]
        ponies_impactGrass =  row[33]
        ponies_saplingsEaten =  row[34]
        ponies_youngScrubEaten =  row[35]
        ponies_treesEaten =  row[36]
        ponies_scrubEaten =  row[37]
        cows_reproduce =  row[38]
        cows_gain_from_grass =  row[39]
        cows_gain_from_Trees =  row[40]
        cows_gain_from_Scrub =  row[41]
        cows_gain_from_Saplings =  row[42]
        cows_gain_from_YoungScrub =  row[43]
        cows_impactGrass =  row[44]
        cows_saplingsEaten =  row[45]
        cows_youngScrubEaten =  row[46]
        cows_treesEaten =  row[47]
        cows_scrubEaten =  row[48]
        fallowDeer_reproduce =  row[49]
        fallowDeer_gain_from_grass =  row[50]
        fallowDeer_gain_from_Trees =  row[51]
        fallowDeer_gain_from_Scrub =  row[52]
        fallowDeer_gain_from_Saplings =  row[53]
        fallowDeer_gain_from_YoungScrub =  row[54]
        fallowDeer_impactGrass =  row[55]
        fallowDeer_saplingsEaten =  row[56]
        fallowDeer_youngScrubEaten =  row[57]
        fallowDeer_treesEaten =  row[58]
        fallowDeer_scrubEaten =  row[59]
        redDeer_reproduce =  row[60]
        redDeer_gain_from_grass =  row[61]
        redDeer_gain_from_Trees =  row[62]
        redDeer_gain_from_Scrub =  row[63]
        redDeer_gain_from_Saplings =  row[64]
        redDeer_gain_from_YoungScrub =  row[65]
        redDeer_impactGrass =  row[66]
        redDeer_saplingsEaten =  row[67]
        redDeer_youngScrubEaten =  row[68]
        redDeer_treesEaten =  row[69]
        redDeer_scrubEaten =  row[70]
        pigs_reproduce =  row[71]
        pigs_gain_from_grass =  row[72]
        pigs_gain_from_Saplings =  row[73]
        pigs_gain_from_YoungScrub =  row[74]
        pigs_impactGrass =  row[75]
        pigs_saplingsEaten =  row[76]
        pigs_youngScrubEaten =  row[77]


        model = KneppModel_counterfactual(
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
            width = 50, height = 36)
        model.run_model()

        run_number +=1
        print(run_number)    

        results = model.datacollector.get_model_vars_dataframe()
        results['run_number'] = run_number
        final_results_list.append(results)
    
    # append to dataframe
    counterfactual = pd.concat(final_results_list)
    counterfactual['accepted?'] = "noReintro"

    counterfactual.to_excel("noReintro.xlsx")

    # return the number of simulations, final results, forecasting, and counterfactual 
    return number_simulations, final_results, counterfactual, accepted_parameters
