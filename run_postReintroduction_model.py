from run_preReintroduction_model import run_model
from KneppModel_ABM import KneppModel
import numpy as np
import random
import pandas as pd
import timeit

# # # Run the post-reintroduction model (2009-2020)

# time the program
start = timeit.default_timer()

def run_postreintro_model():
    accepted_parameters, all_accepted_runs, accepted_year, variables = run_model()
    all_accepted_parameters = pd.merge(accepted_parameters, accepted_year)

    # make list of variables
    final_results_list = []
    final_parameters = []
    run_number = 0
    # run the model for 48 months, 10 times    
    for index, row in all_accepted_parameters.iterrows():
        # keep track of the runs
        run_number += 1
        # make the final conditions of the pre-reintro model the initial conditions
        initial_roeDeer = int(row["Roe deer"])
        initial_grassland = row["Grassland"]
        initial_woodland = row["Woodland"]
        initial_scrubland = row["Thorny Scrub"]
        initial_ponies = 23
        initial_cows = 53
        initial_fallowDeer = 0
        initial_redDeer = 0
        initial_pigs = 20
        # loop through the other parameter sets
        chance_reproduceSapling = row["chance_reproduceSapling"]
        chance_reproduceYoungScrub = row["chance_reproduceYoungScrub"]
        chance_regrowGrass = row["chance_regrowGrass"]
        chance_saplingBecomingTree = row["chance_saplingBecomingTree"]
        chance_youngScrubMatures = row["chance_youngScrubMatures"]
        chance_scrubOutcompetedByTree = row["chance_scrubOutcompetedByTree"]
        chance_grassOutcompetedByTreeScrub = row["chance_grassOutcompetedByTreeScrub"]
        chance_saplingOutcompetedByTree = row["chance_saplingOutcompetedByTree"]
        chance_saplingOutcompetedByScrub = row["chance_saplingOutcompetedByScrub"]
        chance_youngScrubOutcompetedByScrub = row["chance_youngScrubOutcompetedByScrub"]
        chance_youngScrubOutcompetedByTree = row["chance_youngScrubOutcompetedByTree"]
        # roe deer
        roeDeer_reproduce = row["roeDeer_reproduce"]
        roeDeer_gain_from_grass = row["roeDeer_gain_from_grass"]
        roeDeer_gain_from_Trees = row["roeDeer_gain_from_Trees"]
        roeDeer_gain_from_Scrub = row["roeDeer_gain_from_Scrub"]
        roeDeer_gain_from_Saplings = row["roeDeer_gain_from_Saplings"]
        roeDeer_gain_from_YoungScrub = row["roeDeer_gain_from_YoungScrub"]
        roeDeer_impactGrass = row["roeDeer_impactGrass"]
        roeDeer_saplingsEaten = row["roeDeer_saplingsEaten"]
        roeDeer_youngScrubEaten = row["roeDeer_youngScrubEaten"]
        roeDeer_treesEaten = row["roeDeer_treesEaten"]
        roeDeer_scrubEaten = row["roeDeer_scrubEaten"]
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


        # parameters = generate_parameters()
        parameters_used = [
            run_number,
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
            pigs_impactGrass, pigs_saplingsEaten, pigs_youngScrubEaten 
            ]

        # remember parameters used 
        final_parameters.append(parameters_used)
        # call the model
        model_2009 = KneppModel(
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
            width = 10, height = 10)
        


        # # # Run it for 132 months (March 2009-2020), stopping it whenever a large herbivore is culled # # #
        

                                    # # # # # # # 2009 until 2015 # # # # # # #


        # March 2009-Feb 2010        
        model_2009.run_model(12)
        results_2009 = model_2009.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_2009["Time"] += 50
        final_results_list.append(results_2009)
        
        
        # March 2010 -Feb 2011: force new culled values and run the model again
        initial_ponies = 13
        initial_cows = 77
        initial_fallowDeer = 42
        initial_pigs = 17
        initial_roeDeer = (results_2009["Roe deer"][0])
        initial_grassland = (results_2009["Grassland"][0])
        initial_woodland = (results_2009["Woodland"][0])
        initial_scrubland = (results_2009["Thorny Scrub"][0])
        # call the model
        model_2010 = KneppModel(
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
            width = 10, height = 10)
        model_2010.run_model(12)
        results_2010 = model_2010.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_2010["Time"] += 62
        final_results_list.append(results_2010)


        # March 2011 - Feb 2012: force new culled values and run the model again
        initial_ponies = 15
        initial_cows = 92
        initial_fallowDeer = 81
        initial_pigs = 22
        initial_roeDeer = (results_2010["Roe deer"][0])
        initial_grassland = (results_2010["Grassland"][0])
        initial_woodland = (results_2010["Woodland"][0])
        initial_scrubland = (results_2010["Thorny Scrub"][0])

        # call the model
        model_2011 = KneppModel(
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
            width = 10, height = 10)
        model_2011.run_model(12)
        results_2011 = model_2011.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_2011["Time"] += 74
        final_results_list.append(results_2011)



        # March 2012 - Feb 2013: force new culled values and run the model again
        initial_ponies = 17
        initial_cows = 116
        initial_fallowDeer = 100
        initial_pigs = 33
        initial_roeDeer = (results_2011["Roe deer"][0])
        initial_grassland = (results_2011["Grassland"][0])
        initial_woodland = (results_2011["Woodland"][0])
        initial_scrubland = (results_2011["Thorny Scrub"][0])
        # call the model
        model_2012 = KneppModel(
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
            width = 10, height = 10)
        model_2012.run_model(12)
        results_2012 = model_2012.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_2012["Time"] += 86
        final_results_list.append(results_2012)



        # March 2013 - Feb 2014: force new culled values and run the model again
        initial_cows = 129
        initial_fallowDeer = 100
        initial_redDeer = 13
        initial_pigs = 6
        initial_ponies = 10
        initial_roeDeer = (results_2012["Roe deer"][0])
        initial_grassland = (results_2012["Grassland"][0])
        initial_woodland = (results_2012["Woodland"][0])
        initial_scrubland = (results_2012["Thorny Scrub"][0])
        # call the model
        model_2013 = KneppModel(
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
            width = 10, height = 10)
        model_2013.run_model(12)
        results_2013 = model_2013.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_2013["Time"] += 98
        final_results_list.append(results_2013)
            

        # March 2014 - Feb 2015: force new culled values and run the model again
        initial_cows = 264
        initial_fallowDeer = 100
        initial_redDeer = 13
        initial_pigs = 18
        initial_roeDeer = (results_2013["Roe deer"][0])
        initial_grassland = (results_2013["Grassland"][0])
        initial_woodland = (results_2013["Woodland"][0])
        initial_scrubland = (results_2013["Thorny Scrub"][0])
        # call the model
        model_2014 = KneppModel(
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
            width = 10, height = 10)
        model_2014.run_model(12)
        results_2014 = model_2014.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_2014["Time"] += 110
        final_results_list.append(results_2014)



    
                                        # # # # # # # 2015 # # # # # # #


    # March 2015
        initial_cows = 107
        initial_fallowDeer = 100
        initial_redDeer = 13
        initial_pigs = 18
        initial_roeDeer = (results_2014["Roe deer"][0])
        initial_grassland = (results_2014["Grassland"][0])
        initial_woodland = (results_2014["Woodland"][0])
        initial_scrubland = (results_2014["Thorny Scrub"][0])
        # call the model
        model_March2015 = KneppModel(
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
            width = 10, height = 10)
        model_March2015.step()
        results_March2015 = model_March2015.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_March2015["Time"] += 122
        final_results_list.append(results_March2015)



    # April 2015: one pig culled, 5 born
        initial_pigs = (results_March2015["Tamworth pigs"][0]) - 1
        initial_cows = (results_March2015["Longhorn cattle"][0])
        initial_fallowDeer = (results_March2015["Fallow deer"][0])
        initial_redDeer = (results_March2015["Red deer"][0])
        initial_roeDeer = (results_March2015["Roe deer"][0])
        initial_grassland = (results_March2015["Grassland"][0])
        initial_woodland = (results_March2015["Woodland"][0])
        initial_scrubland = (results_March2015["Thorny Scrub"][0])
        model_Apr2015 = KneppModel(
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
            width = 10, height = 10)
        model_Apr2015.step()
        results_Apr2015 = model_Apr2015.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Apr2015["Time"] += 123
        final_results_list.append(results_Apr2015)


    # May 2015: 8 pigs culled
        initial_pigs = (results_Apr2015["Tamworth pigs"][0]) - 8
        initial_cows = (results_Apr2015["Longhorn cattle"][0])
        initial_fallowDeer = (results_Apr2015["Fallow deer"][0])
        initial_redDeer = (results_Apr2015["Red deer"][0])
        initial_roeDeer = (results_Apr2015["Roe deer"][0])
        initial_grassland = (results_Apr2015["Grassland"][0])
        initial_woodland = (results_Apr2015["Woodland"][0])
        initial_scrubland = (results_Apr2015["Thorny Scrub"][0])
        
        # call the model
        model_May2015 = KneppModel(
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
            width = 10, height = 10)
        model_May2015.step()
        results_May2015 = model_May2015.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_May2015["Time"] += 124
        final_results_list.append(results_May2015)



    # June 2015: 5 cows culled
        initial_cows = (results_May2015["Longhorn cattle"][0]) - 5
        initial_pigs = (results_May2015["Tamworth pigs"][0])
        initial_fallowDeer = (results_May2015["Fallow deer"][0])
        initial_redDeer = (results_May2015["Red deer"][0])
        initial_roeDeer = (results_May2015["Roe deer"][0])
        initial_grassland = (results_May2015["Grassland"][0])
        initial_woodland = (results_May2015["Woodland"][0])
        initial_scrubland = (results_May2015["Thorny Scrub"][0])
        # call the model
        model_June2015 = KneppModel(
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
            width = 10, height = 10)
        model_June2015.step()
        results_June2015 = model_June2015.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_June2015["Time"] += 125
        final_results_list.append(results_June2015)


    # July & Aug 2015: 2 fallow deer culled in Aug; 
        initial_fallowDeer = (results_June2015["Fallow deer"][0]) - 2
        initial_cows = (results_June2015["Longhorn cattle"][0])
        initial_pigs = (results_June2015["Tamworth pigs"][0])
        initial_redDeer = (results_June2015["Red deer"][0])
        initial_roeDeer = (results_June2015["Roe deer"][0])
        initial_grassland = (results_June2015["Grassland"][0])
        initial_woodland = (results_June2015["Woodland"][0])
        initial_scrubland = (results_June2015["Thorny Scrub"][0])
        # call the model
        model_JulyAug2015 = KneppModel(
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
            width = 10, height = 10)
        for _ in range(2):
            model_JulyAug2015.step()
        results_JulyAug2015 = model_JulyAug2015.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_JulyAug2015["Time"] += 126
        final_results_list.append(results_JulyAug2015)


   # Sept 2015: 2 male fallow deer culled; 2 cattle culled and 3 bulls added
        initial_fallowDeer = (results_JulyAug2015["Fallow deer"][0]) - 2
        initial_cows = (results_JulyAug2015["Longhorn cattle"][0]) + 1 # 2 culled, 3 added
        initial_pigs = (results_JulyAug2015["Tamworth pigs"][0])
        initial_redDeer = (results_JulyAug2015["Red deer"][0])
        initial_roeDeer = (results_JulyAug2015["Roe deer"][0])
        initial_grassland = (results_JulyAug2015["Grassland"][0])
        initial_woodland = (results_JulyAug2015["Woodland"][0])
        initial_scrubland = (results_JulyAug2015["Thorny Scrub"][0])
        model_Sept2015 = KneppModel(
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
            width = 10, height = 10)
        model_Sept2015.step()
        results_Sept2015 = model_Sept2015.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Sept2015["Time"] += 128
        final_results_list.append(results_Sept2015)



   # Oct 2015: 2 female and 1 male fallow deer culled; 38 female cows and 1 bull removed
        initial_fallowDeer = (results_Sept2015["Fallow deer"][0]) - 3
        initial_cows = (results_Sept2015["Longhorn cattle"][0]) - 39 
        initial_pigs = (results_Sept2015["Tamworth pigs"][0])
        initial_redDeer = (results_Sept2015["Red deer"][0])
        initial_roeDeer = (results_Sept2015["Roe deer"][0])
        initial_grassland = (results_Sept2015["Grassland"][0])
        initial_woodland = (results_Sept2015["Woodland"][0])
        initial_scrubland = (results_Sept2015["Thorny Scrub"][0])
        model_Oct2015 = KneppModel(
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
            width = 10, height = 10)
        model_Oct2015.step()
        results_Oct2015 = model_Oct2015.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Oct2015["Time"] += 129
        final_results_list.append(results_Oct2015)



   # Nov 2015: 5 female and 2 male fallow deer culled
        initial_fallowDeer = (results_Oct2015["Fallow deer"][0]) - 7
        initial_cows = (results_Oct2015["Longhorn cattle"][0])
        initial_pigs = (results_Oct2015["Tamworth pigs"][0])
        initial_redDeer = (results_Oct2015["Red deer"][0])
        initial_roeDeer = (results_Oct2015["Roe deer"][0])
        initial_grassland = (results_Oct2015["Grassland"][0])
        initial_woodland = (results_Oct2015["Woodland"][0])
        initial_scrubland = (results_Oct2015["Thorny Scrub"][0])
        # call the model
        model_Nov2015 = KneppModel(
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
            width = 10, height = 10)
        model_Nov2015.step()
        results_Nov2015 = model_Nov2015.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Nov2015["Time"] += 130
        final_results_list.append(results_Nov2015)



  # Dec 2015: 4 female and 2 male fallow deer culled; 3 female cows and 2 bulls removed; 
        initial_fallowDeer = (results_Nov2015["Fallow deer"][0]) - 6
        initial_cows = (results_Nov2015["Longhorn cattle"][0]) - 5
        initial_pigs = (results_Nov2015["Tamworth pigs"][0])
        initial_redDeer = (results_Nov2015["Red deer"][0])
        initial_roeDeer = (results_Nov2015["Roe deer"][0])
        initial_grassland = (results_Nov2015["Grassland"][0])
        initial_woodland = (results_Nov2015["Woodland"][0])
        initial_scrubland = (results_Nov2015["Thorny Scrub"][0])
        # call the model
        model_Dec2015 = KneppModel(
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
            width = 10, height = 10)
        model_Dec2015.step()
        results_Dec2015 = model_Dec2015.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Dec2015["Time"] += 131
        final_results_list.append(results_Dec2015)


  # Jan 2016: 6 female and 1 male fallow deer culled; 4 female pigs culled and 1 boar added 
        initial_fallowDeer = (results_Dec2015["Fallow deer"][0]) - 7
        initial_pigs = (results_Dec2015["Tamworth pigs"][0]) - 3 # 4 removed, 1 boar added
        initial_cows = (results_Dec2015["Longhorn cattle"][0])
        initial_redDeer = (results_Dec2015["Red deer"][0])
        initial_roeDeer = (results_Dec2015["Roe deer"][0])
        initial_grassland = (results_Dec2015["Grassland"][0])
        initial_woodland = (results_Dec2015["Woodland"][0])
        initial_scrubland = (results_Dec2015["Thorny Scrub"][0])
        model_Jan2016 = KneppModel(
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
            width = 10, height = 10)
        model_Jan2016.step()
        results_Jan2016 = model_Jan2016.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Jan2016["Time"] += 132
        final_results_list.append(results_Jan2016)


 # Feb 2016: 10 female fallow deer culled; 2 female pigs culled
        initial_fallowDeer = (results_Jan2016["Fallow deer"][0]) - 10
        initial_pigs = (results_Jan2016["Tamworth pigs"][0]) - 2
        initial_cows = (results_Jan2016["Longhorn cattle"][0])
        initial_redDeer = (results_Jan2016["Red deer"][0])
        initial_roeDeer = (results_Jan2016["Roe deer"][0])
        initial_grassland = (results_Jan2016["Grassland"][0])
        initial_woodland = (results_Jan2016["Woodland"][0])
        initial_scrubland = (results_Jan2016["Thorny Scrub"][0])
        # call the model
        model_Feb2016 = KneppModel(
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
            width = 10, height = 10)
        model_Feb2016.step()
        results_Feb2016 = model_Feb2016.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Feb2016["Time"] += 133
        final_results_list.append(results_Feb2016)



                                        # # # # # # # 2016 # # # # # # #


 # March 2016: 1 Exmoor pony added; 3 pigs added and 4 culled
        initial_ponies = (results_Feb2016["Exmoor pony"][0]) + 1
        initial_cows = (results_Feb2016["Longhorn cattle"][0])
        initial_pigs = (results_Feb2016["Tamworth pigs"][0]) - 1 # 3 added and 4 culled
        initial_roeDeer = (results_Feb2016["Roe deer"][0])
        initial_grassland = (results_Feb2016["Grassland"][0])
        initial_woodland = (results_Feb2016["Woodland"][0])
        initial_scrubland = (results_Feb2016["Thorny Scrub"][0])
        initial_fallowDeer = (results_Feb2016["Fallow deer"][0])
        initial_redDeer = (results_Feb2016["Red deer"][0])
        # call the model
        model_March2016 = KneppModel(
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
            width = 10, height = 10)
        model_March2016.step()
        results_March2016 = model_March2016.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_March2016["Time"] += 134
        final_results_list.append(results_March2016)
    



 # April 2016: 1 cow added
        initial_ponies = (results_March2016["Exmoor pony"][0])
        initial_cows = (results_March2016["Longhorn cattle"][0]) + 1
        initial_pigs = (results_March2016["Tamworth pigs"][0])
        initial_fallowDeer = (results_March2016["Fallow deer"][0])
        initial_redDeer = (results_March2016["Red deer"][0])
        initial_roeDeer = (results_March2016["Roe deer"][0])
        initial_grassland = (results_March2016["Grassland"][0])
        initial_woodland = (results_March2016["Woodland"][0])
        initial_scrubland = (results_March2016["Thorny Scrub"][0])
        # call the model
        model_April2016 = KneppModel(
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
            width = 10, height = 10)
        model_April2016.step()
        results_April2016 = model_April2016.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_April2016["Time"] += 135
        final_results_list.append(results_April2016)



 # May 2016: 2 cows culled
        initial_ponies = (results_April2016["Exmoor pony"][0])
        initial_cows = (results_April2016["Longhorn cattle"][0]) - 2
        initial_pigs = (results_April2016["Tamworth pigs"][0])
        initial_fallowDeer = (results_April2016["Fallow deer"][0])
        initial_redDeer = (results_April2016["Red deer"][0])
        initial_roeDeer = (results_April2016["Roe deer"][0])
        initial_grassland = (results_April2016["Grassland"][0])
        initial_woodland = (results_April2016["Woodland"][0])
        initial_scrubland = (results_April2016["Thorny Scrub"][0])
        # call the model
        model_May2016 = KneppModel(
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
            width = 10, height = 10)
        model_May2016.step()
        results_May2016 = model_May2016.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_May2016["Time"] += 136
        final_results_list.append(results_May2016)



 # June 2016: 30 cows culled, 4 added (stock supplement)
        initial_ponies = (results_May2016["Exmoor pony"][0])
        initial_cows = (results_May2016["Longhorn cattle"][0]) - 24
        initial_pigs = (results_May2016["Tamworth pigs"][0])
        initial_fallowDeer = (results_May2016["Fallow deer"][0])
        initial_redDeer = (results_May2016["Red deer"][0])
        initial_roeDeer = (results_May2016["Roe deer"][0])
        initial_grassland = (results_May2016["Grassland"][0])
        initial_woodland = (results_May2016["Woodland"][0])
        initial_scrubland = (results_May2016["Thorny Scrub"][0])
        # call the model
        model_June2016 = KneppModel(
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
            width = 10, height = 10)
        model_June2016.step()
        results_June2016 = model_June2016.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_June2016["Time"] += 137
        final_results_list.append(results_June2016)



 # July 2016: 2 cows removed: 1 male, 1 female
        initial_ponies = (results_June2016["Exmoor pony"][0])
        initial_cows = (results_June2016["Longhorn cattle"][0]) - 2
        initial_pigs = (results_June2016["Tamworth pigs"][0])
        initial_fallowDeer = (results_June2016["Fallow deer"][0])
        initial_redDeer = (results_June2016["Red deer"][0])
        initial_roeDeer = (results_June2016["Roe deer"][0])
        initial_grassland = (results_June2016["Grassland"][0])
        initial_woodland = (results_June2016["Woodland"][0])
        initial_scrubland = (results_June2016["Thorny Scrub"][0])
        # call the model
        model_July2016 = KneppModel(
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
            width = 10, height = 10)
        model_July2016.step()
        results_July2016 = model_July2016.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_July2016["Time"] += 138
        final_results_list.append(results_July2016)




 # August 2016: 5 fallow deer removed (2 males, 3 females)
        initial_ponies = (results_July2016["Exmoor pony"][0])
        initial_cows = (results_July2016["Longhorn cattle"][0])
        initial_pigs = (results_July2016["Tamworth pigs"][0])
        initial_fallowDeer = (results_July2016 ["Fallow deer"][0]) - 5
        initial_redDeer = (results_July2016["Red deer"][0])
        initial_roeDeer = (results_July2016["Roe deer"][0])
        initial_grassland = (results_July2016["Grassland"][0])
        initial_woodland = (results_July2016["Woodland"][0])
        initial_scrubland = (results_July2016["Thorny Scrub"][0])
        # call the model
        model_August2016 = KneppModel(
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
            width = 10, height = 10)
        model_August2016.step()
        results_August2016 = model_August2016.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_August2016["Time"] += 139
        final_results_list.append(results_August2016)




 # September & Oct 2016: 19 cows added and 9 removed
        initial_ponies = (results_August2016["Exmoor pony"][0]) 
        initial_cows = (results_August2016["Longhorn cattle"][0]) + 10
        initial_pigs = (results_August2016["Tamworth pigs"][0])
        initial_fallowDeer = (results_August2016 ["Fallow deer"][0])
        initial_redDeer = (results_August2016["Red deer"][0])
        initial_roeDeer = (results_August2016["Roe deer"][0])
        initial_grassland = (results_August2016["Grassland"][0])
        initial_woodland = (results_August2016["Woodland"][0])
        initial_scrubland = (results_August2016["Thorny Scrub"][0])
        # call the model
        model_Sept2016 = KneppModel(
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
            width = 10, height = 10)
        for _ in range(2):
            model_Sept2016.step()
        results_Sept2016 = model_Sept2016.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Sept2016["Time"] += 140
        final_results_list.append(results_Sept2016)




 # Nov 2016: 3 fallow deer culled (2 males, 1 female); 5 cows removed (all females)
        initial_ponies = (results_Sept2016["Exmoor pony"][0]) 
        initial_cows = (results_Sept2016["Longhorn cattle"][0]) - 5
        initial_pigs = (results_Sept2016["Tamworth pigs"][0])
        initial_fallowDeer = (results_Sept2016 ["Fallow deer"][0]) - 3
        initial_redDeer = (results_Sept2016["Red deer"][0])
        initial_roeDeer = (results_Sept2016["Roe deer"][0])
        initial_grassland = (results_Sept2016["Grassland"][0])
        initial_woodland = (results_Sept2016["Woodland"][0])
        initial_scrubland = (results_Sept2016["Thorny Scrub"][0])
        # call the model
        model_Nov2016 = KneppModel(
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
            width = 10, height = 10)
        model_Nov2016.step()
        results_Nov2016 = model_Nov2016.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Nov2016["Time"] += 142
        final_results_list.append(results_Nov2016)




