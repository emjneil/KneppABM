# run experiments on the accepted parameter sets
from run_model_linux import run_all_models
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
    accepted_parameters = pd.read_csv('outputs/ten_perc/accepted_parameters_10%.csv')
    accepted_parameters.drop(['Unnamed: 0', 'run_number'], axis=1, inplace=True)
    accepted_parameters = accepted_parameters[0:5]

    final_results_list = []
    run_number = 0

    # take the accepted parameters, and go row by row, running the model
    for _, row in accepted_parameters.iterrows():
        chance_reproduceSapling = row[0]
        chance_reproduceYoungScrub =  row[1]
        chance_regrowGrass =  row[2]
        chance_saplingBecomingTree =  row[3]
        chance_youngScrubMatures =  row[4]
        chance_scrubOutcompetedByTree =  row[5]
        chance_grassOutcompetedByTree =  row[6]
        chance_grassOutcompetedByScrub = row[7]
        chance_saplingOutcompetedByTree =  row[8]
        chance_saplingOutcompetedByScrub =  row[9]
        chance_youngScrubOutcompetedByScrub =  row[10]
        chance_youngScrubOutcompetedByTree =  row[11]
        initial_roeDeer = row[12]
        initial_grassland =  row[13]
        initial_woodland =  row[14]
        initial_scrubland =  row[15]
        roeDeer_reproduce =  row[16]
        roeDeer_gain_from_grass =  row[17]
        roeDeer_gain_from_Trees =  row[18]
        roeDeer_gain_from_Scrub =  row[19]
        roeDeer_gain_from_Saplings =  row[20]
        roeDeer_gain_from_YoungScrub =  row[21]
        ponies_gain_from_grass =  row[22]
        ponies_gain_from_Trees =  row[23]
        ponies_gain_from_Scrub =  row[24]
        ponies_gain_from_Saplings =  row[25]
        ponies_gain_from_YoungScrub =  row[26]
        cows_reproduce =  row[27]
        cows_gain_from_grass =  row[28]
        cows_gain_from_Trees =  row[29]
        cows_gain_from_Scrub =  row[30]
        cows_gain_from_Saplings =  row[31]
        cows_gain_from_YoungScrub =  row[32]
        fallowDeer_reproduce =  row[33]
        fallowDeer_gain_from_grass =  row[34]
        fallowDeer_gain_from_Trees =  row[35]
        fallowDeer_gain_from_Scrub =  row[36]
        fallowDeer_gain_from_Saplings =  row[37]
        fallowDeer_gain_from_YoungScrub =  row[38]
        redDeer_reproduce =  row[39]
        redDeer_gain_from_grass =  row[40]
        redDeer_gain_from_Trees =  row[41]
        redDeer_gain_from_Scrub =  row[42]
        redDeer_gain_from_Saplings =  row[43]
        redDeer_gain_from_YoungScrub =  row[44]
        pigs_reproduce =  row[45]
        pigs_gain_from_grass =  row[46]
        pigs_gain_from_Trees = row[47]
        pigs_gain_from_Scrub = row[48]
        pigs_gain_from_Saplings =  row[49]
        pigs_gain_from_YoungScrub =  row[50]
        # stocking values
        fallowDeer_stocking = 247
        cattle_stocking = 81
        redDeer_stocking = 35
        tamworthPig_stocking = 7
        exmoor_stocking = 15
        # euro bison parameters
        reproduce_bison = np.random.uniform(0.18,0.31) # make this between the min/max consumer values 
        # bison should have higher impact than any other consumer
        bison_gain_from_grass =  np.random.uniform(0,0.59)
        bison_gain_from_Trees = np.random.uniform(0,0.215)
        bison_gain_from_Scrub = np.random.uniform(0,0.093)
        bison_gain_from_Saplings =  np.random.uniform(0,0.06)
        bison_gain_from_YoungScrub =  np.random.uniform(0,0.016)    
        # euro elk parameters
        reproduce_elk = np.random.uniform(0.18,0.31) # make this between the min/max consumer values 
        # bison should have higher impact than any other consumer
        elk_gain_from_grass =  np.random.uniform(0,0.59)
        elk_gain_from_Trees = np.random.uniform(0,0.215)
        elk_gain_from_Scrub = np.random.uniform(0,0.093)
        elk_gain_from_Saplings =  np.random.uniform(0,0.06)
        elk_gain_from_YoungScrub =  np.random.uniform(0,0.016)  
        # reindeer parameters
        reproduce_reindeer = np.random.uniform(0.18,0.31) # make this between the min/max consumer values 
        # reindeer should have impacts between red and fallow deer
        reindeer_gain_from_grass =  np.random.uniform(0.743,0.797)
        reindeer_gain_from_Trees = np.random.uniform(0.446,0.534)
        reindeer_gain_from_Scrub = np.random.uniform(0.188,0.249)
        reindeer_gain_from_Saplings =  np.random.uniform(0.076,0.118)
        reindeer_gain_from_YoungScrub =  np.random.uniform(0.065,0.073)  


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
            width = 25, height = 18, max_time = 784, reintroduction = True,
            introduce_euroBison = True, introduce_elk = False, introduce_reindeer = False)
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
    accepted_parameters = pd.read_csv('outputs/ten_perc/accepted_parameters_10%.csv')
    accepted_parameters.drop(['Unnamed: 0', 'run_number'], axis=1, inplace=True)
    accepted_parameters = accepted_parameters[0:5]
    final_results_list = []
    run_number = 0

    # take the accepted parameters, and go row by row, running the model
    for _, row in accepted_parameters.iterrows():
        chance_reproduceSapling = row[0]
        chance_reproduceYoungScrub =  row[1]
        chance_regrowGrass =  row[2]
        chance_saplingBecomingTree =  row[3]
        chance_youngScrubMatures =  row[4]
        chance_scrubOutcompetedByTree =  row[5]
        chance_grassOutcompetedByTree =  row[6]
        chance_grassOutcompetedByScrub = row[7]
        chance_saplingOutcompetedByTree =  row[8]
        chance_saplingOutcompetedByScrub =  row[9]
        chance_youngScrubOutcompetedByScrub =  row[10]
        chance_youngScrubOutcompetedByTree =  row[11]
        initial_roeDeer = row[12]
        initial_grassland =  row[13]
        initial_woodland =  row[14]
        initial_scrubland =  row[15]
        roeDeer_reproduce =  row[16]
        roeDeer_gain_from_grass =  row[17]
        roeDeer_gain_from_Trees =  row[18]
        roeDeer_gain_from_Scrub =  row[19]
        roeDeer_gain_from_Saplings =  row[20]
        roeDeer_gain_from_YoungScrub =  row[21]
        ponies_gain_from_grass =  row[22]
        ponies_gain_from_Trees =  row[23]
        ponies_gain_from_Scrub =  row[24]
        ponies_gain_from_Saplings =  row[25]
        ponies_gain_from_YoungScrub =  row[26]
        cows_reproduce =  row[27]
        cows_gain_from_grass =  row[28]
        cows_gain_from_Trees =  row[29]
        cows_gain_from_Scrub =  row[30]
        cows_gain_from_Saplings =  row[31]
        cows_gain_from_YoungScrub =  row[32]
        fallowDeer_reproduce =  row[33]
        fallowDeer_gain_from_grass =  row[34]
        fallowDeer_gain_from_Trees =  row[35]
        fallowDeer_gain_from_Scrub =  row[36]
        fallowDeer_gain_from_Saplings =  row[37]
        fallowDeer_gain_from_YoungScrub =  row[38]
        redDeer_reproduce =  row[39]
        redDeer_gain_from_grass =  row[40]
        redDeer_gain_from_Trees =  row[41]
        redDeer_gain_from_Scrub =  row[42]
        redDeer_gain_from_Saplings =  row[43]
        redDeer_gain_from_YoungScrub =  row[44]
        pigs_reproduce =  row[45]
        pigs_gain_from_grass =  row[46]
        pigs_gain_from_Trees = row[47]
        pigs_gain_from_Scrub = row[48]
        pigs_gain_from_Saplings =  row[49]
        pigs_gain_from_YoungScrub =  row[50]
        # stocking values
        fallowDeer_stocking = 247
        cattle_stocking = 81
        redDeer_stocking = 35
        tamworthPig_stocking = 7
        exmoor_stocking = 15
        # euro bison parameters
        reproduce_bison = np.random.uniform(0.18,0.31) # make this between the min/max consumer values 
        # bison should have higher impact than any other consumer
        bison_gain_from_grass =  np.random.uniform(0,0.59)
        bison_gain_from_Trees = np.random.uniform(0,0.215)
        bison_gain_from_Scrub = np.random.uniform(0,0.093)
        bison_gain_from_Saplings =  np.random.uniform(0,0.06)
        bison_gain_from_YoungScrub =  np.random.uniform(0,0.016)    
        # euro elk parameters
        reproduce_elk = np.random.uniform(0.18,0.31) # make this between the min/max consumer values 
        # bison should have higher impact than any other consumer
        elk_gain_from_grass =  np.random.uniform(0,0.59)
        elk_gain_from_Trees = np.random.uniform(0,0.215)
        elk_gain_from_Scrub = np.random.uniform(0,0.093)
        elk_gain_from_Saplings =  np.random.uniform(0,0.06)
        elk_gain_from_YoungScrub =  np.random.uniform(0,0.016)   
        # reindeer parameters
        reproduce_reindeer = np.random.uniform(0.18,0.31) # make this between the min/max consumer values 
        # reindeer should have impacts between red and fallow deer
        reindeer_gain_from_grass =  np.random.uniform(0.743,0.797)
        reindeer_gain_from_Trees = np.random.uniform(0.446,0.534)
        reindeer_gain_from_Scrub = np.random.uniform(0.188,0.249)
        reindeer_gain_from_Saplings =  np.random.uniform(0.076,0.118)
        reindeer_gain_from_YoungScrub =  np.random.uniform(0.065,0.073)  

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
            width = 25, height = 18, max_time = 784, reintroduction = True,
            introduce_euroBison = False, introduce_elk = True, introduce_reindeer = False)

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
    accepted_parameters = pd.read_csv('outputs/ten_perc/accepted_parameters_10%.csv')
    accepted_parameters.drop(['Unnamed: 0', 'run_number'], axis=1, inplace=True)
    accepted_parameters = accepted_parameters[0:5]
    final_results_list = []
    run_number = 0

    # take the accepted parameters, and go row by row, running the model
    for _, row in accepted_parameters.iterrows():
        chance_reproduceSapling = row[0]
        chance_reproduceYoungScrub =  row[1]
        chance_regrowGrass =  row[2]
        chance_saplingBecomingTree =  row[3]
        chance_youngScrubMatures =  row[4]
        chance_scrubOutcompetedByTree =  row[5]
        chance_grassOutcompetedByTree =  row[6]
        chance_grassOutcompetedByScrub = row[7]
        chance_saplingOutcompetedByTree =  row[8]
        chance_saplingOutcompetedByScrub =  row[9]
        chance_youngScrubOutcompetedByScrub =  row[10]
        chance_youngScrubOutcompetedByTree =  row[11]
        initial_roeDeer = row[12]
        initial_grassland =  row[13]
        initial_woodland =  row[14]
        initial_scrubland =  row[15]
        roeDeer_reproduce =  row[16]
        roeDeer_gain_from_grass =  row[17]
        roeDeer_gain_from_Trees =  row[18]
        roeDeer_gain_from_Scrub =  row[19]
        roeDeer_gain_from_Saplings =  row[20]
        roeDeer_gain_from_YoungScrub =  row[21]
        ponies_gain_from_grass =  row[22]
        ponies_gain_from_Trees =  row[23]
        ponies_gain_from_Scrub =  row[24]
        ponies_gain_from_Saplings =  row[25]
        ponies_gain_from_YoungScrub =  row[26]
        cows_reproduce =  row[27]
        cows_gain_from_grass =  row[28]
        cows_gain_from_Trees =  row[29]
        cows_gain_from_Scrub =  row[30]
        cows_gain_from_Saplings =  row[31]
        cows_gain_from_YoungScrub =  row[32]
        fallowDeer_reproduce =  row[33]
        fallowDeer_gain_from_grass =  row[34]
        fallowDeer_gain_from_Trees =  row[35]
        fallowDeer_gain_from_Scrub =  row[36]
        fallowDeer_gain_from_Saplings =  row[37]
        fallowDeer_gain_from_YoungScrub =  row[38]
        redDeer_reproduce =  row[39]
        redDeer_gain_from_grass =  row[40]
        redDeer_gain_from_Trees =  row[41]
        redDeer_gain_from_Scrub =  row[42]
        redDeer_gain_from_Saplings =  row[43]
        redDeer_gain_from_YoungScrub =  row[44]
        pigs_reproduce =  row[45]
        pigs_gain_from_grass =  row[46]
        pigs_gain_from_Trees = row[47]
        pigs_gain_from_Scrub = row[48]
        pigs_gain_from_Saplings =  row[49]
        pigs_gain_from_YoungScrub =  row[50]
        # stocking values
        fallowDeer_stocking = 247
        cattle_stocking = 81
        redDeer_stocking = 35
        tamworthPig_stocking = 7
        exmoor_stocking = 15
        # euro bison parameters
        reproduce_bison = np.random.uniform(0.18,0.31) # make this between the min/max consumer values 
        # bison should have higher impact than any other consumer
        bison_gain_from_grass =  np.random.uniform(0.44,0.59)
        bison_gain_from_Trees = np.random.uniform(0.016,0.215)
        bison_gain_from_Scrub = np.random.uniform(0.07,0.093)
        bison_gain_from_Saplings =  np.random.uniform(0.045,0.06)
        bison_gain_from_YoungScrub =  np.random.uniform(0.012,0.016)  
        # euro elk parameters
        reproduce_elk = np.random.uniform(0.18,0.31) # make this between the min/max consumer values 
        # bison should have higher impact than any other consumer
        elk_gain_from_grass =  np.random.uniform(0.44,0.59)
        elk_gain_from_Trees = np.random.uniform(0.016,0.215)
        elk_gain_from_Scrub = np.random.uniform(0.07,0.093)
        elk_gain_from_Saplings =  np.random.uniform(0.045,0.06)
        elk_gain_from_YoungScrub =  np.random.uniform(0.012,0.016)   
        # reindeer parameters
        reproduce_reindeer = np.random.uniform(0.18,0.31) # make this between the min/max consumer values 
        # reindeer should have impacts between red and fallow deer
        reindeer_gain_from_grass =  np.random.uniform(0.743,0.797)
        reindeer_gain_from_Trees = np.random.uniform(0.446,0.534)
        reindeer_gain_from_Scrub = np.random.uniform(0.188,0.249)
        reindeer_gain_from_Saplings =  np.random.uniform(0.076,0.118)
        reindeer_gain_from_YoungScrub =  np.random.uniform(0.065,0.073)  

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
            width = 25, height = 18, max_time = 784, reintroduction = True,
            introduce_euroBison = False, introduce_elk = False, introduce_reindeer = True)

        model.run_model()

        run_number +=1
        print(run_number)
        results = model.datacollector.get_model_vars_dataframe()
        results['run_number'] = run_number
        results['introduction'] = "Reindeer"
        final_results_list.append(results)

    # append to dataframe
    change_reintro = pd.concat(final_results_list)
    palette=['#db5f57', '#57d3db', '#57db5f','#5f57db', '#db57d3']

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
        ax.fill_between(ax.lines[3].get_xdata(),ax.lines[3].get_ydata(), ax.lines[6].get_ydata(), color = '#db5f57', alpha =0.2)
        ax.fill_between(ax.lines[4].get_xdata(),ax.lines[4].get_ydata(), ax.lines[7].get_ydata(), color = '#57d3db', alpha =0.2)
        ax.fill_between(ax.lines[5].get_xdata(),ax.lines[5].get_ydata(), ax.lines[8].get_ydata(), color = '#57db5f', alpha =0.2)
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
