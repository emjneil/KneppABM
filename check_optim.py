# ------ ABM of the Knepp Estate (2005-2046) --------
from KneppModel_ABM import KneppModel 
from geneticAlgorithm import run_optimizer
import numpy as np
import random
import pandas as pd

variables = [
    # habitat variables
    "chance_reproduceSapling", # this is to initialize the initial dominant condition
    "chance_reproduceYoungScrub",  # this is to initialize the initial dominant condition
    "chance_regrowGrass", # this is to initialize the initial dominant condition
    "chance_saplingBecomingTree",
    "chance_youngScrubMatures",
    "chance_scrubOutcompetedByTree", # if tree matures, chance of scrub decreasing
    "chance_grassOutcompetedByTree",
    "chance_grassOutcompetedByScrub",
    "chance_saplingOutcompetedByTree",
    "chance_saplingOutcompetedByScrub",
    "chance_youngScrubOutcompetedByScrub",
    "chance_youngScrubOutcompetedByTree",
    # roe deer variables
    "roeDeer_reproduce",
    "roeDeer_gain_from_grass",
    "roeDeer_gain_from_Trees",
    "roeDeer_gain_from_Scrub",
    "roeDeer_gain_from_Saplings", 
    "roeDeer_gain_from_YoungScrub", 
    "roeDeer_impactGrass",
    "roeDeer_saplingsEaten",
    "roeDeer_youngScrubEaten",
    "roeDeer_treesEaten",
    "roeDeer_scrubEaten",
    # Exmoor pony variables
    "ponies_gain_from_grass", 
    "ponies_gain_from_Trees", 
    "ponies_gain_from_Scrub", 
    "ponies_gain_from_Saplings", 
    "ponies_gain_from_YoungScrub", 
    "ponies_impactGrass", 
    "ponies_saplingsEaten", 
    "ponies_youngScrubEaten", 
    "ponies_treesEaten", 
    "ponies_scrubEaten", 
    # Cow variables
    "cows_reproduce", 
    "cows_gain_from_grass", 
    "cows_gain_from_Trees", 
    "cows_gain_from_Scrub", 
    "cows_gain_from_Saplings", 
    "cows_gain_from_YoungScrub", 
    "cows_impactGrass", 
    "cows_saplingsEaten", 
    "cows_youngScrubEaten", 
    "cows_treesEaten", 
    "cows_scrubEaten", 
    # Fallow deer variables
    "fallowDeer_reproduce", 
    "fallowDeer_gain_from_grass", 
    "fallowDeer_gain_from_Trees", 
    "fallowDeer_gain_from_Scrub", 
    "fallowDeer_gain_from_Saplings", 
    "fallowDeer_gain_from_YoungScrub", 
    "fallowDeer_impactGrass", 
    "fallowDeer_saplingsEaten", 
    "fallowDeer_youngScrubEaten", 
    "fallowDeer_treesEaten", 
    "fallowDeer_scrubEaten",
    # Red deer variables
    "redDeer_reproduce", 
    "redDeer_gain_from_grass", 
    "redDeer_gain_from_Trees", 
    "redDeer_gain_from_Scrub", 
    "redDeer_gain_from_Saplings", 
    "redDeer_gain_from_YoungScrub", 
    "redDeer_impactGrass", 
    "redDeer_saplingsEaten", 
    "redDeer_youngScrubEaten", 
    "redDeer_treesEaten", 
    "redDeer_scrubEaten", 
    # Pig variables
    "pigs_reproduce", 
    "pigs_gain_from_grass", 
    "pigs_gain_from_Saplings", 
    "pigs_gain_from_YoungScrub", 
    "pigs_impactGrass", 
    "pigs_saplingsEaten", 
    "pigs_youngScrubEaten" 
    ]

# # # # Run the model # # # # 
final_results_list = []
final_parameters = []


# define parameters 
data = np.array([2.14640414e-01, 1.27429762e-01, 2.48598840e-01, 6.38804329e-04,
       1.25202164e-03, 6.28817878e-01, 3.84309028e-02, 1.73619971e-01,
       9.09465491e-01, 7.04967854e-01, 2.64991933e-01, 4.93093884e-01,
       1.83753609e-01, 4.49413634e-01, 6.63794244e-02, 1.18006194e-01,
       2.32875880e-02, 3.31495962e-01, 4.77913229e-01, 5.33772467e-01,
       5.62464194e-02, 3.11133150e-01, 4.93014281e-01, 1.39671528e-01,
       1.60183212e-01, 4.56217869e-02, 5.31463289e-02, 3.02970658e-01,
       4.30833338e-01, 9.90689713e-02, 1.07476228e-01, 5.28377414e-01,
       2.65606244e-02, 5.03209123e-02, 1.40849903e-01, 6.69560509e-01,
       4.97850560e-01, 2.71894286e-01, 4.74087966e-01, 1.83050850e-01,
       2.65510327e-01, 4.88448975e-01, 3.25708684e-01, 1.45626189e-01,
       4.07401171e-01, 4.18174983e+01, 1.65198247e+01, 8.10016451e+01,
       8.38062147e+01, 2.60804182e+01, 7.65958600e+01, 4.39386888e+03,
       1.08546184e+03, 1.16313086e+03, 2.12090381e+03, 6.67257499e+02,
       3.83329133e+03, 6.36887989e+02, 1.47869268e+03, 4.42938235e+03,
       3.13160152e+03, 3.24785911e+03, 4.58972826e+03, 4.77156111e+02,
       1.95666263e+02, 1.15417779e+02, 1.59960520e+02, 4.54744289e+02,
       4.03527402e+02, 1.57918848e+02, 4.58347445e+02, 2.75874577e+02,
       3.76294124e+02]) 
# pass column names in the columns parameter 
df = pd.DataFrame(data).transpose()
df.columns = variables

