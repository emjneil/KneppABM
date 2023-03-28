# ------ Optimization of the Knepp ABM model --------
from model import KneppModel 
import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution
import seaborn as sns
import matplotlib.pyplot as plt
import sys

# ------ Optimization of the Knepp ABM model --------


popsize, maxiter = 50,50

def updt(total, progress, extra=""):
     # Print a progress bar. Original source: https://stackoverflow.com/a/15860757/1391441
    barLength, status = 20, ""
    progress = float(progress) / float(total) 
    if progress >= 1.:
        progress, status = 1, "\r\n"
    block = int(round(barLength * progress))
    text = "\r[{}] {:.0f}% {}{}".format(
        "#" * block + "-" * (barLength - block),
        round(progress * 100, 0), extra, status)
    sys.stdout.write(text)
    sys.stdout.flush()

def objectiveFunction(x, info):
    # this will update the progress bar
    updt(popsize * (maxiter + 1) * len(x), info['Nfeval'] + 1)
    info['Nfeval'] += 1

   
    # define the parameters (12)
    chance_reproduceSapling = x[0]
    chance_reproduceYoungScrub =x[1]
    chance_regrowGrass =x[2]
    chance_saplingBecomingTree =x[3]
    chance_youngScrubMatures =x[4]
    chance_scrubOutcompetedByTree = x[5]
    chance_grassOutcompetedByTree =x[6]
    chance_grassOutcompetedByScrub =x[7]
    chance_saplingOutcompetedByTree =x[8]
    chance_saplingOutcompetedByScrub =x[9]
    chance_youngScrubOutcompetedByScrub = x[10]
    chance_youngScrubOutcompetedByTree =x[11]

    # initial values
    roe_deer_reproduce =x[12]
    roe_deer_gain_from_grass =x[13]
    roe_deer_gain_from_trees = x[14]
    roe_deer_gain_from_scrub = x[15]
    roe_deer_gain_from_saplings = x[16]
    roe_deer_gain_from_young_scrub = x[17]
    fallow_deer_reproduce = x[18]
    fallow_deer_gain_from_grass = x[19]
    fallow_deer_gain_from_trees = x[20]
    fallow_deer_gain_from_scrub = x[21]
    fallow_deer_gain_from_saplings = x[22]
    fallow_deer_gain_from_young_scrub = x[23]
    red_deer_reproduce = x[24]
    red_deer_gain_from_grass = x[25]
    red_deer_gain_from_trees = x[26]
    red_deer_gain_from_scrub = x[27]
    red_deer_gain_from_saplings = x[28]
    red_deer_gain_from_young_scrub = x[29]
    ponies_gain_from_grass = x[30]
    ponies_gain_from_trees = x[31]
    ponies_gain_from_scrub = x[32]
    ponies_gain_from_saplings = x[33]
    ponies_gain_from_young_scrub = x[34]
    cattle_reproduce = x[35]
    cows_gain_from_grass = x[36]
    cows_gain_from_trees = x[37]
    cows_gain_from_scrub = x[38]
    cows_gain_from_saplings = x[39]
    cows_gain_from_young_scrub = x[40]
    tamworth_pig_reproduce = x[41]
    tamworth_pig_gain_from_grass =x[42]
    tamworth_pig_gain_from_trees = x[43]
    tamworth_pig_gain_from_scrub = x[44]
    tamworth_pig_gain_from_saplings =x[45]
    tamworth_pig_gain_from_young_scrub = x[46]
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
    # stocking values
    initial_roe = 12
    fallowDeer_stocking = 247
    cattle_stocking = 81
    redDeer_stocking = 35
    tamworthPig_stocking = 7
    exmoor_stocking = 15
    # forecasting
    fallowDeer_stocking_forecast = 86
    cattle_stocking_forecast = 76
    redDeer_stocking_forecast = 21
    tamworthPig_stocking_forecast = 7
    exmoor_stocking_forecast = 15
    roeDeer_stocking_forecast = 12
    introduced_species_stocking_forecast = 0

    # run the model
    model = KneppModel(initial_roe, roe_deer_reproduce, roe_deer_gain_from_saplings, roe_deer_gain_from_trees, roe_deer_gain_from_scrub, roe_deer_gain_from_young_scrub, roe_deer_gain_from_grass,
                        chance_youngScrubMatures, chance_saplingBecomingTree, chance_reproduceSapling,chance_reproduceYoungScrub, chance_regrowGrass, 
                        chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_scrubOutcompetedByTree, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByTree, chance_youngScrubOutcompetedByScrub, 
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
                        max_time = 184, reintroduction = True, introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)

    model.run_model()

    # remember the results of the model (dominant conditions, # of agents)
    results = model.datacollector.get_model_vars_dataframe()
    
    # find the middle of each filter
    # find the middle of each filter
    filtered_result = (
        # pre-reintro model
        ((((list(results.loc[results['Time'] == 49, 'Roe deer'])[0])-26)/26)**2) +
        ((((list(results.loc[results['Time'] == 49, 'Grassland'])[0])-58.4)/58.4)**2) +
        ((((list(results.loc[results['Time'] == 49, 'Thorny Scrub'])[0])-12.7)/12.7)**2) +
        ((((list(results.loc[results['Time'] == 49, 'Woodland'])[0])-11.4)/11.4)**2) +
        # # March 2016
        ((((list(results.loc[results['Time'] == 133, 'Fallow deer'])[0])-140)/140)**2) +
        ((((list(results.loc[results['Time'] == 133, 'Red deer'])[0])-26)/26)**2) +
        ((((list(results.loc[results['Time'] == 133, 'Tamworth pigs'])[0])-9)/9)**2) +
        ((((list(results.loc[results['Time'] == 133, 'Longhorn cattle'])[0])-86)/86)**2) +
        ((((list(results.loc[results['Time'] == 133, 'Exmoor pony'])[0])-11)/11)**2) +
        # # March 2017
        ((((list(results.loc[results['Time'] == 145, 'Fallow deer'])[0])-165)/165)**2) +
        ((((list(results.loc[results['Time'] == 145, 'Longhorn cattle'])[0])-79)/79)**2) +
        ((((list(results.loc[results['Time'] == 145, 'Tamworth pigs'])[0])-7)/7)**2) +
        ((((list(results.loc[results['Time'] == 145, 'Exmoor pony'])[0])-10)/10)**2) +
        # March 2018
        ((((list(results.loc[results['Time'] == 157, 'Red deer'])[0])-24)/24)**2) +
        ((((list(results.loc[results['Time'] == 157, 'Longhorn cattle'])[0])-88)/88)**2) +
        ((((list(results.loc[results['Time'] == 157, 'Tamworth pigs'])[0])-16)/16)**2) +
        ((((list(results.loc[results['Time'] == 157, 'Exmoor pony'])[0])-9)/9)**2) +
        # # March 2019
        ((((list(results.loc[results['Time'] == 169, 'Fallow deer'])[0])-278)/278)**2) +
        ((((list(results.loc[results['Time'] == 169, 'Red deer'])[0])-37)/37)**2) +
        ((((list(results.loc[results['Time'] == 169, 'Longhorn cattle'])[0])-87)/87)**2) +
        ((((list(results.loc[results['Time'] == 169, 'Tamworth pigs'])[0])-9)/9)**2) +
        # March 2020
        ((((list(results.loc[results['Time'] == 181, 'Fallow deer'])[0])-247)/247)**2) +
        ((((list(results.loc[results['Time'] == 181, 'Red deer'])[0])-35)/35)**2) +
        ((((list(results.loc[results['Time'] == 181, 'Tamworth pigs'])[0])-7)/7)**2) +
        ((((list(results.loc[results['Time'] == 181, 'Longhorn cattle'])[0])-81)/81)**2) +
        # May 2020
        ((((list(results.loc[results['Time'] == 183, 'Exmoor pony'])[0])-15)/15)**2) +
        ((((list(results.loc[results['Time'] == 183, 'Tamworth pigs'])[0])-19)/19)**2) +
        ((((list(results.loc[results['Time'] == 183, 'Longhorn cattle'])[0])-81)/81)**2) +
        ((((list(results.loc[results['Time'] == 183, 'Roe deer'])[0])-50)/50)**2) +
        ((((list(results.loc[results['Time'] == 183, 'Grassland'])[0])-26.8)/26.8)**2) +
        ((((list(results.loc[results['Time'] == 183, 'Thorny Scrub'])[0])-51.8)/51.8)**2) +
        ((((list(results.loc[results['Time'] == 183, 'Woodland'])[0])-21.5)/21.5)**2)      
         )


    # only print the last year's result if it's reasonably close to the filters
    if filtered_result < 2:
        print("r:", filtered_result)
        with pd.option_context('display.max_columns',None):
            just_nodes = results[results['Time'] == 183]
            print(just_nodes[["Time", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"]])
    else:
        print("n:", int(filtered_result))
    # return the output
    return filtered_result
   

def run_optimizer():
    # Define the bounds
    bds = [
        (0,1),(0,1),(0,1),(0.0017,0.0083),(0.0024,0.028),
        (0,1), # mature scrub competition
        (0,1),(0,1), # grass
        (0,1),(0,1), # saplings
        (0,1),(0,1), # young scrub 
        # roe deer parameters
        (0,0.5),(0,1),(0,1),(0,1),(0,0.5),(0,0.5),
        # fallow deer parameters
        (0,0.5),(0,1),(0,1),(0,1),(0,0.5),(0,0.5),
        # red deer
        (0,0.5),(0,1),(0,1),(0,1),(0,0.5),(0,0.5),
        # exmoor pony parameters
                (0,1),(0,1),(0,1),(0,0.5),(0,0.5),
        # cattle parameters
        (0,0.5),(0,1),(0,1),(0,1),(0,0.5),(0,0.5),
        # pig parameters
        (0,0.5),(0,1),(0,1),(0,1),(0,0.5),(0,0.5)]


    # popsize and maxiter are defined at the top of the page
    optimization = differential_evolution(objectiveFunction, bounds = bds, popsize = popsize, seed = 0, maxiter = maxiter, polish=False, args=({'Nfeval': 0},))

    # save the results to a txt file
    with open('/Users/emilyneil/Desktop/KneppABM/outputs/post_reintro/differentialEvolution_outputs.txt', 'w') as f:
        print('Differential Evolution Outputs:', optimization, file=f)
    print(optimization)
    return optimization.x



def graph_results():
    output_parameters = run_optimizer()

    # define the parameters
    initial_roe = 12
    chance_reproduceSapling = output_parameters[0]
    chance_reproduceYoungScrub = output_parameters[1]
    chance_regrowGrass =output_parameters[2]
    chance_saplingBecomingTree =output_parameters[3]
    chance_youngScrubMatures =output_parameters[4]
    chance_scrubOutcompetedByTree =output_parameters[5]
    chance_grassOutcompetedByTree =output_parameters[6]
    chance_grassOutcompetedByScrub =output_parameters[7]
    chance_saplingOutcompetedByTree =output_parameters[8]
    chance_saplingOutcompetedByScrub = output_parameters[9]
    chance_youngScrubOutcompetedByScrub = output_parameters[10]
    chance_youngScrubOutcompetedByTree =output_parameters[11]
    # consumer values
    roe_deer_reproduce =output_parameters[12]
    roe_deer_gain_from_grass =output_parameters[13]
    roe_deer_gain_from_trees =output_parameters[14]
    roe_deer_gain_from_scrub = output_parameters[15]
    roe_deer_gain_from_saplings = output_parameters[16]
    roe_deer_gain_from_young_scrub = output_parameters[17]
    fallow_deer_reproduce = output_parameters[18]
    fallow_deer_gain_from_grass = output_parameters[19]
    fallow_deer_gain_from_trees = output_parameters[20]
    fallow_deer_gain_from_scrub = output_parameters[21]
    fallow_deer_gain_from_saplings = output_parameters[22]
    fallow_deer_gain_from_young_scrub = output_parameters[23]
    red_deer_reproduce = output_parameters[24]
    red_deer_gain_from_grass = output_parameters[25]
    red_deer_gain_from_trees = output_parameters[26]
    red_deer_gain_from_scrub = output_parameters[27]
    red_deer_gain_from_saplings = output_parameters[28]
    red_deer_gain_from_young_scrub = output_parameters[29]
    ponies_gain_from_grass = output_parameters[30]
    ponies_gain_from_trees = output_parameters[31]
    ponies_gain_from_scrub = output_parameters[32]
    ponies_gain_from_saplings = output_parameters[33]
    ponies_gain_from_young_scrub = output_parameters[34]
    cattle_reproduce = output_parameters[35]
    cows_gain_from_grass = output_parameters[36]
    cows_gain_from_trees = output_parameters[37]
    cows_gain_from_scrub = output_parameters[38]
    cows_gain_from_saplings = output_parameters[39]
    cows_gain_from_young_scrub = output_parameters[40]
    tamworth_pig_reproduce = output_parameters[41]
    tamworth_pig_gain_from_grass =output_parameters[42]
    tamworth_pig_gain_from_trees = output_parameters[43]
    tamworth_pig_gain_from_scrub = output_parameters[44]
    tamworth_pig_gain_from_saplings = output_parameters[45]
    tamworth_pig_gain_from_young_scrub = output_parameters[46]
    # stocking values
    fallowDeer_stocking = 247
    cattle_stocking = 81
    redDeer_stocking = 35
    tamworthPig_stocking = 7
    exmoor_stocking = 15
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
    # forecasting
    fallowDeer_stocking_forecast = 86
    cattle_stocking_forecast = 76
    redDeer_stocking_forecast = 21
    tamworthPig_stocking_forecast = 7
    exmoor_stocking_forecast = 15
    roeDeer_stocking_forecast = 12
    introduced_species_stocking_forecast = 0
    final_results_list = []
    run_number = 0
    number_simulations = 10

    for _ in range(number_simulations):
        # keep track of the runs 
        run_number += 1
        print(run_number)
        model = KneppModel(initial_roe, roe_deer_reproduce, roe_deer_gain_from_saplings, roe_deer_gain_from_trees, roe_deer_gain_from_scrub, roe_deer_gain_from_young_scrub, roe_deer_gain_from_grass,
                        chance_youngScrubMatures, chance_saplingBecomingTree, chance_reproduceSapling,chance_reproduceYoungScrub, chance_regrowGrass, 
                        chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_scrubOutcompetedByTree, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByTree, chance_youngScrubOutcompetedByScrub, 
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
                        max_time = 184, reintroduction = True, introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)

        model.run_model()

        # first graph:  does it pass the filters? looking at the number of individual trees, etc.
        results = model.datacollector.get_model_vars_dataframe()
        final_results_list.append(results)

    final_results = pd.concat(final_results_list)
    final_results.to_excel('final_results_DE.xlsx')

    # y values - number of trees, scrub, etc. 
    y_values = final_results[["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"]].values.flatten()
    species_list = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"], 185*number_simulations) 
    indices = np.repeat(final_results['Time'], 12)

    final_df = pd.DataFrame(
    {'Abundance': y_values, 'Ecosystem Element': species_list, 'Time': indices})

    # calculate median 
    m = final_df.groupby(['Time', 'Ecosystem Element'])[['Abundance']].apply(np.median)
    m.name = 'Median'
    final_df = final_df.join(m, on=['Time', 'Ecosystem Element'])
    # calculate quantiles
    perc1 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance'].quantile(.95)
    perc1.name = 'ninetyfivePerc'
    final_df = final_df.join(perc1, on=['Time', 'Ecosystem Element'])
    perc2 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance'].quantile(.05)
    perc2.name = "fivePerc"
    final_df = final_df.join(perc2, on=['Time','Ecosystem Element'])
    final_df = final_df.reset_index(drop=True)

    colors = ["#6788ee"]
    g = sns.FacetGrid(final_df, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    g.map(sns.lineplot, 'Time', 'Median')
    g.map(sns.lineplot, 'Time', 'fivePerc')
    g.map(sns.lineplot, 'Time', 'ninetyfivePerc')    # add subplot titles
    for ax in g.axes.flat:
        ax.fill_between(ax.lines[1].get_xdata(),ax.lines[1].get_ydata(), ax.lines[2].get_ydata(), color="#6788ee", alpha=0.2)
        ax.set_ylabel('Abundance')
    axes = g.axes.flatten()
    # fill between the quantiles
    axes = g.axes.flatten()
    axes[0].set_title("Roe deer")
    axes[1].set_title("Exmoor pony")
    axes[2].set_title("Fallow deer")
    axes[3].set_title("Longhorn cattle")
    axes[4].set_title("Red deer")
    axes[5].set_title("Tamworth pigs")
    axes[6].set_title("Grass")
    axes[7].set_title("Mature Trees")
    axes[8].set_title("Mature Scrub")
    axes[9].set_title("Saplings")
    axes[10].set_title("Young Scrub")
    axes[11].set_title("Bare Areas")
    # stop the plots from overlapping
    g.fig.suptitle("Optimizer Outputs")
    plt.tight_layout()
    plt.savefig('optimizer_outputs_numbers_DE.png')
    plt.show()


    # does it pass the filters - conditions?
    y_values_conditions =  final_results[["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"]].values.flatten()            
    # species list. this should be +1 the number of simulations
    species_list_conditions = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 185*number_simulations) 
    # indices
    indices_conditions = np.repeat(final_results['Time'], 10)
    final_df_condit = pd.DataFrame(
    {'Abundance': y_values_conditions, 'Ecosystem Element': species_list_conditions, 'Time': indices_conditions})
    # calculate median 
    m = final_df_condit.groupby(['Time', 'Ecosystem Element'])[['Abundance']].apply(np.median)
    m.name = 'Median'
    final_df_condit = final_df_condit.join(m, on=['Time', 'Ecosystem Element'])
    # calculate quantiles
    perc1 = final_df_condit.groupby(['Time', 'Ecosystem Element'])['Abundance'].quantile(.95)
    perc1.name = 'ninetyfivePerc'
    final_df_condit = final_df_condit.join(perc1, on=['Time', 'Ecosystem Element'])
    perc2 = final_df_condit.groupby(['Time', 'Ecosystem Element'])['Abundance'].quantile(.05)
    perc2.name = "fivePerc"
    final_df_condit = final_df_condit.join(perc2, on=['Time','Ecosystem Element'])
    final_df_condit = final_df_condit.reset_index(drop=True)

    colors = ["#6788ee"]
    # first graph: counterfactual & forecasting
    f = sns.FacetGrid(final_df_condit, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    f.map(sns.lineplot, 'Time', 'Median')
    f.map(sns.lineplot, 'Time', 'fivePerc')
    f.map(sns.lineplot, 'Time', 'ninetyfivePerc')    # add subplot titles
    for ax in f.axes.flat:
        ax.fill_between(ax.lines[1].get_xdata(),ax.lines[1].get_ydata(), ax.lines[2].get_ydata(), color="#6788ee", alpha=0.2)
        ax.set_ylabel('Abundance')
    axes = f.axes.flatten()
    # fill between the quantiles
    axes = f.axes.flatten()
    axes[0].set_title("Roe deer")
    axes[1].set_title("Exmoor pony")
    axes[2].set_title("Fallow deer")
    axes[3].set_title("Longhorn cattle")
    axes[4].set_title("Red deer")
    axes[5].set_title("Tamworth pigs")
    axes[6].set_title("Grassland")
    axes[7].set_title("Woodland")
    axes[8].set_title("Thorny scrub")
    axes[9].set_title("Bare ground")
    # add filter lines
    f.axes[0].vlines(x=50,ymin=6,ymax=40, color='r')
    f.axes[6].vlines(x=50,ymin=16.8,ymax=89.9, color='r')
    f.axes[7].vlines(x=50,ymin=5.8,ymax=17, color='r')
    f.axes[8].vlines(x=50,ymin=4.3,ymax=21, color='r')
    f.axes[1].vlines(x=123,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=123,ymin=90,ymax=140, color='r')
    f.axes[5].vlines(x=123,ymin=12,ymax=32, color='r')
    # May 2015
    f.axes[3].vlines(x=124,ymin=104,ymax=154, color='r')
    f.axes[5].vlines(x=124,ymin=4,ymax=24, color='r')
    f.axes[1].vlines(x=124,ymin=9,ymax=11, color='r')
    # June 2015
    f.axes[3].vlines(x=125,ymin=104,ymax=154, color='r')
    f.axes[1].vlines(x=125,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=125,ymin=4,ymax=24, color='r')
    # July 2015
    f.axes[3].vlines(x=126,ymin=104,ymax=154, color='r')
    f.axes[1].vlines(x=126,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=126,ymin=4,ymax=24, color='r')
    # Aug 2015
    f.axes[3].vlines(x=127,ymin=104,ymax=154, color='r')
    f.axes[1].vlines(x=127,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=127,ymin=4,ymax=24, color='r')
    # Sept 2015
    f.axes[3].vlines(x=128,ymin=105,ymax=155, color='r')
    f.axes[1].vlines(x=128,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=128,ymin=4,ymax=24, color='r')
    # Oct 2015
    f.axes[3].vlines(x=129,ymin=66,ymax=116, color='r')
    f.axes[1].vlines(x=129,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=129,ymin=4,ymax=24, color='r')
    # Nov 2015
    f.axes[3].vlines(x=130,ymin=66,ymax=116, color='r')
    f.axes[1].vlines(x=130,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=130,ymin=3,ymax=23, color='r')
    # Dec 2015
    f.axes[3].vlines(x=131,ymin=61,ymax=111, color='r')
    f.axes[1].vlines(x=131,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=131,ymin=3,ymax=23, color='r')
    # Jan 2016
    f.axes[3].vlines(x=132,ymin=61,ymax=111, color='r')
    f.axes[1].vlines(x=132,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=132,ymin=1,ymax=20, color='r')
    # Feb 2016
    f.axes[1].vlines(x=133,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=133,ymin=61,ymax=111, color='r')
    f.axes[5].vlines(x=133,ymin=1,ymax=20, color='r')
    # March 2016
    f.axes[1].vlines(x=134,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=134,ymin=61,ymax=111, color='r')
    f.axes[2].vlines(x=134,ymin=90,ymax=190, color='r')
    f.axes[4].vlines(x=134,ymin=21,ymax=31, color='r')
    f.axes[5].vlines(x=134,ymin=1,ymax=19, color='r')
    # April 2016
    f.axes[1].vlines(x=135,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=135,ymin=78,ymax=128, color='r')
    f.axes[5].vlines(x=135,ymin=1,ymax=19, color='r')
    # May 2016
    f.axes[1].vlines(x=136,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=136,ymin=83,ymax=133, color='r')
    f.axes[5].vlines(x=136,ymin=7,ymax=27, color='r')
    # June 2016
    f.axes[1].vlines(x=137,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=137,ymin=64,ymax=114, color='r')
    f.axes[5].vlines(x=137,ymin=7,ymax=27, color='r')
    # July 2016
    f.axes[1].vlines(x=138,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=138,ymin=62,ymax=112, color='r')
    f.axes[5].vlines(x=138,ymin=7,ymax=27, color='r')
    # Aug 2016
    f.axes[1].vlines(x=139,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=139,ymin=62,ymax=112, color='r')
    f.axes[5].vlines(x=139,ymin=7,ymax=27, color='r')
    # Sept 2016
    f.axes[1].vlines(x=140,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=140,ymin=72,ymax=122, color='r')
    f.axes[5].vlines(x=140,ymin=7,ymax=27, color='r')
    # Oct 2016
    f.axes[1].vlines(x=141,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=141,ymin=72,ymax=122, color='r')
    f.axes[5].vlines(x=141,ymin=7,ymax=27, color='r')
    # Nov 2016
    f.axes[1].vlines(x=142,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=142,ymin=67,ymax=117, color='r')
    f.axes[5].vlines(x=142,ymin=7,ymax=27, color='r')
    # Dec 2016
    f.axes[1].vlines(x=143,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=143,ymin=54,ymax=104, color='r')
    f.axes[5].vlines(x=143,ymin=3,ymax=23, color='r')
    # Jan 2017
    f.axes[1].vlines(x=144,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=144,ymin=54,ymax=104, color='r')
    f.axes[5].vlines(x=144,ymin=1,ymax=19, color='r')
    # Feb 2017
    f.axes[1].vlines(x=145,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=145,ymin=54,ymax=104, color='r')
    f.axes[5].vlines(x=145,ymin=1,ymax=17, color='r')
    # March 2017
    f.axes[1].vlines(x=146,ymin=9,ymax=11, color='r')
    f.axes[2].vlines(x=146,ymin=115,ymax=200, color='r')
    f.axes[3].vlines(x=146,ymin=54,ymax=104, color='r')
    f.axes[5].vlines(x=146,ymin=1,ymax=17, color='r')
    # April 2017
    f.axes[1].vlines(x=147,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=147,ymin=75,ymax=125, color='r')
    f.axes[5].vlines(x=147,ymin=12,ymax=32, color='r')
    # May 2017
    f.axes[1].vlines(x=148,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=148,ymin=84,ymax=134, color='r')
    f.axes[5].vlines(x=148,ymin=12,ymax=32, color='r')
    # June 2017
    f.axes[1].vlines(x=149,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=149,ymin=69,ymax=119, color='r')
    f.axes[5].vlines(x=149,ymin=12,ymax=32, color='r')
    # July 2017
    f.axes[1].vlines(x=150,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=150,ymin=69,ymax=119, color='r')
    f.axes[5].vlines(x=150,ymin=12,ymax=32, color='r')
    # Aug 2017
    f.axes[1].vlines(x=151,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=151,ymin=69,ymax=119, color='r')
    f.axes[5].vlines(x=151,ymin=12,ymax=32, color='r')
    # Sept 2017
    f.axes[1].vlines(x=152,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=152,ymin=65,ymax=115, color='r')
    f.axes[5].vlines(x=152,ymin=20,ymax=24, color='r')
    # Oct 2017
    f.axes[1].vlines(x=153,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=153,ymin=63,ymax=113, color='r')
    f.axes[5].vlines(x=153,ymin=12,ymax=32, color='r')
    # Nov 2017
    f.axes[1].vlines(x=154,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=154,ymin=63,ymax=113, color='r')
    f.axes[5].vlines(x=154,ymin=12,ymax=32, color='r')
    # Dec 2017
    f.axes[1].vlines(x=155,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=155,ymin=63,ymax=113, color='r')
    f.axes[5].vlines(x=155,ymin=8,ymax=28, color='r')
    # Jan 2018
    f.axes[1].vlines(x=156,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=156,ymin=63,ymax=113, color='r')
    f.axes[5].vlines(x=156,ymin=1,ymax=21, color='r')
    # Feb 2018
    f.axes[1].vlines(x=157,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=157,ymin=63,ymax=113, color='r')
    f.axes[5].vlines(x=157,ymin=6,ymax=26, color='r')
    # March 2018
    f.axes[1].vlines(x=158,ymin=8,ymax=10, color='r')
    f.axes[3].vlines(x=158,ymin=63,ymax=113, color='r')
    f.axes[4].vlines(x=158,ymin=19,ymax=29, color='r')
    f.axes[5].vlines(x=158,ymin=6,ymax=26, color='r')
    # April 2018
    f.axes[1].vlines(x=159,ymin=8,ymax=10, color='r')
    f.axes[3].vlines(x=159,ymin=76,ymax=126, color='r')
    f.axes[5].vlines(x=159,ymin=6,ymax=26, color='r')
    # May 2018
    f.axes[1].vlines(x=160,ymin=8,ymax=10, color='r')
    f.axes[3].vlines(x=160,ymin=92,ymax=142, color='r')
    f.axes[5].vlines(x=160,ymin=13,ymax=33, color='r')
    # June 2018
    f.axes[1].vlines(x=161,ymin=8,ymax=10, color='r')
    f.axes[3].vlines(x=161,ymin=78,ymax=128, color='r')
    f.axes[5].vlines(x=161,ymin=13,ymax=33, color='r')
    # July 2018
    f.axes[1].vlines(x=162,ymin=8,ymax=10, color='r')
    f.axes[3].vlines(x=162,ymin=78,ymax=128, color='r')
    f.axes[5].vlines(x=162,ymin=12,ymax=32, color='r')
    # Aug 2018
    f.axes[3].vlines(x=163,ymin=77,ymax=127, color='r')
    f.axes[5].vlines(x=163,ymin=12,ymax=32, color='r')
    # Sept 2018
    f.axes[3].vlines(x=164,ymin=81,ymax=131, color='r')
    f.axes[5].vlines(x=164,ymin=12,ymax=32, color='r')
    # Oct 2018
    f.axes[3].vlines(x=165,ymin=76,ymax=126, color='r')
    f.axes[5].vlines(x=165,ymin=11,ymax=31, color='r')
    # Nov 2018
    f.axes[3].vlines(x=166,ymin=68,ymax=118, color='r')
    f.axes[5].vlines(x=166,ymin=1,ymax=19, color='r')
    # Dec 2018
    f.axes[3].vlines(x=167,ymin=64,ymax=114, color='r')
    f.axes[5].vlines(x=167,ymin=1,ymax=19, color='r')
    # Jan 2019
    f.axes[3].vlines(x=168,ymin=64,ymax=114, color='r')
    f.axes[5].vlines(x=168,ymin=1,ymax=19, color='r')
    # Feb 2019
    f.axes[3].vlines(x=169,ymin=62,ymax=112, color='r')
    f.axes[5].vlines(x=169,ymin=1,ymax=20, color='r')
    # March 2019
    f.axes[2].vlines(x=170,ymin=253,ymax=303, color='r')
    f.axes[3].vlines(x=170,ymin=62,ymax=112, color='r')
    f.axes[4].vlines(x=170,ymin=32,ymax=42, color='r')
    f.axes[5].vlines(x=170,ymin=1,ymax=19, color='r')
    # April 2019
    f.axes[3].vlines(x=171,ymin=76,ymax=126, color='r')
    f.axes[5].vlines(x=171,ymin=1,ymax=18, color='r')
    # May 2019
    f.axes[3].vlines(x=172,ymin=85,ymax=135, color='r')
    f.axes[5].vlines(x=172,ymin=1,ymax=18, color='r')
    # June 2019
    f.axes[3].vlines(x=173,ymin=64,ymax=114, color='r')
    f.axes[5].vlines(x=173,ymin=1,ymax=18, color='r')
    # July 2019
    f.axes[3].vlines(x=174,ymin=66,ymax=116, color='r')
    f.axes[5].vlines(x=174,ymin=1,ymax=19, color='r')
    # Aug 2019
    f.axes[3].vlines(x=175,ymin=66,ymax=116, color='r')
    f.axes[5].vlines(x=175,ymin=1,ymax=19, color='r')  
    # Sept 2019
    f.axes[3].vlines(x=176,ymin=68,ymax=118, color='r')
    f.axes[5].vlines(x=176,ymin=1,ymax=19, color='r')
    # Oct 2019
    f.axes[3].vlines(x=177,ymin=63,ymax=113, color='r')
    f.axes[5].vlines(x=177,ymin=1,ymax=19, color='r')
    # Nov 2019
    f.axes[3].vlines(x=178,ymin=62,ymax=112, color='r')
    f.axes[5].vlines(x=178,ymin=1,ymax=19, color='r')
    # Dec 2019
    f.axes[3].vlines(x=179,ymin=55,ymax=105, color='r')
    f.axes[5].vlines(x=179,ymin=1,ymax=20, color='r')
    # Jan 2020
    f.axes[3].vlines(x=180,ymin=55,ymax=105, color='r')
    f.axes[5].vlines(x=180,ymin=1,ymax=20, color='r')
    # Feb 2020
    f.axes[3].vlines(x=181,ymin=54,ymax=104, color='r')
    f.axes[5].vlines(x=181,ymin=1,ymax=18, color='r')
    # March 2020
    f.axes[2].vlines(x=182,ymin=222,ymax=272, color='r')
    f.axes[4].vlines(x=182,ymin=30,ymax=40, color='r')
    f.axes[3].vlines(x=182,ymin=56,ymax=106, color='r')
    f.axes[5].vlines(x=182,ymin=1,ymax=17, color='r')
    # April 2020
    f.axes[1].vlines(x=183,ymin=14,ymax=17, color='r')
    f.axes[3].vlines(x=183,ymin=56,ymax=106, color='r')
    f.axes[5].vlines(x=183,ymin=1,ymax=17, color='r')
    # plot next set of filter lines
    f.axes[0].vlines(x=184,ymin=20,ymax=80, color='r')
    f.axes[1].vlines(x=184,ymin=14,ymax=17, color='r')
    f.axes[3].vlines(x=184,ymin=56,ymax=106, color='r')
    f.axes[5].vlines(x=184,ymin=9,ymax=29, color='r')
    f.axes[6].vlines(x=184,ymin=16.8,ymax=36.8, color='r')
    f.axes[7].vlines(x=184,ymin=16.5,ymax=26.5, color='r')
    f.axes[8].vlines(x=184,ymin=41.8,ymax=61.8, color='r')
    # stop the plots from overlapping
    f.fig.suptitle("Optimizer Outputs")
    plt.tight_layout()
    plt.savefig('optimizer_outputs_conditions_DE.png')
    plt.show()



graph_results()