# Dec 2016: 9 fallow deer culled (2 males, 7 females); 13 cows sold; 4 pigs sold (females)
        initial_ponies = (results_Nov2016["Exmoor pony"][0]) 
        initial_cows = (results_Nov2016["Longhorn cattle"][0]) - 13
        initial_pigs = (results_Nov2016["Tamworth pigs"][0]) - 4
        initial_fallowDeer = (results_Nov2016 ["Fallow deer"][0]) - 9
        initial_redDeer = (results_Nov2016["Red deer"][0])
        initial_roeDeer = (results_Nov2016["Roe deer"][0])
        initial_grassland = (results_Nov2016["Grassland"][0])
        initial_woodland = (results_Nov2016["Woodland"][0])
        initial_scrubland = (results_Nov2016["Thorny Scrub"][0])
        # call the model
        model_Dec2016 = KneppModel(
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
            width = 10, height = 10)
        model_Dec2016.step()
        results_Dec2016 = model_Dec2016.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Dec2016["Time"] += 143
        final_results_list.append(results_Dec2016)




# Jan 2017: 4 pigs sold, 1 boar added
        initial_ponies = (results_Dec2016["Exmoor pony"][0]) 
        initial_cows = (results_Dec2016["Longhorn cattle"][0])
        initial_pigs = (results_Dec2016["Tamworth pigs"][0]) - 3
        initial_fallowDeer = (results_Dec2016 ["Fallow deer"][0])
        initial_redDeer = (results_Dec2016["Red deer"][0])
        initial_roeDeer = (results_Dec2016["Roe deer"][0])
        initial_grassland = (results_Dec2016["Grassland"][0])
        initial_woodland = (results_Dec2016["Woodland"][0])
        initial_scrubland = (results_Dec2016["Thorny Scrub"][0])
        # call the model
        model_Jan2017 = KneppModel(
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
            width = 10, height = 10)
        model_Jan2017.step()
        results_Jan2017 = model_Jan2017.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Jan2017["Time"] += 144
        final_results_list.append(results_Jan2017)




