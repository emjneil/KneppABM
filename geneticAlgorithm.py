# ------ Optimization of the Knepp ABM model --------
from model import KneppModel 
import numpy as np
import pandas as pd
from geneticalgorithm import geneticalgorithm as ga
import seaborn as sns
import matplotlib.pyplot as plt
import sys

# ------ Optimization of the Knepp ABM model --------


def objectiveFunction(x):

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
    tamworth_pig_gain_from_trees = x[42]
    tamworth_pig_gain_from_scrub = x[43]
    tamworth_pig_gain_from_grass =x[44]
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
                        max_time = 185, reintroduction = True, introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)

    model.run_model()

    # remember the results of the model (dominant conditions, # of agents)
    results = model.datacollector.get_model_vars_dataframe()
    
    # find the middle of each filter
    filtered_result = (
        # pre-reintro model
        ((((list(results.loc[results['Time'] == 49, 'Roe deer'])[0])-26)/26)**2) +
        ((((list(results.loc[results['Time'] == 49, 'Grassland'])[0])-58.4)/58.4)**2) +
        ((((list(results.loc[results['Time'] == 49, 'Thorny Scrub'])[0])-12.7)/12.7)**2) +
        ((((list(results.loc[results['Time'] == 49, 'Woodland'])[0])-11.4)/11.4)**2) +

        # # post-reintro model: April 2015
        # ((((list(results.loc[results['Time'] == 123, 'Longhorn cattle'])[0])-115)/115)**2) +
        # ((((list(results.loc[results['Time'] == 123, 'Tamworth pigs'])[0])-22)/22)**2) +
        ((((list(results.loc[results['Time'] == 123, 'Exmoor pony'])[0])-10)/10)**2) +
        # # # May 2015
        # ((((list(results.loc[results['Time'] == 124, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 124, 'Longhorn cattle'])[0])-129)/129)**2) +
        # ((((list(results.loc[results['Time'] == 124, 'Tamworth pigs'])[0])-14)/14)**2) +
        # # June 2015
        # ((((list(results.loc[results['Time'] == 125, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 125, 'Longhorn cattle'])[0])-129)/129)**2) +
        # ((((list(results.loc[results['Time'] == 125, 'Tamworth pigs'])[0])-14)/14)**2) +
        # July 2015
        # ((((list(results.loc[results['Time'] == 126, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 126, 'Longhorn cattle'])[0])-129)/129)**2) +
        # ((((list(results.loc[results['Time'] == 126, 'Tamworth pigs'])[0])-14)/14)**2) +
        # # Aug 2015
        # ((((list(results.loc[results['Time'] == 127, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 127, 'Longhorn cattle'])[0])-129)/129)**2) +
        # ((((list(results.loc[results['Time'] == 127, 'Tamworth pigs'])[0])-14)/14)**2) +
        # # # Sept 2015
        # ((((list(results.loc[results['Time'] == 128, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 128, 'Longhorn cattle'])[0])-130)/130)**2) +
        # ((((list(results.loc[results['Time'] == 128, 'Tamworth pigs'])[0])-14)/14)**2) +
        # # # Oct 2015
        # ((((list(results.loc[results['Time'] == 129, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 129, 'Longhorn cattle'])[0])-91)/91)**2) +
        # ((((list(results.loc[results['Time'] == 129, 'Tamworth pigs'])[0])-14)/14)**2) +
        # # Nov 2015
        # ((((list(results.loc[results['Time'] == 130, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 130, 'Longhorn cattle'])[0])-91)/91)**2) +
        # ((((list(results.loc[results['Time'] == 130, 'Tamworth pigs'])[0])-13)/13)**2) +
        # # # Dec 2015
        # ((((list(results.loc[results['Time'] == 131, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 131, 'Longhorn cattle'])[0])-86)/86)**2) +
        # ((((list(results.loc[results['Time'] == 131, 'Tamworth pigs'])[0])-13)/13)**2) +
        # # # Jan 2016
        # ((((list(results.loc[results['Time'] == 132, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 132, 'Longhorn cattle'])[0])-86)/86)**2) +
        # ((((list(results.loc[results['Time'] == 132, 'Tamworth pigs'])[0])-10)/10)**2) +
        # # # Feb 2016
        # ((((list(results.loc[results['Time'] == 133, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 133, 'Longhorn cattle'])[0])-86)/86)**2) +
        # ((((list(results.loc[results['Time'] == 133, 'Tamworth pigs'])[0])-8)/8)**2) +
        # March 2016
        # ((((list(results.loc[results['Time'] == 134, 'Fallow deer'])[0])-140)/140)**2) +
        # ((((list(results.loc[results['Time'] == 134, 'Red deer'])[0])-26)/26)**2) +
        # ((((list(results.loc[results['Time'] == 134, 'Tamworth pigs'])[0])-9)/9)**2) +
        # ((((list(results.loc[results['Time'] == 134, 'Longhorn cattle'])[0])-86)/86)**2) +
        ((((list(results.loc[results['Time'] == 134, 'Exmoor pony'])[0])-11)/11)**2) +
        # # # # April 2016
        # ((((list(results.loc[results['Time'] == 135, 'Longhorn cattle'])[0])-103)/103)**2) +
        # ((((list(results.loc[results['Time'] == 135, 'Exmoor pony'])[0])-11)/11)**2) +
        # ((((list(results.loc[results['Time'] == 135, 'Tamworth pigs'])[0])-9)/9)**2) +
        # # # # May 2016
        # ((((list(results.loc[results['Time'] == 136, 'Longhorn cattle'])[0])-108)/108)**2) +
        # ((((list(results.loc[results['Time'] == 136, 'Tamworth pigs'])[0])-17)/17)**2) +
        # ((((list(results.loc[results['Time'] == 136, 'Exmoor pony'])[0])-11)/11)**2) +
        # # # June 2016
        # ((((list(results.loc[results['Time'] == 137, 'Longhorn cattle'])[0])-89)/89)**2) +
        # ((((list(results.loc[results['Time'] == 137, 'Exmoor pony'])[0])-11)/11)**2) +
        # ((((list(results.loc[results['Time'] == 137, 'Tamworth pigs'])[0])-17)/17)**2) +
        # # July 2016
        # ((((list(results.loc[results['Time'] == 138, 'Exmoor pony'])[0])-11)/11)**2) +
        # ((((list(results.loc[results['Time'] == 138, 'Tamworth pigs'])[0])-17)/17)**2) +
        # ((((list(results.loc[results['Time'] == 138, 'Longhorn cattle'])[0])-87)/87)**2) +
        # # # August 2016
        # ((((list(results.loc[results['Time'] == 139, 'Exmoor pony'])[0])-11)/11)**2) +
        # ((((list(results.loc[results['Time'] == 139, 'Tamworth pigs'])[0])-17)/17)**2) +
        # ((((list(results.loc[results['Time'] == 139, 'Longhorn cattle'])[0])-87)/87)**2) +
        # # # September 2016
        # ((((list(results.loc[results['Time'] == 140, 'Exmoor pony'])[0])-11)/11)**2) +
        # ((((list(results.loc[results['Time'] == 140, 'Tamworth pigs'])[0])-17)/17)**2) +
        # ((((list(results.loc[results['Time'] == 140, 'Longhorn cattle'])[0])-97)/97)**2) +
        # # # Oct 2016
        # ((((list(results.loc[results['Time'] == 141, 'Exmoor pony'])[0])-11)/11)**2) +
        # ((((list(results.loc[results['Time'] == 141, 'Tamworth pigs'])[0])-17)/17)**2) +
        # ((((list(results.loc[results['Time'] == 141, 'Longhorn cattle'])[0])-97)/97)**2) +
        # # # Nov 2016
        # ((((list(results.loc[results['Time'] == 142, 'Exmoor pony'])[0])-11)/11)**2) +
        # ((((list(results.loc[results['Time'] == 142, 'Tamworth pigs'])[0])-17)/17)**2) +
        # ((((list(results.loc[results['Time'] == 142, 'Longhorn cattle'])[0])-92)/92)**2) +
        # # # Dec 2016
        # ((((list(results.loc[results['Time'] == 143, 'Exmoor pony'])[0])-11)/11)**2) +
        # ((((list(results.loc[results['Time'] == 143, 'Tamworth pigs'])[0])-13)/13)**2) +
        # ((((list(results.loc[results['Time'] == 143, 'Longhorn cattle'])[0])-79)/79)**2) +
        # # # Jan 2017
        # ((((list(results.loc[results['Time'] == 144, 'Exmoor pony'])[0])-11)/11)**2) +
        # ((((list(results.loc[results['Time'] == 144, 'Tamworth pigs'])[0])-9)/9)**2) +
        # ((((list(results.loc[results['Time'] == 144, 'Longhorn cattle'])[0])-79)/79)**2) +
        # # # Feb 2017
        # ((((list(results.loc[results['Time'] == 145, 'Exmoor pony'])[0])-11)/11)**2) +
        # ((((list(results.loc[results['Time'] == 145, 'Tamworth pigs'])[0])-7)/7)**2) +
        # ((((list(results.loc[results['Time'] == 145, 'Longhorn cattle'])[0])-79)/79)**2) +
        # March 2017
        # ((((list(results.loc[results['Time'] == 146, 'Fallow deer'])[0])-165)/165)**2) +
        # ((((list(results.loc[results['Time'] == 146, 'Longhorn cattle'])[0])-79)/79)**2) +
        # ((((list(results.loc[results['Time'] == 146, 'Tamworth pigs'])[0])-7)/7)**2) +
        ((((list(results.loc[results['Time'] == 146, 'Exmoor pony'])[0])-10)/10)**2) +
        # # # April 2017
        # ((((list(results.loc[results['Time'] == 147, 'Longhorn cattle'])[0])-100)/100)**2) +
        # ((((list(results.loc[results['Time'] == 147, 'Tamworth pigs'])[0])-22)/22)**2) +
        ((((list(results.loc[results['Time'] == 147, 'Exmoor pony'])[0])-10)/10)**2) +
        # # # May 2017
        # ((((list(results.loc[results['Time'] == 148, 'Longhorn cattle'])[0])-109)/109)**2) +
        ((((list(results.loc[results['Time'] == 148, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 148, 'Tamworth pigs'])[0])-22)/22)**2) +
        # # June 2017
        # ((((list(results.loc[results['Time'] == 149, 'Longhorn cattle'])[0])-94)/94)**2) +
        ((((list(results.loc[results['Time'] == 149, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 149, 'Tamworth pigs'])[0])-22)/22)**2) +
        # # # July 2017
        ((((list(results.loc[results['Time'] == 150, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 150, 'Longhorn cattle'])[0])-94)/94)**2) +
        # ((((list(results.loc[results['Time'] == 150, 'Tamworth pigs'])[0])-22)/22)**2) +
        # # Aug 2017
        ((((list(results.loc[results['Time'] == 151, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 151, 'Longhorn cattle'])[0])-94)/94)**2) +
        # ((((list(results.loc[results['Time'] == 151, 'Tamworth pigs'])[0])-22)/22)**2) +
        # # # Sept 2017
        ((((list(results.loc[results['Time'] == 152, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 152, 'Longhorn cattle'])[0])-90)/90)**2) +
        # ((((list(results.loc[results['Time'] == 152, 'Tamworth pigs'])[0])-22)/22)**2) +
        # # # Oct 2017
        ((((list(results.loc[results['Time'] == 153, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 153, 'Longhorn cattle'])[0])-88)/88)**2) +
        # ((((list(results.loc[results['Time'] == 153, 'Tamworth pigs'])[0])-22)/22)**2) +
        # # # Nov 2017
        ((((list(results.loc[results['Time'] == 154, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 154, 'Longhorn cattle'])[0])-88)/88)**2) +
        # ((((list(results.loc[results['Time'] == 154, 'Tamworth pigs'])[0])-22)/22)**2) +
        # # # Dec 2017
        # ((((list(results.loc[results['Time'] == 155, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 155, 'Longhorn cattle'])[0])-88)/88)**2) +
        # ((((list(results.loc[results['Time'] == 155, 'Tamworth pigs'])[0])-18)/18)**2) +
        # # # Jan 2018
        # ((((list(results.loc[results['Time'] == 156, 'Tamworth pigs'])[0])-11)/11)**2) +
        ((((list(results.loc[results['Time'] == 156, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 156, 'Longhorn cattle'])[0])-88)/88)**2) +
        # # # Feb 2018
        ((((list(results.loc[results['Time'] == 157, 'Exmoor pony'])[0])-10)/10)**2) +
        # ((((list(results.loc[results['Time'] == 157, 'Tamworth pigs'])[0])-16)/16)**2) +
        # ((((list(results.loc[results['Time'] == 157, 'Longhorn cattle'])[0])-88)/88)**2) +
        # March 2018
        # ((((list(results.loc[results['Time'] == 158, 'Red deer'])[0])-24)/24)**2) +
        # ((((list(results.loc[results['Time'] == 158, 'Longhorn cattle'])[0])-88)/88)**2) +
        # ((((list(results.loc[results['Time'] == 158, 'Tamworth pigs'])[0])-16)/16)**2) +
        ((((list(results.loc[results['Time'] == 158, 'Exmoor pony'])[0])-9)/9)**2) +
        # # # April 2018
        # # ((((list(results.loc[results['Time'] == 159, 'Longhorn cattle'])[0])-101)/101)**2) +
        # ((((list(results.loc[results['Time'] == 159, 'Exmoor pony'])[0])-9)/9)**2) +
        # ((((list(results.loc[results['Time'] == 159, 'Tamworth pigs'])[0])-16)/16)**2) +
        # # # May 2018
        # ((((list(results.loc[results['Time'] == 160, 'Longhorn cattle'])[0])-117)/117)**2) +
        # ((((list(results.loc[results['Time'] == 160, 'Tamworth pigs'])[0])-23)/23)**2) +
        # ((((list(results.loc[results['Time'] == 160, 'Exmoor pony'])[0])-9)/9)**2) +
        # # # June 2018
        # ((((list(results.loc[results['Time'] == 161, 'Longhorn cattle'])[0])-103)/103)**2) +
        # ((((list(results.loc[results['Time'] == 161, 'Exmoor pony'])[0])-9)/9)**2) +
        # ((((list(results.loc[results['Time'] == 161, 'Tamworth pigs'])[0])-23)/23)**2) +
        # # # July 2019
        ((((list(results.loc[results['Time'] == 162, 'Exmoor pony'])[0])-9)/9)**2) +
        # ((((list(results.loc[results['Time'] == 162, 'Longhorn cattle'])[0])-103)/103)**2) +
        # ((((list(results.loc[results['Time'] == 162, 'Tamworth pigs'])[0])-22)/22)**2) +
        # # # # Aug 2019
        # ((((list(results.loc[results['Time'] == 163, 'Longhorn cattle'])[0])-102)/102)**2) +
        # ((((list(results.loc[results['Time'] == 163, 'Tamworth pigs'])[0])-22)/22)**2) +
        # # # Sept 2019
        # ((((list(results.loc[results['Time'] == 164, 'Longhorn cattle'])[0])-106)/106)**2) +
        # ((((list(results.loc[results['Time'] == 164, 'Tamworth pigs'])[0])-22)/22)**2) +
        # # # # Oct 2019
        # ((((list(results.loc[results['Time'] == 165, 'Longhorn cattle'])[0])-101)/101)**2) +
        # ((((list(results.loc[results['Time'] == 165, 'Tamworth pigs'])[0])-21)/21)**2) +
        # # # # Nov 2019
        # ((((list(results.loc[results['Time'] == 166, 'Longhorn cattle'])[0])-93)/93)**2) +
        # ((((list(results.loc[results['Time'] == 166, 'Tamworth pigs'])[0])-9)/9)**2) +
        # # # # Dec 2019
        # ((((list(results.loc[results['Time'] == 167, 'Longhorn cattle'])[0])-89)/89)**2) +
        # ((((list(results.loc[results['Time'] == 167, 'Tamworth pigs'])[0])-9)/9)**2) +
        # # # # Jan 2020
        # ((((list(results.loc[results['Time'] == 168, 'Longhorn cattle'])[0])-89)/89)**2) +
        # ((((list(results.loc[results['Time'] == 168, 'Tamworth pigs'])[0])-9)/9)**2) +
        # # # # Feb 2020
        # ((((list(results.loc[results['Time'] == 169, 'Longhorn cattle'])[0])-87)/87)**2) +
        # ((((list(results.loc[results['Time'] == 169, 'Tamworth pigs'])[0])-10)/10)**2) +
        # March 2019
        # ((((list(results.loc[results['Time'] == 170, 'Fallow deer'])[0])-278)/278)**2) +
        # ((((list(results.loc[results['Time'] == 170, 'Red deer'])[0])-37)/37)**2) +
        # ((((list(results.loc[results['Time'] == 170, 'Longhorn cattle'])[0])-87)/87)**2) +
        # ((((list(results.loc[results['Time'] == 170, 'Tamworth pigs'])[0])-9)/9)**2) +
        # # # # April 2019
        # ((((list(results.loc[results['Time'] == 171, 'Longhorn cattle'])[0])-101)/101)**2) +
        # ((((list(results.loc[results['Time'] == 171, 'Tamworth pigs'])[0])-8)/8)**2) +
        # # # # May 2019
        # ((((list(results.loc[results['Time'] == 172, 'Longhorn cattle'])[0])-110)/110)**2) +
        # ((((list(results.loc[results['Time'] == 172, 'Tamworth pigs'])[0])-8)/8)**2) +
        # # # # June 2019
        # ((((list(results.loc[results['Time'] == 173, 'Longhorn cattle'])[0])-89)/89)**2) +
        # ((((list(results.loc[results['Time'] == 173, 'Tamworth pigs'])[0])-8)/8)**2) +
        # # # # July 2019        
        # ((((list(results.loc[results['Time'] == 174, 'Tamworth pigs'])[0])-9)/9)**2) +
        # ((((list(results.loc[results['Time'] == 174, 'Longhorn cattle'])[0])-91)/91)**2) +
        # # # Aug 2019 
        # ((((list(results.loc[results['Time'] == 175, 'Longhorn cattle'])[0])-91)/91)**2) +
        # ((((list(results.loc[results['Time'] == 175, 'Tamworth pigs'])[0])-9)/9)**2) +
        # # # Sept 2019 
        # ((((list(results.loc[results['Time'] == 176, 'Longhorn cattle'])[0])-93)/93)**2) +
        # ((((list(results.loc[results['Time'] == 176, 'Tamworth pigs'])[0])-9)/9)**2) +
        # # # Oct 2019 
        # ((((list(results.loc[results['Time'] == 177, 'Longhorn cattle'])[0])-88)/88)**2) +
        # ((((list(results.loc[results['Time'] == 177, 'Tamworth pigs'])[0])-9)/9)**2) +
        # # Nov 2019 
        # ((((list(results.loc[results['Time'] == 178, 'Longhorn cattle'])[0])-87)/87)**2) +
        # ((((list(results.loc[results['Time'] == 178, 'Tamworth pigs'])[0])-9)/9)**2) +
        # # # Dec 2019 
        # ((((list(results.loc[results['Time'] == 179, 'Longhorn cattle'])[0])-80)/80)**2) +
        # ((((list(results.loc[results['Time'] == 179, 'Tamworth pigs'])[0])-10)/10)**2) +
        # # # Jan 2020 
        # ((((list(results.loc[results['Time'] == 180, 'Longhorn cattle'])[0])-80)/80)**2) +
        # ((((list(results.loc[results['Time'] == 180, 'Tamworth pigs'])[0])-10)/10)**2) +
        # # # Feb 2020 
        # ((((list(results.loc[results['Time'] == 181, 'Longhorn cattle'])[0])-79)/79)**2) +
        # ((((list(results.loc[results['Time'] == 181, 'Tamworth pigs'])[0])-8)/8)**2) +
        # # March 2021 
        # ((((list(results.loc[results['Time'] == 182, 'Fallow deer'])[0])-247)/247)**2) +
        # ((((list(results.loc[results['Time'] == 182, 'Red deer'])[0])-35)/35)**2) +
        # ((((list(results.loc[results['Time'] == 182, 'Tamworth pigs'])[0])-7)/7)**2) +
        # ((((list(results.loc[results['Time'] == 182, 'Longhorn cattle'])[0])-81)/81)**2) +
        # # # April 2021
        # ((((list(results.loc[results['Time'] == 183, 'Tamworth pigs'])[0])-7)/7)**2) +
        # ((((list(results.loc[results['Time'] == 183, 'Longhorn cattle'])[0])-81)/81)**2) +
        ((((list(results.loc[results['Time'] == 183, 'Exmoor pony'])[0])-15)/15)**2) +
        # May 2021
        ((((list(results.loc[results['Time'] == 184, 'Exmoor pony'])[0])-15)/15)**2)
        # ((((list(results.loc[results['Time'] == 184, 'Tamworth pigs'])[0])-19)/19)**2) +
        # ((((list(results.loc[results['Time'] == 184, 'Longhorn cattle'])[0])-81)/81)**2) +
        # ((((list(results.loc[results['Time'] == 184, 'Roe deer'])[0])-50)/50)**2) +
        # ((((list(results.loc[results['Time'] == 184, 'Grassland'])[0])-26.8)/26.8)**2) +
        # ((((list(results.loc[results['Time'] == 184, 'Thorny Scrub'])[0])-51.8)/51.8)**2) +
        # ((((list(results.loc[results['Time'] == 184, 'Woodland'])[0])-21.5)/21.5)**2)      
         )

    # only print the last year's result if it's reasonably close to the filters
    if filtered_result < 10:
        print("r:", filtered_result)
        with pd.option_context('display.max_columns',None):
            just_nodes = results[results['Time'] == 184]
            print(just_nodes[["Time", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"]])
    else:
        print("n:", int(filtered_result))
    # return the output
    return filtered_result
   

def run_optimizer():
    # Define the bounds
    bds = np.array([
        [0,0.15],[0,0.15],[0.1,1],[0.001,0.005],[0.0025,0.025],
        [0,0.1], # mature scrub competition
        [0,0.1],[0,0.1], # grass
        [0,0.1],[0,0.1], # saplings
        [0,0.1],[0,0.1], # young scrub 
        # roe deer parameters
        [0.13,0.2],[0.7,1],[0.7,1],[0.5,1],[0,0.5],[0,0.5],
        # fallow deer parameters
        [0.28,0.3],[0.5,1],[0.4,1],[0.1,1],[0,0.5],[0,0.5],
        # red deer parameters
        [0.3,0.35],[0.4,1],[0.4,1],[0.1,1],[0,0.5],[0,0.5],
        # exmoor pony parameters
                    [0.3,1],[0.4,1],[0.1,1],[0,0.5],[0,0.5],
        # cattle parameters
        [0.18,0.2],[0.25,1],[0.3,1],[0.1,1],[0,0.5],[0,0.5],
        # pig parameters
        [0.33,0.35],[0.1,1],[0,1],[0,1],[0,0.5],[0,0.5]])

#  [0.10719667 0.03794083 0.99782111 0.00129944 0.03545324 0.36514799
#  0.54504865 0.61012509 0.82048947 0.27410968 0.7761421  0.11078935
#  0.12223506 0.48985377 0.52272807 0.75623978 0.203387   0.9963075
#  0.29123401 0.62614995 0.54106028 0.67277476 0.75364159 0.69184503
#  0.3397313  0.48804847 0.429809   0.61966094 0.07756558 0.62974428
#  0.63742293 0.6993552  0.32279283 0.29488305 0.63867909 0.19191731
#  0.56828674 0.12692419 0.17619645 0.53204822 0.33129289 0.33975284
#  0.53624514 0.87668461 0.08158304 0.40413896 0.25088916]

#  Objective function:
#  0.30540294465712925

    # popsize and maxiter are defined at the top of the page
    algorithm_param = {'max_num_iteration': 1,\
                    'population_size':1,\
                    'mutation_probability':0.1,\
                    'elit_ratio': 0.01,\
                    'crossover_probability': 0.5,\
                    'parents_portion': 0.3,\
                    'crossover_type':'uniform',\
                    'max_iteration_without_improv': None}


    optimization =  ga(function = objectiveFunction, dimension = 47, variable_type = 'real',variable_boundaries= bds, algorithm_parameters = algorithm_param, function_timeout=6000)
    optimization.run()
    with open('optim_outputs.txt', 'w') as f:
        print('Optimization_outputs:', optimization.output_dict, file=f)
    print(optimization)
    return optimization.output_dict




def graph_results():
    output_parameters = run_optimizer()

    # define the parameters
    initial_roe = 12
    chance_reproduceSapling = output_parameters["variable"][0]
    chance_reproduceYoungScrub = output_parameters["variable"][1]
    chance_regrowGrass =output_parameters["variable"][2]
    chance_saplingBecomingTree =output_parameters["variable"][3]
    chance_youngScrubMatures =output_parameters["variable"][4]
    chance_scrubOutcompetedByTree =output_parameters["variable"][5]
    chance_grassOutcompetedByTree =output_parameters["variable"][6]
    chance_grassOutcompetedByScrub =output_parameters["variable"][7]
    chance_saplingOutcompetedByTree =output_parameters["variable"][8]
    chance_saplingOutcompetedByScrub = output_parameters["variable"][9]
    chance_youngScrubOutcompetedByScrub = output_parameters["variable"][10]
    chance_youngScrubOutcompetedByTree =output_parameters["variable"][11]
    # consumer values
    roe_deer_reproduce =output_parameters["variable"][12]
    roe_deer_gain_from_grass =output_parameters["variable"][13]
    roe_deer_gain_from_trees =output_parameters["variable"][14]
    roe_deer_gain_from_scrub = output_parameters["variable"][15]
    roe_deer_gain_from_saplings = output_parameters["variable"][16]
    roe_deer_gain_from_young_scrub = output_parameters["variable"][17]
    fallow_deer_reproduce = output_parameters["variable"][18]
    fallow_deer_gain_from_grass = output_parameters["variable"][19]
    fallow_deer_gain_from_trees = output_parameters["variable"][20]
    fallow_deer_gain_from_scrub = output_parameters["variable"][21]
    fallow_deer_gain_from_saplings = output_parameters["variable"][22]
    fallow_deer_gain_from_young_scrub = output_parameters["variable"][23]
    red_deer_reproduce = output_parameters["variable"][24]
    red_deer_gain_from_grass = output_parameters["variable"][25]
    red_deer_gain_from_trees = output_parameters["variable"][26]
    red_deer_gain_from_scrub = output_parameters["variable"][27]
    red_deer_gain_from_saplings = output_parameters["variable"][28]
    red_deer_gain_from_young_scrub = output_parameters["variable"][29]
    ponies_gain_from_grass = output_parameters["variable"][30]
    ponies_gain_from_trees = output_parameters["variable"][31]
    ponies_gain_from_scrub = output_parameters["variable"][32]
    ponies_gain_from_saplings = output_parameters["variable"][33]
    ponies_gain_from_young_scrub = output_parameters["variable"][34]
    cattle_reproduce = output_parameters["variable"][35]
    cows_gain_from_grass = output_parameters["variable"][36]
    cows_gain_from_trees = output_parameters["variable"][37]
    cows_gain_from_scrub = output_parameters["variable"][38]
    cows_gain_from_saplings = output_parameters["variable"][39]
    cows_gain_from_young_scrub = output_parameters["variable"][40]
    tamworth_pig_reproduce = output_parameters["variable"][41]
    tamworth_pig_gain_from_trees = output_parameters["variable"][42]
    tamworth_pig_gain_from_scrub = output_parameters["variable"][43]
    tamworth_pig_gain_from_grass =output_parameters["variable"][44]
    tamworth_pig_gain_from_saplings =output_parameters["variable"][45]
    tamworth_pig_gain_from_young_scrub = output_parameters["variable"][46]
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
    number_simulations = 2

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
    plt.savefig('optimizer_outputs_numbers.png')
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
    f.axes[7].vlines(x=184,ymin=19,ymax=21.5, color='r')
    f.axes[8].vlines(x=184,ymin=41.8,ymax=61.8, color='r')
    # stop the plots from overlapping
    f.fig.suptitle("Optimizer Outputs")
    plt.tight_layout()
    plt.savefig('optimizer_outputs_conditions.png')
    plt.show()



    # # # # # REALITY CHECKS # # # # # # 

    # habitat deaths - stacked bar charts. what's killing saplings? 
    sapling_df = pd.DataFrame(
    {'Time': final_results['Time'], 'Grown up': final_results['Saplings grown up'], 'Outcompeted by Trees': final_results['Saplings Outcompeted by Trees'], 'Outcompeted by Scrub': final_results['Saplings Outcompeted by Scrub'], "Eaten by roe deer": final_results['Saplings eaten by roe deer'],
    "Eaten by Fallow deer": final_results['Saplings eaten by Fallow deer'],"Eaten by Exmoor pony": final_results['Saplings eaten by Exmoor pony'], "Eaten by longhorn cattle": final_results['Saplings eaten by longhorn cattle'], "Eaten by red deer": final_results['Saplings eaten by red deer'], "Eaten by pigs": final_results['Saplings eaten by pigs']})
    sapling_average = sapling_df.groupby(['Time'],as_index=False).mean()
    col_map = plt.get_cmap('Paired')
    sapling_average.plot.bar(x='Time', stacked=True, color=col_map.colors)
    plt.xticks([25, 50, 75, 100, 125, 150, 175])
    plt.ylabel('Amount Died')
    plt.title('What kills saplings?')
    plt.box(False)
    plt.tight_layout()
    plt.savefig('what_eats_saplings.png')
    plt.show()

    # habitat deaths - stacked bar charts. what's killing young scrub? 
    youngscrub_df = pd.DataFrame(
    {'Time': final_results['Time'], 'Grown up': final_results['Young scrub grown up'], 'Outcompeted by Trees': final_results['Young Scrub Outcompeted by Trees'], 'Outcompeted by Scrub': final_results['Young Scrub Outcompeted by Scrub'], "Eaten by roe deer": final_results['Young Scrub eaten by roe deer'],
    "Eaten by Fallow deer": final_results['Young Scrub eaten by Fallow deer'],"Eaten by Exmoor pony": final_results['Young Scrub eaten by Exmoor pony'], "Eaten by longhorn cattle": final_results['Young Scrub eaten by longhorn cattle'], "Eaten by red deer": final_results['Young Scrub eaten by red deer'], "Eaten by pigs": final_results['Young Scrub eaten by pigs']})
    youngScrub_average = youngscrub_df.groupby(['Time'],as_index=False).mean()
    youngScrub_average.plot.bar(x='Time', stacked=True, color=col_map.colors)
    plt.xticks([25, 50, 75, 100, 125, 150, 175])
    plt.ylabel('Amount Died')
    plt.title('What kills young scrub?')
    plt.box(False)
    plt.tight_layout()
    plt.savefig('what_eats_youngScrub.png')
    plt.show()

    # habitat deaths - stacked bar charts. what's killing grass? 
    grass_df = pd.DataFrame(
    {'Time': final_results['Time'], 'Outcompeted by Trees': final_results['Grass Outcompeted by Trees'], 'Outcompeted by Scrub': final_results['Grass Outcompeted by Scrub'], "Eaten by roe deer": final_results['Grass eaten by roe deer'],
    "Eaten by Fallow deer": final_results['Grass eaten by Fallow deer'],"Eaten by Exmoor pony": final_results['Grass eaten by Exmoor pony'], "Eaten by longhorn cattle": final_results['Grass eaten by longhorn cattle'], "Eaten by red deer": final_results['Grass eaten by red deer'], "Eaten by pigs": final_results['Grass eaten by pigs']})
    grass_average = grass_df.groupby(['Time'],as_index=False).mean()
    grass_average.plot.bar(x='Time', stacked=True, color=col_map.colors)
    plt.xticks([25, 50, 75, 100, 125, 150, 175])
    plt.ylabel('Amount Died')
    plt.title('What kills grass?')
    plt.box(False)
    plt.tight_layout()
    plt.savefig('what_eats_grass.png')
    plt.show()

    # habitat deaths - stacked bar charts. what's killing scrub? 
    scrub_df = pd.DataFrame(
    {'Time': final_results['Time'], 'Outcompeted by Trees': final_results['Scrub Outcompeted by Trees'], "Eaten by roe deer": final_results['Scrub eaten by roe deer'],
    "Eaten by Fallow deer": final_results['Scrub eaten by Fallow deer'],"Eaten by Exmoor pony": final_results['Scrub eaten by Exmoor pony'], "Eaten by longhorn cattle": final_results['Scrub eaten by longhorn cattle'], "Eaten by red deer": final_results['Scrub eaten by red deer'], "Eaten by pigs": final_results['Scrub eaten by pigs']})
    scrub_average = scrub_df.groupby(['Time'],as_index=False).mean()
    scrub_average.plot.bar(x='Time', stacked=True, color=col_map.colors)
    plt.xticks([25, 50, 75, 100, 125, 150, 175])
    plt.ylabel('Amount Died')
    plt.box(False)
    plt.title('What kills scrub?')
    plt.tight_layout()
    plt.savefig('what_eats_scrub.png')
    plt.show()

    # habitat deaths - stacked bar charts. what's killing trees? 
    trees_df = pd.DataFrame(
    {'Time': final_results['Time'], "Eaten by roe deer": final_results['Trees eaten by roe deer'],
    "Eaten by Fallow deer": final_results['Trees eaten by Fallow deer'],"Eaten by Exmoor pony": final_results['Trees eaten by Exmoor pony'], "Eaten by longhorn cattle": final_results['Trees eaten by longhorn cattle'], "Eaten by red deer": final_results['Trees eaten by red deer'], "Eaten by pigs": final_results['Trees eaten by pigs']})
    trees_average = trees_df.groupby(['Time'],as_index=False).mean()
    trees_average.plot.bar(x='Time', stacked=True, color=col_map.colors)
    plt.xticks([25, 50, 75, 100, 125, 150, 175])
    plt.ylabel('Amount Died')
    plt.box(False)
    plt.title('What kills trees?')
    plt.tight_layout()
    plt.savefig('what_eats_trees.png')
    plt.show()




    # forecasting

    final_results_list = []
    run_number = 0
    number_simulations = 5

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
                    max_time = 784, reintroduction = True, introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)
      
        model.run_model()

        results = model.datacollector.get_model_vars_dataframe()
        results['run_number'] = run_number
        final_results_list.append(results)

    forecasting = pd.concat(final_results_list)

    palette=['#db5f57', '#57d3db', '#57db5f','#5f57db', '#db57d3']

    # graph that
    final_results = forecasting[["Time", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground", "run_number"]]
    grouping_variable = np.repeat(final_results['run_number'], 10)
    y_values = final_results.drop(['run_number', 'Time'], axis=1).values.flatten()
    species_list = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 785*number_simulations)
    indices = np.repeat(final_results['Time'], 10)

    final_df = pd.DataFrame(
    {'Abundance %': y_values, 'runNumber': grouping_variable, 'Ecosystem Element': species_list, 'Time': indices})
    # calculate median
    m = final_df.groupby(['Time', 'Ecosystem Element'])[['Abundance %']].apply(np.median)
    m.name = 'Median'
    final_df = final_df.join(m, on=['Time', 'Ecosystem Element'])
    # calculate quantiles
    perc1 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(.95)
    perc1.name = 'ninetyfivePerc'
    final_df = final_df.join(perc1, on=['Time', 'Ecosystem Element'])
    perc2 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(.05)
    perc2.name = "fivePerc"
    final_df = final_df.join(perc2, on=['Time', 'Ecosystem Element'])

    final_df = final_df.reset_index(drop=True)
    final_df.to_csv("forecasting_experiment.csv")

    counterfactual_graph = final_df.reset_index(drop=True)
    f = sns.FacetGrid(final_df, col="Ecosystem Element", palette = palette, col_wrap=4, sharey = False)
    f.map(sns.lineplot, 'Time', 'Median') 
    # 0
    f.map(sns.lineplot, 'Time', 'fivePerc') 
    # 1
    f.map(sns.lineplot, 'Time', 'ninetyfivePerc')
    # 2
    for ax in f.axes.flat:
        ax.fill_between(ax.lines[1].get_xdata(),ax.lines[1].get_ydata(), ax.lines[2].get_ydata(), color="#db5f57",alpha =0.2)
        ax.set_ylabel('Abundance')
    # add subplot titles
    axes = f.axes.flatten()
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

    f.fig.suptitle('Forecasting ten years ahead')
    plt.tight_layout()
    plt.savefig('forecasting_experiment_test.png')
    plt.show()




    # What happens to habitats if there are no herbivores?

    final_results_list = []
    run_number = 0
    number_simulations = 10
    initial_roe = 0
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
                    max_time = 1200, reintroduction = True, introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)

        model.run_model()

        # first graph:  does it pass the filters? looking at the number of individual trees, etc.
        results = model.datacollector.get_model_vars_dataframe()
        final_results_list.append(results)

    final_results = pd.concat(final_results_list)

    # y values - number of trees, scrub, etc. 
    y_values_conditions =  final_results[["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"]].values.flatten()            
    species_list_conditions = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 1201*number_simulations) 
    indices_conditions = np.repeat(final_results['Time'], 10)
    final_df = pd.DataFrame(
    {'Abundance': y_values_conditions, 'Ecosystem Element': species_list_conditions, 'Time': indices_conditions})
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
    # stop the plots from overlapping
    g.fig.suptitle('Reality check: No herbivores (conditions)')
    plt.tight_layout()
    plt.savefig('what_if_no_herbs')
    plt.show()

    # y values - number of trees, scrub, etc. 
    y_values = final_results[["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"]].values.flatten()
    species_list = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"], 1201*number_simulations) 
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
    g.fig.suptitle('Reality check: No herbivores (habitat elements)')
    plt.tight_layout()
    plt.savefig('what_if_no_herbs_numbers_conditions.png')
    plt.show()






    # what if we run it a long time with no reintroductions
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
                    max_time = 784, reintroduction = False, introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)


        model.run_model()

        # first graph:  does it pass the filters? looking at the number of individual trees, etc.
        results = model.datacollector.get_model_vars_dataframe()
        final_results_list.append(results)

    final_results = pd.concat(final_results_list)

    # y values - number of trees, scrub, etc. 
    y_values_conditions =  final_results[["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"]].values.flatten()            
    species_list_conditions = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 785*number_simulations) 
    indices_conditions = np.repeat(final_results['Time'], 10)
    final_df = pd.DataFrame(
    {'Abundance': y_values_conditions, 'Ecosystem Element': species_list_conditions, 'Time': indices_conditions})
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
    # stop the plots from overlapping
    g.fig.suptitle('Reality check: Roe deer only')
    plt.tight_layout()
    plt.savefig('what_if_no_reintro.png')
    plt.show()


    # y values - number of trees, scrub, etc. 
    y_values = final_results[["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"]].values.flatten()
    species_list = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"], 785*number_simulations) 
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
    g.fig.suptitle('Reality check: Roe deer only (habitat elements)')
    plt.tight_layout()
    plt.savefig('what_if_no_reintro_numbers.png')
    plt.show()






    # Herbivore overload
    final_results_list = []
    run_number = 0
    roeDeer_reproduce = 0.5
    cows_reproduce = 0.5
    fallowDeer_reproduce = 0.5
    redDeer_reproduce = 0.5
    pigs_reproduce = 0.5
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

    # y values - number of trees, scrub, etc. 
    y_values_conditions =  final_results[["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"]].values.flatten()            
    species_list_conditions = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 185*number_simulations) 
    indices_conditions = np.repeat(final_results['Time'], 10)
    final_df = pd.DataFrame(
    {'Abundance': y_values_conditions, 'Ecosystem Element': species_list_conditions, 'Time': indices_conditions})
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
    # stop the plots from overlapping
    g.fig.suptitle('Reality check: Overloaded herbivores')
    plt.tight_layout()
    plt.savefig('what_if_manyHerbs_conditions.png')
    plt.show()


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
    g.fig.suptitle('Reality check: Overloaded herbivores (habitat elements)')
    plt.tight_layout()
    plt.savefig('what_if_manyHerbs_numbers.png')
    plt.show()

    return output_parameters



graph_results()