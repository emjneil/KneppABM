# ------ ABM of the Knepp Estate (2005-2046) --------
from KneppModel_ABM import KneppModel 
import numpy as np
import random
import pandas as pd


# # # # Run the model # # # # 


def run_all_models():

    # define number of simulations
    number_simulations =  2
    # make list of variables
    final_results_list = []
    final_parameters = []
    run_number = 0


    for _ in range(number_simulations):
        # keep track of the runs
        run_number += 1
        print(run_number)
        # choose my percent above/below number
        perc_aboveBelow = 0.01

        # define the parameters
        chance_reproduceSapling = random.uniform(0.0037389-(0.0037389*perc_aboveBelow), 0.0037389+(0.0037389*perc_aboveBelow))
        chance_reproduceYoungScrub = random.uniform(0.00322869-(0.00322869*perc_aboveBelow), 0.00322869+(0.00322869*perc_aboveBelow))
        chance_regrowGrass = random.uniform(0.0139838-(0.0139838*perc_aboveBelow), 0.0139838+(0.0139838*perc_aboveBelow))
        chance_saplingBecomingTree = random.uniform(0.00232948-(0.00232948*perc_aboveBelow), 0.00232948+(0.00232948*perc_aboveBelow))
        chance_youngScrubMatures =random.uniform(0.00865091-(0.00865091*perc_aboveBelow), 0.00865091+(0.00865091*perc_aboveBelow))
        chance_scrubOutcompetedByTree = random.uniform(0.00199731-(0.00199731*perc_aboveBelow), 0.00199731+(0.00199731*perc_aboveBelow))
        chance_grassOutcompetedByTree = random.uniform(0.09451909-(0.09451909*perc_aboveBelow), 0.09451909+(0.09451909*perc_aboveBelow))
        chance_grassOutcompetedByScrub = random.uniform(0.09333696-(0.09333696*perc_aboveBelow), 0.09333696+(0.09333696*perc_aboveBelow))
        chance_saplingOutcompetedByTree = random.uniform(0.08138607-(0.08138607*perc_aboveBelow), 0.08138607+(0.08138607*perc_aboveBelow))
        chance_saplingOutcompetedByScrub = random.uniform(0.01685629-(0.01685629*perc_aboveBelow), 0.01685629+(0.01685629*perc_aboveBelow))
        chance_youngScrubOutcompetedByScrub =random.uniform(0.07791945-(0.07791945*perc_aboveBelow), 0.07791945+(0.07791945*perc_aboveBelow))
        chance_youngScrubOutcompetedByTree = random.uniform(0.07842738-(0.07842738*perc_aboveBelow), 0.07842738+(0.07842738*perc_aboveBelow))

        # initial values
        initial_roeDeer = 0.12
        initial_grassland = 0.8
        initial_woodland = 0.14
        initial_scrubland = 0.01

        # roe deer
        roeDeer_reproduce = random.uniform(0.1783482-(0.1783482*perc_aboveBelow), 0.1783482+(0.1783482*perc_aboveBelow))
        roeDeer_gain_from_grass = random.uniform(0.9328174-(0.9328174*perc_aboveBelow), 0.9328174+(0.9328174*perc_aboveBelow))
        roeDeer_gain_from_Trees =random.uniform(0.9144764-(0.9144764*perc_aboveBelow), 0.9144764+(0.9144764*perc_aboveBelow))
        roeDeer_gain_from_Scrub =random.uniform(0.91391136-(0.91391136*perc_aboveBelow), 0.91391136+(0.91391136*perc_aboveBelow))
        roeDeer_gain_from_Saplings = random.uniform(0.11702867-(0.11702867*perc_aboveBelow), 0.11702867+(0.11702867*perc_aboveBelow))
        roeDeer_gain_from_YoungScrub = random.uniform(0.11623631-(0.11623631*perc_aboveBelow), 0.11623631+(0.11623631*perc_aboveBelow))
        # Fallow deer
        fallowDeer_reproduce = random.uniform(0.31526015-(0.31526015*perc_aboveBelow), 0.31526015+(0.31526015*perc_aboveBelow))
        fallowDeer_gain_from_grass = random.uniform(0.92255558-(0.92255558*perc_aboveBelow), 0.92255558+(0.92255558*perc_aboveBelow))
        fallowDeer_gain_from_Trees = random.uniform(0.89146959-(0.89146959*perc_aboveBelow), 0.89146959+(0.89146959*perc_aboveBelow))
        fallowDeer_gain_from_Scrub = random.uniform(0.89571586-(0.89571586*perc_aboveBelow), 0.89571586+(0.89571586*perc_aboveBelow))
        fallowDeer_gain_from_Saplings = random.uniform(0.11610159-(0.11610159*perc_aboveBelow), 0.11610159+(0.11610159*perc_aboveBelow))
        fallowDeer_gain_from_YoungScrub = random.uniform(0.10764306-(0.10764306*perc_aboveBelow), 0.10764306+(0.10764306*perc_aboveBelow))
        # Red deer
        redDeer_reproduce = random.uniform(0.36341145-(0.36341145*perc_aboveBelow), 0.36341145+(0.36341145*perc_aboveBelow))
        redDeer_gain_from_grass = random.uniform(0.92949652-(0.92949652*perc_aboveBelow), 0.92949652+(0.92949652*perc_aboveBelow))
        redDeer_gain_from_Trees = random.uniform(0.9052971-(0.9052971*perc_aboveBelow), 0.9052971+(0.9052971*perc_aboveBelow))
        redDeer_gain_from_Scrub = random.uniform(0.89380651-(0.89380651*perc_aboveBelow), 0.89380651+(0.89380651*perc_aboveBelow))
        redDeer_gain_from_Saplings = random.uniform(0.11747397-(0.11747397*perc_aboveBelow), 0.11747397+(0.11747397*perc_aboveBelow))
        redDeer_gain_from_YoungScrub = random.uniform(0.08173538-(0.08173538*perc_aboveBelow), 0.08173538+(0.08173538*perc_aboveBelow))
        
        # Exmoor ponies
        ponies_gain_from_grass = random.uniform(0.90420608-(0.90420608*perc_aboveBelow), 0.90420608+(0.90420608*perc_aboveBelow))
        ponies_gain_from_Trees = random.uniform(0.89434907-(0.89434907*perc_aboveBelow), 0.89434907+(0.89434907*perc_aboveBelow)) 
        ponies_gain_from_Scrub = random.uniform(0.882705-(0.882705*perc_aboveBelow), 0.882705+(0.882705*perc_aboveBelow))
        ponies_gain_from_Saplings = random.uniform(0.10818295-(0.10818295*perc_aboveBelow), 0.10818295+(0.10818295*perc_aboveBelow))
        ponies_gain_from_YoungScrub = random.uniform(0.06682179-(0.06682179*perc_aboveBelow), 0.06682179+(0.06682179*perc_aboveBelow))
        # Longhorn cattle
        cows_reproduce = random.uniform(0.18626336-(0.18626336*perc_aboveBelow), 0.18626336+(0.18626336*perc_aboveBelow))
        cows_gain_from_grass = random.uniform(0.90102432-(0.90102432*perc_aboveBelow), 0.90102432+(0.90102432*perc_aboveBelow))
        cows_gain_from_Trees = random.uniform(0.89963841-(0.89963841*perc_aboveBelow), 0.89963841+(0.89963841*perc_aboveBelow))
        cows_gain_from_Scrub = random.uniform(0.88759371-(0.88759371*perc_aboveBelow), 0.88759371+(0.88759371*perc_aboveBelow))
        cows_gain_from_Saplings = random.uniform(0.09148747-(0.09148747*perc_aboveBelow), 0.09148747+(0.09148747*perc_aboveBelow))
        cows_gain_from_YoungScrub = random.uniform(0.0842241-(0.0842241*perc_aboveBelow), 0.0842241+(0.0842241*perc_aboveBelow))
        # Tamworth pigs
        pigs_reproduce = random.uniform(0.17226346-(0.17226346*perc_aboveBelow), 0.17226346+(0.17226346*perc_aboveBelow))
        pigs_gain_from_grass = random.uniform(0.8765768-(0.8765768*perc_aboveBelow), 0.8765768+(0.8765768*perc_aboveBelow))
        pigs_gain_from_Trees =random.uniform(0.90491902-(0.90491902*perc_aboveBelow), 0.90491902+(0.90491902*perc_aboveBelow))
        pigs_gain_from_Scrub = random.uniform(0.90649852-(0.90649852*perc_aboveBelow), 0.90649852+(0.90649852*perc_aboveBelow))
        pigs_gain_from_Saplings = random.uniform(0.10604675-(0.10604675*perc_aboveBelow), 0.10604675+(0.10604675*perc_aboveBelow))
        pigs_gain_from_YoungScrub = random.uniform(0.11007447-(0.11007447*perc_aboveBelow), 0.11007447+(0.11007447*perc_aboveBelow))
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
        run_number]

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
        "run_number"]

    # check out the parameters used
    final_parameters = pd.DataFrame(data=final_parameters, columns=variables)


    # filter the runs and tag the dataframe; keep track of how many filters passed
    final_results["passed_filters"] = 0
    # pre-reintroduction model
    my_time = final_results.loc[final_results['Time'] == 50]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Roe deer"] <= 40) & (row["Roe deer"] >= 6) & (row["Grassland"] <= 90) & (row["Grassland"] >= 49) & (row["Woodland"] <= 27) & (row["Woodland"] >= 7) & (row["Thorny Scrub"] <= 21) & (row["Thorny Scrub"] >= 1):
            accepted_runs.append(row["run_number"])
    # change the number of accepted runs
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 

    # April 2015
    for index, row in my_time.iterrows():
        if (row["Roe deer"] <= 123) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Longhorn cattle"] <= 140) & (row["Longhorn cattle"] >= 90) & (row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
    # change the number of accepted runs
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 

    print(final_results)

    # keep track of how many filters are passed
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_April2015.run_number.values): row["passed filters"] +=1 
    # May 2015
    accepted_May2015 = filtered_April2015[(filtered_April2015["Time"] == 124) &
    (filtered_April2015["Longhorn cattle"] <= 154) & (filtered_April2015["Longhorn cattle"] >= 104) &
    (filtered_April2015["Tamworth pigs"] <= 24) & (filtered_April2015["Tamworth pigs"] >= 4) &
    (filtered_April2015["Exmoor pony"] <= 11) & (filtered_April2015["Exmoor pony"] >= 9)]
    print("number passed May 2015 filters:", len(accepted_May2015))
    filtered_May2015 = filtered_April2015[filtered_April2015['run_number'].isin(accepted_May2015['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_May2015.run_number.values): row["passed filters"] +=1 
    # June 2015
    accepted_June2015 = filtered_May2015[(filtered_May2015["Time"] == 125) &
    (filtered_May2015["Longhorn cattle"] <= 154) & (filtered_May2015["Longhorn cattle"] >= 104) &
    (filtered_May2015["Exmoor pony"] <= 11) & (filtered_May2015["Exmoor pony"] >= 9) &
    (filtered_May2015["Tamworth pigs"] <= 24) & (filtered_May2015["Tamworth pigs"] >= 4)]
    print("number passed June 2015 filters:", len(accepted_June2015))
    filtered_June2015 = filtered_May2015[filtered_May2015['run_number'].isin(accepted_June2015['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_June2015.run_number.values): row["passed filters"] +=1 
    # July 2015
    accepted_July2015 = filtered_June2015[(filtered_June2015["Time"] == 126) &
    (filtered_June2015["Longhorn cattle"] <= 154) & (filtered_June2015["Longhorn cattle"] >= 104) &
    (filtered_June2015["Exmoor pony"] <= 11) & (filtered_June2015["Exmoor pony"] >= 9) &
    (filtered_June2015["Tamworth pigs"] <= 24) & (filtered_June2015["Tamworth pigs"] >= 4)]
    print("number passed July 2015 filters:", len(accepted_July2015))
    filtered_July2015 = filtered_June2015[filtered_June2015['run_number'].isin(accepted_July2015['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_July2015.run_number.values): row["passed filters"] +=1 
    # Aug 2015
    accepted_Aug2015 = filtered_July2015[(filtered_July2015["Time"] == 127) &
    (filtered_July2015["Longhorn cattle"] <= 154) & (filtered_July2015["Longhorn cattle"] >= 104) &
    (filtered_July2015["Exmoor pony"] <= 11) & (filtered_July2015["Exmoor pony"] >= 9) &
    (filtered_July2015["Tamworth pigs"] <= 24) & (filtered_July2015["Tamworth pigs"] >= 4)]
    print("number passed Aug 2015 filters:", len(accepted_Aug2015))
    filtered_Aug2015 = filtered_July2015[filtered_July2015['run_number'].isin(accepted_Aug2015['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Aug2015.run_number.values): row["passed filters"] +=1 
    # Sept 2015
    accepted_Sept2015 = filtered_Aug2015[(filtered_Aug2015["Time"] == 128) &
    (filtered_Aug2015["Longhorn cattle"] <= 155) & (filtered_Aug2015["Longhorn cattle"] >= 105) &
    (filtered_Aug2015["Exmoor pony"] <= 11) & (filtered_Aug2015["Exmoor pony"] >= 9) &
    (filtered_Aug2015["Tamworth pigs"] <= 24) & (filtered_Aug2015["Tamworth pigs"] >= 4)]
    print("number passed Sept 2015 filters:", len(accepted_Sept2015))
    filtered_Sept2015 = filtered_Aug2015[filtered_Aug2015['run_number'].isin(accepted_Sept2015['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Sept2015.run_number.values): row["passed filters"] +=1 
    # Oct 2015
    accepted_Oct2015 = filtered_Sept2015[(filtered_Sept2015["Time"] == 129) &
    (filtered_Sept2015["Longhorn cattle"] <= 116) & (filtered_Sept2015["Longhorn cattle"] >= 66) &
    (filtered_Sept2015["Exmoor pony"] <= 11) & (filtered_Sept2015["Exmoor pony"] >= 9) &
    (filtered_Sept2015["Tamworth pigs"] <= 24) & (filtered_Sept2015["Tamworth pigs"] >= 4)]
    print("number passed Oct 2015 filters:", len(accepted_Oct2015))
    filtered_Oct2015 = filtered_Sept2015[filtered_Sept2015['run_number'].isin(accepted_Oct2015['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Oct2015.run_number.values): row["passed filters"] +=1 
    # Nov 2015
    accepted_Nov2015 = filtered_Oct2015[(filtered_Oct2015["Time"] == 130) &
    (filtered_Oct2015["Longhorn cattle"] <= 116) & (filtered_Oct2015["Longhorn cattle"] >= 66) &
    (filtered_Oct2015["Exmoor pony"] <= 11) & (filtered_Oct2015["Exmoor pony"] >= 9) &
    (filtered_Oct2015["Tamworth pigs"] <= 23) & (filtered_Oct2015["Tamworth pigs"] >= 3)]
    print("number passed Nov 2015 filters:", len(accepted_Nov2015))
    filtered_Nov2015 = filtered_Oct2015[filtered_Oct2015['run_number'].isin(accepted_Nov2015['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Nov2015.run_number.values): row["passed filters"] +=1 
    # Dec 2015
    accepted_Dec2015 = filtered_Nov2015[(filtered_Nov2015["Time"] == 131) &
    (filtered_Nov2015["Longhorn cattle"] <= 111) & (filtered_Nov2015["Longhorn cattle"] >= 61) &
    (filtered_Nov2015["Exmoor pony"] <= 11) & (filtered_Nov2015["Exmoor pony"] >= 9) &
    (filtered_Nov2015["Tamworth pigs"] <= 23) & (filtered_Nov2015["Tamworth pigs"] >= 3)]
    print("number passed Dec 2015 filters:", len(accepted_Dec2015))
    filtered_Dec2015 = filtered_Nov2015[filtered_Nov2015['run_number'].isin(accepted_Dec2015['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Dec2015.run_number.values): row["passed filters"] +=1 
    # Jan 2016
    accepted_Jan2016 = filtered_Dec2015[(filtered_Dec2015["Time"] == 132) &
    (filtered_Dec2015["Longhorn cattle"] <= 111) & (filtered_Dec2015["Longhorn cattle"] >= 61) &
    (filtered_Dec2015["Exmoor pony"] <= 11) & (filtered_Dec2015["Exmoor pony"] >= 9) &
    (filtered_Dec2015["Tamworth pigs"] <= 20) & (filtered_Dec2015["Tamworth pigs"] >= 1)]
    print("number passed Jan 2016 filters:", len(accepted_Jan2016))
    filtered_Jan2016 = filtered_Dec2015[filtered_Dec2015['run_number'].isin(accepted_Jan2016['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Jan2016.run_number.values): row["passed filters"] +=1 
    # Feb 2016
    accepted_Feb2016 = filtered_Jan2016[(filtered_Jan2016["Time"] == 133) &
    (filtered_Jan2016["Exmoor pony"] <= 11) & (filtered_Jan2016["Exmoor pony"] >= 9) &
    (filtered_Jan2016["Longhorn cattle"] <= 111) & (filtered_Jan2016["Longhorn cattle"] >= 61) &
    (filtered_Jan2016["Tamworth pigs"] <= 20) & (filtered_Jan2016["Tamworth pigs"] >= 1)]
    print("number passed February 2016 filters:", len(accepted_Feb2016))
    filtered_Feb2016 = filtered_Jan2016[filtered_Jan2016['run_number'].isin(accepted_Feb2016['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Feb2016.run_number.values): row["passed filters"] +=1 
    # March 2016
    accepted_March2016 = filtered_Feb2016[(filtered_Feb2016["Time"] == 134) &
    (filtered_Feb2016["Exmoor pony"] <= 12) & (filtered_Feb2016["Exmoor pony"] >= 10) &
    (filtered_Feb2016["Longhorn cattle"] <= 111) & (filtered_Feb2016["Longhorn cattle"] >= 61) &
    (filtered_Feb2016["Fallow deer"] <= 190) & (filtered_Feb2016["Fallow deer"] >= 90) &
    (filtered_Feb2016["Red deer"] <= 31) & (filtered_Feb2016["Red deer"] >= 21) &
    (filtered_Feb2016["Tamworth pigs"] <= 19) & (filtered_Feb2016["Tamworth pigs"] >= 1)]
    print("number passed March 2016 filters:", len(accepted_March2016))
    filtered_March2016 = filtered_Feb2016[filtered_Feb2016['run_number'].isin(accepted_March2016['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_March2016.run_number.values): row["passed filters"] +=1 
    # April 2016
    accepted_April2016 = filtered_March2016[(filtered_March2016["Time"] == 135) &
    (filtered_March2016["Exmoor pony"] <= 12) & (filtered_March2016["Exmoor pony"] >= 10) &
    (filtered_March2016["Longhorn cattle"] <= 128) & (filtered_March2016["Longhorn cattle"] >= 78) &
    (filtered_March2016["Tamworth pigs"] <= 19) & (filtered_March2016["Tamworth pigs"] >= 1)]
    print("number passed April 2016 filters:", len(accepted_April2016))
    filtered_April2016 = filtered_March2016[filtered_March2016['run_number'].isin(accepted_April2016['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_April2016.run_number.values): row["passed filters"] +=1 
    # May 2016
    accepted_May2016 = filtered_April2016[(filtered_April2016["Time"] == 136) &
    (filtered_April2016["Exmoor pony"] <= 12) & (filtered_April2016["Exmoor pony"] >= 10) &
    (filtered_April2016["Longhorn cattle"] <= 133) & (filtered_April2016["Longhorn cattle"] >= 83) &
    (filtered_April2016["Tamworth pigs"] <= 27) & (filtered_April2016["Tamworth pigs"] >= 7)]
    print("number passed May 2016 filters:", len(accepted_May2016))
    filtered_May2016 = filtered_April2016[filtered_April2016['run_number'].isin(accepted_May2016['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_May2016.run_number.values): row["passed filters"] +=1 
    # June 2016
    accepted_June2016 = filtered_May2016[(filtered_May2016["Time"] == 137) &
    (filtered_May2016["Exmoor pony"] <= 12) & (filtered_May2016["Exmoor pony"] >= 10) &
    (filtered_May2016["Longhorn cattle"] <= 114) & (filtered_May2016["Longhorn cattle"] >= 64) &
    (filtered_May2016["Tamworth pigs"] <= 27) & (filtered_May2016["Tamworth pigs"] >= 7)]
    print("number passed June 2016 filters:", len(accepted_June2016))
    filtered_June2016 = filtered_May2016[filtered_May2016['run_number'].isin(accepted_June2016['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_June2016.run_number.values): row["passed filters"] +=1 
    # July 2016
    accepted_July2016 = filtered_June2016[(filtered_June2016["Time"] == 138) &
    (filtered_June2016["Exmoor pony"] <= 12) & (filtered_June2016["Exmoor pony"] >= 10) &
    (filtered_June2016["Longhorn cattle"] <= 112) & (filtered_June2016["Longhorn cattle"] >= 62) &
    (filtered_June2016["Tamworth pigs"] <= 27) & (filtered_June2016["Tamworth pigs"] >= 7)]
    print("number passed July 2016 filters:", len(accepted_July2016))
    filtered_July2016 = filtered_June2016[filtered_June2016['run_number'].isin(accepted_July2016['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_July2016.run_number.values): row["passed filters"] +=1 
    # Aug 2016
    accepted_Aug2016 = filtered_July2016[(filtered_July2016["Time"] == 139) &
    (filtered_July2016["Exmoor pony"] <= 12) & (filtered_July2016["Exmoor pony"] >= 10) &
    (filtered_July2016["Longhorn cattle"] <= 112) & (filtered_July2016["Longhorn cattle"] >= 62) &
    (filtered_July2016["Tamworth pigs"] <= 27) & (filtered_July2016["Tamworth pigs"] >= 7)]
    print("number passed Aug 2016 filters:", len(accepted_Aug2016))
    filtered_Aug2016 = filtered_July2016[filtered_July2016['run_number'].isin(accepted_Aug2016['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Aug2016.run_number.values): row["passed filters"] +=1 
    # Sept 2016
    accepted_Sept2016 = filtered_Aug2016[(filtered_Aug2016["Time"] == 140) &
    (filtered_Aug2016["Exmoor pony"] <= 12) & (filtered_Aug2016["Exmoor pony"] >= 10) &
    (filtered_Aug2016["Longhorn cattle"] <= 122) & (filtered_Aug2016["Longhorn cattle"] >= 72) &
    (filtered_Aug2016["Tamworth pigs"] <= 27) & (filtered_Aug2016["Tamworth pigs"] >= 7)]
    print("number passed Sept 2016 filters:", len(accepted_Sept2016))
    filtered_Sept2016 = filtered_Aug2016[filtered_Aug2016['run_number'].isin(accepted_Sept2016['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Sept2016.run_number.values): row["passed filters"] +=1 
    # Oct 2016
    accepted_Oct2016 = filtered_Sept2016[(filtered_Sept2016["Time"] == 141) &
    (filtered_Sept2016["Exmoor pony"] <= 12) & (filtered_Sept2016["Exmoor pony"] >= 10) &
    (filtered_Sept2016["Longhorn cattle"] <= 122) & (filtered_Sept2016["Longhorn cattle"] >= 72) &
    (filtered_Sept2016["Tamworth pigs"] <= 27) & (filtered_Sept2016["Tamworth pigs"] >= 7)]
    print("number passed Oct 2016 filters:", len(accepted_Oct2016))
    filtered_Oct2016 = filtered_Aug2016[filtered_Aug2016['run_number'].isin(accepted_Oct2016['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Oct2016.run_number.values): row["passed filters"] +=1 
    # Nov 2016
    accepted_Nov2016 = filtered_Oct2016[(filtered_Oct2016["Time"] == 142) &
    (filtered_Oct2016["Exmoor pony"] <= 12) & (filtered_Oct2016["Exmoor pony"] >= 10) &
    (filtered_Oct2016["Longhorn cattle"] <= 117) & (filtered_Oct2016["Longhorn cattle"] >= 67) &
    (filtered_Oct2016["Tamworth pigs"] <= 27) & (filtered_Oct2016["Tamworth pigs"] >= 7)]
    print("number passed Nov 2016 filters:", len(accepted_Nov2016))
    filtered_Nov2016 = filtered_Oct2016[filtered_Oct2016['run_number'].isin(accepted_Nov2016['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Nov2016.run_number.values): row["passed filters"] +=1 
    # Dec 2016
    accepted_Dec2016 = filtered_Nov2016[(filtered_Nov2016["Time"] == 143) &
    (filtered_Nov2016["Exmoor pony"] <= 12) & (filtered_Nov2016["Exmoor pony"] >= 10) &
    (filtered_Nov2016["Longhorn cattle"] <= 104) & (filtered_Nov2016["Longhorn cattle"] >= 54)&
    (filtered_Nov2016["Tamworth pigs"] <= 23) & (filtered_Nov2016["Tamworth pigs"] >= 3)]
    print("number passed Dec 2016 filters:", len(accepted_Dec2016))
    filtered_Dec2016 = filtered_Nov2016[filtered_Nov2016['run_number'].isin(accepted_Dec2016['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Dec2016.run_number.values): row["passed filters"] +=1 
    # Jan 2017
    accepted_Jan2017= filtered_Dec2016[(filtered_Dec2016["Time"] == 144) &
    (filtered_Dec2016["Exmoor pony"] <= 12) & (filtered_Dec2016["Exmoor pony"] >= 10) &
    (filtered_Dec2016["Longhorn cattle"] <= 104) & (filtered_Dec2016["Longhorn cattle"] >= 54) &
    (filtered_Dec2016["Tamworth pigs"] <= 19) & (filtered_Dec2016["Tamworth pigs"] >= 1)]
    print("number passed Jan 2017 filters:", len(accepted_Jan2017))
    filtered_Jan2017 = filtered_Dec2016[filtered_Dec2016['run_number'].isin(accepted_Jan2017['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Jan2017.run_number.values): row["passed filters"] +=1 
    # Feb 2017
    accepted_Feb2017 = filtered_Jan2017[(filtered_Jan2017["Time"] == 145) &
    (filtered_Jan2017["Exmoor pony"] <= 12) & (filtered_Jan2017["Exmoor pony"] >= 10) &
    (filtered_Jan2017["Longhorn cattle"] <= 104) & (filtered_Jan2017["Longhorn cattle"] >= 54) &
    (filtered_Jan2017["Tamworth pigs"] <= 17) & (filtered_Jan2017["Tamworth pigs"] >= 1)]
    print("number passed Feb 2017 filters:", len(accepted_Feb2017))
    filtered_Feb2017 = filtered_Jan2017[filtered_Jan2017['run_number'].isin(accepted_Feb2017['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Feb2017.run_number.values): row["passed filters"] +=1 
    
    
    # March 2017
    accepted_March2017 = filtered_Feb2017[(filtered_Feb2017["Time"] == 146) &
    (filtered_Feb2017["Exmoor pony"] <= 11) & (filtered_Feb2017["Exmoor pony"] >= 9) &
    (filtered_Feb2017["Fallow deer"] <= 215) & (filtered_Feb2017["Fallow deer"] >= 115) &
    (filtered_Feb2017["Longhorn cattle"] <= 104) & (filtered_Feb2017["Longhorn cattle"] >= 54) &
    (filtered_Feb2017["Tamworth pigs"] <= 17) & (filtered_Feb2017["Tamworth pigs"] >= 1)]
    print("number passed March 2017 filters:", len(accepted_March2017))
    filtered_March2017 = filtered_Feb2017[filtered_Feb2017['run_number'].isin(accepted_March2017['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_March2017.run_number.values): row["passed filters"] +=1 
    # April 2017
    accepted_April2017 = filtered_March2017[(filtered_March2017["Time"] == 147) &
    (filtered_March2017["Exmoor pony"] <= 11) & (filtered_March2017["Exmoor pony"] >= 9) &
    (filtered_March2017["Longhorn cattle"] <= 125) & (filtered_March2017["Longhorn cattle"] >= 75) &
    (filtered_March2017["Tamworth pigs"] <= 32) & (filtered_March2017["Tamworth pigs"] >= 12)]
    print("number passed April 2017 filters:", len(accepted_April2017))
    filtered_April2017 = filtered_March2017[filtered_March2017['run_number'].isin(accepted_April2017['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_April2017.run_number.values): row["passed filters"] +=1 
    # May 2017
    accepted_May2017 = filtered_April2017[(filtered_April2017["Time"] == 148) &
    (filtered_April2017["Exmoor pony"] <= 11) & (filtered_April2017["Exmoor pony"] >= 9) &
    (filtered_April2017["Longhorn cattle"] <= 134) & (filtered_April2017["Longhorn cattle"] >= 84) &
    (filtered_April2017["Tamworth pigs"] <= 32) & (filtered_April2017["Tamworth pigs"] >= 12)]
    print("number passed May 2017 filters:", len(accepted_May2017))
    filtered_May2017 = filtered_April2017[filtered_April2017['run_number'].isin(accepted_May2017['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_May2017.run_number.values): row["passed filters"] +=1 
    # June 2017
    accepted_June2017 = filtered_May2017[(filtered_May2017["Time"] == 149) &
    (filtered_May2017["Exmoor pony"] <= 11) & (filtered_May2017["Exmoor pony"] >= 9) &
    (filtered_May2017["Longhorn cattle"] <= 119) & (filtered_May2017["Longhorn cattle"] >= 69) &
    (filtered_May2017["Tamworth pigs"] <= 32) & (filtered_May2017["Tamworth pigs"] >= 12)]
    print("number passed June 2017 filters:", len(accepted_June2017))
    filtered_June2017 = filtered_May2017[filtered_May2017['run_number'].isin(accepted_June2017['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_June2017.run_number.values): row["passed filters"] +=1 
    # July 2017
    accepted_July2017 = filtered_June2017[(filtered_June2017["Time"] == 150) &
    (filtered_June2017["Exmoor pony"] <= 11) & (filtered_June2017["Exmoor pony"] >= 9) &
    (filtered_June2017["Longhorn cattle"] <= 119) & (filtered_June2017["Longhorn cattle"] >= 69)&
    (filtered_June2017["Tamworth pigs"] <= 32) & (filtered_June2017["Tamworth pigs"] >= 12)]
    print("number passed July 2017 filters:", len(accepted_July2017))
    filtered_July2017 = filtered_June2017[filtered_June2017['run_number'].isin(accepted_July2017['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_July2017.run_number.values): row["passed filters"] +=1 
    # Aug 2017
    accepted_Aug2017 = filtered_July2017[(filtered_July2017["Time"] == 151) &
    (filtered_July2017["Exmoor pony"] <= 11) & (filtered_July2017["Exmoor pony"] >= 9) &
    (filtered_July2017["Longhorn cattle"] <= 119) & (filtered_July2017["Longhorn cattle"] >= 69)&
    (filtered_July2017["Tamworth pigs"] <= 32) & (filtered_July2017["Tamworth pigs"] >= 12)]
    print("number passed Aug 2017 filters:", len(accepted_Aug2017))
    filtered_Aug2017 = filtered_July2017[filtered_July2017['run_number'].isin(accepted_Aug2017['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Aug2017.run_number.values): row["passed filters"] +=1 
    # Sept 2017
    accepted_Sept2017 = filtered_Aug2017[(filtered_Aug2017["Time"] == 152) &
    (filtered_Aug2017["Exmoor pony"] <= 11) & (filtered_Aug2017["Exmoor pony"] >= 9) &
    (filtered_Aug2017["Longhorn cattle"] <= 115) & (filtered_Aug2017["Longhorn cattle"] >= 65)&
    (filtered_Aug2017["Tamworth pigs"] <= 32) & (filtered_Aug2017["Tamworth pigs"] >= 12)]
    print("number passed Sept 2017 filters:", len(accepted_Sept2017))
    filtered_Sept2017 = filtered_Aug2017[filtered_Aug2017['run_number'].isin(accepted_Sept2017['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Sept2017.run_number.values): row["passed filters"] +=1 
    # Oct 2017
    accepted_Oct2017 = filtered_Sept2017[(filtered_Sept2017["Time"] == 153) &
    (filtered_Sept2017["Exmoor pony"] <= 11) & (filtered_Sept2017["Exmoor pony"] >= 9) &
    (filtered_Sept2017["Longhorn cattle"] <= 113) & (filtered_Sept2017["Longhorn cattle"] >= 63)&
    (filtered_Sept2017["Tamworth pigs"] <= 32) & (filtered_Sept2017["Tamworth pigs"] >= 12)]
    print("number passed Oct 2017 filters:", len(accepted_Oct2017))
    filtered_Oct2017 = filtered_Sept2017[filtered_Sept2017['run_number'].isin(accepted_Oct2017['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Oct2017.run_number.values): row["passed filters"] +=1 
    # Nov 2017
    accepted_Nov2017 = filtered_Oct2017[(filtered_Oct2017["Time"] == 154) &
    (filtered_Oct2017["Exmoor pony"] <= 11) & (filtered_Oct2017["Exmoor pony"] >= 9) &
    (filtered_Oct2017["Longhorn cattle"] <= 113) & (filtered_Oct2017["Longhorn cattle"] >= 63)&
    (filtered_Oct2017["Tamworth pigs"] <= 32) & (filtered_Oct2017["Tamworth pigs"] >= 12)]
    print("number passed Nov 2017 filters:", len(accepted_Nov2017))
    filtered_Nov2017 = filtered_Oct2017[filtered_Oct2017['run_number'].isin(accepted_Nov2017['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Nov2017.run_number.values): row["passed filters"] +=1 
    # Dec 2017
    accepted_Dec2017 = filtered_Nov2017[(filtered_Nov2017["Time"] == 155) &
    (filtered_Nov2017["Exmoor pony"] <= 11) & (filtered_Nov2017["Exmoor pony"] >= 9) &
    (filtered_Nov2017["Longhorn cattle"] <= 113) & (filtered_Nov2017["Longhorn cattle"] >= 63)&
    (filtered_Nov2017["Tamworth pigs"] <= 28) & (filtered_Nov2017["Tamworth pigs"] >= 8)]
    print("number passed Dec 2017 filters:", len(accepted_Dec2017))
    filtered_Dec2017 = filtered_Nov2017[filtered_Nov2017['run_number'].isin(accepted_Dec2017['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Dec2017.run_number.values): row["passed filters"] +=1 
    # January 2018
    accepted_Jan2018 = filtered_Dec2017[(filtered_Dec2017["Time"] == 156) &
    (filtered_Dec2017["Exmoor pony"] <= 11) & (filtered_Dec2017["Exmoor pony"] >= 9) &
    (filtered_Dec2017["Longhorn cattle"] <= 113) & (filtered_Dec2017["Longhorn cattle"] >= 63)&
    (filtered_Dec2017["Tamworth pigs"] <= 21) & (filtered_Dec2017["Tamworth pigs"] >= 1)]
    print("number passed January 2018 filters:", len(accepted_Jan2018))
    filtered_Jan2018 = filtered_Dec2017[filtered_Dec2017['run_number'].isin(accepted_Jan2018['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Jan2018.run_number.values): row["passed filters"] +=1 
    # February 2018
    accepted_Feb2018 = filtered_Jan2018[(filtered_Jan2018["Time"] == 157) &
    (filtered_Jan2018["Exmoor pony"] <= 11) & (filtered_Jan2018["Exmoor pony"] >= 9) &
    (filtered_Jan2018["Longhorn cattle"] <= 113) & (filtered_Jan2018["Longhorn cattle"] >= 63)&
    (filtered_Jan2018["Tamworth pigs"] <= 26) & (filtered_Jan2018["Tamworth pigs"] >= 6)]
    print("number passed Feb 2018 filters:", len(accepted_Feb2018)) 
    filtered_Feb2018 = filtered_Jan2018[filtered_Jan2018['run_number'].isin(accepted_Feb2018['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Feb2018.run_number.values): row["passed filters"] +=1 
    
    # March 2018
    accepted_March2018 = filtered_Feb2018[(filtered_Feb2018["Time"] == 158) &
    (filtered_Feb2018["Exmoor pony"] <= 10) & (filtered_Feb2018["Exmoor pony"] >= 8) &
    (filtered_Feb2018["Longhorn cattle"] <= 113) & (filtered_Feb2018["Longhorn cattle"] >= 63) &
    (filtered_Feb2018["Red deer"] <= 29) & (filtered_Feb2018["Red deer"] >= 19) &
    (filtered_Feb2018["Tamworth pigs"] <= 26) & (filtered_Feb2018["Tamworth pigs"] >= 6)]
    print("number passed March 2018 filters:", len(accepted_March2018)) 
    filtered_March2018 = filtered_Feb2018[filtered_Feb2018['run_number'].isin(accepted_March2018['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_March2018.run_number.values): row["passed filters"] +=1 
    # April 2018
    accepted_April2018 = filtered_March2018[(filtered_March2018["Time"] == 159) &
    (filtered_March2018["Exmoor pony"] <= 10) & (filtered_March2018["Exmoor pony"] >= 8) &
    (filtered_March2018["Longhorn cattle"] <= 126) & (filtered_March2018["Longhorn cattle"] >= 76) &
    (filtered_March2018["Tamworth pigs"] <= 26) & (filtered_March2018["Tamworth pigs"] >= 6)]
    print("number passed April 2018 filters:", len(accepted_April2018)) 
    filtered_April2018 = filtered_March2018[filtered_March2018['run_number'].isin(accepted_April2018['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_April2018.run_number.values): row["passed filters"] +=1 
    # May 2018
    accepted_May2018 = filtered_April2018[(filtered_April2018["Time"] == 160) &
    (filtered_April2018["Exmoor pony"] <= 10) & (filtered_April2018["Exmoor pony"] >= 8) &
    (filtered_April2018["Longhorn cattle"] <= 142) & (filtered_April2018["Longhorn cattle"] >= 92)&
    (filtered_April2018["Tamworth pigs"] <= 33) & (filtered_April2018["Tamworth pigs"] >= 13)]
    print("number passed May 2018 filters:", len(accepted_May2018)) 
    filtered_May2018 = filtered_April2018[filtered_April2018['run_number'].isin(accepted_May2018['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_May2018.run_number.values): row["passed filters"] +=1 
    # June 2018
    accepted_June2018 = filtered_May2018[(filtered_May2018["Time"] == 161) &
    (filtered_May2018["Exmoor pony"] <= 10) & (filtered_May2018["Exmoor pony"] >= 8) &
    (filtered_May2018["Longhorn cattle"] <= 128) & (filtered_May2018["Longhorn cattle"] >= 78)&
    (filtered_May2018["Tamworth pigs"] <= 33) & (filtered_May2018["Tamworth pigs"] >= 13)]
    print("number passed June 2018 filters:", len(accepted_June2018)) 
    filtered_June2018 = filtered_May2018[filtered_May2018['run_number'].isin(accepted_June2018['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_June2018.run_number.values): row["passed filters"] +=1 
    # July 2018
    accepted_July2018 = filtered_June2018[(filtered_June2018["Time"] == 162) &
    (filtered_June2018["Exmoor pony"] <= 10) & (filtered_June2018["Exmoor pony"] >= 8) &
    (filtered_June2018["Longhorn cattle"] <= 128) & (filtered_June2018["Longhorn cattle"] >= 78)&
    (filtered_June2018["Tamworth pigs"] <= 32) & (filtered_June2018["Tamworth pigs"] >= 12)]
    print("number passed July 2018 filters:", len(accepted_July2018)) 
    filtered_July2018 = filtered_June2018[filtered_June2018['run_number'].isin(accepted_July2018['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_July2018.run_number.values): row["passed filters"] +=1 
    # Aug 2018
    accepted_Aug2018 = filtered_July2018[(filtered_July2018["Time"] == 163) &
    (filtered_July2018["Longhorn cattle"] <= 127) & (filtered_July2018["Longhorn cattle"] >= 77) &
    (filtered_July2018["Tamworth pigs"] <= 32) & (filtered_July2018["Tamworth pigs"] >= 12)]
    print("number passed Aug 2018 filters:", len(accepted_Aug2018)) 
    filtered_Aug2018 = filtered_July2018[filtered_July2018['run_number'].isin(accepted_Aug2018['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Aug2018.run_number.values): row["passed filters"] +=1 
    # Sept 2018
    accepted_Sept2018 = filtered_Aug2018[(filtered_Aug2018["Time"] == 164) &
    (filtered_Aug2018["Longhorn cattle"] <= 131) & (filtered_Aug2018["Longhorn cattle"] >= 81) &
    (filtered_Aug2018["Tamworth pigs"] <= 32) & (filtered_Aug2018["Tamworth pigs"] >= 12)]
    print("number passed Sept 2018 filters:", len(accepted_Sept2018)) 
    filtered_Sept2018 = filtered_Aug2018[filtered_Aug2018['run_number'].isin(accepted_Sept2018['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Sept2018.run_number.values): row["passed filters"] +=1 
    # Oct 2018
    accepted_Oct2018 = filtered_Sept2018[(filtered_Sept2018["Time"] == 165) &
    (filtered_Sept2018["Longhorn cattle"] <= 126) & (filtered_Sept2018["Longhorn cattle"] >= 76) &
    (filtered_Sept2018["Tamworth pigs"] <= 31) & (filtered_Sept2018["Tamworth pigs"] >= 11)]
    print("number passed Oct 2018 filters:", len(accepted_Oct2018))
    filtered_Oct2018 = filtered_Sept2018[filtered_Sept2018['run_number'].isin(accepted_Oct2018['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Oct2018.run_number.values): row["passed filters"] +=1 
    # Nov 2018
    accepted_Nov2018 = filtered_Oct2018[(filtered_Oct2018["Time"] == 166) &
    (filtered_Oct2018["Longhorn cattle"] <= 118) & (filtered_Oct2018["Longhorn cattle"] >= 68) &
    (filtered_Oct2018["Tamworth pigs"] <= 19) & (filtered_Oct2018["Tamworth pigs"] >= 1)]
    print("number passed Nov 2018 filters:", len(accepted_Nov2018)) 
    filtered_Nov2018 = filtered_Oct2018[filtered_Oct2018['run_number'].isin(accepted_Nov2018['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Nov2018.run_number.values): row["passed filters"] +=1 
    # Dec 2018
    accepted_Dec2018 = filtered_Nov2018[(filtered_Nov2018["Time"] == 167) &
    (filtered_Nov2018["Longhorn cattle"] <= 114) & (filtered_Nov2018["Longhorn cattle"] >= 64) &
    (filtered_Nov2018["Tamworth pigs"] <= 19) & (filtered_Nov2018["Tamworth pigs"] >= 1)]
    print("number passed Dec 2018 filters:", len(accepted_Dec2018)) 
    filtered_Dec2018 = filtered_Nov2018[filtered_Nov2018['run_number'].isin(accepted_Dec2018['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Dec2018.run_number.values): row["passed filters"] +=1 
    # Jan 2019
    accepted_Jan2019 = filtered_Dec2018[(filtered_Dec2018["Time"] == 168) &
    (filtered_Dec2018["Longhorn cattle"] <= 114) & (filtered_Dec2018["Longhorn cattle"] >= 64) &
    (filtered_Dec2018["Tamworth pigs"] <= 19) & (filtered_Dec2018["Tamworth pigs"] >= 1)]
    print("number passed Jan 2019 filters:", len(accepted_Jan2019)) 
    filtered_Jan2019 = filtered_Dec2018[filtered_Dec2018['run_number'].isin(accepted_Jan2019['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Jan2019.run_number.values): row["passed filters"] +=1 
    # Feb 2019
    accepted_Feb2019 = filtered_Jan2019[(filtered_Jan2019["Time"] == 169) &
    (filtered_Jan2019["Longhorn cattle"] <= 112) & (filtered_Jan2019["Longhorn cattle"] >= 62) &
    (filtered_Jan2019["Tamworth pigs"] <= 20) & (filtered_Jan2019["Tamworth pigs"] >= 1)]
    print("number passed Feb 2019 filters:", len(accepted_Feb2019)) 
    filtered_Feb2019 = filtered_Jan2019[filtered_Jan2019['run_number'].isin(accepted_Feb2019['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Feb2019.run_number.values): row["passed filters"] +=1 
    
    
    
    # # March 2019
    # accepted_March2019 = filtered_Feb2019[(filtered_Feb2019["Time"] == 170) &
    # (filtered_Feb2019["Fallow deer"] <= 303) & (filtered_Feb2019["Fallow deer"] >= 253) &
    # (filtered_Feb2019["Longhorn cattle"] <= 112) & (filtered_Feb2019["Longhorn cattle"] >= 62) &
    # (filtered_Feb2019["Red deer"] <= 42) & (filtered_Feb2019["Red deer"] >= 32) &
    # (filtered_Feb2019["Tamworth pigs"] <= 19) & (filtered_Feb2019["Tamworth pigs"] >= 1)]
    # print("number passed March 2019 filters:", len(accepted_March2019)) 
    # filtered_March2019 = filtered_Feb2019[filtered_Feb2019['run_number'].isin(accepted_March2019['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Feb2019.run_number.values): row["passed filters"] +=1 
    # # April 2019
    # accepted_April2019 = filtered_March2019[(filtered_March2019["Time"] == 171) &
    # (filtered_March2019["Longhorn cattle"] <= 126) & (filtered_March2019["Longhorn cattle"] >= 76) &
    # (filtered_March2019["Tamworth pigs"] <= 18) & (filtered_March2019["Tamworth pigs"] >= 1)]
    # print("number passed April 2019 filters:", len(accepted_April2019)) 
    # filtered_April2019 = filtered_March2019[filtered_March2019['run_number'].isin(accepted_April2019['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Feb2019.run_number.values): row["passed filters"] +=1 
    # # May 2019
    # accepted_May2019 = filtered_April2019[(filtered_April2019["Time"] == 172) &
    # (filtered_April2019["Longhorn cattle"] <= 135) & (filtered_April2019["Longhorn cattle"] >= 85) &
    # (filtered_April2019["Tamworth pigs"] <= 18) & (filtered_April2019["Tamworth pigs"] >= 1)]
    # print("number passed May 2019 filters:", len(accepted_May2019))
    # filtered_May2019 = filtered_April2019[filtered_April2019['run_number'].isin(accepted_May2019['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Feb2019.run_number.values): row["passed filters"] +=1 
    # # June 2019
    # accepted_June2019 = filtered_May2019[(filtered_May2019["Time"] == 173) &
    # (filtered_May2019["Longhorn cattle"] <= 114) & (filtered_May2019["Longhorn cattle"] >= 64) &
    # (filtered_May2019["Tamworth pigs"] <= 18) & (filtered_May2019["Tamworth pigs"] >= 1)]
    # print("number passed June 2019 filters:", len(accepted_June2019)) 
    # filtered_June2019 = filtered_May2019[filtered_May2019['run_number'].isin(accepted_June2019['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Feb2019.run_number.values): row["passed filters"] +=1 
    # # July 2019
    # accepted_July2019 = filtered_June2019[(filtered_June2019["Time"] == 174) &
    # (filtered_June2019["Longhorn cattle"] <= 116) & (filtered_June2019["Longhorn cattle"] >= 66) &
    # (filtered_June2019["Tamworth pigs"] <= 19) & (filtered_June2019["Tamworth pigs"] >= 1)]
    # print("number passed July 2019 filters:", len(accepted_July2019)) 
    # filtered_July2019 = filtered_June2019[filtered_June2019['run_number'].isin(accepted_July2019['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Feb2019.run_number.values): row["passed filters"] +=1 
    # # Aug 2019
    # accepted_Aug2019 = filtered_July2019[(filtered_July2019["Time"] == 175) &
    # (filtered_July2019["Longhorn cattle"] <= 116) & (filtered_July2019["Longhorn cattle"] >= 66) &
    # (filtered_July2019["Tamworth pigs"] <= 19) & (filtered_July2019["Tamworth pigs"] >= 1)]
    # print("number passed Aug 2019 filters:", len(accepted_Aug2019)) 
    # filtered_Aug2019 = filtered_July2019[filtered_July2019['run_number'].isin(accepted_Aug2019['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Feb2019.run_number.values): row["passed filters"] +=1 
    # # Sept 2019
    # accepted_Sept2019 = filtered_Aug2019[(filtered_Aug2019["Time"] == 176) &
    # (filtered_Aug2019["Longhorn cattle"] <= 118) & (filtered_Aug2019["Longhorn cattle"] >= 68) &
    # (filtered_Aug2019["Tamworth pigs"] <= 19) & (filtered_Aug2019["Tamworth pigs"] >= 1)]
    # print("number passed Sept 2019 filters:", len(accepted_Sept2019)) 
    # filtered_Sept2019 = filtered_Aug2019[filtered_Aug2019['run_number'].isin(accepted_Sept2019['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Feb2019.run_number.values): row["passed filters"] +=1 
    # # Oct 2019
    # accepted_Oct2019 = filtered_Sept2019[(filtered_Sept2019["Time"] == 177) &
    # (filtered_Sept2019["Longhorn cattle"] <= 113) & (filtered_Sept2019["Longhorn cattle"] >= 63) &
    # (filtered_Sept2019["Tamworth pigs"] <= 19) & (filtered_Sept2019["Tamworth pigs"] >= 1)]
    # print("number passed Oct 2019 filters:", len(accepted_Oct2019)) 
    # filtered_Oct2019 = filtered_Sept2019[filtered_Sept2019['run_number'].isin(accepted_Oct2019['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Feb2019.run_number.values): row["passed filters"] +=1 
    # # Nov 2019
    # accepted_Nov2019 = filtered_Oct2019[(filtered_Oct2019["Time"] == 178) &
    # (filtered_Oct2019["Longhorn cattle"] <= 112) & (filtered_Oct2019["Longhorn cattle"] >= 62) &
    # (filtered_Oct2019["Tamworth pigs"] <= 19) & (filtered_Oct2019["Tamworth pigs"] >= 1)]
    # print("number passed Nov 2019 filters:", len(accepted_Nov2019)) 
    # filtered_Nov2019 = filtered_Oct2019[filtered_Oct2019['run_number'].isin(accepted_Nov2019['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Feb2019.run_number.values): row["passed filters"] +=1 
    # # Dec 2019
    # accepted_Dec2019 = filtered_Nov2019[(filtered_Nov2019["Time"] == 179) &
    # (filtered_Nov2019["Longhorn cattle"] <= 105) & (filtered_Nov2019["Longhorn cattle"] >= 55) &
    # (filtered_Nov2019["Tamworth pigs"] <= 20) & (filtered_Nov2019["Tamworth pigs"] >= 1)]
    # print("number passed Dec 2019 filters:", len(accepted_Dec2019))
    # filtered_Dec2019 = filtered_Nov2019[filtered_Nov2019['run_number'].isin(accepted_Dec2019['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Feb2019.run_number.values): row["passed filters"] +=1 
    # # Jan 2020
    # accepted_Jan2020 = filtered_Dec2019[(filtered_Dec2019["Time"] == 180) &
    # (filtered_Dec2019["Longhorn cattle"] <= 105) & (filtered_Dec2019["Longhorn cattle"] >= 55) &
    # (filtered_Dec2019["Tamworth pigs"] <= 20) & (filtered_Dec2019["Tamworth pigs"] >= 1)]
    # print("number passed Jan 2020 filters:", len(accepted_Jan2020))
    # filtered_Jan2020 = filtered_Dec2019[filtered_Dec2019['run_number'].isin(accepted_Jan2020['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Feb2019.run_number.values): row["passed filters"] +=1 
    # # Feb 2020
    # accepted_Feb2020 = filtered_Jan2020[(filtered_Jan2020["Time"] == 181) &
    # (filtered_Jan2020["Longhorn cattle"] <= 104) & (filtered_Jan2020["Longhorn cattle"] >= 54) &
    # (filtered_Jan2020["Tamworth pigs"] <= 18) & (filtered_Jan2020["Tamworth pigs"] >= 1)]
    # print("number passed Feb 2020 filters:", len(accepted_Feb2020))
    # filtered_Feb2020 = filtered_Jan2020[filtered_Jan2020['run_number'].isin(accepted_Feb2020['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Feb2019.run_number.values): row["passed filters"] +=1 
    
    
    # # March 2020
    # accepted_March2020 = filtered_Feb2020[(filtered_Feb2020["Time"] == 182) &
    # (filtered_Feb2020["Fallow deer"] <= 272) & (filtered_Feb2020["Fallow deer"] >= 222) &
    # (filtered_Feb2020["Red deer"] <= 40) & (filtered_Feb2020["Red deer"] >= 32) &
    # (filtered_Feb2020["Longhorn cattle"] <= 106) & (filtered_Feb2020["Longhorn cattle"] >= 56)&
    # (filtered_Feb2020["Tamworth pigs"] <= 17) & (filtered_Feb2020["Tamworth pigs"] >= 1)]
    # print("number passed March 2020 filters:", len(accepted_March2020)) 
    # filtered_March2020 = filtered_Feb2020[filtered_Feb2020['run_number'].isin(accepted_March2020['run_number'])]
    # # April 2020
    # accepted_April2020 = filtered_March2020[(filtered_March2020["Time"] == 183) &
    # (filtered_March2020["Exmoor pony"] <= 17) & (filtered_March2020["Exmoor pony"] >= 14) &
    # (filtered_March2020["Longhorn cattle"] <= 106) & (filtered_March2020["Longhorn cattle"] >= 56) &
    # (filtered_March2020["Tamworth pigs"] <= 17) & (filtered_March2020["Tamworth pigs"] >= 1)]
    # print("number passed April 2020 filters:", len(accepted_April2020)) 
    # filtered_April2020 = filtered_March2020[filtered_March2020['run_number'].isin(accepted_April2020['run_number'])]
    # May 2020
    all_accepted_runs = filtered_preReintro[(filtered_preReintro["Time"] == 184) &
    # (filtered_preReintro["Tamworth pigs"] <= 29) & (filtered_preReintro["Tamworth pigs"] >= 9) &
    (filtered_preReintro["Exmoor pony"] <= 17) & (filtered_preReintro["Exmoor pony"] >= 14) &
    # (filtered_preReintro["Longhorn cattle"] <= 106) & (filtered_preReintro["Longhorn cattle"] >= 56) &
    (filtered_preReintro["Roe deer"] <= 80) & (filtered_preReintro["Roe deer"] >= 20) & 
    (filtered_preReintro["Grassland"] <= 69) & (filtered_preReintro["Grassland"] >= 49) & 
    (filtered_preReintro["Thorny Scrub"] <= 35) & (filtered_preReintro["Thorny Scrub"] >= 21) &
    (filtered_preReintro["Woodland"] <= 29) & (filtered_preReintro["Woodland"] >= 9)]

    print("number passed all filters:", len(all_accepted_runs))

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


    # save to csv
    # accepted_parameters.to_csv('/Users/emilyneil/Desktop/KneppABM/outputs/one_perc/accepted_parameters.csv')
    accepted_parameters.to_csv('accepted_parameters.csv')

    return number_simulations, final_results, accepted_parameters