# Feb 2017: 8 fallow deer sold (females), 2 pigs sold and boar removed
        initial_ponies = (results_Jan2017["Exmoor pony"][0]) 
        initial_cows = (results_Jan2017["Longhorn cattle"][0])
        initial_pigs = (results_Jan2017["Tamworth pigs"][0]) - 3
        initial_fallowDeer = (results_Jan2017 ["Fallow deer"][0]) - 8
        initial_redDeer = (results_Jan2017["Red deer"][0])
        initial_roeDeer = (results_Jan2017["Roe deer"][0])
        initial_grassland = (results_Jan2017["Grassland"][0])
        initial_woodland = (results_Jan2017["Woodland"][0])
        initial_scrubland = (results_Jan2017["Thorny Scrub"][0])
        # call the model
        model_Feb2017 = KneppModel(
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
            width = 10, height = 10)
        model_Feb2017.step()
        results_Feb2017 = model_Feb2017.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Feb2017["Time"] += 145
        final_results_list.append(results_Feb2017)










                                        # # # # # # # 2017 # # # # # # #


 # March 2017: 1 Exmoor pony subtracted; 12 less red deer
        initial_ponies = (results_Feb2017["Exmoor pony"][0]) - 1
        initial_cows = (results_Feb2017["Longhorn cattle"][0])
        initial_pigs = (results_Feb2017["Tamworth pigs"][0])
        initial_roeDeer = (results_Feb2017["Roe deer"][0])
        initial_grassland = (results_Feb2017["Grassland"][0])
        initial_woodland = (results_Feb2017["Woodland"][0])
        initial_scrubland = (results_Feb2017["Thorny Scrub"][0])
        initial_fallowDeer = (results_Feb2017["Fallow deer"][0])
        initial_redDeer = (results_Feb2017["Red deer"][0]) - 12
        # call the model
        model_March2017 = KneppModel(
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
            width = 10, height = 10)
        model_March2017.step()
        results_March2017 = model_March2017.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_March2017["Time"] += 146
        final_results_list.append(results_March2017)
    



 # April & May 2017: 3 cows culled
        initial_ponies = (results_March2017["Exmoor pony"][0])
        initial_cows = (results_March2017["Longhorn cattle"][0]) - 3
        initial_pigs = (results_March2017["Tamworth pigs"][0])
        initial_fallowDeer = (results_March2017["Fallow deer"][0])
        initial_redDeer = (results_March2017["Red deer"][0])
        initial_roeDeer = (results_March2017["Roe deer"][0])
        initial_grassland = (results_March2017["Grassland"][0])
        initial_woodland = (results_March2017["Woodland"][0])
        initial_scrubland = (results_March2017["Thorny Scrub"][0])
        model_April2017 = KneppModel(
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
            width = 10, height = 10)
        for _ in range(2):
            model_April2017.step()
        results_April2017 = model_April2017.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_April2017["Time"] += 147
        final_results_list.append(results_April2017)



 # June & July 2017: 24 cows culled, 3 bulls added
        initial_ponies = (results_April2017["Exmoor pony"][0])
        initial_cows = (results_April2017["Longhorn cattle"][0]) - 21
        initial_pigs = (results_April2017["Tamworth pigs"][0])
        initial_fallowDeer = (results_April2017["Fallow deer"][0])
        initial_redDeer = (results_April2017["Red deer"][0])
        initial_roeDeer = (results_April2017["Roe deer"][0])
        initial_grassland = (results_April2017["Grassland"][0])
        initial_woodland = (results_April2017["Woodland"][0])
        initial_scrubland = (results_April2017["Thorny Scrub"][0])
        # call the model
        model_June2017 = KneppModel(
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
            width = 10, height = 10)
        for _ in range(2):
            model_June2017.step()
        results_June2017 = model_June2017.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_June2017["Time"] += 149
        final_results_list.append(results_June2017)



 # August 2017: 16 fallow deer removed (13 females, 3 male)
        initial_ponies = (results_June2017["Exmoor pony"][0])
        initial_cows = (results_June2017["Longhorn cattle"][0])
        initial_pigs = (results_June2017["Tamworth pigs"][0])
        initial_fallowDeer = (results_June2017 ["Fallow deer"][0]) - 16
        initial_redDeer = (results_June2017["Red deer"][0])
        initial_roeDeer = (results_June2017["Roe deer"][0])
        initial_grassland = (results_June2017["Grassland"][0])
        initial_woodland = (results_June2017["Woodland"][0])
        initial_scrubland = (results_June2017["Thorny Scrub"][0])
        # call the model
        model_August2017 = KneppModel(
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
            width = 10, height = 10)
        model_August2017.step()
        results_August2017 = model_August2017.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_August2017["Time"] += 151
        final_results_list.append(results_August2017)




 # September 2017: 5 fallow deer culled (1 male, 4 females); 27 cows culled, 23 added (no males);
        initial_ponies = (results_August2017["Exmoor pony"][0]) 
        initial_cows = (results_August2017["Longhorn cattle"][0]) - 4
        initial_pigs = (results_August2017["Tamworth pigs"][0])
        initial_fallowDeer = (results_August2017 ["Fallow deer"][0]) - 5
        initial_redDeer = (results_August2017["Red deer"][0])
        initial_roeDeer = (results_August2017["Roe deer"][0])
        initial_grassland = (results_August2017["Grassland"][0])
        initial_woodland = (results_August2017["Woodland"][0])
        initial_scrubland = (results_August2017["Thorny Scrub"][0])
        # call the model
        model_Sept2017 = KneppModel(
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
            width = 10, height = 10)
        model_Sept2017.step()
        results_Sept2017 = model_Sept2017.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Sept2017["Time"] += 152
        final_results_list.append(results_Sept2017)




