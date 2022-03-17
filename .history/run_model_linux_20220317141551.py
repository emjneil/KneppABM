# ------ ABM of the Knepp Estate (2005-2046) --------
from KneppModel_ABM import KneppModel 
import numpy as np
import random
import pandas as pd


# # # # Run the model # # # # 


def run_all_models():

    # define number of simulations
    number_simulations =  5
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
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # April 2015
    my_time = final_results.loc[final_results['Time'] == 123]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Longhorn cattle"] <= 140) & (row["Longhorn cattle"] >= 90) & (row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # May 2015
    my_time = final_results.loc[final_results['Time'] == 124]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 154) & (row["Longhorn cattle"] >= 104) & (row["Tamworth pigs"] <= 24) & (row["Tamworth pigs"] >= 4) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # June 2015
    my_time = final_results.loc[final_results['Time'] == 125]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 154) & (row["Longhorn cattle"] >= 104) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 24) & (row["Tamworth pigs"] >= 4):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # July 2015
    my_time = final_results.loc[final_results['Time'] == 126]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 154) & (row["Longhorn cattle"] >= 104) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 24) & (row["Tamworth pigs"] >= 4):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Aug 2015
    my_time = final_results.loc[final_results['Time'] == 127]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 154) & (row["Longhorn cattle"] >= 104) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 24) & (row["Tamworth pigs"] >= 4):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Sept 2015
    my_time = final_results.loc[final_results['Time'] == 128]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 155) & (row["Longhorn cattle"] >= 105) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 24) & (row["Tamworth pigs"] >= 4):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Oct 2015
    my_time = final_results.loc[final_results['Time'] == 129]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 116) & (row["Longhorn cattle"] >= 66) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 24) & (row["Tamworth pigs"] >= 4):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Nov 2015
    my_time = final_results.loc[final_results['Time'] == 130]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 116) & (row["Longhorn cattle"] >= 66) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 23) & (row["Tamworth pigs"] >= 3):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Dec 2015
    my_time = final_results.loc[final_results['Time'] == 131]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 111) & (row["Longhorn cattle"] >= 61) &(row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Tamworth pigs"] <= 23) & (row["Tamworth pigs"] >= 3):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Jan 2016
    my_time = final_results.loc[final_results['Time'] == 132]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 111) & (row["Longhorn cattle"] >= 61) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Feb 2016
    my_time = final_results.loc[final_results['Time'] == 133]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Longhorn cattle"] <= 111) & (row["Longhorn cattle"] >= 61) &(row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # March 2016
    my_time = final_results.loc[final_results['Time'] == 134]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 111) & (row["Longhorn cattle"] >= 61) & (row["Fallow deer"] <= 190) & (row["Fallow deer"] >= 90) & (row["Red deer"] <= 31) & (row["Red deer"] >= 21) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # April 2016
    my_time = final_results.loc[final_results['Time'] == 135]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 128) & (row["Longhorn cattle"] >= 78) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # May 2016
    my_time = final_results.loc[final_results['Time'] == 136]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 133) & (row["Longhorn cattle"] >= 83) &(row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # June 2016
    my_time = final_results.loc[final_results['Time'] == 137]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 114) & (row["Longhorn cattle"] >= 64) & (row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # July 2016
    my_time = final_results.loc[final_results['Time'] == 138]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) & (row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Aug 2016
    my_time = final_results.loc[final_results['Time'] == 139]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) & (row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Sept 2016
    my_time = final_results.loc[final_results['Time'] == 140]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) &(row["Longhorn cattle"] <= 122) & (row["Longhorn cattle"] >= 72) & (row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Oct 2016
    my_time = final_results.loc[final_results['Time'] == 141]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 122) & (row["Longhorn cattle"] >= 72) & (row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Nov 2016
    my_time = final_results.loc[final_results['Time'] == 142]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) &(row["Longhorn cattle"] <= 117) & (row["Longhorn cattle"] >= 67) &(row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Dec 2016
    my_time = final_results.loc[final_results['Time'] == 143]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) &(row["Longhorn cattle"] <= 104) & (row["Longhorn cattle"] >= 54)& (row["Tamworth pigs"] <= 23) & (row["Tamworth pigs"] >= 3):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Jan 2017
    my_time = final_results.loc[final_results['Time'] == 144]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 104) & (row["Longhorn cattle"] >= 54) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Feb 2017
    my_time = final_results.loc[final_results['Time'] == 145]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 104) & (row["Longhorn cattle"] >= 54) & (row["Tamworth pigs"] <= 17) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 


    # March 2017
    my_time = final_results.loc[final_results['Time'] == 146]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Fallow deer"] <= 215) & (row["Fallow deer"] >= 115) &(row["Longhorn cattle"] <= 104) & (row["Longhorn cattle"] >= 54) &(row["Tamworth pigs"] <= 17) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # April 2017
    my_time = final_results.loc[final_results['Time'] == 147]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 125) & (row["Longhorn cattle"] >= 75) &(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # May 2017
    my_time = final_results.loc[final_results['Time'] == 148]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if  (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 134) & (row["Longhorn cattle"] >= 84) &(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # June 2017
    my_time = final_results.loc[final_results['Time'] == 149]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 119) & (row["Longhorn cattle"] >= 69) &(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # July 2017
    my_time = final_results.loc[final_results['Time'] == 150]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 119) & (row["Longhorn cattle"] >= 69)&(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Aug 2017
    my_time = final_results.loc[final_results['Time'] == 151]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 119) & (row["Longhorn cattle"] >= 69)&(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Sept 2017
    my_time = final_results.loc[final_results['Time'] == 152]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 115) & (row["Longhorn cattle"] >= 65)& (row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Oct 2017
    my_time = final_results.loc[final_results['Time'] == 153]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63)&(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Nov 2017
    my_time = final_results.loc[final_results['Time'] == 154]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63)&(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Dec 2017
    my_time = final_results.loc[final_results['Time'] == 155]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63)&(row["Tamworth pigs"] <= 28) & (row["Tamworth pigs"] >= 8):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # January 2018
    my_time = final_results.loc[final_results['Time'] == 156]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63)&(row["Tamworth pigs"] <= 21) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # February 2018
    my_time = final_results.loc[final_results['Time'] == 157]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63)&(row["Tamworth pigs"] <= 26) & (row["Tamworth pigs"] >= 6):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
   

    # March 2018
    my_time = final_results.loc[final_results['Time'] == 158]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 10) & (row["Exmoor pony"] >= 8) & (row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63) &(row["Red deer"] <= 29) & (row["Red deer"] >= 19) &(row["Tamworth pigs"] <= 26) & (row["Tamworth pigs"] >= 6):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # April 2018
    my_time = final_results.loc[final_results['Time'] == 159]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 10) & (row["Exmoor pony"] >= 8) & (row["Longhorn cattle"] <= 126) & (row["Longhorn cattle"] >= 76) &(row["Tamworth pigs"] <= 26) & (row["Tamworth pigs"] >= 6):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # May 2018
    my_time = final_results.loc[final_results['Time'] == 160]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 10) & (row["Exmoor pony"] >= 8) &(row["Longhorn cattle"] <= 142) & (row["Longhorn cattle"] >= 92)&(row["Tamworth pigs"] <= 33) & (row["Tamworth pigs"] >= 13):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # June 2018
    my_time = final_results.loc[final_results['Time'] == 161]
    accepted_runs = []
    for index, row in my_time.iterrows(): 
        if (row["Exmoor pony"] <= 10) & (row["Exmoor pony"] >= 8) & (row["Longhorn cattle"] <= 128) & (row["Longhorn cattle"] >= 78)& (row["Tamworth pigs"] <= 33) & (row["Tamworth pigs"] >= 13):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # July 2018
    my_time = final_results.loc[final_results['Time'] == 162]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if  (row["Exmoor pony"] <= 10) & (row["Exmoor pony"] >= 8) &(row["Longhorn cattle"] <= 128) & (row["Longhorn cattle"] >= 78)&(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Aug 2018
    my_time = final_results.loc[final_results['Time'] == 163]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 127) & (row["Longhorn cattle"] >= 77) &(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Sept 2018
    my_time = final_results.loc[final_results['Time'] == 164]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 131) & (row["Longhorn cattle"] >= 81) & (row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Oct 2018
    my_time = final_results.loc[final_results['Time'] == 165]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 126) & (row["Longhorn cattle"] >= 76) & (row["Tamworth pigs"] <= 31) & (row["Tamworth pigs"] >= 11):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Nov 2018
    my_time = final_results.loc[final_results['Time'] == 166]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 118) & (row["Longhorn cattle"] >= 68) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Dec 2018
    my_time = final_results.loc[final_results['Time'] == 167]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 114) & (row["Longhorn cattle"] >= 64) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Jan 2019
    my_time = final_results.loc[final_results['Time'] == 168]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 114) & (row["Longhorn cattle"] >= 64) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Feb 2019
    my_time = final_results.loc[final_results['Time'] == 169]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) &(row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
  

    # March 2019
    my_time = final_results.loc[final_results['Time'] == 170]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Fallow deer"] <= 303) & (row["Fallow deer"] >= 253) &(row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) &(row["Red deer"] <= 42) & (row["Red deer"] >= 32) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # April 2019
    my_time = final_results.loc[final_results['Time'] == 171]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 126) & (row["Longhorn cattle"] >= 76) &(row["Tamworth pigs"] <= 18) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # May 2019
    my_time = final_results.loc[final_results['Time'] == 172]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 135) & (row["Longhorn cattle"] >= 85) & (row["Tamworth pigs"] <= 18) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # June 2019
    my_time = final_results.loc[final_results['Time'] == 173]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 114) & (row["Longhorn cattle"] >= 64) & (row["Tamworth pigs"] <= 18) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # July 2019
    my_time = final_results.loc[final_results['Time'] == 174]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 116) & (row["Longhorn cattle"] >= 66) &(row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Aug 2019
    my_time = final_results.loc[final_results['Time'] == 175]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 116) & (row["Longhorn cattle"] >= 66) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Sept 2019
    my_time = final_results.loc[final_results['Time'] == 176]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 118) & (row["Longhorn cattle"] >= 68) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Oct 2019
    my_time = final_results.loc[final_results['Time'] == 177]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63) &(row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Nov 2019
    my_time = final_results.loc[final_results['Time'] == 178]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Dec 2019
    my_time = final_results.loc[final_results['Time'] == 179]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 105) & (row["Longhorn cattle"] >= 55) & (row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
  
    # Jan 2020
   my_time = final_results.loc[final_results['Time'] == 180]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) &(row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
  
    accepted_Jan2020 = filtered_Dec2019[(filtered_Dec2019["Time"] == 180) &
    (filtered_Dec2019["Longhorn cattle"] <= 105) & (filtered_Dec2019["Longhorn cattle"] >= 55) &
    (filtered_Dec2019["Tamworth pigs"] <= 20) & (filtered_Dec2019["Tamworth pigs"] >= 1)]
    print("number passed Jan 2020 filters:", len(accepted_Jan2020))
    filtered_Jan2020 = filtered_Dec2019[filtered_Dec2019['run_number'].isin(accepted_Jan2020['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Feb2019.run_number.values): row["passed filters"] +=1 
    # Feb 2020
   my_time = final_results.loc[final_results['Time'] == 169]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) &(row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
  
    accepted_Feb2020 = filtered_Jan2020[(filtered_Jan2020["Time"] == 181) &
    (filtered_Jan2020["Longhorn cattle"] <= 104) & (filtered_Jan2020["Longhorn cattle"] >= 54) &
    (filtered_Jan2020["Tamworth pigs"] <= 18) & (filtered_Jan2020["Tamworth pigs"] >= 1)]
    print("number passed Feb 2020 filters:", len(accepted_Feb2020))
    filtered_Feb2020 = filtered_Jan2020[filtered_Jan2020['run_number'].isin(accepted_Feb2020['run_number'])]
    for index, row in final_results.iterrows():
        if row.run_number in (accepted_Feb2019.run_number.values): row["passed filters"] +=1 
    
    
    # March 2020
   my_time = final_results.loc[final_results['Time'] == 169]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) &(row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
  
    accepted_March2020 = filtered_Feb2020[(filtered_Feb2020["Time"] == 182) &
    (filtered_Feb2020["Fallow deer"] <= 272) & (filtered_Feb2020["Fallow deer"] >= 222) &
    (filtered_Feb2020["Red deer"] <= 40) & (filtered_Feb2020["Red deer"] >= 32) &
    (filtered_Feb2020["Longhorn cattle"] <= 106) & (filtered_Feb2020["Longhorn cattle"] >= 56)&
    (filtered_Feb2020["Tamworth pigs"] <= 17) & (filtered_Feb2020["Tamworth pigs"] >= 1)]
    print("number passed March 2020 filters:", len(accepted_March2020)) 
    filtered_March2020 = filtered_Feb2020[filtered_Feb2020['run_number'].isin(accepted_March2020['run_number'])]
    # April 2020
   my_time = final_results.loc[final_results['Time'] == 169]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) &(row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
  
    accepted_April2020 = filtered_March2020[(filtered_March2020["Time"] == 183) &
    (filtered_March2020["Exmoor pony"] <= 17) & (filtered_March2020["Exmoor pony"] >= 14) &
    (filtered_March2020["Longhorn cattle"] <= 106) & (filtered_March2020["Longhorn cattle"] >= 56) &
    (filtered_March2020["Tamworth pigs"] <= 17) & (filtered_March2020["Tamworth pigs"] >= 1)]
    print("number passed April 2020 filters:", len(accepted_April2020)) 
    filtered_April2020 = filtered_March2020[filtered_March2020['run_number'].isin(accepted_April2020['run_number'])]
    # May 2020
   my_time = final_results.loc[final_results['Time'] == 169]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) &(row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
  
    all_accepted_runs = filtered_preReintro[(filtered_preReintro["Time"] == 184) &
    (filtered_preReintro["Tamworth pigs"] <= 29) & (filtered_preReintro["Tamworth pigs"] >= 9) &
    (filtered_preReintro["Exmoor pony"] <= 17) & (filtered_preReintro["Exmoor pony"] >= 14) &
    (filtered_preReintro["Longhorn cattle"] <= 106) & (filtered_preReintro["Longhorn cattle"] >= 56) &
    (filtered_preReintro["Roe deer"] <= 80) & (filtered_preReintro["Roe deer"] >= 20) & 
    (filtered_preReintro["Grassland"] <= 69) & (filtered_preReintro["Grassland"] >= 49) & 
    (filtered_preReintro["Thorny Scrub"] <= 35) & (filtered_preReintro["Thorny Scrub"] >= 21) &
    (filtered_preReintro["Woodland"] <= 29) & (filtered_preReintro["Woodland"] >= 9)]

    print(final_results)

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

