# ------ Optimization of the Knepp ABM model --------
from KneppModel_ABM import KneppModel 
import numpy as np
import pandas as pd
from geneticalgorithm import geneticalgorithm as ga
import seaborn as sns
import matplotlib.pyplot as plt

# ------ Optimization of the Knepp ABM model --------

# have it change the reindeer parameters
# manually change whether it's browser, grazer, or intermediate. Run it once per each and take best result
# if it's not possible to hit the filters with current stocking densities? Optimise those too. 

# grazer -  1 - levels out around 12-15%
#  [0.27995299 0.66148828 0.02037398 0.0590684  0.18684425 0.21771809
#  0.56247843 0.59172031 0.29453923 0.08512734 0.05911069 0.54202918
#  0.3118936 ]


def objectiveFunction(x):
    # habitats
    chance_reproduceSapling = 0.04206406
    chance_reproduceYoungScrub =0.1109531
    chance_regrowGrass = 0.24463218
    chance_saplingBecomingTree = 0.00289472
    chance_youngScrubMatures = 0.00601638
    chance_scrubOutcompetedByTree = 0.03450849
    chance_grassOutcompetedByTree = 0.28874493
    chance_grassOutcompetedByScrub = 0.29790348
    chance_saplingOutcompetedByTree = 0.35425409
    chance_saplingOutcompetedByScrub =0.25885052
    chance_youngScrubOutcompetedByScrub = 0.37929889
    chance_youngScrubOutcompetedByTree = 0.3982258

    # initial values
    initial_roeDeer = 0.12
    initial_grassland = 0.8
    initial_woodland = 0.14
    initial_scrubland = 0.01

    # roe deer
    roeDeer_reproduce = 0.18215313
    roeDeer_gain_from_grass = 0.69330732
    roeDeer_gain_from_Trees = 0.6982617
    roeDeer_gain_from_Scrub = 0.46792347
    roeDeer_gain_from_Saplings =0.14360982
    roeDeer_gain_from_YoungScrub =0.10447744
    # Fallow deer
    fallowDeer_reproduce = 0.28586154
    fallowDeer_gain_from_grass =0.60193723
    fallowDeer_gain_from_Trees = 0.62907582
    fallowDeer_gain_from_Scrub = 0.41669232
    fallowDeer_gain_from_Saplings = 0.13022322
    fallowDeer_gain_from_YoungScrub = 0.07403832
    # Red deer
    redDeer_reproduce = 0.3065381
    redDeer_gain_from_grass = 0.5464753
    redDeer_gain_from_Trees = 0.57759807
    redDeer_gain_from_Scrub = 0.39375145
    redDeer_gain_from_Saplings = 0.11916663
    redDeer_gain_from_YoungScrub = 0.06335441
    # Exmoor ponies
    ponies_gain_from_grass = 0.46791793
    ponies_gain_from_Trees = 0.50082365
    ponies_gain_from_Scrub = 0.34385853
    ponies_gain_from_Saplings = 0.10451826
    ponies_gain_from_YoungScrub =0.05673449
    # Longhorn cattle
    cows_reproduce = 0.20204395
    cows_gain_from_grass = 0.44058728
    cows_gain_from_Trees = 0.45394087
    cows_gain_from_Scrub = 0.2761602
    cows_gain_from_Saplings = 0.08643107
    cows_gain_from_YoungScrub = 0.04245426
    # Tamworth pigs
    pigs_reproduce = 0.33496453
    pigs_gain_from_grass =0.39056552
    pigs_gain_from_Trees = 0.6909069
    pigs_gain_from_Scrub = 0.47493354
    pigs_gain_from_Saplings = 0.07887992
    pigs_gain_from_YoungScrub = 0.08125611
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

    # forecasted stocking densities
    fallowDeer_stocking_forecast = round(x[0]*100)
    cattle_stocking_forecast = round(x[1]*100)
    redDeer_stocking_forecast = round(x[2]*100)
    tamworthPig_stocking_forecast = round(x[3]*100)
    exmoor_stocking_forecast = round(x[4]*100)
    # reindeer parameters
    reproduce_reindeer = 0
    # reindeer should have impacts between red and fallow deer
    reindeer_gain_from_grass = 0
    reindeer_gain_from_Trees =0
    reindeer_gain_from_Scrub =0
    reindeer_gain_from_Saplings = 0
    reindeer_gain_from_YoungScrub = 0
    reindeer_stocking_forecast = 0
    roeDeer_stocking_forecast = round(x[5]*100)

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
        introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False, cull_roe = True)

    model.run_model()

    # remember the results of the model (dominant conditions, # of agents)
    results = model.datacollector.get_model_vars_dataframe()
    
    # find the middle of each filter - 50 years in future
    filtered_result = (
        # (((list(results.loc[results['Time'] == 784, 'Grassland'])[0])-50)**2) +
        # (((list(results.loc[results['Time'] == 784, 'Thorny Scrub'])[0])-25)**2) +
        (((list(results.loc[results['Time'] == 384, 'Woodland'])[0])-35)**2) +
        (((list(results.loc[results['Time'] == 784, 'Woodland'])[0])-35)**2))          


    print("r:", filtered_result)
    with pd.option_context('display.max_columns',None):
        just_nodes = results[results['Time'] == 784]
        print(just_nodes[["Time","Roe deer", "Grassland", "Woodland", "Thorny Scrub", "Bare ground", "Reindeer"]])

    return filtered_result
   