# Oct 2017: 4 fallow deer culled (females); 2 cows removed
        initial_ponies = (results_Sept2017["Exmoor pony"][0]) 
        initial_cows = (results_Sept2017["Longhorn cattle"][0]) - 2
        initial_pigs = (results_Sept2017["Tamworth pigs"][0])
        initial_fallowDeer = (results_Sept2017 ["Fallow deer"][0]) - 4
        initial_redDeer = (results_Sept2017["Red deer"][0])
        initial_roeDeer = (results_Sept2017["Roe deer"][0])
        initial_grassland = (results_Sept2017["Grassland"][0])
        initial_woodland = (results_Sept2017["Woodland"][0])
        initial_scrubland = (results_Sept2017["Thorny Scrub"][0])
        # call the model
        model_Oct2017 = KneppModel(
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
            width = 10, height = 10)
        model_Oct2017.step()
        results_Oct2017 = model_Oct2017.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Oct2017["Time"] += 153
        final_results_list.append(results_Oct2017)



 # Nov 2017: 2 falloe deer culled (males)
        initial_ponies = (results_Oct2017["Exmoor pony"][0]) 
        initial_cows = (results_Oct2017["Longhorn cattle"][0])
        initial_pigs = (results_Oct2017["Tamworth pigs"][0])
        initial_fallowDeer = (results_Oct2017 ["Fallow deer"][0]) - 2
        initial_redDeer = (results_Oct2017["Red deer"][0])
        initial_roeDeer = (results_Oct2017["Roe deer"][0])
        initial_grassland = (results_Oct2017["Grassland"][0])
        initial_woodland = (results_Oct2017["Woodland"][0])
        initial_scrubland = (results_Oct2017["Thorny Scrub"][0])
        # call the model
        model_Nov2017 = KneppModel(
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
            width = 10, height = 10)
        model_Nov2017.step()
        results_Nov2017 = model_Nov2017.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Nov2017["Time"] += 154
        final_results_list.append(results_Nov2017)




