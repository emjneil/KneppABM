# ------ Optimization of the Knepp ABM model --------
from model import KneppModel 
import numpy as np
import pandas as pd
from geneticalgorithm import geneticalgorithm as ga
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import statistics
import random

# ------ Optimization of the Knepp ABM model --------

def objectiveFunction(x):

    accepted_parameters = pd.read_csv('combined_accepted_parameters.csv') 
    accepted_parameters.drop(['Unnamed: 0'], axis=1, inplace=True)
    # visualize the best run
    accepted_parameters = accepted_parameters.loc[(accepted_parameters['run_number'] == 55724)]


    # define the parameters 
    chance_reproduceSapling = accepted_parameters["chance_reproduceSapling"].item()
    chance_reproduceYoungScrub =  accepted_parameters["chance_reproduceYoungScrub"].item()
    chance_regrowGrass =  accepted_parameters["chance_regrowGrass"].item()
    chance_saplingBecomingTree =  accepted_parameters["chance_saplingBecomingTree"].item()
    chance_youngScrubMatures =  accepted_parameters["chance_youngScrubMatures"].item()
    chance_scrubOutcompetedByTree =  accepted_parameters["chance_scrubOutcompetedByTree"].item()
    chance_grassOutcompetedByTree =  accepted_parameters["chance_grassOutcompetedByTree"].item()
    chance_grassOutcompetedByScrub = accepted_parameters["chance_grassOutcompetedByScrub"].item()

    initial_roe = 12
    fallowDeer_stocking = 247
    cattle_stocking = 81
    redDeer_stocking = 35
    tamworthPig_stocking = 7
    exmoor_stocking = 15

    roe_deer_reproduce = accepted_parameters["roe_deer_reproduce"].item()
    roe_deer_gain_from_grass =  accepted_parameters["roe_deer_gain_from_grass"].item()
    roe_deer_gain_from_trees =  accepted_parameters["roe_deer_gain_from_trees"].item()
    roe_deer_gain_from_scrub =  accepted_parameters["roe_deer_gain_from_scrub"].item()
    roe_deer_gain_from_saplings =  accepted_parameters["roe_deer_gain_from_saplings"].item()
    roe_deer_gain_from_young_scrub =  accepted_parameters["roe_deer_gain_from_young_scrub"].item()
    ponies_gain_from_grass =  accepted_parameters["ponies_gain_from_grass"].item()
    ponies_gain_from_trees =  accepted_parameters["ponies_gain_from_trees"].item()
    ponies_gain_from_scrub =  accepted_parameters["ponies_gain_from_scrub"].item()
    ponies_gain_from_saplings =  accepted_parameters["ponies_gain_from_saplings"].item()
    ponies_gain_from_young_scrub =  accepted_parameters["ponies_gain_from_young_scrub"].item()
    cattle_reproduce =  accepted_parameters["cattle_reproduce"].item()
    cows_gain_from_grass =  accepted_parameters["cows_gain_from_grass"].item()
    cows_gain_from_trees =  accepted_parameters["cows_gain_from_trees"].item()
    cows_gain_from_scrub =  accepted_parameters["cows_gain_from_scrub"].item()
    cows_gain_from_saplings =  accepted_parameters["cows_gain_from_saplings"].item()
    cows_gain_from_young_scrub =  accepted_parameters["cows_gain_from_young_scrub"].item()
    fallow_deer_reproduce =  accepted_parameters["fallow_deer_reproduce"].item()
    fallow_deer_gain_from_grass =  accepted_parameters["fallow_deer_gain_from_grass"].item()
    fallow_deer_gain_from_trees =  accepted_parameters["fallow_deer_gain_from_trees"].item()
    fallow_deer_gain_from_scrub =  accepted_parameters["fallow_deer_gain_from_scrub"].item()
    fallow_deer_gain_from_saplings =  accepted_parameters["fallow_deer_gain_from_saplings"].item()
    fallow_deer_gain_from_young_scrub =  accepted_parameters["fallow_deer_gain_from_young_scrub"] .item()  
    red_deer_reproduce =  accepted_parameters["red_deer_reproduce"].item()
    red_deer_gain_from_grass =  accepted_parameters["red_deer_gain_from_grass"].item()
    red_deer_gain_from_trees =  accepted_parameters["red_deer_gain_from_trees"].item()
    red_deer_gain_from_scrub =  accepted_parameters["red_deer_gain_from_scrub"].item()
    red_deer_gain_from_saplings =  accepted_parameters["red_deer_gain_from_saplings"].item()
    red_deer_gain_from_young_scrub =  accepted_parameters["red_deer_gain_from_young_scrub"].item()
    tamworth_pig_reproduce =  accepted_parameters["tamworth_pig_reproduce"].item()
    tamworth_pig_gain_from_grass =  accepted_parameters["tamworth_pig_gain_from_grass"].item()
    tamworth_pig_gain_from_trees = accepted_parameters["tamworth_pig_gain_from_trees"].item()
    tamworth_pig_gain_from_scrub = accepted_parameters["tamworth_pig_gain_from_scrub"].item()
    tamworth_pig_gain_from_saplings =  accepted_parameters["tamworth_pig_gain_from_saplings"].item()
    tamworth_pig_gain_from_young_scrub =  accepted_parameters["tamworth_pig_gain_from_young_scrub"].item()

    european_bison_reproduce = 0
    # bison should have higher impact than any other consumer
    european_bison_gain_from_grass =  0
    european_bison_gain_from_trees =0
    european_bison_gain_from_scrub =0
    european_bison_gain_from_saplings = 0
    european_bison_gain_from_young_scrub = 0  
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
    # stocking values
    initial_roe = 12
    fallowDeer_stocking = 247
    cattle_stocking = 81
    redDeer_stocking = 35
    tamworthPig_stocking = 7
    exmoor_stocking = 15
    # forecasting
    fallowDeer_stocking_forecast = int(247 + (x[0]*247))
    cattle_stocking_forecast = int(81 + (x[1]*81))
    redDeer_stocking_forecast =  int(35 + (x[2]*35))
    tamworthPig_stocking_forecast =  int(7 + (x[3]*7))
    exmoor_stocking_forecast = int(15 + (x[4]*15))
    
    introduced_species_stocking_forecast = 0
    # tree mortality
    chance_scrub_saves_saplings = accepted_parameters["chance_scrub_saves_saplings"].item()

    random.seed(1)
    np.random.seed(1)

    # run the model
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
                        max_time = 485, reintroduction = True, introduce_euroBison = False, introduce_elk = True, introduce_reindeer = False)


    model.reset_randomizer(seed=1)

    model.run_model()

    # remember the results of the model (dominant conditions, # of agents)
    results = model.datacollector.get_model_vars_dataframe()

    # target 10% grassland
    filtered_result = (
        # pre-reintro model
        ((((list(results.loc[results['Time'] == 484, 'Grassland'])[0])-10)/10)**2)
        )

    # only print the last year's result if it's reasonably close to the filters
    if filtered_result < 1:
        print("r:", filtered_result)
        with pd.option_context('display.max_columns',None):
            just_nodes = results[results['Time'] == 484]
            print(just_nodes[["Time", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"]])
    else:
        print("n:", filtered_result)
    # return the output
    return filtered_result
   


def run_optimizer():
    # Define the bounds
    bds = np.array([
        [-1,2],[-1,2],[-1,2],[-1,2],[-1,2]])
        # [0,0],[0,0],[0,0],[0,0],[-0,0]])

    # popsize and maxiter are defined at the top of the page, was 10x100
    algorithm_param = {'max_num_iteration':5,
                    'population_size':50,\
                    'mutation_probability':0.1,\
                    'elit_ratio': 0.01,\
                    'crossover_probability': 0.5,\
                    'parents_portion': 0.3,\
                    'crossover_type':'uniform',\
                    'max_iteration_without_improv': 8}


    optimization =  ga(function = objectiveFunction, dimension = 5, variable_type = 'real',variable_boundaries= bds, algorithm_parameters = algorithm_param, function_timeout=6000)
    optimization.run()
    outputs = list(optimization.output_dict["variable"]) + [(optimization.output_dict["function"])]
    # return excel with rows = output values and number of filters passed
    pd.DataFrame(outputs).to_excel('stocking_density_outputs.xlsx', header=False, index=False)
    return optimization.output_dict



def graph_results():

    output_parameters = run_optimizer()

    accepted_parameters = pd.read_csv('combined_accepted_parameters.csv') 
    accepted_parameters.drop(['Unnamed: 0'], axis=1, inplace=True)
    # accepted_parameters = accepted_parameters.iloc[11:12]

    final_results_list = []

    for _, row in accepted_parameters.iterrows():

        chance_reproduceSapling = row["chance_reproduceSapling"]
        chance_reproduceYoungScrub =  row["chance_reproduceYoungScrub"]
        chance_regrowGrass =  row["chance_regrowGrass"]
        chance_saplingBecomingTree =  row["chance_saplingBecomingTree"]
        chance_youngScrubMatures =  row["chance_youngScrubMatures"]
        chance_scrubOutcompetedByTree =  row["chance_scrubOutcompetedByTree"]
        chance_grassOutcompetedByTree =  row["chance_grassOutcompetedByTree"]
        chance_grassOutcompetedByScrub = row["chance_grassOutcompetedByScrub"]

        initial_roe = 12
        fallowDeer_stocking = 247
        cattle_stocking = 81
        redDeer_stocking = 35
        tamworthPig_stocking = 7
        exmoor_stocking = 15

        roe_deer_reproduce = row["roe_deer_reproduce"]
        roe_deer_gain_from_grass =  row["roe_deer_gain_from_grass"]
        roe_deer_gain_from_trees =  row["roe_deer_gain_from_trees"]
        roe_deer_gain_from_scrub =  row["roe_deer_gain_from_scrub"]
        roe_deer_gain_from_saplings =  row["roe_deer_gain_from_saplings"]
        roe_deer_gain_from_young_scrub =  row["roe_deer_gain_from_young_scrub"]
        ponies_gain_from_grass =  row["ponies_gain_from_grass"]
        ponies_gain_from_trees =  row["ponies_gain_from_trees"]
        ponies_gain_from_scrub =  row["ponies_gain_from_scrub"]
        ponies_gain_from_saplings =  row["ponies_gain_from_saplings"]
        ponies_gain_from_young_scrub =  row["ponies_gain_from_young_scrub"]
        cattle_reproduce =  row["cattle_reproduce"]
        cows_gain_from_grass =  row["cows_gain_from_grass"]
        cows_gain_from_trees =  row["cows_gain_from_trees"]
        cows_gain_from_scrub =  row["cows_gain_from_scrub"]
        cows_gain_from_saplings =  row["cows_gain_from_saplings"]
        cows_gain_from_young_scrub =  row["cows_gain_from_young_scrub"]
        fallow_deer_reproduce =  row["fallow_deer_reproduce"]
        fallow_deer_gain_from_grass =  row["fallow_deer_gain_from_grass"]
        fallow_deer_gain_from_trees =  row["fallow_deer_gain_from_trees"]
        fallow_deer_gain_from_scrub =  row["fallow_deer_gain_from_scrub"]
        fallow_deer_gain_from_saplings =  row["fallow_deer_gain_from_saplings"]
        fallow_deer_gain_from_young_scrub =  row["fallow_deer_gain_from_young_scrub"]   
        red_deer_reproduce =  row["red_deer_reproduce"]
        red_deer_gain_from_grass =  row["red_deer_gain_from_grass"]
        red_deer_gain_from_trees =  row["red_deer_gain_from_trees"]
        red_deer_gain_from_scrub =  row["red_deer_gain_from_scrub"]
        red_deer_gain_from_saplings =  row["red_deer_gain_from_saplings"]
        red_deer_gain_from_young_scrub =  row["red_deer_gain_from_young_scrub"]
        tamworth_pig_reproduce =  row["tamworth_pig_reproduce"]
        tamworth_pig_gain_from_grass =  row["tamworth_pig_gain_from_grass"]
        tamworth_pig_gain_from_trees = row["tamworth_pig_gain_from_trees"]
        tamworth_pig_gain_from_scrub = row["tamworth_pig_gain_from_scrub"]
        tamworth_pig_gain_from_saplings =  row["tamworth_pig_gain_from_saplings"]
        tamworth_pig_gain_from_young_scrub =  row["tamworth_pig_gain_from_young_scrub"]


        # euro bison parameters
        european_bison_reproduce = 0
        # bison should have higher impact than any other consumer
        european_bison_gain_from_grass =  0
        european_bison_gain_from_trees =0
        european_bison_gain_from_scrub =0
        european_bison_gain_from_saplings = 0
        european_bison_gain_from_young_scrub = 0  
        # euro elk parameters
        european_elk_reproduce = 0
        # bison should have higher impact than any other consumer
        european_elk_gain_from_grass =  0
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
        fallowDeer_stocking_forecast = int(247 + (output_parameters["variable"][0]*247))
        cattle_stocking_forecast = int(81 + (output_parameters["variable"][1]*81))
        redDeer_stocking_forecast =  int(35 + (output_parameters["variable"][2]*35))
        tamworthPig_stocking_forecast =  int(7 + (output_parameters["variable"][3]*7))
        exmoor_stocking_forecast = int(15 + (output_parameters["variable"][4]*15))
        introduced_species_stocking_forecast = 0
        chance_scrub_saves_saplings = row["chance_scrub_saves_saplings"]

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
                            max_time = 485, reintroduction = True, introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)


        model.reset_randomizer(seed=1)

        model.run_model()

        results = model.datacollector.get_model_vars_dataframe()
        final_results_list.append(results)


    # append to dataframe
    forecasting = pd.concat(final_results_list)

    palette=['#009e73', '#f0e442', '#0072b2','#cc79a7']

    # graph that
    final_df =  pd.DataFrame(
                    (forecasting[["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland","Woodland", "Thorny Scrub","Bare ground"]].values.flatten()), columns=['Abundance %'])
    final_df["Time"] = pd.DataFrame(np.concatenate([np.repeat(forecasting['Time'], 10)], axis=0))
    final_df["Ecosystem Element"] = pd.DataFrame(np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs","Grassland", "Woodland", "Thorny Scrub", "Bare ground"], len(forecasting)))

    # calculate median 
    m = final_df.groupby(['Time', 'Ecosystem Element'])[['Abundance %']].apply(np.median)
    m.name = 'Median'
    final_df = final_df.join(m, on=['Time','Ecosystem Element'])
    # calculate quantiles - try graphing smaller percentiles on top 
    perc1 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(1) 
    perc1.name = 'onehundperc'
    final_df = final_df.join(perc1, on=['Time', 'Ecosystem Element'])
    perc2 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(0) 
    perc2.name = "zeroperc"
    final_df = final_df.join(perc2, on=['Time', 'Ecosystem Element'])
    # now show more quantiles, 95th
    perc3 = final_df.groupby(['Time',  'Ecosystem Element'])['Abundance %'].quantile(0.975) 
    perc3.name = 'ninetyfiveperc'
    final_df = final_df.join(perc3, on=['Time',  'Ecosystem Element'])
    perc4 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(0.025)
    perc4.name = "fiveperc"
    final_df = final_df.join(perc4, on=['Time', 'Ecosystem Element'])
    # and 80th
    perc5 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(0.9)
    perc5.name = 'eightyperc'
    final_df = final_df.join(perc5, on=['Time',  'Ecosystem Element'])
    perc6 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(0.1)
    perc6.name = "twentyperc"
    final_df = final_df.join(perc6, on=['Time', 'Ecosystem Element'])

    final_df = final_df.reset_index(drop=True)
    final_df.to_csv("stocking_experiment.csv")


graph_results()