def run_optimizer():

    # Define bounds
    bds = np.array([
        # stocking densities
        # [124,370],[41,122],[18,53],[4,11],[8,23],
        [0.75,3.70],[0.25,1.5],[0.15,0.75],[0.04,0.25],[0.08,0.5],
        # new species growth & impact
        # [0.16,0.25],[0.4,0.76],[0.4,0.76],[0.25,0.52],[0.07,0.15],[0.036,0.11],
        # new species stocking density
        # [0.1,0.5],
        # roe culls
        [0.2,4]
    ])

#      The best solution found:                                                                           
#  [1.00396431 0.61177667 0.19238756 0.1167678  0.1143261  0.26472061]

#  Objective function:
#  410.0

    algorithm_param = {'max_num_iteration': 10,\
                    'population_size':100,\
                    'mutation_probability':0.1,\
                    'elit_ratio': 0.01,\
                    'crossover_probability': 0.5,\
                    'parents_portion': 0.3,\
                    'crossover_type':'uniform',\
                    'max_iteration_without_improv': None}


    optimization =  ga(function = objectiveFunction, dimension = 6, variable_type = 'real',variable_boundaries= bds, algorithm_parameters = algorithm_param, function_timeout=6000)
    optimization.run()
    with open('/Users/emilyneil/Desktop/KneppABM/outputs/experiment_optimization_outputs.txt', 'w') as f:
        print('Experiment_optimization_outputs:', optimization.output_dict, file=f)
    print(optimization)

    return optimization.output_dict