# Dec 2017: 46 fallow deer removed (4 males, 42 females); -1 red deer (male); -4 pigs
        initial_ponies = (results_Nov2017["Exmoor pony"][0]) 
        initial_cows = (results_Nov2017["Longhorn cattle"][0])
        initial_pigs = (results_Nov2017["Tamworth pigs"][0]) - 4
        initial_fallowDeer = (results_Nov2017 ["Fallow deer"][0]) - 46
        initial_redDeer = (results_Nov2017["Red deer"][0]) - 1
        initial_roeDeer = (results_Nov2017["Roe deer"][0])
        initial_grassland = (results_Nov2017["Grassland"][0])
        initial_woodland = (results_Nov2017["Woodland"][0])
        initial_scrubland = (results_Nov2017["Thorny Scrub"][0])
        # call the model
        model_Dec2017 = KneppModel(
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
            width = 10, height = 10)
        model_Dec2017.step()
        results_Dec2017 = model_Dec2017.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Dec2017["Time"] += 155
        final_results_list.append(results_Dec2017)




# Jan 2018: 9 pigs sold; 1 boar added
        initial_ponies = (results_Dec2017["Exmoor pony"][0]) 
        initial_cows = (results_Dec2017["Longhorn cattle"][0])
        initial_pigs = (results_Dec2017["Tamworth pigs"][0]) - 8
        initial_fallowDeer = (results_Dec2017 ["Fallow deer"][0])
        initial_redDeer = (results_Dec2017["Red deer"][0])
        initial_roeDeer = (results_Dec2017["Roe deer"][0])
        initial_grassland = (results_Dec2017["Grassland"][0])
        initial_woodland = (results_Dec2017["Woodland"][0])
        initial_scrubland = (results_Dec2017["Thorny Scrub"][0])
        # call the model
        model_Jan2018 = KneppModel(
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
            width = 10, height = 10)
        model_Jan2018.step()
        results_Jan2018 = model_Jan2018.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Jan2018["Time"] += 156
        final_results_list.append(results_Jan2018)




