# run experiments on the accepted parameter sets
from KneppModel_ABM import KneppModel
from mesa import Model
from mesa.datacollection import DataCollector
import numpy as np
import pandas as pd
from schedule import RandomActivationByBreed
from mesa.space import MultiGrid
import seaborn as sns
import matplotlib.pyplot as plt
import random


                                # # # # ------ Define the model ------ # # # #


def introduce_euroBison(): # these are large intermediate feeders
    # get the parameters
    accepted_parameters = pd.read_csv('combined_accepted_parameters.csv')
    accepted_parameters.drop(['Unnamed: 0', 'run_number'], axis=1, inplace=True)
    # accepted_parameters = accepted_parameters[0:10]

    final_results_list = []
    run_number = 0

    # take the accepted parameters, and go row by row, running the model
    for _, row in accepted_parameters.iterrows():
        chance_reproduceSapling = row["chance_reproduceSapling"]
        chance_reproduceYoungScrub =  row["chance_reproduceYoungScrub"]
        chance_regrowGrass =  row["chance_regrowGrass"]
        chance_saplingBecomingTree =  row["chance_saplingBecomingTree"]
        chance_youngScrubMatures =  row["chance_youngScrubMatures"]
        chance_scrubOutcompetedByTree =  row["chance_scrubOutcompetedByTree"]
        chance_grassOutcompetedByTree =  row["chance_grassOutcompetedByTree"]
        chance_grassOutcompetedByScrub = row["chance_grassOutcompetedByScrub"]
        chance_saplingOutcompetedByTree =  row["chance_saplingOutcompetedByTree"]
        chance_saplingOutcompetedByScrub =  row["chance_saplingOutcompetedByScrub"]
        chance_youngScrubOutcompetedByScrub =  row["chance_youngScrubOutcompetedByScrub"]
        chance_youngScrubOutcompetedByTree =  row["chance_youngScrubOutcompetedByTree"]
        initial_roeDeer = row["initial_roeDeer"]
        initial_grassland =  row["initial_grassland"]
        initial_woodland =  row["initial_woodland"]
        initial_scrubland =  row["initial_scrubland"]
        roeDeer_reproduce =  row["roeDeer_reproduce"]
        roeDeer_gain_from_grass =  row["roeDeer_gain_from_grass"]
        roeDeer_gain_from_Trees =  row["roeDeer_gain_from_Trees"]
        roeDeer_gain_from_Scrub =  row["roeDeer_gain_from_Scrub"]
        roeDeer_gain_from_Saplings =  row["roeDeer_gain_from_Saplings"]
        roeDeer_gain_from_YoungScrub =  row["roeDeer_gain_from_YoungScrub"]
        ponies_gain_from_grass =  row["ponies_gain_from_grass"]
        ponies_gain_from_Trees =  row["ponies_gain_from_Trees"]
        ponies_gain_from_Scrub =  row["ponies_gain_from_Scrub"]
        ponies_gain_from_Saplings =  row["ponies_gain_from_Saplings"]
        ponies_gain_from_YoungScrub =  row["ponies_gain_from_YoungScrub"]
        cows_reproduce =  row["cows_reproduce"]
        cows_gain_from_grass =  row["cows_gain_from_grass"]
        cows_gain_from_Trees =  row["cows_gain_from_Trees"]
        cows_gain_from_Scrub =  row["cows_gain_from_Scrub"]
        cows_gain_from_Saplings =  row["cows_gain_from_Saplings"]
        cows_gain_from_YoungScrub =  row["cows_gain_from_YoungScrub"]
        fallowDeer_reproduce =  row["fallowDeer_reproduce"]
        fallowDeer_gain_from_grass =  row["fallowDeer_gain_from_grass"]
        fallowDeer_gain_from_Trees =  row["fallowDeer_gain_from_Trees"]
        fallowDeer_gain_from_Scrub =  row["fallowDeer_gain_from_Scrub"]
        fallowDeer_gain_from_Saplings =  row["fallowDeer_gain_from_Saplings"]
        fallowDeer_gain_from_YoungScrub =  row["fallowDeer_gain_from_YoungScrub"]
        redDeer_reproduce =  row["redDeer_reproduce"]
        redDeer_gain_from_grass =  row["redDeer_gain_from_grass"]
        redDeer_gain_from_Trees =  row["redDeer_gain_from_Trees"]
        redDeer_gain_from_Scrub =  row["redDeer_gain_from_Scrub"]
        redDeer_gain_from_Saplings =  row["redDeer_gain_from_Saplings"]
        redDeer_gain_from_YoungScrub =  row["redDeer_gain_from_YoungScrub"]
        pigs_reproduce =  row["pigs_reproduce"]
        pigs_gain_from_grass =  row["pigs_gain_from_grass"]
        pigs_gain_from_Trees = row["pigs_gain_from_Trees"]
        pigs_gain_from_Scrub = row["pigs_gain_from_Scrub"]
        pigs_gain_from_Saplings =  row["pigs_gain_from_Saplings"]
        pigs_gain_from_YoungScrub =  row["pigs_gain_from_YoungScrub"]
        # stocking values
        fallowDeer_stocking = 247
        cattle_stocking = 81
        redDeer_stocking = 35
        tamworthPig_stocking = 7
        exmoor_stocking = 15
        # euro bison parameters
        reproduce_bison = np.random.uniform(0.18,0.22) # make this between the min/max consumer values
        # bison should have higher impact than cows
        bison_gain_from_grass =  np.random.uniform(0.396,0.44)
        bison_gain_from_Trees = np.random.uniform(0.405,0.45)
        bison_gain_from_Scrub = np.random.uniform(0.243,0.27)
        bison_gain_from_Saplings =  np.random.uniform(0.0774,0.086)
        bison_gain_from_YoungScrub =  np.random.uniform(0.0378,0.042)
        # euro elk parameters
        reproduce_elk = np.random.uniform(0.162,0.337) # make this between the min/max consumer values
        # bison should have higher impact than any other consumer
        elk_gain_from_grass =  np.random.uniform(0.396,0.44)
        elk_gain_from_Trees =  np.random.uniform(0.405,0.45)
        elk_gain_from_Scrub = np.random.uniform(0.243,0.27)
        elk_gain_from_Saplings =  np.random.uniform(0.0774,0.086)
        elk_gain_from_YoungScrub =  np.random.uniform(0.0378,0.042)
        # reindeer parameters
        reproduce_reindeer = np.random.uniform(0.162,0.337) # make this between the min/max consumer values
        # reindeer should have impacts between red and fallow deer
        reindeer_gain_from_grass =  np.random.uniform(0.491,0.662)
        reindeer_gain_from_Trees = np.random.uniform(0.52,0.692)
        reindeer_gain_from_Scrub = np.random.uniform(0.355,0.459)
        reindeer_gain_from_Saplings =  np.random.uniform(0.107,0.143)
        reindeer_gain_from_YoungScrub =  np.random.uniform(0.057,0.0814)
        # forecasting things
        fallowDeer_stocking_forecast = 247
        cattle_stocking_forecast = 81
        redDeer_stocking_forecast = 35
        tamworthPig_stocking_forecast = 7
        exmoor_stocking_forecast = 15
        roeDeer_stocking_forecast = 0
        reindeer_stocking_forecast = 0
            
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
            width = 25, height = 18, max_time = 784, reintroduction = True,
            introduce_euroBison = True, introduce_elk = False, introduce_reindeer = False, cull_roe = False)

        model.run_model()
        run_number +=1
        print(run_number)
        results = model.datacollector.get_model_vars_dataframe()
        results['run_number'] = run_number
        final_results_list.append(results)

    # append to dataframe
    change_reintro = pd.concat(final_results_list)

    # put together the dataframe
    final_results = change_reintro[["Time", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "European bison", "European elk", "Reindeer", "Grassland", "Woodland", "Thorny Scrub", "Bare ground", "run_number"]]
    grouping_variable = np.repeat(final_results['run_number'], 13)
    y_values = final_results.drop(['run_number','Time'], axis=1).values.flatten()
    species_list = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "European bison", "European elk", "Reindeer", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 785*len(accepted_parameters))
    indices = np.repeat(final_results['Time'], 13)
    final_df = pd.DataFrame(
    {'Abundance %': y_values, 'runNumber': grouping_variable, 'Ecosystem Element': species_list, 'Time': indices})
    # calculate median
    m = final_df.groupby(['Time', 'Ecosystem Element'])[['Abundance %']].apply(np.median)
    m.name = 'Median'
    final_df = final_df.join(m, on=['Time', 'Ecosystem Element'])
    # calculate quantiles
    perc1 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(.95)
    perc1.name = 'ninetyfivePerc'
    final_df = final_df.join(perc1, on=['Time',  'Ecosystem Element'])
    perc2 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(.05)
    perc2.name = "fivePerc"
    reintroduce_euroBison = final_df.join(perc2, on=['Time', 'Ecosystem Element'])
    reintroduce_euroBison = reintroduce_euroBison.reset_index(drop=True)
    reintroduce_euroBison['introduction'] = "euroBison"

    return reintroduce_euroBison





