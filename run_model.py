# ------ ABM of the Knepp Estate (2005-2046) --------
from KneppModel_ABM import KneppModel 
import numpy as np
import random
import pandas as pd
import timeit


# # # # Run the model # # # # 


def run_all_models():
    
    # time the program
    start = timeit.default_timer()

    # define number of simulations
    number_simulations =  1
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
        chance_grassOutcompetedByTree = np.random.uniform(0,1)
        chance_grassOutcompetedByScrub = np.random.uniform(0,1)
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
            pigs_impactGrass, pigs_saplingsEaten, pigs_youngScrubEaten 
            ]
        # append to dataframe
        final_parameters.append(parameters_used)

        # keep track of the runs
        run_number +=1
        print(run_number)
        model = KneppModel(
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
        "chance_grassOutcompetedByTree",
        "chance_grassOutcompetedByScrub",
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

    # filter the runs and tag the dataframe
    # pre-reintroduction model
    accepted_preReintro = final_results[(final_results["Time"] == 50) &
    (final_results["Roe deer"] <= 40) & (final_results["Roe deer"] >= 12) & 
    (final_results["Grassland"] <= 90) & (final_results["Grassland"] >= 49) & 
    (final_results["Woodland"] <= 27) & (final_results["Woodland"] >= 7) & 
    (final_results["Thorny Scrub"] <= 21) & (final_results["Thorny Scrub"] >= 1)]
    print("number passed pre-reintro filters:", len(accepted_preReintro))
    # April 2015
    accepted_April2015 = accepted_preReintro[(accepted_preReintro["Time"] == 123) &
    (accepted_preReintro["Longhorn cattle"] <= 127) & (accepted_preReintro["Longhorn cattle"] >= 104) &
    (accepted_preReintro["Tamworth pigs"] <= 24) & (accepted_preReintro["Tamworth pigs"] >= 20)]
    print("number passed April 2015 filters:", len(accepted_April2015))
    # May 2015
    accepted_May2015 = accepted_April2015[(accepted_April2015["Time"] == 124) &
    (accepted_April2015["Longhorn cattle"] <= 142) & (accepted_April2015["Longhorn cattle"] >= 116)]
    print("number passed May 2015 filters:", len(accepted_May2015))
    # June 2015
    accepted_June2015 = accepted_May2015[(accepted_May2015["Time"] == 125) &
    (accepted_May2015["Longhorn cattle"] <= 142) & (accepted_May2015["Longhorn cattle"] >= 116)]
    print("number passed June 2015 filters:", len(accepted_June2015))
    # Feb 2016
    accepted_Feb2016 = accepted_June2015[(accepted_June2015["Time"] == 133) &
    (accepted_June2015["Exmoor pony"] == 10)]
    print("number passed February 2016 filters:", len(accepted_Feb2016))
    # March 2016
    accepted_March2016 = accepted_Feb2016[(accepted_Feb2016["Time"] == 134) &
    (accepted_Feb2016["Fallow deer"] <= 154) & (accepted_Feb2016["Fallow deer"] >= 126) &
    (accepted_Feb2016["Red deer"] <= 29) & (accepted_Feb2016["Red deer"] >= 23) &
    (accepted_Feb2016["Tamworth pigs"] <= 10) & (accepted_Feb2016["Tamworth pigs"] >= 8)]
    print("number passed March 2016 filters:", len(accepted_March2016))
    # April 2016
    accepted_April2016 = accepted_March2016[(accepted_March2016["Time"] == 135) &
    (accepted_March2016["Longhorn cattle"] <= 113) & (accepted_March2016["Longhorn cattle"] >= 93)]
    print("number passed April 2016 filters:", len(accepted_April2016))
    # May 2016
    accepted_May2016 = accepted_April2016[(accepted_April2016["Time"] == 136) &
    (accepted_April2016["Longhorn cattle"] <= 119) & (accepted_April2016["Longhorn cattle"] >= 97) &
    (accepted_April2016["Tamworth pigs"] <= 19) & (accepted_April2016["Tamworth pigs"] >= 15)]
    print("number passed May 2016 filters:", len(accepted_May2016))
    # June 2016
    accepted_June2016 = accepted_May2016[(accepted_May2016["Time"] == 137) &
    (accepted_May2016["Longhorn cattle"] <= 98) & (accepted_May2016["Longhorn cattle"] >= 80)]
    print("number passed June 2016 filters:", len(accepted_June2016))
    # Feb 2017
    accepted_Feb2017 = accepted_June2016[(accepted_June2016["Time"] == 145) &
    (accepted_June2016["Exmoor pony"] == 11)]
    print("number passed Feb 2017 filters:", len(accepted_Feb2017))
    # March 2017
    accepted_March2017 = accepted_Feb2017[(accepted_Feb2017["Time"] == 146) &
    (accepted_Feb2017["Fallow deer"] <= 182) & (accepted_Feb2017["Fallow deer"] >= 149) ]
    print("number passed March 2017 filters:", len(accepted_March2017))
    # April 2017
    accepted_April2017 = accepted_March2017[(accepted_March2017["Time"] == 147) &
    (accepted_March2017["Longhorn cattle"] <= 110) & (accepted_March2017["Longhorn cattle"] >= 90) &
    (accepted_March2017["Tamworth pigs"] <= 24) & (accepted_March2017["Tamworth pigs"] >= 20)]
    print("number passed April 2017 filters:", len(accepted_April2017))
    # May 2017
    accepted_May2017 = accepted_April2017[(accepted_April2017["Time"] == 148) &
    (accepted_April2017["Longhorn cattle"] <= 120) & (accepted_April2017["Longhorn cattle"] >= 98)]
    print("number passed May 2017 filters:", len(accepted_May2017))
    # June 2017
    accepted_June2017 = accepted_May2017[(accepted_May2017["Time"] == 149) &
    (accepted_May2017["Longhorn cattle"] <= 103) & (accepted_May2017["Longhorn cattle"] >= 85)]
    print("number passed June 2017 filters:", len(accepted_June2017))
    # January 2018
    accepted_Jan2018 = accepted_June2017[(accepted_June2017["Time"] == 156) &
    (accepted_June2017["Tamworth pigs"] <= 13) & (accepted_June2017["Tamworth pigs"] >= 11)]
    print("number passed January 2018 filters:", len(accepted_Jan2018))
    # February 2018
    accepted_Feb2018 = accepted_Jan2018[(accepted_Jan2018["Time"] == 157) &
    (accepted_Jan2018["Tamworth pigs"] <= 18) & (accepted_Jan2018["Tamworth pigs"] >= 14) &
    (accepted_Jan2018["Exmoor pony"] == 10)]
    print("number passed Feb 2018 filters:", len(accepted_Feb2018)) 
    # March 2018
    accepted_March2018 = accepted_Feb2018[(accepted_Feb2018["Time"] == 158) &
    (accepted_Feb2018["Fallow deer"] <= 276) & (accepted_Feb2018["Fallow deer"] >= 226) &
    (accepted_Feb2018["Red deer"] <= 26) & (accepted_Feb2018["Red deer"] >= 22)]
    print("number passed March 2018 filters:", len(accepted_March2018)) 
    # April 2018
    accepted_April2018 = accepted_March2018[(accepted_March2018["Time"] == 159) &
    (accepted_March2018["Longhorn cattle"] <= 111) & (accepted_March2018["Longhorn cattle"] >= 91)]
    print("number passed April 2018 filters:", len(accepted_April2018)) 
     # May 2018
    accepted_May2018 = accepted_April2018[(accepted_April2018["Time"] == 160) &
    (accepted_April2018["Longhorn cattle"] <= 129) & (accepted_April2018["Longhorn cattle"] >= 105) &
    (accepted_April2018["Tamworth pigs"] <= 25) & (accepted_April2018["Tamworth pigs"] >= 21)]
    print("number passed May 2018 filters:", len(accepted_May2018)) 
    # June 2018
    accepted_June2018 = accepted_May2018[(accepted_May2018["Time"] == 161) &
    (accepted_May2018["Longhorn cattle"] <= 113) & (accepted_May2018["Longhorn cattle"] >= 93)]
    print("number passed June 2018 filters:", len(accepted_June2018)) 
    # March 2019
    accepted_March2019 = accepted_June2018[(accepted_June2018["Time"] == 170) &
    (accepted_June2018["Fallow deer"] <= 306) & (accepted_June2018["Fallow deer"] >= 250) &
    (accepted_June2018["Red deer"] <= 41) & (accepted_June2018["Red deer"] >= 33)]
    print("number passed March 2019 filters:", len(accepted_March2019)) 
    # April 2019
    accepted_April2019 = accepted_March2019[(accepted_March2019["Time"] == 171) &
    (accepted_March2019["Longhorn cattle"] <= 111) & (accepted_March2019["Longhorn cattle"] >= 91)]
    print("number passed April 2019 filters:", len(accepted_April2019)) 
    # May 2019
    accepted_May2019 = accepted_April2019[(accepted_April2019["Time"] == 172) &
    (accepted_April2019["Longhorn cattle"] <= 121) & (accepted_April2019["Longhorn cattle"] >= 99)]
    print("number passed May 2019 filters:", len(accepted_May2019))
    # June 2019
    accepted_June2019 = accepted_May2019[(accepted_May2019["Time"] == 173) &
    (accepted_May2019["Longhorn cattle"] <= 98) & (accepted_May2019["Longhorn cattle"] >= 80)]
    print("number passed June 2019 filters:", len(accepted_June2019)) 
    # July 2019
    accepted_July2019 = accepted_June2019[(accepted_June2019["Time"] == 174) &
    (accepted_June2019["Tamworth pigs"] <= 10) & (accepted_June2019["Tamworth pigs"] >= 8)]
    print("number passed July 2019 filters:", len(accepted_July2019)) 
    # March 2020
    accepted_March2020 = accepted_July2019[(accepted_July2019["Time"] == 182) &
    (accepted_July2019["Fallow deer"] <= 272) & (accepted_July2019["Fallow deer"] >= 222) &
    (accepted_July2019["Red deer"] <= 39) & (accepted_July2019["Red deer"] >= 32)]
    print("number passed March 2020 filters:", len(accepted_March2020)) 
    # May 2020
    all_accepted_runs = accepted_March2020[(accepted_March2020["Time"] == 184) &
    (accepted_March2020["Tamworth pigs"] <= 21) & (accepted_March2020["Tamworth pigs"] >= 17) &
    (accepted_March2020["Exmoor pony"] == 15) &
    (accepted_March2020["Roe deer"] <= 40) & (accepted_March2020["Roe deer"] >= 20) &
    (accepted_March2020["Grassland"] <= 69) & (accepted_March2020["Grassland"] >= 49) &
    (accepted_March2020["Thorny Scrub"] <= 35) & (accepted_March2020["Thorny Scrub"] >= 21) &
    (accepted_March2020["Woodland"] <= 29) & (accepted_March2020["Woodland"] >= 9)]
    print("number passed all filters:", len(all_accepted_runs))


    # accepted parameters
    accepted_parameters = final_parameters[final_parameters['run_number'].isin(all_accepted_runs['run_number'])]
    # tag the accepted simulations
    final_results['accepted?'] = np.where(final_results['run_number'].isin(accepted_parameters['run_number']), 'Accepted', 'Rejected')

    with pd.option_context('display.max_columns',None):
        print(final_results[(final_results["Time"] == 184)])
    
    with pd.option_context('display.max_rows',None, 'display.max_columns',None):
        print("accepted_years: \n", all_accepted_runs)

    
    # calculate the time it takes to run per node, currently 8.5min for 1k runs
    stop = timeit.default_timer()
    print('Total time: ', (stop - start)) 

    return number_simulations, final_results, accepted_parameters