# Feb 2018: 14 fallow deer culled (13 females, 1 male); 1 red deer culled (male)
        initial_ponies = (results_Jan2018["Exmoor pony"][0]) 
        initial_cows = (results_Jan2018["Longhorn cattle"][0])
        initial_pigs = (results_Jan2018["Tamworth pigs"][0]) - 1
        initial_fallowDeer = (results_Jan2018 ["Fallow deer"][0]) - 14
        initial_redDeer = (results_Jan2018["Red deer"][0]) - 1
        initial_roeDeer = (results_Jan2018["Roe deer"][0])
        initial_grassland = (results_Jan2018["Grassland"][0])
        initial_woodland = (results_Jan2018["Woodland"][0])
        initial_scrubland = (results_Jan2018["Thorny Scrub"][0])
        # call the model
        model_Feb2018 = KneppModel(
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
            width = 10, height = 10)
        model_Feb2018.step()
        results_Feb2018 = model_Feb2018.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Feb2018["Time"] += 157
        final_results_list.append(results_Feb2018)











                                        # # # # # # # 2018 # # # # # # #


 # March 2018: 1 Exmoor pony subtracted
        initial_ponies = (results_Feb2018["Exmoor pony"][0]) - 1
        initial_cows = (results_Feb2018["Longhorn cattle"][0])
        initial_pigs = (results_Feb2018["Tamworth pigs"][0])
        initial_roeDeer = (results_Feb2018["Roe deer"][0])
        initial_grassland = (results_Feb2018["Grassland"][0])
        initial_woodland = (results_Feb2018["Woodland"][0])
        initial_scrubland = (results_Feb2018["Thorny Scrub"][0])
        initial_fallowDeer = (results_Feb2018["Fallow deer"][0])
        initial_redDeer = (results_Feb2018["Red deer"][0])
        # call the model
        model_March2018 = KneppModel(
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
            width = 10, height = 10)
        model_March2018.step()
        results_March2018 = model_March2018.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_March2018["Time"] += 158
        final_results_list.append(results_March2018)
    



 # April & May 2018: 1 cow added
        initial_ponies = (results_March2018["Exmoor pony"][0])
        initial_cows = (results_March2018["Longhorn cattle"][0]) + 1
        initial_pigs = (results_March2018["Tamworth pigs"][0])
        initial_fallowDeer = (results_March2018["Fallow deer"][0])
        initial_redDeer = (results_March2018["Red deer"][0])
        initial_roeDeer = (results_March2018["Roe deer"][0])
        initial_grassland = (results_March2018["Grassland"][0])
        initial_woodland = (results_March2018["Woodland"][0])
        initial_scrubland = (results_March2018["Thorny Scrub"][0])
        model_April2018 = KneppModel(
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
            width = 10, height = 10)
        for _ in range(2):
            model_April2018.step()
        results_April2018 = model_April2018.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_April2018["Time"] += 159
        final_results_list.append(results_April2018)



 # June 2018: 2 bulls added and 22 culled
        initial_ponies = (results_April2018["Exmoor pony"][0])
        initial_cows = (results_April2018["Longhorn cattle"][0]) - 20
        initial_pigs = (results_April2018["Tamworth pigs"][0])
        initial_fallowDeer = (results_April2018["Fallow deer"][0])
        initial_redDeer = (results_April2018["Red deer"][0])
        initial_roeDeer = (results_April2018["Roe deer"][0])
        initial_grassland = (results_April2018["Grassland"][0])
        initial_woodland = (results_April2018["Woodland"][0])
        initial_scrubland = (results_April2018["Thorny Scrub"][0])
        # call the model
        model_June2018 = KneppModel(
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
            width = 10, height = 10)
        model_June2018.step()
        results_June2018 = model_June2018.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_June2018["Time"] += 161
        final_results_list.append(results_June2018)



 # July 2018: 1 red deer culled; 1 pig culled
        initial_ponies = (results_June2018["Exmoor pony"][0])
        initial_cows = (results_June2018["Longhorn cattle"][0])
        initial_pigs = (results_June2018["Tamworth pigs"][0]) - 1
        initial_fallowDeer = (results_June2018 ["Fallow deer"][0])
        initial_redDeer = (results_June2018["Red deer"][0]) - 1
        initial_roeDeer = (results_June2018["Roe deer"][0])
        initial_grassland = (results_June2018["Grassland"][0])
        initial_woodland = (results_June2018["Woodland"][0])
        initial_scrubland = (results_June2018["Thorny Scrub"][0])
        # call the model
        model_July2018 = KneppModel(
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
            width = 10, height = 10)
        model_July2018.step()
        results_July2018 = model_July2018.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_July2018["Time"] += 162
        final_results_list.append(results_July2018)



# August 2018: all ponies removed; 1 red deer and one cow removed; - 15 fallow deer
        initial_ponies = (results_July2018["Exmoor pony"][0])
        initial_cows = (results_July2018["Longhorn cattle"][0]) + 4
        initial_pigs = (results_July2018["Tamworth pigs"][0])
        initial_fallowDeer = (results_July2018 ["Fallow deer"][0]) - 19
        initial_redDeer = (results_July2018["Red deer"][0])
        initial_roeDeer = (results_July2018["Roe deer"][0])
        initial_grassland = (results_July2018["Grassland"][0])
        initial_woodland = (results_July2018["Woodland"][0])
        initial_scrubland = (results_July2018["Thorny Scrub"][0])
        # call the model
        model_Aug2018 = KneppModel(
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
            width = 10, height = 10)
        model_Aug2018.step()
        results_Aug2018 = model_Aug2018.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Aug2018["Time"] += 163
        final_results_list.append(results_Aug2018)



# Sept 2018: -19 fallow der; +4 cattle; -1 pig
        initial_ponies = (results_Aug2018["Exmoor pony"][0]) 
        initial_cows = (results_Aug2018["Longhorn cattle"][0]) + 4
        initial_pigs = (results_Aug2018["Tamworth pigs"][0]) -1
        initial_fallowDeer = (results_Aug2018 ["Fallow deer"][0]) - 19
        initial_redDeer = (results_Aug2018["Red deer"][0])
        initial_roeDeer = (results_Aug2018["Roe deer"][0])
        initial_grassland = (results_Aug2018["Grassland"][0])
        initial_woodland = (results_Aug2018["Woodland"][0])
        initial_scrubland = (results_Aug2018["Thorny Scrub"][0])
        # call the model
        model_Sept2018 = KneppModel(
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
            width = 10, height = 10)
        model_Sept2018.step()
        results_Sept2018 = model_Sept2018.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Sept2018["Time"] += 164
        final_results_list.append(results_Sept2018)




# Oct 2018: -4 cows; -4 fallow deer
        initial_ponies = (results_Sept2018["Exmoor pony"][0]) 
        initial_cows = (results_Sept2018["Longhorn cattle"][0]) - 4
        initial_pigs = (results_Sept2018["Tamworth pigs"][0])
        initial_fallowDeer = (results_Sept2018 ["Fallow deer"][0]) - 4
        initial_redDeer = (results_Sept2018["Red deer"][0])
        initial_roeDeer = (results_Sept2018["Roe deer"][0])
        initial_grassland = (results_Sept2018["Grassland"][0])
        initial_woodland = (results_Sept2018["Woodland"][0])
        initial_scrubland = (results_Sept2018["Thorny Scrub"][0])
        # call the model
        model_Oct2018 = KneppModel(
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
            width = 10, height = 10)
        model_Oct2018.step()
        results_Oct2018 = model_Oct2018.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Oct2018["Time"] += 165
        final_results_list.append(results_Oct2018)



 # Nov 2018: -8 cows; -12 pigs
        initial_ponies = (results_Oct2018["Exmoor pony"][0]) 
        initial_cows = (results_Oct2018["Longhorn cattle"][0]) - 8
        initial_pigs = (results_Oct2018["Tamworth pigs"][0]) - 12
        initial_fallowDeer = (results_Oct2018 ["Fallow deer"][0])
        initial_redDeer = (results_Oct2018["Red deer"][0])
        initial_roeDeer = (results_Oct2018["Roe deer"][0])
        initial_grassland = (results_Oct2018["Grassland"][0])
        initial_woodland = (results_Oct2018["Woodland"][0])
        initial_scrubland = (results_Oct2018["Thorny Scrub"][0])
        # call the model
        model_Nov2018 = KneppModel(
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
            width = 10, height = 10)
        model_Nov2018.step()
        results_Nov2018 = model_Nov2018.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Nov2018["Time"] += 166
        final_results_list.append(results_Nov2018)




