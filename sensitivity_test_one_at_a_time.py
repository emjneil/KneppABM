# graph the runs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from model import KneppModel 
import numpy as np
import pandas as pd
from scipy.stats import linregress
import random


def run_sensitivity():
    # define the parameters
    best_parameter = pd.read_csv('best_parameter_set.csv')

    chance_reproduceSapling = best_parameter["chance_reproduceSapling"].item()
    chance_reproduceYoungScrub =  best_parameter["chance_reproduceYoungScrub"].item()
    chance_regrowGrass =  best_parameter["chance_regrowGrass"].item()
    chance_saplingBecomingTree =  best_parameter["chance_saplingBecomingTree"].item()
    chance_youngScrubMatures =  best_parameter["chance_youngScrubMatures"].item()
    chance_scrubOutcompetedByTree =  best_parameter["chance_scrubOutcompetedByTree"].item()
    chance_grassOutcompetedByTree =  best_parameter["chance_grassOutcompetedByTree"].item()
    chance_grassOutcompetedByScrub = best_parameter["chance_grassOutcompetedByScrub"].item()

    initial_roe = 12
    fallowDeer_stocking = 247
    cattle_stocking = 81
    redDeer_stocking = 35
    tamworthPig_stocking = 7
    exmoor_stocking = 15

    roe_deer_reproduce = best_parameter["roe_deer_reproduce"].item()
    roe_deer_gain_from_grass =  best_parameter["roe_deer_gain_from_grass"].item()
    roe_deer_gain_from_trees =  best_parameter["roe_deer_gain_from_trees"].item()
    roe_deer_gain_from_scrub =  best_parameter["roe_deer_gain_from_scrub"].item()
    roe_deer_gain_from_saplings =  best_parameter["roe_deer_gain_from_saplings"].item()
    roe_deer_gain_from_young_scrub =  best_parameter["roe_deer_gain_from_young_scrub"].item()
    ponies_gain_from_grass =  best_parameter["ponies_gain_from_grass"].item()
    ponies_gain_from_trees =  best_parameter["ponies_gain_from_trees"].item()
    ponies_gain_from_scrub =  best_parameter["ponies_gain_from_scrub"].item()
    ponies_gain_from_saplings =  best_parameter["ponies_gain_from_saplings"].item()
    ponies_gain_from_young_scrub =  best_parameter["ponies_gain_from_young_scrub"].item()
    cattle_reproduce =  best_parameter["cattle_reproduce"].item()
    cows_gain_from_grass =  best_parameter["cows_gain_from_grass"].item()
    cows_gain_from_trees =  best_parameter["cows_gain_from_trees"].item()
    cows_gain_from_scrub =  best_parameter["cows_gain_from_scrub"].item()
    cows_gain_from_saplings =  best_parameter["cows_gain_from_saplings"].item()
    cows_gain_from_young_scrub =  best_parameter["cows_gain_from_young_scrub"].item()
    fallow_deer_reproduce =  best_parameter["fallow_deer_reproduce"].item()
    fallow_deer_gain_from_grass =  best_parameter["fallow_deer_gain_from_grass"].item()
    fallow_deer_gain_from_trees =  best_parameter["fallow_deer_gain_from_trees"].item()
    fallow_deer_gain_from_scrub =  best_parameter["fallow_deer_gain_from_scrub"].item()
    fallow_deer_gain_from_saplings =  best_parameter["fallow_deer_gain_from_saplings"].item()
    fallow_deer_gain_from_young_scrub =  best_parameter["fallow_deer_gain_from_young_scrub"].item()  
    red_deer_reproduce =  best_parameter["red_deer_reproduce"].item()
    red_deer_gain_from_grass =  best_parameter["red_deer_gain_from_grass"].item()
    red_deer_gain_from_trees =  best_parameter["red_deer_gain_from_trees"].item()
    red_deer_gain_from_scrub =  best_parameter["red_deer_gain_from_scrub"].item()
    red_deer_gain_from_saplings =  best_parameter["red_deer_gain_from_saplings"].item()
    red_deer_gain_from_young_scrub =  best_parameter["red_deer_gain_from_young_scrub"].item()
    tamworth_pig_reproduce =  best_parameter["tamworth_pig_reproduce"].item()
    tamworth_pig_gain_from_grass =  best_parameter["tamworth_pig_gain_from_grass"].item()
    tamworth_pig_gain_from_trees = best_parameter["tamworth_pig_gain_from_trees"].item()
    tamworth_pig_gain_from_scrub = best_parameter["tamworth_pig_gain_from_scrub"].item()
    tamworth_pig_gain_from_saplings =  best_parameter["tamworth_pig_gain_from_saplings"].item()
    tamworth_pig_gain_from_young_scrub =  best_parameter["tamworth_pig_gain_from_young_scrub"].item()


    # euro bison parameters
    european_bison_reproduce = random.uniform(cattle_reproduce-(cattle_reproduce*0.1), cattle_reproduce+(cattle_reproduce*0.1))
    # bison should have higher impact than any other consumer
    european_bison_gain_from_grass = random.uniform(cows_gain_from_grass, cows_gain_from_grass+(cows_gain_from_grass*0.1))
    european_bison_gain_from_trees =random.uniform(cows_gain_from_trees, cows_gain_from_trees+(cows_gain_from_trees*0.1))
    european_bison_gain_from_scrub =random.uniform(cows_gain_from_scrub, cows_gain_from_scrub+(cows_gain_from_scrub*0.1))
    european_bison_gain_from_saplings = random.uniform(cows_gain_from_saplings, cows_gain_from_saplings+(cows_gain_from_saplings*0.1))
    european_bison_gain_from_young_scrub = random.uniform(cows_gain_from_young_scrub, cows_gain_from_young_scrub+(cows_gain_from_young_scrub*0.1))
    # euro elk parameters
    european_elk_reproduce = random.uniform(red_deer_reproduce-(red_deer_reproduce*0.1), red_deer_reproduce+(red_deer_reproduce*0.1))
    # bison should have higher impact than any other consumer
    european_elk_gain_from_grass =  random.uniform(red_deer_gain_from_grass-(red_deer_gain_from_grass*0.1), red_deer_gain_from_grass)
    european_elk_gain_from_trees = random.uniform(red_deer_gain_from_trees-(red_deer_gain_from_trees*0.1), red_deer_gain_from_trees)
    european_elk_gain_from_scrub = random.uniform(red_deer_gain_from_scrub-(red_deer_gain_from_scrub*0.1), red_deer_gain_from_scrub)
    european_elk_gain_from_saplings =  random.uniform(red_deer_gain_from_saplings-(red_deer_gain_from_saplings*0.1), red_deer_gain_from_saplings)
    european_elk_gain_from_young_scrub =  random.uniform(red_deer_gain_from_young_scrub-(red_deer_gain_from_young_scrub*0.1), red_deer_gain_from_young_scrub)

    # reindeer parameters
    reindeer_reproduce = 0
    # reindeer should have impacts between red and fallow deer
    reindeer_gain_from_grass = 0
    reindeer_gain_from_trees =0
    reindeer_gain_from_scrub =0
    reindeer_gain_from_saplings = 0
    reindeer_gain_from_young_scrub = 0
    # forecasting parameters
    fallowDeer_stocking_forecast = 247
    cattle_stocking_forecast = 81
    redDeer_stocking_forecast = 35
    tamworthPig_stocking_forecast = 7
    exmoor_stocking_forecast = 15
    introduced_species_stocking_forecast = 0
    chance_scrub_saves_saplings = best_parameter["chance_scrub_saves_saplings"].item()


    final_parameters = [
                chance_youngScrubMatures, chance_saplingBecomingTree, chance_reproduceSapling,chance_reproduceYoungScrub, chance_regrowGrass, 
                chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_scrubOutcompetedByTree,  
                roe_deer_reproduce, roe_deer_gain_from_saplings, roe_deer_gain_from_trees, roe_deer_gain_from_scrub, roe_deer_gain_from_young_scrub, roe_deer_gain_from_grass,
                ponies_gain_from_saplings, ponies_gain_from_trees, ponies_gain_from_scrub, ponies_gain_from_young_scrub, ponies_gain_from_grass, 
                cattle_reproduce, cows_gain_from_grass, cows_gain_from_trees, cows_gain_from_scrub, cows_gain_from_saplings, cows_gain_from_young_scrub, 
                fallow_deer_reproduce, fallow_deer_gain_from_saplings, fallow_deer_gain_from_trees, fallow_deer_gain_from_scrub, fallow_deer_gain_from_young_scrub, fallow_deer_gain_from_grass,
                red_deer_reproduce, red_deer_gain_from_saplings, red_deer_gain_from_trees, red_deer_gain_from_scrub, red_deer_gain_from_young_scrub, red_deer_gain_from_grass,
                tamworth_pig_reproduce, tamworth_pig_gain_from_saplings,tamworth_pig_gain_from_trees,tamworth_pig_gain_from_scrub,tamworth_pig_gain_from_young_scrub,tamworth_pig_gain_from_grass,
                chance_scrub_saves_saplings]

    variables = [
        # habitat variables
        "chance_youngScrubMatures",
        "chance_saplingBecomingTree",
        "chance_reproduceSapling", # this is to initialize the initial dominant condition
        "chance_reproduceYoungScrub",  # this is to initialize the initial dominant condition
        "chance_regrowGrass", # this is to initialize the initial dominant condition
        "chance_grassOutcompetedByTree",
        "chance_grassOutcompetedByScrub",
        "chance_scrubOutcompetedByTree", # if tree matures, chance of scrub decreasing
        # roe deer variables
        "roe_deer_reproduce",
        "roe_deer_gain_from_saplings",
        "roe_deer_gain_from_trees",
        "roe_deer_gain_from_scrub",
        "roe_deer_gain_from_young_scrub", 
        "roe_deer_gain_from_grass", 
        # Exmoor pony variables
        "ponies_gain_from_saplings", 
        "ponies_gain_from_trees", 
        "ponies_gain_from_scrub", 
        "ponies_gain_from_young_scrub", 
        "ponies_gain_from_grass", 
        # Cow variables
        "cattle_reproduce", 
        "cows_gain_from_grass", 
        "cows_gain_from_trees", 
        "cows_gain_from_scrub", 
        "cows_gain_from_saplings", 
        "cows_gain_from_young_scrub", 
        # Fallow deer variables
        "fallow_deer_reproduce", 
        "fallow_deer_gain_from_saplings", 
        "fallow_deer_gain_from_trees", 
        "fallow_deer_gain_from_scrub", 
        "fallow_deer_gain_from_young_scrub", 
        "fallow_deer_gain_from_grass", 
        # Red deer variables
        "red_deer_reproduce", 
        "red_deer_gain_from_saplings", 
        "red_deer_gain_from_trees", 
        "red_deer_gain_from_scrub", 
        "red_deer_gain_from_young_scrub", 
        "red_deer_gain_from_grass", 
        # Pig variables
        "tamworth_pig_reproduce", 
        "tamworth_pig_gain_from_saplings", 
        "tamworth_pig_gain_from_trees", 
        "tamworth_pig_gain_from_scrub",
        "tamworth_pig_gain_from_young_scrub", 
        "tamworth_pig_gain_from_grass",
        # last one
        "chance_scrub_saves_saplings"
        ]


    # check out the parameters used
    final_parameters = pd.DataFrame(data=[final_parameters], columns=variables)

    # SENSITIVITY TEST
    sensitivity_results_list = []
    parameter_names = []
    perc_numbers = []


    run_number  = 0
    # choose my percent above/below number
    # perc_aboveBelow = [-0.1, -0.05,-0.01, 0, 0.01, 0.05, 0.1]    
    perc_aboveBelow = [-0.1, 0.1]

    final_parameters = final_parameters.iloc[0,0:45]

    # loop through each one, changing one cell at a time
    for param_name, df_row in final_parameters.iteritems():
        for perc_number in perc_aboveBelow:
            final_parameters_temp = final_parameters
            run_number += 1
            ifor_val = df_row + (df_row*perc_number)
            final_parameters_temp.at[param_name] = ifor_val

            print(run_number)

            # choose my parameters 
            chance_youngScrubMatures = final_parameters_temp["chance_youngScrubMatures"]
            chance_saplingBecomingTree = final_parameters_temp["chance_saplingBecomingTree"]
            chance_reproduceSapling = final_parameters_temp["chance_reproduceSapling"]
            chance_reproduceYoungScrub = final_parameters_temp["chance_reproduceYoungScrub"]
            chance_regrowGrass = final_parameters_temp["chance_regrowGrass"]
            chance_grassOutcompetedByTree = final_parameters_temp["chance_grassOutcompetedByTree"]
            chance_grassOutcompetedByScrub = final_parameters_temp["chance_grassOutcompetedByScrub"]
            chance_scrubOutcompetedByTree = final_parameters_temp["chance_scrubOutcompetedByTree"]

            initial_roe = 12
            fallowDeer_stocking = 247
            cattle_stocking = 81
            redDeer_stocking = 35
            tamworthPig_stocking = 7
            exmoor_stocking = 15

            roe_deer_reproduce = final_parameters_temp["roe_deer_reproduce"]
            roe_deer_gain_from_saplings = final_parameters_temp["roe_deer_gain_from_saplings"]
            roe_deer_gain_from_trees = final_parameters_temp["roe_deer_gain_from_trees"]
            roe_deer_gain_from_scrub = final_parameters_temp["roe_deer_gain_from_scrub"]
            roe_deer_gain_from_young_scrub = final_parameters_temp["roe_deer_gain_from_young_scrub"]
            roe_deer_gain_from_grass = final_parameters_temp["roe_deer_gain_from_grass"]
            ponies_gain_from_saplings = final_parameters_temp["ponies_gain_from_saplings"]
            ponies_gain_from_trees = final_parameters_temp["ponies_gain_from_trees"]
            ponies_gain_from_scrub = final_parameters_temp["ponies_gain_from_scrub"]
            ponies_gain_from_young_scrub = final_parameters_temp["ponies_gain_from_young_scrub"]
            ponies_gain_from_grass = final_parameters_temp["ponies_gain_from_grass"]
            cattle_reproduce = final_parameters_temp["cattle_reproduce"]
            cows_gain_from_grass = final_parameters_temp["cows_gain_from_grass"]
            cows_gain_from_trees = final_parameters_temp["cows_gain_from_trees"]
            cows_gain_from_scrub = final_parameters_temp["cows_gain_from_scrub"]
            cows_gain_from_saplings = final_parameters_temp["cows_gain_from_saplings"]
            cows_gain_from_young_scrub = final_parameters_temp["cows_gain_from_young_scrub"]
            fallow_deer_reproduce = final_parameters_temp["fallow_deer_reproduce"]
            fallow_deer_gain_from_saplings = final_parameters_temp["fallow_deer_gain_from_saplings"]
            fallow_deer_gain_from_trees = final_parameters_temp["fallow_deer_gain_from_trees"]
            fallow_deer_gain_from_scrub = final_parameters_temp["fallow_deer_gain_from_scrub"]
            fallow_deer_gain_from_young_scrub = final_parameters_temp["fallow_deer_gain_from_young_scrub"]
            fallow_deer_gain_from_grass = final_parameters_temp["fallow_deer_gain_from_grass"]
            red_deer_reproduce = final_parameters_temp["red_deer_reproduce"]
            red_deer_gain_from_saplings = final_parameters_temp["red_deer_gain_from_saplings"]
            red_deer_gain_from_trees = final_parameters_temp["red_deer_gain_from_trees"]
            red_deer_gain_from_scrub = final_parameters_temp["red_deer_gain_from_scrub"]
            red_deer_gain_from_young_scrub = final_parameters_temp["red_deer_gain_from_young_scrub"]
            red_deer_gain_from_grass = final_parameters_temp["red_deer_gain_from_grass"]
            tamworth_pig_reproduce = final_parameters_temp["tamworth_pig_reproduce"]
            tamworth_pig_gain_from_saplings = final_parameters_temp["tamworth_pig_gain_from_saplings"]
            tamworth_pig_gain_from_trees = final_parameters_temp["tamworth_pig_gain_from_trees"]
            tamworth_pig_gain_from_scrub = final_parameters_temp["tamworth_pig_gain_from_scrub"]
            tamworth_pig_gain_from_young_scrub = final_parameters_temp["tamworth_pig_gain_from_young_scrub"]
            tamworth_pig_gain_from_grass = final_parameters_temp["tamworth_pig_gain_from_grass"]
            chance_scrub_saves_saplings = final_parameters_temp["chance_scrub_saves_saplings"]

            # euro bison parameters
            european_bison_reproduce = 0
            # bison should have higher impact than any other consumer
            european_bison_gain_from_grass = 0
            european_bison_gain_from_trees = 0
            european_bison_gain_from_scrub = 0
            european_bison_gain_from_saplings = 0
            european_bison_gain_from_young_scrub = 0
            # euro elk parameters
            european_elk_reproduce = 0
            # bison should have higher impact than any other consumer
            european_elk_gain_from_grass = 0
            european_elk_gain_from_trees = 0
            european_elk_gain_from_scrub = 0
            european_elk_gain_from_saplings =  0
            european_elk_gain_from_young_scrub =  0

            # reindeer parameters
            reindeer_reproduce = 0
            # reindeer should have impacts between red and fallow deer
            reindeer_gain_from_grass = 0
            reindeer_gain_from_trees =0
            reindeer_gain_from_scrub =0
            reindeer_gain_from_saplings = 0
            reindeer_gain_from_young_scrub = 0
            # forecasting parameters
            fallowDeer_stocking_forecast = 247
            cattle_stocking_forecast = 81
            redDeer_stocking_forecast = 35
            tamworthPig_stocking_forecast = 7
            exmoor_stocking_forecast = 15
            introduced_species_stocking_forecast = 0

            random.seed(1)
            np.random.seed(1)

            model = KneppModel(initial_roe, roe_deer_reproduce, roe_deer_gain_from_saplings, roe_deer_gain_from_trees, roe_deer_gain_from_scrub, roe_deer_gain_from_young_scrub, roe_deer_gain_from_grass,
                                chance_youngScrubMatures, chance_saplingBecomingTree, chance_reproduceSapling,chance_reproduceYoungScrub, chance_regrowGrass, 
                                chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_scrubOutcompetedByTree, 
                                ponies_gain_from_saplings, ponies_gain_from_trees, ponies_gain_from_scrub, ponies_gain_from_young_scrub, ponies_gain_from_grass, 
                                cattle_reproduce, cows_gain_from_grass, cows_gain_from_trees, cows_gain_from_scrub, cows_gain_from_saplings, cows_gain_from_young_scrub, 
                                fallow_deer_reproduce, fallow_deer_gain_from_saplings, fallow_deer_gain_from_trees, fallow_deer_gain_from_scrub, fallow_deer_gain_from_young_scrub, fallow_deer_gain_from_grass,
                                red_deer_reproduce, red_deer_gain_from_saplings, red_deer_gain_from_trees, red_deer_gain_from_scrub, red_deer_gain_from_young_scrub, red_deer_gain_from_grass,
                                tamworth_pig_reproduce, tamworth_pig_gain_from_saplings,tamworth_pig_gain_from_trees,tamworth_pig_gain_from_scrub,tamworth_pig_gain_from_young_scrub,tamworth_pig_gain_from_grass,
                                european_bison_reproduce, european_bison_gain_from_grass, european_bison_gain_from_trees, european_bison_gain_from_scrub, european_bison_gain_from_saplings, european_bison_gain_from_young_scrub,
                                european_elk_reproduce, european_elk_gain_from_grass, european_elk_gain_from_trees, european_elk_gain_from_scrub, european_elk_gain_from_saplings, european_elk_gain_from_young_scrub,
                                reindeer_reproduce, reindeer_gain_from_grass, reindeer_gain_from_trees, reindeer_gain_from_scrub, reindeer_gain_from_saplings, reindeer_gain_from_young_scrub,
                                fallowDeer_stocking, cattle_stocking, redDeer_stocking, tamworthPig_stocking, exmoor_stocking,
                                fallowDeer_stocking_forecast, cattle_stocking_forecast, redDeer_stocking_forecast, tamworthPig_stocking_forecast, exmoor_stocking_forecast, introduced_species_stocking_forecast,
                                chance_scrub_saves_saplings,
                                max_time = 185, reintroduction = True, introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)


            model.reset_randomizer(seed=1)

            model.run_model()

            # remember the results of the model 
            final_results = model.datacollector.get_model_vars_dataframe()

            # how many filters were passed? 
            passed_filters = 0
            # pre-reintroduction model
            my_time = final_results.loc[final_results['Time'] == 49]

            for index, row in my_time.iterrows():
                if (row["Roe deer"] <= 40) & (row["Roe deer"] >= 12) & (row["Grassland"] <= 80) & (row["Grassland"] >= 20) & (row["Woodland"] <= 17) & (row["Woodland"] >= 5.8) & (row["Thorny Scrub"] <= 51.8) & (row["Thorny Scrub"] >= 4.3):
                    passed_filters+=1
            # April 2015
            my_time = final_results.loc[final_results['Time'] == 122]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Longhorn cattle"] <= 140) & (row["Longhorn cattle"] >= 90) & (row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
                    passed_filters+=1
            # May 2015
            my_time = final_results.loc[final_results['Time'] == 123]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 154) & (row["Longhorn cattle"] >= 104) & (row["Tamworth pigs"] <= 24) & (row["Tamworth pigs"] >= 4) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9):
                    passed_filters+=1
            # June 2015
            my_time = final_results.loc[final_results['Time'] == 124]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 154) & (row["Longhorn cattle"] >= 104) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 24) & (row["Tamworth pigs"] >= 4):
                    passed_filters+=1
            # July 2015
            my_time = final_results.loc[final_results['Time'] == 125]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 154) & (row["Longhorn cattle"] >= 104) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 24) & (row["Tamworth pigs"] >= 4):
                    passed_filters+=1
            # Aug 2015
            my_time = final_results.loc[final_results['Time'] == 126]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 154) & (row["Longhorn cattle"] >= 104) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 24) & (row["Tamworth pigs"] >= 4):
                    passed_filters+=1
            # Sept 2015
            my_time = final_results.loc[final_results['Time'] == 127]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 155) & (row["Longhorn cattle"] >= 105) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 24) & (row["Tamworth pigs"] >= 4):
                    passed_filters+=1
            # Oct 2015
            my_time = final_results.loc[final_results['Time'] == 128]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 116) & (row["Longhorn cattle"] >= 66) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 24) & (row["Tamworth pigs"] >= 4):
                    passed_filters+=1
            # Nov 2015
            my_time = final_results.loc[final_results['Time'] == 129]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 116) & (row["Longhorn cattle"] >= 66) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 23) & (row["Tamworth pigs"] >= 3):
                    passed_filters+=1
            # Dec 2015
            my_time = final_results.loc[final_results['Time'] == 130]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 111) & (row["Longhorn cattle"] >= 61) &(row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Tamworth pigs"] <= 23) & (row["Tamworth pigs"] >= 3):
                    passed_filters+=1
            # Jan 2016
            my_time = final_results.loc[final_results['Time'] == 131]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 111) & (row["Longhorn cattle"] >= 61) & (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # Feb 2016
            my_time = final_results.loc[final_results['Time'] == 132]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Longhorn cattle"] <= 111) & (row["Longhorn cattle"] >= 61) &(row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # March 2016
            my_time = final_results.loc[final_results['Time'] == 133]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 111) & (row["Longhorn cattle"] >= 61) & (row["Fallow deer"] <= 190) & (row["Fallow deer"] >= 90) & (row["Red deer"] <= 31) & (row["Red deer"] >= 21) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # April 2016
            my_time = final_results.loc[final_results['Time'] == 134]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 128) & (row["Longhorn cattle"] >= 78) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # May 2016
            my_time = final_results.loc[final_results['Time'] == 135]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 133) & (row["Longhorn cattle"] >= 83) &(row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
                    passed_filters+=1
            # June 2016
            my_time = final_results.loc[final_results['Time'] == 136]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 114) & (row["Longhorn cattle"] >= 64) & (row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
                    passed_filters+=1
            # July 2016
            my_time = final_results.loc[final_results['Time'] == 137]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) & (row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
                    passed_filters+=1
            # Aug 2016
            my_time = final_results.loc[final_results['Time'] == 138]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) & (row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
                    passed_filters+=1
            # Sept 2016
            my_time = final_results.loc[final_results['Time'] == 139]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) &(row["Longhorn cattle"] <= 122) & (row["Longhorn cattle"] >= 72) & (row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
                    passed_filters+=1
            # Oct 2016
            my_time = final_results.loc[final_results['Time'] == 140]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 122) & (row["Longhorn cattle"] >= 72) & (row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
                    passed_filters+=1
            # Nov 2016
            my_time = final_results.loc[final_results['Time'] == 141]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) &(row["Longhorn cattle"] <= 117) & (row["Longhorn cattle"] >= 67) &(row["Tamworth pigs"] <= 27) & (row["Tamworth pigs"] >= 7):
                    passed_filters+=1
            # Dec 2016
            my_time = final_results.loc[final_results['Time'] == 142]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) &(row["Longhorn cattle"] <= 104) & (row["Longhorn cattle"] >= 54)& (row["Tamworth pigs"] <= 23) & (row["Tamworth pigs"] >= 3):
                    passed_filters+=1
            # Jan 2017
            my_time = final_results.loc[final_results['Time'] == 143]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 104) & (row["Longhorn cattle"] >= 54) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # Feb 2017
            my_time = final_results.loc[final_results['Time'] == 144]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 12) & (row["Exmoor pony"] >= 10) & (row["Longhorn cattle"] <= 104) & (row["Longhorn cattle"] >= 54) & (row["Tamworth pigs"] <= 17) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # March 2017
            my_time = final_results.loc[final_results['Time'] == 145]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) & (row["Fallow deer"] <= 215) & (row["Fallow deer"] >= 115) &(row["Longhorn cattle"] <= 104) & (row["Longhorn cattle"] >= 54) &(row["Tamworth pigs"] <= 17) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # April 2017
            my_time = final_results.loc[final_results['Time'] == 146]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 125) & (row["Longhorn cattle"] >= 75) &(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
                    passed_filters+=1
            # May 2017
            my_time = final_results.loc[final_results['Time'] == 147]
            for index, row in my_time.iterrows():
                if  (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 134) & (row["Longhorn cattle"] >= 84) &(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
                    passed_filters+=1
            # June 2017
            my_time = final_results.loc[final_results['Time'] == 148]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 119) & (row["Longhorn cattle"] >= 69) &(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
                    passed_filters+=1
            # July 2017
            my_time = final_results.loc[final_results['Time'] == 149]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 119) & (row["Longhorn cattle"] >= 69)&(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
                    passed_filters+=1
            # Aug 2017
            my_time = final_results.loc[final_results['Time'] == 150]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 119) & (row["Longhorn cattle"] >= 69)&(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
                    passed_filters+=1
            # Sept 2017
            my_time = final_results.loc[final_results['Time'] == 151]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 115) & (row["Longhorn cattle"] >= 65)& (row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
                    passed_filters+=1
            # Oct 2017
            my_time = final_results.loc[final_results['Time'] == 152]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63)&(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
                    passed_filters+=1
            # Nov 2017
            my_time = final_results.loc[final_results['Time'] == 153]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63)&(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
                    passed_filters+=1
            # Dec 2017
            my_time = final_results.loc[final_results['Time'] == 154]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63)&(row["Tamworth pigs"] <= 28) & (row["Tamworth pigs"] >= 8):
                    passed_filters+=1
            # January 2018
            my_time = final_results.loc[final_results['Time'] == 155]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63)&(row["Tamworth pigs"] <= 21) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # February 2018
            my_time = final_results.loc[final_results['Time'] == 156]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 11) & (row["Exmoor pony"] >= 9) &(row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63)&(row["Tamworth pigs"] <= 26) & (row["Tamworth pigs"] >= 6):
                    passed_filters+=1
            # March 2018
            my_time = final_results.loc[final_results['Time'] == 157]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 10) & (row["Exmoor pony"] >= 8) & (row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63) &(row["Red deer"] <= 29) & (row["Red deer"] >= 19) &(row["Tamworth pigs"] <= 26) & (row["Tamworth pigs"] >= 6):
                    passed_filters+=1
            # April 2018
            my_time = final_results.loc[final_results['Time'] == 158]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 10) & (row["Exmoor pony"] >= 8) & (row["Longhorn cattle"] <= 126) & (row["Longhorn cattle"] >= 76) &(row["Tamworth pigs"] <= 26) & (row["Tamworth pigs"] >= 6):
                    passed_filters+=1
            # May 2018
            my_time = final_results.loc[final_results['Time'] == 159]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 10) & (row["Exmoor pony"] >= 8) &(row["Longhorn cattle"] <= 142) & (row["Longhorn cattle"] >= 92)&(row["Tamworth pigs"] <= 33) & (row["Tamworth pigs"] >= 13):
                    passed_filters+=1
            # June 2018
            my_time = final_results.loc[final_results['Time'] == 160]
            for index, row in my_time.iterrows(): 
                if (row["Exmoor pony"] <= 10) & (row["Exmoor pony"] >= 8) & (row["Longhorn cattle"] <= 128) & (row["Longhorn cattle"] >= 78)& (row["Tamworth pigs"] <= 33) & (row["Tamworth pigs"] >= 13):
                    passed_filters+=1
            # July 2018
            my_time = final_results.loc[final_results['Time'] == 161]
            for index, row in my_time.iterrows():
                if  (row["Exmoor pony"] <= 10) & (row["Exmoor pony"] >= 8) &(row["Longhorn cattle"] <= 128) & (row["Longhorn cattle"] >= 78)&(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
                    passed_filters+=1
            # Aug 2018
            my_time = final_results.loc[final_results['Time'] == 162]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 127) & (row["Longhorn cattle"] >= 77) &(row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
                    passed_filters+=1
            # Sept 2018
            my_time = final_results.loc[final_results['Time'] == 163]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 131) & (row["Longhorn cattle"] >= 81) & (row["Tamworth pigs"] <= 32) & (row["Tamworth pigs"] >= 12):
                    passed_filters+=1
            # Oct 2018
            my_time = final_results.loc[final_results['Time'] == 164]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 126) & (row["Longhorn cattle"] >= 76) & (row["Tamworth pigs"] <= 31) & (row["Tamworth pigs"] >= 11):
                    passed_filters+=1
            # Nov 2018
            my_time = final_results.loc[final_results['Time'] == 165]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 118) & (row["Longhorn cattle"] >= 68) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # Dec 2018
            my_time = final_results.loc[final_results['Time'] == 166]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 114) & (row["Longhorn cattle"] >= 64) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # Jan 2019
            my_time = final_results.loc[final_results['Time'] == 167]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 114) & (row["Longhorn cattle"] >= 64) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # Feb 2019
            my_time = final_results.loc[final_results['Time'] == 168]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) &(row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # March 2019
            my_time = final_results.loc[final_results['Time'] == 169]
            for index, row in my_time.iterrows():
                if (row["Fallow deer"] <= 303) & (row["Fallow deer"] >= 253) &(row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) &(row["Red deer"] <= 42) & (row["Red deer"] >= 32) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # April 2019
            my_time = final_results.loc[final_results['Time'] == 170]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 126) & (row["Longhorn cattle"] >= 76) &(row["Tamworth pigs"] <= 18) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # May 2019
            my_time = final_results.loc[final_results['Time'] == 171]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 135) & (row["Longhorn cattle"] >= 85) & (row["Tamworth pigs"] <= 18) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # June 2019
            my_time = final_results.loc[final_results['Time'] == 172]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 114) & (row["Longhorn cattle"] >= 64) & (row["Tamworth pigs"] <= 18) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # July 2019
            my_time = final_results.loc[final_results['Time'] == 173]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 116) & (row["Longhorn cattle"] >= 66) &(row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # Aug 2019
            my_time = final_results.loc[final_results['Time'] == 174]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 116) & (row["Longhorn cattle"] >= 66) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # Sept 2019
            my_time = final_results.loc[final_results['Time'] == 175]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 118) & (row["Longhorn cattle"] >= 68) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # Oct 2019
            my_time = final_results.loc[final_results['Time'] == 176]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 113) & (row["Longhorn cattle"] >= 63) &(row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # Nov 2019
            my_time = final_results.loc[final_results['Time'] == 177]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 112) & (row["Longhorn cattle"] >= 62) & (row["Tamworth pigs"] <= 19) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # Dec 2019
            my_time = final_results.loc[final_results['Time'] == 178]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 105) & (row["Longhorn cattle"] >= 55) & (row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # Jan 2020
            my_time = final_results.loc[final_results['Time'] == 179]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 105) & (row["Longhorn cattle"] >= 55) & (row["Tamworth pigs"] <= 20) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # Feb 2020
            my_time = final_results.loc[final_results['Time'] == 180]
            for index, row in my_time.iterrows():
                if (row["Longhorn cattle"] <= 104) & (row["Longhorn cattle"] >= 54) & (row["Tamworth pigs"] <= 18) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # March 2020
            my_time = final_results.loc[final_results['Time'] == 181]
            for index, row in my_time.iterrows():
                if (row["Fallow deer"] <= 272) & (row["Fallow deer"] >= 222) & (row["Red deer"] <= 40) & (row["Red deer"] >= 32) &(row["Longhorn cattle"] <= 106) & (row["Longhorn cattle"] >= 56)&(row["Tamworth pigs"] <= 17) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # April 2020
            my_time = final_results.loc[final_results['Time'] == 182]
            for index, row in my_time.iterrows():
                if (row["Exmoor pony"] <= 17) & (row["Exmoor pony"] >= 14) &(row["Longhorn cattle"] <= 106) & (row["Longhorn cattle"] >= 56) &(row["Tamworth pigs"] <= 17) & (row["Tamworth pigs"] >= 1):
                    passed_filters+=1
            # May 2020
            my_time = final_results.loc[final_results['Time'] == 183]
            for index, row in my_time.iterrows():
                if (row["Tamworth pigs"] <= 29) & (row["Tamworth pigs"] >= 9) &(row["Exmoor pony"] <= 17) & (row["Exmoor pony"] >= 14) &(row["Longhorn cattle"] <= 106) & (row["Longhorn cattle"] >= 56) &(row["Roe deer"] <= 80) & (row["Roe deer"] >= 20) & (row["Grassland"] <= 36.8) & (row["Grassland"] >= 16.8) & (row["Thorny Scrub"] <= 61.8) & (row["Thorny Scrub"] >= 41.8) &(row["Woodland"] <= 31.5) & (row["Woodland"] >= 11.5):
                    passed_filters+=1

            print(passed_filters, perc_number, param_name)

            sensitivity_results_list.append(passed_filters/63)
            perc_numbers.append(str(perc_number))
            parameter_names.append(param_name)


    # append to dataframe
    final_sensitivity_results = pd.concat([pd.DataFrame({'Filters': sensitivity_results_list}), pd.DataFrame({'Percentage': perc_numbers}),(pd.DataFrame({'Parameter_Name': parameter_names}).reset_index(drop=True))], axis=1).reset_index(drop=True)
    print(final_sensitivity_results)
    final_sensitivity_results.to_excel("all_parameter_changes.xlsx")


