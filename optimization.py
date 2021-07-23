# ------ Optimization of the Knepp ABM model --------
from KneppModel_ABM import KneppModel 
import numpy as np
from scipy.optimize import differential_evolution
import numpy as np
import pandas as pd


# ------ Optimization of the Knepp ABM model --------

def objectiveFunction(x):
    # define the parameters
    initial_roeDeer = int(x[0])
    initial_grassland = int(x[1])
    initial_woodland = int(x[2])
    initial_scrubland = int(x[3]) 
    chance_reproduceSapling = x[4] 
    chance_reproduceYoungScrub = x[5] 
    chance_regrowGrass = x[6] 
    chance_saplingBecomingTree = x[7] 
    chance_youngScrubMatures = x[8] 
    chance_scrubOutcompetedByTree = x[9] 
    chance_grassOutcompetedByTreeScrub = x[10] 
    chance_saplingOutcompetedByTree = x[11] 
    chance_saplingOutcompetedByScrub = x[12] 
    chance_youngScrubOutcompetedByScrub = x[13] 
    chance_youngScrubOutcompetedByTree = x[14] 
    roeDeer_reproduce = x[15] 
    roeDeer_gain_from_grass = x[16] 
    roeDeer_gain_from_Trees = x[17] 
    roeDeer_gain_from_Scrub = x[18] 
    roeDeer_gain_from_Saplings = x[19] 
    roeDeer_gain_from_YoungScrub = x[20] 
    fallowDeer_reproduce = x[21] 
    fallowDeer_gain_from_grass = x[22] 
    fallowDeer_gain_from_Trees = x[23] 
    fallowDeer_gain_from_Scrub = x[24] 
    fallowDeer_gain_from_Saplings = x[25] 
    fallowDeer_gain_from_YoungScrub = x[26] 
    redDeer_reproduce = x[27] 
    redDeer_gain_from_grass = x[28] 
    redDeer_gain_from_Trees = x[29] 
    redDeer_gain_from_Scrub = x[30] 
    redDeer_gain_from_Saplings = x[31] 
    redDeer_gain_from_YoungScrub = x[32] 
    ponies_gain_from_grass = x[33] 
    ponies_gain_from_Trees = x[34] 
    ponies_gain_from_Scrub = x[35] 
    ponies_gain_from_Saplings = x[36] 
    ponies_gain_from_YoungScrub = x[37] 
    cows_reproduce = x[38] 
    cows_gain_from_grass = x[39] 
    cows_gain_from_Trees = x[40] 
    cows_gain_from_Scrub = x[41] 
    cows_gain_from_Saplings = x[42] 
    cows_gain_from_YoungScrub = x[43] 
    pigs_reproduce = x[44] 
    pigs_gain_from_grass = x[45]
    pigs_gain_from_Saplings = x[46]
    pigs_gain_from_YoungScrub = x[47]


    # put large herbivore impacts in order 
    grass_impact_bds = list(x[48:54])
    organized_grass = np.sort(grass_impact_bds)
    roeDeer_impactGrass = int(organized_grass[0])
    fallowDeer_impactGrass = int(organized_grass[1])
    redDeer_impactGrass = int(organized_grass[2])
    ponies_impactGrass = int(organized_grass[3])
    cows_impactGrass = int(organized_grass[4])
    pigs_impactGrass = int(organized_grass[5])
    # saplings 
    saplings_impact_bds = list(x[54:60])
    organized_saplings = np.sort(saplings_impact_bds)
    roeDeer_saplingsEaten = int(organized_saplings[0])
    fallowDeer_saplingsEaten = int(organized_saplings[1])
    redDeer_saplingsEaten = int(organized_saplings[2])
    ponies_saplingsEaten = int(organized_saplings[3])
    cows_saplingsEaten = int(organized_saplings[4])
    pigs_saplingsEaten = int(organized_saplings[5])
    # young scrub 
    youngScrub_impact_bds = list(x[60:66])
    organized_youngScrub = np.sort(youngScrub_impact_bds)
    roeDeer_youngScrubEaten = int(organized_youngScrub[0])
    fallowDeer_youngScrubEaten = int(organized_youngScrub[1])
    redDeer_youngScrubEaten = int(organized_youngScrub[2])
    ponies_youngScrubEaten = int(organized_youngScrub[3])
    cows_youngScrubEaten = int(organized_youngScrub[4])
    pigs_youngScrubEaten = int(organized_youngScrub[5])
    # scrub eaten
    scrub_impact_bds = list(x[66:71])
    organizedScrub = np.sort(scrub_impact_bds)
    roeDeer_scrubEaten = int(organizedScrub[0])
    fallowDeer_scrubEaten = int(organizedScrub[1])
    redDeer_scrubEaten = int(organizedScrub[2])
    ponies_scrubEaten = int(organizedScrub[3])
    cows_scrubEaten = int(organizedScrub[4])
    # trees eaten
    trees_impact_bds = list(x[71:76])
    organized_trees = np.sort(trees_impact_bds)
    roeDeer_treesEaten = int(organized_trees[0])
    fallowDeer_treesEaten = int(organized_trees[1])
    redDeer_treesEaten = int(organized_trees[2])
    ponies_treesEaten = int(organized_trees[3])
    cows_treesEaten = int(organized_trees[4])

    model = KneppModel(
        chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
        chance_scrubOutcompetedByTree, chance_grassOutcompetedByTreeScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
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
        ((((list(results.loc[results['Time'] == 50, 'Roe deer'])[0])-23)**2)/23) +
        ((((list(results.loc[results['Time'] == 50, 'Grassland'])[0])-70)**2)/70) +
        ((((list(results.loc[results['Time'] == 50, 'Thorny Scrub'])[0])-11)**2)/11) +
        ((((list(results.loc[results['Time'] == 50, 'Woodland'])[0])-17)**2)/17) +
        # post-reintro model: April 2015
        ((((list(results.loc[results['Time'] == 123, 'Longhorn cattle'])[0])-115)**2)/115) +
        ((((list(results.loc[results['Time'] == 123, 'Tamworth pigs'])[0])-22)**2)/22) +
        # May 2015
        ((((list(results.loc[results['Time'] == 124, 'Longhorn cattle'])[0])-129)**2)/129) +
        # June 2015
        ((((list(results.loc[results['Time'] == 125, 'Longhorn cattle'])[0])-129)**2)/129) +
        # Feb 2016
        ((((list(results.loc[results['Time'] == 133, 'Exmoor pony'])[0])-10)**2)/10) +
        # March 2016
        ((((list(results.loc[results['Time'] == 134, 'Fallow deer'])[0])-140)**2)/140) +
        ((((list(results.loc[results['Time'] == 134, 'Red deer'])[0])-26)**2)/26) +
        ((((list(results.loc[results['Time'] == 134, 'Tamworth pigs'])[0])-9)**2)/9) +
        # April 2016
        ((((list(results.loc[results['Time'] == 135, 'Longhorn cattle'])[0])-103)**2)/103) +
        # May 2016
        ((((list(results.loc[results['Time'] == 136, 'Longhorn cattle'])[0])-108)**2)/108) +
        ((((list(results.loc[results['Time'] == 136, 'Tamworth pigs'])[0])-17)**2)/17) +
        # June 2016
        ((((list(results.loc[results['Time'] == 137, 'Longhorn cattle'])[0])-129)**2)/129) +
        # Feb 2017
        ((((list(results.loc[results['Time'] == 145, 'Exmoor pony'])[0])-11)**2)/11) +
        # March 2017
        ((((list(results.loc[results['Time'] == 146, 'Fallow deer'])[0])-165)**2)/165) +
        # April 2017
        ((((list(results.loc[results['Time'] == 147, 'Longhorn cattle'])[0])-100)**2)/100) +
        ((((list(results.loc[results['Time'] == 147, 'Tamworth pigs'])[0])-22)**2)/22) +
        # May 2017
        ((((list(results.loc[results['Time'] == 148, 'Longhorn cattle'])[0])-109)**2)/109) +
        # June 2017
        ((((list(results.loc[results['Time'] == 149, 'Longhorn cattle'])[0])-94)**2)/94) +
        # Jan 2018
        ((((list(results.loc[results['Time'] == 156, 'Tamworth pigs'])[0])-12)**2)/12) +
        # Feb 2018
        ((((list(results.loc[results['Time'] == 157, 'Exmoor pony'])[0])-10)**2)/10) +
        ((((list(results.loc[results['Time'] == 157, 'Tamworth pigs'])[0])-16)**2)/16) +
        # March 2018
        ((((list(results.loc[results['Time'] == 158, 'Fallow deer'])[0])-251)**2)/251) +
        ((((list(results.loc[results['Time'] == 158, 'Red deer'])[0])-24)**2)/24) +
        # April 2018
        ((((list(results.loc[results['Time'] == 159, 'Longhorn cattle'])[0])-101)**2)/101) +
        # May 2018
        ((((list(results.loc[results['Time'] == 160, 'Longhorn cattle'])[0])-117)**2)/117) +
        ((((list(results.loc[results['Time'] == 160, 'Tamworth pigs'])[0])-23)**2)/23) +
        # June 2018
        ((((list(results.loc[results['Time'] == 161, 'Longhorn cattle'])[0])-103)**2)/103) +
        # March 2019
        ((((list(results.loc[results['Time'] == 170, 'Fallow deer'])[0])-278)**2)/278) +
        ((((list(results.loc[results['Time'] == 170, 'Red deer'])[0])-37)**2)/37) +
        # April 2019
        ((((list(results.loc[results['Time'] == 171, 'Longhorn cattle'])[0])-101)**2)/101) +
        # May 2019
        ((((list(results.loc[results['Time'] == 172, 'Longhorn cattle'])[0])-110)**2)/110) +
        # June 2019
        ((((list(results.loc[results['Time'] == 173, 'Longhorn cattle'])[0])-89)**2)/89) +
        # July 2019        
        ((((list(results.loc[results['Time'] == 174, 'Tamworth pigs'])[0])-9)**2)/9) +
        # March 2021 
        ((((list(results.loc[results['Time'] == 182, 'Fallow deer'])[0])-247)**2)/247) +
        ((((list(results.loc[results['Time'] == 182, 'Red deer'])[0])-35)**2)/35) +
        # May 2021
        ((((list(results.loc[results['Time'] == 184, 'Exmoor pony'])[0])-15)**2)/15) +
        ((((list(results.loc[results['Time'] == 184, 'Tamworth pigs'])[0])-19)**2)/19) +
        ((((list(results.loc[results['Time'] == 184, 'Roe deer'])[0])-30)**2)/30) +
        ((((list(results.loc[results['Time'] == 184, 'Grassland'])[0])-59)**2)/59) +
        ((((list(results.loc[results['Time'] == 184, 'Thorny Scrub'])[0])-28)**2)/28) +
        ((((list(results.loc[results['Time'] == 184, 'Woodland'])[0])-19)**2)/19))
                         

    # if filtered_result < 1000:
    print("r:", filtered_result)
    with pd.option_context('display.max_columns',None):
        print(results[results['Time'] == 184])

    return filtered_result
   