# Dec 2018 and Jan 2019: -19 fallow; -4 cows; -1 red
        initial_ponies = (results_Nov2018["Exmoor pony"][0]) 
        initial_cows = (results_Nov2018["Longhorn cattle"][0]) - 4
        initial_pigs = (results_Nov2018["Tamworth pigs"][0])
        initial_fallowDeer = (results_Nov2018 ["Fallow deer"][0]) - 19
        initial_redDeer = (results_Nov2018["Red deer"][0]) - 1
        initial_roeDeer = (results_Nov2018["Roe deer"][0])
        initial_grassland = (results_Nov2018["Grassland"][0])
        initial_woodland = (results_Nov2018["Woodland"][0])
        initial_scrubland = (results_Nov2018["Thorny Scrub"][0])
        # call the model
        model_Dec2018 = KneppModel(
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
            width = 10, height = 10)
        for _ in range(2):
            model_Dec2018.step()
        results__Dec2018 = model_Dec2018.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results__Dec2018["Time"] += 167
        final_results_list.append(results__Dec2018)




# Feb 2019: -2 cows; +1 pig
        initial_ponies = (results__Dec2018["Exmoor pony"][0]) 
        initial_cows = (results__Dec2018["Longhorn cattle"][0]) - 2
        initial_pigs = (results__Dec2018["Tamworth pigs"][0]) + 1
        initial_fallowDeer = (results__Dec2018 ["Fallow deer"][0])
        initial_redDeer = (results__Dec2018["Red deer"][0]) - 1
        initial_roeDeer = (results__Dec2018["Roe deer"][0])
        initial_grassland = (results__Dec2018["Grassland"][0])
        initial_woodland = (results__Dec2018["Woodland"][0])
        initial_scrubland = (results__Dec2018["Thorny Scrub"][0])
        # call the model
        model_Feb2019 = KneppModel(
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
            width = 10, height = 10)
        model_Feb2019.step()
        results_Feb2019 = model_Feb2019.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Feb2019["Time"] += 169
        final_results_list.append(results_Feb2019)









                                        # # # # # # # 2019 # # # # # # #


    # March, April, May 2019: -1 pig
        initial_ponies = (results_Feb2019["Exmoor pony"][0])
        initial_cows = (results_Feb2019["Longhorn cattle"][0])
        initial_pigs = (results_Feb2019["Tamworth pigs"][0]) - 1
        initial_roeDeer = (results_Feb2019["Roe deer"][0])
        initial_grassland = (results_Feb2019["Grassland"][0])
        initial_woodland = (results_Feb2019["Woodland"][0])
        initial_scrubland = (results_Feb2019["Thorny Scrub"][0])
        initial_fallowDeer = (results_Feb2019["Fallow deer"][0])
        initial_redDeer = (results_Feb2019["Red deer"][0])
        # call the model
        model_March2019 = KneppModel(
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
            width = 10, height = 10)
        for _ in range(2):
            model_March2019.step()
        results_March2019 = model_March2019.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_March2019["Time"] += 170
        final_results_list.append(results_March2019)
    


 # June 2018: 28 cows culled
        initial_ponies = (results_March2019["Exmoor pony"][0])
        initial_cows = (results_March2019["Longhorn cattle"][0]) - 28
        initial_pigs = (results_March2019["Tamworth pigs"][0])
        initial_fallowDeer = (results_March2019["Fallow deer"][0])
        initial_redDeer = (results_March2019["Red deer"][0])
        initial_roeDeer = (results_March2019["Roe deer"][0])
        initial_grassland = (results_March2019["Grassland"][0])
        initial_woodland = (results_March2019["Woodland"][0])
        initial_scrubland = (results_March2019["Thorny Scrub"][0])
        # call the model
        model_June2019 = KneppModel(
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
            width = 10, height = 10)
        model_June2019.step()
        results_June2019 = model_June2019.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_June2019["Time"] += 172
        final_results_list.append(results_June2019)



 # July & Aug 2019: 26 pigs culled, 3 cows culled and 5 added
        initial_ponies = (results_June2019["Exmoor pony"][0])
        initial_cows = (results_June2019["Longhorn cattle"][0]) + 2
        initial_pigs = (results_June2019["Tamworth pigs"][0]) - 26
        initial_fallowDeer = (results_June2019 ["Fallow deer"][0])
        initial_redDeer = (results_June2019["Red deer"][0]) - 1
        initial_roeDeer = (results_June2019["Roe deer"][0])
        initial_grassland = (results_June2019["Grassland"][0])
        initial_woodland = (results_June2019["Woodland"][0])
        initial_scrubland = (results_June2019["Thorny Scrub"][0])
        # call the model
        model_July2019 = KneppModel(
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
            width = 10, height = 10)
        for _ in range(2):
            model_July2019.step()
        results_July2019 = model_July2019.datacollector.get_model_vars_dataframe()
        results_July2019["Time"] += 173
        final_results_list.append(results_July2019)



# Sept 2019: -15 fallow deer; 23 cows culled and 25 added;
        initial_ponies = (results_July2019["Exmoor pony"][0]) 
        initial_cows = (results_July2019["Longhorn cattle"][0]) + 2
        initial_pigs = (results_July2019["Tamworth pigs"][0])
        initial_fallowDeer = (results_July2019 ["Fallow deer"][0]) - 15
        initial_redDeer = (results_July2019["Red deer"][0])
        initial_roeDeer = (results_July2019["Roe deer"][0])
        initial_grassland = (results_July2019["Grassland"][0])
        initial_woodland = (results_July2019["Woodland"][0])
        initial_scrubland = (results_July2019["Thorny Scrub"][0])
        # call the model
        model_Sept2019 = KneppModel(
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
            width = 10, height = 10)
        model_Sept2019.step()
        results_Sept2019 = model_Sept2019.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Sept2019["Time"] += 175
        final_results_list.append(results_Sept2019)




# Oct 2019: -5 cows
        initial_ponies = (results_Sept2019["Exmoor pony"][0]) 
        initial_cows = (results_Sept2019["Longhorn cattle"][0]) - 5
        initial_pigs = (results_Sept2019["Tamworth pigs"][0])
        initial_fallowDeer = (results_Sept2019 ["Fallow deer"][0])
        initial_redDeer = (results_Sept2019["Red deer"][0])
        initial_roeDeer = (results_Sept2019["Roe deer"][0])
        initial_grassland = (results_Sept2019["Grassland"][0])
        initial_woodland = (results_Sept2019["Woodland"][0])
        initial_scrubland = (results_Sept2019["Thorny Scrub"][0])
        # call the model
        model_Oct2019 = KneppModel(
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
            width = 10, height = 10)
        model_Oct2019.step()
        results_Oct2019 = model_Oct2019.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Oct2019["Time"] += 176
        final_results_list.append(results_Oct2019)



 # Nov 2018: -7 fallow deer; -1 cow; -3 red deer
        initial_ponies = (results_Oct2019["Exmoor pony"][0]) 
        initial_cows = (results_Oct2019["Longhorn cattle"][0]) - 1
        initial_pigs = (results_Oct2019["Tamworth pigs"][0])
        initial_fallowDeer = (results_Oct2019 ["Fallow deer"][0]) -7
        initial_redDeer = (results_Oct2019["Red deer"][0]) - 3
        initial_roeDeer = (results_Oct2019["Roe deer"][0])
        initial_grassland = (results_Oct2019["Grassland"][0])
        initial_woodland = (results_Oct2019["Woodland"][0])
        initial_scrubland = (results_Oct2019["Thorny Scrub"][0])
        # call the model
        model_Nov2019 = KneppModel(
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
            width = 10, height = 10)
        model_Nov2019.step()
        results_Nov2019 = model_Nov2019.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Nov2019["Time"] += 177
        final_results_list.append(results_Nov2019)




