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
    initial_roeDeer = random.randint(6, 18)
    initial_grassland = random.randint(75, 85)
    initial_woodland = random.randint(9, 19)
    initial_scrubland = random.randint(0, 6)

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
    roeDeer_reproduce = x[12] 
    roeDeer_gain_from_grass = x[13] 
    roeDeer_gain_from_Trees = x[14] 
    roeDeer_gain_from_Scrub = x[15] 
    roeDeer_gain_from_Saplings = x[16] 
    roeDeer_gain_from_YoungScrub = x[17] 
    fallowDeer_reproduce = x[18] 
    fallowDeer_gain_from_grass = x[19] 
    fallowDeer_gain_from_Trees = x[20] 
    fallowDeer_gain_from_Scrub = x[21] 
    fallowDeer_gain_from_Saplings = x[22] 
    fallowDeer_gain_from_YoungScrub = x[23] 
    redDeer_reproduce = x[24] 
    redDeer_gain_from_grass = x[25] 
    redDeer_gain_from_Trees = x[26] 
    redDeer_gain_from_Scrub = x[27] 
    redDeer_gain_from_Saplings = x[28] 
    redDeer_gain_from_YoungScrub = x[29] 
    ponies_gain_from_grass = x[30] 
    ponies_gain_from_Trees = x[31] 
    ponies_gain_from_Scrub = x[32] 
    ponies_gain_from_Saplings = x[33] 
    ponies_gain_from_YoungScrub = x[34] 
    cows_reproduce = x[35] 
    cows_gain_from_grass = x[36] 
    cows_gain_from_Trees = x[37] 
    cows_gain_from_Scrub = x[38] 
    cows_gain_from_Saplings = x[39] 
    cows_gain_from_YoungScrub = x[40] 
    pigs_reproduce = x[41] 
    pigs_gain_from_grass = x[42]
    pigs_gain_from_Saplings = x[43]
    pigs_gain_from_YoungScrub = x[44]

    # put large herbivore impacts in order 
    # grass_impact_bds = list(x[49:55])
    # organized_grass = np.sort(grass_impact_bds)
    # roeDeer_impactGrass = int(organized_grass[0])
    roeDeer_impactGrass = round(x[45])
    fallowDeer_impactGrass = round(x[46])
    redDeer_impactGrass = round(x[47])
    ponies_impactGrass = round(x[48])
    cows_impactGrass = round(x[49])
    pigs_impactGrass = round(x[50])
    # saplings 
    # saplings_impact_bds = list(x[55:61])
    # organized_saplings = np.sort(saplings_impact_bds)
    roeDeer_saplingsEaten = round(x[51])
    fallowDeer_saplingsEaten = round(x[52])
    redDeer_saplingsEaten = round(x[53])
    ponies_saplingsEaten = round(x[54])
    cows_saplingsEaten = round(x[55])
    pigs_saplingsEaten = round(x[56])
    # young scrub 
    # youngScrub_impact_bds = list(x[61:67])
    # organized_youngScrub = np.sort(youngScrub_impact_bds)
    roeDeer_youngScrubEaten = round(x[57])
    fallowDeer_youngScrubEaten = round(x[58])
    redDeer_youngScrubEaten = round(x[59])
    ponies_youngScrubEaten = round(x[60])
    cows_youngScrubEaten = round(x[61])
    pigs_youngScrubEaten = round(x[62])
    # scrub eaten
    # scrub_impact_bds = list(x[67:72])
    # organizedScrub = np.sort(scrub_impact_bds)
    roeDeer_scrubEaten = round(x[63])
    fallowDeer_scrubEaten = round(x[64])
    redDeer_scrubEaten = round(x[65])
    ponies_scrubEaten = round(x[66])
    cows_scrubEaten = round(x[67])
    # trees eaten
    # trees_impact_bds = list(x[72:77])
    # organized_trees = np.sort(trees_impact_bds)
    roeDeer_treesEaten = round(x[68])
    fallowDeer_treesEaten = round(x[69])
    redDeer_treesEaten = round(x[70])
    ponies_treesEaten = round(x[71])
    cows_treesEaten = round(x[72])


    # # impact grass
    # roeDeer_impactGrass = random.randint(0,100)
    # fallowDeer_impactGrass=random.randint(roeDeer_impactGrass,100)
    # redDeer_impactGrass = random.randint(fallowDeer_impactGrass,100)
    # ponies_impactGrass = random.randint(redDeer_impactGrass,100)
    # cows_impactGrass = random.randint(ponies_impactGrass,100)
    # pigs_impactGrass = random.randint(cows_impactGrass,100)
    # # impact saplings
    # roeDeer_saplingsEaten = random.randint(0,5000)
    # fallowDeer_saplingsEaten = random.randint(roeDeer_saplingsEaten,5000)
    # redDeer_saplingsEaten = random.randint(fallowDeer_saplingsEaten,5000)
    # ponies_saplingsEaten = random.randint(redDeer_saplingsEaten,5000)
    # cows_saplingsEaten =  random.randint(ponies_saplingsEaten,5000)
    # pigs_saplingsEaten = random.randint(cows_saplingsEaten,5000)
    # # impact young scrub
    # roeDeer_youngScrubEaten = random.randint(0,5000)
    # fallowDeer_youngScrubEaten = random.randint(roeDeer_youngScrubEaten,5000)
    # redDeer_youngScrubEaten = random.randint(fallowDeer_youngScrubEaten,5000)
    # ponies_youngScrubEaten = random.randint(redDeer_youngScrubEaten,5000)
    # cows_youngScrubEaten = random.randint(ponies_youngScrubEaten,5000)
    # pigs_youngScrubEaten = random.randint(cows_youngScrubEaten,5000)
    # # impact scrub
    # roeDeer_scrubEaten = random.randint(0,500)
    # fallowDeer_scrubEaten = random.randint(roeDeer_scrubEaten,500)
    # redDeer_scrubEaten = random.randint(fallowDeer_scrubEaten,500)
    # ponies_scrubEaten = random.randint(redDeer_scrubEaten,500)
    # cows_scrubEaten = random.randint(ponies_scrubEaten,500)
    # # impact trees
    # roeDeer_treesEaten = random.randint(0,500)
    # fallowDeer_treesEaten = random.randint(roeDeer_treesEaten,500)
    # redDeer_treesEaten = random.randint(fallowDeer_treesEaten,500)
    # ponies_treesEaten = random.randint(redDeer_treesEaten,500)
    # cows_treesEaten =  random.randint(ponies_treesEaten,500)


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
        [0.1,0.9],[0.1,0.9],[0.4,1],[0.0001,0.001],[0.0001,0.005],[0.1,1],[0.1,1],[0.1,1],[0.1,1],[0.1,1],[0.1,1],[0.1,1],
        # roe deer parameters
        [0.05,0.2],[0.5,1],[0.1,1],[0.1,1],[0.1,1],[0.1,1],
        # fallow deer parameters
        [0.3,0.35],[0.5,1],[0.1,1],[0.1,1],[0.1,1],[0.1,1],
        # red deer parameters
        [0.1,0.3],[0.5,1],[0.1,1],[0.1,1],[0.1,1],[0.1,1],
        # exmoor pony parameters
        [0.5,1],[0.1,1],[0.1,1],[0.1,1],[0.1,1],
        # cattle parameters
        [0.1,0.25],[0.5,1],[0.1,1],[0.1,1],[0.1,1],[0.1,1],
        # pig parameters
        [0.01,0.15],[0.5,1],[0.1,1],[0.1,1],
        # grass impact
        [5,10],[20,25],[20,25],[25,45],[25,50],[50,100],
        # sapling impact - assumed to not eat more than 10 per day
        [25,75],[30,100],[50,150],[75,200],[75,200],[200,250],
        # young scrub impact - assumed to not eat more than 10 per day
        [25,75],[30,100],[50,150],[75,200],[75,200],[200,250],
        # scrub impact - assumed to not eat more than 1 per day
        [6,9],[10,14],[15,30],[15,30],[20,30],
        # tree impact - assumed to not eat more than 1 per day
        [6,9],[10,14],[15,30],[15,30],[20,30]
    ])

    algorithm_param = {'max_num_iteration': 10,\
                    'population_size':10,\
                    'mutation_probability':0.1,\
                    'elit_ratio': 0.01,\
                    'crossover_probability': 0.5,\
                    'parents_portion': 0.3,\
                    'crossover_type':'uniform',\
                    'max_iteration_without_improv':None}


    optimization =  ga(function = objectiveFunction, dimension = 73, variable_type = 'real',variable_boundaries= bds, algorithm_parameters = algorithm_param, function_timeout=6000)
    optimization.run()
    with open('optim_outputs.txt', 'w') as f:
        print('Optimization_outputs:', optimization.output_dict, file=f)
    print(optimization)

    # calculate the time it takes to run per node, currently 8.5min for 1k runs
    stop = timeit.default_timer()
    print('Total time: ', (stop - start)) 

    return optimization.output_dict
