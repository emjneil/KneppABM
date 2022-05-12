# ------ ABM of the Knepp Estate (2005-2046) --------
from KneppModel_ABM import KneppModel 
import numpy as np
import random
import pandas as pd


# # # # Run the model # # # # 


def run_all_models():
    
    print("now doing 25%")

    # define number of simulations
    number_simulations =  100000
    # make list of variables
    final_results_list = []
    final_parameters = []
    run_number = 0


    for _ in range(number_simulations):
        # keep track of the runs 
        run_number += 1
        print(run_number)
        # choose my percent above/below number
        perc_aboveBelow = 0.25


        # define the parameters
        chance_reproduceSapling = random.uniform(0.10689392-(0.10689392*perc_aboveBelow), 0.10689392+(0.10689392*perc_aboveBelow))
        chance_reproduceYoungScrub = random.uniform(0.24015217-(0.24015217*perc_aboveBelow), 0.24015217+(0.24015217*perc_aboveBelow))
        chance_regrowGrass = random.uniform(0.30423892-(0.30423892*perc_aboveBelow), 0.30423892+(0.30423892*perc_aboveBelow))
        chance_saplingBecomingTree = random.uniform(0.00284643-(0.00284643*perc_aboveBelow), 0.00284643+(0.00284643*perc_aboveBelow))
        chance_youngScrubMatures =random.uniform(0.00573939-(0.00573939*perc_aboveBelow), 0.00573939+(0.00573939*perc_aboveBelow))
        chance_scrubOutcompetedByTree = random.uniform(0.02412406-(0.02412406*perc_aboveBelow), 0.02412406+(0.02412406*perc_aboveBelow))
        chance_grassOutcompetedByTree = random.uniform(0.94724942-(0.94724942*perc_aboveBelow), 0.94724942+(0.94724942*perc_aboveBelow))
        chance_grassOutcompetedByScrub = random.uniform(0.94365962-(0.94365962*perc_aboveBelow), 0.94365962+(0.94365962*perc_aboveBelow))
        chance_saplingOutcompetedByTree = random.uniform(0.90002424-(0.90002424*perc_aboveBelow), 0.90002424+(0.90002424*perc_aboveBelow))
        chance_saplingOutcompetedByScrub = random.uniform(0.89430521-(0.89430521*perc_aboveBelow), 0.89430521+(0.89430521*perc_aboveBelow))
        chance_youngScrubOutcompetedByScrub =random.uniform(0.90509186-(0.90509186*perc_aboveBelow), 0.90509186+(0.90509186*perc_aboveBelow))
        chance_youngScrubOutcompetedByTree = random.uniform(0.94722833-(0.94722833*perc_aboveBelow), 0.94722833+(0.94722833*perc_aboveBelow))

        # initial values
        initial_roeDeer = 0.12
        initial_grassland = 0.8
        initial_woodland = 0.14
        initial_scrubland = 0.01

        # roe deer
        roeDeer_reproduce = random.uniform(0.18203732-(0.18203732*perc_aboveBelow), 0.18203732+(0.18203732*perc_aboveBelow))
        roeDeer_gain_from_grass = random.uniform(0.85140101-(0.85140101*perc_aboveBelow), 0.85140101+(0.85140101*perc_aboveBelow))
        roeDeer_gain_from_Trees =random.uniform(0.55494915-(0.55494915*perc_aboveBelow), 0.55494915+(0.55494915*perc_aboveBelow))
        roeDeer_gain_from_Scrub =random.uniform(0.3150886-(0.3150886*perc_aboveBelow), 0.3150886+(0.3150886*perc_aboveBelow))
        roeDeer_gain_from_Saplings = random.uniform(0.17500993-(0.17500993*perc_aboveBelow), 0.17500993+(0.17500993*perc_aboveBelow))
        roeDeer_gain_from_YoungScrub = random.uniform(0.10840577-(0.10840577*perc_aboveBelow), 0.10840577+(0.10840577*perc_aboveBelow))

        # Fallow deer
        fallowDeer_reproduce = random.uniform(0.28541271-(0.28541271*perc_aboveBelow), 0.28541271+(0.28541271*perc_aboveBelow))
        fallowDeer_gain_from_grass = random.uniform(0.79704305-(0.79704305*perc_aboveBelow), 0.79704305+(0.79704305*perc_aboveBelow))
        fallowDeer_gain_from_Trees = random.uniform(0.53392473-(0.53392473*perc_aboveBelow), 0.53392473+(0.53392473*perc_aboveBelow))
        fallowDeer_gain_from_Scrub = random.uniform(0.24861395-(0.24861395*perc_aboveBelow), 0.24861395+(0.24861395*perc_aboveBelow))
        fallowDeer_gain_from_Saplings = random.uniform(0.1184058-(0.1184058*perc_aboveBelow), 0.1184058+(0.1184058*perc_aboveBelow))
        fallowDeer_gain_from_YoungScrub = random.uniform(0.07327595-(0.07327595*perc_aboveBelow), 0.07327595+(0.07327595*perc_aboveBelow))
        # Red deer
        redDeer_reproduce = random.uniform(0.30656575-(0.30656575*perc_aboveBelow), 0.30656575+(0.30656575*perc_aboveBelow))
        redDeer_gain_from_grass = random.uniform(0.74254951-(0.74254951*perc_aboveBelow), 0.74254951+(0.74254951*perc_aboveBelow))
        redDeer_gain_from_Trees = random.uniform(0.44633234-(0.44633234*perc_aboveBelow), 0.44633234+(0.44633234*perc_aboveBelow))
        redDeer_gain_from_Scrub = random.uniform(0.18817947-(0.18817947*perc_aboveBelow), 0.18817947+(0.18817947*perc_aboveBelow))
        redDeer_gain_from_Saplings = random.uniform(0.07572942-(0.07572942*perc_aboveBelow), 0.07572942+(0.07572942*perc_aboveBelow))
        redDeer_gain_from_YoungScrub = random.uniform(0.06516447-(0.06516447*perc_aboveBelow), 0.06516447+(0.06516447*perc_aboveBelow))
        # Exmoor ponies
        ponies_gain_from_grass = random.uniform(0.6766493-(0.6766493*perc_aboveBelow), 0.6766493+(0.6766493*perc_aboveBelow))
        ponies_gain_from_Trees = random.uniform(0.29251235-(0.29251235*perc_aboveBelow), 0.29251235+(0.29251235*perc_aboveBelow)) 
        ponies_gain_from_Scrub = random.uniform(0.14860288-(0.14860288*perc_aboveBelow), 0.14860288+(0.14860288*perc_aboveBelow))
        ponies_gain_from_Saplings = random.uniform(0.07-(0.07*perc_aboveBelow), 0.07+(0.07*perc_aboveBelow))
        ponies_gain_from_YoungScrub = random.uniform(0.03731702-(0.03731702*perc_aboveBelow), 0.03731702+(0.03731702*perc_aboveBelow))
        # Longhorn cattle
        cows_reproduce = random.uniform(0.18684058-(0.18684058*perc_aboveBelow), 0.18684058+(0.18684058*perc_aboveBelow))
        cows_gain_from_grass = random.uniform(0.60323306-(0.60323306*perc_aboveBelow), 0.60323306+(0.60323306*perc_aboveBelow))
        cows_gain_from_Trees = random.uniform(0.21599744-(0.21599744*perc_aboveBelow), 0.21599744+(0.21599744*perc_aboveBelow))
        cows_gain_from_Scrub = random.uniform(0.09316363-(0.09316363*perc_aboveBelow), 0.09316363+(0.09316363*perc_aboveBelow))
        cows_gain_from_Saplings = random.uniform(0.06101444-(0.06101444*perc_aboveBelow), 0.06101444+(0.06101444*perc_aboveBelow))
        cows_gain_from_YoungScrub = random.uniform(0.01609566-(0.01609566*perc_aboveBelow), 0.01609566+(0.01609566*perc_aboveBelow))
        # Tamworth pigs
        pigs_reproduce = random.uniform(0.24870944-(0.24870944*perc_aboveBelow), 0.24870944+(0.24870944*perc_aboveBelow))
        pigs_gain_from_grass = random.uniform(0.59825361-(0.59825361*perc_aboveBelow), 0.59825361+(0.59825361*perc_aboveBelow))
        pigs_gain_from_Trees =random.uniform(0.2569851-(0.2569851*perc_aboveBelow), 0.2569851+(0.2569851*perc_aboveBelow))
        pigs_gain_from_Scrub = random.uniform(0.1637277-(0.1637277*perc_aboveBelow), 0.1637277+(0.1637277*perc_aboveBelow))
        pigs_gain_from_Saplings = random.uniform(0.14782646-(0.14782646*perc_aboveBelow), 0.14782646+(0.14782646*perc_aboveBelow))
        pigs_gain_from_YoungScrub = random.uniform(0.09885063-(0.09885063*perc_aboveBelow), 0.09885063+(0.09885063*perc_aboveBelow))
        
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
            width = 25, height = 18, max_time = 184, reintroduction = True,
            introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)

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
        "run_number"]

    # check out the parameters used
    final_parameters = pd.DataFrame(data=final_parameters, columns=variables)


    # filter the runs and tag the dataframe; keep track of how many filters passed
    final_results["passed_filters"] = 0
    # pre-reintroduction model
    my_time = final_results.loc[final_results['Time'] == 50]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Roe deer"] <= 40) & (row["Roe deer"] >= 12) & (row["Grassland"] <= 80) & (row["Grassland"] >= 49) & (row["Woodland"] <= 27) & (row["Woodland"] >= 7) & (row["Thorny Scrub"] <= 21) & (row["Thorny Scrub"] >= 1):
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
        if (row["Longhorn cattle"] <= 105) & (row["Longhorn cattle"] >= 55) & (row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
  
    # Feb 2020
    my_time = final_results.loc[final_results['Time'] == 181]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Longhorn cattle"] <= 104) & (row["Longhorn cattle"] >= 54) & (row["Tamworth pigs"] <= 18) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
  
    # March 2020
    my_time = final_results.loc[final_results['Time'] == 182]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Fallow deer"] <= 272) & (row["Fallow deer"] >= 222) & (row["Red deer"] <= 40) & (row["Red deer"] >= 32) &(row["Longhorn cattle"] <= 106) & (row["Longhorn cattle"] >= 56)&(row["Tamworth pigs"] <= 17) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # April 2020
    my_time = final_results.loc[final_results['Time'] == 183]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Exmoor pony"] <= 17) & (row["Exmoor pony"] >= 14) &(row["Longhorn cattle"] <= 106) & (row["Longhorn cattle"] >= 56) &(row["Tamworth pigs"] <= 17) & (row["Tamworth pigs"] >= 1):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    # May 2020
    my_time = final_results.loc[final_results['Time'] == 184]
    accepted_runs = []
    for index, row in my_time.iterrows():
        if (row["Tamworth pigs"] <= 29) & (row["Tamworth pigs"] >= 9) &(row["Exmoor pony"] <= 17) & (row["Exmoor pony"] >= 14) &(row["Longhorn cattle"] <= 106) & (row["Longhorn cattle"] >= 56) &(row["Roe deer"] <= 80) & (row["Roe deer"] >= 20) & (row["Grassland"] <= 69) & (row["Grassland"] >= 49) & (row["Thorny Scrub"] <= 35) & (row["Thorny Scrub"] >= 21) &(row["Woodland"] <= 29) & (row["Woodland"] >= 9):
            accepted_runs.append(row["run_number"])
    final_results['passed_filters'] = np.where(final_results['run_number'].isin(accepted_runs),final_results['passed_filters']+1,final_results['passed_filters']) 
    

    # get the top 1% of results 
    last_year = final_results.loc[final_results['Time'] == 184] # pick one year to look at
    best_results = last_year.nlargest(1000, 'passed_filters')
    # keep track of how many passed filters
    filters_passed_graph = best_results[["passed_filters"]]/64
    filters_passed_graph["perc"] = 25
    # filters_passed_graph.to_excel('/Users/emilyneil/Desktop/KneppABM/outputs/one_perc/filters_passed_graph.xlsx')
    filters_passed_graph.to_excel('filters_passed_graph_25%.xlsx')

    # accepted parameters
    accepted_parameters = final_parameters[final_parameters['run_number'].isin(best_results['run_number'])]
    # tag the accepted simulations
    final_results['accepted?'] = np.where(final_results['run_number'].isin(accepted_parameters['run_number']), 'Accepted', 'Rejected')

    # save to csv - all parameters
    final_parameters["accepted?"] = np.where(final_parameters['run_number'].isin(best_results['run_number']), 'Accepted', 'Rejected')
    # final_parameters.to_csv('/Users/emilyneil/Desktop/KneppABM/outputs/one_perc/all_parameters.csv')
    final_parameters.to_csv('all_parameters_25%.csv')
    # and accepted parameters
    # accepted_parameters.to_csv('/Users/emilyneil/Desktop/KneppABM/outputs/one_perc/accepted_parameters.csv')
    # final_results.to_csv('/Users/emilyneil/Desktop/KneppABM/outputs/one_perc/final_results.csv')
    accepted_parameters.to_csv('accepted_parameters_25%.csv')
    final_results.to_csv('final_results_25%.csv')

    return number_simulations, final_results, accepted_parameters