run_sensitivity()





def graph_sensitivity(): 

    df =  pd.read_excel('all_parameter_changes.xlsx', engine='openpyxl')

    # manually find the top 3-10 with steepest gradient - then look at those
    df["Filters"] = df["Filters"] * 100

    df["Top_Parameters"] = ["All other parameters" if cell != "chance_youngScrubMatures" and cell !="chance_youngScrubMatures" and cell != "chance_saplingBecomingTree" and cell != "chance_saplingBecomingTree" and cell != "chance_reproduceSapling" else cell for cell in df.Parameter_Name] 

    df["Top_Parameters"] = ["Scrub diagonal" if cell == "chance_youngScrubMatures" else cell for cell in df["Top_Parameters"]]
    df["Top_Parameters"] = ["Grass diagonal" if cell == "chance_youngScrubMatures" else cell for cell in df["Top_Parameters"]]
    df["Top_Parameters"] = ["Grass impact on fallow deer" if cell == "chance_saplingBecomingTree" else cell for cell in df["Top_Parameters"]]
    df["Top_Parameters"] = ["Scrub impact on grassland" if cell == "chance_saplingBecomingTree" else cell for cell in df["Top_Parameters"]]
    df["Top_Parameters"] = ["Woodland impact on ponies" if cell == "chance_reproduceSapling" else cell for cell in df["Top_Parameters"]]
    print(df)


    # now plot it
    g = sns.lineplot(data=df, x="Percentage", y="Filters", hue="Top_Parameters", palette="Paired", marker="o")
    g.set(ylim=(0, 100))

    # plt.legend(title='Parameters', ncol=2)
    plt.title('Sensitivity test results')
    plt.xlabel('Delta')
    plt.ylabel('Percentage of filters passed')
    plt.legend(title='Parameters', loc='lower right')
    plt.tight_layout()
    plt.savefig('sensitivity_test.png')

    plt.show()
    
# graph_sensitivity()

# # ROE DEER
# roe_gradients = []
# # find the gradient
# for grouped_name, grouped_data in grouped_dfs:
#     res = linregress(grouped_data["Parameter_Value"], grouped_data["Roe deer"])
#     roe_gradient = [grouped_name, res.slope]
#     roe_gradients.append(roe_gradient)
# roe_gradients = pd.DataFrame(roe_gradients)
# roe_gradients.columns = ['Parameter_names', 'Gradient']
# # take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
# roe_gradients['Gradient'] = roe_gradients['Gradient'].abs()
# roe_gradients = roe_gradients.sort_values(['Gradient'], ascending=[False])
# top_ten = roe_gradients.iloc[0:10,:]
# top_ten.to_excel("/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/final_df_gradients_roeDeer.xlsx")
# # plot those
# top_ten_roe = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
# sns.set(font_scale=1)
# ro = sns.relplot(data=top_ten_roe, x='Parameter_Value', y='Roe deer', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
# ro.fig.suptitle('Roe deer gradients')
# ro.set_titles('{col_name}')
# plt.tight_layout()
# plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/sensitivity_roe.png')
# plt.show()