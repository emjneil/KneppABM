# ------ Optimization of the Knepp ABM model --------
from KneppModel_ABM import KneppModel 
import numpy as np
import numpy as np
import pandas as pd
import random
from geneticalgorithm import geneticalgorithm as ga
import timeit

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
    chance_grassOutcompetedByScrub = x[7]
    chance_saplingOutcompetedByTree = x[8] 
    chance_saplingOutcompetedByScrub = x[9] 
    chance_youngScrubOutcompetedByScrub = x[10] 
    chance_youngScrubOutcompetedByTree = x[11] 
    # initial values
    initial_roeDeer = x[12]
    initial_grassland = x[13]
    initial_woodland = x[14]
    initial_scrubland = x[15]
    roeDeer_reproduce = x[16] 
    roeDeer_gain_from_grass = x[17] 
    roeDeer_gain_from_Trees = x[18] 
    roeDeer_gain_from_Scrub = x[19] 
    roeDeer_gain_from_Saplings = x[20] 
    roeDeer_gain_from_YoungScrub = x[21] 
    fallowDeer_reproduce = x[22] 
    fallowDeer_gain_from_grass = x[23] 
    fallowDeer_gain_from_Trees = x[24] 
    fallowDeer_gain_from_Scrub = x[25] 
    fallowDeer_gain_from_Saplings = x[26] 
    fallowDeer_gain_from_YoungScrub = x[27] 
    redDeer_reproduce = x[28] 
    redDeer_gain_from_grass = x[29] 
    redDeer_gain_from_Trees = x[30] 
    redDeer_gain_from_Scrub = x[31] 
    redDeer_gain_from_Saplings = x[32] 
    redDeer_gain_from_YoungScrub = x[33] 
    ponies_gain_from_grass = x[34] 
    ponies_gain_from_Trees = x[35] 
    ponies_gain_from_Scrub = x[36] 
    ponies_gain_from_Saplings = x[37] 
    ponies_gain_from_YoungScrub = x[38] 
    cows_reproduce = x[39] 
    cows_gain_from_grass = x[40] 
    cows_gain_from_Trees = x[41] 
    cows_gain_from_Scrub = x[42] 
    cows_gain_from_Saplings = x[43] 
    cows_gain_from_YoungScrub = x[44] 
    pigs_reproduce = x[45] 
    pigs_gain_from_grass = x[46]
    pigs_gain_from_Saplings = x[47]
    pigs_gain_from_YoungScrub = x[48]
    # put large herbivore impacts in order 
    roeDeer_impactGrass = x[49]
    fallowDeer_impactGrass = x[50]
    redDeer_impactGrass = x[51]
    ponies_impactGrass = x[52]
    cows_impactGrass = x[53]
    pigs_impactGrass = x[54]
    # saplings 
    roeDeer_saplingsEaten = x[55]
    fallowDeer_saplingsEaten = x[56]
    redDeer_saplingsEaten = x[57]
    ponies_saplingsEaten = x[58]
    cows_saplingsEaten = x[59]
    pigs_saplingsEaten = x[60]
    # young scrub 
    roeDeer_youngScrubEaten = x[61]
    fallowDeer_youngScrubEaten = x[62]
    redDeer_youngScrubEaten = x[63]
    ponies_youngScrubEaten = x[64]
    cows_youngScrubEaten = x[65]
    pigs_youngScrubEaten = x[66]
    # scrub eaten
    roeDeer_scrubEaten = x[67]
    fallowDeer_scrubEaten = x[68]
    redDeer_scrubEaten = x[69]
    ponies_scrubEaten = x[70]
    cows_scrubEaten = x[71]
    # trees eaten
    roeDeer_treesEaten = x[72]
    fallowDeer_treesEaten = x[73]
    redDeer_treesEaten = x[74]
    ponies_treesEaten = x[75]
    cows_treesEaten = x[76]


    model = KneppModel(
        chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
        chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
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
        (((list(results.loc[results['Time'] == 49, 'Roe deer'])[0])-23)**2) +
        (((list(results.loc[results['Time'] == 49, 'Grassland'])[0])-70)**2) +
        (((list(results.loc[results['Time'] == 49, 'Thorny Scrub'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 49, 'Woodland'])[0])-17)**2) +
        # post-reintro model: April 2015
        (((list(results.loc[results['Time'] == 123, 'Longhorn cattle'])[0])-115)**2) +
        (((list(results.loc[results['Time'] == 123, 'Tamworth pigs'])[0])-22)**2) +
        (((list(results.loc[results['Time'] == 123, 'Exmoor pony'])[0])-10)**2) +
        # May 2015
        (((list(results.loc[results['Time'] == 124, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 124, 'Longhorn cattle'])[0])-129)**2) +
        (((list(results.loc[results['Time'] == 124, 'Tamworth pigs'])[0])-14)**2) +
        # June 2015
        (((list(results.loc[results['Time'] == 125, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 125, 'Longhorn cattle'])[0])-129)**2) +
        (((list(results.loc[results['Time'] == 125, 'Tamworth pigs'])[0])-14)**2) +
        # July 2015
        (((list(results.loc[results['Time'] == 126, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 126, 'Longhorn cattle'])[0])-129)**2) +
        (((list(results.loc[results['Time'] == 126, 'Tamworth pigs'])[0])-14)**2) +
        # Aug 2015
        (((list(results.loc[results['Time'] == 127, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 127, 'Longhorn cattle'])[0])-129)**2) +
        (((list(results.loc[results['Time'] == 127, 'Tamworth pigs'])[0])-14)**2) +
        # Sept 2015
        (((list(results.loc[results['Time'] == 128, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 128, 'Longhorn cattle'])[0])-130)**2) +
        (((list(results.loc[results['Time'] == 128, 'Tamworth pigs'])[0])-14)**2) +
        # Oct 2015
        (((list(results.loc[results['Time'] == 129, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 129, 'Longhorn cattle'])[0])-91)**2) +
        (((list(results.loc[results['Time'] == 129, 'Tamworth pigs'])[0])-14)**2) +
        # Nov 2015
        (((list(results.loc[results['Time'] == 130, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 130, 'Longhorn cattle'])[0])-91)**2) +
        (((list(results.loc[results['Time'] == 130, 'Tamworth pigs'])[0])-13)**2) +
        # Dec 2015
        (((list(results.loc[results['Time'] == 131, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 131, 'Longhorn cattle'])[0])-86)**2) +
        (((list(results.loc[results['Time'] == 131, 'Tamworth pigs'])[0])-13)**2) +
        # Jan 2016
        (((list(results.loc[results['Time'] == 132, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 132, 'Longhorn cattle'])[0])-86)**2) +
        (((list(results.loc[results['Time'] == 132, 'Tamworth pigs'])[0])-10)**2) +
        # Feb 2016
        (((list(results.loc[results['Time'] == 133, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 133, 'Longhorn cattle'])[0])-86)**2) +
        (((list(results.loc[results['Time'] == 133, 'Tamworth pigs'])[0])-8)**2) +
        # # March 2016
        (((list(results.loc[results['Time'] == 134, 'Fallow deer'])[0])-140)**2) +
        (((list(results.loc[results['Time'] == 134, 'Red deer'])[0])-26)**2) +
        (((list(results.loc[results['Time'] == 134, 'Tamworth pigs'])[0])-9)**2) +
        (((list(results.loc[results['Time'] == 134, 'Longhorn cattle'])[0])-86)**2) +
        (((list(results.loc[results['Time'] == 134, 'Exmoor pony'])[0])-11)**2) +
        # April 2016
        (((list(results.loc[results['Time'] == 135, 'Longhorn cattle'])[0])-103)**2) +
        (((list(results.loc[results['Time'] == 135, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 135, 'Tamworth pigs'])[0])-9)**2) +
        # # May 2016
        (((list(results.loc[results['Time'] == 136, 'Longhorn cattle'])[0])-108)**2) +
        (((list(results.loc[results['Time'] == 136, 'Tamworth pigs'])[0])-17)**2) +
        (((list(results.loc[results['Time'] == 136, 'Exmoor pony'])[0])-11)**2) +
        # June 2016
        (((list(results.loc[results['Time'] == 137, 'Longhorn cattle'])[0])-89)**2) +
        (((list(results.loc[results['Time'] == 137, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 137, 'Tamworth pigs'])[0])-17)**2) +
        # July 2016
        (((list(results.loc[results['Time'] == 138, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 138, 'Tamworth pigs'])[0])-17)**2) +
        (((list(results.loc[results['Time'] == 138, 'Longhorn cattle'])[0])-87)**2) +
        # August 2016
        (((list(results.loc[results['Time'] == 139, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 139, 'Tamworth pigs'])[0])-17)**2) +
        (((list(results.loc[results['Time'] == 139, 'Longhorn cattle'])[0])-87)**2) +
        # September 2016
        (((list(results.loc[results['Time'] == 140, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 140, 'Tamworth pigs'])[0])-17)**2) +
        (((list(results.loc[results['Time'] == 140, 'Longhorn cattle'])[0])-97)**2) +
        # Oct 2016
        (((list(results.loc[results['Time'] == 141, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 141, 'Tamworth pigs'])[0])-17)**2) +
        (((list(results.loc[results['Time'] == 141, 'Longhorn cattle'])[0])-97)**2) +
        # Nov 2016
        (((list(results.loc[results['Time'] == 142, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 142, 'Tamworth pigs'])[0])-17)**2) +
        (((list(results.loc[results['Time'] == 142, 'Longhorn cattle'])[0])-92)**2) +
        # Dec 2016
        (((list(results.loc[results['Time'] == 143, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 143, 'Tamworth pigs'])[0])-13)**2) +
        (((list(results.loc[results['Time'] == 143, 'Longhorn cattle'])[0])-79)**2) +
        # Jan 2017
        (((list(results.loc[results['Time'] == 144, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 144, 'Tamworth pigs'])[0])-9)**2) +
        (((list(results.loc[results['Time'] == 144, 'Longhorn cattle'])[0])-79)**2) +
        # Feb 2017
        (((list(results.loc[results['Time'] == 145, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 145, 'Tamworth pigs'])[0])-7)**2) +
        (((list(results.loc[results['Time'] == 145, 'Longhorn cattle'])[0])-79)**2) +
        # # March 2017
        (((list(results.loc[results['Time'] == 146, 'Fallow deer'])[0])-165)**2) +
        (((list(results.loc[results['Time'] == 146, 'Longhorn cattle'])[0])-79)**2) +
        (((list(results.loc[results['Time'] == 146, 'Tamworth pigs'])[0])-7)**2) +
        (((list(results.loc[results['Time'] == 146, 'Exmoor pony'])[0])-10)**2) +
        # April 2017
        (((list(results.loc[results['Time'] == 147, 'Longhorn cattle'])[0])-100)**2) +
        (((list(results.loc[results['Time'] == 147, 'Tamworth pigs'])[0])-22)**2) +
        (((list(results.loc[results['Time'] == 147, 'Exmoor pony'])[0])-10)**2) +
        # May 2017
        (((list(results.loc[results['Time'] == 148, 'Longhorn cattle'])[0])-109)**2) +
        (((list(results.loc[results['Time'] == 148, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 148, 'Tamworth pigs'])[0])-22)**2) +
        # June 2017
        (((list(results.loc[results['Time'] == 149, 'Longhorn cattle'])[0])-94)**2) +
        (((list(results.loc[results['Time'] == 149, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 149, 'Tamworth pigs'])[0])-22)**2) +
        # July 2017
        (((list(results.loc[results['Time'] == 150, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 150, 'Longhorn cattle'])[0])-94)**2) +
        (((list(results.loc[results['Time'] == 150, 'Tamworth pigs'])[0])-22)**2) +
        # Aug 2017
        (((list(results.loc[results['Time'] == 151, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 151, 'Longhorn cattle'])[0])-94)**2) +
        (((list(results.loc[results['Time'] == 151, 'Tamworth pigs'])[0])-22)**2) +
        # Sept 2017
        (((list(results.loc[results['Time'] == 152, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 152, 'Longhorn cattle'])[0])-90)**2) +
        (((list(results.loc[results['Time'] == 152, 'Tamworth pigs'])[0])-22)**2) +
        # Oct 2017
        (((list(results.loc[results['Time'] == 153, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 153, 'Longhorn cattle'])[0])-88)**2) +
        (((list(results.loc[results['Time'] == 153, 'Tamworth pigs'])[0])-22)**2) +
        # Nov 2017
        (((list(results.loc[results['Time'] == 154, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 154, 'Longhorn cattle'])[0])-88)**2) +
        (((list(results.loc[results['Time'] == 154, 'Tamworth pigs'])[0])-22)**2) +
        # # Dec 2017
        (((list(results.loc[results['Time'] == 155, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 155, 'Longhorn cattle'])[0])-88)**2) +
        (((list(results.loc[results['Time'] == 155, 'Tamworth pigs'])[0])-18)**2) +
        # Jan 2018
        (((list(results.loc[results['Time'] == 156, 'Tamworth pigs'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 156, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 156, 'Longhorn cattle'])[0])-88)**2) +
        # Feb 2018
        (((list(results.loc[results['Time'] == 157, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 157, 'Tamworth pigs'])[0])-16)**2) +
        (((list(results.loc[results['Time'] == 157, 'Longhorn cattle'])[0])-88)**2) +
        # March 2018
        (((list(results.loc[results['Time'] == 158, 'Fallow deer'])[0])-251)**2) +
        (((list(results.loc[results['Time'] == 158, 'Red deer'])[0])-24)**2) +
        (((list(results.loc[results['Time'] == 158, 'Longhorn cattle'])[0])-88)**2) +
        (((list(results.loc[results['Time'] == 158, 'Tamworth pigs'])[0])-16)**2) +
        (((list(results.loc[results['Time'] == 158, 'Exmoor pony'])[0])-9)**2) +
        # April 2018
        (((list(results.loc[results['Time'] == 159, 'Longhorn cattle'])[0])-101)**2) +
        (((list(results.loc[results['Time'] == 159, 'Exmoor pony'])[0])-9)**2) +
        (((list(results.loc[results['Time'] == 159, 'Tamworth pigs'])[0])-16)**2) +
        # # May 2018
        (((list(results.loc[results['Time'] == 160, 'Longhorn cattle'])[0])-117)**2) +
        (((list(results.loc[results['Time'] == 160, 'Tamworth pigs'])[0])-23)**2) +
        (((list(results.loc[results['Time'] == 160, 'Exmoor pony'])[0])-9)**2) +
        # June 2018
        (((list(results.loc[results['Time'] == 161, 'Longhorn cattle'])[0])-103)**2) +
        (((list(results.loc[results['Time'] == 161, 'Exmoor pony'])[0])-9)**2) +
        (((list(results.loc[results['Time'] == 161, 'Tamworth pigs'])[0])-23)**2) +
        # July 2019
        (((list(results.loc[results['Time'] == 162, 'Exmoor pony'])[0])-9)**2) +
        (((list(results.loc[results['Time'] == 162, 'Longhorn cattle'])[0])-103)**2) +
        (((list(results.loc[results['Time'] == 162, 'Tamworth pigs'])[0])-22)**2) +
        # Aug 2019
        (((list(results.loc[results['Time'] == 163, 'Longhorn cattle'])[0])-102)**2) +
        (((list(results.loc[results['Time'] == 163, 'Tamworth pigs'])[0])-22)**2) +
        # Sept 2019
        (((list(results.loc[results['Time'] == 164, 'Longhorn cattle'])[0])-106)**2) +
        (((list(results.loc[results['Time'] == 164, 'Tamworth pigs'])[0])-22)**2) +
        # Oct 2019
        (((list(results.loc[results['Time'] == 165, 'Longhorn cattle'])[0])-101)**2) +
        (((list(results.loc[results['Time'] == 165, 'Tamworth pigs'])[0])-21)**2) +
        # Nov 2019
        (((list(results.loc[results['Time'] == 166, 'Longhorn cattle'])[0])-93)**2) +
        (((list(results.loc[results['Time'] == 166, 'Tamworth pigs'])[0])-9)**2) +
        # Dec 2019
        (((list(results.loc[results['Time'] == 167, 'Longhorn cattle'])[0])-89)**2) +
        (((list(results.loc[results['Time'] == 167, 'Tamworth pigs'])[0])-9)**2) +
        # Jan 2020
        (((list(results.loc[results['Time'] == 168, 'Longhorn cattle'])[0])-89)**2) +
        (((list(results.loc[results['Time'] == 168, 'Tamworth pigs'])[0])-9)**2) +
        # Feb 2020
        (((list(results.loc[results['Time'] == 169, 'Longhorn cattle'])[0])-87)**2) +
        (((list(results.loc[results['Time'] == 169, 'Tamworth pigs'])[0])-10)**2) +
        # March 2019
        (((list(results.loc[results['Time'] == 170, 'Fallow deer'])[0])-278)**2) +
        (((list(results.loc[results['Time'] == 170, 'Red deer'])[0])-37)**2) +
        (((list(results.loc[results['Time'] == 170, 'Longhorn cattle'])[0])-87)**2) +
        (((list(results.loc[results['Time'] == 170, 'Tamworth pigs'])[0])-9)**2) +
        # April 2019
        (((list(results.loc[results['Time'] == 171, 'Longhorn cattle'])[0])-101)**2) +
        (((list(results.loc[results['Time'] == 171, 'Tamworth pigs'])[0])-8)**2) +
        # May 2019
        (((list(results.loc[results['Time'] == 172, 'Longhorn cattle'])[0])-110)**2) +
        (((list(results.loc[results['Time'] == 172, 'Tamworth pigs'])[0])-8)**2) +
        # June 2019
        (((list(results.loc[results['Time'] == 173, 'Longhorn cattle'])[0])-89)**2) +
        (((list(results.loc[results['Time'] == 173, 'Tamworth pigs'])[0])-8)**2) +
        # July 2019        
        (((list(results.loc[results['Time'] == 174, 'Tamworth pigs'])[0])-9)**2) +
        (((list(results.loc[results['Time'] == 174, 'Longhorn cattle'])[0])-91)**2) +
        # Aug 2019 
        (((list(results.loc[results['Time'] == 175, 'Longhorn cattle'])[0])-91)**2) +
        (((list(results.loc[results['Time'] == 175, 'Tamworth pigs'])[0])-9)**2) +
        # Sept 2019 
        (((list(results.loc[results['Time'] == 176, 'Longhorn cattle'])[0])-93)**2) +
        (((list(results.loc[results['Time'] == 176, 'Tamworth pigs'])[0])-9)**2) +
        # Oct 2019 
        (((list(results.loc[results['Time'] == 177, 'Longhorn cattle'])[0])-88)**2) +
        (((list(results.loc[results['Time'] == 177, 'Tamworth pigs'])[0])-9)**2) +
        # Nov 2019 
        (((list(results.loc[results['Time'] == 178, 'Longhorn cattle'])[0])-87)**2) +
        (((list(results.loc[results['Time'] == 178, 'Tamworth pigs'])[0])-9)**2) +
        # Dec 2019 
        (((list(results.loc[results['Time'] == 179, 'Longhorn cattle'])[0])-80)**2) +
        (((list(results.loc[results['Time'] == 179, 'Tamworth pigs'])[0])-10)**2) +
        # Jan 2020 
        (((list(results.loc[results['Time'] == 180, 'Longhorn cattle'])[0])-80)**2) +
        (((list(results.loc[results['Time'] == 180, 'Tamworth pigs'])[0])-10)**2) +
        # Feb 2020 
        (((list(results.loc[results['Time'] == 181, 'Longhorn cattle'])[0])-79)**2) +
        (((list(results.loc[results['Time'] == 181, 'Tamworth pigs'])[0])-8)**2) +
        # March 2021 
        (((list(results.loc[results['Time'] == 182, 'Fallow deer'])[0])-247)**2) +
        (((list(results.loc[results['Time'] == 182, 'Red deer'])[0])-35)**2) +
        (((list(results.loc[results['Time'] == 182, 'Tamworth pigs'])[0])-7)**2) +
        (((list(results.loc[results['Time'] == 182, 'Longhorn cattle'])[0])-81)**2) +
        # April 2021
        (((list(results.loc[results['Time'] == 183, 'Tamworth pigs'])[0])-7)**2) +
        (((list(results.loc[results['Time'] == 183, 'Longhorn cattle'])[0])-81)**2) +
        (((list(results.loc[results['Time'] == 183, 'Exmoor pony'])[0])-15)**2) +
        # # May 2021
        (((list(results.loc[results['Time'] == 184, 'Exmoor pony'])[0])-15)**2) +
        (((list(results.loc[results['Time'] == 184, 'Tamworth pigs'])[0])-19)**2) +
        (((list(results.loc[results['Time'] == 184, 'Longhorn cattle'])[0])-81)**2) +
        (((list(results.loc[results['Time'] == 184, 'Roe deer'])[0])-30)**2) +
        (((list(results.loc[results['Time'] == 184, 'Grassland'])[0])-59)**2) +
        (((list(results.loc[results['Time'] == 184, 'Thorny Scrub'])[0])-28)**2) +
        (((list(results.loc[results['Time'] == 184, 'Woodland'])[0])-19)**2))
                         

    # if filtered_result < 50000:
    print("r:", filtered_result)
    with pd.option_context('display.max_columns',None):
        print(results[results['Time'] == 49])
        print(results[results['Time'] == 184])

    return filtered_result
   

