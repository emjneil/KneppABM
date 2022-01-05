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
    chance_saplingBecomingTree = 0.0042
    chance_youngScrubMatures = 0.0075

    chance_scrubOutcompetedByTree = x[3] 
    chance_grassOutcompetedByTree = x[4] 
    chance_grassOutcompetedByScrub = x[5]
    chance_saplingOutcompetedByTree = x[6] 
    chance_saplingOutcompetedByScrub = x[7] 
    chance_youngScrubOutcompetedByScrub = x[8] 
    chance_youngScrubOutcompetedByTree = x[9] 
    # initial values
    initial_roeDeer = 0.12
    initial_grassland = 0.8
    initial_woodland = 0.14
    initial_scrubland = 0.01
    roeDeer_reproduce = x[10] 
    roeDeer_gain_from_grass = x[11] 
    roeDeer_gain_from_Trees = x[12] 
    roeDeer_gain_from_Scrub = x[13] 
    roeDeer_gain_from_Saplings = x[14] 
    roeDeer_gain_from_YoungScrub = x[15] 
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
    max_start_saplings = x[16]
    max_start_youngScrub = x[17]

    model = KneppModel(
        chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
        chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
        initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland, 
        roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
        ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
        cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
        fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
        redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
        pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
        max_start_saplings, max_start_youngScrub,
        width = 50, height = 36, max_time = 50, reintroduction = False, 
        RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)
    model.run_model()

    # remember the results of the model (dominant conditions, # of agents)
    results = model.datacollector.get_model_vars_dataframe()
    
    # find the middle of each filter
    if (list(results.loc[results['Time'] == 1, 'Saplings'])[0]) >= (list(results.loc[results['Time'] == 0, 'Saplings'])[0]) and (list(results.loc[results['Time'] == 1, 'Young Scrub'])[0]) >= (list(results.loc[results['Time'] == 0, 'Young Scrub'])[0]):
        filtered_result = (
            # pre-reintro model
            (((list(results.loc[results['Time'] == 49, 'Roe deer'])[0])-23)**2) +
            (((list(results.loc[results['Time'] == 49, 'Grassland'])[0])-70)**2) +
            (((list(results.loc[results['Time'] == 49, 'Thorny Scrub'])[0])-13)**2) +
            (((list(results.loc[results['Time'] == 49, 'Woodland'])[0])-17)**2))
            # (((list(results.loc[results['Time'] == 184, 'Roe deer'])[0])-40)**2))
    else:
        filtered_result = (
            (((list(results.loc[results['Time'] == 49, 'Saplings'])[0])-(list(results.loc[results['Time'] == 0, 'Saplings'])[0]))**2) +
            (((list(results.loc[results['Time'] == 49, 'Young Scrub'])[0])-(list(results.loc[results['Time'] == 0, 'Young Scrub'])[0]))**2))

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
        [0.75,1],[0.75,1],[0.2,0.5],
        # [0.0035,0.005],[0.005,0.01],
        # habitat competition
        [0.001,0.004],[0.75,1],[0.75,1],[0.9,1],[0.1,0.2],[0.15,0.35],[0.9,1],     
        # roe deer parameters
        [0.15,0.25],[0.01,0.25],[0.025,0.25],[0.025,0.25],[0.005,0.025],[0.005,0.025],
        # starting conditions for saplings and young scrub     
        [0.1,0.5],[0.1,0.5]
    ])

#  The best solution found:
#  [0.17285622 0.27738208 0.03444647 0.00479091 0.0058205  0.00095767
#  0.05973459 0.06092576 0.16474949 0.12017726 0.16120201 0.21980398
#  0.24136651 0.23519178 0.1526595  0.15925745 0.01129432 0.02149714
#  0.072894   0.06720785]

#  Objective function:
#  4.0

#  The best solution found:                                                                           
#  [3.82981390e-01 3.43314509e-01 3.40067344e-02 4.21949220e-03
#  7.58930878e-03 6.55979076e-04 1.01123935e-01 7.54906513e-02
#  8.47954284e-01 4.30460769e-01 4.03980773e-01 9.62142514e-01
#  1.95478067e-01 1.57700783e-01 6.49264124e-02 6.48546736e-02
#  1.55015717e-02 1.64787819e-02 2.41189674e-02 1.91987780e-02]

