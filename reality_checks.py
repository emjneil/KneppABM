# ------ Optimization of the Knepp ABM model --------
from KneppModel_ABM import KneppModel 
import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution
import seaborn as sns
import matplotlib.pyplot as plt
import sys



chance_reproduceSapling = 0.10689392
chance_reproduceYoungScrub = 0.24015217
chance_regrowGrass = 0.30423892
chance_saplingBecomingTree = 0.00284643
chance_youngScrubMatures = 0.00573939
chance_scrubOutcompetedByTree = 0.02412406
chance_grassOutcompetedByTree = 0.94724942
chance_grassOutcompetedByScrub = 0.94365962
chance_saplingOutcompetedByTree = 0.90002424
chance_saplingOutcompetedByScrub = 0.89430521
chance_youngScrubOutcompetedByScrub = 0.90509186
chance_youngScrubOutcompetedByTree = 0.94722833

# initial values
initial_roeDeer = 0.12
initial_grassland = 0.8
initial_woodland = 0.14
initial_scrubland = 0.01

# roe deer
roeDeer_reproduce = 0.18203732
roeDeer_gain_from_grass = 0.85140101
roeDeer_gain_from_Trees = 0.55494915
roeDeer_gain_from_Scrub = 0.3150886
roeDeer_gain_from_Saplings = 0.17500993
roeDeer_gain_from_YoungScrub = 0.10840577
# Fallow deer
fallowDeer_reproduce = 0.28541271
fallowDeer_gain_from_grass = 0.79704305
fallowDeer_gain_from_Trees = 0.53392473
fallowDeer_gain_from_Scrub = 0.24861395
fallowDeer_gain_from_Saplings = 0.1184058
fallowDeer_gain_from_YoungScrub = 0.07327595
# Red deer
redDeer_reproduce = 0.30656575
redDeer_gain_from_grass = 0.74254951
redDeer_gain_from_Trees = 0.44633234
redDeer_gain_from_Scrub = 0.18817947
redDeer_gain_from_Saplings = 0.07572942
redDeer_gain_from_YoungScrub = 0.06516447
# Exmoor ponies
ponies_gain_from_grass = 0.6766493
ponies_gain_from_Trees = 0.29251235
ponies_gain_from_Scrub = 0.14860288
ponies_gain_from_Saplings = 0.07
ponies_gain_from_YoungScrub = 0.03731702
# Longhorn cattle
cows_reproduce = 0.18684058
cows_gain_from_grass = 0.60323306
cows_gain_from_Trees = 0.21599744
cows_gain_from_Scrub = 0.09316363
cows_gain_from_Saplings = 0.06101444
cows_gain_from_YoungScrub = 0.01609566
# Tamworth pigs
pigs_reproduce = 0.24870944
pigs_gain_from_grass = 0.59825361
pigs_gain_from_Trees = 0.2569851
pigs_gain_from_Scrub = 0.1637277
pigs_gain_from_Saplings = 0.14782646
pigs_gain_from_YoungScrub = 0.09885063



# # 1. Do herbivores die in the absence of food? 
# no_grassland = 0
# no_woodland = 0
# no_scrubland = 0
# no_regrowing_grass = 0

# model = KneppModel(
#     chance_reproduceSapling, chance_reproduceYoungScrub, no_regrowing_grass, chance_saplingBecomingTree, chance_youngScrubMatures, 
#     chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
#     initial_roeDeer, no_grassland, no_woodland, no_scrubland, 
#     roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
#     ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
#     cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
#     fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
#     redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
#     pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Trees, pigs_gain_from_Scrub, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
#     width = 25, height = 18, max_time = 184, reintroduction = True, 
#     RC1_noFood = True, RC2_noTreesScrub = True, RC3_noTrees = True, RC4_noScrub = True)
# model.run_model()

# results_reality1 = model.datacollector.get_model_vars_dataframe()
# # y values
# y_values_reality1 = results_reality1[["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"]].values.flatten()
# # y_values_reality1 = results_reality1.drop(['Time'], axis=1).values.flatten()
# species_list = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 185) 
# indices = np.repeat(results_reality1['Time'], 10)
# colors = ["#6788ee", "#e26952", "#3F9E4D"]

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



