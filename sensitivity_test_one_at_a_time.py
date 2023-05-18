# graph the runs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from KneppModel_ABM import KneppModel 
import numpy as np
import pandas as pd
from scipy.stats import linregress


# open the accepted parameters
accepted_parameters = pd.read_csv('combined_accepted_parameters.csv') 

# check the 12 non-uniform KS parameters in accepted_parameters
# ks_params = ["chance_reproduceSapling", "chance_reproduceYoungScrub", "chance_saplingBecomingTree", "chance_youngScrubMatures", "chance_grassOutcompetedByTree", "chance_grassOutcompetedByScrub", "chance_saplingOutcompetedByTree", "roeDeer_reproduce", "cows_reproduce", "fallowDeer_reproduce", "redDeer_reproduce", "pigs_reproduce"]

# ks_params = 
# "roeDeer_reproduce", - linux24

# alter each one, one at a time
sensitivity_results_list = []
sensitivity_parameters = []
perc_numbers=[]
run_number  = 0
# choose my percent above/below number
perc_aboveBelow = [-0.5, -0.1,-0.01, 0, 0.01, 0.1, 0.5]
final_parameters = accepted_parameters.iloc[:,1:52]
# accepted_parameters.iloc[0:3,1:52]
# loop through each one, changing one cell at a time
for i,row1 in final_parameters.iterrows():
    for index, row in row1.iteritems():
        if index == "roeDeer_reproduce":
            for perc_number in perc_aboveBelow:
                # make a temp parameter set
                final_parameters_temp = final_parameters
                ifor_val = row + (row*perc_number)
                final_parameters_temp.loc[i,index]= ifor_val
                # choose my parameters 
                chance_reproduceSapling = final_parameters_temp.iloc[i,0]
                chance_reproduceYoungScrub = final_parameters_temp.iloc[i,1]
                chance_regrowGrass = final_parameters_temp.iloc[i,2]
                chance_saplingBecomingTree = final_parameters_temp.iloc[i,3]
                chance_youngScrubMatures = final_parameters_temp.iloc[i,4]
                chance_scrubOutcompetedByTree = final_parameters_temp.iloc[i,5]
                chance_grassOutcompetedByTree = final_parameters_temp.iloc[i,6]
                chance_grassOutcompetedByScrub = final_parameters_temp.iloc[i,7]
                chance_saplingOutcompetedByTree = final_parameters_temp.iloc[i,8]
                chance_saplingOutcompetedByScrub = final_parameters_temp.iloc[i,9]
                chance_youngScrubOutcompetedByScrub = final_parameters_temp.iloc[i,10]
                chance_youngScrubOutcompetedByTree = final_parameters_temp.iloc[i,11]
                initial_roeDeer = final_parameters_temp.iloc[i,12]
                initial_grassland = final_parameters_temp.iloc[i,13]
                initial_woodland = final_parameters_temp.iloc[i,14]
                initial_scrubland = final_parameters_temp.iloc[i,15]
                roeDeer_reproduce = final_parameters_temp.iloc[i,16]
                roeDeer_gain_from_grass = final_parameters_temp.iloc[i,17]
                roeDeer_gain_from_Trees = final_parameters_temp.iloc[i,18]
                roeDeer_gain_from_Scrub = final_parameters_temp.iloc[i,19]
                roeDeer_gain_from_Saplings = final_parameters_temp.iloc[i,20]
                roeDeer_gain_from_YoungScrub = final_parameters_temp.iloc[i,21]
                ponies_gain_from_grass = final_parameters_temp.iloc[i,22]
                ponies_gain_from_Trees = final_parameters_temp.iloc[i,23]
                ponies_gain_from_Scrub = final_parameters_temp.iloc[i,24]
                ponies_gain_from_Saplings = final_parameters_temp.iloc[i,25]
                ponies_gain_from_YoungScrub = final_parameters_temp.iloc[i,26]
                cows_reproduce = final_parameters_temp.iloc[i,27]
                cows_gain_from_grass = final_parameters_temp.iloc[i,28]
                cows_gain_from_Trees = final_parameters_temp.iloc[i,29]
                cows_gain_from_Scrub = final_parameters_temp.iloc[i,30]
                cows_gain_from_Saplings = final_parameters_temp.iloc[i,31]
                cows_gain_from_YoungScrub = final_parameters_temp.iloc[i,32]
                fallowDeer_reproduce = final_parameters_temp.iloc[i,33]
                fallowDeer_gain_from_grass = final_parameters_temp.iloc[i,34]
                fallowDeer_gain_from_Trees = final_parameters_temp.iloc[i,35]
                fallowDeer_gain_from_Scrub = final_parameters_temp.iloc[i,36]
                fallowDeer_gain_from_Saplings = final_parameters_temp.iloc[i,37]
                fallowDeer_gain_from_YoungScrub = final_parameters_temp.iloc[i,38]
                redDeer_reproduce = final_parameters_temp.iloc[i,39]
                redDeer_gain_from_grass = final_parameters_temp.iloc[i,40]
                redDeer_gain_from_Trees = final_parameters_temp.iloc[i,41]
                redDeer_gain_from_Scrub = final_parameters_temp.iloc[i,42]
                redDeer_gain_from_Saplings = final_parameters_temp.iloc[i,43]
                redDeer_gain_from_YoungScrub = final_parameters_temp.iloc[i,44]
                pigs_reproduce = final_parameters_temp.iloc[i,45]
                pigs_gain_from_grass = final_parameters_temp.iloc[i,46]
                pigs_gain_from_Trees = final_parameters_temp.iloc[i,47]
                pigs_gain_from_Scrub = final_parameters_temp.iloc[i,48]
                pigs_gain_from_Saplings = final_parameters_temp.iloc[i,49]
                pigs_gain_from_YoungScrub = final_parameters_temp.iloc[i,50]
                # # stocking values
                fallowDeer_stocking = 247
                cattle_stocking = 81
                redDeer_stocking = 35
                tamworthPig_stocking = 7
                exmoor_stocking = 15
                # # euro bison parameters
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
                # reindeer parameters
                reproduce_reindeer = 0
                # reindeer should have impacts between red and fallow deer
                reindeer_gain_from_grass = 0
                reindeer_gain_from_Trees =0
                reindeer_gain_from_Scrub =0
                reindeer_gain_from_Saplings = 0
                reindeer_gain_from_YoungScrub = 0
                # forecasting things
                fallowDeer_stocking_forecast = 247
                cattle_stocking_forecast = 81
                redDeer_stocking_forecast = 35
                tamworthPig_stocking_forecast = 7
                exmoor_stocking_forecast = 15
                roeDeer_stocking_forecast = 0
                reindeer_stocking_forecast = 0
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
                    width = 25, height = 18, max_time = 184, reintroduction = True,
                    introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False, cull_roe = False)

                model.run_model()

                # remember the results of the model (dominant conditions, # of agents)
                final_results = model.datacollector.get_model_vars_dataframe()

                # check how many filters were passed
                final_results["passed_filters"] = 0
                # pre-reintroduction model
                if (final_results.loc[50,"Roe deer"] <= 40) & (final_results.loc[50,"Roe deer"] >= 12) & (final_results.loc[50,"Grassland"] <= 80) & (final_results.loc[50,"Grassland"] >= 49) & (final_results.loc[50,"Woodland"] <= 27) & (final_results.loc[50,"Woodland"] >= 7) & (final_results.loc[50,"Thorny Scrub"] <= 21) & (final_results.loc[50,"Thorny Scrub"] >= 1):
                    final_results["passed_filters"] += 1
                # April 2015
                if (final_results.loc[123,"Exmoor pony"] <= 11) & (final_results.loc[123,"Exmoor pony"] >= 9) & (final_results.loc[123,"Longhorn cattle"] <= 140) & (final_results.loc[123,"Longhorn cattle"] >= 90) & (final_results.loc[123,"Tamworth pigs"] <= 32) & (final_results.loc[123,"Tamworth pigs"] >= 12):
                    final_results["passed_filters"] += 1
                # May 2015
                if (final_results.loc[124,"Longhorn cattle"] <= 154) & (final_results.loc[124,"Longhorn cattle"] >= 104) & (final_results.loc[124,"Tamworth pigs"] <= 24) & (final_results.loc[124,"Tamworth pigs"] >= 4) & (final_results.loc[124,"Exmoor pony"] <= 11) & (final_results.loc[124,"Exmoor pony"] >= 9):
                    final_results["passed_filters"] += 1
                # June 2015
                if (final_results.loc[125,"Longhorn cattle"] <= 154) & (final_results.loc[125,"Longhorn cattle"] >= 104) & (final_results.loc[125,"Exmoor pony"] <= 11) & (final_results.loc[125,"Exmoor pony"] >= 9) & (final_results.loc[125,"Tamworth pigs"] <= 24) & (final_results.loc[125,"Tamworth pigs"] >= 4):
                    final_results["passed_filters"] += 1        
                # July 2015
                if (final_results.loc[126,"Longhorn cattle"] <= 154) & (final_results.loc[126,"Longhorn cattle"] >= 104) & (final_results.loc[126,"Exmoor pony"] <= 11) & (final_results.loc[126,"Exmoor pony"] >= 9) & (final_results.loc[126,"Tamworth pigs"] <= 24) & (final_results.loc[126,"Tamworth pigs"] >= 4):
                        final_results["passed_filters"] += 1
                # Aug 2015
                if (final_results.loc[127,"Longhorn cattle"] <= 154) & (final_results.loc[127,"Longhorn cattle"] >= 104) & (final_results.loc[127,"Exmoor pony"] <= 11) & (final_results.loc[127,"Exmoor pony"] >= 9) & (final_results.loc[127,"Tamworth pigs"] <= 24) & (final_results.loc[127,"Tamworth pigs"] >= 4):
                    final_results["passed_filters"] += 1
                # Sept 2015
                if (final_results.loc[128,"Longhorn cattle"] <= 155) & (final_results.loc[128,"Longhorn cattle"] >= 105) & (final_results.loc[128,"Exmoor pony"] <= 11) & (final_results.loc[128,"Exmoor pony"] >= 9) & (final_results.loc[128,"Tamworth pigs"] <= 24) & (final_results.loc[128,"Tamworth pigs"] >= 4):
                    final_results["passed_filters"] += 1
                # Oct 2015
                if (final_results.loc[129,"Longhorn cattle"] <= 116) & (final_results.loc[129,"Longhorn cattle"] >= 66) & (final_results.loc[129,"Exmoor pony"] <= 11) & (final_results.loc[129,"Exmoor pony"] >= 9) & (final_results.loc[129,"Tamworth pigs"] <= 24) & (final_results.loc[129,"Tamworth pigs"] >= 4):
                    final_results["passed_filters"] += 1
                # Nov 2015
                if (final_results.loc[130,"Longhorn cattle"] <= 116) & (final_results.loc[130,"Longhorn cattle"] >= 66) & (final_results.loc[130,"Exmoor pony"] <= 11) & (final_results.loc[130,"Exmoor pony"] >= 9) & (final_results.loc[130,"Tamworth pigs"] <= 23) & (final_results.loc[130,"Tamworth pigs"] >= 3):
                    final_results["passed_filters"] += 1
                # Dec 2015
                if (final_results.loc[131,"Longhorn cattle"] <= 111) & (final_results.loc[131,"Longhorn cattle"] >= 61) &(final_results.loc[131,"Exmoor pony"] <= 11) & (final_results.loc[131,"Exmoor pony"] >= 9) &(final_results.loc[131,"Tamworth pigs"] <= 23) & (final_results.loc[131,"Tamworth pigs"] >= 3):
                    final_results["passed_filters"] += 1
                # Jan 2016
                if (final_results.loc[132,"Longhorn cattle"] <= 111) & (final_results.loc[132,"Longhorn cattle"] >= 61) & (final_results.loc[132,"Exmoor pony"] <= 11) & (final_results.loc[132,"Exmoor pony"] >= 9) & (final_results.loc[132,"Tamworth pigs"] <= 20) & (final_results.loc[132,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # Feb 2016
                if (final_results.loc[133,"Exmoor pony"] <= 11) & (final_results.loc[133,"Exmoor pony"] >= 9) & (final_results.loc[133,"Longhorn cattle"] <= 111) & (final_results.loc[133,"Longhorn cattle"] >= 61) &(final_results.loc[133,"Tamworth pigs"] <= 20) & (final_results.loc[133,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # March 2016
                if (final_results.loc[134,"Exmoor pony"] <= 12) & (final_results.loc[134,"Exmoor pony"] >= 10) & (final_results.loc[134,"Longhorn cattle"] <= 111) & (final_results.loc[134,"Longhorn cattle"] >= 61) & (final_results.loc[134,"Fallow deer"] <= 190) & (final_results.loc[134,"Fallow deer"] >= 90) & (final_results.loc[134,"Red deer"] <= 31) & (final_results.loc[134,"Red deer"] >= 21) & (final_results.loc[134,"Tamworth pigs"] <= 19) & (final_results.loc[134,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # April 2016
                if (final_results.loc[135,"Exmoor pony"] <= 12) & (final_results.loc[135,"Exmoor pony"] >= 10) & (final_results.loc[135,"Longhorn cattle"] <= 128) & (final_results.loc[135,"Longhorn cattle"] >= 78) & (final_results.loc[135,"Tamworth pigs"] <= 19) & (final_results.loc[135,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # May 2016
                if (final_results.loc[136,"Exmoor pony"] <= 12) & (final_results.loc[136,"Exmoor pony"] >= 10) & (final_results.loc[136,"Longhorn cattle"] <= 133) & (final_results.loc[136,"Longhorn cattle"] >= 83) &(final_results.loc[136,"Tamworth pigs"] <= 27) & (final_results.loc[136,"Tamworth pigs"] >= 7):
                    final_results["passed_filters"] += 1
                # June 2016
                if (final_results.loc[137,"Exmoor pony"] <= 12) & (final_results.loc[137,"Exmoor pony"] >= 10) & (final_results.loc[137,"Longhorn cattle"] <= 114) & (final_results.loc[137,"Longhorn cattle"] >= 64) & (final_results.loc[137,"Tamworth pigs"] <= 27) & (final_results.loc[137,"Tamworth pigs"] >= 7):
                    final_results["passed_filters"] += 1
                # July 2016
                if (final_results.loc[138,"Exmoor pony"] <= 12) & (final_results.loc[138,"Exmoor pony"] >= 10) & (final_results.loc[138,"Longhorn cattle"] <= 112) & (final_results.loc[138,"Longhorn cattle"] >= 62) & (final_results.loc[138,"Tamworth pigs"] <= 27) & (final_results.loc[138,"Tamworth pigs"] >= 7):
                    final_results["passed_filters"] += 1
                # Aug 2016
                if (final_results.loc[139,"Exmoor pony"] <= 12) & (final_results.loc[139,"Exmoor pony"] >= 10) & (final_results.loc[139,"Longhorn cattle"] <= 112) & (final_results.loc[139,"Longhorn cattle"] >= 62) & (final_results.loc[139,"Tamworth pigs"] <= 27) & (final_results.loc[139,"Tamworth pigs"] >= 7):
                    final_results["passed_filters"] += 1
                # Sept 2016
                if (final_results.loc[140,"Exmoor pony"] <= 12) & (final_results.loc[140,"Exmoor pony"] >= 10) &(final_results.loc[140,"Longhorn cattle"] <= 122) & (final_results.loc[140,"Longhorn cattle"] >= 72) & (final_results.loc[140,"Tamworth pigs"] <= 27) & (final_results.loc[140,"Tamworth pigs"] >= 7):
                    final_results["passed_filters"] += 1
                # Oct 2016
                if (final_results.loc[141,"Exmoor pony"] <= 12) & (final_results.loc[141,"Exmoor pony"] >= 10) & (final_results.loc[141,"Longhorn cattle"] <= 122) & (final_results.loc[141,"Longhorn cattle"] >= 72) & (final_results.loc[141,"Tamworth pigs"] <= 27) & (final_results.loc[141,"Tamworth pigs"] >= 7):
                    final_results["passed_filters"] += 1
                # Nov 2016
                if (final_results.loc[142,"Exmoor pony"] <= 12) & (final_results.loc[142,"Exmoor pony"] >= 10) &(final_results.loc[142,"Longhorn cattle"] <= 117) & (final_results.loc[142,"Longhorn cattle"] >= 67) &(final_results.loc[142,"Tamworth pigs"] <= 27) & (final_results.loc[142,"Tamworth pigs"] >= 7):
                    final_results["passed_filters"] += 1
                # Dec 2016
                if (final_results.loc[143,"Exmoor pony"] <= 12) & (final_results.loc[143,"Exmoor pony"] >= 10) &(final_results.loc[143,"Longhorn cattle"] <= 104) & (final_results.loc[143,"Longhorn cattle"] >= 54)& (final_results.loc[143,"Tamworth pigs"] <= 23) & (final_results.loc[143,"Tamworth pigs"] >= 3):
                    final_results["passed_filters"] += 1
                # Jan 2017
                if (final_results.loc[144,"Exmoor pony"] <= 12) & (final_results.loc[144,"Exmoor pony"] >= 10) & (final_results.loc[144,"Longhorn cattle"] <= 104) & (final_results.loc[144,"Longhorn cattle"] >= 54) & (final_results.loc[144,"Tamworth pigs"] <= 19) & (final_results.loc[144,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # Feb 2017
                    if (final_results.loc[145,"Exmoor pony"] <= 12) & (final_results.loc[145,"Exmoor pony"] >= 10) & (final_results.loc[145,"Longhorn cattle"] <= 104) & (final_results.loc[145,"Longhorn cattle"] >= 54) & (final_results.loc[145,"Tamworth pigs"] <= 17) & (final_results.loc[145,"Tamworth pigs"] >= 1):
                        final_results["passed_filters"] += 1
                # March 2017
                if (final_results.loc[146,"Exmoor pony"] <= 11) & (final_results.loc[146,"Exmoor pony"] >= 9) & (final_results.loc[146,"Fallow deer"] <= 215) & (final_results.loc[146,"Fallow deer"] >= 115) &(final_results.loc[146,"Longhorn cattle"] <= 104) & (final_results.loc[146,"Longhorn cattle"] >= 54) &(final_results.loc[146,"Tamworth pigs"] <= 17) & (final_results.loc[146,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # April 2017
                if (final_results.loc[147,"Exmoor pony"] <= 11) & (final_results.loc[147,"Exmoor pony"] >= 9) &(final_results.loc[147,"Longhorn cattle"] <= 125) & (final_results.loc[147,"Longhorn cattle"] >= 75) &(final_results.loc[147,"Tamworth pigs"] <= 32) & (final_results.loc[147,"Tamworth pigs"] >= 12):
                    final_results["passed_filters"] += 1
                # May 2017
                if  (final_results.loc[148,"Exmoor pony"] <= 11) & (final_results.loc[148,"Exmoor pony"] >= 9) &(final_results.loc[148,"Longhorn cattle"] <= 134) & (final_results.loc[148,"Longhorn cattle"] >= 84) &(final_results.loc[148,"Tamworth pigs"] <= 32) & (final_results.loc[148,"Tamworth pigs"] >= 12):
                    final_results["passed_filters"] += 1
                # June 2017
                if (final_results.loc[149,"Exmoor pony"] <= 11) & (final_results.loc[149,"Exmoor pony"] >= 9) &(final_results.loc[149,"Longhorn cattle"] <= 119) & (final_results.loc[149,"Longhorn cattle"] >= 69) &(final_results.loc[149,"Tamworth pigs"] <= 32) & (final_results.loc[149,"Tamworth pigs"] >= 12):
                    final_results["passed_filters"] += 1
                # July 2017
                if (final_results.loc[150,"Exmoor pony"] <= 11) & (final_results.loc[150,"Exmoor pony"] >= 9) &(final_results.loc[150,"Longhorn cattle"] <= 119) & (final_results.loc[150,"Longhorn cattle"] >= 69)&(final_results.loc[150,"Tamworth pigs"] <= 32) & (final_results.loc[150,"Tamworth pigs"] >= 12):
                    final_results["passed_filters"] += 1
                # Aug 2017
                if (final_results.loc[151,"Exmoor pony"] <= 11) & (final_results.loc[151,"Exmoor pony"] >= 9) &(final_results.loc[151,"Longhorn cattle"] <= 119) & (final_results.loc[151,"Longhorn cattle"] >= 69)&(final_results.loc[151,"Tamworth pigs"] <= 32) & (final_results.loc[151,"Tamworth pigs"] >= 12):
                    final_results["passed_filters"] += 1
                # Sept 2017
                if (final_results.loc[152,"Exmoor pony"] <= 11) & (final_results.loc[152,"Exmoor pony"] >= 9) &(final_results.loc[152,"Longhorn cattle"] <= 115) & (final_results.loc[152,"Longhorn cattle"] >= 65)& (final_results.loc[152,"Tamworth pigs"] <= 32) & (final_results.loc[152,"Tamworth pigs"] >= 12):
                    final_results["passed_filters"] += 1
                # Oct 2017
                if (final_results.loc[153,"Exmoor pony"] <= 11) & (final_results.loc[153,"Exmoor pony"] >= 9) &(final_results.loc[153,"Longhorn cattle"] <= 113) & (final_results.loc[153,"Longhorn cattle"] >= 63)&(final_results.loc[153,"Tamworth pigs"] <= 32) & (final_results.loc[153,"Tamworth pigs"] >= 12):
                    final_results["passed_filters"] += 1
                # Nov 2017
                if (final_results.loc[154,"Exmoor pony"] <= 11) & (final_results.loc[154,"Exmoor pony"] >= 9) &(final_results.loc[154,"Longhorn cattle"] <= 113) & (final_results.loc[154,"Longhorn cattle"] >= 63)&(final_results.loc[154,"Tamworth pigs"] <= 32) & (final_results.loc[154,"Tamworth pigs"] >= 12):
                    final_results["passed_filters"] += 1
                # Dec 2017
                if (final_results.loc[155,"Exmoor pony"] <= 11) & (final_results.loc[155,"Exmoor pony"] >= 9) &(final_results.loc[155,"Longhorn cattle"] <= 113) & (final_results.loc[155,"Longhorn cattle"] >= 63)&(final_results.loc[155,"Tamworth pigs"] <= 28) & (final_results.loc[155,"Tamworth pigs"] >= 8):
                    final_results["passed_filters"] += 1
                # January 2018
                if (final_results.loc[156,"Exmoor pony"] <= 11) & (final_results.loc[156,"Exmoor pony"] >= 9) &(final_results.loc[156,"Longhorn cattle"] <= 113) & (final_results.loc[156,"Longhorn cattle"] >= 63)&(final_results.loc[156,"Tamworth pigs"] <= 21) & (final_results.loc[156,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # February 2018
                if (final_results.loc[157,"Exmoor pony"] <= 11) & (final_results.loc[157,"Exmoor pony"] >= 9) &(final_results.loc[157,"Longhorn cattle"] <= 113) & (final_results.loc[157,"Longhorn cattle"] >= 63)&(final_results.loc[157,"Tamworth pigs"] <= 26) & (final_results.loc[157,"Tamworth pigs"] >= 6):
                    final_results["passed_filters"] += 1
                # March 2018
                if (final_results.loc[158,"Exmoor pony"] <= 10) & (final_results.loc[158,"Exmoor pony"] >= 8) & (final_results.loc[158,"Longhorn cattle"] <= 113) & (final_results.loc[158,"Longhorn cattle"] >= 63) &(final_results.loc[158,"Red deer"] <= 29) & (final_results.loc[158,"Red deer"] >= 19) &(final_results.loc[158,"Tamworth pigs"] <= 26) & (final_results.loc[158,"Tamworth pigs"] >= 6):
                    final_results["passed_filters"] += 1
                # April 2018
                if (final_results.loc[159,"Exmoor pony"] <= 10) & (final_results.loc[159,"Exmoor pony"] >= 8) & (final_results.loc[159,"Longhorn cattle"] <= 126) & (final_results.loc[159,"Longhorn cattle"] >= 76) &(final_results.loc[159,"Tamworth pigs"] <= 26) & (final_results.loc[159,"Tamworth pigs"] >= 6):
                    final_results["passed_filters"] += 1
                # May 2018
                if (final_results.loc[160,"Exmoor pony"] <= 10) & (final_results.loc[160,"Exmoor pony"] >= 8) &(final_results.loc[160,"Longhorn cattle"] <= 142) & (final_results.loc[160,"Longhorn cattle"] >= 92)&(final_results.loc[160,"Tamworth pigs"] <= 33) & (final_results.loc[160,"Tamworth pigs"] >= 13):
                    final_results["passed_filters"] += 1
                # June 2018
                if (final_results.loc[161,"Exmoor pony"] <= 10) & (final_results.loc[161,"Exmoor pony"] >= 8) & (final_results.loc[161,"Longhorn cattle"] <= 128) & (final_results.loc[161,"Longhorn cattle"] >= 78)& (final_results.loc[161,"Tamworth pigs"] <= 33) & (final_results.loc[161,"Tamworth pigs"] >= 13):
                    final_results["passed_filters"] += 1
                # July 2018
                if (final_results.loc[162,"Exmoor pony"] <= 10) & (final_results.loc[162,"Exmoor pony"] >= 8) &(final_results.loc[162,"Longhorn cattle"] <= 128) & (final_results.loc[162,"Longhorn cattle"] >= 78)&(final_results.loc[162,"Tamworth pigs"] <= 32) & (final_results.loc[162,"Tamworth pigs"] >= 12):
                    final_results["passed_filters"] += 1
                # Aug 2018
                if (final_results.loc[163,"Longhorn cattle"] <= 127) & (final_results.loc[163,"Longhorn cattle"] >= 77) &(final_results.loc[163,"Tamworth pigs"] <= 32) & (final_results.loc[163,"Tamworth pigs"] >= 12):
                    final_results["passed_filters"] += 1
                # Sept 2018
                if (final_results.loc[164,"Longhorn cattle"] <= 131) & (final_results.loc[164,"Longhorn cattle"] >= 81) & (final_results.loc[164,"Tamworth pigs"] <= 32) & (final_results.loc[164,"Tamworth pigs"] >= 12):
                    final_results["passed_filters"] += 1
                # Oct 2018
                if (final_results.loc[165,"Longhorn cattle"] <= 126) & (final_results.loc[165,"Longhorn cattle"] >= 76) & (final_results.loc[165,"Tamworth pigs"] <= 31) & (final_results.loc[165,"Tamworth pigs"] >= 11):
                    final_results["passed_filters"] += 1
                # Nov 2018
                if (final_results.loc[166,"Longhorn cattle"] <= 118) & (final_results.loc[166,"Longhorn cattle"] >= 68) & (final_results.loc[166,"Tamworth pigs"] <= 19) & (final_results.loc[166,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # Dec 2018
                if (final_results.loc[167,"Longhorn cattle"] <= 114) & (final_results.loc[167,"Longhorn cattle"] >= 64) & (final_results.loc[167,"Tamworth pigs"] <= 19) & (final_results.loc[167,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # Jan 2019
                if (final_results.loc[168,"Longhorn cattle"] <= 114) & (final_results.loc[168,"Longhorn cattle"] >= 64) & (final_results.loc[168,"Tamworth pigs"] <= 19) & (final_results.loc[168,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # Feb 2019
                if (final_results.loc[169,"Longhorn cattle"] <= 112) & (final_results.loc[169,"Longhorn cattle"] >= 62) &(final_results.loc[169,"Tamworth pigs"] <= 20) & (final_results.loc[169,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # March 2019
                if (final_results.loc[170,"Fallow deer"] <= 303) & (final_results.loc[170,"Fallow deer"] >= 253) &(final_results.loc[170,"Longhorn cattle"] <= 112) & (final_results.loc[170,"Longhorn cattle"] >= 62) &(final_results.loc[170,"Red deer"] <= 42) & (final_results.loc[170,"Red deer"] >= 32) & (final_results.loc[170,"Tamworth pigs"] <= 19) & (final_results.loc[170,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # April 2019
                if (final_results.loc[171,"Longhorn cattle"] <= 126) & (final_results.loc[171,"Longhorn cattle"] >= 76) &(final_results.loc[171,"Tamworth pigs"] <= 18) & (final_results.loc[171,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # May 2019
                if (final_results.loc[172,"Longhorn cattle"] <= 135) & (final_results.loc[172,"Longhorn cattle"] >= 85) & (final_results.loc[172,"Tamworth pigs"] <= 18) & (final_results.loc[172,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # June 2019
                if (final_results.loc[173,"Longhorn cattle"] <= 114) & (final_results.loc[173,"Longhorn cattle"] >= 64) & (final_results.loc[173,"Tamworth pigs"] <= 18) & (final_results.loc[173,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # July 2019
                if (final_results.loc[174,"Longhorn cattle"] <= 116) & (final_results.loc[174,"Longhorn cattle"] >= 66) &(final_results.loc[174,"Tamworth pigs"] <= 19) & (final_results.loc[174,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # Aug 2019
                if (final_results.loc[175,"Longhorn cattle"] <= 116) & (final_results.loc[175,"Longhorn cattle"] >= 66) & (final_results.loc[175,"Tamworth pigs"] <= 19) & (final_results.loc[175,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # Sept 2019
                if (final_results.loc[176,"Longhorn cattle"] <= 118) & (final_results.loc[176,"Longhorn cattle"] >= 68) & (final_results.loc[176,"Tamworth pigs"] <= 19) & (final_results.loc[176,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # Oct 2019
                if (final_results.loc[177,"Longhorn cattle"] <= 113) & (final_results.loc[177,"Longhorn cattle"] >= 63) &(final_results.loc[177,"Tamworth pigs"] <= 19) & (final_results.loc[177,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # Nov 2019
                if (final_results.loc[178,"Longhorn cattle"] <= 112) & (final_results.loc[178,"Longhorn cattle"] >= 62) & (final_results.loc[178,"Tamworth pigs"] <= 19) & (final_results.loc[178,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # Dec 2019
                if (final_results.loc[179,"Longhorn cattle"] <= 105) & (final_results.loc[179,"Longhorn cattle"] >= 55) & (final_results.loc[179,"Tamworth pigs"] <= 20) & (final_results.loc[179,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # Jan 2020
                if (final_results.loc[180,"Longhorn cattle"] <= 105) & (final_results.loc[180,"Longhorn cattle"] >= 55) & (final_results.loc[180,"Tamworth pigs"] <= 20) & (final_results.loc[180,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1

                # Feb 2020
                if (final_results.loc[181,"Longhorn cattle"] <= 104) & (final_results.loc[181,"Longhorn cattle"] >= 54) & (final_results.loc[181,"Tamworth pigs"] <= 18) & (final_results.loc[181,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # March 2020
                if (final_results.loc[182,"Fallow deer"] <= 272) & (final_results.loc[182,"Fallow deer"] >= 222) & (final_results.loc[182,"Red deer"] <= 40) & (final_results.loc[182,"Red deer"] >= 32) &(final_results.loc[182,"Longhorn cattle"] <= 106) & (final_results.loc[182,"Longhorn cattle"] >= 56)&(final_results.loc[182,"Tamworth pigs"] <= 17) & (final_results.loc[182,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # April 2020
                if (final_results.loc[183,"Exmoor pony"] <= 17) & (final_results.loc[183,"Exmoor pony"] >= 14) &(final_results.loc[183,"Longhorn cattle"] <= 106) & (final_results.loc[183,"Longhorn cattle"] >= 56) &(final_results.loc[183,"Tamworth pigs"] <= 17) & (final_results.loc[183,"Tamworth pigs"] >= 1):
                    final_results["passed_filters"] += 1
                # May 2020
                if (final_results.loc[184,"Tamworth pigs"] <= 29) & (final_results.loc[184,"Tamworth pigs"] >= 9) &(final_results.loc[184,"Exmoor pony"] <= 17) & (final_results.loc[184,"Exmoor pony"] >= 14) &(final_results.loc[184,"Longhorn cattle"] <= 106) & (final_results.loc[184,"Longhorn cattle"] >= 56) &(final_results.loc[184,"Roe deer"] <= 80) & (final_results.loc[184,"Roe deer"] >= 20) & (final_results.loc[184,"Grassland"] <= 69) & (final_results.loc[184,"Grassland"] >= 49) & (final_results.loc[184,"Thorny Scrub"] <= 35) & (final_results.loc[184,"Thorny Scrub"] >= 21) &(final_results.loc[184,"Woodland"] <= 29) & (final_results.loc[184,"Woodland"] >= 9):
                    final_results["passed_filters"] += 1

                # how many filters did they pass?
                sensitivity_results_list.append(final_results.loc[0,"passed_filters"]/64)
                # and the parameter changed
                sensitivity_parameters.append(ifor_val)
                perc_numbers.append(str(perc_number))

# append to dataframe
merged_dfs = pd.concat([pd.DataFrame({'Filters': sensitivity_results_list}), pd.DataFrame({'Parameter': sensitivity_parameters}), pd.DataFrame({'Percentage': perc_numbers})], axis=1)

# plot it
sns.scatterplot(data=merged_dfs, x="Parameter", y="Filters", hue="Percentage", palette="viridis")
plt.title('Sensitivity test results for the parameter: roeDeer_reproduce')
plt.xlabel('Parameter value')
plt.ylabel('Percentage of filters passed')
plt.legend(title='Percentage around accepted \n parameter values', ncol=2)
plt.savefig('ks-test-roeDeer_reproduce.png')

plt.show()