def graph_results():
    output_parameters = run_optimizer()
    # habitats
    chance_reproduceSapling = 0.04206406
    chance_reproduceYoungScrub =0.1109531
    chance_regrowGrass = 0.24463218
    chance_saplingBecomingTree = 0.00289472
    chance_youngScrubMatures = 0.00601638
    chance_scrubOutcompetedByTree = 0.03450849
    chance_grassOutcompetedByTree = 0.28874493
    chance_grassOutcompetedByScrub = 0.29790348
    chance_saplingOutcompetedByTree = 0.35425409
    chance_saplingOutcompetedByScrub =0.25885052
    chance_youngScrubOutcompetedByScrub = 0.37929889
    chance_youngScrubOutcompetedByTree = 0.3982258

    # initial values
    initial_roeDeer = 0.12
    initial_grassland = 0.8
    initial_woodland = 0.14
    initial_scrubland = 0.01

    # roe deer
    roeDeer_reproduce = 0.18215313
    roeDeer_gain_from_grass = 0.69330732
    roeDeer_gain_from_Trees = 0.6982617
    roeDeer_gain_from_Scrub = 0.46792347
    roeDeer_gain_from_Saplings =0.14360982
    roeDeer_gain_from_YoungScrub =0.10447744
    # Fallow deer
    fallowDeer_reproduce = 0.28586154
    fallowDeer_gain_from_grass =0.60193723
    fallowDeer_gain_from_Trees = 0.62907582
    fallowDeer_gain_from_Scrub = 0.41669232
    fallowDeer_gain_from_Saplings = 0.13022322
    fallowDeer_gain_from_YoungScrub = 0.07403832
    # Red deer
    redDeer_reproduce = 0.3065381
    redDeer_gain_from_grass = 0.5464753
    redDeer_gain_from_Trees = 0.57759807
    redDeer_gain_from_Scrub = 0.39375145
    redDeer_gain_from_Saplings = 0.11916663
    redDeer_gain_from_YoungScrub = 0.06335441
    # Exmoor ponies
    ponies_gain_from_grass = 0.46791793
    ponies_gain_from_Trees = 0.50082365
    ponies_gain_from_Scrub = 0.34385853
    ponies_gain_from_Saplings = 0.10451826
    ponies_gain_from_YoungScrub =0.05673449
    # Longhorn cattle
    cows_reproduce = 0.20204395
    cows_gain_from_grass = 0.44058728
    cows_gain_from_Trees = 0.45394087
    cows_gain_from_Scrub = 0.2761602
    cows_gain_from_Saplings = 0.08643107
    cows_gain_from_YoungScrub = 0.04245426
    # Tamworth pigs
    pigs_reproduce = 0.33496453
    pigs_gain_from_grass =0.39056552
    pigs_gain_from_Trees = 0.6909069
    pigs_gain_from_Scrub = 0.47493354
    pigs_gain_from_Saplings = 0.07887992
    pigs_gain_from_YoungScrub = 0.08125611
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

    fallowDeer_stocking_forecast = round(output_parameters["variable"][0]*100)
    cattle_stocking_forecast = round(output_parameters["variable"][1]*100)
    redDeer_stocking_forecast = round(output_parameters["variable"][2]*100)
    tamworthPig_stocking_forecast = round(output_parameters["variable"][3]*100)
    exmoor_stocking_forecast = round(output_parameters["variable"][4]*100)
    # reindeer parameters
    reproduce_reindeer =0
    # reindeer should have impacts between red and fallow deer
    reindeer_gain_from_grass = 0
    reindeer_gain_from_Trees =0
    reindeer_gain_from_Scrub =0
    reindeer_gain_from_Saplings = 0
    reindeer_gain_from_YoungScrub = 0
    reindeer_stocking_forecast = 0
    roeDeer_stocking_forecast = round(output_parameters["variable"][5]*100)

    # fallowDeer_stocking_forecast = round(0.27995299*100)
    # cattle_stocking_forecast = round(0.66148828*100)
    # redDeer_stocking_forecast = round(0.02037398*100)
    # tamworthPig_stocking_forecast = round(0.0590684*100)
    # exmoor_stocking_forecast = round(0.18684425*100)
    # # reindeer parameters
    # reproduce_reindeer = 0.21771809
    # # reindeer should have impacts between red and fallow deer
    # reindeer_gain_from_grass = 0.56247843
    # reindeer_gain_from_Trees = 0.59172031
    # reindeer_gain_from_Scrub =0.29453923
    # reindeer_gain_from_Saplings = 0.08512734
    # reindeer_gain_from_YoungScrub = 0.05911069
    # reindeer_stocking_forecast = round(0.54202918*100)
    # roeDeer_stocking_forecast = round(0.3118936*100)


    # run it
    final_results_list = []
    run_number = 0
    number_simulations = 10

    for _ in range(number_simulations):
        # keep track of the runs 
        run_number += 1
        print(run_number)

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
            introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False, cull_roe = True)

        # first graph:  does it pass the filters? looking at the number of individual trees, etc.
        model.run_model()
        results = model.datacollector.get_model_vars_dataframe()
        final_results_list.append(results)

    final_results = pd.concat(final_results_list)

    y_values = final_results[["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland","Woodland", "Thorny Scrub","Bare ground"]].values.flatten()
    species_list = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland","Woodland", "Thorny Scrub","Bare ground"],785*number_simulations) 
    indices = np.repeat(final_results['Time'], 10)

    final_df = pd.DataFrame(
    {'Abundance': y_values, 'Ecosystem Element': species_list, 'Time': indices})
    colors = ["#6788ee"]

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
    axes[6].set_title("Grassland")
    axes[7].set_title("Woodland")
    axes[8].set_title("Thorny scrub")
    axes[9].set_title("Bare ground")
    # axes[10].set_title("New Consumer Species")
    # stop the plots from overlapping
    g.fig.suptitle("Engineering the system towards 25% woodland")
    plt.tight_layout()
    plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/experiment_optimizer_outputs.png')
    plt.show()

graph_results()