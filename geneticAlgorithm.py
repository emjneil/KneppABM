# ------ Optimization of the Knepp ABM model --------
from KneppModel_ABM import KneppModel 
import numpy as np
import numpy as np
import pandas as pd
from geneticalgorithm import geneticalgorithm as ga

# ------ Optimization of the Knepp ABM model --------

def objectiveFunction(x):
    # define the parameters
    initial_roeDeer = round(x[0])
    initial_grassland = round(x[1])
    initial_woodland = round(x[2])
    initial_scrubland = round(x[3]) 
    chance_reproduceSapling = x[4] 
    chance_reproduceYoungScrub = x[5] 
    chance_regrowGrass = x[6] 
    chance_saplingBecomingTree = x[7] 
    chance_youngScrubMatures = x[8] 
    roeDeer_reproduce = x[9] 
    roeDeer_gain_from_grass = x[10] 
    roeDeer_gain_from_Trees = x[11] 
    roeDeer_gain_from_Scrub = x[12] 
    roeDeer_gain_from_Saplings = x[13] 
    roeDeer_gain_from_YoungScrub = x[14] 
    fallowDeer_reproduce = x[15] 
    fallowDeer_gain_from_grass = x[16] 
    fallowDeer_gain_from_Trees = x[17] 
    fallowDeer_gain_from_Scrub = x[18] 
    fallowDeer_gain_from_Saplings = x[19] 
    fallowDeer_gain_from_YoungScrub = x[20] 
    redDeer_reproduce = x[21] 
    redDeer_gain_from_grass = x[22] 
    redDeer_gain_from_Trees = x[23] 
    redDeer_gain_from_Scrub = x[24] 
    redDeer_gain_from_Saplings = x[25] 
    redDeer_gain_from_YoungScrub = x[26] 
    ponies_gain_from_grass = x[27] 
    ponies_gain_from_Trees = x[28] 
    ponies_gain_from_Scrub = x[29] 
    ponies_gain_from_Saplings = x[30] 
    ponies_gain_from_YoungScrub = x[31] 
    cows_reproduce = x[32] 
    cows_gain_from_grass = x[33] 
    cows_gain_from_Trees = x[34] 
    cows_gain_from_Scrub = x[35] 
    cows_gain_from_Saplings = x[36] 
    cows_gain_from_YoungScrub = x[37] 
    pigs_reproduce = x[38] 
    pigs_gain_from_grass = x[39]
    pigs_gain_from_Saplings = x[40]
    pigs_gain_from_YoungScrub = x[41]

    # put large herbivore impacts in order 
    # grass_impact_bds = list(x[49:55])
    # organized_grass = np.sort(grass_impact_bds)
    # roeDeer_impactGrass = int(organized_grass[0])
    roeDeer_impactGrass = round(x[42])
    fallowDeer_impactGrass = round(x[43])
    redDeer_impactGrass = round(x[44])
    ponies_impactGrass = round(x[45])
    cows_impactGrass = round(x[46])
    pigs_impactGrass = round(x[47])
    # saplings 
    # saplings_impact_bds = list(x[55:61])
    # organized_saplings = np.sort(saplings_impact_bds)
    roeDeer_saplingsEaten = round(x[48])
    fallowDeer_saplingsEaten = round(x[49])
    redDeer_saplingsEaten = round(x[50])
    ponies_saplingsEaten = round(x[51])
    cows_saplingsEaten = round(x[52])
    pigs_saplingsEaten = round(x[53])
    # young scrub 
    # youngScrub_impact_bds = list(x[61:67])
    # organized_youngScrub = np.sort(youngScrub_impact_bds)
    roeDeer_youngScrubEaten = round(x[54])
    fallowDeer_youngScrubEaten = round(x[55])
    redDeer_youngScrubEaten = round(x[56])
    ponies_youngScrubEaten = round(x[57])
    cows_youngScrubEaten = round(x[58])
    pigs_youngScrubEaten = round(x[59])
    # scrub eaten
    # scrub_impact_bds = list(x[67:72])
    # organizedScrub = np.sort(scrub_impact_bds)
    roeDeer_scrubEaten = round(x[60])
    fallowDeer_scrubEaten = round(x[61])
    redDeer_scrubEaten = round(x[62])
    ponies_scrubEaten = round(x[63])
    cows_scrubEaten = round(x[64])
    # trees eaten
    # trees_impact_bds = list(x[72:77])
    # organized_trees = np.sort(trees_impact_bds)
    roeDeer_treesEaten = round(x[65])
    fallowDeer_treesEaten = round(x[66])
    redDeer_treesEaten = round(x[67])
    ponies_treesEaten = round(x[68])
    cows_treesEaten = round(x[69])

    model = KneppModel(
        chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
        initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland, 
        roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
        roeDeer_impactGrass, roeDeer_saplingsEaten, roeDeer_youngScrubEaten, roeDeer_treesEaten, roeDeer_scrubEaten,
        ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
        ponies_impactGrass, ponies_saplingsEaten, ponies_youngScrubEaten, ponies_treesEaten, ponies_scrubEaten, 
        cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
        cows_impactGrass, cows_saplingsEaten, cows_youngScrubEaten, cows_treesEaten, cows_scrubEaten, 
        fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
        fallowDeer_impactGrass, fallowDeer_saplingsEaten, fallowDeer_youngScrubEaten, fallowDeer_treesEaten, fallowDeer_scrubEaten,
        redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
        redDeer_impactGrass, redDeer_saplingsEaten, redDeer_youngScrubEaten, redDeer_treesEaten, redDeer_scrubEaten, 
        pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
        pigs_impactGrass, pigs_saplingsEaten, pigs_youngScrubEaten, 
        width = 50, height = 36)
    model.run_model()

    # remember the results of the model (dominant conditions, # of agents)
    results = model.datacollector.get_model_vars_dataframe()
    
    # find the middle of each filter
    filtered_result = (
        # pre-reintro model
        (((list(results.loc[results['Time'] == 25, 'Thorny Scrub'])[0])-6)**2) +
        (((list(results.loc[results['Time'] == 49, 'Roe deer'])[0])-23)**2) +
        (((list(results.loc[results['Time'] == 49, 'Grassland'])[0])-70)**2) +
        (((list(results.loc[results['Time'] == 49, 'Thorny Scrub'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 49, 'Woodland'])[0])-17)**2))
        # # post-reintro model: April 2015
        # ((((list(results.loc[results['Time'] == 123, 'Longhorn cattle'])[0])-115)**2)/115) +
        # ((((list(results.loc[results['Time'] == 123, 'Tamworth pigs'])[0])-23)**2)/23) +
        # # May 2015
        # ((((list(results.loc[results['Time'] == 124, 'Longhorn cattle'])[0])-129)**2)/129) +
        # # June 2015
        # ((((list(results.loc[results['Time'] == 125, 'Longhorn cattle'])[0])-134)**2)/134) +
        # # Feb 2016
        # ((((list(results.loc[results['Time'] == 133, 'Exmoor pony'])[0])-10)**2)/10) +
        # # March 2016
        # ((((list(results.loc[results['Time'] == 134, 'Fallow deer'])[0])-140)**2)/140) +
        # ((((list(results.loc[results['Time'] == 134, 'Red deer'])[0])-26)**2)/26) +
        # ((((list(results.loc[results['Time'] == 134, 'Tamworth pigs'])[0])-10)**2)/10) +
        # # April 2016
        # ((((list(results.loc[results['Time'] == 135, 'Longhorn cattle'])[0])-102)**2)/102) +
        # # May 2016
        # ((((list(results.loc[results['Time'] == 136, 'Longhorn cattle'])[0])-110)**2)/110) +
        # ((((list(results.loc[results['Time'] == 136, 'Tamworth pigs'])[0])-17)**2)/17) +
        # # June 2016
        # ((((list(results.loc[results['Time'] == 137, 'Longhorn cattle'])[0])-113)**2)/113) +
        # # Feb 2017
        # ((((list(results.loc[results['Time'] == 145, 'Exmoor pony'])[0])-11)**2)/11) +
        # # March 2017
        # ((((list(results.loc[results['Time'] == 146, 'Fallow deer'])[0])-165)**2)/165) +
        # # April 2017
        # ((((list(results.loc[results['Time'] == 147, 'Longhorn cattle'])[0])-103)**2)/103) +
        # ((((list(results.loc[results['Time'] == 147, 'Tamworth pigs'])[0])-22)**2)/22) +
        # # May 2017
        # ((((list(results.loc[results['Time'] == 148, 'Longhorn cattle'])[0])-109)**2)/109) +
        # # June 2017
        # ((((list(results.loc[results['Time'] == 149, 'Longhorn cattle'])[0])-115)**2)/115) +
        # # Jan 2018
        # ((((list(results.loc[results['Time'] == 156, 'Tamworth pigs'])[0])-20)**2)/20) +
        # # Feb 2018
        # ((((list(results.loc[results['Time'] == 157, 'Exmoor pony'])[0])-10)**2)/10) +
        # ((((list(results.loc[results['Time'] == 157, 'Tamworth pigs'])[0])-17)**2)/17) +
        # # March 2018
        # ((((list(results.loc[results['Time'] == 158, 'Fallow deer'])[0])-251)**2)/251) +
        # ((((list(results.loc[results['Time'] == 158, 'Red deer'])[0])-24)**2)/24) +
        # # April 2018
        # ((((list(results.loc[results['Time'] == 159, 'Longhorn cattle'])[0])-100)**2)/100) +
        # # May 2018
        # ((((list(results.loc[results['Time'] == 160, 'Longhorn cattle'])[0])-117)**2)/117) +
        # ((((list(results.loc[results['Time'] == 160, 'Tamworth pigs'])[0])-23)**2)/23) +
        # # June 2018
        # ((((list(results.loc[results['Time'] == 161, 'Longhorn cattle'])[0])-123)**2)/123) +
        # # March 2019
        # ((((list(results.loc[results['Time'] == 170, 'Fallow deer'])[0])-278)**2)/278) +
        # ((((list(results.loc[results['Time'] == 170, 'Red deer'])[0])-37)**2)/37) +
        # # April 2019
        # ((((list(results.loc[results['Time'] == 171, 'Longhorn cattle'])[0])-101)**2)/101) +
        # # May 2019
        # ((((list(results.loc[results['Time'] == 172, 'Longhorn cattle'])[0])-110)**2)/110) +
        # # June 2019
        # ((((list(results.loc[results['Time'] == 173, 'Longhorn cattle'])[0])-117)**2)/117) +
        # # July 2019        
        # ((((list(results.loc[results['Time'] == 174, 'Tamworth pigs'])[0])-36)**2)/36) +
        # # March 2021 
        # ((((list(results.loc[results['Time'] == 182, 'Fallow deer'])[0])-247)**2)/247) +
        # ((((list(results.loc[results['Time'] == 182, 'Red deer'])[0])-35)**2)/35) +
        # # May 2021
        # ((((list(results.loc[results['Time'] == 184, 'Exmoor pony'])[0])-15)**2)/15) +
        # ((((list(results.loc[results['Time'] == 184, 'Tamworth pigs'])[0])-19)**2)/19) +
        # ((((list(results.loc[results['Time'] == 184, 'Roe deer'])[0])-30)**2)/30) +
        # ((((list(results.loc[results['Time'] == 184, 'Grassland'])[0])-59)**2)/59) +
        # ((((list(results.loc[results['Time'] == 184, 'Thorny Scrub'])[0])-28)**2)/28) +
        # ((((list(results.loc[results['Time'] == 184, 'Woodland'])[0])-19)**2)/19))
                         

    if filtered_result < 5000:
        print("r:", filtered_result)
        with pd.option_context('display.max_columns',None):
            print(results[results['Time'] == 0])
            print(results[results['Time'] == 1])
            print(results[results['Time'] == 50])

    return filtered_result
   

