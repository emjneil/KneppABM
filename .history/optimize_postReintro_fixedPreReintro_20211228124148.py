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
    chance_reproduceSapling = 0.11
    chance_reproduceYoungScrub = 0.26
    chance_regrowGrass = 0.27
    chance_saplingBecomingTree = 0.0042
    chance_youngScrubMatures = 0.0075
    chance_scrubOutcompetedByTree = 0.0012
    chance_grassOutcompetedByTree = 0.86
    chance_grassOutcompetedByScrub = 0.85
    chance_saplingOutcompetedByTree = 0.98
    chance_saplingOutcompetedByScrub = 0.011
    chance_youngScrubOutcompetedByScrub = 0.3
    chance_youngScrubOutcompetedByTree = 0.77
    # initial values
    initial_roeDeer = 0.12
    initial_grassland = 0.8
    initial_woodland = 0.14
    initial_scrubland = 0.01
    roeDeer_reproduce = 0.2
    roeDeer_gain_from_grass = 0.17
    roeDeer_gain_from_Trees = 0.2
    roeDeer_gain_from_Scrub = 0.2
    roeDeer_gain_from_Saplings = 0.014
    roeDeer_gain_from_YoungScrub = 0.01

    fallowDeer_reproduce = x[0]
    fallowDeer_gain_from_grass = x[1]
    fallowDeer_gain_from_Trees = x[2]
    fallowDeer_gain_from_Scrub = x[3]
    fallowDeer_gain_from_Saplings =x[4]
    fallowDeer_gain_from_YoungScrub =x[5]

    redDeer_reproduce = 0.29
    redDeer_gain_from_grass = 0.16
    redDeer_gain_from_Trees = 0.084
    redDeer_gain_from_Scrub = 0.16
    redDeer_gain_from_Saplings = 0.005
    redDeer_gain_from_YoungScrub = 0.0044

    pigs_reproduce = x[6]
    pigs_gain_from_grass =x[7]
    pigs_gain_from_Saplings =x[8]
    pigs_gain_from_YoungScrub = x[9]

    ponies_gain_from_grass = 0.03
    ponies_gain_from_Trees = 0.12
    ponies_gain_from_Scrub = 0.088
    ponies_gain_from_Saplings = 0.0014
    ponies_gain_from_YoungScrub = 0.006
    cows_reproduce = 0.23
    cows_gain_from_grass = 0.03
    cows_gain_from_Trees = 0.05
    cows_gain_from_Scrub = 0.05
    cows_gain_from_Saplings = 0.00075
    cows_gain_from_YoungScrub = 0.00075

    max_start_saplings = 0.012
    max_start_youngScrub = 0.025


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
        width = 50, height = 36, max_time = 184, reintroduction = True, 
        RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)
    model.run_model()

    # remember the results of the model (dominant conditions, # of agents)
    results = model.datacollector.get_model_vars_dataframe()
    
    # find the middle of each filter
    filtered_result = (
        # pre-reintro model
        (((list(results.loc[results['Time'] == 49, 'Roe deer'])[0])-23)**2) +
        (((list(results.loc[results['Time'] == 49, 'Grassland'])[0])-70)**2) +
        (((list(results.loc[results['Time'] == 49, 'Thorny Scrub'])[0])-13)**2) +
        (((list(results.loc[results['Time'] == 49, 'Woodland'])[0])-17)**2) +
        # post-reintro model: April 2015
        # (((list(results.loc[results['Time'] == 123, 'Longhorn cattle'])[0])-115)**2) +
        (((list(results.loc[results['Time'] == 123, 'Tamworth pigs'])[0])-22)**2) +
        (((list(results.loc[results['Time'] == 123, 'Exmoor pony'])[0])-10)**2) +
        # # May 2015
        (((list(results.loc[results['Time'] == 124, 'Exmoor pony'])[0])-10)**2) +
        # (((list(results.loc[results['Time'] == 124, 'Longhorn cattle'])[0])-129)**2) +
        (((list(results.loc[results['Time'] == 124, 'Tamworth pigs'])[0])-14)**2) +
        # June 2015
        (((list(results.loc[results['Time'] == 125, 'Exmoor pony'])[0])-10)**2) +
        # (((list(results.loc[results['Time'] == 125, 'Longhorn cattle'])[0])-129)**2) +
        (((list(results.loc[results['Time'] == 125, 'Tamworth pigs'])[0])-14)**2) +
        # July 2015
        (((list(results.loc[results['Time'] == 126, 'Exmoor pony'])[0])-10)**2) +
        # (((list(results.loc[results['Time'] == 126, 'Longhorn cattle'])[0])-129)**2) +
        (((list(results.loc[results['Time'] == 126, 'Tamworth pigs'])[0])-14)**2) +
        # Aug 2015
        (((list(results.loc[results['Time'] == 127, 'Exmoor pony'])[0])-10)**2) +
        # (((list(results.loc[results['Time'] == 127, 'Longhorn cattle'])[0])-129)**2) +
        (((list(results.loc[results['Time'] == 127, 'Tamworth pigs'])[0])-14)**2) +
        # # Sept 2015
        (((list(results.loc[results['Time'] == 128, 'Exmoor pony'])[0])-10)**2) +
        # (((list(results.loc[results['Time'] == 128, 'Longhorn cattle'])[0])-130)**2) +
        (((list(results.loc[results['Time'] == 128, 'Tamworth pigs'])[0])-14)**2) +
        # # Oct 2015
        (((list(results.loc[results['Time'] == 129, 'Exmoor pony'])[0])-10)**2) +
        # (((list(results.loc[results['Time'] == 129, 'Longhorn cattle'])[0])-91)**2) +
        (((list(results.loc[results['Time'] == 129, 'Tamworth pigs'])[0])-14)**2) +
        # Nov 2015
        (((list(results.loc[results['Time'] == 130, 'Exmoor pony'])[0])-10)**2) +
        # (((list(results.loc[results['Time'] == 130, 'Longhorn cattle'])[0])-91)**2) +
        (((list(results.loc[results['Time'] == 130, 'Tamworth pigs'])[0])-13)**2) +
        # # Dec 2015
        (((list(results.loc[results['Time'] == 131, 'Exmoor pony'])[0])-10)**2) +
        # (((list(results.loc[results['Time'] == 131, 'Longhorn cattle'])[0])-86)**2) +
        (((list(results.loc[results['Time'] == 131, 'Tamworth pigs'])[0])-13)**2) +
        # # Jan 2016
        (((list(results.loc[results['Time'] == 132, 'Exmoor pony'])[0])-10)**2) +
        # (((list(results.loc[results['Time'] == 132, 'Longhorn cattle'])[0])-86)**2) +
        (((list(results.loc[results['Time'] == 132, 'Tamworth pigs'])[0])-10)**2) +
        # # Feb 2016
        (((list(results.loc[results['Time'] == 133, 'Exmoor pony'])[0])-10)**2) +
        # (((list(results.loc[results['Time'] == 133, 'Longhorn cattle'])[0])-86)**2) +
        (((list(results.loc[results['Time'] == 133, 'Tamworth pigs'])[0])-8)**2) +
        # # March 2016
        (((list(results.loc[results['Time'] == 134, 'Fallow deer'])[0])-140)**2) +
        (((list(results.loc[results['Time'] == 134, 'Red deer'])[0])-26)**2) +
        (((list(results.loc[results['Time'] == 134, 'Tamworth pigs'])[0])-9)**2) +
        # (((list(results.loc[results['Time'] == 134, 'Longhorn cattle'])[0])-86)**2) +
        (((list(results.loc[results['Time'] == 134, 'Exmoor pony'])[0])-11)**2) +
        # # April 2016
        # (((list(results.loc[results['Time'] == 135, 'Longhorn cattle'])[0])-103)**2) +
        (((list(results.loc[results['Time'] == 135, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 135, 'Tamworth pigs'])[0])-9)**2) +
        # # # May 2016
        # (((list(results.loc[results['Time'] == 136, 'Longhorn cattle'])[0])-108)**2) +
        (((list(results.loc[results['Time'] == 136, 'Tamworth pigs'])[0])-17)**2) +
        (((list(results.loc[results['Time'] == 136, 'Exmoor pony'])[0])-11)**2) +
        # # June 2016
        # (((list(results.loc[results['Time'] == 137, 'Longhorn cattle'])[0])-89)**2) +
        (((list(results.loc[results['Time'] == 137, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 137, 'Tamworth pigs'])[0])-17)**2) +
        # July 2016
        (((list(results.loc[results['Time'] == 138, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 138, 'Tamworth pigs'])[0])-17)**2) +
        # (((list(results.loc[results['Time'] == 138, 'Longhorn cattle'])[0])-87)**2) +
        # # August 2016
        (((list(results.loc[results['Time'] == 139, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 139, 'Tamworth pigs'])[0])-17)**2) +
        # (((list(results.loc[results['Time'] == 139, 'Longhorn cattle'])[0])-87)**2) +
        # # September 2016
        (((list(results.loc[results['Time'] == 140, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 140, 'Tamworth pigs'])[0])-17)**2) +
        # (((list(results.loc[results['Time'] == 140, 'Longhorn cattle'])[0])-97)**2) +
        # # Oct 2016
        (((list(results.loc[results['Time'] == 141, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 141, 'Tamworth pigs'])[0])-17)**2) +
        # (((list(results.loc[results['Time'] == 141, 'Longhorn cattle'])[0])-97)**2) +
        # # Nov 2016
        (((list(results.loc[results['Time'] == 142, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 142, 'Tamworth pigs'])[0])-17)**2) +
        # (((list(results.loc[results['Time'] == 142, 'Longhorn cattle'])[0])-92)**2) +
        # # Dec 2016
        (((list(results.loc[results['Time'] == 143, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 143, 'Tamworth pigs'])[0])-13)**2) +
        # (((list(results.loc[results['Time'] == 143, 'Longhorn cattle'])[0])-79)**2) +
        # # Jan 2017
        (((list(results.loc[results['Time'] == 144, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 144, 'Tamworth pigs'])[0])-9)**2) +
        # (((list(results.loc[results['Time'] == 144, 'Longhorn cattle'])[0])-79)**2) +
        # # Feb 2017
        (((list(results.loc[results['Time'] == 145, 'Exmoor pony'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 145, 'Tamworth pigs'])[0])-7)**2) +
        # (((list(results.loc[results['Time'] == 145, 'Longhorn cattle'])[0])-79)**2) +
        # # # March 2017
        (((list(results.loc[results['Time'] == 146, 'Fallow deer'])[0])-165)**2) +
        # (((list(results.loc[results['Time'] == 146, 'Longhorn cattle'])[0])-79)**2) +
        (((list(results.loc[results['Time'] == 146, 'Tamworth pigs'])[0])-7)**2) +
        (((list(results.loc[results['Time'] == 146, 'Exmoor pony'])[0])-10)**2) +
        # # April 2017
        # (((list(results.loc[results['Time'] == 147, 'Longhorn cattle'])[0])-100)**2) +
        (((list(results.loc[results['Time'] == 147, 'Tamworth pigs'])[0])-22)**2) +
        (((list(results.loc[results['Time'] == 147, 'Exmoor pony'])[0])-10)**2) +
        # # May 2017
        # (((list(results.loc[results['Time'] == 148, 'Longhorn cattle'])[0])-109)**2) +
        (((list(results.loc[results['Time'] == 148, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 148, 'Tamworth pigs'])[0])-22)**2) +
        # June 2017
        # (((list(results.loc[results['Time'] == 149, 'Longhorn cattle'])[0])-94)**2) +
        (((list(results.loc[results['Time'] == 149, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 149, 'Tamworth pigs'])[0])-22)**2) +
        # # July 2017
        (((list(results.loc[results['Time'] == 150, 'Exmoor pony'])[0])-10)**2) +
        # (((list(results.loc[results['Time'] == 150, 'Longhorn cattle'])[0])-94)**2) +
        (((list(results.loc[results['Time'] == 150, 'Tamworth pigs'])[0])-22)**2) +
        # Aug 2017
        (((list(results.loc[results['Time'] == 151, 'Exmoor pony'])[0])-10)**2) +
        # (((list(results.loc[results['Time'] == 151, 'Longhorn cattle'])[0])-94)**2) +
        (((list(results.loc[results['Time'] == 151, 'Tamworth pigs'])[0])-22)**2) +
        # # Sept 2017
        (((list(results.loc[results['Time'] == 152, 'Exmoor pony'])[0])-10)**2) +
        # (((list(results.loc[results['Time'] == 152, 'Longhorn cattle'])[0])-90)**2) +
        (((list(results.loc[results['Time'] == 152, 'Tamworth pigs'])[0])-22)**2) +
        # # Oct 2017
        (((list(results.loc[results['Time'] == 153, 'Exmoor pony'])[0])-10)**2) +
        # (((list(results.loc[results['Time'] == 153, 'Longhorn cattle'])[0])-88)**2) +
        (((list(results.loc[results['Time'] == 153, 'Tamworth pigs'])[0])-22)**2) +
        # # Nov 2017
        (((list(results.loc[results['Time'] == 154, 'Exmoor pony'])[0])-10)**2) +
        # (((list(results.loc[results['Time'] == 154, 'Longhorn cattle'])[0])-88)**2) +
        (((list(results.loc[results['Time'] == 154, 'Tamworth pigs'])[0])-22)**2) +
        # # Dec 2017
        (((list(results.loc[results['Time'] == 155, 'Exmoor pony'])[0])-10)**2) +
        # (((list(results.loc[results['Time'] == 155, 'Longhorn cattle'])[0])-88)**2) +
        (((list(results.loc[results['Time'] == 155, 'Tamworth pigs'])[0])-18)**2) +
        # # Jan 2018
        (((list(results.loc[results['Time'] == 156, 'Tamworth pigs'])[0])-11)**2) +
        (((list(results.loc[results['Time'] == 156, 'Exmoor pony'])[0])-10)**2) +
        # (((list(results.loc[results['Time'] == 156, 'Longhorn cattle'])[0])-88)**2) +
        # # Feb 2018
        (((list(results.loc[results['Time'] == 157, 'Exmoor pony'])[0])-10)**2) +
        (((list(results.loc[results['Time'] == 157, 'Tamworth pigs'])[0])-16)**2) +
        # (((list(results.loc[results['Time'] == 157, 'Longhorn cattle'])[0])-88)**2) +
        # March 2018
        (((list(results.loc[results['Time'] == 158, 'Red deer'])[0])-24)**2) +
        # (((list(results.loc[results['Time'] == 158, 'Longhorn cattle'])[0])-88)**2) +
        (((list(results.loc[results['Time'] == 158, 'Tamworth pigs'])[0])-16)**2) +
        (((list(results.loc[results['Time'] == 158, 'Exmoor pony'])[0])-9)**2) +
        # April 2018
        # (((list(results.loc[results['Time'] == 159, 'Longhorn cattle'])[0])-101)**2) +
        (((list(results.loc[results['Time'] == 159, 'Exmoor pony'])[0])-9)**2) +
        (((list(results.loc[results['Time'] == 159, 'Tamworth pigs'])[0])-16)**2) +
        # # May 2018
        # (((list(results.loc[results['Time'] == 160, 'Longhorn cattle'])[0])-117)**2) +
        (((list(results.loc[results['Time'] == 160, 'Tamworth pigs'])[0])-23)**2) +
        (((list(results.loc[results['Time'] == 160, 'Exmoor pony'])[0])-9)**2) +
        # # June 2018
        # (((list(results.loc[results['Time'] == 161, 'Longhorn cattle'])[0])-103)**2) +
        (((list(results.loc[results['Time'] == 161, 'Exmoor pony'])[0])-9)**2) +
        (((list(results.loc[results['Time'] == 161, 'Tamworth pigs'])[0])-23)**2) +
        # # July 2019
        (((list(results.loc[results['Time'] == 162, 'Exmoor pony'])[0])-9)**2) +
        # (((list(results.loc[results['Time'] == 162, 'Longhorn cattle'])[0])-103)**2) +
        (((list(results.loc[results['Time'] == 162, 'Tamworth pigs'])[0])-22)**2) +
        # # # Aug 2019
        # (((list(results.loc[results['Time'] == 163, 'Longhorn cattle'])[0])-102)**2) +
        (((list(results.loc[results['Time'] == 163, 'Tamworth pigs'])[0])-22)**2) +
        # # Sept 2019
        # (((list(results.loc[results['Time'] == 164, 'Longhorn cattle'])[0])-106)**2) +
        (((list(results.loc[results['Time'] == 164, 'Tamworth pigs'])[0])-22)**2) +
        # # # Oct 2019
        # (((list(results.loc[results['Time'] == 165, 'Longhorn cattle'])[0])-101)**2) +
        (((list(results.loc[results['Time'] == 165, 'Tamworth pigs'])[0])-21)**2) +
        # # # Nov 2019
        # (((list(results.loc[results['Time'] == 166, 'Longhorn cattle'])[0])-93)**2) +
        (((list(results.loc[results['Time'] == 166, 'Tamworth pigs'])[0])-9)**2) +
        # # # Dec 2019
        # (((list(results.loc[results['Time'] == 167, 'Longhorn cattle'])[0])-89)**2) +
        (((list(results.loc[results['Time'] == 167, 'Tamworth pigs'])[0])-9)**2) +
        # # # Jan 2020
        # (((list(results.loc[results['Time'] == 168, 'Longhorn cattle'])[0])-89)**2) +
        (((list(results.loc[results['Time'] == 168, 'Tamworth pigs'])[0])-9)**2) +
        # # # Feb 2020
        # (((list(results.loc[results['Time'] == 169, 'Longhorn cattle'])[0])-87)**2) +
        (((list(results.loc[results['Time'] == 169, 'Tamworth pigs'])[0])-10)**2) +
        # March 2019
        (((list(results.loc[results['Time'] == 170, 'Fallow deer'])[0])-278)**2) +
        (((list(results.loc[results['Time'] == 170, 'Red deer'])[0])-37)**2) +
        # (((list(results.loc[results['Time'] == 170, 'Longhorn cattle'])[0])-87)**2) +
        (((list(results.loc[results['Time'] == 170, 'Tamworth pigs'])[0])-9)**2) +
        # # # April 2019
        # (((list(results.loc[results['Time'] == 171, 'Longhorn cattle'])[0])-101)**2) +
        (((list(results.loc[results['Time'] == 171, 'Tamworth pigs'])[0])-8)**2) +
        # # # May 2019
        # (((list(results.loc[results['Time'] == 172, 'Longhorn cattle'])[0])-110)**2) +
        (((list(results.loc[results['Time'] == 172, 'Tamworth pigs'])[0])-8)**2) +
        # # # June 2019
        # (((list(results.loc[results['Time'] == 173, 'Longhorn cattle'])[0])-89)**2) +
        (((list(results.loc[results['Time'] == 173, 'Tamworth pigs'])[0])-8)**2) +
        # # # July 2019        
        (((list(results.loc[results['Time'] == 174, 'Tamworth pigs'])[0])-9)**2) +
        # (((list(results.loc[results['Time'] == 174, 'Longhorn cattle'])[0])-91)**2) +
        # # Aug 2019 
        # (((list(results.loc[results['Time'] == 175, 'Longhorn cattle'])[0])-91)**2) +
        (((list(results.loc[results['Time'] == 175, 'Tamworth pigs'])[0])-9)**2) +
        # # Sept 2019 
        # (((list(results.loc[results['Time'] == 176, 'Longhorn cattle'])[0])-93)**2) +
        (((list(results.loc[results['Time'] == 176, 'Tamworth pigs'])[0])-9)**2) +
        # # Oct 2019 
        # (((list(results.loc[results['Time'] == 177, 'Longhorn cattle'])[0])-88)**2) +
        (((list(results.loc[results['Time'] == 177, 'Tamworth pigs'])[0])-9)**2) +
        # Nov 2019 
        # (((list(results.loc[results['Time'] == 178, 'Longhorn cattle'])[0])-87)**2) +
        (((list(results.loc[results['Time'] == 178, 'Tamworth pigs'])[0])-9)**2) +
        # # Dec 2019 
        # (((list(results.loc[results['Time'] == 179, 'Longhorn cattle'])[0])-80)**2) +
        (((list(results.loc[results['Time'] == 179, 'Tamworth pigs'])[0])-10)**2) +
        # # Jan 2020 
        # (((list(results.loc[results['Time'] == 180, 'Longhorn cattle'])[0])-80)**2) +
        (((list(results.loc[results['Time'] == 180, 'Tamworth pigs'])[0])-10)**2) +
        # # Feb 2020 
        # (((list(results.loc[results['Time'] == 181, 'Longhorn cattle'])[0])-79)**2) +
        (((list(results.loc[results['Time'] == 181, 'Tamworth pigs'])[0])-8)**2) +
        # March 2021 
        (((list(results.loc[results['Time'] == 182, 'Fallow deer'])[0])-247)**2) +
        (((list(results.loc[results['Time'] == 182, 'Red deer'])[0])-35)**2) +
        (((list(results.loc[results['Time'] == 182, 'Tamworth pigs'])[0])-7)**2) +
        # (((list(results.loc[results['Time'] == 182, 'Longhorn cattle'])[0])-81)**2) +
        # # April 2021
        (((list(results.loc[results['Time'] == 183, 'Tamworth pigs'])[0])-7)**2) +
        # (((list(results.loc[results['Time'] == 183, 'Longhorn cattle'])[0])-81)**2) +
        (((list(results.loc[results['Time'] == 183, 'Exmoor pony'])[0])-15)**2) +
        # May 2021
        (((list(results.loc[results['Time'] == 184, 'Exmoor pony'])[0])-15)**2) +
        (((list(results.loc[results['Time'] == 184, 'Tamworth pigs'])[0])-19)**2))
        # (((list(results.loc[results['Time'] == 184, 'Longhorn cattle'])[0])-81)**2))
        # (((list(results.loc[results['Time'] == 184, 'Roe deer'])[0])-50)**2) +
        # (((list(results.loc[results['Time'] == 184, 'Grassland'])[0])-57)**2) +
        # (((list(results.loc[results['Time'] == 184, 'Thorny Scrub'])[0])-26)**2) +
        # (((list(results.loc[results['Time'] == 184, 'Woodland'])[0])-19)**2))          