def run_optimizer():

    # time the program
    start = timeit.default_timer()


    # Define bounds
    bds = np.array([
        # habitat parameters
        [0.1,1],[0.1,1],[0.5,1],[0,0.001],[0,0.001],[0.1,1],[0.1,1],[0.1,1],[0.1,1],[0.1,1],[0.1,1],[0.1,1],
        # initial values
        [0.06,0.18],[0.75,0.85],[0.09,0.19],[0,0.06],
        # roe deer parameters
        [0.01,0.5],[0.5,1],[0.1,1],[0.1,1],[0.1,1],[0.1,1],
        # fallow deer parameters
        [0.1,0.5],[0.8,1],[0.1,1],[0.1,1],[0.1,1],[0.1,1],
        # red deer parameters
        [0.1,0.5],[0.7,1],[0.1,1],[0.1,1],[0.1,1],[0.1,1],
        # exmoor pony parameters
        [0.8,1],[0.1,1],[0.1,1],[0.1,1],[0.1,1],
        # cattle parameters
        [0.1,0.35],[0.6,1],[0.1,1],[0.1,1],[0.1,1],[0.1,1],
        # pig parameters
        [0.01,0.5],[0.5,1],[0.1,1],[0.1,1],
        # grass impact
        [0,1],[0,1],[0,1],[0,1],[0,1],[0.5,1],
        # sapling impact - assumed to not eat more than 10 per day
        [0.01,0.5],[0.01,0.5],[0.01,0.5],[0.01,0.5],[0.01,0.5],[0.01,0.5],
        # young scrub impact - assumed to not eat more than 10 per day
        [0.01,0.5],[0.01,0.5],[0.01,0.5],[0.01,0.5],[0.01,0.5],[0.01,0.5],
        # scrub impact - assumed to not eat more than 1 per day
        [0.01,0.5],[0.01,0.5],[0.01,0.5],[0.01,0.5],[0.01,0.5],
        # tree impact - assumed to not eat more than 1 per day
        [0.01,0.5],[0.01,0.5],[0.01,0.5],[0.01,0.5],[0.01,0.5], 
    ])

    algorithm_param = {'max_num_iteration': 100,\
                    'population_size':50,\
                    'mutation_probability':0.1,\
                    'elit_ratio': 0.01,\
                    'crossover_probability': 0.5,\
                    'parents_portion': 0.3,\
                    'crossover_type':'uniform',\
                    'max_iteration_without_improv':None}


    optimization =  ga(function = objectiveFunction, dimension = 77, variable_type = 'real',variable_boundaries= bds, algorithm_parameters = algorithm_param, function_timeout=6000)
    optimization.run()
    with open('optim_outputs.txt', 'w') as f:
        print('Optimization_outputs:', optimization.output_dict, file=f)
    print(optimization)

    # calculate the time it takes to run per node, currently 8.5min for 1k runs
    stop = timeit.default_timer()
    print('Total time: ', (stop - start)) 

    return optimization.output_dict
