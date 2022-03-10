# ------ ABM of the Knepp Estate (2005-2046) --------
from KneppModel_ABM import KneppModel 
import numpy as np
import random
import pandas as pd


# # # # Run the model # # # # 


def run_all_models():

    # define number of simulations
    number_simulations =  100
    # make list of variables
    final_results_list = []
    final_parameters = []
    run_number = 0


    for _ in range(number_simulations):
        # keep track of the runs
        run_number += 1
        print(run_number)
        # choose my percent above/below number
        perc_aboveBelow = 0.1

        # define the parameters
        chance_reproduceSapling = random.uniform(0.01599083-(0.01599083*perc_aboveBelow), 0.01599083+(0.01599083*perc_aboveBelow))
        chance_reproduceYoungScrub = random.uniform(0.05596995-(0.05596995*perc_aboveBelow), 0.05596995+(0.05596995*perc_aboveBelow))

        chance_regrowGrass = random.uniform(0.0841251-(0.0841251*perc_aboveBelow), 0.0841251+(0.0841251*perc_aboveBelow))
        chance_saplingBecomingTree = random.uniform(0.00212349-(0.00212349*perc_aboveBelow), 0.00212349+(0.00212349*perc_aboveBelow))
        chance_youngScrubMatures =random.uniform(0.01186857-(0.01186857*perc_aboveBelow), 0.01186857+(0.01186857*perc_aboveBelow))
        chance_scrubOutcompetedByTree = random.uniform(0.00880328-(0.00880328*perc_aboveBelow), 0.00880328+(0.00880328*perc_aboveBelow))

        chance_grassOutcompetedByTree = random.uniform(0.17032938-(0.17032938*perc_aboveBelow), 0.17032938+(0.17032938*perc_aboveBelow))
        chance_grassOutcompetedByScrub = random.uniform(0.17482715-(0.17482715*perc_aboveBelow), 0.17482715+(0.17482715*perc_aboveBelow))
        chance_saplingOutcompetedByTree = random.uniform(0.06540329-(0.06540329*perc_aboveBelow), 0.06540329+(0.06540329*perc_aboveBelow))
        chance_saplingOutcompetedByScrub = random.uniform(0.02308093-(0.02308093*perc_aboveBelow), 0.02308093+(0.02308093*perc_aboveBelow))
        chance_youngScrubOutcompetedByScrub =random.uniform(0.06625781-(0.06625781*perc_aboveBelow), 0.06625781+(0.06625781*perc_aboveBelow))
        chance_youngScrubOutcompetedByTree = random.uniform(0.06854397-(0.06854397*perc_aboveBelow), 0.06854397+(0.06854397*perc_aboveBelow))

        # initial values
        initial_roeDeer = 0.12
        initial_grassland = 0.8
        initial_woodland = 0.14
        initial_scrubland = 0.01
        # roe deer
        roeDeer_reproduce = random.uniform(0.18321307-(0.18321307*perc_aboveBelow), 0.18321307+(0.18321307*perc_aboveBelow))
        roeDeer_gain_from_grass = random.uniform(0.91357378-(0.91357378*perc_aboveBelow), 0.91357378+(0.91357378*perc_aboveBelow))
        roeDeer_gain_from_Trees =random.uniform(0.86834529-(0.86834529*perc_aboveBelow), 0.86834529+(0.86834529*perc_aboveBelow))
        roeDeer_gain_from_Scrub =random.uniform(0.93482336-(0.93482336*perc_aboveBelow), 0.93482336+(0.93482336*perc_aboveBelow))
        roeDeer_gain_from_Saplings = random.uniform(0.13490778-(0.13490778*perc_aboveBelow), 0.13490778+(0.13490778*perc_aboveBelow))
        roeDeer_gain_from_YoungScrub = random.uniform(0.11024164-(0.11024164*perc_aboveBelow), 0.11024164+(0.11024164*perc_aboveBelow))
        # Fallow deer
        fallowDeer_reproduce = random.uniform(0.37292093-(0.37292093*perc_aboveBelow), 0.37292093+(0.37292093*perc_aboveBelow))
        fallowDeer_gain_from_grass = random.uniform(0.91237466-(0.91237466*perc_aboveBelow), 0.91237466+(0.91237466*perc_aboveBelow))
        fallowDeer_gain_from_Trees = random.uniform(0.87144027-(0.87144027*perc_aboveBelow), 0.87144027+(0.87144027*perc_aboveBelow))
        fallowDeer_gain_from_Scrub = random.uniform(0.86708181-(0.86708181*perc_aboveBelow), 0.86708181+(0.86708181*perc_aboveBelow))
        fallowDeer_gain_from_Saplings = random.uniform(0.13661793-(0.13661793*perc_aboveBelow), 0.13661793+(0.13661793*perc_aboveBelow))
        fallowDeer_gain_from_YoungScrub = random.uniform(0.11656884-(0.11656884*perc_aboveBelow), 0.11656884+(0.11656884*perc_aboveBelow))
        # Red deer
        redDeer_reproduce = random.uniform(0.39482522-(0.39482522*perc_aboveBelow), 0.39482522+(0.39482522*perc_aboveBelow))
        redDeer_gain_from_grass = random.uniform(0.92850426-(0.92850426*perc_aboveBelow), 0.92850426+(0.92850426*perc_aboveBelow))
        redDeer_gain_from_Trees = random.uniform(0.92358395-(0.92358395*perc_aboveBelow), 0.92358395+(0.92358395*perc_aboveBelow))
        redDeer_gain_from_Scrub = random.uniform(0.91620809-(0.91620809*perc_aboveBelow), 0.91620809+(0.91620809*perc_aboveBelow))
        redDeer_gain_from_Saplings = random.uniform(0.11779972-(0.11779972*perc_aboveBelow), 0.11779972+(0.11779972*perc_aboveBelow))
        redDeer_gain_from_YoungScrub = random.uniform(0.09440902-(0.09440902*perc_aboveBelow), 0.09440902+(0.09440902*perc_aboveBelow))
        # Exmoor ponies
        ponies_gain_from_grass = random.uniform(0.90086234-(0.90086234*perc_aboveBelow), 0.90086234+(0.90086234*perc_aboveBelow))
        ponies_gain_from_Trees = random.uniform(0.87800124-(0.87800124*perc_aboveBelow), 0.87800124+(0.87800124*perc_aboveBelow)) 
        ponies_gain_from_Scrub = random.uniform(0.8764282-(0.8764282*perc_aboveBelow), 0.8764282+(0.8764282*perc_aboveBelow))
        ponies_gain_from_Saplings = random.uniform(0.07381227-(0.07381227*perc_aboveBelow), 0.07381227+(0.07381227*perc_aboveBelow))
        ponies_gain_from_YoungScrub = random.uniform(0.09842013-(0.09842013*perc_aboveBelow), 0.09842013+(0.09842013*perc_aboveBelow))
        # Longhorn cattle
        cows_reproduce = random.uniform(0.19456058-(0.19456058*perc_aboveBelow), 0.19456058+(0.19456058*perc_aboveBelow))
        cows_gain_from_grass = random.uniform(0.89778476-(0.89778476*perc_aboveBelow), 0.89778476+(0.89778476*perc_aboveBelow))
        cows_gain_from_Trees = random.uniform(0.89226723-(0.89226723*perc_aboveBelow), 0.89226723+(0.89226723*perc_aboveBelow))
        cows_gain_from_Scrub = random.uniform(0.87588117-(0.87588117*perc_aboveBelow), 0.87588117+(0.87588117*perc_aboveBelow))
        cows_gain_from_Saplings = random.uniform(0.09952247-(0.09952247*perc_aboveBelow), 0.09952247+(0.09952247*perc_aboveBelow))
        cows_gain_from_YoungScrub = random.uniform(0.06801822-(0.06801822*perc_aboveBelow), 0.06801822+(0.06801822*perc_aboveBelow))
        # Tamworth pigs
        pigs_reproduce = random.uniform(0.26223023-(0.26223023*perc_aboveBelow), 0.26223023+(0.26223023*perc_aboveBelow))
        pigs_gain_from_grass = random.uniform(0.81523531-(0.81523531*perc_aboveBelow), 0.81523531+(0.81523531*perc_aboveBelow))
        pigs_gain_from_Trees =random.uniform(0.87275063-(0.87275063*perc_aboveBelow), 0.87275063+(0.87275063*perc_aboveBelow))
        pigs_gain_from_Scrub = random.uniform(0.89307688-(0.89307688*perc_aboveBelow), 0.89307688+(0.89307688*perc_aboveBelow))
        pigs_gain_from_Saplings = random.uniform(0.11723434-(0.11723434*perc_aboveBelow), 0.11723434+(0.11723434*perc_aboveBelow))
        pigs_gain_from_YoungScrub = random.uniform(0.08835914-(0.08835914*perc_aboveBelow), 0.08835914+(0.08835914*perc_aboveBelow))
        # starting conditions for saplings and young scrub
        max_start_saplings = 0.1
        max_start_youngScrub = 0.1

        # keep track of my parameters
        parameters_used = [
        chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
        chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
        initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland, 
        roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
        ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
        cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
        fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
        redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
        pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Trees, pigs_gain_from_Scrub, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
        max_start_saplings, max_start_youngScrub, run_number]

        # append to dataframe
        final_parameters.append(parameters_used)

        model = KneppModel(
            chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
            chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
            initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland, 
            roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
            ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
            cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
            fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
            redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
            pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Trees, pigs_gain_from_Scrub, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
            max_start_saplings, max_start_youngScrub,
            width = 25, height = 18, max_time = 184, reintroduction = True, 
            RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)

        model.run_model()

        # remember the results of the model (dominant conditions, # of agents)
        results = model.datacollector.get_model_vars_dataframe()
        results['run_number'] = run_number
        final_results_list.append(results)
    
    # append to dataframe
    final_results = pd.concat(final_results_list)

    variables = [
        "chance_reproduceSapling", "chance_reproduceYoungScrub", "chance_regrowGrass", "chance_saplingBecomingTree", "chance_youngScrubMatures", 
        "chance_scrubOutcompetedByTree", "chance_grassOutcompetedByTree", "chance_grassOutcompetedByScrub", "chance_saplingOutcompetedByTree", "chance_saplingOutcompetedByScrub", "chance_youngScrubOutcompetedByScrub", "chance_youngScrubOutcompetedByTree",
        "initial_roeDeer", "initial_grassland", "initial_woodland", "initial_scrubland", 
        "roeDeer_reproduce", "roeDeer_gain_from_grass", "roeDeer_gain_from_Trees", "roeDeer_gain_from_Scrub", "roeDeer_gain_from_Saplings", "roeDeer_gain_from_YoungScrub",
        "ponies_gain_from_grass", "ponies_gain_from_Trees", "ponies_gain_from_Scrub", "ponies_gain_from_Saplings", "ponies_gain_from_YoungScrub", 
        "cows_reproduce", "cows_gain_from_grass", "cows_gain_from_Trees", "cows_gain_from_Scrub", "cows_gain_from_Saplings", "cows_gain_from_YoungScrub", 
        "fallowDeer_reproduce", "fallowDeer_gain_from_grass", "fallowDeer_gain_from_Trees", "fallowDeer_gain_from_Scrub", "fallowDeer_gain_from_Saplings", "fallowDeer_gain_from_YoungScrub", 
        "redDeer_reproduce", "redDeer_gain_from_grass", "redDeer_gain_from_Trees", "redDeer_gain_from_Scrub", "redDeer_gain_from_Saplings", "redDeer_gain_from_YoungScrub", 
        "pigs_reproduce", "pigs_gain_from_grass", "pigs_gain_from_Trees", "pigs_gain_from_Scrub", "pigs_gain_from_Saplings", "pigs_gain_from_YoungScrub", 
        "max_start_saplings", "max_start_youngScrub", "run_number"]

    # check out the parameters used
    final_parameters = pd.DataFrame(data=final_parameters, columns=variables)


    # filter the runs and tag the dataframe
    # pre-reintroduction model
    accepted_preReintro = final_results[(final_results["Time"] == 50) &
    (final_results["Roe deer"] <= 40) & (final_results["Roe deer"] >= 6) &
    (final_results["Grassland"] <= 90) & (final_results["Grassland"] >= 49) & 
    (final_results["Woodland"] <= 27) & (final_results["Woodland"] >= 7) & 
    (final_results["Thorny Scrub"] <= 21) & (final_results["Thorny Scrub"] >= 1)]
    print("number passed pre-reintro filters:", len(accepted_preReintro))
    filtered_preReintro = final_results[final_results['run_number'].isin(accepted_preReintro['run_number'])]
    # April 2015
    accepted_April2015 = filtered_preReintro[(filtered_preReintro["Time"] == 123) &
    (filtered_preReintro["Exmoor pony"] <= 11) & (filtered_preReintro["Exmoor pony"] >= 9) &
    # (filtered_preReintro["Longhorn cattle"] <= 127) & (filtered_preReintro["Longhorn cattle"] >= 104)]
    (filtered_preReintro["Tamworth pigs"] <= 32) & (filtered_preReintro["Tamworth pigs"] >= 12)]
    print("number passed April 2015 filters:", len(accepted_April2015))
    filtered_April2015 = filtered_preReintro[filtered_preReintro['run_number'].isin(accepted_April2015['run_number'])]
    # May 2015
    accepted_May2015 = filtered_April2015[(filtered_April2015["Time"] == 124) &
    # (filtered_April2015["Longhorn cattle"] <= 142) & (filtered_April2015["Longhorn cattle"] >= 116) &
    (filtered_April2015["Tamworth pigs"] <= 24) & (filtered_April2015["Tamworth pigs"] >= 4) &
    (filtered_April2015["Exmoor pony"] <= 11) & (filtered_April2015["Exmoor pony"] >= 9)]
    print("number passed May 2015 filters:", len(accepted_May2015))
    filtered_May2015 = filtered_April2015[filtered_April2015['run_number'].isin(accepted_May2015['run_number'])]
    # June 2015
    accepted_June2015 = filtered_May2015[(filtered_May2015["Time"] == 125) &
    # (filtered_May2015["Longhorn cattle"] <= 142) & (filtered_May2015["Longhorn cattle"] >= 116) &
    (filtered_May2015["Exmoor pony"] <= 11) & (filtered_May2015["Exmoor pony"] >= 9) &
    (filtered_May2015["Tamworth pigs"] <= 24) & (filtered_May2015["Tamworth pigs"] >= 4)]
    print("number passed June 2015 filters:", len(accepted_June2015))
    filtered_June2015 = filtered_May2015[filtered_May2015['run_number'].isin(accepted_June2015['run_number'])]
    # July 2015
    accepted_July2015 = filtered_June2015[(filtered_June2015["Time"] == 126) &
    # (filtered_June2015["Longhorn cattle"] <= 142) & (filtered_June2015["Longhorn cattle"] >= 116) &
    (filtered_June2015["Exmoor pony"] <= 11) & (filtered_June2015["Exmoor pony"] >= 9) &
    (filtered_June2015["Tamworth pigs"] <= 24) & (filtered_June2015["Tamworth pigs"] >= 4)]
    print("number passed July 2015 filters:", len(accepted_July2015))
    filtered_July2015 = filtered_June2015[filtered_June2015['run_number'].isin(accepted_July2015['run_number'])]
    # Aug 2015
    accepted_Aug2015 = filtered_July2015[(filtered_July2015["Time"] == 127) &
    # (filtered_July2015["Longhorn cattle"] <= 142) & (filtered_July2015["Longhorn cattle"] >= 116) &
    (filtered_July2015["Exmoor pony"] <= 11) & (filtered_July2015["Exmoor pony"] >= 9) &
    (filtered_July2015["Tamworth pigs"] <= 24) & (filtered_July2015["Tamworth pigs"] >= 4)]
    print("number passed Aug 2015 filters:", len(accepted_Aug2015))
    filtered_Aug2015 = filtered_July2015[filtered_July2015['run_number'].isin(accepted_Aug2015['run_number'])]
    # Sept 2015
    accepted_Sept2015 = filtered_Aug2015[(filtered_Aug2015["Time"] == 128) &
    # (filtered_Aug2015["Longhorn cattle"] <= 143) & (filtered_Aug2015["Longhorn cattle"] >= 117) &
    (filtered_Aug2015["Exmoor pony"] <= 11) & (filtered_Aug2015["Exmoor pony"] >= 9) &
    (filtered_Aug2015["Tamworth pigs"] <= 24) & (filtered_Aug2015["Tamworth pigs"] >= 4)]
    print("number passed Sept 2015 filters:", len(accepted_Sept2015))
    filtered_Sept2015 = filtered_Aug2015[filtered_Aug2015['run_number'].isin(accepted_Sept2015['run_number'])]
    # Oct 2015
    accepted_Oct2015 = filtered_Sept2015[(filtered_Sept2015["Time"] == 129) &
    # (filtered_Sept2015["Longhorn cattle"] <= 100) & (filtered_Sept2015["Longhorn cattle"] >= 82) &
    (filtered_Sept2015["Exmoor pony"] <= 11) & (filtered_Sept2015["Exmoor pony"] >= 9) &
    (filtered_Sept2015["Tamworth pigs"] <= 24) & (filtered_Sept2015["Tamworth pigs"] >= 4)]
    print("number passed Oct 2015 filters:", len(accepted_Oct2015))
    filtered_Oct2015 = filtered_Sept2015[filtered_Sept2015['run_number'].isin(accepted_Oct2015['run_number'])]
    # Nov 2015
    accepted_Nov2015 = filtered_Oct2015[(filtered_Oct2015["Time"] == 130) &
    # (filtered_Oct2015["Longhorn cattle"] <= 100) & (filtered_Oct2015["Longhorn cattle"] >= 82) &
    (filtered_Oct2015["Exmoor pony"] <= 11) & (filtered_Oct2015["Exmoor pony"] >= 9) &
    (filtered_Oct2015["Tamworth pigs"] <= 23) & (filtered_Oct2015["Tamworth pigs"] >= 3)]
    print("number passed Nov 2015 filters:", len(accepted_Nov2015))
    filtered_Nov2015 = filtered_Oct2015[filtered_Oct2015['run_number'].isin(accepted_Nov2015['run_number'])]
    # Dec 2015
    accepted_Dec2015 = filtered_Nov2015[(filtered_Nov2015["Time"] == 131) &
    # (filtered_Nov2015["Longhorn cattle"] <= 94) & (filtered_Nov2015["Longhorn cattle"] >= 77) &
    (filtered_Nov2015["Exmoor pony"] <= 11) & (filtered_Nov2015["Exmoor pony"] >= 9) &
    (filtered_Nov2015["Tamworth pigs"] <= 23) & (filtered_Nov2015["Tamworth pigs"] >= 3)]
    print("number passed Dec 2015 filters:", len(accepted_Dec2015))
    filtered_Dec2015 = filtered_Nov2015[filtered_Nov2015['run_number'].isin(accepted_Dec2015['run_number'])]
    # Jan 2016
    accepted_Jan2016 = filtered_Dec2015[(filtered_Dec2015["Time"] == 132) &
    # (filtered_Dec2015["Longhorn cattle"] <= 94) & (filtered_Dec2015["Longhorn cattle"] >= 77) &
    (filtered_Dec2015["Exmoor pony"] <= 11) & (filtered_Dec2015["Exmoor pony"] >= 9) &
    (filtered_Dec2015["Tamworth pigs"] <= 20) & (filtered_Dec2015["Tamworth pigs"] >= 1)]
    print("number passed Jan 2016 filters:", len(accepted_Jan2016))
    filtered_Jan2016 = filtered_Dec2015[filtered_Dec2015['run_number'].isin(accepted_Jan2016['run_number'])]
    # Feb 2016
    accepted_Feb2016 = filtered_Jan2016[(filtered_Jan2016["Time"] == 133) &
    (filtered_Jan2016["Exmoor pony"] <= 11) & (filtered_Jan2016["Exmoor pony"] >= 9) &
    # (filtered_Jan2016["Longhorn cattle"] <= 94) & (filtered_Jan2016["Longhorn cattle"] >= 77)]
    (filtered_Jan2016["Tamworth pigs"] <= 20) & (filtered_Jan2016["Tamworth pigs"] >= 1)]
    print("number passed February 2016 filters:", len(accepted_Feb2016))
    filtered_Feb2016 = filtered_Jan2016[filtered_Jan2016['run_number'].isin(accepted_Feb2016['run_number'])]
    
    
    # March 2016
    accepted_March2016 = filtered_Feb2016[(filtered_Feb2016["Time"] == 134) &
    (filtered_Feb2016["Exmoor pony"] <= 12) & (filtered_Feb2016["Exmoor pony"] >= 10) &
    # (filtered_Feb2016["Longhorn cattle"] <= 94) & (filtered_Feb2016["Longhorn cattle"] >= 77) &
    # (filtered_Feb2016["Fallow deer"] <= 154) & (filtered_Feb2016["Fallow deer"] >= 126) &
    # (filtered_Feb2016["Red deer"] <= 29) & (filtered_Feb2016["Red deer"] >= 23)]
    (filtered_Feb2016["Tamworth pigs"] <= 19) & (filtered_Feb2016["Tamworth pigs"] >= 1)]
    print("number passed March 2016 filters:", len(accepted_March2016))
    filtered_March2016 = filtered_Feb2016[filtered_Feb2016['run_number'].isin(accepted_March2016['run_number'])]
    # April 2016
    accepted_April2016 = filtered_March2016[(filtered_March2016["Time"] == 135) &
    (filtered_March2016["Exmoor pony"] <= 12) & (filtered_March2016["Exmoor pony"] >= 10) &
    # (filtered_March2016["Longhorn cattle"] <= 113) & (filtered_March2016["Longhorn cattle"] >= 93)]
    (filtered_March2016["Tamworth pigs"] <= 19) & (filtered_March2016["Tamworth pigs"] >= 1)]
    print("number passed April 2016 filters:", len(accepted_April2016))
    filtered_April2016 = filtered_March2016[filtered_March2016['run_number'].isin(accepted_April2016['run_number'])]
    # May 2016
    accepted_May2016 = filtered_April2016[(filtered_April2016["Time"] == 136) &
    (filtered_April2016["Exmoor pony"] <= 12) & (filtered_April2016["Exmoor pony"] >= 10) &
    # (filtered_April2016["Longhorn cattle"] <= 119) & (filtered_April2016["Longhorn cattle"] >= 97)]
    (filtered_April2016["Tamworth pigs"] <= 27) & (filtered_April2016["Tamworth pigs"] >= 7)]
    # print("number passed May 2016 filters:", len(accepted_May2016))
    # filtered_May2016 = filtered_April2016[filtered_April2016['run_number'].isin(accepted_May2016['run_number'])]
    # June 2016
    accepted_June2016 = filtered_May2016[(filtered_May2016["Time"] == 137) &
    (filtered_May2016["Exmoor pony"] <= 12) & (filtered_May2016["Exmoor pony"] >= 10) &
    # (filtered_May2016["Longhorn cattle"] <= 98) & (filtered_May2016["Longhorn cattle"] >= 80)]
    (filtered_May2016["Tamworth pigs"] <= 27) & (filtered_May2016["Tamworth pigs"] >= 7)]
    print("number passed June 2016 filters:", len(accepted_June2016))
    filtered_June2016 = filtered_May2016[filtered_May2016['run_number'].isin(accepted_June2016['run_number'])]
    # July 2016
    accepted_July2016 = filtered_June2016[(filtered_June2016["Time"] == 138) &
    (filtered_June2016["Exmoor pony"] <= 12) & (filtered_June2016["Exmoor pony"] >= 10) &
    # (filtered_June2016["Longhorn cattle"] <= 96) & (filtered_June2016["Longhorn cattle"] >= 78)]
    (filtered_June2016["Tamworth pigs"] <= 27) & (filtered_June2016["Tamworth pigs"] >= 7)]
    print("number passed July 2016 filters:", len(accepted_July2016))
    filtered_July2016 = filtered_June2016[filtered_June2016['run_number'].isin(accepted_July2016['run_number'])]
    # Aug 2016
    accepted_Aug2016 = filtered_July2016[(filtered_July2016["Time"] == 139) &
    (filtered_July2016["Exmoor pony"] <= 12) & (filtered_July2016["Exmoor pony"] >= 10) &
    # (filtered_July2016["Longhorn cattle"] <= 96) & (filtered_July2016["Longhorn cattle"] >= 78)]
    (filtered_July2016["Tamworth pigs"] <= 27) & (filtered_July2016["Tamworth pigs"] >= 7)]
    print("number passed Aug 2016 filters:", len(accepted_Aug2016))
    filtered_Aug2016 = filtered_July2016[filtered_July2016['run_number'].isin(accepted_Aug2016['run_number'])]
    # Sept 2016
    accepted_Sept2016 = filtered_Aug2016[(filtered_Aug2016["Time"] == 140) &
    (filtered_Aug2016["Exmoor pony"] <= 12) & (filtered_Aug2016["Exmoor pony"] >= 10) &
    # (filtered_Aug2016["Longhorn cattle"] <= 107) & (filtered_Aug2016["Longhorn cattle"] >= 87)]
    (filtered_Aug2016["Tamworth pigs"] <= 27) & (filtered_Aug2016["Tamworth pigs"] >= 7)]
    print("number passed Sept 2016 filters:", len(accepted_Sept2016))
    filtered_Sept2016 = filtered_Aug2016[filtered_Aug2016['run_number'].isin(accepted_Sept2016['run_number'])]
    # Oct 2016
    accepted_Oct2016 = filtered_Sept2016[(filtered_Sept2016["Time"] == 141) &
    (filtered_Sept2016["Exmoor pony"] <= 12) & (filtered_Sept2016["Exmoor pony"] >= 10) &
    # (filtered_Sept2016["Longhorn cattle"] <= 107) & (filtered_Sept2016["Longhorn cattle"] >= 87)]
    (filtered_Sept2016["Tamworth pigs"] <= 27) & (filtered_Sept2016["Tamworth pigs"] >= 7)]
    print("number passed Oct 2016 filters:", len(accepted_Oct2016))
    filtered_Oct2016 = filtered_Aug2016[filtered_Aug2016['run_number'].isin(accepted_Oct2016['run_number'])]
    # Nov 2016
    accepted_Nov2016 = filtered_Oct2016[(filtered_Oct2016["Time"] == 142) &
    (filtered_Oct2016["Exmoor pony"] <= 12) & (filtered_Oct2016["Exmoor pony"] >= 10) &
    # (filtered_Oct2016["Longhorn cattle"] <= 101) & (filtered_Oct2016["Longhorn cattle"] >= 83)]
    (filtered_Oct2016["Tamworth pigs"] <= 27) & (filtered_Oct2016["Tamworth pigs"] >= 7)]
    print("number passed Nov 2016 filters:", len(accepted_Nov2016))
    filtered_Nov2016 = filtered_Oct2016[filtered_Oct2016['run_number'].isin(accepted_Nov2016['run_number'])]
    # Dec 2016
    accepted_Dec2016 = filtered_Nov2016[(filtered_Nov2016["Time"] == 143) &
    (filtered_Nov2016["Exmoor pony"] <= 12) & (filtered_Nov2016["Exmoor pony"] >= 10) &
    # (filtered_Nov2016["Longhorn cattle"] <= 87) & (filtered_Nov2016["Longhorn cattle"] >= 71)]
    (filtered_Nov2016["Tamworth pigs"] <= 23) & (filtered_Nov2016["Tamworth pigs"] >= 3)]
    print("number passed Dec 2016 filters:", len(accepted_Dec2016))
    filtered_Dec2016 = filtered_Nov2016[filtered_Nov2016['run_number'].isin(accepted_Dec2016['run_number'])]
    # Jan 2017
    accepted_Jan2017= filtered_Dec2016[(filtered_Dec2016["Time"] == 144) &
    (filtered_Dec2016["Exmoor pony"] <= 12) & (filtered_Dec2016["Exmoor pony"] >= 10) &
    # (filtered_Dec2016["Longhorn cattle"] <= 87) & (filtered_Dec2016["Longhorn cattle"] >= 71)]
    (filtered_Dec2016["Tamworth pigs"] <= 19) & (filtered_Dec2016["Tamworth pigs"] >= 1)]
    print("number passed Jan 2017 filters:", len(accepted_Jan2017))
    filtered_Jan2017 = filtered_Dec2016[filtered_Dec2016['run_number'].isin(accepted_Jan2017['run_number'])]
    # Feb 2017
    accepted_Feb2017 = filtered_Jan2017[(filtered_Jan2017["Time"] == 145) &
    (filtered_Jan2017["Exmoor pony"] <= 12) & (filtered_Jan2017["Exmoor pony"] >= 10) &
    # (filtered_Jan2017["Longhorn cattle"] <= 87) & (filtered_Jan2017["Longhorn cattle"] >= 71)]
    (filtered_Jan2017["Tamworth pigs"] <= 17) & (filtered_Jan2017["Tamworth pigs"] >= 1)]
    print("number passed Feb 2017 filters:", len(accepted_Feb2017))
    filtered_Feb2017 = filtered_Jan2017[filtered_Jan2017['run_number'].isin(accepted_Feb2017['run_number'])]
    
    
    # March 2017
    accepted_March2017 = filtered_Feb2017[(filtered_Feb2017["Time"] == 146) &
    (filtered_Feb2017["Exmoor pony"] <= 11) & (filtered_Feb2017["Exmoor pony"] >= 9) &
    # (filtered_Feb2017["Fallow deer"] <= 182) & (filtered_Feb2017["Fallow deer"] >= 149) &
    # (filtered_Feb2017["Longhorn cattle"] <= 87) & (filtered_Feb2017["Longhorn cattle"] >= 71)]
    (filtered_Feb2017["Tamworth pigs"] <= 17) & (filtered_Feb2017["Tamworth pigs"] >= 1)]
    print("number passed March 2017 filters:", len(accepted_March2017))
    filtered_March2017 = filtered_Feb2017[filtered_Feb2017['run_number'].isin(accepted_March2017['run_number'])]
    # April 2017
    accepted_April2017 = filtered_March2017[(filtered_March2017["Time"] == 147) &
    (filtered_March2017["Exmoor pony"] <= 11) & (filtered_March2017["Exmoor pony"] >= 9) &
    # (filtered_March2017["Longhorn cattle"] <= 110) & (filtered_March2017["Longhorn cattle"] >= 90)]
    (filtered_March2017["Tamworth pigs"] <= 32) & (filtered_March2017["Tamworth pigs"] >= 12)]
    print("number passed April 2017 filters:", len(accepted_April2017))
    filtered_April2017 = filtered_March2017[filtered_March2017['run_number'].isin(accepted_April2017['run_number'])]
    # May 2017
    accepted_May2017 = filtered_April2017[(filtered_April2017["Time"] == 148) &
    (filtered_April2017["Exmoor pony"] <= 11) & (filtered_April2017["Exmoor pony"] >= 9) &
    # (filtered_April2017["Longhorn cattle"] <= 120) & (filtered_April2017["Longhorn cattle"] >= 98)]
    (filtered_April2017["Tamworth pigs"] <= 32) & (filtered_April2017["Tamworth pigs"] >= 12)]
    print("number passed May 2017 filters:", len(accepted_May2017))
    filtered_May2017 = filtered_April2017[filtered_April2017['run_number'].isin(accepted_May2017['run_number'])]
    # June 2017
    accepted_June2017 = filtered_May2017[(filtered_May2017["Time"] == 149) &
    (filtered_May2017["Exmoor pony"] <= 11) & (filtered_May2017["Exmoor pony"] >= 9) &
    # (filtered_May2017["Longhorn cattle"] <= 103) & (filtered_May2017["Longhorn cattle"] >= 85)]
    (filtered_May2017["Tamworth pigs"] <= 32) & (filtered_May2017["Tamworth pigs"] >= 12)]
    print("number passed June 2017 filters:", len(accepted_June2017))
    filtered_June2017 = filtered_May2017[filtered_May2017['run_number'].isin(accepted_June2017['run_number'])]
    # July 2017
    accepted_July2017 = filtered_June2017[(filtered_June2017["Time"] == 150) &
    (filtered_June2017["Exmoor pony"] <= 11) & (filtered_June2017["Exmoor pony"] >= 9) &
    # (filtered_June2017["Longhorn cattle"] <= 103) & (filtered_June2017["Longhorn cattle"] >= 85)]
    (filtered_June2017["Tamworth pigs"] <= 32) & (filtered_June2017["Tamworth pigs"] >= 12)]
    print("number passed July 2017 filters:", len(accepted_July2017))
    filtered_July2017 = filtered_June2017[filtered_June2017['run_number'].isin(accepted_July2017['run_number'])]
    # Aug 2017
    accepted_Aug2017 = filtered_July2017[(filtered_July2017["Time"] == 151) &
    (filtered_July2017["Exmoor pony"] <= 11) & (filtered_July2017["Exmoor pony"] >= 9) &
    # (filtered_July2017["Longhorn cattle"] <= 103) & (filtered_July2017["Longhorn cattle"] >= 85)]
    (filtered_July2017["Tamworth pigs"] <= 32) & (filtered_July2017["Tamworth pigs"] >= 12)]
    print("number passed Aug 2017 filters:", len(accepted_Aug2017))
    filtered_Aug2017 = filtered_July2017[filtered_July2017['run_number'].isin(accepted_Aug2017['run_number'])]
    # Sept 2017
    accepted_Sept2017 = filtered_Aug2017[(filtered_Aug2017["Time"] == 152) &
    (filtered_Aug2017["Exmoor pony"] <= 11) & (filtered_Aug2017["Exmoor pony"] >= 9) &
    # (filtered_Aug2017["Longhorn cattle"] <= 99) & (filtered_Aug2017["Longhorn cattle"] >= 81)]
    (filtered_Aug2017["Tamworth pigs"] <= 32) & (filtered_Aug2017["Tamworth pigs"] >= 12)]
    print("number passed Sept 2017 filters:", len(accepted_Sept2017))
    filtered_Sept2017 = filtered_Aug2017[filtered_Aug2017['run_number'].isin(accepted_Sept2017['run_number'])]
    # Oct 2017
    accepted_Oct2017 = filtered_Sept2017[(filtered_Sept2017["Time"] == 153) &
    (filtered_Sept2017["Exmoor pony"] <= 11) & (filtered_Sept2017["Exmoor pony"] >= 9) &
    # (filtered_Sept2017["Longhorn cattle"] <= 97) & (filtered_Sept2017["Longhorn cattle"] >= 79)]
    (filtered_Sept2017["Tamworth pigs"] <= 32) & (filtered_Sept2017["Tamworth pigs"] >= 12)]
    print("number passed Oct 2017 filters:", len(accepted_Oct2017))
    filtered_Oct2017 = filtered_Sept2017[filtered_Sept2017['run_number'].isin(accepted_Oct2017['run_number'])]
    # Nov 2017
    accepted_Nov2017 = filtered_Oct2017[(filtered_Oct2017["Time"] == 154) &
    (filtered_Oct2017["Exmoor pony"] <= 11) & (filtered_Oct2017["Exmoor pony"] >= 9) &
    # (filtered_Oct2017["Longhorn cattle"] <= 97) & (filtered_Oct2017["Longhorn cattle"] >= 79)]
    (filtered_Oct2017["Tamworth pigs"] <= 32) & (filtered_Oct2017["Tamworth pigs"] >= 12)]
    print("number passed Nov 2017 filters:", len(accepted_Nov2017))
    filtered_Nov2017 = filtered_Oct2017[filtered_Oct2017['run_number'].isin(accepted_Nov2017['run_number'])]
    # Dec 2017
    accepted_Dec2017 = filtered_Nov2017[(filtered_Nov2017["Time"] == 155) &
    (filtered_Nov2017["Exmoor pony"] <= 11) & (filtered_Nov2017["Exmoor pony"] >= 9) &
    # (filtered_Nov2017["Longhorn cattle"] <= 97) & (filtered_Nov2017["Longhorn cattle"] >= 79)]
    (filtered_Nov2017["Tamworth pigs"] <= 28) & (filtered_Nov2017["Tamworth pigs"] >= 8)]
    print("number passed Dec 2017 filters:", len(accepted_Dec2017))
    filtered_Dec2017 = filtered_Nov2017[filtered_Nov2017['run_number'].isin(accepted_Dec2017['run_number'])]
    # January 2018
    accepted_Jan2018 = filtered_Dec2017[(filtered_Dec2017["Time"] == 156) &
    (filtered_Dec2017["Exmoor pony"] <= 11) & (filtered_Dec2017["Exmoor pony"] >= 9) &
    # (filtered_Dec2017["Longhorn cattle"] <= 97) & (filtered_Dec2017["Longhorn cattle"] >= 79)]
    (filtered_Dec2017["Tamworth pigs"] <= 21) & (filtered_Dec2017["Tamworth pigs"] >= 1)]
    print("number passed January 2018 filters:", len(accepted_Jan2018))
    filtered_Jan2018 = filtered_Dec2017[filtered_Dec2017['run_number'].isin(accepted_Jan2018['run_number'])]
    # February 2018
    accepted_Feb2018 = filtered_Jan2018[(filtered_Jan2018["Time"] == 157) &
    (filtered_Jan2018["Exmoor pony"] <= 11) & (filtered_Jan2018["Exmoor pony"] >= 9) &
    # (filtered_Jan2018["Longhorn cattle"] <= 97) & (filtered_Jan2018["Longhorn cattle"] >= 79)]
    (filtered_Jan2018["Tamworth pigs"] <= 26) & (filtered_Jan2018["Tamworth pigs"] >= 6)]
    print("number passed Feb 2018 filters:", len(accepted_Feb2018)) 
    filtered_Feb2018 = filtered_Jan2018[filtered_Jan2018['run_number'].isin(accepted_Feb2018['run_number'])]
    
    # March 2018
    accepted_March2018 = filtered_Feb2018[(filtered_Feb2018["Time"] == 158) &
    (filtered_Feb2018["Exmoor pony"] <= 10) & (filtered_Feb2018["Exmoor pony"] >= 8) &
    # (filtered_Feb2018["Fallow deer"] <= 276) & (filtered_Feb2018["Fallow deer"] >= 226) &
    # (filtered_Feb2018["Longhorn cattle"] <= 97) & (filtered_Feb2018["Longhorn cattle"] >= 79) &
    # (filtered_Feb2018["Red deer"] <= 26) & (filtered_Feb2018["Red deer"] >= 22)]
    (filtered_Feb2018["Tamworth pigs"] <= 26) & (filtered_Feb2018["Tamworth pigs"] >= 6)]
    print("number passed March 2018 filters:", len(accepted_March2018)) 
    filtered_March2018 = filtered_Feb2018[filtered_Feb2018['run_number'].isin(accepted_March2018['run_number'])]
    # April 2018
    accepted_April2018 = filtered_March2018[(filtered_March2018["Time"] == 159) &
    (filtered_March2018["Exmoor pony"] <= 10) & (filtered_March2018["Exmoor pony"] >= 8) &
    # (filtered_March2018["Longhorn cattle"] <= 111) & (filtered_March2018["Longhorn cattle"] >= 91)]
    (filtered_March2018["Tamworth pigs"] <= 26) & (filtered_March2018["Tamworth pigs"] >= 6)]
    print("number passed April 2018 filters:", len(accepted_April2018)) 
    filtered_April2018 = filtered_March2018[filtered_March2018['run_number'].isin(accepted_April2018['run_number'])]
    # May 2018
    accepted_May2018 = filtered_April2018[(filtered_April2018["Time"] == 160) &
    (filtered_April2018["Exmoor pony"] <= 10) & (filtered_April2018["Exmoor pony"] >= 8) &
    # (filtered_April2018["Longhorn cattle"] <= 129) & (filtered_April2018["Longhorn cattle"] >= 105)]
    (filtered_April2018["Tamworth pigs"] <= 33) & (filtered_April2018["Tamworth pigs"] >= 13)]
    print("number passed May 2018 filters:", len(accepted_May2018)) 
    filtered_May2018 = filtered_April2018[filtered_April2018['run_number'].isin(accepted_May2018['run_number'])]
    # June 2018
    accepted_June2018 = filtered_May2018[(filtered_May2018["Time"] == 161) &
    (filtered_May2018["Exmoor pony"] <= 10) & (filtered_May2018["Exmoor pony"] >= 8) &
    # (filtered_May2018["Longhorn cattle"] <= 113) & (filtered_May2018["Longhorn cattle"] >= 93)]
    (filtered_May2018["Tamworth pigs"] <= 33) & (filtered_May2018["Tamworth pigs"] >= 13)]
    print("number passed June 2018 filters:", len(accepted_June2018)) 
    filtered_June2018 = filtered_May2018[filtered_May2018['run_number'].isin(accepted_June2018['run_number'])]
    # July 2018
    accepted_July2018 = filtered_June2018[(filtered_June2018["Time"] == 162) &
    (filtered_June2018["Exmoor pony"] <= 10) & (filtered_June2018["Exmoor pony"] >= 8) &
    # (filtered_June2018["Longhorn cattle"] <= 113) & (filtered_June2018["Longhorn cattle"] >= 93)]
    (filtered_June2018["Tamworth pigs"] <= 32) & (filtered_June2018["Tamworth pigs"] >= 12)]
    print("number passed July 2018 filters:", len(accepted_July2018)) 
    filtered_July2018 = filtered_June2018[filtered_June2018['run_number'].isin(accepted_July2018['run_number'])]
    # Aug 2018
    accepted_Aug2018 = filtered_July2018[(filtered_July2018["Time"] == 163) &
    # (filtered_July2018["Longhorn cattle"] <= 112) & (filtered_July2018["Longhorn cattle"] >= 92)]
    (filtered_July2018["Tamworth pigs"] <= 32) & (filtered_July2018["Tamworth pigs"] >= 12)]
    print("number passed Aug 2018 filters:", len(accepted_Aug2018)) 
    filtered_Aug2018 = filtered_July2018[filtered_July2018['run_number'].isin(accepted_Aug2018['run_number'])]
    # Sept 2018
    accepted_Sept2018 = filtered_Aug2018[(filtered_Aug2018["Time"] == 164) &
    # (filtered_Aug2018["Longhorn cattle"] <= 117) & (filtered_Aug2018["Longhorn cattle"] >= 95)]
    (filtered_Aug2018["Tamworth pigs"] <= 32) & (filtered_Aug2018["Tamworth pigs"] >= 12)]
    print("number passed Sept 2018 filters:", len(accepted_Sept2018)) 
    filtered_Sept2018 = filtered_Aug2018[filtered_Aug2018['run_number'].isin(accepted_Sept2018['run_number'])]
    # Oct 2018
    accepted_Oct2018 = filtered_Sept2018[(filtered_Sept2018["Time"] == 165) &
    # (filtered_Sept2018["Longhorn cattle"] <= 111) & (filtered_Sept2018["Longhorn cattle"] >= 91)]
    (filtered_Sept2018["Tamworth pigs"] <= 31) & (filtered_Sept2018["Tamworth pigs"] >= 11)]
    print("number passed Oct 2018 filters:", len(accepted_Oct2018))
    filtered_Oct2018 = filtered_Sept2018[filtered_Sept2018['run_number'].isin(accepted_Oct2018['run_number'])]
    # Nov 2018
    accepted_Nov2018 = filtered_Oct2018[(filtered_Oct2018["Time"] == 166) &
    # (filtered_Oct2018["Longhorn cattle"] <= 102) & (filtered_Oct2018["Longhorn cattle"] >= 84)]
    (filtered_Oct2018["Tamworth pigs"] <= 19) & (filtered_Oct2018["Tamworth pigs"] >= 1)]
    print("number passed Nov 2018 filters:", len(accepted_Nov2018)) 
    filtered_Nov2018 = filtered_Oct2018[filtered_Oct2018['run_number'].isin(accepted_Nov2018['run_number'])]
    # Dec 2018
    accepted_Dec2018 = filtered_Nov2018[(filtered_Nov2018["Time"] == 167) &
    # (filtered_Nov2018["Longhorn cattle"] <= 98) & (filtered_Nov2018["Longhorn cattle"] >= 80)]
    (filtered_Nov2018["Tamworth pigs"] <= 19) & (filtered_Nov2018["Tamworth pigs"] >= 1)]
    print("number passed Dec 2018 filters:", len(accepted_Dec2018)) 
    filtered_Dec2018 = filtered_Nov2018[filtered_Nov2018['run_number'].isin(accepted_Dec2018['run_number'])]
    # Jan 2019
    accepted_Jan2019 = filtered_Dec2018[(filtered_Dec2018["Time"] == 168) &
    # (filtered_Dec2018["Longhorn cattle"] <= 98) & (filtered_Dec2018["Longhorn cattle"] >= 80)]
    (filtered_Dec2018["Tamworth pigs"] <= 19) & (filtered_Dec2018["Tamworth pigs"] >= 1)]
    print("number passed Jan 2019 filters:", len(accepted_Jan2019)) 
    filtered_Jan2019 = filtered_Dec2018[filtered_Dec2018['run_number'].isin(accepted_Jan2019['run_number'])]
    # Feb 2019
    accepted_Feb2019 = filtered_Jan2019[(filtered_Jan2019["Time"] == 169) &
    # (filtered_Jan2019["Longhorn cattle"] <= 96) & (filtered_Jan2019["Longhorn cattle"] >= 78)]
    (filtered_Jan2019["Tamworth pigs"] <= 20) & (filtered_Jan2019["Tamworth pigs"] >= 1)]
    print("number passed Feb 2019 filters:", len(accepted_Feb2019)) 
    filtered_Feb2019 = filtered_Jan2019[filtered_Jan2019['run_number'].isin(accepted_Feb2019['run_number'])]
    
    
    
    # March 2019
    accepted_March2019 = filtered_Feb2019[(filtered_Feb2019["Time"] == 170) &
    # (filtered_Feb2019["Fallow deer"] <= 306) & (filtered_Feb2019["Fallow deer"] >= 250) &
    # (filtered_Feb2019["Longhorn cattle"] <= 96) & (filtered_Feb2019["Longhorn cattle"] >= 78) &
    # (filtered_Feb2019["Red deer"] <= 41) & (filtered_Feb2019["Red deer"] >= 33)]
    (filtered_Feb2019["Tamworth pigs"] <= 19) & (filtered_Feb2019["Tamworth pigs"] >= 1)]
    print("number passed March 2019 filters:", len(accepted_March2019)) 
    filtered_March2019 = filtered_Feb2019[filtered_Feb2019['run_number'].isin(accepted_March2019['run_number'])]
    # April 2019
    accepted_April2019 = filtered_March2019[(filtered_March2019["Time"] == 171) &
    # (filtered_March2019["Longhorn cattle"] <= 111) & (filtered_March2019["Longhorn cattle"] >= 91)]
    # (filtered_March2019["Tamworth pigs"] <= 18) & (filtered_March2019["Tamworth pigs"] >= 1)]
    print("number passed April 2019 filters:", len(accepted_April2019)) 
    filtered_April2019 = filtered_March2019[filtered_March2019['run_number'].isin(accepted_April2019['run_number'])]
    # May 2019
    accepted_May2019 = filtered_April2019[(filtered_April2019["Time"] == 172) &
    # (filtered_April2019["Longhorn cattle"] <= 121) & (filtered_April2019["Longhorn cattle"] >= 99)]
    # # (filtered_April2019["Tamworth pigs"] <= 18) & (filtered_April2019["Tamworth pigs"] >= 1)]
    # print("number passed May 2019 filters:", len(accepted_May2019))
    # filtered_May2019 = filtered_April2019[filtered_April2019['run_number'].isin(accepted_May2019['run_number'])]
    # # June 2019
    # accepted_June2019 = filtered_May2019[(filtered_May2019["Time"] == 173) &
    # (filtered_May2019["Longhorn cattle"] <= 98) & (filtered_May2019["Longhorn cattle"] >= 80)]
    # # (filtered_May2019["Tamworth pigs"] <= 18) & (filtered_May2019["Tamworth pigs"] >= 1)]
    # print("number passed June 2019 filters:", len(accepted_June2019)) 
    # filtered_June2019 = filtered_May2019[filtered_May2019['run_number'].isin(accepted_June2019['run_number'])]
    # # July 2019
    # accepted_July2019 = filtered_June2019[(filtered_June2019["Time"] == 174) &
    # (filtered_June2019["Longhorn cattle"] <= 100) & (filtered_June2019["Longhorn cattle"] >= 82)]
    # # (filtered_June2019["Tamworth pigs"] <= 19) & (filtered_June2019["Tamworth pigs"] >= 1)]
    # print("number passed July 2019 filters:", len(accepted_July2019)) 
    # filtered_July2019 = filtered_June2019[filtered_June2019['run_number'].isin(accepted_July2019['run_number'])]
    # # Aug 2019
    # accepted_Aug2019 = filtered_July2019[(filtered_July2019["Time"] == 175) &
    # (filtered_July2019["Longhorn cattle"] <= 100) & (filtered_July2019["Longhorn cattle"] >= 82)]
    # # (filtered_July2019["Tamworth pigs"] <= 19) & (filtered_July2019["Tamworth pigs"] >= 1)]
    # print("number passed Aug 2019 filters:", len(accepted_Aug2019)) 
    # filtered_Aug2019 = filtered_July2019[filtered_July2019['run_number'].isin(accepted_Aug2019['run_number'])]
    # # Sept 2019
    # accepted_Sept2019 = filtered_Aug2019[(filtered_Aug2019["Time"] == 176) &
    # (filtered_Aug2019["Longhorn cattle"] <= 102) & (filtered_Aug2019["Longhorn cattle"] >= 84)]
    # # (filtered_Aug2019["Tamworth pigs"] <= 19) & (filtered_Aug2019["Tamworth pigs"] >= 1)]
    # print("number passed Sept 2019 filters:", len(accepted_Sept2019)) 
    # filtered_Sept2019 = filtered_Aug2019[filtered_Aug2019['run_number'].isin(accepted_Sept2019['run_number'])]
    # # Oct 2019
    # accepted_Oct2019 = filtered_Sept2019[(filtered_Sept2019["Time"] == 177) &
    # (filtered_Sept2019["Longhorn cattle"] <= 97) & (filtered_Sept2019["Longhorn cattle"] >= 79)]
    # # (filtered_Sept2019["Tamworth pigs"] <= 19) & (filtered_Sept2019["Tamworth pigs"] >= 1)]
    # print("number passed Oct 2019 filters:", len(accepted_Oct2019)) 
    # filtered_Oct2019 = filtered_Sept2019[filtered_Sept2019['run_number'].isin(accepted_Oct2019['run_number'])]
    # # Nov 2019
    # accepted_Nov2019 = filtered_Oct2019[(filtered_Oct2019["Time"] == 178) &
    # (filtered_Oct2019["Longhorn cattle"] <= 96) & (filtered_Oct2019["Longhorn cattle"] >= 78)]
    # # (filtered_Oct2019["Tamworth pigs"] <= 19) & (filtered_Oct2019["Tamworth pigs"] >= 1)]
    # print("number passed Nov 2019 filters:", len(accepted_Nov2019)) 
    # filtered_Nov2019 = filtered_Oct2019[filtered_Oct2019['run_number'].isin(accepted_Nov2019['run_number'])]
    # # Dec 2019
    # accepted_Dec2019 = filtered_Nov2019[(filtered_Nov2019["Time"] == 179) &
    # (filtered_Nov2019["Longhorn cattle"] <= 88) & (filtered_Nov2019["Longhorn cattle"] >= 72)]
    # # (filtered_Nov2019["Tamworth pigs"] <= 20) & (filtered_Nov2019["Tamworth pigs"] >= 1)]
    # print("number passed Dec 2019 filters:", len(accepted_Dec2019))
    # filtered_Dec2019 = filtered_Nov2019[filtered_Nov2019['run_number'].isin(accepted_Dec2019['run_number'])]
    # # Jan 2020
    # accepted_Jan2020 = filtered_Dec2019[(filtered_Dec2019["Time"] == 180) &
    # (filtered_Dec2019["Longhorn cattle"] <= 88) & (filtered_Dec2019["Longhorn cattle"] >= 72)]
    # # (filtered_Dec2019["Tamworth pigs"] <= 20) & (filtered_Dec2019["Tamworth pigs"] >= 1)]
    # print("number passed Jan 2020 filters:", len(accepted_Jan2020))
    # filtered_Jan2020 = filtered_Dec2019[filtered_Dec2019['run_number'].isin(accepted_Jan2020['run_number'])]
    # # Feb 2020
    # accepted_Feb2020 = filtered_Jan2020[(filtered_Jan2020["Time"] == 181) &
    # (filtered_Jan2020["Longhorn cattle"] <= 87) & (filtered_Jan2020["Longhorn cattle"] >= 71)]
    # # (filtered_Jan2020["Tamworth pigs"] <= 18) & (filtered_Jan2020["Tamworth pigs"] >= 1)]
    # print("number passed Feb 2020 filters:", len(accepted_Feb2020))
    # filtered_Feb2020 = filtered_Jan2020[filtered_Jan2020['run_number'].isin(accepted_Feb2020['run_number'])]
    
    
    # # March 2020
    # accepted_March2020 = filtered_Feb2020[(filtered_Feb2020["Time"] == 182) &
    # (filtered_Feb2020["Fallow deer"] <= 272) & (filtered_Feb2020["Fallow deer"] >= 222) &
    # (filtered_Feb2020["Red deer"] <= 39) & (filtered_Feb2020["Red deer"] >= 32) &
    # (filtered_Feb2020["Longhorn cattle"] <= 89) & (filtered_Feb2020["Longhorn cattle"] >= 73)]
    # # (filtered_Feb2020["Tamworth pigs"] <= 17) & (filtered_Feb2020["Tamworth pigs"] >= 1)]
    # print("number passed March 2020 filters:", len(accepted_March2020)) 
    # filtered_March2020 = filtered_Feb2020[filtered_Feb2020['run_number'].isin(accepted_March2020['run_number'])]
    # # April 2020
    # accepted_April2020 = filtered_March2020[(filtered_March2020["Time"] == 183) &
    # (filtered_March2020["Exmoor pony"] <= 17) & (filtered_March2020["Exmoor pony"] >= 14) &
    # (filtered_March2020["Longhorn cattle"] <= 89) & (filtered_March2020["Longhorn cattle"] >= 73)]
    # # (filtered_March2020["Tamworth pigs"] <= 17) & (filtered_March2020["Tamworth pigs"] >= 1)]
    # print("number passed April 2020 filters:", len(accepted_April2020)) 
    # filtered_April2020 = filtered_March2020[filtered_March2020['run_number'].isin(accepted_April2020['run_number'])]
    # May 2020
    all_accepted_runs = filtered_April2020[(filtered_April2020["Time"] == 184) &
    (filtered_April2020["Tamworth pigs"] <= 29) & (filtered_April2020["Tamworth pigs"] >= 9) &
    (filtered_April2020["Exmoor pony"] <= 17) & (filtered_April2020["Exmoor pony"] >= 14) &
    # (filtered_April2020["Longhorn cattle"] <= 89) & (filtered_April2020["Longhorn cattle"] >= 73) &
    (filtered_April2020["Roe deer"] <= 80) & (filtered_April2020["Roe deer"] >= 20) & 
    (filtered_April2020["Grassland"] <= 69) & (filtered_April2020["Grassland"] >= 49) & 
    (filtered_April2020["Thorny Scrub"] <= 35) & (filtered_April2020["Thorny Scrub"] >= 21) &
    (filtered_April2020["Woodland"] <= 29) & (filtered_April2020["Woodland"] >= 9)]

    print("number passed all filters:", len(all_accepted_runs))

    # with open('/Users/emilyneil/Desktop/KneppABM/many_outputs2/fifty_perc/passed_filters.txt', 'w') as f:
    #         print("number passed pre-reintro filters:", len(accepted_preReintro), file=f)
    #         print("number passed April 2015 filters:", len(accepted_April2015), file=f)
    #         print("number passed May 2015 filters:", len(accepted_May2015), file=f)
    #         print("number passed June 2015 filters:", len(accepted_June2015), file=f)
    #         print("number passed July 2015 filters:", len(accepted_July2015), file=f)
    #         print("number passed Aug 2015 filters:", len(accepted_Aug2015), file=f)
    #         print("number passed Sept 2015 filters:", len(accepted_Sept2015), file=f)
    #         print("number passed Oct 2015 filters:", len(accepted_Oct2015), file=f)
    #         print("number passed Nov 2015 filters:", len(accepted_Nov2015), file=f)
    #         print("number passed Dec 2015 filters:", len(accepted_Dec2015), file=f)
    #         print("number passed Jan 2016 filters:", len(accepted_Jan2016), file=f)
    #         print("number passed February 2016 filters:", len(accepted_Feb2016), file=f)
    #         print("number passed March 2016 filters:", len(accepted_March2016), file=f)
    #         print("number passed April 2016 filters:", len(accepted_April2016), file=f)
    #         print("number passed May 2016 filters:", len(accepted_May2016), file=f)
    #         print("number passed June 2016 filters:", len(accepted_June2016), file=f)
    #         print("number passed July 2016 filters:", len(accepted_July2016), file=f)
    #         print("number passed Aug 2016 filters:", len(accepted_Aug2016), file=f)
    #         print("number passed Sept 2016 filters:", len(accepted_Sept2016), file=f)
    #         print("number passed Oct 2016 filters:", len(accepted_Oct2016), file=f)
    #         print("number passed Nov 2016 filters:", len(accepted_Nov2016), file=f)
    #         print("number passed Dec 2016 filters:", len(accepted_Dec2016), file=f)
    #         print("number passed Jan 2017 filters:", len(accepted_Jan2017), file=f)
    #         print("number passed Feb 2017 filters:", len(accepted_Feb2017), file=f)
    #         print("number passed March 2017 filters:", len(accepted_March2017), file=f)
    #         print("number passed April 2017 filters:", len(accepted_April2017), file=f)
    #         print("number passed May 2017 filters:", len(accepted_May2017), file=f)
    #         print("number passed June 2017 filters:", len(accepted_June2017), file=f)
    #         print("number passed July 2017 filters:", len(accepted_July2017), file=f)
    #         print("number passed Aug 2017 filters:", len(accepted_Aug2017), file=f)
    #         print("number passed Sept 2017 filters:", len(accepted_Sept2017), file=f)
    #         print("number passed Oct 2017 filters:", len(accepted_Oct2017), file=f)
    #         print("number passed Nov 2017 filters:", len(accepted_Nov2017), file=f)
    #         print("number passed Dec 2017 filters:", len(accepted_Dec2017), file=f)
    #         print("number passed January 2018 filters:", len(accepted_Jan2018), file=f)
    #         print("number passed Feb 2018 filters:", len(accepted_Feb2018), file=f) 
    #         print("number passed March 2018 filters:", len(accepted_March2018), file=f) 
    #         print("number passed April 2018 filters:", len(accepted_April2018), file=f) 
    #         print("number passed May 2018 filters:", len(accepted_May2018), file=f) 
    #         print("number passed June 2018 filters:", len(accepted_June2018), file=f) 
    #         print("number passed July 2018 filters:", len(accepted_July2018), file=f) 
    #         print("number passed Aug 2018 filters:", len(accepted_Aug2018), file=f) 
    #         print("number passed Sept 2018 filters:", len(accepted_Sept2018), file=f) 
    #         print("number passed Oct 2018 filters:", len(accepted_Oct2018), file=f)
    #         print("number passed Nov 2018 filters:", len(accepted_Nov2018), file=f) 
    #         print("number passed Dec 2018 filters:", len(accepted_Dec2018), file=f) 
    #         print("number passed Jan 2019 filters:", len(accepted_Jan2019), file=f) 
    #         print("number passed Feb 2019 filters:", len(accepted_Feb2019), file=f) 
    #         print("number passed March 2019 filters:", len(accepted_March2019), file=f) 
    #         print("number passed April 2019 filters:", len(accepted_April2019), file=f) 
    #         print("number passed May 2019 filters:", len(accepted_May2019), file=f)
    #         print("number passed June 2019 filters:", len(accepted_June2019), file=f) 
    #         print("number passed July 2019 filters:", len(accepted_July2019), file=f) 
    #         print("number passed Aug 2019 filters:", len(accepted_Aug2019), file=f) 
    #         print("number passed Sept 2019 filters:", len(accepted_Sept2019), file=f) 
    #         print("number passed Oct 2019 filters:", len(accepted_Oct2019), file=f) 
    #         print("number passed Nov 2019 filters:", len(accepted_Nov2019), file=f) 
    #         print("number passed Dec 2019 filters:", len(accepted_Dec2019), file=f)
    #         print("number passed Jan 2020 filters:", len(accepted_Jan2020), file=f)
    #         print("number passed Feb 2020 filters:", len(accepted_Feb2020), file=f)
    #         print("number passed March 2020 filters:", len(accepted_March2020), file=f) 
    #         print("number passed April 2020 filters:", len(accepted_April2020), file=f) 
    #         print("number passed all filters:", len(all_accepted_runs), file=f)


    # accepted parameters
    accepted_parameters = final_parameters[final_parameters['run_number'].isin(all_accepted_runs['run_number'])]
    # tag the accepted simulations
    final_results['accepted?'] = np.where(final_results['run_number'].isin(accepted_parameters['run_number']), 'Accepted', 'Rejected')

    # with pd.option_context('display.max_columns',None):
    #     print(accepted_parameters)
    #     # just_nodes = final_results[final_results['Time'] == 184]
    #     # print(just_nodes[["Time", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"]])
    
    # with pd.option_context('display.max_rows',None, 'display.max_columns',None):
    #     print("accepted_years: \n", all_accepted_runs)


    # save to excel sheet
    # final_parameters.to_excel("all_parameters.xlsx")
    accepted_parameters.to_csv('/Users/emilyneil/Desktop/KneppABM/many_outputs2/fifty_perc/accepted_parameters.csv')

    return number_simulations, final_results, accepted_parameters