# run it 5% lower for each parameter, one at a time
# then graph it



for i in df.columns:
    parameters = df
    
    # run it 10% higher for each parameter, one at a time
    print(i)
    old_i = 1
    # i = int(i + (i*0.1))
    initial_roeDeer = random.randint(6, 18)
    initial_grassland = random.randint(75, 85)
    initial_woodland = random.randint(9, 19)
    initial_scrubland = random.randint(0, 6)

    # save all the outputs 

    # choose my parameters 

    # keep track of my parameters
    parameters_used = [
        
        ]
    # append to dataframe
    final_parameters.append(parameters_used)

    # keep track of the runs
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
    final_results_list.append(results)

# append to dataframe
final_results = pd.concat(final_results_list)




variables_2 = [
    # number of runs
    "run_number",
    # habitat variables
    "chance_reproduceSapling", # this is to initialize the initial dominant condition
    "chance_reproduceYoungScrub",  # this is to initialize the initial dominant condition
    "chance_regrowGrass", # this is to initialize the initial dominant condition
    "chance_saplingBecomingTree",
    "chance_youngScrubMatures",
    "chance_scrubOutcompetedByTree", # if tree matures, chance of scrub decreasing
    "chance_grassOutcompetedByTree",
    "chance_grassOutcompetedByScrub",
    "chance_saplingOutcompetedByTree",
    "chance_saplingOutcompetedByScrub",
    "chance_youngScrubOutcompetedByScrub",
    "chance_youngScrubOutcompetedByTree",
    # initial values
    "initial_roeDeer",
    "initial_grassland",
    "initial_woodland",
    "initial_scrubland",
    # roe deer variables
    "roeDeer_reproduce",
    "roeDeer_gain_from_grass",
    "roeDeer_gain_from_Trees",
    "roeDeer_gain_from_Scrub",
    "roeDeer_gain_from_Saplings", 
    "roeDeer_gain_from_YoungScrub", 
    "roeDeer_impactGrass",
    "roeDeer_saplingsEaten",
    "roeDeer_youngScrubEaten",
    "roeDeer_treesEaten",
    "roeDeer_scrubEaten",
    # Exmoor pony variables
    "ponies_gain_from_grass", 
    "ponies_gain_from_Trees", 
    "ponies_gain_from_Scrub", 
    "ponies_gain_from_Saplings", 
    "ponies_gain_from_YoungScrub", 
    "ponies_impactGrass", 
    "ponies_saplingsEaten", 
    "ponies_youngScrubEaten", 
    "ponies_treesEaten", 
    "ponies_scrubEaten", 
    # Cow variables
    "cows_reproduce", 
    "cows_gain_from_grass", 
    "cows_gain_from_Trees", 
    "cows_gain_from_Scrub", 
    "cows_gain_from_Saplings", 
    "cows_gain_from_YoungScrub", 
    "cows_impactGrass", 
    "cows_saplingsEaten", 
    "cows_youngScrubEaten", 
    "cows_treesEaten", 
    "cows_scrubEaten", 
    # Fallow deer variables
    "fallowDeer_reproduce", 
    "fallowDeer_gain_from_grass", 
    "fallowDeer_gain_from_Trees", 
    "fallowDeer_gain_from_Scrub", 
    "fallowDeer_gain_from_Saplings", 
    "fallowDeer_gain_from_YoungScrub", 
    "fallowDeer_impactGrass", 
    "fallowDeer_saplingsEaten", 
    "fallowDeer_youngScrubEaten", 
    "fallowDeer_treesEaten", 
    "fallowDeer_scrubEaten",
    # Red deer variables
    "redDeer_reproduce", 
    "redDeer_gain_from_grass", 
    "redDeer_gain_from_Trees", 
    "redDeer_gain_from_Scrub", 
    "redDeer_gain_from_Saplings", 
    "redDeer_gain_from_YoungScrub", 
    "redDeer_impactGrass", 
    "redDeer_saplingsEaten", 
    "redDeer_youngScrubEaten", 
    "redDeer_treesEaten", 
    "redDeer_scrubEaten", 
    # Pig variables
    "pigs_reproduce", 
    "pigs_gain_from_grass", 
    "pigs_gain_from_Saplings", 
    "pigs_gain_from_YoungScrub", 
    "pigs_impactGrass", 
    "pigs_saplingsEaten", 
    "pigs_youngScrubEaten" 
    ]

# check out the parameters used
final_parameters = pd.DataFrame(data=final_parameters, columns=variables_2)
print(final_parameters['initial_grassland'].min())
print(final_parameters['initial_grassland'].max())

