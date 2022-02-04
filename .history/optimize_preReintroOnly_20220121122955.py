# ------ Optimization of the Knepp ABM model --------
from KneppModel_ABM import KneppModel 
import numpy as np
import pandas as pd
from geneticalgorithm import geneticalgorithm as ga
import seaborn as sns
import matplotlib.pyplot as plt

# ------ Optimization of the Knepp ABM model --------
def objectiveFunction(x):

    # define the parameters
    chance_reproduceSapling = x[0] 
    chance_reproduceYoungScrub = x[1] 
    chance_regrowGrass = x[2] 
    chance_saplingBecomingTree = x[3]
    chance_youngScrubMatures = x[4]
    chance_scrubOutcompetedByTree = x[5] 
    chance_grassOutcompetedByTree = x[6]
    chance_grassOutcompetedByScrub =  x[7]
    chance_saplingOutcompetedByTree = x[8] 
    chance_saplingOutcompetedByScrub = x[9] 
    chance_youngScrubOutcompetedByScrub = x[10] 
    chance_youngScrubOutcompetedByTree = x[11] 
    # initial values
    initial_roeDeer = 0.12
    initial_grassland = 0.8
    initial_woodland = 0.14
    initial_scrubland = 0.01
    roeDeer_reproduce = x[12] 
    roeDeer_gain_from_grass = x[13] 
    roeDeer_gain_from_Trees = x[14] 
    roeDeer_gain_from_Scrub = x[15] 
    roeDeer_gain_from_Saplings = x[16] 
    roeDeer_gain_from_YoungScrub = x[17] 
    fallowDeer_reproduce = 0
    fallowDeer_gain_from_grass = 0.01
    fallowDeer_gain_from_Trees = 0.01
    fallowDeer_gain_from_Scrub = 0.01
    fallowDeer_gain_from_Saplings =0.01
    fallowDeer_gain_from_YoungScrub = 0.01
    redDeer_reproduce = 0
    redDeer_gain_from_grass = 0.01
    redDeer_gain_from_Trees =0.01
    redDeer_gain_from_Scrub = 0.01
    redDeer_gain_from_Saplings = 0.01
    redDeer_gain_from_YoungScrub = 0.01
    ponies_gain_from_grass = 0.01
    ponies_gain_from_Trees = 0.01
    ponies_gain_from_Scrub = 0.01
    ponies_gain_from_Saplings = 0.01 
    ponies_gain_from_YoungScrub =0.01
    cows_reproduce =0
    cows_gain_from_grass = 0.01
    cows_gain_from_Trees =0.01
    cows_gain_from_Scrub = 0.01
    cows_gain_from_Saplings =0.01
    cows_gain_from_YoungScrub = 0.01
    pigs_reproduce = 0
    pigs_gain_from_grass =0.01
    pigs_gain_from_Saplings =0.01
    pigs_gain_from_YoungScrub = 0.01
    pigs_gain_from_soil = 0.01
    max_start_saplings = 0.1
    max_start_youngScrub = 0.1

    model = KneppModel(
        chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
        chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
        initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland, 
        roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
        ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
        cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
        fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
        redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
        pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, pigs_gain_from_soil, 
        max_start_saplings, max_start_youngScrub,
        width = 25, height = 18, max_time = 50, reintroduction = False, 
        RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)
    model.run_model()

    # remember the results of the model (dominant conditions, # of agents)
    results = model.datacollector.get_model_vars_dataframe()
    
    # find the middle of each filter
    # if (list(results.loc[results['Time'] == 1, 'Saplings'])[0]) >= (list(results.loc[results['Time'] == 0, 'Saplings'])[0]) and (list(results.loc[results['Time'] == 1, 'Young Scrub'])[0]) >= (list(results.loc[results['Time'] == 0, 'Young Scrub'])[0]):
    filtered_result = (
        # pre-reintro model
        (((list(results.loc[results['Time'] == 49, 'Roe deer'])[0])-23)**2) +
        (((list(results.loc[results['Time'] == 49, 'Grassland'])[0])-70)**2) +
        (((list(results.loc[results['Time'] == 49, 'Thorny Scrub'])[0])-13)**2) +
        (((list(results.loc[results['Time'] == 49, 'Woodland'])[0])-17)**2))
    # else:
    #     filtered_result = (
    #         (((list(results.loc[results['Time'] == 49, 'Saplings'])[0])-(list(results.loc[results['Time'] == 0, 'Saplings'])[0]))**2) +
    #         (((list(results.loc[results['Time'] == 49, 'Young Scrub'])[0])-(list(results.loc[results['Time'] == 0, 'Young Scrub'])[0]))**2))

    if filtered_result < 100:
        with pd.option_context('display.max_columns',None):
            just_nodes = results[results['Time'] == 50]
            print("r:", filtered_result)
            print(just_nodes[["Time", "Roe deer", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"]])
    else:
        print("n:", filtered_result)
    return filtered_result

def run_optimizer():

    # Define bounds
    bds = np.array([
        # habitat repro & growth
        [0.055,0.065],[0.08,0.082],[0.12,0.13],[0.0015,0.0016],[0.008,0.01],
        # habitat competition
        [0.016,0.017], # mature scrub
        [0.65,0.67],[0.65,0.66], # grass
        [0.55,0.69],[0.2,0.3], # saplings
        [0.26,0.28],[0.5,0.55], # young scrub  
        # roe deer parameters
        [0.15,0.2],[0.1,0.2],[0.1,0.15],[0.5,0.75],[0.1,0.25],[0.2,0.5]
    ])
    # chance_saplingBecomingTree = 0.0042
    # chance_youngScrubMatures = 0.0075 [0.0015,0.006],[0.004,0.08],

#  The best solution found:
#  [0.07028645 0.08051435 0.12754197 0.00156164 0.01028124 0.01638776
#  0.67035911 0.65763469 0.68813852 0.34452987 0.29680586 0.54006603
#  0.18857749 0.17336236 0.15385756 0.12136387 0.15609413 0.23389317]

#  Objective function:
#  23.0

    algorithm_param = {'max_num_iteration':1,\
                    'population_size':1,\
                    'mutation_probability':0.1,\
                    'elit_ratio': 0.01,\
                    'crossover_probability': 0.5,\
                    'parents_portion': 0.3,\
                    'crossover_type':'uniform',\
                    'max_iteration_without_improv': None}


    optimization =  ga(function = objectiveFunction, dimension = 18, variable_type = 'real',variable_boundaries= bds, algorithm_parameters = algorithm_param, function_timeout=6000)
    optimization.run()
    with open('optim_outputs_preReintro.txt', 'w') as f:
        print('Optimization_outputs:', optimization.output_dict, file=f)
    print(optimization)

    return optimization.output_dict



def graph_results():
    # output_parameters = run_optimizer()
    chance_reproduceSapling = 0.07028645
    chance_reproduceYoungScrub = 0.08051435
    chance_regrowGrass =0.12754197
    chance_saplingBecomingTree =0.00156164
    chance_youngScrubMatures = 0.01028124 
    chance_scrubOutcompetedByTree = 0.01638776
    chance_grassOutcompetedByTree = 0.67035911
    chance_grassOutcompetedByScrub =  0.65763469
    chance_saplingOutcompetedByTree =0.68813852
    chance_saplingOutcompetedByScrub = 0.34452987
    chance_youngScrubOutcompetedByScrub =0.29680586
    chance_youngScrubOutcompetedByTree =  0.54006603
    # habitats
    # chance_reproduceSapling = output_parameters["variable"][0] 
    # chance_reproduceYoungScrub = output_parameters["variable"][1]
    # chance_regrowGrass = output_parameters["variable"][2]
    # chance_saplingBecomingTree =output_parameters["variable"][3]
    # chance_youngScrubMatures =output_parameters["variable"][4]
    # chance_scrubOutcompetedByTree = output_parameters["variable"][5]
    # chance_grassOutcompetedByTree = output_parameters["variable"][6]
    # chance_grassOutcompetedByScrub =  output_parameters["variable"][7]
    # chance_saplingOutcompetedByTree =output_parameters["variable"][8]
    # chance_saplingOutcompetedByScrub = output_parameters["variable"][9]
    # chance_youngScrubOutcompetedByScrub =output_parameters["variable"][10]
    # chance_youngScrubOutcompetedByTree = output_parameters["variable"][11]
    # initial values
    initial_roeDeer = 0.12
    initial_grassland = 0.8
    initial_woodland = 0.14
    initial_scrubland = 0.01

    roeDeer_reproduce = 0.18857749
    roeDeer_gain_from_grass =  0.17336236
    roeDeer_gain_from_Trees = 0.15385756 
    roeDeer_gain_from_Scrub =0.12136387
    roeDeer_gain_from_Saplings =  0.15609413 
    roeDeer_gain_from_YoungScrub =  0.23389317

    # roeDeer_reproduce = output_parameters["variable"][12]
    # roeDeer_gain_from_grass = output_parameters["variable"][13] 
    # roeDeer_gain_from_Trees = output_parameters["variable"][14]
    # roeDeer_gain_from_Scrub = output_parameters["variable"][15]
    # roeDeer_gain_from_Saplings = output_parameters["variable"][16]
    # roeDeer_gain_from_YoungScrub = output_parameters["variable"][17]

    fallowDeer_reproduce = 0
    fallowDeer_gain_from_grass = 0.01
    fallowDeer_gain_from_Trees = 0.01
    fallowDeer_gain_from_Scrub = 0.01
    fallowDeer_gain_from_Saplings =0.01
    fallowDeer_gain_from_YoungScrub = 0.01
    redDeer_reproduce = 0
    redDeer_gain_from_grass = 0.01
    redDeer_gain_from_Trees =0.01
    redDeer_gain_from_Scrub = 0.01
    redDeer_gain_from_Saplings = 0.01
    redDeer_gain_from_YoungScrub = 0.01
    ponies_gain_from_grass = 0.01
    ponies_gain_from_Trees = 0.01
    ponies_gain_from_Scrub = 0.01
    ponies_gain_from_Saplings = 0.01 
    ponies_gain_from_YoungScrub =0.01
    cows_reproduce =0
    cows_gain_from_grass = 0.01
    cows_gain_from_Trees =0.01
    cows_gain_from_Scrub = 0.01
    cows_gain_from_Saplings =0.01
    cows_gain_from_YoungScrub = 0.01
    pigs_reproduce = 0
    pigs_gain_from_grass =0.01
    pigs_gain_from_Saplings =0.01
    pigs_gain_from_YoungScrub = 0.01
    pigs_gain_from_soil = 0.01
    max_start_saplings = 0.1
    max_start_youngScrub = 0.1

    model = KneppModel(
        chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
        chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
        initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland, 
        roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
        ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
        cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
        fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
        redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
        pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, pigs_gain_from_soil, 
        max_start_saplings, max_start_youngScrub,
        width = 25, height = 18, max_time = 50, reintroduction = False, 
        RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)
    model.run_model()

    # remember the results of the model (dominant conditions, # of agents)
    final_results = model.datacollector.get_model_vars_dataframe()

    # y values - number of trees, scrub, etc. 
    y_values = final_results.drop(['Time', "Bare ground","Grassland", "Woodland", "Thorny Scrub", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub", "Grown saplings", "Grown young scrub", "Outcompeted Grass", "Outcompeted Young Scrub", "Outcompeted Saplings", "Outcompeted Mature Scrub", "Outcompeted Grass-Scrub", "Outcompeted Young Scrub-Scrub", "Outcompeted Saplings-Scrub"], axis=1).values.flatten()        
    # species list. this should be +1 the number of simulations
    species_list = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"], 51) 
    # indices
    indices = np.repeat(final_results['Time'], 12)
    final_df = pd.DataFrame(
    {'Abundance': y_values, 'Ecosystem Element': species_list, 'Time': indices})
    colors = ["#6788ee"]
    # first graph: counterfactual & forecasting
    g = sns.FacetGrid(final_df, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    g.map(sns.lineplot, 'Time', 'Abundance')
    # add subplot titles
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
    axes[11].set_title("Bare ground")

    # stop the plots from overlapping
    g.fig.suptitle("Optimizer Outputs")
    plt.tight_layout()
    plt.savefig('OptimOutputs_PreReintro_numbers.png')
    plt.show()


    # y values
    y_values_conditions = final_results.drop(['Time', "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub", "Grown saplings", "Grown young scrub", "Outcompeted Grass", "Outcompeted Young Scrub", "Outcompeted Saplings", "Outcompeted Mature Scrub", "Outcompeted Grass-Scrub", "Outcompeted Young Scrub-Scrub", "Outcompeted Saplings-Scrub"], axis=1).values.flatten()        
    # species list. this should be +1 the number of simulations
    species_list_conditions = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 51) 
    # indices
    indices_conditions = np.repeat(final_results['Time'], 10)
    final_df_conditions = pd.DataFrame(
    {'Abundance': y_values_conditions, 'Ecosystem Element': species_list_conditions, 'Time': indices_conditions})
    colors = ["#6788ee"]

    # first graph: counterfactual & forecasting
    c = sns.FacetGrid(final_df_conditions, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    c.map(sns.lineplot, 'Time', 'Abundance')
    # add subplot titles
    axes = c.axes.flatten()
    # fill between the quantiles
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
    c.axes[0].vlines(x=50,ymin=6,ymax=40, color='r')
    c.axes[6].vlines(x=50,ymin=49,ymax=90, color='r')
    c.axes[7].vlines(x=50,ymin=7,ymax=27, color='r')
    c.axes[8].vlines(x=50,ymin=1,ymax=21, color='r')
    # stop the plots from overlapping
    c.fig.suptitle("Optimizer Outputs: Number of herbivores, and percentage habitat types")
    plt.tight_layout()
    plt.savefig('OptimOutputs_PreReintro_conditions.png')
    plt.show()



    # what are roe deer eating? 
    roe_food = final_results.drop(['Time', "Bare ground","Grassland", "Woodland", "Thorny Scrub", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Grown saplings", "Grown young scrub", "Outcompeted Grass", "Outcompeted Young Scrub", "Outcompeted Saplings", "Outcompeted Mature Scrub", "Outcompeted Grass-Scrub", "Outcompeted Young Scrub-Scrub", "Outcompeted Saplings-Scrub"], axis=1).values.flatten()        
    # species list. this should be +1 the number of simulations
    food_list = np.tile(["Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], 51) 
    # indices
    indices_food = np.repeat(final_results['Time'], 5)
    final_df_food = pd.DataFrame(
    {'Abundance': roe_food, 'Ecosystem Element': food_list, 'Time': indices_food})
    # first graph: counterfactual & forecasting
    f = sns.FacetGrid(final_df_food, col="Ecosystem Element", palette = colors, col_wrap=3, sharey = True)
    f.map(sns.lineplot, 'Time', 'Abundance')
    # add subplot titles
    axes = f.axes.flatten()
    axes[0].set_title("grass")
    axes[1].set_title("trees")
    axes[2].set_title("scrub")
    axes[3].set_title("saplings")
    axes[4].set_title("young scrub")

    # stop the plots from overlapping
    f.fig.suptitle("Amount of food eaten by roe deer")
    plt.tight_layout()
    plt.savefig('Eaten_Food.png')
    plt.show()




    # habitat deaths - stacked bar charts. what's killing what? 
    stacked_habitats = final_results.drop(['Time', "Bare ground","Grassland", "Woodland", "Thorny Scrub", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grown saplings", "Grown young scrub", "Outcompeted Grass", "Outcompeted Mature Scrub", "Outcompeted Saplings", "Outcompeted Young Scrub", "Outcompeted Grass-Scrub", "Outcompeted Young Scrub-Scrub", "Outcompeted Saplings-Scrub", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten()        
    # list those that grew up (a different form of habitat transition)
    grown_saplings = final_results.drop(['Time', "Bare ground", "Grassland", "Woodland", "Thorny Scrub", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Grown young scrub", "Outcompeted Grass", "Outcompeted Mature Scrub", "Outcompeted Saplings", "Outcompeted Young Scrub", "Outcompeted Grass-Scrub", "Outcompeted Young Scrub-Scrub", "Outcompeted Saplings-Scrub", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten()
    grown_saplings_tiled = np.repeat(grown_saplings, 6)
    grown_youngScrub = final_results.drop(['Time', "Bare ground", "Grassland", "Woodland", "Thorny Scrub", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Grown saplings", "Outcompeted Grass", "Outcompeted Mature Scrub", "Outcompeted Saplings", "Outcompeted Young Scrub", "Outcompeted Grass-Scrub", "Outcompeted Young Scrub-Scrub", "Outcompeted Saplings-Scrub", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten()
    grown_youngScrub_tiled = np.repeat(grown_youngScrub, 6)
    # list those that were outcompeted by trees
    outcompeted_grass = final_results.drop(['Time', "Bare ground", "Grassland", "Woodland", "Thorny Scrub", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Grown saplings", "Grown young scrub", "Outcompeted Mature Scrub", "Outcompeted Saplings", "Outcompeted Young Scrub", "Outcompeted Grass-Scrub", "Outcompeted Young Scrub-Scrub", "Outcompeted Saplings-Scrub", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten()
    outcompeted_grass_tiled = np.repeat(outcompeted_grass, 6)
    # outcompeted_scrub = final_results.drop(['Time', "Bare ground", "Grassland", "Woodland", "Thorny Scrub", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Grown saplings", "Grown young scrub", "Outcompeted Grass", "Outcompeted Saplings", "Outcompeted Young Scrub", "Outcompeted Grass-Scrub", "Outcompeted Young Scrub-Scrub", "Outcompeted Saplings-Scrub", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten() 
    # outcompeted_scrub_tiled = np.repeat(outcompeted_scrub, 6)
    # outcompeted_sapling = final_results.drop(['Time', "Bare ground", "Grassland", "Woodland", "Thorny Scrub", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Grown saplings", "Grown young scrub", "Outcompeted Grass", "Outcompeted Mature Scrub", "Outcompeted Young Scrub", "Outcompeted Grass-Scrub", "Outcompeted Young Scrub-Scrub", "Outcompeted Saplings-Scrub", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten() 
    # outcompeted_sapling_tiled = np.repeat(outcompeted_sapling, 6)


    # outcompeted_grass = final_results.drop(['Time', "Bare ground", "Grassland", "Woodland", "Thorny Scrub", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Grown saplings", "Grown young scrub", "Outcompeted Grass", "Outcompeted Mature Scrub", "Outcompeted Saplings", "Outcompeted Young Scrub", "Outcompeted Grass-Scrub", "Outcompeted Young Scrub-Scrub", "Outcompeted Saplings-Scrub", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten() 
 # stacked_competition = np.tile(["Outcompeted Saplings", "Outcompeted Young Scrub", "Outcompeted Grass-Scrub", "Outcompeted Young Scrub-Scrub", "Outcompeted Saplings-Scrub", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], 51) 

    stacked_eco_element = np.tile(["Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"], 51)
    stacked_time = np.repeat(final_results['Time'], 6)

    # grown_saplings = final_results.drop(['Time', "Bare ground", "Grassland", "Woodland", "Thorny Scrub", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Grown saplings", "Grown young scrub", "Outcompeted Grass", "Outcompeted Mature Scrub", "Outcompeted Saplings", "Outcompeted Young Scrub", "Outcompeted Grass-Scrub", "Outcompeted Young Scrub-Scrub", "Outcompeted Saplings-Scrub", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten()

    # stacked_indices = np.repeat(final_results['Time'], 15)

    final_df_stacked = pd.DataFrame(
    {'Time': stacked_time, 'Ecosystem Element': stacked_eco_element, 'Abundance': stacked_habitats, 'Grown saplings': grown_saplings_tiled, 'Grown Young Scrub': grown_youngScrub_tiled})
    print(final_df_stacked)

    # g = sns.FacetGrid(final_df_stacked, col = 'Abundance', hue = 'Ecosystem Element')
    # g = (g.map(sns.barplot, 'Time', 'Ecosystem Element', ci = None).add_legend())

    # plt.show()

    # grown = sns.FacetGrid(final_df_grown, col="Ecosystem Element", palette = colors, col_wrap=3, sharey = True)
    # grown.map(sns.lineplot, 'Time', 'Abundance')

        # # what's being eaten - by each herbivore
        #                 "Eaten Grass": lambda m: self.count_eaten(m, roeDeer_agent, "grass"),
        #                 "Eaten Trees": lambda m: self.count_eaten(m, roeDeer_agent, "trees"),
        #                 "Eaten Mature Scrub": lambda m: self.count_eaten(m, roeDeer_agent, "scrub"),
        #                 "Eaten Saplings": lambda m: self.count_eaten(m, roeDeer_agent, "saplings"),
        #                 "Eaten Young Scrub": lambda m: self.count_eaten(m, roeDeer_agent, "youngScrub"), 
        #                 # competition by trees
        #                 "Outcompeted Grass": lambda m: self.count_habitats_outcompeted_trees(m, "grass"),
        #                 "Outcompeted Mature Scrub": lambda m: self.count_habitats_outcompeted_trees(m, "scrub"),
        #                 "Outcompeted Saplings": lambda m: self.count_habitats_outcompeted_trees(m, "saplings"),
        #                 "Outcompeted Young Scrub": lambda m: self.count_habitats_outcompeted_trees(m, "youngScrub"), 
        #                 # competition by scrub
        #                 "Outcompeted Grass-Scrub": lambda m: self.count_habitats_outcompeted_scrub(m, "grass"),
        #                 "Outcompeted Saplings-Scrub": lambda m: self.count_habitats_outcompeted_scrub(m, "saplings"),
        #                 "Outcompeted Young Scrub-Scrub": lambda m: self.count_habitats_outcompeted_scrub(m, "youngScrub"), 
        #                 # death by growing up (saplings, young scrub)
        #                 "Grown saplings": lambda m: self.count_habitats_grew(m, "saplings"),
        #                 "Grown young scrub": lambda m: self.count_habitats_grew(m, "youngScrub")



    # how many habitats are dying by growing up?
    grown_habitats = final_results.drop(['Time', "Bare ground","Grassland", "Woodland", "Thorny Scrub", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub", "Outcompeted Grass", "Outcompeted Young Scrub", "Outcompeted Saplings", "Outcompeted Mature Scrub", "Outcompeted Grass-Scrub", "Outcompeted Young Scrub-Scrub", "Outcompeted Saplings-Scrub"], axis=1).values.flatten()        
    # species list. this should be +1 the number of simulations
    grown_list = np.tile(["Grown saplings", "Grown young scrub"], 51) 
    # indices
    indices_grown = np.repeat(final_results['Time'], 2)
    final_df_grown = pd.DataFrame(
    {'Abundance': grown_habitats, 'Ecosystem Element': grown_list, 'Time': indices_grown})
    # first graph: counterfactual & forecasting
    grown = sns.FacetGrid(final_df_grown, col="Ecosystem Element", palette = colors, col_wrap=3, sharey = True)
    grown.map(sns.lineplot, 'Time', 'Abundance')
    # add subplot titles
    axes = grown.axes.flatten()
    axes[0].set_title("saplings")
    axes[1].set_title("young scrub")
    # stop the plots from overlapping
    grown.fig.suptitle("Habitats that grew up")
    plt.tight_layout()
    plt.savefig('Grown_habitats.png')
    plt.show()

   # how many habitats are dying by competition with trees
    outcompeted_habitats = final_results.drop(['Time', "Bare ground","Grassland", "Woodland", "Thorny Scrub", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub", "Grown saplings", "Grown young scrub", "Outcompeted Grass-Scrub", "Outcompeted Young Scrub-Scrub", "Outcompeted Saplings-Scrub"], axis=1).values.flatten()        
    # species list. this should be +1 the number of simulations
    outcompeted_list = np.tile(["Outcompeted Grass", "Outcompeted Mature Scrub", "Outcompeted Saplings", "Outcompeted Young Scrub"], 51) 
    # indices
    indices_outcompeted = np.repeat(final_results['Time'], 4)
    final_df_outcompeted = pd.DataFrame(
    {'Abundance': outcompeted_habitats, 'Ecosystem Element': outcompeted_list, 'Time': indices_outcompeted})
    # first graph: counterfactual & forecasting
    outcompeted = sns.FacetGrid(final_df_outcompeted, col="Ecosystem Element", palette = colors, col_wrap=3, sharey = True)
    outcompeted.map(sns.lineplot, 'Time', 'Abundance')
    # add subplot titles
    axes = outcompeted.axes.flatten()
    axes[0].set_title("grass")
    axes[1].set_title("mature scrub")
    axes[2].set_title("saplings")
    axes[3].set_title("young scrub")
    # stop the plots from overlapping
    outcompeted.fig.suptitle("Habitats that were outcompeted by trees")
    plt.tight_layout()
    plt.savefig('Outcompeted_habitats_trees.png')
    plt.show()


   # how many habitats are dying by competition with scrub
    outcompeted_habitats_scrub = final_results.drop(['Time', "Bare ground","Grassland", "Woodland", "Thorny Scrub", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub", "Grown saplings", "Grown young scrub", "Outcompeted Grass", "Outcompeted Mature Scrub", "Outcompeted Saplings", "Outcompeted Young Scrub"], axis=1).values.flatten()        
    # species list. this should be +1 the number of simulations
    outcompeted_list_scrub = np.tile(["Outcompeted Grass-Scrub", "Outcompeted Young Scrub-Scrub", "Outcompeted Saplings-Scrub"], 51) 
    # indices
    indices_outcompeted_scrub = np.repeat(final_results['Time'], 3)
    final_df_outcompeted_scrub = pd.DataFrame(
    {'Abundance': outcompeted_habitats_scrub, 'Ecosystem Element': outcompeted_list_scrub, 'Time': indices_outcompeted_scrub})
    # first graph: counterfactual & forecasting
    outcompeted_scrub = sns.FacetGrid(final_df_outcompeted_scrub, col="Ecosystem Element", palette = colors, col_wrap=3, sharey = True)
    outcompeted_scrub.map(sns.lineplot, 'Time', 'Abundance')
    # add subplot titles
    axes = outcompeted_scrub.axes.flatten()
    axes[0].set_title("grass")
    axes[1].set_title("saplings")
    axes[2].set_title("young scrub")
    # stop the plots from overlapping
    outcompeted_scrub.fig.suptitle("Habitats that were outcompeted by scrub")
    plt.tight_layout()
    plt.savefig('Outcompeted_habitats_scrub.png')
    plt.show()

    # # # # # # REALITY CHECKS # # # # # # 


    # 0. What happens if I run it for 1k steps?
    reality_check_0 = KneppModel(
        chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
        chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
        initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland, 
        roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
        ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
        cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
        fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
        redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
        pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, pigs_gain_from_soil,
        max_start_saplings, max_start_youngScrub,
        width = 25, height = 18, max_time = 2500, reintroduction = False, 
        RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)
    reality_check_0.run_model()
    results_reality0 = reality_check_0.datacollector.get_model_vars_dataframe()
    
    # first lets look at the number of individual trees, scrub,e tc. 
    y_values_reality0 = results_reality0.drop(['Time', "Grassland", "Woodland", "Thorny Scrub", "Bare ground", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten()
    species_list_ages = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"], 2501) 
    indices_list_ages = np.repeat(results_reality0['Time'], 12)
    final_df_reality0 = pd.DataFrame(
    {'Abundance': y_values_reality0, 'Ecosystem Element': species_list_ages, 'Time': indices_list_ages})
    # and graph it
    g_rc0 = sns.FacetGrid(final_df_reality0, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    g_rc0.map(sns.lineplot, 'Time', 'Abundance')
    axes = g_rc0.axes.flatten()
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
    axes[11].set_title("Bare ground")
    g_rc0.fig.suptitle('Reality check: Simulate far into the future')
    plt.tight_layout()
    plt.savefig('RealityCheck_run1k_preReintro_numbers.png')
    plt.show()


    # now let's look at the habitat conditions (% of total area)
    y_values_reality01 = results_reality0.drop(['Time', "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten()
    species_list_ages1 = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 2501) 
    indices_list_ages1 = np.repeat(results_reality0['Time'], 10)
    final_df_reality01 = pd.DataFrame(
    {'Abundance': y_values_reality01, 'Ecosystem Element': species_list_ages1, 'Time': indices_list_ages1})
    # and graph it
    g_rc01 = sns.FacetGrid(final_df_reality01, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    g_rc01.map(sns.lineplot, 'Time', 'Abundance')
    axes = g_rc01.axes.flatten()
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

    g_rc01.axes[0].vlines(x=50,ymin=6,ymax=40, color='r')
    g_rc01.axes[6].vlines(x=50,ymin=49,ymax=90, color='r')
    g_rc01.axes[7].vlines(x=50,ymin=7,ymax=27, color='r')
    g_rc01.axes[8].vlines(x=50,ymin=1,ymax=21, color='r')
    # stop the plots from overlapping
    g_rc01.fig.suptitle('Reality check: Simulate far into the future')
    plt.tight_layout()
    plt.savefig('RealityCheck_run1k_preReintro_conditions.png')
    plt.show()





    # # 1. Do roe deer die in the absence of food? 
    # no_regrowing_grass = 0
    # no_grassland = 0
    # no_woodland = 0
    # no_scrubland = 0

    # reality_check_1 = KneppModel(
    #     chance_reproduceSapling, chance_reproduceYoungScrub, no_regrowing_grass, chance_saplingBecomingTree, chance_youngScrubMatures, 
    #     chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
    #     initial_roeDeer, no_grassland, no_woodland, no_scrubland, 
    #     roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
    #     ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
    #     cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
    #     fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
    #     redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
    #     pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
    #     width = 25, height = 18, max_time = 50, reintroduction = False, 
    #     RC1_noFood = True, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)
    # reality_check_1.run_model()
    # results_reality1 = reality_check_1.datacollector.get_model_vars_dataframe()
    # # y values
    # y_values_reality1 = results_reality1.drop(['Time', "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten()
    # final_df_reality1 = pd.DataFrame(
    # {'Abundance': y_values_reality1, 'Ecosystem Element': species_list_conditions, 'Time': indices_conditions})
    # # first graph: counterfactual & forecasting
    # g_rc1 = sns.FacetGrid(final_df_reality1, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    # g_rc1.map(sns.lineplot, 'Time', 'Abundance')
    # # add subplot titles
    # axes = g_rc1.axes.flatten()
    # # fill between the quantiles
    # axes[0].set_title("Roe deer")
    # axes[1].set_title("Exmoor pony")
    # axes[2].set_title("Fallow deer")
    # axes[3].set_title("Longhorn cattle")
    # axes[4].set_title("Red deer")
    # axes[5].set_title("Tamworth pigs")
    # axes[6].set_title("Grassland")
    # axes[7].set_title("Woodland")
    # axes[8].set_title("Thorny scrub")
    # axes[9].set_title("Bare ground")
    # # stop the plots from overlapping
    # g_rc1.fig.suptitle('Reality check: No food for herbivores')
    # plt.tight_layout()
    # plt.savefig('RealityCheck_noFoodForHerbivores_preReintro.png')
    # plt.show()
    


    # # 2. What if there's no competition for grassland (no thorny scrub or trees)? 
    # reality_check_2 = KneppModel(
    #     chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
    #     chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
    #     initial_roeDeer, initial_grassland, no_woodland, no_scrubland, 
    #     roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
    #     ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
    #     cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
    #     fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
    #     redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
    #     pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
    #     width = 25, height = 18, max_time = 50, reintroduction = False, 
    #     RC1_noFood = False, RC2_noTreesScrub = True, RC3_noTrees = False, RC4_noScrub = False)
    # reality_check_2.run_model()
    # results_reality2 = reality_check_2.datacollector.get_model_vars_dataframe()
    # # y values
    # y_values_reality2 = results_reality2.drop(['Time', "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten()
    # final_df_reality2 = pd.DataFrame(
    # {'Abundance': y_values_reality2, 'Ecosystem Element': species_list_conditions, 'Time': indices_conditions})
    # # first graph: counterfactual & forecasting
    # g_rc3 = sns.FacetGrid(final_df_reality2, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    # g_rc3.map(sns.lineplot, 'Time', 'Abundance')
    # # add subplot titles
    # axes = g_rc3.axes.flatten()
    # # fill between the quantiles
    # axes[0].set_title("Roe deer")
    # axes[1].set_title("Exmoor pony")
    # axes[2].set_title("Fallow deer")
    # axes[3].set_title("Longhorn cattle")
    # axes[4].set_title("Red deer")
    # axes[5].set_title("Tamworth pigs")
    # axes[6].set_title("Grassland")
    # axes[7].set_title("Woodland")
    # axes[8].set_title("Thorny scrub")
    # axes[9].set_title("Bare ground")
    # # stop the plots from overlapping
    # g_rc3.fig.suptitle('Reality check: No competition for grassland')
    # plt.tight_layout()
    # plt.savefig('RealityCheck_noCompetitionForGrass_preReintro.png')
    # plt.show()



    # # 3. No competition for scrub (no trees)? 
    # reality_check_4 = KneppModel(
    #     chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
    #     chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
    #     initial_roeDeer, initial_grassland, no_woodland, initial_scrubland, 
    #     roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
    #     ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
    #     cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
    #     fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
    #     redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
    #     pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
    #     width = 25, height = 18, max_time = 50, reintroduction = False, 
    #     RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = True, RC4_noScrub = False)

    # reality_check_4.run_model()
    # results_reality4 = reality_check_4.datacollector.get_model_vars_dataframe()
    # # y values
    # y_values_reality4 = results_reality4.drop(['Time', "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten()

    # final_df_reality4 = pd.DataFrame(
    # {'Abundance': y_values_reality4, 'Ecosystem Element': species_list_conditions, 'Time': indices_conditions})
    # # first graph: counterfactual & forecasting
    # g_rc4 = sns.FacetGrid(final_df_reality4, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    # g_rc4.map(sns.lineplot, 'Time', 'Abundance')
    # # add subplot titles
    # axes = g_rc4.axes.flatten()
    # # fill between the quantiles
    # axes[0].set_title("Roe deer")
    # axes[1].set_title("Exmoor pony")
    # axes[2].set_title("Fallow deer")
    # axes[3].set_title("Longhorn cattle")
    # axes[4].set_title("Red deer")
    # axes[5].set_title("Tamworth pigs")
    # axes[6].set_title("Grassland")
    # axes[7].set_title("Woodland")
    # axes[8].set_title("Thorny scrub")
    # axes[9].set_title("Bare ground")
    # # stop the plots from overlapping
    # g_rc4.fig.suptitle('Reality check: No competition for scrubland')
    # plt.tight_layout()
    # plt.savefig('RealityCheck_noCompetitionForScrub_preReintro.png')
    # plt.show()




    # # 4. No facilitation for tree saplings (no scrub)?
    # reality_check_5 = KneppModel(
    #     chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
    #     chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
    #     initial_roeDeer, initial_grassland, initial_woodland, no_scrubland, 
    #     roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
    #     ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
    #     cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
    #     fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
    #     redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
    #     pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
    #     width = 25, height = 18, max_time = 50, reintroduction = False,
    #     RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = True)
    # reality_check_5.run_model()
    # results_reality5 = reality_check_5.datacollector.get_model_vars_dataframe()
    # # y values
    # y_values_reality5 = results_reality5.drop(['Time', "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten()
    # final_df_reality5 = pd.DataFrame(
    # {'Abundance': y_values_reality5, 'Ecosystem Element': species_list_conditions, 'Time': indices_conditions})
    # # first graph: counterfactual & forecasting
    # g_rc5 = sns.FacetGrid(final_df_reality5, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    # g_rc5.map(sns.lineplot, 'Time', 'Abundance')
    # # add subplot titles
    # axes = g_rc5.axes.flatten()
    # # fill between the quantiles
    # axes[0].set_title("Roe deer")
    # axes[1].set_title("Exmoor pony")
    # axes[2].set_title("Fallow deer")
    # axes[3].set_title("Longhorn cattle")
    # axes[4].set_title("Red deer")
    # axes[5].set_title("Tamworth pigs")
    # axes[6].set_title("Grassland")
    # axes[7].set_title("Woodland")
    # axes[8].set_title("Thorny scrub")
    # axes[9].set_title("Bare ground")
    # # stop the plots from overlapping
    # g_rc5.fig.suptitle('Reality check: No facilitation for woodland (scrub = 0)')
    # plt.tight_layout()
    # plt.savefig('RealityCheck_noFacilitation_preReintro.png')
    # plt.show()


    # 5. What happens to habitats if there are no herbivores?
    no_roe = 0
    reality_check_6 = KneppModel(
        chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
        chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
        no_roe, initial_grassland, initial_woodland, initial_scrubland, 
        roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
        ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
        cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
        fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
        redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
        pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, pigs_gain_from_soil, 
        max_start_saplings, max_start_youngScrub,
        width = 25, height = 18, max_time = 2500, reintroduction = False,
        RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)

    reality_check_6.run_model()
    results_reality6 = reality_check_6.datacollector.get_model_vars_dataframe()
    # y values
    y_values_reality6 = results_reality6.drop(['Time', "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten()
    final_df_reality6 = pd.DataFrame(
    {'Abundance': y_values_reality6, 'Ecosystem Element': species_list_ages1, 'Time': indices_list_ages1})
    # first graph: counterfactual & forecasting
    g_rc6 = sns.FacetGrid(final_df_reality6, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    g_rc6.map(sns.lineplot, 'Time', 'Abundance')
    # add subplot titles
    axes = g_rc6.axes.flatten()
    # fill between the quantiles
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
    # stop the plots from overlapping
    g_rc6.fig.suptitle('Reality check: No herbivores (conditions)')
    plt.tight_layout()
    plt.savefig('RealityCheck_noHerbivores_preReintro_conditions.png')
    plt.show()


    y_values_reality61 = results_reality6.drop(['Time', "Grassland", "Woodland", "Thorny Scrub", "Bare ground", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten()
    final_df_reality61 = pd.DataFrame(
    {'Abundance': y_values_reality61, 'Ecosystem Element': species_list_ages, 'Time': indices_list_ages})
    # and graph it
    g_rc61 = sns.FacetGrid(final_df_reality61, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    g_rc61.map(sns.lineplot, 'Time', 'Abundance')
    axes = g_rc61.axes.flatten()
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
    axes[11].set_title("Bare ground")
    g_rc61.fig.suptitle('Reality check: No Herbivores')
    plt.tight_layout()
    plt.savefig('RealityCheck_noHerbivores_preReintro.png')
    plt.show()


graph_results()