def reintroduce_euroElk(): # these are large browsers
    reintroduce_euroBison = introduce_euroBison()

    # get the parameters
    accepted_parameters = pd.read_csv('combined_accepted_parameters.csv')
    accepted_parameters.drop(['Unnamed: 0', 'run_number'], axis=1, inplace=True)
    # accepted_parameters = accepted_parameters[0:10]
    final_results_list = []
    run_number = 0

    # take the accepted parameters, and go row by row, running the model
    for _, row in accepted_parameters.iterrows():
        chance_reproduceSapling = row["chance_reproduceSapling"]
        chance_reproduceYoungScrub =  row["chance_reproduceYoungScrub"]
        chance_regrowGrass =  row["chance_regrowGrass"]
        chance_saplingBecomingTree =  row["chance_saplingBecomingTree"]
        chance_youngScrubMatures =  row["chance_youngScrubMatures"]
        chance_scrubOutcompetedByTree =  row["chance_scrubOutcompetedByTree"]
        chance_grassOutcompetedByTree =  row["chance_grassOutcompetedByTree"]
        chance_grassOutcompetedByScrub = row["chance_grassOutcompetedByScrub"]
        chance_saplingOutcompetedByTree =  row["chance_saplingOutcompetedByTree"]
        chance_saplingOutcompetedByScrub =  row["chance_saplingOutcompetedByScrub"]
        chance_youngScrubOutcompetedByScrub =  row["chance_youngScrubOutcompetedByScrub"]
        chance_youngScrubOutcompetedByTree =  row["chance_youngScrubOutcompetedByTree"]
        initial_roeDeer = row["initial_roeDeer"]
        initial_grassland =  row["initial_grassland"]
        initial_woodland =  row["initial_woodland"]
        initial_scrubland =  row["initial_scrubland"]
        roeDeer_reproduce =  row["roeDeer_reproduce"]
        roeDeer_gain_from_grass =  row["roeDeer_gain_from_grass"]
        roeDeer_gain_from_Trees =  row["roeDeer_gain_from_Trees"]
        roeDeer_gain_from_Scrub =  row["roeDeer_gain_from_Scrub"]
        roeDeer_gain_from_Saplings =  row["roeDeer_gain_from_Saplings"]
        roeDeer_gain_from_YoungScrub =  row["roeDeer_gain_from_YoungScrub"]
        ponies_gain_from_grass =  row["ponies_gain_from_grass"]
        ponies_gain_from_Trees =  row["ponies_gain_from_Trees"]
        ponies_gain_from_Scrub =  row["ponies_gain_from_Scrub"]
        ponies_gain_from_Saplings =  row["ponies_gain_from_Saplings"]
        ponies_gain_from_YoungScrub =  row["ponies_gain_from_YoungScrub"]
        cows_reproduce =  row["cows_reproduce"]
        cows_gain_from_grass =  row["cows_gain_from_grass"]
        cows_gain_from_Trees =  row["cows_gain_from_Trees"]
        cows_gain_from_Scrub =  row["cows_gain_from_Scrub"]
        cows_gain_from_Saplings =  row["cows_gain_from_Saplings"]
        cows_gain_from_YoungScrub =  row["cows_gain_from_YoungScrub"]
        fallowDeer_reproduce =  row["fallowDeer_reproduce"]
        fallowDeer_gain_from_grass =  row["fallowDeer_gain_from_grass"]
        fallowDeer_gain_from_Trees =  row["fallowDeer_gain_from_Trees"]
        fallowDeer_gain_from_Scrub =  row["fallowDeer_gain_from_Scrub"]
        fallowDeer_gain_from_Saplings =  row["fallowDeer_gain_from_Saplings"]
        fallowDeer_gain_from_YoungScrub =  row["fallowDeer_gain_from_YoungScrub"]
        redDeer_reproduce =  row["redDeer_reproduce"]
        redDeer_gain_from_grass =  row["redDeer_gain_from_grass"]
        redDeer_gain_from_Trees =  row["redDeer_gain_from_Trees"]
        redDeer_gain_from_Scrub =  row["redDeer_gain_from_Scrub"]
        redDeer_gain_from_Saplings =  row["redDeer_gain_from_Saplings"]
        redDeer_gain_from_YoungScrub =  row["redDeer_gain_from_YoungScrub"]
        pigs_reproduce =  row["pigs_reproduce"]
        pigs_gain_from_grass =  row["pigs_gain_from_grass"]
        pigs_gain_from_Trees = row["pigs_gain_from_Trees"]
        pigs_gain_from_Scrub = row["pigs_gain_from_Scrub"]
        pigs_gain_from_Saplings =  row["pigs_gain_from_Saplings"]
        pigs_gain_from_YoungScrub =  row["pigs_gain_from_YoungScrub"]
        # stocking values
        fallowDeer_stocking = 247
        cattle_stocking = 81
        redDeer_stocking = 35
        tamworthPig_stocking = 7
        exmoor_stocking = 15
       # euro bison parameters
        reproduce_bison = np.random.uniform(0.18,0.22) # make this between the min/max consumer values
        # bison should have higher impact than cows
        bison_gain_from_grass =  np.random.uniform(0.396,0.44)
        bison_gain_from_Trees = np.random.uniform(0.405,0.45)
        bison_gain_from_Scrub = np.random.uniform(0.243,0.27)
        bison_gain_from_Saplings =  np.random.uniform(0.0774,0.086)
        bison_gain_from_YoungScrub =  np.random.uniform(0.0378,0.042)
        # euro elk parameters
        reproduce_elk = np.random.uniform(0.162,0.337) # make this between the min/max consumer values
        # bison should have higher impact than any other consumer
        elk_gain_from_grass =  np.random.uniform(0.396,0.44)
        elk_gain_from_Trees =  np.random.uniform(0.405,0.45)
        elk_gain_from_Scrub = np.random.uniform(0.243,0.27)
        elk_gain_from_Saplings =  np.random.uniform(0.0774,0.086)
        elk_gain_from_YoungScrub =  np.random.uniform(0.0378,0.042)
        # reindeer parameters
        reproduce_reindeer = np.random.uniform(0.162,0.337) # make this between the min/max consumer values
        # reindeer should have impacts between red and fallow deer
        reindeer_gain_from_grass =  np.random.uniform(0.491,0.662)
        reindeer_gain_from_Trees = np.random.uniform(0.52,0.692)
        reindeer_gain_from_Scrub = np.random.uniform(0.355,0.459)
        reindeer_gain_from_Saplings =  np.random.uniform(0.107,0.143)
        reindeer_gain_from_YoungScrub =  np.random.uniform(0.057,0.0814)
        # forecasting things
        fallowDeer_stocking_forecast = 247
        cattle_stocking_forecast = 81
        redDeer_stocking_forecast = 35
        tamworthPig_stocking_forecast = 7
        exmoor_stocking_forecast = 15
        roeDeer_stocking_forecast = 0
        reindeer_stocking_forecast = 0
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
            width = 25, height = 18, max_time = 784, reintroduction = True,
            introduce_euroBison = False, introduce_elk = True, introduce_reindeer = False, cull_roe = False)

        model.run_model()

        run_number +=1
        print(run_number)
        results = model.datacollector.get_model_vars_dataframe()
        results['run_number'] = run_number
        results['introduction'] = "euroElk"
        final_results_list.append(results)

    # append to dataframe
    change_reintro = pd.concat(final_results_list)

    # graph that
    final_results = change_reintro[["Time", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "European bison", "European elk", "Reindeer", "Grassland", "Woodland", "Thorny Scrub", "Bare ground", "run_number", "introduction"]]
    grouping_variable = np.repeat(final_results['run_number'], 13)
    y_values = final_results.drop(['run_number','introduction','Time'], axis=1).values.flatten()
    species_list = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs","European bison", "European elk", "Reindeer","Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 785*len(accepted_parameters))
    indices = np.repeat(final_results['Time'], 13)
    accepted_shape = np.repeat(final_results['introduction'], 13)

    final_df = pd.DataFrame(
    {'Abundance %': y_values, 'runNumber': grouping_variable, 'Ecosystem Element': species_list, 'Time': indices, 'introduction': accepted_shape})

    # calculate median
    m = final_df.groupby(['Time', 'introduction', 'Ecosystem Element'])[['Abundance %']].apply(np.median)
    m.name = 'Median'
    final_df = final_df.join(m, on=['Time', 'introduction', 'Ecosystem Element'])
    # calculate quantiles
    perc1 = final_df.groupby(['Time', 'introduction', 'Ecosystem Element'])['Abundance %'].quantile(.95)
    perc1.name = 'ninetyfivePerc'
    final_df = final_df.join(perc1, on=['Time', 'introduction', 'Ecosystem Element'])
    perc2 = final_df.groupby(['Time', 'introduction', 'Ecosystem Element'])['Abundance %'].quantile(.05)
    perc2.name = "fivePerc"
    reintroduce_euroElk = final_df.join(perc2, on=['Time','introduction', 'Ecosystem Element'])
    # colors = ["#6788ee", "#e26952", "#3F9E4D"]
    reintroduce_euroElk = reintroduce_euroElk.reset_index(drop=True)
    # concat euro bison and elk results
    final_df = pd.concat([reintroduce_euroElk, reintroduce_euroBison])
    return final_df