# filter the runs and tag the dataframe
# pre-reintroduction model
accepted_preReintro = final_results[(final_results["Time"] == 49) &
(final_results["Roe deer"] <= 40) & (final_results["Roe deer"] >= 6) &
(final_results["Grassland"] <= 90) & (final_results["Grassland"] >= 49) & 
(final_results["Woodland"] <= 27) & (final_results["Woodland"] >= 7) & 
(final_results["Thorny Scrub"] <= 21) & (final_results["Thorny Scrub"] >= 1)]
print("number passed pre-reintro filters:", len(accepted_preReintro))
# April 2015
accepted_April2015 = accepted_preReintro[(accepted_preReintro["Time"] == 123) &
(accepted_preReintro["Exmoor pony"] <= 11) & (accepted_preReintro["Exmoor pony"] >= 9) &
(accepted_preReintro["Longhorn cattle"] <= 127) & (accepted_preReintro["Longhorn cattle"] >= 104) &
(accepted_preReintro["Tamworth pigs"] <= 24) & (accepted_preReintro["Tamworth pigs"] >= 20)]
print("number passed April 2015 filters:", len(accepted_April2015))
# May 2015
accepted_May2015 = accepted_April2015[(accepted_April2015["Time"] == 124) &
(accepted_April2015["Longhorn cattle"] <= 142) & (accepted_April2015["Longhorn cattle"] >= 116) &
(accepted_April2015["Tamworth pigs"] <= 15) & (accepted_April2015["Tamworth pigs"] >= 13) &
(accepted_April2015["Exmoor pony"] <= 11) & (accepted_April2015["Exmoor pony"] >= 9)]
print("number passed May 2015 filters:", len(accepted_May2015))
# June 2015
accepted_June2015 = accepted_May2015[(accepted_May2015["Time"] == 125) &
(accepted_May2015["Longhorn cattle"] <= 142) & (accepted_May2015["Longhorn cattle"] >= 116) &
(accepted_May2015["Exmoor pony"] <= 11) & (accepted_May2015["Exmoor pony"] >= 9) &
(accepted_May2015["Tamworth pigs"] <= 15) & (accepted_May2015["Tamworth pigs"] >= 13)]
print("number passed June 2015 filters:", len(accepted_June2015))
# July 2015
accepted_July2015 = accepted_June2015[(accepted_June2015["Time"] == 126) &
(accepted_June2015["Longhorn cattle"] <= 142) & (accepted_June2015["Longhorn cattle"] >= 116) &
(accepted_June2015["Exmoor pony"] <= 11) & (accepted_June2015["Exmoor pony"] >= 9) &
(accepted_June2015["Tamworth pigs"] <= 15) & (accepted_June2015["Tamworth pigs"] >= 13)]
print("number passed July 2015 filters:", len(accepted_July2015))
# Aug 2015
accepted_Aug2015 = accepted_July2015[(accepted_July2015["Time"] == 127) &
(accepted_July2015["Longhorn cattle"] <= 142) & (accepted_July2015["Longhorn cattle"] >= 116) &
(accepted_July2015["Exmoor pony"] <= 11) & (accepted_July2015["Exmoor pony"] >= 9) &
(accepted_July2015["Tamworth pigs"] <= 15) & (accepted_July2015["Tamworth pigs"] >= 13)]
print("number passed Aug 2015 filters:", len(accepted_Aug2015))
# Sept 2015
accepted_Sept2015 = accepted_Aug2015[(accepted_Aug2015["Time"] == 128) &
(accepted_Aug2015["Longhorn cattle"] <= 143) & (accepted_Aug2015["Longhorn cattle"] >= 117) &
(accepted_Aug2015["Exmoor pony"] <= 11) & (accepted_Aug2015["Exmoor pony"] >= 9) &
(accepted_Aug2015["Tamworth pigs"] <= 15) & (accepted_Aug2015["Tamworth pigs"] >= 13)]
print("number passed Sept 2015 filters:", len(accepted_Sept2015))
# Oct 2015
accepted_Oct2015 = accepted_Sept2015[(accepted_Sept2015["Time"] == 129) &
(accepted_Sept2015["Longhorn cattle"] <= 100) & (accepted_Sept2015["Longhorn cattle"] >= 82) &
(accepted_Sept2015["Exmoor pony"] <= 11) & (accepted_Sept2015["Exmoor pony"] >= 9) &
(accepted_Sept2015["Tamworth pigs"] <= 15) & (accepted_Sept2015["Tamworth pigs"] >= 13)]
print("number passed Oct 2015 filters:", len(accepted_Oct2015))
# Nov 2015
accepted_Nov2015 = accepted_Oct2015[(accepted_Oct2015["Time"] == 130) &
(accepted_Oct2015["Longhorn cattle"] <= 100) & (accepted_Oct2015["Longhorn cattle"] >= 82) &
(accepted_Oct2015["Exmoor pony"] <= 11) & (accepted_Oct2015["Exmoor pony"] >= 9) &
(accepted_Oct2015["Tamworth pigs"] <= 14) & (accepted_Oct2015["Tamworth pigs"] >= 12)]
print("number passed Nov 2015 filters:", len(accepted_Nov2015))
# Dec 2015
accepted_Dec2015 = accepted_Nov2015[(accepted_Nov2015["Time"] == 131) &
(accepted_Nov2015["Longhorn cattle"] <= 94) & (accepted_Nov2015["Longhorn cattle"] >= 77) &
(accepted_Nov2015["Exmoor pony"] <= 11) & (accepted_Nov2015["Exmoor pony"] >= 9) &
(accepted_Nov2015["Tamworth pigs"] <= 14) & (accepted_Nov2015["Tamworth pigs"] >= 12)]
print("number passed Dec 2015 filters:", len(accepted_Dec2015))
# Jan 2016
accepted_Jan2016 = accepted_Dec2015[(accepted_Dec2015["Time"] == 132) &
(accepted_Dec2015["Longhorn cattle"] <= 94) & (accepted_Dec2015["Longhorn cattle"] >= 77) &
(accepted_Dec2015["Exmoor pony"] <= 11) & (accepted_Dec2015["Exmoor pony"] >= 9) &
(accepted_Dec2015["Tamworth pigs"] <= 11) & (accepted_Dec2015["Tamworth pigs"] >= 9)]
print("number passed Jan 2016 filters:", len(accepted_Jan2016))
# Feb 2016
accepted_Feb2016 = accepted_Jan2016[(accepted_Jan2016["Time"] == 133) &
(accepted_Jan2016["Exmoor pony"] <= 11) & (accepted_Jan2016["Exmoor pony"] >= 9) &
(accepted_Jan2016["Longhorn cattle"] <= 94) & (accepted_Jan2016["Longhorn cattle"] >= 77) &
(accepted_Jan2016["Tamworth pigs"] <= 9) & (accepted_Jan2016["Tamworth pigs"] >= 7)]
print("number passed February 2016 filters:", len(accepted_Feb2016))
# March 2016
accepted_March2016 = accepted_Feb2016[(accepted_Feb2016["Time"] == 134) &
(accepted_Feb2016["Exmoor pony"] <= 12) & (accepted_Feb2016["Exmoor pony"] >= 10) &
(accepted_Feb2016["Longhorn cattle"] <= 94) & (accepted_Feb2016["Longhorn cattle"] >= 77) &
(accepted_Feb2016["Fallow deer"] <= 154) & (accepted_Feb2016["Fallow deer"] >= 126) &
(accepted_Feb2016["Red deer"] <= 29) & (accepted_Feb2016["Red deer"] >= 23) &
(accepted_Feb2016["Tamworth pigs"] <= 10) & (accepted_Feb2016["Tamworth pigs"] >= 8)]
print("number passed March 2016 filters:", len(accepted_March2016))
# April 2016
accepted_April2016 = accepted_March2016[(accepted_March2016["Time"] == 135) &
(accepted_March2016["Exmoor pony"] <= 12) & (accepted_March2016["Exmoor pony"] >= 10) &
(accepted_March2016["Longhorn cattle"] <= 113) & (accepted_March2016["Longhorn cattle"] >= 93) &
(accepted_March2016["Tamworth pigs"] <= 10) & (accepted_March2016["Tamworth pigs"] >= 8)]
print("number passed April 2016 filters:", len(accepted_April2016))
# May 2016
accepted_May2016 = accepted_April2016[(accepted_April2016["Time"] == 136) &
(accepted_April2016["Exmoor pony"] <= 12) & (accepted_April2016["Exmoor pony"] >= 10) &
(accepted_April2016["Longhorn cattle"] <= 119) & (accepted_April2016["Longhorn cattle"] >= 97) &
(accepted_April2016["Tamworth pigs"] <= 19) & (accepted_April2016["Tamworth pigs"] >= 15)]
print("number passed May 2016 filters:", len(accepted_May2016))
# June 2016
accepted_June2016 = accepted_May2016[(accepted_May2016["Time"] == 137) &
(accepted_May2016["Exmoor pony"] <= 12) & (accepted_May2016["Exmoor pony"] >= 10) &
(accepted_May2016["Longhorn cattle"] <= 98) & (accepted_May2016["Longhorn cattle"] >= 80) &
(accepted_May2016["Tamworth pigs"] <= 19) & (accepted_May2016["Tamworth pigs"] >= 15)]
print("number passed June 2016 filters:", len(accepted_June2016))
# July 2016
accepted_July2016 = accepted_June2016[(accepted_June2016["Time"] == 138) &
(accepted_June2016["Exmoor pony"] <= 12) & (accepted_June2016["Exmoor pony"] >= 10) &
(accepted_June2016["Longhorn cattle"] <= 96) & (accepted_June2016["Longhorn cattle"] >= 78) &
(accepted_June2016["Tamworth pigs"] <= 19) & (accepted_June2016["Tamworth pigs"] >= 15)]
print("number passed July 2016 filters:", len(accepted_July2016))
# Aug 2016
accepted_Aug2016 = accepted_July2016[(accepted_July2016["Time"] == 139) &
(accepted_July2016["Exmoor pony"] <= 12) & (accepted_July2016["Exmoor pony"] >= 10) &
(accepted_July2016["Longhorn cattle"] <= 96) & (accepted_July2016["Longhorn cattle"] >= 78) &
(accepted_July2016["Tamworth pigs"] <= 19) & (accepted_July2016["Tamworth pigs"] >= 15)]
print("number passed Aug 2016 filters:", len(accepted_Aug2016))
# Sept 2016
accepted_Sept2016 = accepted_Aug2016[(accepted_Aug2016["Time"] == 140) &
(accepted_Aug2016["Exmoor pony"] <= 12) & (accepted_Aug2016["Exmoor pony"] >= 10) &
(accepted_Aug2016["Longhorn cattle"] <= 107) & (accepted_Aug2016["Longhorn cattle"] >= 87) &
(accepted_Aug2016["Tamworth pigs"] <= 19) & (accepted_Aug2016["Tamworth pigs"] >= 15)]
print("number passed Sept 2016 filters:", len(accepted_Sept2016))
# Oct 2016
accepted_Oct2016 = accepted_Sept2016[(accepted_Sept2016["Time"] == 141) &
(accepted_Sept2016["Exmoor pony"] <= 12) & (accepted_Sept2016["Exmoor pony"] >= 10) &
(accepted_Sept2016["Longhorn cattle"] <= 107) & (accepted_Sept2016["Longhorn cattle"] >= 87) &
(accepted_Sept2016["Tamworth pigs"] <= 19) & (accepted_Sept2016["Tamworth pigs"] >= 15)]
print("number passed Oct 2016 filters:", len(accepted_Oct2016))
# Nov 2016
accepted_Nov2016 = accepted_Oct2016[(accepted_Oct2016["Time"] == 142) &
(accepted_Oct2016["Exmoor pony"] <= 12) & (accepted_Oct2016["Exmoor pony"] >= 10) &
(accepted_Oct2016["Longhorn cattle"] <= 101) & (accepted_Oct2016["Longhorn cattle"] >= 83) &
(accepted_Oct2016["Tamworth pigs"] <= 19) & (accepted_Oct2016["Tamworth pigs"] >= 15)]
print("number passed Nov 2016 filters:", len(accepted_Nov2016))
# Dec 2016
accepted_Dec2016 = accepted_Nov2016[(accepted_Nov2016["Time"] == 143) &
(accepted_Nov2016["Exmoor pony"] <= 12) & (accepted_Nov2016["Exmoor pony"] >= 10) &
(accepted_Nov2016["Longhorn cattle"] <= 87) & (accepted_Nov2016["Longhorn cattle"] >= 71) &
(accepted_Nov2016["Tamworth pigs"] <= 14) & (accepted_Nov2016["Tamworth pigs"] >= 12)]
print("number passed Dec 2016 filters:", len(accepted_Dec2016))
# Jan 2017
accepted_Jan2017= accepted_Dec2016[(accepted_Dec2016["Time"] == 144) &
(accepted_Dec2016["Exmoor pony"] <= 12) & (accepted_Dec2016["Exmoor pony"] >= 10) &
(accepted_Dec2016["Longhorn cattle"] <= 87) & (accepted_Dec2016["Longhorn cattle"] >= 71) &
(accepted_Dec2016["Tamworth pigs"] <= 10) & (accepted_Dec2016["Tamworth pigs"] >= 8)]
print("number passed Jan 2017 filters:", len(accepted_Jan2017))
# Feb 2017
accepted_Feb2017 = accepted_Jan2017[(accepted_Jan2017["Time"] == 145) &
(accepted_Jan2017["Exmoor pony"] <= 12) & (accepted_Jan2017["Exmoor pony"] >= 10) &
(accepted_Jan2017["Longhorn cattle"] <= 87) & (accepted_Jan2017["Longhorn cattle"] >= 71) &
(accepted_Jan2017["Tamworth pigs"] <= 8) & (accepted_Jan2017["Tamworth pigs"] >= 6)]
print("number passed Feb 2017 filters:", len(accepted_Feb2017))
# March 2017
accepted_March2017 = accepted_Feb2017[(accepted_Feb2017["Time"] == 146) &
(accepted_Feb2017["Exmoor pony"] <= 11) & (accepted_Feb2017["Exmoor pony"] >= 9) &
(accepted_Feb2017["Fallow deer"] <= 182) & (accepted_Feb2017["Fallow deer"] >= 149) &
(accepted_Feb2017["Longhorn cattle"] <= 87) & (accepted_Feb2017["Longhorn cattle"] >= 71) &
(accepted_Feb2017["Tamworth pigs"] <= 8) & (accepted_Feb2017["Tamworth pigs"] >= 6)]
print("number passed March 2017 filters:", len(accepted_March2017))
# April 2017
accepted_April2017 = accepted_March2017[(accepted_March2017["Time"] == 147) &
(accepted_March2017["Exmoor pony"] <= 11) & (accepted_March2017["Exmoor pony"] >= 9) &
(accepted_March2017["Longhorn cattle"] <= 110) & (accepted_March2017["Longhorn cattle"] >= 90) &
(accepted_March2017["Tamworth pigs"] <= 24) & (accepted_March2017["Tamworth pigs"] >= 20)]
print("number passed April 2017 filters:", len(accepted_April2017))
# May 2017
accepted_May2017 = accepted_April2017[(accepted_April2017["Time"] == 148) &
(accepted_April2017["Exmoor pony"] <= 11) & (accepted_April2017["Exmoor pony"] >= 9) &
(accepted_April2017["Longhorn cattle"] <= 120) & (accepted_April2017["Longhorn cattle"] >= 98) &
(accepted_April2017["Tamworth pigs"] <= 24) & (accepted_April2017["Tamworth pigs"] >= 20)]
print("number passed May 2017 filters:", len(accepted_May2017))
# June 2017
accepted_June2017 = accepted_May2017[(accepted_May2017["Time"] == 149) &
(accepted_May2017["Exmoor pony"] <= 11) & (accepted_May2017["Exmoor pony"] >= 9) &
(accepted_May2017["Longhorn cattle"] <= 103) & (accepted_May2017["Longhorn cattle"] >= 85) &
(accepted_May2017["Tamworth pigs"] <= 24) & (accepted_May2017["Tamworth pigs"] >= 20)]
print("number passed June 2017 filters:", len(accepted_June2017))
# July 2017
accepted_July2017 = accepted_June2017[(accepted_June2017["Time"] == 150) &
(accepted_June2017["Exmoor pony"] <= 11) & (accepted_June2017["Exmoor pony"] >= 9) &
(accepted_June2017["Longhorn cattle"] <= 103) & (accepted_June2017["Longhorn cattle"] >= 85) &
(accepted_June2017["Tamworth pigs"] <= 24) & (accepted_June2017["Tamworth pigs"] >= 20)]
print("number passed July 2017 filters:", len(accepted_July2017))
# Aug 2017
accepted_Aug2017 = accepted_July2017[(accepted_July2017["Time"] == 151) &
(accepted_July2017["Exmoor pony"] <= 11) & (accepted_July2017["Exmoor pony"] >= 9) &
(accepted_July2017["Longhorn cattle"] <= 103) & (accepted_July2017["Longhorn cattle"] >= 85) &
(accepted_July2017["Tamworth pigs"] <= 24) & (accepted_July2017["Tamworth pigs"] >= 20)]
print("number passed Aug 2017 filters:", len(accepted_Aug2017))
# Sept 2017
accepted_Sept2017 = accepted_Aug2017[(accepted_Aug2017["Time"] == 152) &
(accepted_Aug2017["Exmoor pony"] <= 11) & (accepted_Aug2017["Exmoor pony"] >= 9) &
(accepted_Aug2017["Longhorn cattle"] <= 99) & (accepted_Aug2017["Longhorn cattle"] >= 81) &
(accepted_Aug2017["Tamworth pigs"] <= 24) & (accepted_Aug2017["Tamworth pigs"] >= 20)]
print("number passed Sept 2017 filters:", len(accepted_Sept2017))
# Oct 2017
accepted_Oct2017 = accepted_Sept2017[(accepted_Sept2017["Time"] == 153) &
(accepted_Sept2017["Exmoor pony"] <= 11) & (accepted_Sept2017["Exmoor pony"] >= 9) &
(accepted_Sept2017["Longhorn cattle"] <= 97) & (accepted_Sept2017["Longhorn cattle"] >= 79) &
(accepted_Sept2017["Tamworth pigs"] <= 24) & (accepted_Sept2017["Tamworth pigs"] >= 20)]
print("number passed Oct 2017 filters:", len(accepted_Oct2017))
# Nov 2017
accepted_Nov2017 = accepted_Oct2017[(accepted_Oct2017["Time"] == 154) &
(accepted_Oct2017["Exmoor pony"] <= 11) & (accepted_Oct2017["Exmoor pony"] >= 9) &
(accepted_Oct2017["Longhorn cattle"] <= 97) & (accepted_Oct2017["Longhorn cattle"] >= 79) &
(accepted_Oct2017["Tamworth pigs"] <= 24) & (accepted_Oct2017["Tamworth pigs"] >= 20)]
print("number passed Nov 2017 filters:", len(accepted_Nov2017))
# Dec 2017
accepted_Dec2017 = accepted_Nov2017[(accepted_Nov2017["Time"] == 155) &
(accepted_Nov2017["Exmoor pony"] <= 11) & (accepted_Nov2017["Exmoor pony"] >= 9) &
(accepted_Nov2017["Longhorn cattle"] <= 97) & (accepted_Nov2017["Longhorn cattle"] >= 79) &
(accepted_Nov2017["Tamworth pigs"] <= 20) & (accepted_Nov2017["Tamworth pigs"] >= 16)]
print("number passed Dec 2017 filters:", len(accepted_Dec2017))
# January 2018
accepted_Jan2018 = accepted_Dec2017[(accepted_Dec2017["Time"] == 156) &
(accepted_Dec2017["Exmoor pony"] <= 11) & (accepted_Dec2017["Exmoor pony"] >= 9) &
(accepted_Dec2017["Longhorn cattle"] <= 97) & (accepted_Dec2017["Longhorn cattle"] >= 79) &
(accepted_Dec2017["Tamworth pigs"] <= 12) & (accepted_Dec2017["Tamworth pigs"] >= 10)]
print("number passed January 2018 filters:", len(accepted_Jan2018))
# February 2018
accepted_Feb2018 = accepted_Jan2018[(accepted_Jan2018["Time"] == 157) &
(accepted_Jan2018["Exmoor pony"] <= 11) & (accepted_Jan2018["Exmoor pony"] >= 9) &
(accepted_Jan2018["Longhorn cattle"] <= 97) & (accepted_Jan2018["Longhorn cattle"] >= 79) &
(accepted_Jan2018["Tamworth pigs"] <= 18) & (accepted_Jan2018["Tamworth pigs"] >= 14)]
print("number passed Feb 2018 filters:", len(accepted_Feb2018)) 
# March 2018
accepted_March2018 = accepted_Feb2018[(accepted_Feb2018["Time"] == 158) &
(accepted_Feb2018["Exmoor pony"] <= 10) & (accepted_Feb2018["Exmoor pony"] >= 8) &
(accepted_Feb2018["Fallow deer"] <= 276) & (accepted_Feb2018["Fallow deer"] >= 226) &
(accepted_Feb2018["Longhorn cattle"] <= 97) & (accepted_Feb2018["Longhorn cattle"] >= 79) &
(accepted_Feb2018["Red deer"] <= 26) & (accepted_Feb2018["Red deer"] >= 22) &
(accepted_Feb2018["Tamworth pigs"] <= 18) & (accepted_Feb2018["Tamworth pigs"] >= 14)]
print("number passed March 2018 filters:", len(accepted_March2018)) 
# April 2018
accepted_April2018 = accepted_March2018[(accepted_March2018["Time"] == 159) &
(accepted_March2018["Exmoor pony"] <= 10) & (accepted_March2018["Exmoor pony"] >= 8) &
(accepted_March2018["Longhorn cattle"] <= 111) & (accepted_March2018["Longhorn cattle"] >= 91) &
(accepted_March2018["Tamworth pigs"] <= 18) & (accepted_March2018["Tamworth pigs"] >= 14)]
print("number passed April 2018 filters:", len(accepted_April2018)) 
# May 2018
accepted_May2018 = accepted_April2018[(accepted_April2018["Time"] == 160) &
(accepted_April2018["Exmoor pony"] <= 10) & (accepted_April2018["Exmoor pony"] >= 8) &
(accepted_April2018["Longhorn cattle"] <= 129) & (accepted_April2018["Longhorn cattle"] >= 105) &
(accepted_April2018["Tamworth pigs"] <= 25) & (accepted_April2018["Tamworth pigs"] >= 21)]
print("number passed May 2018 filters:", len(accepted_May2018)) 
# June 2018
accepted_June2018 = accepted_May2018[(accepted_May2018["Time"] == 161) &
(accepted_May2018["Exmoor pony"] <= 10) & (accepted_May2018["Exmoor pony"] >= 8) &
(accepted_May2018["Longhorn cattle"] <= 113) & (accepted_May2018["Longhorn cattle"] >= 93) &
(accepted_May2018["Tamworth pigs"] <= 25) & (accepted_May2018["Tamworth pigs"] >= 21)]
print("number passed June 2018 filters:", len(accepted_June2018)) 
# July 2018
accepted_July2018 = accepted_June2018[(accepted_June2018["Time"] == 162) &
(accepted_June2018["Exmoor pony"] <= 10) & (accepted_June2018["Exmoor pony"] >= 8) &
(accepted_June2018["Longhorn cattle"] <= 113) & (accepted_June2018["Longhorn cattle"] >= 93) &
(accepted_June2018["Tamworth pigs"] <= 24) & (accepted_June2018["Tamworth pigs"] >= 20)]
print("number passed July 2018 filters:", len(accepted_July2018)) 
# Aug 2018
accepted_Aug2018 = accepted_July2018[(accepted_July2018["Time"] == 163) &
(accepted_July2018["Longhorn cattle"] <= 112) & (accepted_July2018["Longhorn cattle"] >= 92) &
(accepted_July2018["Tamworth pigs"] <= 24) & (accepted_July2018["Tamworth pigs"] >= 20)]
print("number passed Aug 2018 filters:", len(accepted_Aug2018)) 
# Sept 2018
accepted_Sept2018 = accepted_Aug2018[(accepted_Aug2018["Time"] == 164) &
(accepted_Aug2018["Longhorn cattle"] <= 117) & (accepted_Aug2018["Longhorn cattle"] >= 95) &
(accepted_Aug2018["Tamworth pigs"] <= 24) & (accepted_Aug2018["Tamworth pigs"] >= 20)]
print("number passed Sept 2018 filters:", len(accepted_Sept2018)) 
# Oct 2018
accepted_Oct2018 = accepted_Sept2018[(accepted_Sept2018["Time"] == 165) &
(accepted_Sept2018["Longhorn cattle"] <= 111) & (accepted_Sept2018["Longhorn cattle"] >= 91) &
(accepted_Sept2018["Tamworth pigs"] <= 23) & (accepted_Sept2018["Tamworth pigs"] >= 19)]
print("number passed Oct 2018 filters:", len(accepted_Oct2018)) 
# Nov 2018
accepted_Nov2018 = accepted_Oct2018[(accepted_Oct2018["Time"] == 166) &
(accepted_Oct2018["Longhorn cattle"] <= 102) & (accepted_Oct2018["Longhorn cattle"] >= 84) &
(accepted_Oct2018["Tamworth pigs"] <= 10) & (accepted_Oct2018["Tamworth pigs"] >= 8)]
print("number passed Nov 2018 filters:", len(accepted_Nov2018)) 
# Dec 2018
accepted_Dec2018 = accepted_Nov2018[(accepted_Nov2018["Time"] == 167) &
(accepted_Nov2018["Longhorn cattle"] <= 98) & (accepted_Nov2018["Longhorn cattle"] >= 80) &
(accepted_Nov2018["Tamworth pigs"] <= 10) & (accepted_Nov2018["Tamworth pigs"] >= 8)]
print("number passed Dec 2018 filters:", len(accepted_Dec2018)) 
# Jan 2019
accepted_Jan2019 = accepted_Dec2018[(accepted_Dec2018["Time"] == 168) &
(accepted_Dec2018["Longhorn cattle"] <= 98) & (accepted_Dec2018["Longhorn cattle"] >= 80) &
(accepted_Dec2018["Tamworth pigs"] <= 10) & (accepted_Dec2018["Tamworth pigs"] >= 8)]
print("number passed Jan 2019 filters:", len(accepted_Jan2019)) 
# Feb 2019
accepted_Feb2019 = accepted_Jan2019[(accepted_Jan2019["Time"] == 169) &
(accepted_Jan2019["Longhorn cattle"] <= 96) & (accepted_Jan2019["Longhorn cattle"] >= 78) &
(accepted_Jan2019["Tamworth pigs"] <= 11) & (accepted_Jan2019["Tamworth pigs"] >= 9)]
print("number passed Feb 2019 filters:", len(accepted_Feb2019)) 
# March 2019
accepted_March2019 = accepted_June2018[(accepted_June2018["Time"] == 170) &
(accepted_June2018["Fallow deer"] <= 306) & (accepted_June2018["Fallow deer"] >= 250) &
(accepted_June2018["Longhorn cattle"] <= 96) & (accepted_June2018["Longhorn cattle"] >= 78) &
(accepted_June2018["Red deer"] <= 41) & (accepted_June2018["Red deer"] >= 33) &
(accepted_June2018["Tamworth pigs"] <= 10) & (accepted_June2018["Tamworth pigs"] >= 8)]
print("number passed March 2019 filters:", len(accepted_March2019)) 
# April 2019
accepted_April2019 = accepted_March2019[(accepted_March2019["Time"] == 171) &
(accepted_March2019["Longhorn cattle"] <= 111) & (accepted_March2019["Longhorn cattle"] >= 91) &
(accepted_March2019["Tamworth pigs"] <= 9) & (accepted_March2019["Tamworth pigs"] >= 7)]
print("number passed April 2019 filters:", len(accepted_April2019)) 
# May 2019
accepted_May2019 = accepted_April2019[(accepted_April2019["Time"] == 172) &
(accepted_April2019["Longhorn cattle"] <= 121) & (accepted_April2019["Longhorn cattle"] >= 99) &
(accepted_April2019["Tamworth pigs"] <= 9) & (accepted_April2019["Tamworth pigs"] >= 7)]
print("number passed May 2019 filters:", len(accepted_May2019))
# June 2019
accepted_June2019 = accepted_May2019[(accepted_May2019["Time"] == 173) &
(accepted_May2019["Longhorn cattle"] <= 98) & (accepted_May2019["Longhorn cattle"] >= 80) &
(accepted_May2019["Tamworth pigs"] <= 9) & (accepted_May2019["Tamworth pigs"] >= 7)]
print("number passed June 2019 filters:", len(accepted_June2019)) 
# July 2019
accepted_July2019 = accepted_June2019[(accepted_June2019["Time"] == 174) &
(accepted_June2019["Longhorn cattle"] <= 100) & (accepted_June2019["Longhorn cattle"] >= 82) &
(accepted_June2019["Tamworth pigs"] <= 10) & (accepted_June2019["Tamworth pigs"] >= 8)]
print("number passed July 2019 filters:", len(accepted_July2019)) 
# Aug 2019
accepted_Aug2019 = accepted_July2019[(accepted_July2019["Time"] == 175) &
(accepted_July2019["Longhorn cattle"] <= 100) & (accepted_July2019["Longhorn cattle"] >= 82) &
(accepted_July2019["Tamworth pigs"] <= 10) & (accepted_July2019["Tamworth pigs"] >= 8)]
print("number passed Aug 2019 filters:", len(accepted_Aug2019)) 
# Sept 2019
accepted_Sept2019 = accepted_Aug2019[(accepted_Aug2019["Time"] == 176) &
(accepted_Aug2019["Longhorn cattle"] <= 102) & (accepted_Aug2019["Longhorn cattle"] >= 84) &
(accepted_Aug2019["Tamworth pigs"] <= 10) & (accepted_Aug2019["Tamworth pigs"] >= 8)]
print("number passed Sept 2019 filters:", len(accepted_Sept2019)) 
# Oct 2019
accepted_Oct2019 = accepted_Sept2019[(accepted_Sept2019["Time"] == 177) &
(accepted_Sept2019["Longhorn cattle"] <= 97) & (accepted_Sept2019["Longhorn cattle"] >= 79) &
(accepted_Sept2019["Tamworth pigs"] <= 10) & (accepted_Sept2019["Tamworth pigs"] >= 8)]
print("number passed Oct 2019 filters:", len(accepted_Oct2019)) 
# Nov 2019
accepted_Nov2019 = accepted_Oct2019[(accepted_Oct2019["Time"] == 178) &
(accepted_Oct2019["Longhorn cattle"] <= 96) & (accepted_Oct2019["Longhorn cattle"] >= 78) &
(accepted_Oct2019["Tamworth pigs"] <= 10) & (accepted_Oct2019["Tamworth pigs"] >= 8)]
print("number passed Nov 2019 filters:", len(accepted_Nov2019)) 
# Dec 2019
accepted_Dec2019 = accepted_Oct2019[(accepted_Oct2019["Time"] == 179) &
(accepted_Oct2019["Longhorn cattle"] <= 88) & (accepted_Oct2019["Longhorn cattle"] >= 72) &
(accepted_Oct2019["Tamworth pigs"] <= 11) & (accepted_Oct2019["Tamworth pigs"] >= 9)]
print("number passed Dec 2019 filters:", len(accepted_Dec2019))
# Jan 2020
accepted_Jan2020 = accepted_Dec2019[(accepted_Dec2019["Time"] == 180) &
(accepted_Dec2019["Longhorn cattle"] <= 88) & (accepted_Dec2019["Longhorn cattle"] >= 72) &
(accepted_Dec2019["Tamworth pigs"] <= 11) & (accepted_Dec2019["Tamworth pigs"] >= 9)]
print("number passed Jan 2020 filters:", len(accepted_Jan2020))
# Feb 2020
accepted_Feb2020 = accepted_Jan2020[(accepted_Jan2020["Time"] == 181) &
(accepted_Jan2020["Longhorn cattle"] <= 87) & (accepted_Jan2020["Longhorn cattle"] >= 71) &
(accepted_Jan2020["Tamworth pigs"] <= 9) & (accepted_Jan2020["Tamworth pigs"] >= 7)]
print("number passed Feb 2020 filters:", len(accepted_Feb2020))
# March 2020
accepted_March2020 = accepted_Feb2020[(accepted_Feb2020["Time"] == 182) &
(accepted_Feb2020["Fallow deer"] <= 272) & (accepted_Feb2020["Fallow deer"] >= 222) &
(accepted_Feb2020["Red deer"] <= 39) & (accepted_Feb2020["Red deer"] >= 32) &
(accepted_Feb2020["Longhorn cattle"] <= 89) & (accepted_Feb2020["Longhorn cattle"] >= 73) &
(accepted_Feb2020["Tamworth pigs"] <= 8) & (accepted_Feb2020["Tamworth pigs"] >= 6)]
print("number passed March 2020 filters:", len(accepted_March2020)) 
# April 2020
accepted_April2020 = accepted_March2020[(accepted_March2020["Time"] == 183) &
(accepted_March2020["Exmoor pony"] <= 17) & (accepted_March2020["Exmoor pony"] >= 14) &
(accepted_March2020["Longhorn cattle"] <= 89) & (accepted_March2020["Longhorn cattle"] >= 73) &
(accepted_March2020["Tamworth pigs"] <= 8) & (accepted_March2020["Tamworth pigs"] >= 6)]
print("number passed April 2020 filters:", len(accepted_April2020)) 
    
