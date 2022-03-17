# ------ Optimization of the Knepp ABM model --------
from KneppModel_ABM import KneppModel 
import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution
import seaborn as sns
import matplotlib.pyplot as plt
import sys

# ------ Optimization of the Knepp ABM model --------

popsize, maxiter = 1,1

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

    # define the parameters
    chance_reproduceSapling = x[0]
    chance_reproduceYoungScrub = x[1]
    chance_regrowGrass =x[2]
    chance_saplingBecomingTree =x[3]
    chance_youngScrubMatures =x[4]
    chance_scrubOutcompetedByTree = x[5]
    chance_grassOutcompetedByTree =x[6]
    chance_grassOutcompetedByScrub = x[7]
    chance_saplingOutcompetedByTree =x[8]
    chance_saplingOutcompetedByScrub = x[9]
    chance_youngScrubOutcompetedByScrub = x[10]
    chance_youngScrubOutcompetedByTree =x[11]
    # initial values
    initial_roeDeer = 0.12
    initial_grassland = 0.8
    initial_woodland = 0.14
    initial_scrubland = 0.01
    roeDeer_reproduce =x[12]
    roeDeer_gain_from_grass =x[13]
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
    pigs_gain_from_Trees = x[42]
    pigs_gain_from_Scrub = x[43]
    pigs_gain_from_grass =x[44]
    pigs_gain_from_Saplings =x[45]
    pigs_gain_from_YoungScrub = x[46]
    max_start_saplings = 0.1
    max_start_youngScrub = 0.1

    # run the model
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
        max_start_saplings, max_start_youngScrub,
        width = 25, height = 18, max_time = 184, reintroduction = True, 
        RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)
    model.run_model()

    # remember the results of the model (dominant conditions, # of agents)
    results = model.datacollector.get_model_vars_dataframe()
    
    # find the middle of each filter
    filtered_result = (
        # pre-reintro model
        ((((list(results.loc[results['Time'] == 49, 'Roe deer'])[0])-23)/23)**2) +
        (((list(results.loc[results['Time'] == 49, 'Grassland'])[0])-70)**2) +
        (((list(results.loc[results['Time'] == 49, 'Thorny Scrub'])[0])-13)**2) +
        (((list(results.loc[results['Time'] == 49, 'Woodland'])[0])-17)**2) +
        # post-reintro model: April 2015
        ((((list(results.loc[results['Time'] == 123, 'Longhorn cattle'])[0])-115)/115)**2) +
        ((((list(results.loc[results['Time'] == 123, 'Tamworth pigs'])[0])-22)/22)**2) +
        ((((list(results.loc[results['Time'] == 123, 'Exmoor pony'])[0])-10)/10)**2) +
        # # May 2015
        ((((list(results.loc[results['Time'] == 124, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 124, 'Longhorn cattle'])[0])-129)/129)**2) +
        ((((list(results.loc[results['Time'] == 124, 'Tamworth pigs'])[0])-14)/14)**2) +
        # June 2015
        ((((list(results.loc[results['Time'] == 125, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 125, 'Longhorn cattle'])[0])-129)/129)**2) +
        ((((list(results.loc[results['Time'] == 125, 'Tamworth pigs'])[0])-14)/14)**2) +
        # July 2015
        ((((list(results.loc[results['Time'] == 126, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 126, 'Longhorn cattle'])[0])-129)/129)**2) +
        ((((list(results.loc[results['Time'] == 126, 'Tamworth pigs'])[0])-14)/14)**2) +
        # Aug 2015
        ((((list(results.loc[results['Time'] == 127, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 127, 'Longhorn cattle'])[0])-129)/129)**2) +
        ((((list(results.loc[results['Time'] == 127, 'Tamworth pigs'])[0])-14)/14)**2) +
        # # Sept 2015
        ((((list(results.loc[results['Time'] == 128, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 128, 'Longhorn cattle'])[0])-130)/130)**2) +
        ((((list(results.loc[results['Time'] == 128, 'Tamworth pigs'])[0])-14)/14)**2) +
        # # Oct 2015
        ((((list(results.loc[results['Time'] == 129, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 129, 'Longhorn cattle'])[0])-91)/91)**2) +
        ((((list(results.loc[results['Time'] == 129, 'Tamworth pigs'])[0])-14)/14)**2) +
        # Nov 2015
        ((((list(results.loc[results['Time'] == 130, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 130, 'Longhorn cattle'])[0])-91)/91)**2) +
        ((((list(results.loc[results['Time'] == 130, 'Tamworth pigs'])[0])-13)/13)**2) +
        # # Dec 2015
        ((((list(results.loc[results['Time'] == 131, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 131, 'Longhorn cattle'])[0])-86)/86)**2) +
        ((((list(results.loc[results['Time'] == 131, 'Tamworth pigs'])[0])-13)/13)**2) +
        # # Jan 2016
        ((((list(results.loc[results['Time'] == 132, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 132, 'Longhorn cattle'])[0])-86)/86)**2) +
        ((((list(results.loc[results['Time'] == 132, 'Tamworth pigs'])[0])-10)/10)**2) +
        # # Feb 2016
        ((((list(results.loc[results['Time'] == 133, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 133, 'Longhorn cattle'])[0])-86)/86)**2) +
        ((((list(results.loc[results['Time'] == 133, 'Tamworth pigs'])[0])-8)/8)**2) +
        # # March 2016
        ((((list(results.loc[results['Time'] == 134, 'Fallow deer'])[0])-140)/140)**2) +
        ((((list(results.loc[results['Time'] == 134, 'Red deer'])[0])-26)/26)**2) +
        ((((list(results.loc[results['Time'] == 134, 'Tamworth pigs'])[0])-9)/9)**2) +
        ((((list(results.loc[results['Time'] == 134, 'Longhorn cattle'])[0])-86)/86)**2) +
        ((((list(results.loc[results['Time'] == 134, 'Exmoor pony'])[0])-11)/11)**2) +
        # # April 2016
        ((((list(results.loc[results['Time'] == 135, 'Longhorn cattle'])[0])-103)/103)**2) +
        ((((list(results.loc[results['Time'] == 135, 'Exmoor pony'])[0])-11)/11)**2) +
        ((((list(results.loc[results['Time'] == 135, 'Tamworth pigs'])[0])-9)/9)**2) +
        # # # May 2016
        ((((list(results.loc[results['Time'] == 136, 'Longhorn cattle'])[0])-108)/108)**2) +
        ((((list(results.loc[results['Time'] == 136, 'Tamworth pigs'])[0])-17)/17)**2) +
        ((((list(results.loc[results['Time'] == 136, 'Exmoor pony'])[0])-11)/11)**2) +
        # # June 2016
        ((((list(results.loc[results['Time'] == 137, 'Longhorn cattle'])[0])-89)/89)**2) +
        ((((list(results.loc[results['Time'] == 137, 'Exmoor pony'])[0])-11)/11)**2) +
        ((((list(results.loc[results['Time'] == 137, 'Tamworth pigs'])[0])-17)/17)**2) +
        # July 2016
        ((((list(results.loc[results['Time'] == 138, 'Exmoor pony'])[0])-11)/11)**2) +
        ((((list(results.loc[results['Time'] == 138, 'Tamworth pigs'])[0])-17)/17)**2) +
        ((((list(results.loc[results['Time'] == 138, 'Longhorn cattle'])[0])-87)/87)**2) +
        # # August 2016
        ((((list(results.loc[results['Time'] == 139, 'Exmoor pony'])[0])-11)/11)**2) +
        ((((list(results.loc[results['Time'] == 139, 'Tamworth pigs'])[0])-17)/17)**2) +
        ((((list(results.loc[results['Time'] == 139, 'Longhorn cattle'])[0])-87)/87)**2) +
        # # September 2016
        ((((list(results.loc[results['Time'] == 140, 'Exmoor pony'])[0])-11)/11)**2) +
        ((((list(results.loc[results['Time'] == 140, 'Tamworth pigs'])[0])-17)/17)**2) +
        ((((list(results.loc[results['Time'] == 140, 'Longhorn cattle'])[0])-97)/97)**2) +
        # # Oct 2016
        ((((list(results.loc[results['Time'] == 141, 'Exmoor pony'])[0])-11)/11)**2) +
        ((((list(results.loc[results['Time'] == 141, 'Tamworth pigs'])[0])-17)/17)**2) +
        ((((list(results.loc[results['Time'] == 141, 'Longhorn cattle'])[0])-97)/97)**2) +
        # # Nov 2016
        ((((list(results.loc[results['Time'] == 142, 'Exmoor pony'])[0])-11)/11)**2) +
        ((((list(results.loc[results['Time'] == 142, 'Tamworth pigs'])[0])-17)/17)**2) +
        ((((list(results.loc[results['Time'] == 142, 'Longhorn cattle'])[0])-92)/92)**2) +
        # # Dec 2016
        ((((list(results.loc[results['Time'] == 143, 'Exmoor pony'])[0])-11)/11)**2) +
        ((((list(results.loc[results['Time'] == 143, 'Tamworth pigs'])[0])-13)/13)**2) +
        ((((list(results.loc[results['Time'] == 143, 'Longhorn cattle'])[0])-79)/79)**2) +
        # # Jan 2017
        ((((list(results.loc[results['Time'] == 144, 'Exmoor pony'])[0])-11)/11)**2) +
        ((((list(results.loc[results['Time'] == 144, 'Tamworth pigs'])[0])-9)/9)**2) +
        ((((list(results.loc[results['Time'] == 144, 'Longhorn cattle'])[0])-79)/79)**2) +
        # # Feb 2017
        ((((list(results.loc[results['Time'] == 145, 'Exmoor pony'])[0])-11)/11)**2) +
        ((((list(results.loc[results['Time'] == 145, 'Tamworth pigs'])[0])-7)/7)**2) +
        ((((list(results.loc[results['Time'] == 145, 'Longhorn cattle'])[0])-79)/79)**2) +
        # # # March 2017
        ((((list(results.loc[results['Time'] == 146, 'Fallow deer'])[0])-165)/165)**2) +
        ((((list(results.loc[results['Time'] == 146, 'Longhorn cattle'])[0])-79)/79)**2) +
        ((((list(results.loc[results['Time'] == 146, 'Tamworth pigs'])[0])-7)/7)**2) +
        ((((list(results.loc[results['Time'] == 146, 'Exmoor pony'])[0])-10)/10)**2) +
        # # April 2017
        ((((list(results.loc[results['Time'] == 147, 'Longhorn cattle'])[0])-100)/100)**2) +
        ((((list(results.loc[results['Time'] == 147, 'Tamworth pigs'])[0])-22)/22)**2) +
        ((((list(results.loc[results['Time'] == 147, 'Exmoor pony'])[0])-10)/10)**2) +
        # # May 2017
        ((((list(results.loc[results['Time'] == 148, 'Longhorn cattle'])[0])-109)/109)**2) +
        ((((list(results.loc[results['Time'] == 148, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 148, 'Tamworth pigs'])[0])-22)/22)**2) +
        # June 2017
        ((((list(results.loc[results['Time'] == 149, 'Longhorn cattle'])[0])-94)/94)**2) +
        ((((list(results.loc[results['Time'] == 149, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 149, 'Tamworth pigs'])[0])-22)/22)**2) +
        # # July 2017
        ((((list(results.loc[results['Time'] == 150, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 150, 'Longhorn cattle'])[0])-94)/94)**2) +
        ((((list(results.loc[results['Time'] == 150, 'Tamworth pigs'])[0])-22)/22)**2) +
        # Aug 2017
        ((((list(results.loc[results['Time'] == 151, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 151, 'Longhorn cattle'])[0])-94)/94)**2) +
        ((((list(results.loc[results['Time'] == 151, 'Tamworth pigs'])[0])-22)/22)**2) +
        # # Sept 2017
        ((((list(results.loc[results['Time'] == 152, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 152, 'Longhorn cattle'])[0])-90)/90)**2) +
        ((((list(results.loc[results['Time'] == 152, 'Tamworth pigs'])[0])-22)/22)**2) +
        # # Oct 2017
        ((((list(results.loc[results['Time'] == 153, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 153, 'Longhorn cattle'])[0])-88)/88)**2) +
        ((((list(results.loc[results['Time'] == 153, 'Tamworth pigs'])[0])-22)/22)**2) +
        # # Nov 2017
        ((((list(results.loc[results['Time'] == 154, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 154, 'Longhorn cattle'])[0])-88)/88)**2) +
        ((((list(results.loc[results['Time'] == 154, 'Tamworth pigs'])[0])-22)/22)**2) +
        # # Dec 2017
        ((((list(results.loc[results['Time'] == 155, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 155, 'Longhorn cattle'])[0])-88)/88)**2) +
        ((((list(results.loc[results['Time'] == 155, 'Tamworth pigs'])[0])-18)/18)**2) +
        # # Jan 2018
        ((((list(results.loc[results['Time'] == 156, 'Tamworth pigs'])[0])-11)/11)**2) +
        ((((list(results.loc[results['Time'] == 156, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 156, 'Longhorn cattle'])[0])-88)/88)**2) +
        # # Feb 2018
        ((((list(results.loc[results['Time'] == 157, 'Exmoor pony'])[0])-10)/10)**2) +
        ((((list(results.loc[results['Time'] == 157, 'Tamworth pigs'])[0])-16)/16)**2) +
        ((((list(results.loc[results['Time'] == 157, 'Longhorn cattle'])[0])-88)/88)**2) +
        # March 2018
        ((((list(results.loc[results['Time'] == 158, 'Red deer'])[0])-24)/24)**2) +
        ((((list(results.loc[results['Time'] == 158, 'Longhorn cattle'])[0])-88)/88)**2) +
        ((((list(results.loc[results['Time'] == 158, 'Tamworth pigs'])[0])-16)/16)**2) +
        ((((list(results.loc[results['Time'] == 158, 'Exmoor pony'])[0])-9)/9)**2) +
        # April 2018
        ((((list(results.loc[results['Time'] == 159, 'Longhorn cattle'])[0])-101)/101)**2) +
        ((((list(results.loc[results['Time'] == 159, 'Exmoor pony'])[0])-9)/9)**2) +
        ((((list(results.loc[results['Time'] == 159, 'Tamworth pigs'])[0])-16)/16)**2) +
        # # May 2018
        ((((list(results.loc[results['Time'] == 160, 'Longhorn cattle'])[0])-117)/117)**2) +
        ((((list(results.loc[results['Time'] == 160, 'Tamworth pigs'])[0])-23)/23)**2) +
        ((((list(results.loc[results['Time'] == 160, 'Exmoor pony'])[0])-9)/9)**2) +
        # # June 2018
        ((((list(results.loc[results['Time'] == 161, 'Longhorn cattle'])[0])-103)/103)**2) +
        ((((list(results.loc[results['Time'] == 161, 'Exmoor pony'])[0])-9)/9)**2) +
        ((((list(results.loc[results['Time'] == 161, 'Tamworth pigs'])[0])-23)/23)**2) +
        # # July 2019
        ((((list(results.loc[results['Time'] == 162, 'Exmoor pony'])[0])-9)/9)**2) +
        ((((list(results.loc[results['Time'] == 162, 'Longhorn cattle'])[0])-103)/103)**2) +
        ((((list(results.loc[results['Time'] == 162, 'Tamworth pigs'])[0])-22)/22)**2) +
        # # # Aug 2019
        ((((list(results.loc[results['Time'] == 163, 'Longhorn cattle'])[0])-102)/102)**2) +
        ((((list(results.loc[results['Time'] == 163, 'Tamworth pigs'])[0])-22)/22)**2) +
        # # Sept 2019
        ((((list(results.loc[results['Time'] == 164, 'Longhorn cattle'])[0])-106)/106)**2) +
        ((((list(results.loc[results['Time'] == 164, 'Tamworth pigs'])[0])-22)/22)**2) +
        # # # Oct 2019
        ((((list(results.loc[results['Time'] == 165, 'Longhorn cattle'])[0])-101)/101)**2) +
        ((((list(results.loc[results['Time'] == 165, 'Tamworth pigs'])[0])-21)/21)**2) +
        # # # Nov 2019
        ((((list(results.loc[results['Time'] == 166, 'Longhorn cattle'])[0])-93)/93)**2) +
        ((((list(results.loc[results['Time'] == 166, 'Tamworth pigs'])[0])-9)/9)**2) +
        # # # Dec 2019
        ((((list(results.loc[results['Time'] == 167, 'Longhorn cattle'])[0])-89)/89)**2) +
        ((((list(results.loc[results['Time'] == 167, 'Tamworth pigs'])[0])-9)/9)**2) +
        # # # Jan 2020
        ((((list(results.loc[results['Time'] == 168, 'Longhorn cattle'])[0])-89)/89)**2) +
        ((((list(results.loc[results['Time'] == 168, 'Tamworth pigs'])[0])-9)/9)**2) +
        # # # Feb 2020
        ((((list(results.loc[results['Time'] == 169, 'Longhorn cattle'])[0])-87)/87)**2) +
        ((((list(results.loc[results['Time'] == 169, 'Tamworth pigs'])[0])-10)/10)**2) +
        # March 2019
        ((((list(results.loc[results['Time'] == 170, 'Fallow deer'])[0])-278)/278)**2) +
        (((list(results.loc[results['Time'] == 170, 'Red deer'])[0])-37)**2) +
        ((((list(results.loc[results['Time'] == 170, 'Longhorn cattle'])[0])-87)/87)**2) +
        ((((list(results.loc[results['Time'] == 170, 'Tamworth pigs'])[0])-9)/9)**2) +
        # # # April 2019
        ((((list(results.loc[results['Time'] == 171, 'Longhorn cattle'])[0])-101)/101)**2) +
        ((((list(results.loc[results['Time'] == 171, 'Tamworth pigs'])[0])-8)/8)**2) +
        # # # May 2019
        ((((list(results.loc[results['Time'] == 172, 'Longhorn cattle'])[0])-110)/110)**2) +
        ((((list(results.loc[results['Time'] == 172, 'Tamworth pigs'])[0])-8)/8)**2) +
        # # # June 2019
        ((((list(results.loc[results['Time'] == 173, 'Longhorn cattle'])[0])-89)/89)**2) +
        ((((list(results.loc[results['Time'] == 173, 'Tamworth pigs'])[0])-8)/8)**2) +
        # # # July 2019        
        ((((list(results.loc[results['Time'] == 174, 'Tamworth pigs'])[0])-9)/9)**2) +
        ((((list(results.loc[results['Time'] == 174, 'Longhorn cattle'])[0])-91)/91)**2) +
        # # Aug 2019 
        ((((list(results.loc[results['Time'] == 175, 'Longhorn cattle'])[0])-91)/91)**2) +
        ((((list(results.loc[results['Time'] == 175, 'Tamworth pigs'])[0])-9)/9)**2) +
        # # Sept 2019 
        ((((list(results.loc[results['Time'] == 176, 'Longhorn cattle'])[0])-93)/93)**2) +
        ((((list(results.loc[results['Time'] == 176, 'Tamworth pigs'])[0])-9)/9)**2) +
        # # Oct 2019 
        ((((list(results.loc[results['Time'] == 177, 'Longhorn cattle'])[0])-88)/88)**2) +
        ((((list(results.loc[results['Time'] == 177, 'Tamworth pigs'])[0])-9)/9)**2) +
        # Nov 2019 
        ((((list(results.loc[results['Time'] == 178, 'Longhorn cattle'])[0])-87)/87)**2) +
        ((((list(results.loc[results['Time'] == 178, 'Tamworth pigs'])[0])-9)/9)**2) +
        # # Dec 2019 
        ((((list(results.loc[results['Time'] == 179, 'Longhorn cattle'])[0])-80)/80)**2) +
        ((((list(results.loc[results['Time'] == 179, 'Tamworth pigs'])[0])-10)/10)**2) +
        # # Jan 2020 
        ((((list(results.loc[results['Time'] == 180, 'Longhorn cattle'])[0])-80)/80)**2) +
        ((((list(results.loc[results['Time'] == 180, 'Tamworth pigs'])[0])-10)/10)**2) +
        # # Feb 2020 
        ((((list(results.loc[results['Time'] == 181, 'Longhorn cattle'])[0])-79)/79)**2) +
        ((((list(results.loc[results['Time'] == 181, 'Tamworth pigs'])[0])-8)/8)**2) +
        # March 2021 
        ((((list(results.loc[results['Time'] == 182, 'Fallow deer'])[0])-247)/247)**2) +
        (((list(results.loc[results['Time'] == 182, 'Red deer'])[0])-35)**2) +
        ((((list(results.loc[results['Time'] == 182, 'Tamworth pigs'])[0])-7)/7)**2) +
        ((((list(results.loc[results['Time'] == 182, 'Longhorn cattle'])[0])-81)/81)**2) +
        # # April 2021
        ((((list(results.loc[results['Time'] == 183, 'Tamworth pigs'])[0])-7)/7)**2) +
        ((((list(results.loc[results['Time'] == 183, 'Longhorn cattle'])[0])-81)/81)**2) +
        ((((list(results.loc[results['Time'] == 183, 'Exmoor pony'])[0])-15)/15)**2) +
        # May 2021
        ((((list(results.loc[results['Time'] == 184, 'Exmoor pony'])[0])-15)/15)**2) +
        ((((list(results.loc[results['Time'] == 184, 'Tamworth pigs'])[0])-19)/19)**2) +
        ((((list(results.loc[results['Time'] == 184, 'Longhorn cattle'])[0])-81)/81)**2) +
        ((((list(results.loc[results['Time'] == 184, 'Roe deer'])[0])-50)/50)**2) +
        (((list(results.loc[results['Time'] == 184, 'Grassland'])[0])-57)**2) +
        (((list(results.loc[results['Time'] == 184, 'Thorny Scrub'])[0])-26)**2) +
        (((list(results.loc[results['Time'] == 184, 'Woodland'])[0])-19)**2)
        )

    # only print the last year's result if it's reasonably close to the filters
    if filtered_result < 10:
        print("r:", int(filtered_result))
        with pd.option_context('display.max_columns',None):
            just_nodes = results[results['Time'] == 184]
            print(just_nodes[["Time", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"]])
    else:
        print("n:", int(filtered_result))
    # return the output
    return filtered_result
   

def run_optimizer():
    # Define the bounds
    bds = [
        # habitat repro & growth
        (0.0037,0.0038),(0.0032,0.0034),(0.0135,0.014),(0.0023,0.0024),(0.0086,0.0087),
        (0.0011,0.0016), # mature scrub competition
        (0.094,0.095),(0.093,0.094), # grass
        (0.05,0.09),(0.015,0.02), # saplings
        (0.05,0.09),(0.05,0.09), # young scrub  
        # roe deer parameters
        (0.17,0.20),(0.93,0.95),(0.91,0.94),(0.91,0.94),(0.1,0.15),(0.05,0.12),
        # fallow deer parameters
        (0.315,0.32),(0.91,0.93),(0.9,0.92),(0.9,0.92),(0.1,0.13),(0.05,0.11),
        # red deer parameters
        (0.36,0.37),(0.91,0.93),(0.9,0.92),(0.9,0.92),(0.1,0.13),(0.05,0.11),
        # exmoor pony parameters
        (0.9,0.91),(0.89,0.91),(0.89,0.91),(0.1,0.12),(0.025,0.1),
        # cattle parameters
        (0.185,0.19),(0.9,0.91),(0.89,0.91),(0.89,0.91),(0.1,0.12),(0.025,0.1),
        # pig parameters
        (0.25,0.3),(0.85,0.89),(0.9,0.93),(0.9,0.93),(0.08,0.14),(0.075,0.12)]

    # popsize and maxiter are defined at the top of the page
    optimization = differential_evolution(objectiveFunction, bounds = bds, popsize = popsize, seed = 0, maxiter = maxiter, polish=False, args=({'Nfeval': 0},))
    
#     fun: 48.16998240731519
#  message: 'Maximum number of iterations has been exceeded.'
#     nfev: 94
#      nit: 1
#  success: False
#        x: array([0.0037389 , 0.00322869, 0.0139838 , 0.00232948, 0.00865091,
#        0.00199731, 0.09451909, 0.09333696, 0.08138607, 0.01685629,
#        0.07791945, 0.07842738, 0.1783482 , 0.9328174 , 0.9144764 ,
#        0.91391136, 0.11702867, 0.11623631, 0.31526015, 0.92255558,
#        0.89146959, 0.89571586, 0.11610159, 0.10764306, 0.36341145,
#        0.92949652, 0.9052971 , 0.89380651, 0.11747397, 0.08173538,
#        0.90420608, 0.89434907, 0.882705  , 0.10818295, 0.06682179,
#        0.18626336, 0.90102432, 0.89963841, 0.88759371, 0.09148747,
#        0.0842241 , 0.17226346, 0.8765768 , 0.90491902, 0.90649852,
#        0.10604675, 0.11007447])

#      fun: 7609.0
#  success: False
#        x: array([0.01544956, 0.04336282, 0.07412633, 0.00321202, 0.01445535,
#        0.01257575, 0.08587585, 0.08712148, 0.04722292, 0.03521732,
#        0.04899011, 0.03418888, 0.18596656, 0.75809749, 0.81723451,
#        0.80426454, 0.1527865 , 0.19676023, 0.39373449, 0.72450395,
#        0.76964124, 0.77460503, 0.18508269, 0.1096838 , 0.45777951,
#        0.68688409, 0.78039033, 0.79297531, 0.12888748, 0.13322385,
#        0.64859963, 0.72254674, 0.71662817, 0.13542455, 0.07409187,
#        0.23264077, 0.63862837, 0.73157247, 0.731689  , 0.12956036,
#        0.08408696, 0.18138512, 0.59043987, 0.70348958, 0.74483019,
#        0.10452791, 0.10536622])

    # save the results to a txt file
    with open('/Users/emilyneil/Desktop/KneppABM/outputs/post_reintro/differentialEvolution_outputs.txt', 'w') as f:
        print('Differential Evolution Outputs:', optimization, file=f)
    print(optimization)
    return optimization.x


def graph_results():
    output_parameters = run_optimizer()
    
    # define the parameters
    chance_reproduceSapling =output_parameters[0]
    chance_reproduceYoungScrub = output_parameters[1]
    chance_regrowGrass =output_parameters[2]
    chance_saplingBecomingTree = output_parameters[3]
    chance_youngScrubMatures = output_parameters[4]
    chance_scrubOutcompetedByTree =output_parameters[5]
    chance_grassOutcompetedByTree =output_parameters[6]
    chance_grassOutcompetedByScrub = output_parameters[7]
    chance_saplingOutcompetedByTree = output_parameters[8]
    chance_saplingOutcompetedByScrub = output_parameters[9]
    chance_youngScrubOutcompetedByScrub =output_parameters[10]
    chance_youngScrubOutcompetedByTree =output_parameters[11]
    # initial values
    initial_roeDeer = 0.12
    initial_grassland = 0.8
    initial_woodland = 0.14
    initial_scrubland = 0.01
    roeDeer_reproduce = output_parameters[12]
    roeDeer_gain_from_grass = output_parameters[13]
    roeDeer_gain_from_Trees = output_parameters[14]
    roeDeer_gain_from_Scrub = output_parameters[15]
    roeDeer_gain_from_Saplings =output_parameters[16]
    roeDeer_gain_from_YoungScrub =output_parameters[17]
    fallowDeer_reproduce = output_parameters[18]
    fallowDeer_gain_from_grass = output_parameters[19]
    fallowDeer_gain_from_Trees =output_parameters[20]
    fallowDeer_gain_from_Scrub = output_parameters[21]
    fallowDeer_gain_from_Saplings = output_parameters[22]
    fallowDeer_gain_from_YoungScrub = output_parameters[23]
    redDeer_reproduce =output_parameters[24]
    redDeer_gain_from_grass = output_parameters[25]
    redDeer_gain_from_Trees = output_parameters[26]
    redDeer_gain_from_Scrub = output_parameters[27]
    redDeer_gain_from_Saplings = output_parameters[28]
    redDeer_gain_from_YoungScrub = output_parameters[29]
    ponies_gain_from_grass = output_parameters[30]
    ponies_gain_from_Trees = output_parameters[31]
    ponies_gain_from_Scrub = output_parameters[32]
    ponies_gain_from_Saplings = output_parameters[33]
    ponies_gain_from_YoungScrub = output_parameters[34]
    cows_reproduce = output_parameters[35]
    cows_gain_from_grass = output_parameters[36]
    cows_gain_from_Trees = output_parameters[37]
    cows_gain_from_Scrub = output_parameters[38]
    cows_gain_from_Saplings = output_parameters[39]
    cows_gain_from_YoungScrub = output_parameters[40]
    pigs_reproduce = output_parameters[41]
    pigs_gain_from_grass = output_parameters[42]
    pigs_gain_from_Trees = output_parameters[43]
    pigs_gain_from_Scrub = output_parameters[44]
    pigs_gain_from_Saplings =output_parameters[45]
    pigs_gain_from_YoungScrub =output_parameters[46]
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
        pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Trees, pigs_gain_from_Scrub, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
        max_start_saplings, max_start_youngScrub,
        width = 25, height = 18, max_time = 184, reintroduction = True, 
        RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)
    model.run_model()

    # first graph:  does it pass the filters? looking at the number of individual trees, etc.
    final_results = model.datacollector.get_model_vars_dataframe()

    # y values - number of trees, scrub, etc. 
    y_values = final_results.drop(['Time', "Bare ground","Grassland", "Woodland", "Thorny Scrub", "Saplings grown up", "Saplings Outcompeted by Trees", "Saplings Outcompeted by Scrub", "Saplings eaten by roe deer", "Saplings eaten by Exmoor pony", "Saplings eaten by Fallow deer", "Saplings eaten by longhorn cattle", "Saplings eaten by red deer",  "Saplings eaten by pigs", "Young scrub grown up", "Young Scrub Outcompeted by Trees", "Young Scrub Outcompeted by Scrub", "Young Scrub eaten by roe deer", "Young Scrub eaten by Exmoor pony", 
    "Young Scrub eaten by Fallow deer", "Young Scrub eaten by longhorn cattle", "Young Scrub eaten by red deer", "Young Scrub eaten by pigs", 
    "Grass Outcompeted by Trees", "Grass Outcompeted by Scrub", "Grass eaten by roe deer", "Grass eaten by Exmoor pony", "Grass eaten by Fallow deer", "Grass eaten by longhorn cattle", "Grass eaten by red deer", "Grass eaten by pigs", 
    "Scrub Outcompeted by Trees", "Scrub eaten by roe deer", "Scrub eaten by Exmoor pony", "Scrub eaten by Fallow deer", "Scrub eaten by longhorn cattle", 
    "Scrub eaten by red deer", "Scrub eaten by pigs", "Trees eaten by roe deer", "Trees eaten by Exmoor pony", "Trees eaten by Fallow deer", "Trees eaten by longhorn cattle",  "Trees eaten by red deer", "Trees eaten by pigs", "Boars", "Sow", "Piglet"], axis=1).values.flatten()           
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
    axes[11].set_title("Bare Areas")
    # stop the plots from overlapping
    g.fig.suptitle("Optimizer Outputs")
    plt.tight_layout()
    plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/post_reintro/DE_PostReintro_numbers.png')
    plt.show()

    # does it pass the filters - conditions?
    y_values_conditions = final_results.drop(['Time', "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Saplings grown up", "Saplings Outcompeted by Trees", "Saplings Outcompeted by Scrub", "Saplings eaten by roe deer", "Saplings eaten by Exmoor pony", "Saplings eaten by Fallow deer", "Saplings eaten by longhorn cattle", "Saplings eaten by red deer",  "Saplings eaten by pigs", "Young scrub grown up", "Young Scrub Outcompeted by Trees", "Young Scrub Outcompeted by Scrub", "Young Scrub eaten by roe deer", "Young Scrub eaten by Exmoor pony", 
    "Young Scrub eaten by Fallow deer", "Young Scrub eaten by longhorn cattle", "Young Scrub eaten by red deer", "Young Scrub eaten by pigs", 
    "Grass Outcompeted by Trees", "Grass Outcompeted by Scrub", "Grass eaten by roe deer", "Grass eaten by Exmoor pony", "Grass eaten by Fallow deer", "Grass eaten by longhorn cattle", "Grass eaten by red deer", "Grass eaten by pigs", 
     "Scrub Outcompeted by Trees", "Scrub eaten by roe deer", "Scrub eaten by Exmoor pony", "Scrub eaten by Fallow deer", "Scrub eaten by longhorn cattle", 
     "Scrub eaten by red deer", "Scrub eaten by pigs", "Trees eaten by roe deer", "Trees eaten by Exmoor pony", "Trees eaten by Fallow deer", "Trees eaten by longhorn cattle",  "Trees eaten by red deer", "Trees eaten by pigs", "Boars", "Sow", "Piglet"], axis=1).values.flatten()            
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
    f.axes[6].vlines(x=184,ymin=49,ymax=69, color='r')
    f.axes[7].vlines(x=184,ymin=9,ymax=29, color='r')
    f.axes[8].vlines(x=184,ymin=21,ymax=35, color='r')
    # stop the plots from overlapping
    f.fig.suptitle("Optimizer Outputs")
    plt.tight_layout()
    plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/post_reintro/DE_PostReintro_conditions.png')
    plt.show()




    # How many pigs of each condition (sows, boars, piglets?)
    y_values = final_results.drop(['Time', "Bare ground","Grassland", "Woodland", "Thorny Scrub", "Saplings grown up", "Saplings Outcompeted by Trees", "Saplings Outcompeted by Scrub", "Saplings eaten by roe deer", "Saplings eaten by Exmoor pony", "Saplings eaten by Fallow deer", "Saplings eaten by longhorn cattle", "Saplings eaten by red deer",  "Saplings eaten by pigs", "Young scrub grown up", "Young Scrub Outcompeted by Trees", "Young Scrub Outcompeted by Scrub", "Young Scrub eaten by roe deer", "Young Scrub eaten by Exmoor pony", 
    "Young Scrub eaten by Fallow deer", "Young Scrub eaten by longhorn cattle", "Young Scrub eaten by red deer", "Young Scrub eaten by pigs", 
    "Grass Outcompeted by Trees", "Grass Outcompeted by Scrub", "Grass eaten by roe deer", "Grass eaten by Exmoor pony", "Grass eaten by Fallow deer", "Grass eaten by longhorn cattle", "Grass eaten by red deer", "Grass eaten by pigs", 
    "Scrub Outcompeted by Trees", "Scrub eaten by roe deer", "Scrub eaten by Exmoor pony", "Scrub eaten by Fallow deer", "Scrub eaten by longhorn cattle", 
    "Scrub eaten by red deer", "Scrub eaten by pigs", "Trees eaten by roe deer", "Trees eaten by Exmoor pony", "Trees eaten by Fallow deer", "Trees eaten by longhorn cattle",  "Trees eaten by red deer", "Trees eaten by pigs", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"], axis=1).values.flatten()           
    species_list = np.tile(["Boars", "Sow", "Piglet"], 185) 
    indices = np.repeat(final_results['Time'], 3)
    final_df = pd.DataFrame(
    {'Abundance': y_values, 'Ecosystem Element': species_list, 'Time': indices})
    colors = ["#6788ee"]
    g = sns.FacetGrid(final_df, col="Ecosystem Element", palette = colors, col_wrap=2, sharey = False)
    g.map(sns.lineplot, 'Time', 'Abundance')
    # add subplot titles
    axes = g.axes.flatten()
    # fill between the quantiles
    axes = g.axes.flatten()
    axes[0].set_title("Boars")
    axes[1].set_title("Sow")
    axes[2].set_title("Piglet")
    # stop the plots from overlapping
    g.fig.suptitle("How many pigs")
    plt.tight_layout()
    plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/post_reintro/DE_how_many_pigs.png')
    plt.show()


    # # # # # # REALITY CHECKS # # # # # # 

    # habitat deaths - stacked bar charts. what's killing saplings? 
    sapling_df = pd.DataFrame(
    {'Time': final_results['Time'], 'Grown up': final_results['Saplings grown up'], 'Outcompeted by Trees': final_results['Saplings Outcompeted by Trees'], 'Outcompeted by Scrub': final_results['Saplings Outcompeted by Scrub'], "Eaten by roe deer": final_results['Saplings eaten by roe deer'],
    "Eaten by Fallow deer": final_results['Saplings eaten by Fallow deer'],"Eaten by Exmoor pony": final_results['Saplings eaten by Exmoor pony'], "Eaten by longhorn cattle": final_results['Saplings eaten by longhorn cattle'], "Eaten by red deer": final_results['Saplings eaten by red deer'], "Eaten by pigs": final_results['Saplings eaten by pigs']})
    sapling_df.plot.bar(x='Time', stacked=True)
    plt.xticks([25, 50, 75, 100, 125, 150, 175])
    plt.ylabel('Amount Died')
    plt.title('What kills saplings?')
    plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/post_reintro/DE_Eaten_Saplings_PostReintro.png')
    plt.show()

    # habitat deaths - stacked bar charts. what's killing young scrub? 
    youngscrub_df = pd.DataFrame(
    {'Time': final_results['Time'], 'Grown up': final_results['Young scrub grown up'], 'Outcompeted by Trees': final_results['Young Scrub Outcompeted by Trees'], 'Outcompeted by Scrub': final_results['Young Scrub Outcompeted by Scrub'], "Eaten by roe deer": final_results['Young Scrub eaten by roe deer'],
    "Eaten by Fallow deer": final_results['Young Scrub eaten by Fallow deer'],"Eaten by Exmoor pony": final_results['Young Scrub eaten by Exmoor pony'], "Eaten by longhorn cattle": final_results['Young Scrub eaten by longhorn cattle'], "Eaten by red deer": final_results['Young Scrub eaten by red deer'], "Eaten by pigs": final_results['Young Scrub eaten by pigs']})
    youngscrub_df.plot.bar(x='Time', stacked=True)
    plt.xticks([25, 50, 75, 100, 125, 150, 175])
    plt.ylabel('Amount Died')
    plt.title('What kills young scrub?')
    plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/post_reintro/DE_Eaten_YoungScrub_PostReintro.png')
    plt.show()

    # habitat deaths - stacked bar charts. what's killing grass? 
    grass_df = pd.DataFrame(
    {'Time': final_results['Time'], 'Outcompeted by Trees': final_results['Grass Outcompeted by Trees'], 'Outcompeted by Scrub': final_results['Grass Outcompeted by Scrub'], "Eaten by roe deer": final_results['Grass eaten by roe deer'],
    "Eaten by Fallow deer": final_results['Grass eaten by Fallow deer'],"Eaten by Exmoor pony": final_results['Grass eaten by Exmoor pony'], "Eaten by longhorn cattle": final_results['Grass eaten by longhorn cattle'], "Eaten by red deer": final_results['Grass eaten by red deer'], "Eaten by pigs": final_results['Grass eaten by pigs']})
    grass_df.plot.bar(x='Time', stacked=True)
    plt.xticks([25, 50, 75, 100, 125, 150, 175])
    plt.ylabel('Amount Died')
    plt.title('What kills grass?')
    plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/post_reintro/DE_Eaten_Grass_PostReintro.png')
    plt.show()

    # habitat deaths - stacked bar charts. what's killing scrub? 
    scrub_df = pd.DataFrame(
    {'Time': final_results['Time'], 'Outcompeted by Trees': final_results['Scrub Outcompeted by Trees'], "Eaten by roe deer": final_results['Scrub eaten by roe deer'],
    "Eaten by Fallow deer": final_results['Scrub eaten by Fallow deer'],"Eaten by Exmoor pony": final_results['Scrub eaten by Exmoor pony'], "Eaten by longhorn cattle": final_results['Scrub eaten by longhorn cattle'], "Eaten by red deer": final_results['Scrub eaten by red deer'], "Eaten by pigs": final_results['Scrub eaten by pigs']})
    scrub_df.plot.bar(x='Time', stacked=True)
    plt.xticks([25, 50, 75, 100, 125, 150, 175])
    plt.ylabel('Amount Died')
    plt.title('What kills scrub?')
    plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/post_reintro/DE_Eaten_Scrub_PostReintro.png')
    plt.show()

    # habitat deaths - stacked bar charts. what's killing trees? 
    trees_df = pd.DataFrame(
    {'Time': final_results['Time'], "Eaten by roe deer": final_results['Trees eaten by roe deer'],
    "Eaten by Fallow deer": final_results['Trees eaten by Fallow deer'],"Eaten by Exmoor pony": final_results['Trees eaten by Exmoor pony'], "Eaten by longhorn cattle": final_results['Trees eaten by longhorn cattle'], "Eaten by red deer": final_results['Trees eaten by red deer'], "Eaten by pigs": final_results['Trees eaten by pigs']})
    trees_df.plot.bar(x='Time', stacked=True)
    plt.xticks([25, 50, 75, 100, 125, 150, 175])
    plt.ylabel('Amount Died')
    plt.title('What kills trees?')
    plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/post_reintro/DE_Eaten_Trees_PostReintro.png')
    plt.show()



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
        pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Trees, pigs_gain_from_Scrub, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
        max_start_saplings, max_start_youngScrub,
        width = 25, height = 18, max_time = 2500, reintroduction = False,
        RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)

    reality_check_6.run_model()
    results_reality6 = reality_check_6.datacollector.get_model_vars_dataframe()
    species_list_ages1 = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 2501) 
    indices_list_ages1 = np.repeat(results_reality6['Time'], 10)

    # y values
    y_values_reality6 = results_reality6.drop(['Time', "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas", "Saplings grown up", "Saplings Outcompeted by Trees", "Saplings Outcompeted by Scrub", "Saplings eaten by roe deer", "Saplings eaten by Exmoor pony", "Saplings eaten by Fallow deer", "Saplings eaten by longhorn cattle", "Saplings eaten by red deer",  "Saplings eaten by pigs", "Young scrub grown up", "Young Scrub Outcompeted by Trees", "Young Scrub Outcompeted by Scrub", "Young Scrub eaten by roe deer", "Young Scrub eaten by Exmoor pony", 
    "Young Scrub eaten by Fallow deer", "Young Scrub eaten by longhorn cattle", "Young Scrub eaten by red deer", "Young Scrub eaten by pigs", 
    "Grass Outcompeted by Trees", "Grass Outcompeted by Scrub", "Grass eaten by roe deer", "Grass eaten by Exmoor pony", "Grass eaten by Fallow deer", "Grass eaten by longhorn cattle", "Grass eaten by red deer", "Grass eaten by pigs", 
     "Scrub Outcompeted by Trees", "Scrub eaten by roe deer", "Scrub eaten by Exmoor pony", "Scrub eaten by Fallow deer", "Scrub eaten by longhorn cattle", 
     "Scrub eaten by red deer", "Scrub eaten by pigs", "Trees eaten by roe deer", "Trees eaten by Exmoor pony", "Trees eaten by Fallow deer", "Trees eaten by longhorn cattle",  "Trees eaten by red deer", "Trees eaten by pigs", "Boars", "Sow", "Piglet"], axis=1).values.flatten()
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
    plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/post_reintro/DE_RealityCheck_noHerbivores_preReintro_conditions.png')
    plt.show()


    y_values_reality61 = results_reality6.drop(['Time', "Grassland", "Woodland", "Thorny Scrub", "Bare ground", "Saplings grown up", "Saplings Outcompeted by Trees", "Saplings Outcompeted by Scrub", "Saplings eaten by roe deer", "Saplings eaten by Exmoor pony", "Saplings eaten by Fallow deer", "Saplings eaten by longhorn cattle", "Saplings eaten by red deer",  "Saplings eaten by pigs", "Young scrub grown up", "Young Scrub Outcompeted by Trees", "Young Scrub Outcompeted by Scrub", "Young Scrub eaten by roe deer", "Young Scrub eaten by Exmoor pony", 
    "Young Scrub eaten by Fallow deer", "Young Scrub eaten by longhorn cattle", "Young Scrub eaten by red deer", "Young Scrub eaten by pigs", 
    "Grass Outcompeted by Trees", "Grass Outcompeted by Scrub", "Grass eaten by roe deer", "Grass eaten by Exmoor pony", "Grass eaten by Fallow deer", "Grass eaten by longhorn cattle", "Grass eaten by red deer", "Grass eaten by pigs", 
     "Scrub Outcompeted by Trees", "Scrub eaten by roe deer", "Scrub eaten by Exmoor pony", "Scrub eaten by Fallow deer", "Scrub eaten by longhorn cattle", 
     "Scrub eaten by red deer", "Scrub eaten by pigs", "Trees eaten by roe deer", "Trees eaten by Exmoor pony", "Trees eaten by Fallow deer", "Trees eaten by longhorn cattle",  "Trees eaten by red deer","Trees eaten by pigs", "Boars", "Sow", "Piglet"], axis=1).values.flatten()
    
    species_list_ages = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"], 2501) 
    indices_list_ages = np.repeat(results_reality6['Time'], 12)
    
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
    plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/post_reintro/DE_RealityCheck_noHerbivores_preReintro.png')
    plt.show()




    # what if we run it a long time with no reintroductions

    reality_check_noReintro_long = KneppModel(
    chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
    chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
    initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland, 
    roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
    ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
    cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
    fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
    redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
    pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Trees, pigs_gain_from_Scrub, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
    max_start_saplings, max_start_youngScrub,
    width = 25, height = 18, max_time = 2500, reintroduction = False,
    RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)

    reality_check_noReintro_long.run_model()
    results_reality_long = reality_check_noReintro_long.datacollector.get_model_vars_dataframe()

    y_values_reality_long = results_reality_long.drop(['Time', "Grassland", "Woodland", "Thorny Scrub", "Bare ground", "Saplings grown up", "Saplings Outcompeted by Trees", "Saplings Outcompeted by Scrub", "Saplings eaten by roe deer", "Saplings eaten by Exmoor pony", "Saplings eaten by Fallow deer", "Saplings eaten by longhorn cattle", "Saplings eaten by red deer",  "Saplings eaten by pigs", "Young scrub grown up", "Young Scrub Outcompeted by Trees", "Young Scrub Outcompeted by Scrub", "Young Scrub eaten by roe deer", "Young Scrub eaten by Exmoor pony", 
    "Young Scrub eaten by Fallow deer", "Young Scrub eaten by longhorn cattle", "Young Scrub eaten by red deer", "Young Scrub eaten by pigs", 
    "Grass Outcompeted by Trees", "Grass Outcompeted by Scrub", "Grass eaten by roe deer", "Grass eaten by Exmoor pony", "Grass eaten by Fallow deer", "Grass eaten by longhorn cattle", "Grass eaten by red deer", "Grass eaten by pigs", 
     "Scrub Outcompeted by Trees", "Scrub eaten by roe deer", "Scrub eaten by Exmoor pony", "Scrub eaten by Fallow deer", "Scrub eaten by longhorn cattle", 
     "Scrub eaten by red deer", "Scrub eaten by pigs", "Trees eaten by roe deer", "Trees eaten by Exmoor pony", "Trees eaten by Fallow deer", "Trees eaten by longhorn cattle",  "Trees eaten by red deer","Trees eaten by pigs", "Boars", "Sow", "Piglet"], axis=1).values.flatten()

    species_list_long = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"], 2501) 
    indices_list_long = np.repeat(results_reality_long['Time'], 12)
    
    final_df_reality_long = pd.DataFrame(
    {'Abundance': y_values_reality_long, 'Ecosystem Element': species_list_long, 'Time': indices_list_long})
    # and graph it
    g_rc_long = sns.FacetGrid(final_df_reality_long, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    g_rc_long.map(sns.lineplot, 'Time', 'Abundance')
    axes = g_rc_long.axes.flatten()
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
    g_rc_long.fig.suptitle('Reality check: Roe deer only')
    plt.tight_layout()
    plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/post_reintro/DE_RealityCheck_noReintro_long.png')
    plt.show()

    return output_parameters



graph_results()