#  Objective function:
#  7.0

    algorithm_param = {'max_num_iteration':2,\
                    'population_size':25,\
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
    output_parameters = run_optimizer()

    # habitats
    # chance_reproduceSapling = 0.12
    # chance_reproduceYoungScrub = 0.14
    # chance_regrowGrass = 0.04
    # chance_saplingBecomingTree = 0.0037
    # chance_youngScrubMatures = 0.0068
    # chance_scrubOutcompetedByTree = 0.00051
    # chance_grassOutcompetedByTree = 0.13
    # chance_grassOutcompetedByScrub = 0.055
    # chance_saplingOutcompetedByTree = 0.42
    # chance_saplingOutcompetedByScrub = 0.021
    # chance_youngScrubOutcompetedByScrub = 0.034
    # chance_youngScrubOutcompetedByTree = 0.12

    chance_reproduceSapling = output_parameters["variable"][0]
    chance_reproduceYoungScrub = output_parameters["variable"][1]
    chance_regrowGrass = output_parameters["variable"][2]
    chance_saplingBecomingTree = 0.0042
    chance_youngScrubMatures = 0.0075
    chance_scrubOutcompetedByTree = output_parameters["variable"][3]
    chance_grassOutcompetedByTree = output_parameters["variable"][4]
    chance_grassOutcompetedByScrub = output_parameters["variable"][5]
    chance_saplingOutcompetedByTree = output_parameters["variable"][6]
    chance_saplingOutcompetedByScrub = output_parameters["variable"][7]
    chance_youngScrubOutcompetedByScrub = output_parameters["variable"][8]
    chance_youngScrubOutcompetedByTree = output_parameters["variable"][9]
    # initial values
    initial_roeDeer = 0.12
    initial_grassland = 0.8
    initial_woodland = 0.14
    initial_scrubland = 0.01
    
    # roe deer
    roeDeer_reproduce = output_parameters["variable"][10]
    roeDeer_gain_from_grass = output_parameters["variable"][11]
    roeDeer_gain_from_Trees = output_parameters["variable"][12]
    roeDeer_gain_from_Scrub = output_parameters["variable"][13]
    roeDeer_gain_from_Saplings = output_parameters["variable"][14]
    roeDeer_gain_from_YoungScrub = output_parameters["variable"][15]
    # roeDeer_reproduce = 0.2
    # roeDeer_gain_from_grass = 0.089
    # roeDeer_gain_from_Trees = 0.066
    # roeDeer_gain_from_Scrub = 0.037
    # roeDeer_gain_from_Saplings = 0.0066
    # roeDeer_gain_from_YoungScrub = 0.014

    # Fallow deer
    fallowDeer_reproduce = 0
    fallowDeer_gain_from_grass = 0.01
    fallowDeer_gain_from_Trees = 0.01
    fallowDeer_gain_from_Scrub = 0.01
    fallowDeer_gain_from_Saplings = 0.01
    fallowDeer_gain_from_YoungScrub = 0.01
    # Red deer
    redDeer_reproduce = 0
    redDeer_gain_from_grass = 0.01
    redDeer_gain_from_Trees = 0.01
    redDeer_gain_from_Scrub = 0.01
    redDeer_gain_from_Saplings = 0.01
    redDeer_gain_from_YoungScrub = 0.01
    # Exmoor ponies
    ponies_gain_from_grass = 0.01
    ponies_gain_from_Trees = 0.01
    ponies_gain_from_Scrub = 0.01
    ponies_gain_from_Saplings = 0.01
    ponies_gain_from_YoungScrub = 0.01
    # Longhorn cattle
    cows_reproduce =0
    cows_gain_from_grass =0.01
    cows_gain_from_Trees =0.01
    cows_gain_from_Scrub =0.01
    cows_gain_from_Saplings = 0.01
    cows_gain_from_YoungScrub = 0.01
    # Tamworth pigs
    pigs_reproduce = 0
    pigs_gain_from_grass = 0.01
    pigs_gain_from_Saplings = 0.01
    pigs_gain_from_YoungScrub = 0.01   
    # max_start_saplings = 0.051
    # max_start_youngScrub = 0.13 
    max_start_saplings = output_parameters["variable"][16]
    max_start_youngScrub = output_parameters["variable"][17]

    model = KneppModel(
        chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
        chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
        initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland, 
        roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
        ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
        cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
        fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
        redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
        pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
        max_start_saplings, max_start_youngScrub,
        width = 50, height = 36, max_time = 50, reintroduction = False, 
        RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)
    model.run_model()

    # remember the results of the model (dominant conditions, # of agents)
    final_results = model.datacollector.get_model_vars_dataframe()
    # final_results.to_excel("output.xlsx")


    # y values - number of trees, scrub, etc. 
    y_values = final_results.drop(['Time', "Bare ground","Grassland", "Woodland", "Thorny Scrub", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten()        
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

    # add filter lines
    g.axes[0].vlines(x=50,ymin=6,ymax=40, color='r')
    g.axes[6].vlines(x=50,ymin=49,ymax=90, color='r')
    g.axes[7].vlines(x=50,ymin=7,ymax=27, color='r')
    g.axes[8].vlines(x=50,ymin=1,ymax=21, color='r')
    # stop the plots from overlapping
    g.fig.suptitle("Optimizer Outputs")
    plt.tight_layout()
    plt.savefig('OptimOutputs_PreReintro_numbers.png')
    plt.show()


    # y values
    y_values_conditions = final_results.drop(['Time', "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten()        
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
    roe_food = final_results.drop(['Time', "Bare ground","Grassland", "Woodland", "Thorny Scrub", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"], axis=1).values.flatten()        
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
        pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
        max_start_saplings, max_start_youngScrub,
        width = 50, height = 36, max_time = 2500, reintroduction = False, 
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
    #     width = 50, height = 36, max_time = 50, reintroduction = False, 
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
    #     width = 50, height = 36, max_time = 50, reintroduction = False, 
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
    #     width = 50, height = 36, max_time = 50, reintroduction = False, 
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
    #     width = 50, height = 36, max_time = 50, reintroduction = False,
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
        pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
        max_start_saplings, max_start_youngScrub,
        width = 50, height = 36, max_time = 2500, reintroduction = False,
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