# May 2020
all_accepted_runs = accepted_April2020[(accepted_April2020["Time"] == 184) &
(accepted_April2020["Tamworth pigs"] <= 21) & (accepted_April2020["Tamworth pigs"] >= 17) &
(accepted_April2020["Exmoor pony"] <= 17) & (accepted_April2020["Exmoor pony"] >= 14) &
(accepted_April2020["Longhorn cattle"] <= 89) & (accepted_April2020["Longhorn cattle"] >= 73) &
(accepted_April2020["Roe deer"] <= 40) & (accepted_April2020["Roe deer"] >= 20) &
(accepted_April2020["Grassland"] <= 69) & (accepted_April2020["Grassland"] >= 49) &
(accepted_April2020["Thorny Scrub"] <= 35) & (accepted_April2020["Thorny Scrub"] >= 21) &
(accepted_April2020["Woodland"] <= 29) & (accepted_April2020["Woodland"] >= 9)]
print("number passed all filters:", len(all_accepted_runs))

# accepted parameters
accepted_parameters = final_parameters[final_parameters['run_number'].isin(all_accepted_runs['run_number'])]
# tag the accepted simulations
final_results['accepted?'] = np.where(final_results['run_number'].isin(accepted_parameters['run_number']), 'Accepted', 'Rejected')

with pd.option_context('display.max_columns',None):
    print(final_results[(final_results["Time"] == 184)])

with pd.option_context('display.max_rows',None, 'display.max_columns',None):
    print("accepted_years: \n", all_accepted_runs)

# save to excel sheet
final_parameters.to_excel("parameters.xlsx")
