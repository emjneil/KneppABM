# run experiments on the accepted parameter sets 
from run_model import run_all_models
from KneppModel_ABM import roeDeer_agent, habitatAgent, exmoorPony, redDeer, fallowDeer, longhornCattle, tamworthPigs
from mesa import Model
from mesa.datacollection import DataCollector
import numpy as np
import random
import pandas as pd
from schedule import RandomActivationByBreed
from mesa.space import MultiGrid 



                                # # # # ------ Define the model ------ # # # # 



def run_counterfactual():
    number_simulations, final_results, accepted_parameters = run_all_models()
    # run the counterfactual: what would have happened if rewilding hadn't occurred? 
    final_results_list = []
    run_number = 0

    # take the accepted parameters, and go row by row, running the model
    for _, row in accepted_parameters.iterrows():
        chance_reproduceSapling = row[1]
        chance_reproduceYoungScrub =  row[2]
        chance_regrowGrass =  row[3]
        chance_saplingBecomingTree =  row[4]
        chance_youngScrubMatures =  row[5]
        chance_scrubOutcompetedByTree =  row[6]
        chance_grassOutcompetedByTree =  row[7]
        chance_grassOutcompetedByScrub = row[8]
        chance_saplingOutcompetedByTree =  row[9]
        chance_saplingOutcompetedByScrub =  row[10]
        chance_youngScrubOutcompetedByScrub =  row[11]
        chance_youngScrubOutcompetedByTree =  row[12]
        initial_roeDeer = round(row[13])
        initial_grassland =  round(row[14])
        initial_woodland =  round(row[15])
        initial_scrubland =  round(row[16])
        roeDeer_reproduce =  row[17]
        roeDeer_gain_from_grass =  row[18]
        roeDeer_gain_from_Trees =  row[19]
        roeDeer_gain_from_Scrub =  row[20]
        roeDeer_gain_from_Saplings =  row[21]
        roeDeer_gain_from_YoungScrub =  row[22]
        roeDeer_impactGrass =  row[23]
        roeDeer_saplingsEaten =  row[24]
        roeDeer_youngScrubEaten =  row[25]
        roeDeer_treesEaten =  row[26]
        roeDeer_scrubEaten =  row[27]
        ponies_gain_from_grass =  row[28]
        ponies_gain_from_Trees =  row[29]
        ponies_gain_from_Scrub =  row[30]
        ponies_gain_from_Saplings =  row[31]
        ponies_gain_from_YoungScrub =  row[32]
        ponies_impactGrass =  row[33]
        ponies_saplingsEaten =  row[34]
        ponies_youngScrubEaten =  row[35]
        ponies_treesEaten =  row[36]
        ponies_scrubEaten =  row[37]
        cows_reproduce =  row[38]
        cows_gain_from_grass =  row[39]
        cows_gain_from_Trees =  row[40]
        cows_gain_from_Scrub =  row[41]
        cows_gain_from_Saplings =  row[42]
        cows_gain_from_YoungScrub =  row[43]
        cows_impactGrass =  row[44]
        cows_saplingsEaten =  row[45]
        cows_youngScrubEaten =  row[46]
        cows_treesEaten =  row[47]
        cows_scrubEaten =  row[48]
        fallowDeer_reproduce =  row[49]
        fallowDeer_gain_from_grass =  row[50]
        fallowDeer_gain_from_Trees =  row[51]
        fallowDeer_gain_from_Scrub =  row[52]
        fallowDeer_gain_from_Saplings =  row[53]
        fallowDeer_gain_from_YoungScrub =  row[54]
        fallowDeer_impactGrass =  row[55]
        fallowDeer_saplingsEaten =  row[56]
        fallowDeer_youngScrubEaten =  row[57]
        fallowDeer_treesEaten =  row[58]
        fallowDeer_scrubEaten =  row[59]
        redDeer_reproduce =  row[60]
        redDeer_gain_from_grass =  row[61]
        redDeer_gain_from_Trees =  row[62]
        redDeer_gain_from_Scrub =  row[63]
        redDeer_gain_from_Saplings =  row[64]
        redDeer_gain_from_YoungScrub =  row[65]
        redDeer_impactGrass =  row[66]
        redDeer_saplingsEaten =  row[67]
        redDeer_youngScrubEaten =  row[68]
        redDeer_treesEaten =  row[69]
        redDeer_scrubEaten =  row[70]
        pigs_reproduce =  row[71]
        pigs_gain_from_grass =  row[72]
        pigs_gain_from_Saplings =  row[73]
        pigs_gain_from_YoungScrub =  row[74]
        pigs_impactGrass =  row[75]
        pigs_saplingsEaten =  row[76]
        pigs_youngScrubEaten =  row[77]


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
            width = 25, height = 18, max_time = 184, reintroduction = False, 
            RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)
        model.run_model()

        run_number +=1
        print(run_number)    

        results = model.datacollector.get_model_vars_dataframe()
        results['run_number'] = run_number
        final_results_list.append(results)
    
    # append to dataframe
    counterfactual = pd.concat(final_results_list)
    counterfactual['accepted?'] = "noReintro"

    # return the number of simulations, final results, forecasting, and counterfactual 
    return number_simulations, final_results, counterfactual, accepted_parameters