# fallow deer in VSC 
# pigs in terminal 

    if filtered_result < 10000:
        print("r:", filtered_result)
        with pd.option_context('display.max_columns',None):
            just_nodes1 = results[results['Time'] == 134]  # 140, 126-154
            just_nodes2 = results[results['Time'] == 146] # 165, 149-182
            just_nodes3 = results[results['Time'] == 170] # 278, 250-306
            just_nodes = results[results['Time'] == 182] # 247, 222-272
            print(just_nodes1[["Fallow deer"]])
            print(just_nodes2[["Fallow deer"]])
            print(just_nodes3[["Fallow deer"]])
            print(just_nodes[["Time", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"]])
    else:
        print("n:", filtered_result)

    return filtered_result
   

def run_optimizer():

    # Define bounds
    bds = np.array([
        # fallow deer parameters
        [0,0.25],[0,0.25],[0.1,0.2],[0.1,0.2],[0.001,0.05],[0.001,0.05]

        # # red deer parameters
        # [0.1,0.3],[0.1,0.17],[0,0.2],[0,0.2],[0,0.01],[0,0.01]
        # exmoor pony parameters
        # [0.025,0.1],[0.05,0.15],[0.05,0.15],[0.001,0.008],[0.001,0.008]

        # # cattle parameters
        # [0.2,0.27],[0.025,0.05],[0.025,0.075],[0.025,0.075],[0.0005,0.001],[0.0005,0.001],
        # # pig parameters
        [0,0.25],[0,0.05],[0,0.005],[0,0.005]
    ])

#  The best solution found: - fallow deer
#  [0.40345729 0.31554162 0.24875022 0.06005365 0.03751484 0.0791202 ]
#  Objective function:
#  1290.0

#  The best solution found: - pigs
#  [0.1911991  0.03709294 0.00090633 0.00080373]

#  Objective function:
#  1901.0


#  The best solution found: - red deer
#  [0.29227494 0.15634051 0.33529353 0.36480949 0.04978044 0.07954878]
#  Objective function:
#  29.0

# POST REINTRODUCTION
#  [0.24179841 0.067147   0.00871131 0.1103797  0.0071602  0.00875478
#  0.11277509 0.05171995 0.05998339 0.1112111  0.00576014 0.00102098
#  0.21625509 0.07191859 0.08724847 0.00426801 0.00372351 
#  0.11283141 0.14737943 0.13018309 0.10919425 0.00791606 0.01619882 
#  0.03549491 0.02399074 0.00905413 0.00165407]
#  Objective function:
#  36926.0

#  The best solution found (PRE REINTRODUCTION):
#  [0.10733116 0.25688679 0.26930773 0.00124404 0.86337655 0.8527727
#  0.98167675 0.01140952 0.29977736 0.76964111 0.20142497 0.17379685
#  0.20331529 0.19928593 0.01380466 0.00990924 0.01182659 0.02542889]
#  Objective function:
#  7.0

    algorithm_param = {'max_num_iteration': 25,\
                    'population_size':75,\
                    'mutation_probability':0.25,\
                    'elit_ratio': 0.01,\
                    'crossover_probability': 0.5,\
                    'parents_portion': 0.3,\
                    'crossover_type':'uniform',\
                    'max_iteration_without_improv': None}


    optimization =  ga(function = objectiveFunction, dimension = 10, variable_type = 'real',variable_boundaries= bds, algorithm_parameters = algorithm_param, function_timeout=6000)
    optimization.run()
    with open('optim_outputs_postReintro.txt', 'w') as f:
        print('Optimization_outputs:', optimization.output_dict, file=f)
    print(optimization)

    return optimization.output_dict




def graph_results():
    output_parameters = run_optimizer()

    # define the parameters
    chance_reproduceSapling = 0.11
    chance_reproduceYoungScrub = 0.26
    chance_regrowGrass = 0.27
    chance_saplingBecomingTree = 0.0042
    chance_youngScrubMatures = 0.0075
    chance_scrubOutcompetedByTree = 0.0012
    chance_grassOutcompetedByTree = 0.86
    chance_grassOutcompetedByScrub = 0.85
    chance_saplingOutcompetedByTree = 0.98
    chance_saplingOutcompetedByScrub = 0.011
    chance_youngScrubOutcompetedByScrub = 0.3
    chance_youngScrubOutcompetedByTree = 0.77
    # initial values
    initial_roeDeer = 0.12
    initial_grassland = 0.8
    initial_woodland = 0.14
    initial_scrubland = 0.01
    roeDeer_reproduce = 0.2
    roeDeer_gain_from_grass = 0.17
    roeDeer_gain_from_Trees = 0.2
    roeDeer_gain_from_Scrub = 0.2
    roeDeer_gain_from_Saplings = 0.014
    roeDeer_gain_from_YoungScrub = 0.01

    fallowDeer_reproduce = output_parameters["variable"][0]
    fallowDeer_gain_from_grass = output_parameters["variable"][1]
    fallowDeer_gain_from_Trees = output_parameters["variable"][2]
    fallowDeer_gain_from_Scrub = output_parameters["variable"][3]
    fallowDeer_gain_from_Saplings = output_parameters["variable"][4]
    fallowDeer_gain_from_YoungScrub = output_parameters["variable"][5]

    ponies_gain_from_grass = 0.03
    ponies_gain_from_Trees = 0.12
    ponies_gain_from_Scrub = 0.088
    ponies_gain_from_Saplings = 0.0014
    ponies_gain_from_YoungScrub = 0.006
    cows_reproduce = 0.23
    cows_gain_from_grass = 0.03
    cows_gain_from_Trees = 0.05
    cows_gain_from_Scrub = 0.05
    cows_gain_from_Saplings = 0.00075
    cows_gain_from_YoungScrub = 0.00075
    # cows_reproduce = output_parameters["variable"][6]
    # cows_gain_from_grass = output_parameters["variable"][7]
    # cows_gain_from_Trees = output_parameters["variable"][8]
    # cows_gain_from_Scrub =output_parameters["variable"][9]
    # cows_gain_from_Saplings = output_parameters["variable"][10] 
    # cows_gain_from_YoungScrub = output_parameters["variable"][11] 
    pigs_reproduce = output_parameters["variable"][0] 
    pigs_gain_from_grass = output_parameters["variable"][1] 
    pigs_gain_from_Saplings = output_parameters["variable"][2] 
    pigs_gain_from_YoungScrub = output_parameters["variable"][3] 
    redDeer_reproduce = 0.29
    redDeer_gain_from_grass = 0.16
    redDeer_gain_from_Trees = 0.084
    redDeer_gain_from_Scrub = 0.16
    redDeer_gain_from_Saplings = 0.005
    redDeer_gain_from_YoungScrub = 0.0044
    # ponies_gain_from_grass = 0.01
    # ponies_gain_from_Trees = 0.01
    # ponies_gain_from_Scrub = 0.01
    # ponies_gain_from_Saplings = 0.01 
    # ponies_gain_from_YoungScrub =0.01
    # cows_reproduce =0
    # cows_gain_from_grass = 0.01
    # cows_gain_from_Trees =0.01
    # cows_gain_from_Scrub = 0.01
    # cows_gain_from_Saplings =0.01
    # cows_gain_from_YoungScrub = 0.01
    pigs_reproduce = 0
    pigs_gain_from_grass =0.01
    pigs_gain_from_Saplings =0.01
    pigs_gain_from_YoungScrub = 0.01
    max_start_saplings = 0.012
    max_start_youngScrub = 0.025


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
        width = 50, height = 36, max_time = 184, reintroduction = True, 
        RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)
    model.run_model()

    # first graph:  does it pass the filters? looking at the number of individual trees, etc.
    final_results = model.datacollector.get_model_vars_dataframe()

    y_values = final_results.drop(['Time', "Bare ground","Grassland", "Woodland", "Thorny Scrub", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten()        
    species_list = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"], 185) 
    indices = np.repeat(final_results['Time'], 12)
    final_df = pd.DataFrame(
    {'Abundance': y_values, 'Ecosystem Element': species_list, 'Time': indices})
    colors = ["#6788ee"]
    g = sns.FacetGrid(final_df, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    g.map(sns.lineplot, 'Time', 'Abundance')
    # add subplot titles
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
    axes[11].set_title("Bare ground")
    # stop the plots from overlapping
    g.fig.suptitle("Optimizer Outputs")
    plt.tight_layout()
    plt.savefig('OptimOutputs_PostReintro_numbers.png')
    plt.show()

    # does it pass the filters - conditions?
    y_values_conditions = final_results.drop(['Time', "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Eaten Grass", "Eaten Trees", "Eaten Mature Scrub", "Eaten Saplings", "Eaten Young Scrub"], axis=1).values.flatten()        
    # species list. this should be +1 the number of simulations
    species_list_conditions = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 185) 
    # indices
    indices_conditions = np.repeat(final_results['Time'], 10)
    final_df_condit = pd.DataFrame(
    {'Abundance': y_values_conditions, 'Ecosystem Element': species_list_conditions, 'Time': indices_conditions})
    colors = ["#6788ee"]
    # first graph: counterfactual & forecasting
    f = sns.FacetGrid(final_df_condit, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    f.map(sns.lineplot, 'Time', 'Abundance')
    # add subplot titles
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
    f.axes[6].vlines(x=50,ymin=49,ymax=90, color='r')
    f.axes[7].vlines(x=50,ymin=7,ymax=27, color='r')
    f.axes[8].vlines(x=50,ymin=1,ymax=21, color='r')
    # plot post-reintro lines: April 2015
    f.axes[1].vlines(x=123,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=123,ymin=104,ymax=127, color='r')
    f.axes[5].vlines(x=123,ymin=20,ymax=24, color='r')
    # May 2015
    f.axes[3].vlines(x=124,ymin=116,ymax=142, color='r')
    f.axes[5].vlines(x=124,ymin=13,ymax=15, color='r')
    f.axes[1].vlines(x=124,ymin=9,ymax=11, color='r')
    # June 2015
    f.axes[3].vlines(x=125,ymin=116,ymax=142, color='r')
    f.axes[1].vlines(x=125,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=125,ymin=13,ymax=15, color='r')
    # July 2015
    f.axes[3].vlines(x=126,ymin=116,ymax=142, color='r')
    f.axes[1].vlines(x=126,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=126,ymin=13,ymax=15, color='r')
    # Aug 2015
    f.axes[3].vlines(x=127,ymin=116,ymax=142, color='r')
    f.axes[1].vlines(x=127,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=127,ymin=13,ymax=15, color='r')
    # Sept 2015
    f.axes[3].vlines(x=128,ymin=117,ymax=143, color='r')
    f.axes[1].vlines(x=128,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=128,ymin=13,ymax=15, color='r')
    # Oct 2015
    f.axes[3].vlines(x=129,ymin=82,ymax=100, color='r')
    f.axes[1].vlines(x=129,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=129,ymin=13,ymax=15, color='r')
    # Nov 2015
    f.axes[3].vlines(x=130,ymin=82,ymax=100, color='r')
    f.axes[1].vlines(x=130,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=130,ymin=12,ymax=14, color='r')
    # Dec 2015
    f.axes[3].vlines(x=131,ymin=77,ymax=94, color='r')
    f.axes[1].vlines(x=131,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=131,ymin=12,ymax=14, color='r')
    # Jan 2016
    f.axes[3].vlines(x=132,ymin=77,ymax=94, color='r')
    f.axes[1].vlines(x=132,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=132,ymin=9,ymax=11, color='r')
    # Feb 2016
    f.axes[1].vlines(x=133,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=133,ymin=77,ymax=94, color='r')
    f.axes[5].vlines(x=133,ymin=7,ymax=9, color='r')
    # March 2016
    f.axes[1].vlines(x=134,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=134,ymin=77,ymax=94, color='r')
    f.axes[2].vlines(x=134,ymin=126,ymax=154, color='r')
    f.axes[4].vlines(x=134,ymin=23,ymax=29, color='r')
    f.axes[5].vlines(x=134,ymin=8,ymax=10, color='r')
    # April 2016
    f.axes[1].vlines(x=135,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=135,ymin=93,ymax=113, color='r')
    f.axes[5].vlines(x=135,ymin=8,ymax=10, color='r')
    # May 2016
    f.axes[1].vlines(x=136,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=136,ymin=97,ymax=119, color='r')
    f.axes[5].vlines(x=136,ymin=15,ymax=19, color='r')
    # June 2016
    f.axes[1].vlines(x=137,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=137,ymin=80,ymax=98, color='r')
    f.axes[5].vlines(x=137,ymin=15,ymax=19, color='r')
    # July 2016
    f.axes[1].vlines(x=138,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=138,ymin=78,ymax=96, color='r')
    f.axes[5].vlines(x=138,ymin=15,ymax=19, color='r')
    # Aug 2016
    f.axes[1].vlines(x=139,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=139,ymin=78,ymax=96, color='r')
    f.axes[5].vlines(x=139,ymin=15,ymax=19, color='r')
    # Sept 2016
    f.axes[1].vlines(x=140,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=140,ymin=87,ymax=107, color='r')
    f.axes[5].vlines(x=140,ymin=15,ymax=19, color='r')
    # Oct 2016
    f.axes[1].vlines(x=141,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=141,ymin=87,ymax=107, color='r')
    f.axes[5].vlines(x=141,ymin=15,ymax=19, color='r')
    # Nov 2016
    f.axes[1].vlines(x=142,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=142,ymin=83,ymax=101, color='r')
    f.axes[5].vlines(x=142,ymin=15,ymax=19, color='r')
    # Dec 2016
    f.axes[1].vlines(x=143,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=143,ymin=71,ymax=87, color='r')
    f.axes[5].vlines(x=143,ymin=12,ymax=14, color='r')
    # Jan 2017
    f.axes[1].vlines(x=144,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=144,ymin=71,ymax=87, color='r')
    f.axes[5].vlines(x=144,ymin=8,ymax=10, color='r')
    # Feb 2017
    f.axes[1].vlines(x=145,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=145,ymin=71,ymax=87, color='r')
    f.axes[5].vlines(x=145,ymin=6,ymax=8, color='r')
    # March 2017
    f.axes[1].vlines(x=146,ymin=9,ymax=11, color='r')
    f.axes[2].vlines(x=146,ymin=149,ymax=182, color='r')
    f.axes[3].vlines(x=146,ymin=71,ymax=87, color='r')
    f.axes[5].vlines(x=146,ymin=6,ymax=8, color='r')
    # April 2017
    f.axes[1].vlines(x=147,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=147,ymin=90,ymax=110, color='r')
    f.axes[5].vlines(x=147,ymin=20,ymax=24, color='r')
    # May 2017
    f.axes[1].vlines(x=148,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=148,ymin=98,ymax=120, color='r')
    f.axes[5].vlines(x=148,ymin=20,ymax=24, color='r')
    # June 2017
    f.axes[1].vlines(x=149,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=149,ymin=85,ymax=103, color='r')
    f.axes[5].vlines(x=149,ymin=20,ymax=24, color='r')
    # July 2017
    f.axes[1].vlines(x=150,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=150,ymin=85,ymax=103, color='r')
    f.axes[5].vlines(x=150,ymin=20,ymax=24, color='r')
    # Aug 2017
    f.axes[1].vlines(x=151,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=151,ymin=85,ymax=103, color='r')
    f.axes[5].vlines(x=151,ymin=20,ymax=24, color='r')
    # Sept 2017
    f.axes[1].vlines(x=152,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=152,ymin=81,ymax=99, color='r')
    f.axes[5].vlines(x=152,ymin=20,ymax=24, color='r')
    # Oct 2017
    f.axes[1].vlines(x=153,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=153,ymin=79,ymax=97, color='r')
    f.axes[5].vlines(x=153,ymin=20,ymax=24, color='r')
    # Nov 2017
    f.axes[1].vlines(x=154,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=154,ymin=79,ymax=97, color='r')
    f.axes[5].vlines(x=154,ymin=20,ymax=24, color='r')
    # Dec 2017
    f.axes[1].vlines(x=155,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=155,ymin=79,ymax=97, color='r')
    f.axes[5].vlines(x=155,ymin=16,ymax=20, color='r')
    # Jan 2018
    f.axes[1].vlines(x=156,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=156,ymin=79,ymax=97, color='r')
    f.axes[5].vlines(x=156,ymin=10,ymax=12, color='r')
    # Feb 2018
    f.axes[1].vlines(x=157,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=157,ymin=79,ymax=97, color='r')
    f.axes[5].vlines(x=157,ymin=14,ymax=18, color='r')
    # March 2018
    f.axes[1].vlines(x=158,ymin=8,ymax=10, color='r')
    f.axes[2].vlines(x=158,ymin=226,ymax=276, color='r')
    f.axes[3].vlines(x=158,ymin=79,ymax=97, color='r')
    f.axes[4].vlines(x=158,ymin=22,ymax=26, color='r')
    f.axes[5].vlines(x=158,ymin=14,ymax=18, color='r')
    # April 2018
    f.axes[1].vlines(x=159,ymin=8,ymax=10, color='r')
    f.axes[3].vlines(x=159,ymin=91,ymax=111, color='r')
    f.axes[5].vlines(x=159,ymin=14,ymax=18, color='r')
    # May 2018
    f.axes[1].vlines(x=160,ymin=8,ymax=10, color='r')
    f.axes[3].vlines(x=160,ymin=105,ymax=129, color='r')
    f.axes[5].vlines(x=160,ymin=21,ymax=25, color='r')
    # June 2018
    f.axes[1].vlines(x=161,ymin=8,ymax=10, color='r')
    f.axes[3].vlines(x=161,ymin=93,ymax=113, color='r')
    f.axes[5].vlines(x=161,ymin=21,ymax=25, color='r')
    # July 2018
    f.axes[1].vlines(x=162,ymin=8,ymax=10, color='r')
    f.axes[3].vlines(x=162,ymin=93,ymax=113, color='r')
    f.axes[5].vlines(x=162,ymin=20,ymax=24, color='r')
    # Aug 2018
    f.axes[3].vlines(x=163,ymin=92,ymax=112, color='r')
    f.axes[5].vlines(x=163,ymin=20,ymax=24, color='r')
    # Sept 2018
    f.axes[3].vlines(x=164,ymin=95,ymax=117, color='r')
    f.axes[5].vlines(x=164,ymin=20,ymax=24, color='r')
    # Oct 2018
    f.axes[3].vlines(x=165,ymin=91,ymax=111, color='r')
    f.axes[5].vlines(x=165,ymin=19,ymax=23, color='r')
    # Nov 2018
    f.axes[3].vlines(x=166,ymin=84,ymax=102, color='r')
    f.axes[5].vlines(x=166,ymin=8,ymax=10, color='r')
    # Dec 2018
    f.axes[3].vlines(x=167,ymin=80,ymax=98, color='r')
    f.axes[5].vlines(x=167,ymin=8,ymax=10, color='r')
    # Jan 2019
    f.axes[3].vlines(x=168,ymin=80,ymax=98, color='r')
    f.axes[5].vlines(x=168,ymin=8,ymax=10, color='r')
    # Feb 2019
    f.axes[3].vlines(x=169,ymin=78,ymax=96, color='r')
    f.axes[5].vlines(x=169,ymin=9,ymax=11, color='r')
    # March 2019
    f.axes[2].vlines(x=170,ymin=250,ymax=306, color='r')
    f.axes[3].vlines(x=170,ymin=78,ymax=96, color='r')
    f.axes[4].vlines(x=170,ymin=33,ymax=41, color='r')
    f.axes[5].vlines(x=170,ymin=8,ymax=10, color='r')
    # April 2019
    f.axes[3].vlines(x=171,ymin=91,ymax=111, color='r')
    f.axes[5].vlines(x=171,ymin=7,ymax=9, color='r')
    # May 2019
    f.axes[3].vlines(x=172,ymin=99,ymax=121, color='r')
    f.axes[5].vlines(x=172,ymin=7,ymax=9, color='r')
    # June 2019
    f.axes[3].vlines(x=173,ymin=80,ymax=98, color='r')
    f.axes[5].vlines(x=173,ymin=7,ymax=9, color='r')
    # July 2019
    f.axes[3].vlines(x=174,ymin=82,ymax=100, color='r')
    f.axes[5].vlines(x=174,ymin=8,ymax=10, color='r')
    # Aug 2019
    f.axes[3].vlines(x=175,ymin=82,ymax=100, color='r')
    f.axes[5].vlines(x=175,ymin=8,ymax=10, color='r')  
    # Sept 2019
    f.axes[3].vlines(x=176,ymin=84,ymax=102, color='r')
    f.axes[5].vlines(x=176,ymin=8,ymax=10, color='r')
    # Oct 2019
    f.axes[3].vlines(x=177,ymin=79,ymax=97, color='r')
    f.axes[5].vlines(x=177,ymin=8,ymax=10, color='r')
    # Nov 2019
    f.axes[3].vlines(x=178,ymin=78,ymax=96, color='r')
    f.axes[5].vlines(x=178,ymin=8,ymax=10, color='r')
    # Dec 2019
    f.axes[3].vlines(x=179,ymin=72,ymax=88, color='r')
    f.axes[5].vlines(x=179,ymin=9,ymax=11, color='r')
    # Jan 2020
    f.axes[3].vlines(x=180,ymin=72,ymax=88, color='r')
    f.axes[5].vlines(x=180,ymin=9,ymax=11, color='r')
    # Feb 2020
    f.axes[3].vlines(x=181,ymin=71,ymax=87, color='r')
    f.axes[5].vlines(x=181,ymin=7,ymax=9, color='r')
    # March 2020
    f.axes[2].vlines(x=182,ymin=222,ymax=272, color='r')
    f.axes[4].vlines(x=182,ymin=32,ymax=39, color='r')
    f.axes[3].vlines(x=182,ymin=73,ymax=89, color='r')
    f.axes[5].vlines(x=182,ymin=6,ymax=8, color='r')
    # April 2020
    f.axes[1].vlines(x=183,ymin=14,ymax=17, color='r')
    f.axes[3].vlines(x=183,ymin=73,ymax=89, color='r')
    f.axes[5].vlines(x=183,ymin=6,ymax=8, color='r')
    # plot next set of filter lines
    f.axes[0].vlines(x=184,ymin=20,ymax=80, color='r')
    f.axes[1].vlines(x=184,ymin=14,ymax=17, color='r')
    f.axes[3].vlines(x=184,ymin=73,ymax=89, color='r')
    f.axes[5].vlines(x=184,ymin=17,ymax=21, color='r')
    f.axes[6].vlines(x=184,ymin=49,ymax=69, color='r')
    f.axes[7].vlines(x=184,ymin=9,ymax=29, color='r')
    f.axes[8].vlines(x=184,ymin=21,ymax=35, color='r')
    # stop the plots from overlapping
    f.fig.suptitle("Optimizer Outputs")
    plt.tight_layout()
    plt.savefig('OptimOutputs_PostReintro_conditions.png')
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
        width = 50, height = 36, max_time = 1000, reintroduction = True, 
        RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)
    reality_check_0.run_model()
    results_reality0 = reality_check_0.datacollector.get_model_vars_dataframe()
    # y values
    y_values_reality0 = results_reality0.drop(['Time'], axis=1).values.flatten()
    species_list_ages = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 1001) 
    indices_list_ages = np.repeat(results_reality0['Time'], 10)
    final_df_reality0 = pd.DataFrame(
    {'Abundance': y_values_reality0, 'Ecosystem Element': species_list_ages, 'Time': indices_list_ages})
    # first graph: counterfactual & forecasting
    g_rc0 = sns.FacetGrid(final_df_reality0, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    g_rc0.map(sns.lineplot, 'Time', 'Abundance')
    # add subplot titles
    axes = g_rc0.axes.flatten()
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
    g_rc0.fig.suptitle('Reality check: Simulate far into the future')
    plt.tight_layout()
    plt.savefig('RealityCheck_run1k_PostReintro.png')
    plt.show()



    # # 1. Do herbivores die in the absence of food? 
    # no_grassland = 0
    # no_woodland = 0
    # no_scrubland = 0
    # no_regrowing_grass = 0
    # reality_check_1 = KneppModel_noFood(
    #     chance_reproduceSapling, chance_reproduceYoungScrub, no_regrowing_grass, chance_saplingBecomingTree, chance_youngScrubMatures, 
    #     chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
    #     initial_roeDeer, no_grassland, no_woodland, no_scrubland, 
    #     roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
    #     ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
    #     cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
    #     fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
    #     redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
    #     pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
    #     max_start_saplings, max_start_youngScrub,
    #     width = 50, height = 36)
    # reality_check_1.run_model()
    # results_reality1 = reality_check_1.datacollector.get_model_vars_dataframe()
    # # y values
    # y_values_reality1 = results_reality1.drop(['Time'], axis=1).values.flatten()
    # final_df_reality1 = pd.DataFrame(
    # {'Abundance': y_values_reality1, 'Ecosystem Element': species_list, 'Time': indices})
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
    # plt.savefig('RealityCheck_noFoodForHerbivores_postReintro.png')
    # plt.show()
    


    # # 2. What happens if herbivores have unlimited food? (they gain 1 from everything)
    # gainTons_sapling = 1
    # gainTons_youngScrub = 1
    # gainTons_Trees = 1
    # gainTons_Scrub = 1
    # gainTons_Grass = 1
    # reality_check_2 = KneppModel(
    #     chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
    #     chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
    #     initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland, 
    #     roeDeer_reproduce, gainTons_Grass, gainTons_Trees, gainTons_Scrub, gainTons_sapling, gainTons_youngScrub,
    #     gainTons_Grass, gainTons_Trees, gainTons_Scrub, gainTons_sapling, gainTons_youngScrub, 
    #     cows_reproduce, gainTons_Grass, gainTons_Trees, gainTons_Scrub, gainTons_sapling, gainTons_youngScrub, 
    #     fallowDeer_reproduce, gainTons_Grass, gainTons_Trees, gainTons_Scrub, gainTons_sapling, gainTons_youngScrub, 
    #     redDeer_reproduce, gainTons_Grass, gainTons_Trees, gainTons_Scrub, gainTons_sapling, gainTons_youngScrub, 
    #     pigs_reproduce, gainTons_Grass, gainTons_sapling, gainTons_youngScrub, 
    #     width = 50, height = 36)
    # reality_check_2.run_model()
    # results_reality2 = reality_check_2.datacollector.get_model_vars_dataframe()
    # # y values
    # y_values_reality2 = results_reality2.drop(['Time'], axis=1).values.flatten()
    # final_df_reality2 = pd.DataFrame(
    # {'Abundance': y_values_reality2, 'Ecosystem Element': species_list, 'Time': indices})
    # # first graph: counterfactual & forecasting
    # g_rc2 = sns.FacetGrid(final_df_reality2, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    # g_rc2.map(sns.lineplot, 'Time', 'Abundance')
    # # add subplot titles
    # axes = g_rc2.axes.flatten()
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
    # g_rc2.fig.suptitle('Reality check: Unlimited food for herbivores')
    # plt.tight_layout()
    # plt.savefig('RealityCheck_UnlimitedFood_postReintro.png')
    # plt.show()



    # # 3. What if there's no competition for grassland (no thorny scrub or trees)? 
    # reality_check_3 = KneppModel_noFood(
    #     chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
    #     chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
    #     initial_roeDeer, initial_grassland, no_woodland, no_scrubland, 
    #     roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
    #     ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
    #     cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
    #     fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
    #     redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
    #     pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
    #     width = 50, height = 36)
    # reality_check_3.run_model()
    # results_reality3 = reality_check_3.datacollector.get_model_vars_dataframe()
    # # y values
    # y_values_reality3 = results_reality3.drop(['Time'], axis=1).values.flatten()
    # final_df_reality3 = pd.DataFrame(
    # {'Abundance': y_values_reality3, 'Ecosystem Element': species_list, 'Time': indices})
    # # first graph: counterfactual & forecasting
    # g_rc3 = sns.FacetGrid(final_df_reality3, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
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
    # plt.savefig('RealityCheck_noCompetitionForGrass_postReintro.png')
    # plt.show()



    # # 4. No competition for scrub (no trees)? 
    # reality_check_4 = KneppModel_noTrees(
    #     chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
    #     chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
    #     initial_roeDeer, initial_grassland, no_woodland, no_scrubland, 
    #     roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
    #     ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
    #     cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
    #     fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
    #     redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
    #     pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
    #     width = 50, height = 36)
    # reality_check_4.run_model()
    # results_reality4 = reality_check_4.datacollector.get_model_vars_dataframe()
    # # y values
    # y_values_reality4 = results_reality4.drop(['Time'], axis=1).values.flatten()
    # final_df_reality4 = pd.DataFrame(
    # {'Abundance': y_values_reality4, 'Ecosystem Element': species_list, 'Time': indices})
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
    # plt.savefig('RealityCheck_noCompetitionForScrub_postReintro.png')
    # plt.show()




    # # 5. No facilitation for tree saplings (no scrub)?
    # reality_check_5 = KneppModel_noScrub(
    #     chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
    #     chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
    #     initial_roeDeer, initial_grassland, no_woodland, initial_scrubland, 
    #     roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
    #     ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
    #     cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
    #     fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
    #     redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
    #     pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
    #     width = 50, height = 36)
    # reality_check_5.run_model()
    # results_reality5 = reality_check_5.datacollector.get_model_vars_dataframe()
    # # y values
    # y_values_reality5 = results_reality5.drop(['Time'], axis=1).values.flatten()
    # final_df_reality5 = pd.DataFrame(
    # {'Abundance': y_values_reality5, 'Ecosystem Element': species_list, 'Time': indices})
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
    # plt.savefig('RealityCheck_noFacilitation_postReintro.png')
    # plt.show()


    # # 6. What happens to habitats if there are no herbivores?
    # no_roe = 0
    # reality_check_6 = KneppModel_noHerbivores(
    #     chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
    #     chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
    #     no_roe, initial_grassland, initial_woodland, initial_scrubland, 
    #     roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
    #     ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
    #     cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
    #     fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
    #     redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
    #     pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
    #     width = 50, height = 36)
    # reality_check_6.run_model()
    # results_reality6 = reality_check_6.datacollector.get_model_vars_dataframe()
    # # y values
    # y_values_reality6 = results_reality6.drop(['Time'], axis=1).values.flatten()
    # final_df_reality6 = pd.DataFrame(
    # {'Abundance': y_values_reality6, 'Ecosystem Element': species_list, 'Time': indices})
    # # first graph: counterfactual & forecasting
    # g_rc6 = sns.FacetGrid(final_df_reality6, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    # g_rc6.map(sns.lineplot, 'Time', 'Abundance')
    # # add subplot titles
    # axes = g_rc6.axes.flatten()
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
    # g_rc6.fig.suptitle('Reality check: No herbivores')
    # plt.tight_layout()
    # plt.savefig('RealityCheck_noHerbivores_postReintro.png')
    # plt.show()


graph_results()