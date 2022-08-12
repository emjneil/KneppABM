# ------ ABM of the Knepp Estate (2005-2046) --------
from KneppModel_ABM import KneppModel 
import numpy as np
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# # # # Run the model # # # # 


def run_all_models():
    
    print("now doing run 49")

    # define number of simulations
    number_simulations =  10000
    # make list of variables
    final_results_list = []
    final_parameters = []
    run_number = 0


    for _ in range(number_simulations):
        # keep track of the runs 
        run_number += 1
        print(run_number)
        # choose my percent above/below number
        perc_aboveBelow = 0.5

        # define the parameters
        chance_reproduceSapling = random.uniform(0.04206406-(0.04206406*perc_aboveBelow), 0.04206406+(0.04206406*perc_aboveBelow))
        chance_reproduceYoungScrub = random.uniform(0.1109531-(0.1109531*perc_aboveBelow), 0.1109531+(0.1109531*perc_aboveBelow))
        chance_regrowGrass = random.uniform(0.24463218-(0.24463218*perc_aboveBelow), 0.24463218+(0.24463218*perc_aboveBelow))
        chance_saplingBecomingTree = random.uniform(0.00289472-(0.00289472*perc_aboveBelow), 0.00289472+(0.00289472*perc_aboveBelow))
        chance_youngScrubMatures =random.uniform(0.00601638-(0.00601638*perc_aboveBelow), 0.00601638+(0.00601638*perc_aboveBelow))
        chance_scrubOutcompetedByTree = random.uniform(0.03450849-(0.03450849*perc_aboveBelow), 0.03450849+(0.03450849*perc_aboveBelow))
        chance_grassOutcompetedByTree = random.uniform(0.28874493-(0.28874493*perc_aboveBelow), 0.28874493+(0.28874493*perc_aboveBelow))
        chance_grassOutcompetedByScrub = random.uniform(0.29790348-(0.29790348*perc_aboveBelow), 0.29790348+(0.29790348*perc_aboveBelow))
        chance_saplingOutcompetedByTree = random.uniform(0.35425409-(0.35425409*perc_aboveBelow), 0.35425409+(0.35425409*perc_aboveBelow))
        chance_saplingOutcompetedByScrub = random.uniform(0.25885052-(0.25885052*perc_aboveBelow), 0.25885052+(0.25885052*perc_aboveBelow))
        chance_youngScrubOutcompetedByScrub =random.uniform(0.37929889-(0.37929889*perc_aboveBelow), 0.37929889+(0.37929889*perc_aboveBelow))
        chance_youngScrubOutcompetedByTree = random.uniform(0.3982258-(0.3982258*perc_aboveBelow), 0.3982258+(0.3982258*perc_aboveBelow))

        # initial values
        initial_roeDeer = 0.12
        initial_grassland = 0.8
        initial_woodland = 0.14
        initial_scrubland = 0.01

        # roe deer
        roeDeer_reproduce = random.uniform(0.18215313-(0.18215313*perc_aboveBelow), 0.18215313+(0.18215313*perc_aboveBelow))
        roeDeer_gain_from_grass = random.uniform(0.69330732-(0.69330732*perc_aboveBelow), 0.69330732+(0.69330732*perc_aboveBelow))
        roeDeer_gain_from_Trees =random.uniform(0.6982617-(0.6982617*perc_aboveBelow), 0.6982617+(0.6982617*perc_aboveBelow))
        roeDeer_gain_from_Scrub =random.uniform(0.46792347-(0.46792347*perc_aboveBelow), 0.46792347+(0.46792347*perc_aboveBelow))
        roeDeer_gain_from_Saplings = random.uniform(0.14360982-(0.14360982*perc_aboveBelow), 0.14360982+(0.14360982*perc_aboveBelow))
        roeDeer_gain_from_YoungScrub = random.uniform(0.10447744-(0.10447744*perc_aboveBelow), 0.10447744+(0.10447744*perc_aboveBelow))

        # Fallow deer
        fallowDeer_reproduce = random.uniform(0.28586154-(0.28586154*perc_aboveBelow), 0.28586154+(0.28586154*perc_aboveBelow))
        fallowDeer_gain_from_grass = random.uniform(0.60193723-(0.60193723*perc_aboveBelow), 0.60193723+(0.60193723*perc_aboveBelow))
        fallowDeer_gain_from_Trees = random.uniform(0.62907582-(0.62907582*perc_aboveBelow), 0.62907582+(0.62907582*perc_aboveBelow))
        fallowDeer_gain_from_Scrub = random.uniform(0.41669232-(0.41669232*perc_aboveBelow), 0.41669232+(0.41669232*perc_aboveBelow))
        fallowDeer_gain_from_Saplings = random.uniform(0.13022322-(0.13022322*perc_aboveBelow), 0.13022322+(0.13022322*perc_aboveBelow))
        fallowDeer_gain_from_YoungScrub = random.uniform(0.07403832-(0.07403832*perc_aboveBelow), 0.07403832+(0.07403832*perc_aboveBelow))
        # Red deer
        redDeer_reproduce = random.uniform(0.3065381-(0.3065381*perc_aboveBelow), 0.3065381+(0.3065381*perc_aboveBelow))
        redDeer_gain_from_grass = random.uniform(0.5464753-(0.5464753*perc_aboveBelow), 0.5464753+(0.5464753*perc_aboveBelow))
        redDeer_gain_from_Trees = random.uniform(0.57759807-(0.57759807*perc_aboveBelow), 0.57759807+(0.57759807*perc_aboveBelow))
        redDeer_gain_from_Scrub = random.uniform(0.39375145-(0.39375145*perc_aboveBelow), 0.39375145+(0.39375145*perc_aboveBelow))
        redDeer_gain_from_Saplings = random.uniform(0.11916663-(0.11916663*perc_aboveBelow), 0.11916663+(0.11916663*perc_aboveBelow))
        redDeer_gain_from_YoungScrub = random.uniform(0.06335441-(0.06335441*perc_aboveBelow), 0.06335441+(0.06335441*perc_aboveBelow))
        # Exmoor ponies
        ponies_gain_from_grass = random.uniform(0.46791793-(0.46791793*perc_aboveBelow), 0.46791793+(0.46791793*perc_aboveBelow))
        ponies_gain_from_Trees = random.uniform(0.50082365-(0.50082365*perc_aboveBelow), 0.50082365+(0.50082365*perc_aboveBelow)) 
        ponies_gain_from_Scrub = random.uniform(0.34385853-(0.34385853*perc_aboveBelow), 0.34385853+(0.34385853*perc_aboveBelow))
        ponies_gain_from_Saplings = random.uniform(0.10451826-(0.10451826*perc_aboveBelow), 0.10451826+(0.10451826*perc_aboveBelow))
        ponies_gain_from_YoungScrub = random.uniform(0.05673449-(0.05673449*perc_aboveBelow), 0.05673449+(0.05673449*perc_aboveBelow))
        # Longhorn cattle
        cows_reproduce = random.uniform(0.20204395-(0.20204395*perc_aboveBelow), 0.20204395+(0.20204395*perc_aboveBelow))
        cows_gain_from_grass = random.uniform(0.44058728-(0.44058728*perc_aboveBelow), 0.44058728+(0.44058728*perc_aboveBelow))
        cows_gain_from_Trees = random.uniform(0.45394087-(0.45394087*perc_aboveBelow), 0.45394087+(0.45394087*perc_aboveBelow))
        cows_gain_from_Scrub = random.uniform(0.2761602-(0.2761602*perc_aboveBelow), 0.2761602+(0.2761602*perc_aboveBelow))
        cows_gain_from_Saplings = random.uniform(0.08643107-(0.08643107*perc_aboveBelow), 0.08643107+(0.08643107*perc_aboveBelow))
        cows_gain_from_YoungScrub = random.uniform(0.04245426-(0.04245426*perc_aboveBelow), 0.04245426+(0.04245426*perc_aboveBelow))
        # Tamworth pigs
        pigs_reproduce = random.uniform(0.33496453-(0.33496453*perc_aboveBelow), 0.33496453+(0.33496453*perc_aboveBelow))
        pigs_gain_from_grass = random.uniform(0.39056552-(0.39056552*perc_aboveBelow), 0.39056552+(0.39056552*perc_aboveBelow))
        pigs_gain_from_Trees =random.uniform(0.6909069-(0.6909069*perc_aboveBelow), 0.6909069+(0.6909069*perc_aboveBelow))
        pigs_gain_from_Scrub = random.uniform(0.47493354-(0.47493354*perc_aboveBelow), 0.47493354+(0.47493354*perc_aboveBelow))
        pigs_gain_from_Saplings = random.uniform(0.07887992-(0.07887992*perc_aboveBelow), 0.07887992+(0.07887992*perc_aboveBelow))
        pigs_gain_from_YoungScrub = random.uniform(0.08125611-(0.08125611*perc_aboveBelow), 0.08125611+(0.08125611*perc_aboveBelow))
        
        # stocking values
        fallowDeer_stocking = 247
        cattle_stocking = 81
        redDeer_stocking = 35
        tamworthPig_stocking = 7
        exmoor_stocking = 15

        # euro bison parameters
        reproduce_bison = 0
        # bison should have higher impact than any other consumer
        bison_gain_from_grass =  0
        bison_gain_from_Trees =0
        bison_gain_from_Scrub =0
        bison_gain_from_Saplings = 0
        bison_gain_from_YoungScrub = 0  
        # euro elk parameters
        reproduce_elk = 0
        # bison should have higher impact than any other consumer
        elk_gain_from_grass =  0
        elk_gain_from_Trees = 0
        elk_gain_from_Scrub = 0
        elk_gain_from_Saplings =  0
        elk_gain_from_YoungScrub =  0
        # reindeer parameters
        reproduce_reindeer = 0
        # reindeer should have impacts between red and fallow deer
        reindeer_gain_from_grass = 0
        reindeer_gain_from_Trees =0
        reindeer_gain_from_Scrub =0
        reindeer_gain_from_Saplings = 0
        reindeer_gain_from_YoungScrub = 0
        # forecasting parameters
        fallowDeer_stocking_forecast = 247
        cattle_stocking_forecast = 81
        redDeer_stocking_forecast = 35
        tamworthPig_stocking_forecast = 7
        exmoor_stocking_forecast = 15
        reindeer_stocking_forecast = 0
        roeDeer_stocking_forecast = 0

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
        pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Trees, pigs_gain_from_Scrub, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, fallowDeer_stocking, cattle_stocking, redDeer_stocking, tamworthPig_stocking, exmoor_stocking,
        reproduce_bison, bison_gain_from_grass, bison_gain_from_Trees, bison_gain_from_Scrub, bison_gain_from_Saplings, bison_gain_from_YoungScrub,
        reproduce_elk, elk_gain_from_grass, elk_gain_from_Trees, elk_gain_from_Scrub, elk_gain_from_Saplings, elk_gain_from_YoungScrub,
        reproduce_reindeer, reindeer_gain_from_grass, reindeer_gain_from_Trees, reindeer_gain_from_Scrub, reindeer_gain_from_Saplings, reindeer_gain_from_YoungScrub,
        fallowDeer_stocking_forecast, cattle_stocking_forecast, redDeer_stocking_forecast, tamworthPig_stocking_forecast, exmoor_stocking_forecast, reindeer_stocking_forecast, roeDeer_stocking_forecast,
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
            fallowDeer_stocking, cattle_stocking, redDeer_stocking, tamworthPig_stocking, exmoor_stocking,
            reproduce_bison, bison_gain_from_grass, bison_gain_from_Trees, bison_gain_from_Scrub, bison_gain_from_Saplings, bison_gain_from_YoungScrub,
            reproduce_elk, elk_gain_from_grass, elk_gain_from_Trees, elk_gain_from_Scrub, elk_gain_from_Saplings, elk_gain_from_YoungScrub,
            reproduce_reindeer, reindeer_gain_from_grass, reindeer_gain_from_Trees, reindeer_gain_from_Scrub, reindeer_gain_from_Saplings, reindeer_gain_from_YoungScrub,
            fallowDeer_stocking_forecast, cattle_stocking_forecast, redDeer_stocking_forecast, tamworthPig_stocking_forecast, exmoor_stocking_forecast, reindeer_stocking_forecast, roeDeer_stocking_forecast,
            width = 25, height = 18, max_time = 184, reintroduction = True,
            introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False, cull_roe = False)

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
        "fallowDeer_stocking", "cattle_stocking", "redDeer_stocking", "tamworthPig_stocking", "exmoor_stocking",
        "reproduce_bison", "bison_gain_from_grass", "bison_gain_from_Trees", "bison_gain_from_Scrub", "bison_gain_from_Saplings", "bison_gain_from_YoungScrub",
        "reproduce_elk", "elk_gain_from_grass", "elk_gain_from_Trees", "elk_gain_from_Scrub", "elk_gain_from_Saplings", "elk_gain_from_YoungScrub",
        "reproduce_reindeer", "reindeer_gain_from_grass", "reindeer_gain_from_Trees", "reindeer_gain_from_Scrub", "reindeer_gain_from_Saplings", "reindeer_gain_from_YoungScrub",
        "fallowDeer_stocking_forecast", "cattle_stocking_forecast", "redDeer_stocking_forecast", "tamworthPig_stocking_forecast", "exmoor_stocking_forecast", "reindeer_stocking_forecast", "roeDeer_stocking_forecast",
        "run_number"]
    # check out the parameters used
    final_parameters = pd.DataFrame(data=final_parameters, columns=variables)

    # which filters were the most difficult to pass?
    difficult_filters = pd.DataFrame({
    'filter_number': np.arange(0,63),
    'times_passed': np.zeros(63)})

    # filter the runs and tag the dataframe; keep track of how many filters passed
    final_results["passed_filters"] = 0
    # pre-reintroduction model
    my_time = final_results.loc[final_results['Time'] == 50]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Roe deer"] <= 40) & (row["Roe deer"] >= 12) & (row["Grassland"] <= 80) & (row["Grassland"] >= 49) & (row["Woodland"] <= 27) & (row["Woodland"] >= 7) & (row["Thorny Scrub"] <= 21) & (row["Thorny Scrub"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[0,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    
    # April 2015
    my_time = final_results.loc[final_results['Time'] == 123]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Longhorn cattle"] <= 140) & (row["Longhorn cattle"] >= 90) & (row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[1,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # May 2015
    my_time = final_results.loc[final_results['Time'] == 124]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 154) & (row["Longhorn cattle"] >= 104) & (row["Tamworth pigs"] <= 24) & (row["Tamworth pigs"] >= 4) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[2,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # June 2015
    my_time = final_results.loc[final_results['Time'] == 125]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 154) & (row["Longhorn cattle"] >= 104) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 24) & (row["Tamworth pigs"] >= 4):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[3,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # July 2015
    my_time = final_results.loc[final_results['Time'] == 126]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 154) & (row["Longhorn cattle"] >= 104) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 24) & (row["Tamworth pigs"] >= 4):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[4,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Aug 2015
    my_time = final_results.loc[final_results['Time'] == 127]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 154) & (row["Longhorn cattle"] >= 104) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 24) & (row["Tamworth pigs"] >= 4):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[5,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Sept 2015
    my_time = final_results.loc[final_results['Time'] == 128]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 155) & (row["Longhorn cattle"] >= 105) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 24) & (row["Tamworth pigs"] >= 4):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[6,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Oct 2015
    my_time = final_results.loc[final_results['Time'] == 129]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 116) & (row["Longhorn cattle"] >= 66) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 24) & (row["Tamworth pigs"] >= 4):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[7,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Nov 2015
    my_time = final_results.loc[final_results['Time'] == 130]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 116) & (row["Longhorn cattle"] >= 66) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 23) & (row["Tamworth pigs"] >= 3):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[8,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Dec 2015
    my_time = final_results.loc[final_results['Time'] == 131]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 111) & (row["Longhorn cattle"] >= 61) &(row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Tamworth pigs"] <= 23) & (row["Tamworth pigs"] >= 3):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[9,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Jan 2016
    my_time = final_results.loc[final_results['Time'] == 132]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 111) & (row["Longhorn cattle"] >= 61) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[10,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Feb 2016
    my_time = final_results.loc[final_results['Time'] == 133]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Longhorn cattle"] <= 111) & (row["Longhorn cattle"] >= 61) &(row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[11,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # March 2016
    my_time = final_results.loc[final_results['Time'] == 134]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 111) & (row["Longhorn cattle"] >= 61) & (row["Fallow deer"] <= 190) & (row["Fallow deer"] >= 90) & (row["Red deer"] <= 31) & (row["Red deer"] >= 21) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[12,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # April 2016
    my_time = final_results.loc[final_results['Time'] == 135]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 128) & (row["Longhorn cattle"] >= 78) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[13,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # May 2016
    my_time = final_results.loc[final_results['Time'] == 136]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 133) & (row["Longhorn cattle"] >= 83) &(row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[14,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # June 2016
    my_time = final_results.loc[final_results['Time'] == 137]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 114) & (row["Longhorn cattle"] >= 64) & (row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[15,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # July 2016
    my_time = final_results.loc[final_results['Time'] == 138]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) & (row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[16,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Aug 2016
    my_time = final_results.loc[final_results['Time'] == 139]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) & (row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[17,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Sept 2016
    my_time = final_results.loc[final_results['Time'] == 140]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) &(row["Longhorn cattle"] <= 122) & (row["Longhorn cattle"] >= 72) & (row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[18,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Oct 2016
    my_time = final_results.loc[final_results['Time'] == 141]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 122) & (row["Longhorn cattle"] >= 72) & (row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[19,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Nov 2016
    my_time = final_results.loc[final_results['Time'] == 142]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) &(row["Longhorn cattle"] <= 117) & (row["Longhorn cattle"] >= 67) &(row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[20,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Dec 2016
    my_time = final_results.loc[final_results['Time'] == 143]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) &(row["Longhorn cattle"] <= 104) & (row["Longhorn cattle"] >= 54)& (row["Tamworth pigs"] <= 23) & (row["Tamworth pigs"] >= 3):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[21,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Jan 2017
    my_time = final_results.loc[final_results['Time'] == 144]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 104) & (row["Longhorn cattle"] >= 54) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[22,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Feb 2017
    my_time = final_results.loc[final_results['Time'] == 145]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 104) & (row["Longhorn cattle"] >= 54) & (row["Tamworth pigs"] <= 17) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[23,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 


    # March 2017
    my_time = final_results.loc[final_results['Time'] == 146]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Fallow deer"] <= 215) & (row["Fallow deer"] >= 115) &(row["Longhorn cattle"] <= 104) & (row["Longhorn cattle"] >= 54) &(row["Tamworth pigs"] <= 17) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[24,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # April 2017
    my_time = final_results.loc[final_results['Time'] == 147]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 125) & (row["Longhorn cattle"] >= 75) &(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[25,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # May 2017
    my_time = final_results.loc[final_results['Time'] == 148]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if  (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 134) & (row["Longhorn cattle"] >= 84) &(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[26,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # June 2017
    my_time = final_results.loc[final_results['Time'] == 149]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 119) & (row["Longhorn cattle"] >= 69) &(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[27,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # July 2017
    my_time = final_results.loc[final_results['Time'] == 150]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 119) & (row["Longhorn cattle"] >= 69)&(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[28,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Aug 2017
    my_time = final_results.loc[final_results['Time'] == 151]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 119) & (row["Longhorn cattle"] >= 69)&(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[29,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Sept 2017
    my_time = final_results.loc[final_results['Time'] == 152]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 115) & (row["Longhorn cattle"] >= 65)& (row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[30,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Oct 2017
    my_time = final_results.loc[final_results['Time'] == 153]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63)&(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[31,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Nov 2017
    my_time = final_results.loc[final_results['Time'] == 154]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63)&(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[32,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Dec 2017
    my_time = final_results.loc[final_results['Time'] == 155]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63)&(row["Tamworth pigs"] <= 28) & (row["Tamworth pigs"] >= 8):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[33,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # January 2018
    my_time = final_results.loc[final_results['Time'] == 156]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63)&(row["Tamworth pigs"] <= 21) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[34,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # February 2018
    my_time = final_results.loc[final_results['Time'] == 157]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63)&(row["Tamworth pigs"] <= 26) & (row["Tamworth pigs"] >= 6):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[35,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
   

    # March 2018
    my_time = final_results.loc[final_results['Time'] == 158]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 10) & (row["Exmoor pony"] >= 8) & (row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63) &(row["Red deer"] <= 29) & (row["Red deer"] >= 19) &(row["Tamworth pigs"] <= 26) & (row["Tamworth pigs"] >= 6):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[36,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # April 2018
    my_time = final_results.loc[final_results['Time'] == 159]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 10) & (row["Exmoor pony"] >= 8) & (row["Longhorn cattle"] <= 126) & (row["Longhorn cattle"] >= 76) &(row["Tamworth pigs"] <= 26) & (row["Tamworth pigs"] >= 6):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[37,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # May 2018
    my_time = final_results.loc[final_results['Time'] == 160]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 10) & (row["Exmoor pony"] >= 8) &(row["Longhorn cattle"] <= 142) & (row["Longhorn cattle"] >= 92)&(row["Tamworth pigs"] <= 33) & (row["Tamworth pigs"] >= 13):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[38,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # June 2018
    my_time = final_results.loc[final_results['Time'] == 161]
    accepted_runs = []
    for index, row in my_time.iterrows(): 
        if (row["Exmoor pony"] <= 10) & (row["Exmoor pony"] >= 8) & (row["Longhorn cattle"] <= 128) & (row["Longhorn cattle"] >= 78)& (row["Tamworth pigs"] <= 33) & (row["Tamworth pigs"] >= 13):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[39,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # July 2018
    my_time = final_results.loc[final_results['Time'] == 162]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if  (row["Exmoor pony"] <= 10) & (row["Exmoor pony"] >= 8) &(row["Longhorn cattle"] <= 128) & (row["Longhorn cattle"] >= 78)&(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[40,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Aug 2018
    my_time = final_results.loc[final_results['Time'] == 163]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 127) & (row["Longhorn cattle"] >= 77) &(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[41,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Sept 2018
    my_time = final_results.loc[final_results['Time'] == 164]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 131) & (row["Longhorn cattle"] >= 81) & (row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[42,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Oct 2018
    my_time = final_results.loc[final_results['Time'] == 165]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 126) & (row["Longhorn cattle"] >= 76) & (row["Tamworth pigs"] <= 31) & (row["Tamworth pigs"] >= 11):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[43,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Nov 2018
    my_time = final_results.loc[final_results['Time'] == 166]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 118) & (row["Longhorn cattle"] >= 68) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[44,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Dec 2018
    my_time = final_results.loc[final_results['Time'] == 167]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 114) & (row["Longhorn cattle"] >= 64) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[45,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Jan 2019
    my_time = final_results.loc[final_results['Time'] == 168]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 114) & (row["Longhorn cattle"] >= 64) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[46,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Feb 2019
    my_time = final_results.loc[final_results['Time'] == 169]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) &(row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[47,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
  

    # March 2019
    my_time = final_results.loc[final_results['Time'] == 170]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Fallow deer"] <= 303) & (row["Fallow deer"] >= 253) &(row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) &(row["Red deer"] <= 42) & (row["Red deer"] >= 32) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[48,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # April 2019
    my_time = final_results.loc[final_results['Time'] == 171]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 126) & (row["Longhorn cattle"] >= 76) &(row["Tamworth pigs"] <= 18) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[49,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # May 2019
    my_time = final_results.loc[final_results['Time'] == 172]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 135) & (row["Longhorn cattle"] >= 85) & (row["Tamworth pigs"] <= 18) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[50,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # June 2019
    my_time = final_results.loc[final_results['Time'] == 173]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 114) & (row["Longhorn cattle"] >= 64) & (row["Tamworth pigs"] <= 18) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[51,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # July 2019
    my_time = final_results.loc[final_results['Time'] == 174]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 116) & (row["Longhorn cattle"] >= 66) &(row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[52,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Aug 2019
    my_time = final_results.loc[final_results['Time'] == 175]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 116) & (row["Longhorn cattle"] >= 66) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[53,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Sept 2019
    my_time = final_results.loc[final_results['Time'] == 176]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 118) & (row["Longhorn cattle"] >= 68) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[54,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Oct 2019
    my_time = final_results.loc[final_results['Time'] == 177]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63) &(row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[55,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Nov 2019
    my_time = final_results.loc[final_results['Time'] == 178]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[56,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Dec 2019
    my_time = final_results.loc[final_results['Time'] == 179]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 105) & (row["Longhorn cattle"] >= 55) & (row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[57,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # Jan 2020
    my_time = final_results.loc[final_results['Time'] == 180]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 105) & (row["Longhorn cattle"] >= 55) & (row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[58,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
  
    # Feb 2020
    my_time = final_results.loc[final_results['Time'] == 181]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 104) & (row["Longhorn cattle"] >= 54) & (row["Tamworth pigs"] <= 18) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[59,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
  
    # March 2020
    my_time = final_results.loc[final_results['Time'] == 182]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Fallow deer"] <= 272) & (row["Fallow deer"] >= 222) & (row["Red deer"] <= 40) & (row["Red deer"] >= 32) &(row["Longhorn cattle"] <= 106) & (row["Longhorn cattle"] >= 56)&(row["Tamworth pigs"] <= 17) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[60,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # April 2020
    my_time = final_results.loc[final_results['Time'] == 183]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 17) & (row["Exmoor pony"] >= 14) &(row["Longhorn cattle"] <= 106) & (row["Longhorn cattle"] >= 56) &(row["Tamworth pigs"] <= 17) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[61,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # May 2020
    my_time = final_results.loc[final_results['Time'] == 184]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Tamworth pigs"] <= 29) & (row["Tamworth pigs"] >= 9) &(row["Exmoor pony"] <= 17) & (row["Exmoor pony"] >= 14) &(row["Longhorn cattle"] <= 106) & (row["Longhorn cattle"] >= 56) &(row["Roe deer"] <= 80) & (row["Roe deer"] >= 20) & (row["Grassland"] <= 69) & (row["Grassland"] >= 49) & (row["Thorny Scrub"] <= 35) & (row["Thorny Scrub"] >= 21) &(row["Woodland"] <= 29) & (row["Woodland"] >= 9):
            accepted_runs.append(row["run_number"])
            difficult_filters.loc[62,'times_passed'] += 1
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    

    difficult_filters.to_csv('difficult_filters_49.csv')
    # get the top 1% of results 
    last_year = final_results.loc[final_results['Time'] == 184] # pick one year to look at
    best_results = last_year.nlargest(100, 'passed_filters')
    # keep track of how many passed filters
    filters_passed_graph = best_results[["passed_filters"]]/63
    filters_passed_graph["perc"] = 50
    filters_passed_graph.to_excel('filters_passed_graph_49.xlsx')

    # accepted parameters
    accepted_parameters = final_parameters[final_parameters['run_number'].isin(best_results['run_number'])]
    # tag the accepted simulations
    final_results['accepted?'] = np.where(final_results['run_number'].isin(accepted_parameters['run_number']), 'Accepted', 'Rejected')
    final_results.to_csv('final_results_49.csv')

    # save to csv - all parameters
    final_parameters["accepted?"] = np.where(final_parameters['run_number'].isin(best_results['run_number']), 'Accepted', 'Rejected')
    final_parameters.to_csv('all_parameters_49.csv')
    accepted_parameters.to_csv('accepted_parameters_49.csv')

    return number_simulations, final_results, accepted_parameters

run_all_models()