# Dec 2019: -12 fallow deer, -7 cows;
        initial_ponies = (results_Nov2019["Exmoor pony"][0]) 
        initial_cows = (results_Nov2019["Longhorn cattle"][0]) - 7
        initial_pigs = (results_Nov2019["Tamworth pigs"][0]) + 1
        initial_fallowDeer = (results_Nov2019 ["Fallow deer"][0]) - 12
        initial_redDeer = (results_Nov2019["Red deer"][0]) - 4
        initial_roeDeer = (results_Nov2019["Roe deer"][0])
        initial_grassland = (results_Nov2019["Grassland"][0])
        initial_woodland = (results_Nov2019["Woodland"][0])
        initial_scrubland = (results_Nov2019["Thorny Scrub"][0])
        # call the model
        model_Dec2019 = KneppModel(
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
            width = 10, height = 10)
        model_Dec2019.step()
        results_Dec2019 = model_Dec2019.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Dec2019["Time"] += 178
        final_results_list.append(results_Dec2019)




# Jan 2020: -14 fallow deer;
        initial_ponies = (results_Dec2019["Exmoor pony"][0]) 
        initial_cows = (results_Dec2019["Longhorn cattle"][0])
        initial_pigs = (results_Dec2019["Tamworth pigs"][0])
        initial_fallowDeer = (results_Dec2019 ["Fallow deer"][0]) - 24
        initial_redDeer = (results_Dec2019["Red deer"][0])
        initial_roeDeer = (results_Dec2019["Roe deer"][0])
        initial_grassland = (results_Dec2019["Grassland"][0])
        initial_woodland = (results_Dec2019["Woodland"][0])
        initial_scrubland = (results_Dec2019["Thorny Scrub"][0])
        # call the model
        model_Jan2020 = KneppModel(
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
            width = 10, height = 10)
        model_Jan2020.step()
        results_Jan2020 = model_Jan2020.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Jan2020["Time"] += 179
        final_results_list.append(results_Jan2020)


# Feb 2020: -12 fallow deer; -2 red deer; -2 pigs
        initial_ponies = (results_Jan2020["Exmoor pony"][0]) 
        initial_cows = (results_Jan2020["Longhorn cattle"][0]) - 1
        initial_pigs = (results_Jan2020["Tamworth pigs"][0]) - 2
        initial_fallowDeer = (results_Jan2020 ["Fallow deer"][0]) - 12
        initial_redDeer = (results_Jan2020["Red deer"][0]) - 2
        initial_roeDeer = (results_Jan2020["Roe deer"][0])
        initial_grassland = (results_Jan2020["Grassland"][0])
        initial_woodland = (results_Jan2020["Woodland"][0])
        initial_scrubland = (results_Jan2020["Thorny Scrub"][0])
        # call the model
        model_Feb2020 = KneppModel(
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
            width = 10, height = 10)
        model_Feb2020.step()
        results_Feb2020 = model_Feb2020.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_Feb2020["Time"] += 180
        final_results_list.append(results_Feb2020)







                                    # # # # # 2020 # # # # # #


        # March & April & May 2020: 15 exmoors added back in; -1  cow and +3 cows; -1 pig
        initial_ponies = (results_Feb2020["Exmoor pony"][0]) + 15
        initial_cows = (results_Feb2020["Longhorn cattle"][0]) + 2
        initial_pigs = (results_Feb2020["Tamworth pigs"][0]) - 1
        initial_fallowDeer = (results_Feb2020 ["Fallow deer"][0])
        initial_redDeer = (results_Feb2020["Red deer"][0])
        initial_roeDeer = (results_Feb2020["Roe deer"][0])
        initial_grassland = (results_Feb2020["Grassland"][0])
        initial_woodland = (results_Feb2020["Woodland"][0])
        initial_scrubland = (results_Feb2020["Thorny Scrub"][0])
        # call the model
        model_March2020 = KneppModel(
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
            width = 10, height = 10)
        for _ in range(3):
            model_March2020.step()
        results_March2020 = model_March2020.datacollector.get_model_vars_dataframe()
        # make sure the timelines add up
        results_March2020["Time"] += 181
        final_results_list.append(results_March2020)







                                    # # # # # # Gather the dataframes # # # # # #

    

    # append all the runs to dataframe
    final_results = pd.concat(final_results_list)
    # add run_numbers to the dataframe
    IDs = np.arange(1,len(accepted_year)+1)
    final_results['run_number'] = np.repeat(IDs,134)

   # see what's happening in the final year
    with pd.option_context('display.max_columns', None):
        print("final_results: \n", final_results[(final_results["Time"] == 184)])

    # make a dataframe of all the parameters we tried
    final_parameters = pd.DataFrame(data=final_parameters, columns=variables)





                                      # # # # # # Filter the runs # # # # # #

                                

    # # FILTER RUNS with the correct parameters
    # accepted_year_Apr2015 = final_results[(final_results["Time"] == 123) &
    #                                       (final_results["Longhorn cattle"] == 115)]
    #                                     #   (final_results["Tamworth pig"] == 22)]

    # accepted_year_May2015 = final_results[(final_results["Time"] == 124) &
    #         (final_results["Longhorn cattle"] == 129)]
    #     #   (final_results["Tamworth pig"] == 22)]

    # accepted_year_March2016 = final_results[(final_results["Time"] == 134) &
    #         (final_results["Fallow deer"] == 140)]
    #     #   (final_results["Red deer"] == 26)]

    accepted_year_postReintro = final_results[(final_results["Time"] == 184) &
                                (final_results["Roe deer"] <= 40) & (final_results["Roe deer"] >= 20)
                                # (final_results["Grassland"] <= 69) & (final_results["Grassland"] >= 49) &
                                # (final_results["Woodland"] <= 35) & (final_results["Woodland"] >= 21) &
                                # (final_results["Thorny Scrub"] <= 29) & (final_results["Thorny Scrub"] >= 9)
                                ]

    accepted_parameters_postReintro = final_parameters[final_parameters['run_number'].isin(accepted_year_postReintro['run_number'])]
    # accepted final_results (all time-steps)
    all_accepted_runs_postReintro = final_results[final_results['run_number'].isin(accepted_year_postReintro['run_number'])]
  

    # concantenate all the runs so far (combined, pre and post-reintro)
    all_accepted_runs_combined = pd.concat([all_accepted_runs, all_accepted_runs_postReintro], ignore_index=True)

    # with pd.option_context('display.max_rows',None, 'display.max_columns',None):
    #     
    # 
    ("accepted_years_postReintroduction: \n", accepted_year_postReintro)


    return accepted_parameters_postReintro, all_accepted_runs_postReintro, accepted_year_postReintro, all_accepted_runs_combined


run_postreintro_model()



# calculate the time it takes to run per node, currently 8.5min for 1k runs
stop = timeit.default_timer()
print('Total time: ', (stop - start))