# Define bounds
param_bds = (
    # initial values
    (6,18), (70,90), (4,24), (0,11), 
    # habitat parameters
    (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1),
    # roe deer parameters
    (0,1), (0,1),(0,1),(0,1),(0,1),(0,1),
    # fallow deer parameters
    (0,1), (0,1),(0,1),(0,1),(0,1),(0,1),
    # red deer parameters
    (0,1), (0,1),(0,1),(0,1),(0,1),(0,1),
    # exmoor pony parameters
    (0,1),(0,1),(0,1),(0,1),(0,1),
    # cattle parameters
    (0,1), (0,1),(0,1),(0,1),(0,1),(0,1),
    # pig parameters
    (0,1), (0,1),(0,1),(0,1))

grass_impact_bds = ((0,100), (0,100), (0,100), (0,100), (0,100), (0,100))
saplings_impact_bds = ((0,100), (0,100), (0,100), (0,100), (0,100), (0,100))
youngScrub_impact_bds = ((0,100), (0,100), (0,100), (0,100), (0,100), (0,100))
scrub_impact_bds = ((0,10), (0,10), (0,10), (0,10), (0,10))
tree_impact_bds = ((0,10), (0,10), (0,10), (0,10), (0,10))

bds = param_bds + grass_impact_bds + saplings_impact_bds + youngScrub_impact_bds + scrub_impact_bds + tree_impact_bds

optimization = differential_evolution(objectiveFunction, bounds = bds, maxiter =  5000)
print(optimization)