def reintroduce_reindeer(): # these are medium intermediate feeders (between fallow and red deer)
    final_df = reintroduce_euroElk()

    # get the parameters
    accepted_parameters = pd.read_csv('combined_accepted_parameters.csv')
    accepted_parameters.drop(['Unnamed: 0', 'run_number'], axis=1, inplace=True)
    # accepted_parameters = accepted_parameters[0:10]
    final_results_list = []
    run_number = 0

    # take the accepted parameters, and go row by row, running the model
    for _, row in accepted_parameters.iterrows():
        chance_reproduceSapling = row["chance_reproduceSapling"]
        chance_reproduceYoungScrub =  row["chance_reproduceYoungScrub"]
        chance_regrowGrass =  row["chance_regrowGrass"]
        chance_saplingBecomingTree =  row["chance_saplingBecomingTree"]
        chance_youngScrubMatures =  row["chance_youngScrubMatures"]
        chance_scrubOutcompetedByTree =  row["chance_scrubOutcompetedByTree"]
        chance_grassOutcompetedByTree =  row["chance_grassOutcompetedByTree"]
        chance_grassOutcompetedByScrub = row["chance_grassOutcompetedByScrub"]
        chance_saplingOutcompetedByTree =  row["chance_saplingOutcompetedByTree"]
        chance_saplingOutcompetedByScrub =  row["chance_saplingOutcompetedByScrub"]
        chance_youngScrubOutcompetedByScrub =  row["chance_youngScrubOutcompetedByScrub"]
        chance_youngScrubOutcompetedByTree =  row["chance_youngScrubOutcompetedByTree"]
        initial_roeDeer = row["initial_roeDeer"]
        initial_grassland =  row["initial_grassland"]
        initial_woodland =  row["initial_woodland"]
        initial_scrubland =  row["initial_scrubland"]
        roeDeer_reproduce =  row["roeDeer_reproduce"]
        roeDeer_gain_from_grass =  row["roeDeer_gain_from_grass"]
        roeDeer_gain_from_Trees =  row["roeDeer_gain_from_Trees"]
        roeDeer_gain_from_Scrub =  row["roeDeer_gain_from_Scrub"]
        roeDeer_gain_from_Saplings =  row["roeDeer_gain_from_Saplings"]
        roeDeer_gain_from_YoungScrub =  row["roeDeer_gain_from_YoungScrub"]
        ponies_gain_from_grass =  row["ponies_gain_from_grass"]
        ponies_gain_from_Trees =  row["ponies_gain_from_Trees"]
        ponies_gain_from_Scrub =  row["ponies_gain_from_Scrub"]
        ponies_gain_from_Saplings =  row["ponies_gain_from_Saplings"]
        ponies_gain_from_YoungScrub =  row["ponies_gain_from_YoungScrub"]
        cows_reproduce =  row["cows_reproduce"]
        cows_gain_from_grass =  row["cows_gain_from_grass"]
        cows_gain_from_Trees =  row["cows_gain_from_Trees"]
        cows_gain_from_Scrub =  row["cows_gain_from_Scrub"]
        cows_gain_from_Saplings =  row["cows_gain_from_Saplings"]
        cows_gain_from_YoungScrub =  row["cows_gain_from_YoungScrub"]
        fallowDeer_reproduce =  row["fallowDeer_reproduce"]
        fallowDeer_gain_from_grass =  row["fallowDeer_gain_from_grass"]
        fallowDeer_gain_from_Trees =  row["fallowDeer_gain_from_Trees"]
        fallowDeer_gain_from_Scrub =  row["fallowDeer_gain_from_Scrub"]
        fallowDeer_gain_from_Saplings =  row["fallowDeer_gain_from_Saplings"]
        fallowDeer_gain_from_YoungScrub =  row["fallowDeer_gain_from_YoungScrub"]
        redDeer_reproduce =  row["redDeer_reproduce"]
        redDeer_gain_from_grass =  row["redDeer_gain_from_grass"]
        redDeer_gain_from_Trees =  row["redDeer_gain_from_Trees"]
        redDeer_gain_from_Scrub =  row["redDeer_gain_from_Scrub"]
        redDeer_gain_from_Saplings =  row["redDeer_gain_from_Saplings"]
        redDeer_gain_from_YoungScrub =  row["redDeer_gain_from_YoungScrub"]
        pigs_reproduce =  row["pigs_reproduce"]
        pigs_gain_from_grass =  row["pigs_gain_from_grass"]
        pigs_gain_from_Trees = row["pigs_gain_from_Trees"]
        pigs_gain_from_Scrub = row["pigs_gain_from_Scrub"]
        pigs_gain_from_Saplings =  row["pigs_gain_from_Saplings"]
        pigs_gain_from_YoungScrub =  row["pigs_gain_from_YoungScrub"]
        # stocking values
        fallowDeer_stocking = 247
        cattle_stocking = 81
        redDeer_stocking = 35
        tamworthPig_stocking = 7
        exmoor_stocking = 15
       # euro bison parameters
        reproduce_bison = np.random.uniform(0.18,0.22) # make this between the min/max consumer values
        # bison should have higher impact than cows
        bison_gain_from_grass =  np.random.uniform(0.396,0.44)
        bison_gain_from_Trees = np.random.uniform(0.405,0.45)
        bison_gain_from_Scrub = np.random.uniform(0.243,0.27)
        bison_gain_from_Saplings =  np.random.uniform(0.0774,0.086)
        bison_gain_from_YoungScrub =  np.random.uniform(0.0378,0.042)
        # euro elk parameters
        reproduce_elk = np.random.uniform(0.162,0.337) # make this between the min/max consumer values
        # bison should have higher impact than any other consumer
        elk_gain_from_grass =  np.random.uniform(0.396,0.44)
        elk_gain_from_Trees =  np.random.uniform(0.405,0.45)
        elk_gain_from_Scrub = np.random.uniform(0.243,0.27)
        elk_gain_from_Saplings =  np.random.uniform(0.0774,0.086)
        elk_gain_from_YoungScrub =  np.random.uniform(0.0378,0.042)
        # reindeer parameters
        reproduce_reindeer = np.random.uniform(0.162,0.337) # make this between the min/max consumer values
        # reindeer should have impacts between red and fallow deer
        reindeer_gain_from_grass =  np.random.uniform(0.491,0.662)
        reindeer_gain_from_Trees = np.random.uniform(0.52,0.692)
        reindeer_gain_from_Scrub = np.random.uniform(0.355,0.459)
        reindeer_gain_from_Saplings =  np.random.uniform(0.107,0.143)
        reindeer_gain_from_YoungScrub =  np.random.uniform(0.057,0.0814)
        # forecasting things
        fallowDeer_stocking_forecast = 247
        cattle_stocking_forecast = 81
        redDeer_stocking_forecast = 35
        tamworthPig_stocking_forecast = 7
        exmoor_stocking_forecast = 15
        roeDeer_stocking_forecast = 0
        reindeer_stocking_forecast = 50
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
            width = 25, height = 18, max_time = 784, reintroduction = True,
            introduce_euroBison = False, introduce_elk = False, introduce_reindeer = True, cull_roe = False)

        model.run_model()

        run_number +=1
        print(run_number)
        results = model.datacollector.get_model_vars_dataframe()
        results['run_number'] = run_number
        results['introduction'] = "Reindeer"
        final_results_list.append(results)

    # append to dataframe
    change_reintro = pd.concat(final_results_list)
    palette=['#009e73', '#f0e442', '#0072b2','#cc79a7']

    # graph that
    final_results = change_reintro[["Time", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "European bison", "European elk", "Reindeer","Grassland", "Woodland", "Thorny Scrub", "Bare ground", "run_number", "introduction"]]
    grouping_variable = np.repeat(final_results['run_number'], 13)
    y_values = final_results.drop(['run_number','introduction','Time'], axis=1).values.flatten()
    species_list = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "European bison", "European elk", "Reindeer","Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 785*len(accepted_parameters))
    indices = np.repeat(final_results['Time'], 13)
    accepted_shape = np.repeat(final_results['introduction'], 13)

    final_df_2 = pd.DataFrame(
    {'Abundance %': y_values, 'runNumber': grouping_variable, 'Ecosystem Element': species_list, 'Time': indices, 'introduction': accepted_shape})
    # calculate median
    m = final_df_2.groupby(['Time', 'introduction', 'Ecosystem Element'])[['Abundance %']].apply(np.median)
    m.name = 'Median'
    final_df_2 = final_df_2.join(m, on=['Time', 'introduction', 'Ecosystem Element'])
    # calculate quantiles
    perc1 = final_df_2.groupby(['Time', 'introduction', 'Ecosystem Element'])['Abundance %'].quantile(.95)
    perc1.name = 'ninetyfivePerc'
    final_df_2 = final_df_2.join(perc1, on=['Time', 'introduction', 'Ecosystem Element'])
    perc2 = final_df_2.groupby(['Time', 'introduction', 'Ecosystem Element'])['Abundance %'].quantile(.05)
    perc2.name = "fivePerc"
    reintroduce_reindeer = final_df_2.join(perc2, on=['Time','introduction', 'Ecosystem Element'])
    # colors = ["#6788ee", "#e26952", "#3F9E4D"]
    reintroduce_reindeer = reintroduce_reindeer.reset_index(drop=True)

    # concat euro bison and elk results
    final_df_allHerbs = pd.concat([reintroduce_reindeer, final_df])

    f = sns.FacetGrid(final_df_allHerbs, col="Ecosystem Element", palette=palette, hue = "introduction", col_wrap=5, sharey = False)
    f.map(sns.lineplot, 'Time', 'Median') 
    # 0,1,2,3,4,
    f.map(sns.lineplot, 'Time', 'fivePerc')
    # 5,6,7,8,9,
    f.map(sns.lineplot, 'Time', 'ninetyfivePerc')
    # 10,11,12,13,14,
    for ax in f.axes.flat:
        ax.fill_between(ax.lines[3].get_xdata(),ax.lines[3].get_ydata(), ax.lines[6].get_ydata(), color = '#009e73', alpha =0.2)
        ax.fill_between(ax.lines[4].get_xdata(),ax.lines[4].get_ydata(), ax.lines[7].get_ydata(), color = '#f0e442', alpha =0.2)
        ax.fill_between(ax.lines[5].get_xdata(),ax.lines[5].get_ydata(), ax.lines[8].get_ydata(), color = '#0072b2', alpha =0.2)
        ax.set_ylabel('Abundance')
    # add subplot titles
    axes = f.axes.flatten()
    # fill between the quantiles
    axes[0].set_title("Roe deer")
    axes[1].set_title("Exmoor pony")
    axes[2].set_title("Fallow deer")
    axes[3].set_title("Longhorn cattle")
    axes[4].set_title("Red deer")
    axes[5].set_title("Tamworth pigs")
    axes[6].set_title("European bison")
    axes[7].set_title("European elk")
    axes[8].set_title("Reindeer")
    axes[9].set_title("Grassland")
    axes[10].set_title("Woodland")
    axes[11].set_title("Thorny scrub")
    axes[12].set_title("Bare ground")
    f.fig.suptitle('Introduce Large Herbivores')
    plt.tight_layout()
    plt.legend(labels=['Reindeer','European elk', 'European bison'],bbox_to_anchor=(2.2, 0), loc='lower right', fontsize=12)

    plt.savefig('introductions_experiment.png')
    plt.show()

    final_df_allHerbs.to_csv("reintroduce_euroElk_euroBison.csv")
    return final_df_allHerbs


reintroduce_reindeer()
