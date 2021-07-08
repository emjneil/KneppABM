from KneppModel_ABM import KneppModel
import numpy as np
import random
import pandas as pd


# # # ----- Create a model with agents and run it for 10 steps -----

def run_model():

    # define number of simulations
    number_simulations = 10
    # time for first ODE (January 2005- March 2009, ~ 50 months)
    time_firstModel = 50
    # make list of variables
    final_results_list = []
    final_parameters = []
    run_number = 0


    # run the model for 50 months, 10 times
    for _ in range(number_simulations):
        # keep track of the runs
        run_number +=1
        # define parameters
        initial_roeDeer = random.randint(6, 18)
        initial_grassland = random.randint(70, 90)
        initial_woodland = random.randint(4, 24)
        initial_scrubland = random.randint(0, 11)
        initial_ponies = 0
        initial_cows = 0
        initial_fallowDeer = 0
        initial_redDeer = 0
        initial_pigs = 0
        ratio_mf_cows = 0
        ratio_mf_fallowDeer = 0
        ratio_mf_redDeer = 0
        ratio_mf_pigs = 0
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
        # Exmoor ponies
        ponies_gain_from_grass = 0
        ponies_gain_from_Trees = 0
        ponies_gain_from_Scrub = 0
        ponies_gain_from_Saplings =  0
        ponies_gain_from_YoungScrub = 0
        ponies_impactGrass = 0
        ponies_saplingsEaten = 0
        ponies_youngScrubEaten = 0
        ponies_treesEaten = 0
        ponies_scrubEaten = 0
        # Longhorn cattle
        cows_reproduce = 0
        cows_gain_from_grass = 0
        cows_gain_from_Trees = 0
        cows_gain_from_Scrub = 0
        cows_gain_from_Saplings =  0
        cows_gain_from_YoungScrub = 0
        cows_impactGrass = 0
        cows_saplingsEaten = 0
        cows_youngScrubEaten = 0
        cows_treesEaten = 0
        cows_scrubEaten = 0
        # Fallow deer
        fallowDeer_reproduce = 0
        fallowDeer_gain_from_grass = 0
        fallowDeer_gain_from_Trees = 0
        fallowDeer_gain_from_Scrub = 0
        fallowDeer_gain_from_Saplings =  0
        fallowDeer_gain_from_YoungScrub = 0
        fallowDeer_impactGrass = 0
        fallowDeer_saplingsEaten = 0
        fallowDeer_youngScrubEaten = 0
        fallowDeer_treesEaten = 0
        fallowDeer_scrubEaten = 0
        # Red deer
        redDeer_reproduce = 0
        redDeer_gain_from_grass = 0
        redDeer_gain_from_Trees = 0
        redDeer_gain_from_Scrub = 0
        redDeer_gain_from_Saplings =  0
        redDeer_gain_from_YoungScrub = 0
        redDeer_impactGrass = 0
        redDeer_saplingsEaten = 0
        redDeer_youngScrubEaten = 0
        redDeer_treesEaten = 0
        redDeer_scrubEaten = 0
        # Tamworth pigs
        pigs_reproduce = 0
        pigs_gain_from_grass = 0
        pigs_gain_from_Saplings =  0
        pigs_gain_from_YoungScrub = 0
        pigs_impactGrass = 0
        pigs_saplingsEaten = 0
        pigs_youngScrubEaten = 0


        # parameters = generate_parameters()
        parameters_used = [
            run_number,
            chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
            chance_scrubOutcompetedByTree, chance_grassOutcompetedByTreeScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
            initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland, initial_ponies, initial_cows, initial_fallowDeer, initial_redDeer, initial_pigs,
            ratio_mf_cows, ratio_mf_fallowDeer, ratio_mf_redDeer, ratio_mf_pigs,
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


        # run the model 
        model = KneppModel(
            chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
            chance_scrubOutcompetedByTree, chance_grassOutcompetedByTreeScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
            initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland, initial_ponies, initial_cows, initial_fallowDeer, initial_redDeer, initial_pigs,
            ratio_mf_cows, ratio_mf_fallowDeer, ratio_mf_redDeer, ratio_mf_pigs,
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
        
        # run for 50 months (Jan 2005 - March 2009)
        for _ in range(time_firstModel): 
            # run the model
            model.step()

        # remember the results
        results = model.datacollector.get_model_vars_dataframe()
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
        "initial_ponies",
        "initial_cows",
        "initial_fallowDeer",
        "initial_redDeer",
        "initial_pigs",
        # reintroduced herbivore m/f ratios
        "ratio_mf_cows", 
        "ratio_mf_fallowDeer", 
        "ratio_mf_redDeer", 
        "ratio_mf_pigs",
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

    final_parameters = pd.DataFrame(data=final_parameters, columns=variables)
    # add run_number to final parameter set too
    IDs = np.arange(1,number_simulations+1)
    final_results['run_number'] = np.repeat(IDs,50)



    # # # FILTER RUNS # # #

    accepted_year = final_results[(final_results["Time"] == 50) &
                                (final_results["Roe deer"] <= 40) & (final_results["Roe deer"] >= 12)]
                                # (final_results["Grassland"] <= 90) & (final_results["Grassland"] >= 49) &
                                # (final_results["Woodland"] <= 27) & (final_results["Woodland"] >= 7)]
                                # (final_results["Thorny Scrub"] <= 21) & (final_results["Thorny Scrub"] >= 1)
                                # ]

    # accepted final_results (all time-steps)
    all_accepted_runs = final_results[final_results['run_number'].isin(accepted_year['run_number'])]
  
    # accepted parameters
    accepted_parameters = final_parameters[final_parameters['run_number'].isin(accepted_year['run_number'])]

    # with pd.option_context('display.max_columns',None):
    #     print(final_results[(final_results["Time"] == 50)])

    # with pd.option_context('display.max_rows',None, 'display.max_columns',None):
    #     print("accepted_years: \n", accepted_year)
        
    return accepted_parameters, all_accepted_runs, accepted_year, variables