# If herbivores are overloaded into the system, grassland and bare ground should take over.
# roeDeer_gain_from_grass = 10
# roeDeer_reproduce = 2
# cows_gain_from_grass = 10
# cows_reproduce = 2
# fallowDeer_gain_from_grass = 10
# fallowDeer_reproduce = 2
# redDeer_gain_from_grass = 10
# redDeer_reproduce = 2
# pigs_gain_from_grass = 10
# pigs_reproduce = 2

# model = KneppModel(
#     chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
#     chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
#     initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland, 
#     roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
#     ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
#     cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
#     fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
#     redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
#     pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Trees, pigs_gain_from_Scrub, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub, 
#     width = 25, height = 18, max_time = 184, reintroduction = True, 
#     RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)
# model.run_model()

# final_results = model.datacollector.get_model_vars_dataframe()

# y_values = final_results[["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"]].values.flatten()
# species_list = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 185) 
# indices = np.repeat(final_results['Time'], 10)
# colors = ["#6788ee", "#e26952", "#3F9E4D"]

# final_df = pd.DataFrame(
# {'Abundance': y_values, 'Ecosystem Element': species_list, 'Time': indices})
# colors = ["#6788ee"]
# g = sns.FacetGrid(final_df, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
# g.map(sns.lineplot, 'Time', 'Abundance')
# # add subplot titles
# axes = g.axes.flatten()
# # fill between the quantiles
# axes = g.axes.flatten()
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
# g.fig.suptitle("Reality check: Many herbivores")
# plt.tight_layout()
# plt.savefig('RealityCheck_overloadHerbivores.png')
# plt.show()

# Larger habitat types should not outcompete undergrowth too quickly; for example, it is assumed that woodland with half the maximum number of trees should still have some grass, scrub, saplings, and young scrub present.
initial_roeDeer = 0

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
    width = 25, height = 18, max_time = 184, reintroduction = False, 
    RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)
model.run_model()

# first graph:  does it pass the filters? looking at the number of individual trees, etc.
final_results = model.datacollector.get_model_vars_dataframe()

# y values - number of trees, scrub, etc. 
y_values = final_results.drop(['Time', "Bare ground","Grassland", "Woodland", "Thorny Scrub", "Saplings grown up", "Saplings Outcompeted by Trees", "Saplings Outcompeted by Scrub", "Saplings eaten by roe deer", "Saplings eaten by Exmoor pony", "Saplings eaten by Fallow deer", "Saplings eaten by longhorn cattle", "Saplings eaten by red deer",  "Saplings eaten by pigs", "Young scrub grown up", "Young Scrub Outcompeted by Trees", "Young Scrub Outcompeted by Scrub", "Young Scrub eaten by roe deer", "Young Scrub eaten by Exmoor pony", 
"Young Scrub eaten by Fallow deer", "Young Scrub eaten by longhorn cattle", "Young Scrub eaten by red deer", "Young Scrub eaten by pigs", 
"Grass Outcompeted by Trees", "Grass Outcompeted by Scrub", "Grass eaten by roe deer", "Grass eaten by Exmoor pony", "Grass eaten by Fallow deer", "Grass eaten by longhorn cattle", "Grass eaten by red deer", "Grass eaten by pigs", 
"Scrub Outcompeted by Trees", "Scrub eaten by roe deer", "Scrub eaten by Exmoor pony", "Scrub eaten by Fallow deer", "Scrub eaten by longhorn cattle", 
"Scrub eaten by red deer", "Scrub eaten by pigs", "Trees eaten by roe deer", "Trees eaten by Exmoor pony", "Trees eaten by Fallow deer", "Trees eaten by longhorn cattle",  "Trees eaten by red deer", "Trees eaten by pigs"], axis=1).values.flatten()           
species_list = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"], 185) 
indices = np.repeat(final_results['Time'], 12)
final_df = pd.DataFrame(
{'Abundance': y_values, 'Ecosystem Element': species_list, 'Time': indices})
colors = ["#6788ee"]
g = sns.FacetGrid(final_df, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
g.map(sns.lineplot, 'Time', 'Abundance')

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
g.fig.suptitle("Optimizer Outputs")
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/post_reintro/noHerbivores_numbers.png')
plt.show()