# ------ ABM of the Knepp Estate (2005-2046) --------
from KneppModel_ABM import KneppModel 
from geneticAlgorithm import run_optimizer
import numpy as np
import random
import pandas as pd
import timeit


# # # # Run the model # # # # 


def run_all_models():
    output_parameters = run_optimizer()
    
    # time the program
    start = timeit.default_timer()

    # define number of simulations
    number_simulations =  100
    # make list of variables
    final_results_list = []
    final_parameters = []
    run_number = 0


    for _ in range(number_simulations):
        # choose my parameters 
        initial_roeDeer = random.randint(round(output_parameters["variable"][0]-(output_parameters["variable"][0]*0.1)), round(output_parameters["variable"][0]+(output_parameters["variable"][0]*0.1)))
        initial_grassland = random.randint(round(output_parameters["variable"][1]-(output_parameters["variable"][1]*0.1)), round(output_parameters["variable"][1]+(output_parameters["variable"][1]*0.1)))
        initial_woodland = random.randint(round(output_parameters["variable"][2]-(output_parameters["variable"][2]*0.1)), round(output_parameters["variable"][2]+(output_parameters["variable"][2]*0.1)))
        initial_scrubland = random.randint(round(output_parameters["variable"][3]-(output_parameters["variable"][3]*0.1)), round(output_parameters["variable"][3]+(output_parameters["variable"][3]*0.1)))
        # habitats
        chance_reproduceSapling = random.uniform(output_parameters["variable"][4]-(output_parameters["variable"][4]*0.1), output_parameters["variable"][4]+(output_parameters["variable"][4]*0.1))
        chance_reproduceYoungScrub = random.uniform(output_parameters["variable"][5]-(output_parameters["variable"][5]*0.1), output_parameters["variable"][5]+(output_parameters["variable"][5]*0.1))
        chance_regrowGrass = random.uniform(output_parameters["variable"][6]-(output_parameters["variable"][6]*0.1), output_parameters["variable"][6]+(output_parameters["variable"][6]*0.1))
        chance_saplingBecomingTree = random.uniform(output_parameters["variable"][7]-(output_parameters["variable"][7]*0.1), output_parameters["variable"][7]+(output_parameters["variable"][7]*0.1))
        chance_youngScrubMatures = random.uniform(output_parameters["variable"][8]-(output_parameters["variable"][8]*0.1), output_parameters["variable"][8]+(output_parameters["variable"][8]*0.1))
        # roe deer
        roeDeer_reproduce = random.uniform((output_parameters["variable"][9]-(output_parameters["variable"][9]*0.1)), (output_parameters["variable"][9]+(output_parameters["variable"][9]*0.1)))
        roeDeer_gain_from_grass = random.uniform((output_parameters["variable"][10]-(output_parameters["variable"][10]*0.1)), (output_parameters["variable"][10]+(output_parameters["variable"][10]*0.1)))
        roeDeer_gain_from_Trees = random.uniform((output_parameters["variable"][11]-(output_parameters["variable"][11]*0.1)), (output_parameters["variable"][11]+(output_parameters["variable"][11]*0.1)))
        roeDeer_gain_from_Scrub = random.uniform((output_parameters["variable"][12]-(output_parameters["variable"][12]*0.1)), (output_parameters["variable"][12]+(output_parameters["variable"][12]*0.1)))
        roeDeer_gain_from_Saplings = random.uniform((output_parameters["variable"][13]-(output_parameters["variable"][13]*0.1)), (output_parameters["variable"][13]+(output_parameters["variable"][13]*0.1)))
        roeDeer_gain_from_YoungScrub = random.uniform((output_parameters["variable"][14]-(output_parameters["variable"][14]*0.1)), (output_parameters["variable"][14]+(output_parameters["variable"][14]*0.1)))
        # Fallow deer
        fallowDeer_reproduce = random.uniform((output_parameters["variable"][15]-(output_parameters["variable"][15]*0.1)), (output_parameters["variable"][15]+(output_parameters["variable"][15]*0.1)))
        fallowDeer_gain_from_grass = random.uniform((output_parameters["variable"][16]-(output_parameters["variable"][16]*0.1)), (output_parameters["variable"][16]+(output_parameters["variable"][16]*0.1)))
        fallowDeer_gain_from_Trees = random.uniform((output_parameters["variable"][17]-(output_parameters["variable"][17]*0.1)), (output_parameters["variable"][17]+(output_parameters["variable"][17]*0.1)))
        fallowDeer_gain_from_Scrub = random.uniform((output_parameters["variable"][18]-(output_parameters["variable"][18]*0.1)), (output_parameters["variable"][18]+(output_parameters["variable"][18]*0.1)))
        fallowDeer_gain_from_Saplings = random.uniform((output_parameters["variable"][19]-(output_parameters["variable"][19]*0.1)), (output_parameters["variable"][19]+(output_parameters["variable"][19]*0.1)))
        fallowDeer_gain_from_YoungScrub = random.uniform((output_parameters["variable"][20]-(output_parameters["variable"][20]*0.1)), (output_parameters["variable"][20]+(output_parameters["variable"][20]*0.1)))
         # Red deer
        redDeer_reproduce = random.uniform((output_parameters["variable"][21]-(output_parameters["variable"][21]*0.1)), (output_parameters["variable"][21]+(output_parameters["variable"][21]*0.1)))
        redDeer_gain_from_grass = random.uniform((output_parameters["variable"][22]-(output_parameters["variable"][22]*0.1)), (output_parameters["variable"][22]+(output_parameters["variable"][22]*0.1)))
        redDeer_gain_from_Trees = random.uniform((output_parameters["variable"][23]-(output_parameters["variable"][23]*0.1)), (output_parameters["variable"][23]+(output_parameters["variable"][23]*0.1)))
        redDeer_gain_from_Scrub = random.uniform((output_parameters["variable"][24]-(output_parameters["variable"][24]*0.1)), (output_parameters["variable"][24]+(output_parameters["variable"][24]*0.1)))
        redDeer_gain_from_Saplings = random.uniform((output_parameters["variable"][25]-(output_parameters["variable"][25]*0.1)), (output_parameters["variable"][25]+(output_parameters["variable"][25]*0.1)))
        redDeer_gain_from_YoungScrub = random.uniform((output_parameters["variable"][26]-(output_parameters["variable"][26]*0.1)), (output_parameters["variable"][26]+(output_parameters["variable"][26]*0.1)))
        # Exmoor ponies
        ponies_gain_from_grass = random.uniform((output_parameters["variable"][27]-(output_parameters["variable"][27]*0.1)), (output_parameters["variable"][27]+(output_parameters["variable"][27]*0.1)))
        ponies_gain_from_Trees = random.uniform((output_parameters["variable"][28]-(output_parameters["variable"][28]*0.1)), (output_parameters["variable"][28]+(output_parameters["variable"][28]*0.1)))
        ponies_gain_from_Scrub = random.uniform((output_parameters["variable"][29]-(output_parameters["variable"][29]*0.1)), (output_parameters["variable"][29]+(output_parameters["variable"][29]*0.1)))
        ponies_gain_from_Saplings = random.uniform((output_parameters["variable"][30]-(output_parameters["variable"][30]*0.1)), (output_parameters["variable"][30]+(output_parameters["variable"][30]*0.1)))
        ponies_gain_from_YoungScrub = random.uniform((output_parameters["variable"][31]-(output_parameters["variable"][31]*0.1)), (output_parameters["variable"][31]+(output_parameters["variable"][31]*0.1)))
        # Longhorn cattle
        cows_reproduce = random.uniform((output_parameters["variable"][32]-(output_parameters["variable"][32]*0.1)), (output_parameters["variable"][32]+(output_parameters["variable"][32]*0.1)))
        cows_gain_from_grass = random.uniform((output_parameters["variable"][33]-(output_parameters["variable"][33]*0.1)), (output_parameters["variable"][33]+(output_parameters["variable"][33]*0.1)))
        cows_gain_from_Trees = random.uniform((output_parameters["variable"][34]-(output_parameters["variable"][34]*0.1)), (output_parameters["variable"][34]+(output_parameters["variable"][34]*0.1)))
        cows_gain_from_Scrub = random.uniform((output_parameters["variable"][35]-(output_parameters["variable"][35]*0.1)), (output_parameters["variable"][35]+(output_parameters["variable"][35]*0.1)))
        cows_gain_from_Saplings = random.uniform((output_parameters["variable"][36]-(output_parameters["variable"][36]*0.1)), (output_parameters["variable"][36]+(output_parameters["variable"][36]*0.1)))
        cows_gain_from_YoungScrub = random.uniform((output_parameters["variable"][37]-(output_parameters["variable"][37]*0.1)), (output_parameters["variable"][37]+(output_parameters["variable"][37]*0.1)))
        # Tamworth pigs
        pigs_reproduce = random.uniform((output_parameters["variable"][38]-(output_parameters["variable"][38]*0.1)), (output_parameters["variable"][38]+(output_parameters["variable"][38]*0.1)))
        pigs_gain_from_grass = random.uniform((output_parameters["variable"][39]-(output_parameters["variable"][39]*0.1)), (output_parameters["variable"][39]+(output_parameters["variable"][39]*0.1)))
        pigs_gain_from_Saplings = random.uniform((output_parameters["variable"][40]-(output_parameters["variable"][40]*0.1)), (output_parameters["variable"][40]+(output_parameters["variable"][40]*0.1)))
        pigs_gain_from_YoungScrub = random.uniform((output_parameters["variable"][41]-(output_parameters["variable"][41]*0.1)), (output_parameters["variable"][41]+(output_parameters["variable"][41]*0.1)))
        # impact grass
        roeDeer_impactGrass = random.randint(round(output_parameters["variable"][42]-(output_parameters["variable"][42]*0.1)), round(output_parameters["variable"][42]+(output_parameters["variable"][42]*0.1)))
        fallowDeer_impactGrass = random.randint(round(output_parameters["variable"][43]-(output_parameters["variable"][43]*0.1)),round(output_parameters["variable"][43]+(output_parameters["variable"][43]*0.1)))
        redDeer_impactGrass = random.randint(round(output_parameters["variable"][44]-(output_parameters["variable"][44]*0.1)), round(output_parameters["variable"][44]+(output_parameters["variable"][44]*0.1)))
        ponies_impactGrass = random.randint(round(output_parameters["variable"][45]-(output_parameters["variable"][45]*0.1)), round(output_parameters["variable"][45]+(output_parameters["variable"][45]*0.1)))
        cows_impactGrass = random.randint(round(output_parameters["variable"][46]-(output_parameters["variable"][46]*0.1)), round(output_parameters["variable"][46]+(output_parameters["variable"][46]*0.1)))
        pigs_impactGrass = random.randint(round(output_parameters["variable"][47]-(output_parameters["variable"][47]*0.1)), round(output_parameters["variable"][47]+(output_parameters["variable"][47]*0.1)))
        # impact saplings
        roeDeer_saplingsEaten = random.randint(round(output_parameters["variable"][48]-(output_parameters["variable"][48]*0.1)), round(output_parameters["variable"][48]+(output_parameters["variable"][48]*0.1)))
        fallowDeer_saplingsEaten = random.randint(round(output_parameters["variable"][49]-(output_parameters["variable"][49]*0.1)), round(output_parameters["variable"][49]+(output_parameters["variable"][49]*0.1)))
        redDeer_saplingsEaten = random.randint(round(output_parameters["variable"][50]-(output_parameters["variable"][50]*0.1)), round(output_parameters["variable"][50]+(output_parameters["variable"][50]*0.1)))
        ponies_saplingsEaten = random.randint(round(output_parameters["variable"][51]-(output_parameters["variable"][51]*0.1)), round(output_parameters["variable"][51]+(output_parameters["variable"][51]*0.1)))
        cows_saplingsEaten =  random.randint(round(output_parameters["variable"][52]-(output_parameters["variable"][52]*0.1)), round(output_parameters["variable"][52]+(output_parameters["variable"][52]*0.1)))
        pigs_saplingsEaten = random.randint(round(output_parameters["variable"][53]-(output_parameters["variable"][53]*0.1)), round(output_parameters["variable"][53]+(output_parameters["variable"][53]*0.1)))
        # impact young scrub
        roeDeer_youngScrubEaten = random.randint(round(output_parameters["variable"][54]-(output_parameters["variable"][54]*0.1)), round(output_parameters["variable"][54]+(output_parameters["variable"][54]*0.1)))
        fallowDeer_youngScrubEaten = random.randint(round(output_parameters["variable"][55]-(output_parameters["variable"][55]*0.1)), round(output_parameters["variable"][55]+(output_parameters["variable"][55]*0.1)))
        redDeer_youngScrubEaten = random.randint(round(output_parameters["variable"][56]-(output_parameters["variable"][56]*0.1)), round(output_parameters["variable"][56]+(output_parameters["variable"][56]*0.1)))
        ponies_youngScrubEaten = random.randint(round(output_parameters["variable"][57]-(output_parameters["variable"][57]*0.1)), round(output_parameters["variable"][57]+(output_parameters["variable"][57]*0.1)))
        cows_youngScrubEaten = random.randint(round(output_parameters["variable"][58]-(output_parameters["variable"][58]*0.1)), round(output_parameters["variable"][58]+(output_parameters["variable"][58]*0.1)))
        pigs_youngScrubEaten = random.randint(round(output_parameters["variable"][59]-(output_parameters["variable"][59]*0.1)), round(output_parameters["variable"][59]+(output_parameters["variable"][59]*0.1)))
        # impact scrub
        roeDeer_scrubEaten = random.randint(round(output_parameters["variable"][60]-(output_parameters["variable"][60]*0.1)), round(output_parameters["variable"][60]+(output_parameters["variable"][60]*0.1)))
        fallowDeer_scrubEaten = random.randint(round(output_parameters["variable"][61]-(output_parameters["variable"][61]*0.1)), round(output_parameters["variable"][61]+(output_parameters["variable"][61]*0.1)))
        redDeer_scrubEaten = random.randint(round(output_parameters["variable"][62]-(output_parameters["variable"][62]*0.1)), round(output_parameters["variable"][62]+(output_parameters["variable"][62]*0.1)))
        ponies_scrubEaten = random.randint(round(output_parameters["variable"][63]-(output_parameters["variable"][63]*0.1)), round(output_parameters["variable"][63]+(output_parameters["variable"][63]*0.1)))
        cows_scrubEaten = random.randint(round(output_parameters["variable"][64]-(output_parameters["variable"][64]*0.1)), round(output_parameters["variable"][64]+(output_parameters["variable"][64]*0.1)))
        # impact trees
        roeDeer_treesEaten = random.randint(round(output_parameters["variable"][65]-(output_parameters["variable"][65]*0.1)), round(output_parameters["variable"][65]+(output_parameters["variable"][65]*0.1)))
        fallowDeer_treesEaten = random.randint(round(output_parameters["variable"][66]-(output_parameters["variable"][66]*0.1)), round(output_parameters["variable"][66]+(output_parameters["variable"][66]*0.1)))
        redDeer_treesEaten = random.randint(round(output_parameters["variable"][67]-(output_parameters["variable"][67]*0.1)), round(output_parameters["variable"][67]+(output_parameters["variable"][67]*0.1)))
        ponies_treesEaten = random.randint(round(output_parameters["variable"][68]-(output_parameters["variable"][68]*0.1)), round(output_parameters["variable"][68]+(output_parameters["variable"][68]*0.1)))
        cows_treesEaten =  random.randint(round(output_parameters["variable"][69]-(output_parameters["variable"][69]*0.1)), round(output_parameters["variable"][69]+(output_parameters["variable"][69]*0.1)))


        # keep track of my parameters
        parameters_used = [
            run_number,
            chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
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
    print(final_parameters['initial_grassland'].min())
    print(final_parameters['initial_grassland'].max())

    # filter the runs and tag the dataframe
    # pre-reintroduction model
    accepted_preReintro = final_results[(final_results["Time"] == 49) &
    (final_results["Roe deer"] <= 40) & (final_results["Roe deer"] >= 6) &
    (final_results["Grassland"] <= 90) & (final_results["Grassland"] >= 49) & 
    (final_results["Woodland"] <= 27) & (final_results["Woodland"] >= 7) & 
    (final_results["Thorny Scrub"] <= 21) & (final_results["Thorny Scrub"] >= 1)]
    print("number passed pre-reintro filters:", len(accepted_preReintro))
    # # # April 2015
    # accepted_April2015 = accepted_preReintro[(accepted_preReintro["Time"] == 123) &
    # (accepted_preReintro["Longhorn cattle"] <= 127) & (accepted_preReintro["Longhorn cattle"] >= 104) &
    # (accepted_preReintro["Tamworth pigs"] <= 24) & (accepted_preReintro["Tamworth pigs"] >= 20)]
    # print("number passed April 2015 filters:", len(accepted_April2015))
    # # May 2015
    # accepted_May2015 = accepted_April2015[(accepted_April2015["Time"] == 124) &
    # (accepted_April2015["Longhorn cattle"] <= 142) & (accepted_April2015["Longhorn cattle"] >= 116)]
    # print("number passed May 2015 filters:", len(accepted_May2015))
    # # June 2015
    # accepted_June2015 = accepted_May2015[(accepted_May2015["Time"] == 125) &
    # (accepted_May2015["Longhorn cattle"] <= 142) & (accepted_May2015["Longhorn cattle"] >= 116)]
    # print("number passed June 2015 filters:", len(accepted_June2015))
    # # Feb 2016
    # accepted_Feb2016 = accepted_June2015[(accepted_June2015["Time"] == 133) &
    # (accepted_June2015["Exmoor pony"] == 10)]
    # print("number passed February 2016 filters:", len(accepted_Feb2016))
    # # March 2016
    # accepted_March2016 = accepted_Feb2016[(accepted_Feb2016["Time"] == 134) &
    # (accepted_Feb2016["Fallow deer"] <= 154) & (accepted_Feb2016["Fallow deer"] >= 126) &
    # (accepted_Feb2016["Red deer"] <= 29) & (accepted_Feb2016["Red deer"] >= 23) &
    # (accepted_Feb2016["Tamworth pigs"] <= 10) & (accepted_Feb2016["Tamworth pigs"] >= 8)]
    # print("number passed March 2016 filters:", len(accepted_March2016))
    # # April 2016
    # accepted_April2016 = accepted_March2016[(accepted_March2016["Time"] == 135) &
    # (accepted_March2016["Longhorn cattle"] <= 113) & (accepted_March2016["Longhorn cattle"] >= 93)]
    # print("number passed April 2016 filters:", len(accepted_April2016))
    # # May 2016
    # accepted_May2016 = accepted_April2016[(accepted_April2016["Time"] == 136) &
    # (accepted_April2016["Longhorn cattle"] <= 119) & (accepted_April2016["Longhorn cattle"] >= 97) &
    # (accepted_April2016["Tamworth pigs"] <= 19) & (accepted_April2016["Tamworth pigs"] >= 15)]
    # print("number passed May 2016 filters:", len(accepted_May2016))
    # # June 2016
    # accepted_June2016 = accepted_May2016[(accepted_May2016["Time"] == 137) &
    # (accepted_May2016["Longhorn cattle"] <= 98) & (accepted_May2016["Longhorn cattle"] >= 80)]
    # print("number passed June 2016 filters:", len(accepted_June2016))
    # # Feb 2017
    # accepted_Feb2017 = accepted_June2016[(accepted_June2016["Time"] == 145) &
    # (accepted_June2016["Exmoor pony"] == 11)]
    # print("number passed Feb 2017 filters:", len(accepted_Feb2017))
    # # March 2017
    # accepted_March2017 = accepted_Feb2017[(accepted_Feb2017["Time"] == 146) &
    # (accepted_Feb2017["Fallow deer"] <= 182) & (accepted_Feb2017["Fallow deer"] >= 149) ]
    # print("number passed March 2017 filters:", len(accepted_March2017))
    # # April 2017
    # accepted_April2017 = accepted_March2017[(accepted_March2017["Time"] == 147) &
    # (accepted_March2017["Longhorn cattle"] <= 110) & (accepted_March2017["Longhorn cattle"] >= 90) &
    # (accepted_March2017["Tamworth pigs"] <= 24) & (accepted_March2017["Tamworth pigs"] >= 20)]
    # print("number passed April 2017 filters:", len(accepted_April2017))
    # # May 2017
    # accepted_May2017 = accepted_April2017[(accepted_April2017["Time"] == 148) &
    # (accepted_April2017["Longhorn cattle"] <= 120) & (accepted_April2017["Longhorn cattle"] >= 98)]
    # print("number passed May 2017 filters:", len(accepted_May2017))
    # # June 2017
    # accepted_June2017 = accepted_May2017[(accepted_May2017["Time"] == 149) &
    # (accepted_May2017["Longhorn cattle"] <= 103) & (accepted_May2017["Longhorn cattle"] >= 85)]
    # print("number passed June 2017 filters:", len(accepted_June2017))
    # # January 2018
    # accepted_Jan2018 = accepted_June2017[(accepted_June2017["Time"] == 156) &
    # (accepted_June2017["Tamworth pigs"] <= 13) & (accepted_June2017["Tamworth pigs"] >= 11)]
    # print("number passed January 2018 filters:", len(accepted_Jan2018))
    # # February 2018
    # accepted_Feb2018 = accepted_Jan2018[(accepted_Jan2018["Time"] == 157) &
    # (accepted_Jan2018["Tamworth pigs"] <= 18) & (accepted_Jan2018["Tamworth pigs"] >= 14) &
    # (accepted_Jan2018["Exmoor pony"] == 10)]
    # print("number passed Feb 2018 filters:", len(accepted_Feb2018)) 
    # # March 2018
    # accepted_March2018 = accepted_Feb2018[(accepted_Feb2018["Time"] == 158) &
    # (accepted_Feb2018["Fallow deer"] <= 276) & (accepted_Feb2018["Fallow deer"] >= 226) &
    # (accepted_Feb2018["Red deer"] <= 26) & (accepted_Feb2018["Red deer"] >= 22)]
    # print("number passed March 2018 filters:", len(accepted_March2018)) 
    # # April 2018
    # accepted_April2018 = accepted_March2018[(accepted_March2018["Time"] == 159) &
    # (accepted_March2018["Longhorn cattle"] <= 111) & (accepted_March2018["Longhorn cattle"] >= 91)]
    # print("number passed April 2018 filters:", len(accepted_April2018)) 
    #  # May 2018
    # accepted_May2018 = accepted_April2018[(accepted_April2018["Time"] == 160) &
    # (accepted_April2018["Longhorn cattle"] <= 129) & (accepted_April2018["Longhorn cattle"] >= 105) &
    # (accepted_April2018["Tamworth pigs"] <= 25) & (accepted_April2018["Tamworth pigs"] >= 21)]
    # print("number passed May 2018 filters:", len(accepted_May2018)) 
    # # June 2018
    # accepted_June2018 = accepted_May2018[(accepted_May2018["Time"] == 161) &
    # (accepted_May2018["Longhorn cattle"] <= 113) & (accepted_May2018["Longhorn cattle"] >= 93)]
    # print("number passed June 2018 filters:", len(accepted_June2018)) 
    # # March 2019
    # accepted_March2019 = accepted_June2018[(accepted_June2018["Time"] == 170) &
    # (accepted_June2018["Fallow deer"] <= 306) & (accepted_June2018["Fallow deer"] >= 250) &
    # (accepted_June2018["Red deer"] <= 41) & (accepted_June2018["Red deer"] >= 33)]
    # print("number passed March 2019 filters:", len(accepted_March2019)) 
    # # April 2019
    # accepted_April2019 = accepted_March2019[(accepted_March2019["Time"] == 171) &
    # (accepted_March2019["Longhorn cattle"] <= 111) & (accepted_March2019["Longhorn cattle"] >= 91)]
    # print("number passed April 2019 filters:", len(accepted_April2019)) 
    # # May 2019
    # accepted_May2019 = accepted_April2019[(accepted_April2019["Time"] == 172) &
    # (accepted_April2019["Longhorn cattle"] <= 121) & (accepted_April2019["Longhorn cattle"] >= 99)]
    # print("number passed May 2019 filters:", len(accepted_May2019))
    # # June 2019
    # accepted_June2019 = accepted_May2019[(accepted_May2019["Time"] == 173) &
    # (accepted_May2019["Longhorn cattle"] <= 98) & (accepted_May2019["Longhorn cattle"] >= 80)]
    # print("number passed June 2019 filters:", len(accepted_June2019)) 
    # # July 2019
    # accepted_July2019 = accepted_June2019[(accepted_June2019["Time"] == 174) &
    # (accepted_June2019["Tamworth pigs"] <= 10) & (accepted_June2019["Tamworth pigs"] >= 8)]
    # print("number passed July 2019 filters:", len(accepted_July2019)) 
    # # March 2020
    # accepted_March2020 = accepted_July2019[(accepted_July2019["Time"] == 182) &
    # (accepted_July2019["Fallow deer"] <= 272) & (accepted_July2019["Fallow deer"] >= 222) &
    # (accepted_July2019["Red deer"] <= 39) & (accepted_July2019["Red deer"] >= 32)]
    # print("number passed March 2020 filters:", len(accepted_March2020)) 
    # # May 2020
    # all_accepted_runs = accepted_March2020[(accepted_March2020["Time"] == 184) &
    # (accepted_March2020["Tamworth pigs"] <= 21) & (accepted_March2020["Tamworth pigs"] >= 17) &
    # (accepted_March2020["Exmoor pony"] == 15) &
    # (accepted_March2020["Roe deer"] <= 40) & (accepted_March2020["Roe deer"] >= 20) &
    # (accepted_March2020["Grassland"] <= 69) & (accepted_March2020["Grassland"] >= 49) &
    # (accepted_March2020["Thorny Scrub"] <= 35) & (accepted_March2020["Thorny Scrub"] >= 21) &
    # (accepted_March2020["Woodland"] <= 29) & (accepted_March2020["Woodland"] >= 9)]
    # print("number passed all filters:", len(all_accepted_runs))


    # accepted parameters
    accepted_parameters = final_parameters[final_parameters['run_number'].isin(accepted_preReintro['run_number'])]
    # tag the accepted simulations
    final_results['accepted?'] = np.where(final_results['run_number'].isin(accepted_parameters['run_number']), 'Accepted', 'Rejected')

    # with pd.option_context('display.max_columns',None):
    #     print(final_results[(final_results["Time"] == 184)])
  
    final_results.to_excel("output.xlsx")
    final_parameters.to_excel("parameters.xlsx")


    
    with pd.option_context('display.max_columns',None):
        print("accepted_years: \n", accepted_preReintro)


    # # accepted parameters
    # accepted_parameters = final_parameters[final_parameters['run_number'].isin(all_accepted_runs['run_number'])]
    # # tag the accepted simulations
    # final_results['accepted?'] = np.where(final_results['run_number'].isin(accepted_parameters['run_number']), 'Accepted', 'Rejected')

    # with pd.option_context('display.max_columns',None):
    #     print(final_results[(final_results["Time"] == 184)])
    
    # with pd.option_context('display.max_rows',None, 'display.max_columns',None):
    #     print("accepted_years: \n", all_accepted_runs)

    
    # calculate the time it takes to run per node, currently 8.5min for 1k runs
    stop = timeit.default_timer()
    print('Total time: ', (stop - start)) 

    return number_simulations, final_results, accepted_parameters