def run_optimizer():
    # Define bounds
    bds = np.array([
        # initial values
        [6,18],[75,85],[9,19],[0,6],
        # habitat parameters
        [0,0.25],[0,0.25],[0,1],[0,0.01],[0,0.1],
        # roe deer parameters
        [0,0.5],[0,1],[0,1],[0,1],[0,1],[0,1],
        # fallow deer parameters
        [0,1],[0,1],[0,1],[0,1],[0,1],[0,1],
        # red deer parameters
        [0,1],[0,1],[0,1],[0,1],[0,1],[0,1],
        # exmoor pony parameters
        [0,1],[0,1],[0,1],[0,1],[0,1],
        # cattle parameters
        [0,1],[0,1],[0,1],[0,1],[0,1],[0,1],
        # pig parameters
        [0,1],[0,1],[0,1],[0,1],
        # grass impact
        [0,100],[0,1],[0,1],[0,1],[0,1],[0,1],
        # sapling impact
        [0,5000],[0,1],[0,1],[0,1],[0,1],[0,1],
        # young scrub impact
        [0,5000],[0,1],[0,1],[0,1],[0,1],[0,1],
        # scrub impact
        [0,100],[0,1],[0,1],[0,1],[0,1],
        # tree impact
        [0,100],[0,1],[0,1],[0,1],[0,1]
    ])





    algorithm_param = {'max_num_iteration': 500,\
                    'population_size':10,\
                    'mutation_probability':0.1,\
                    'elit_ratio': 0.01,\
                    'crossover_probability': 0.5,\
                    'parents_portion': 0.3,\
                    'crossover_type':'uniform',\
                    'max_iteration_without_improv':None}


    optimization =  ga(function = objectiveFunction, dimension = 70, variable_type = 'real',variable_boundaries= bds, algorithm_parameters = algorithm_param, function_timeout=6000)
    optimization.run()
    print(optimization)
    return optimization.output_dict
