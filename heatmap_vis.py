# ------ ABM of the Knepp Estate (2005-2046) --------
from KneppModel_ABM import KneppModel 
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# # # # Run the model # # # # 

# define the parameters
chance_reproduceSapling = 0.10453203
chance_reproduceYoungScrub = 0.23984245
chance_regrowGrass = 0.30678081
chance_saplingBecomingTree = 0.00280897
chance_youngScrubMatures = 0.00586312
chance_scrubOutcompetedByTree = 0.02446419
chance_grassOutcompetedByTree = 0.9462915
chance_grassOutcompetedByScrub = 0.9426664
chance_saplingOutcompetedByTree = 0.92489406
chance_saplingOutcompetedByScrub =0.89946235
chance_youngScrubOutcompetedByScrub = 0.92686055
chance_youngScrubOutcompetedByTree = 0.94425658

# initial values
initial_roeDeer = 0.12
initial_grassland = 0.8
initial_woodland = 0.14
initial_scrubland = 0.01

# roe deer
roeDeer_reproduce = 0.1820612
roeDeer_gain_from_grass = 0.87653423
roeDeer_gain_from_Trees = 0.56002015
roeDeer_gain_from_Scrub = 0.31700781
roeDeer_gain_from_Saplings = 0.17359909
roeDeer_gain_from_YoungScrub = 0.10501903
# Fallow deer
fallowDeer_reproduce = 0.28999103
fallowDeer_gain_from_grass = 0.80584063
fallowDeer_gain_from_Trees = 0.54393178
fallowDeer_gain_from_Scrub = 0.28713036
fallowDeer_gain_from_Saplings = 0.10079212
fallowDeer_gain_from_YoungScrub = 0.07335673
# Red deer
redDeer_reproduce = 0.31560646
redDeer_gain_from_grass = 0.76444708
redDeer_gain_from_Trees = 0.45464787
redDeer_gain_from_Scrub = 0.22482635
redDeer_gain_from_Saplings = 0.08840829
redDeer_gain_from_YoungScrub = 0.06817436
# Exmoor ponies
ponies_gain_from_grass = 0.72915031
ponies_gain_from_Trees = 0.4142464
ponies_gain_from_Scrub = 0.16508224
ponies_gain_from_Saplings = 0.07216459
ponies_gain_from_YoungScrub = 0.05341865
# Longhorn cattle
cows_reproduce = 0.21197986
cows_gain_from_grass = 0.68746036
cows_gain_from_Trees = 0.33225956
cows_gain_from_Scrub = 0.11829169
cows_gain_from_Saplings = 0.06269837
cows_gain_from_YoungScrub = 0.03042194
# Tamworth pigs
pigs_reproduce = 0.24808032
pigs_gain_from_grass = 0.60543958
pigs_gain_from_Trees = 0.525367
pigs_gain_from_Scrub = 0.16852274
pigs_gain_from_Saplings = 0.16226507
pigs_gain_from_YoungScrub = 0.05785037
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
    width = 25, height = 18, max_time = 10, reintroduction = True,
    introduce_euroBison = True, introduce_elk = False, introduce_reindeer = False)

model.run_model()

# remember the results of the model (dominant conditions, # of agents)
results2 = model.datacollector.get_agent_vars_dataframe()

# put it into an excel sheet
results2.to_excel("heatmap_all_ecosystem_elements_10.xlsx")
# results2 =  pd.read_excel('heatmap_all_ecosystem_elements.xlsx')

#ggplot 
# emily %>% mutate(X=as.integer(X),Y=as.integer(Y)) %>% group_by(Breed,X,Y) %>%
#   summarise(n=n()) %>%
#   ggplot() +
#   geom_tile(aes(x=X,y=Y,fill=n))  +
#   facet_wrap(Breed~.)

g = sns.FacetGrid(results2,  col="Breed", col_wrap=4, sharey = True)
g.map(
    sns.histplot,'X', 'Y', 
    bins = [np.arange(0,26,1),np.arange(0,19,1)], 
    thresh=None,
    cbar=True,
    cbar_kws=dict(shrink=.75),
    )

g.fig.suptitle('Locations of ecosystem elements')
g.set_titles('{col_name}')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/locations/facetGrid.png')
plt.show()

results2 = pd.read_excel('heatmap_all_ecosystem_elements.xlsx')


# now track 3 individuals for each species (ones that survive at least 10yrs): roe and habitat 
three_species = results2.loc[(results2["AgentID"] <= 450) | 
# roe deer
(results2["AgentID"] == 465) |
# fallow deer
(results2["AgentID"] == 598) |
# red deer
(results2["AgentID"] == 865) |
# exmoor pony
(results2["AgentID"] == 470) |
# longhorn cattle
(results2["AgentID"] == 498) |
# tamworth pig
(results2["AgentID"] == 564)]

g = sns.FacetGrid(three_species,  col="Breed", col_wrap = 4, sharey = False)
g.map(
    sns.histplot,'X', 'Y', 
    bins = [np.arange(0,25,1),np.arange(0,18,1)], 
    thresh=None,
    cbar=True,
    cbar_kws=dict(shrink=.75),
    )

g.fig.suptitle('Locations of ecosystem elements: one individual per consumer')
g.set_titles('{col_name}')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/locations/facetGrid.png')
plt.show()





# # # # # Experiment 1: What if there's no food? # # # # 

# # define the parameters
# chance_reproduceSapling = 0.10453203
# chance_reproduceYoungScrub = 0.23984245
# chance_regrowGrass = 0.30678081
# chance_saplingBecomingTree = 0.00280897
# chance_youngScrubMatures = 0.00586312
# chance_scrubOutcompetedByTree = 0.02446419
# chance_grassOutcompetedByTree = 0.9462915
# chance_grassOutcompetedByScrub = 0.9426664
# chance_saplingOutcompetedByTree = 0.92489406
# chance_saplingOutcompetedByScrub =0.89946235
# chance_youngScrubOutcompetedByScrub = 0.92686055
# chance_youngScrubOutcompetedByTree = 0.94425658

# # initial values
# initial_roeDeer = 0.12
# initial_grassland = 0.01
# initial_woodland = 0.01
# initial_scrubland = 0.01

# # roe deer
# roeDeer_reproduce = 0.1820612
# roeDeer_gain_from_grass = 0.87653423
# roeDeer_gain_from_Trees = 0.56002015
# roeDeer_gain_from_Scrub = 0.31700781
# roeDeer_gain_from_Saplings = 0.17359909
# roeDeer_gain_from_YoungScrub = 0.10501903
# # Fallow deer
# fallowDeer_reproduce = 0.28999103
# fallowDeer_gain_from_grass = 0.80584063
# fallowDeer_gain_from_Trees = 0.54393178
# fallowDeer_gain_from_Scrub = 0.28713036
# fallowDeer_gain_from_Saplings = 0.10079212
# fallowDeer_gain_from_YoungScrub = 0.07335673
# # Red deer
# redDeer_reproduce = 0.31560646
# redDeer_gain_from_grass = 0.76444708
# redDeer_gain_from_Trees = 0.45464787
# redDeer_gain_from_Scrub = 0.22482635
# redDeer_gain_from_Saplings = 0.08840829
# redDeer_gain_from_YoungScrub = 0.06817436
# # Exmoor ponies
# ponies_gain_from_grass = 0.72915031
# ponies_gain_from_Trees = 0.4142464
# ponies_gain_from_Scrub = 0.16508224
# ponies_gain_from_Saplings = 0.07216459
# ponies_gain_from_YoungScrub = 0.05341865
# # Longhorn cattle
# cows_reproduce = 0.21197986
# cows_gain_from_grass = 0.68746036
# cows_gain_from_Trees = 0.33225956
# cows_gain_from_Scrub = 0.11829169
# cows_gain_from_Saplings = 0.06269837
# cows_gain_from_YoungScrub = 0.03042194
# # Tamworth pigs
# pigs_reproduce = 0.24808032
# pigs_gain_from_grass = 0.60543958
# pigs_gain_from_Trees = 0.525367
# pigs_gain_from_Scrub = 0.16852274
# pigs_gain_from_Saplings = 0.16226507
# pigs_gain_from_YoungScrub = 0.05785037
# # # stocking values
# fallowDeer_stocking = 247
# cattle_stocking = 81
# redDeer_stocking = 35
# tamworthPig_stocking = 7
# exmoor_stocking = 15
# # # euro bison parameters
# reproduce_bison = 0
# # bison should have higher impact than any other consumer
# bison_gain_from_grass =  0
# bison_gain_from_Trees =0
# bison_gain_from_Scrub =0
# bison_gain_from_Saplings = 0
# bison_gain_from_YoungScrub = 0  
# # euro elk parameters
# reproduce_elk = 0
# # bison should have higher impact than any other consumer
# elk_gain_from_grass =  0
# elk_gain_from_Trees = 0
# elk_gain_from_Scrub = 0
# elk_gain_from_Saplings =  0
# elk_gain_from_YoungScrub =  0
# # reindeer parameters
# reproduce_reindeer = 0
# # reindeer should have impacts between red and fallow deer
# reindeer_gain_from_grass = 0
# reindeer_gain_from_Trees =0
# reindeer_gain_from_Scrub =0
# reindeer_gain_from_Saplings = 0
# reindeer_gain_from_YoungScrub = 0


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
#     fallowDeer_stocking, cattle_stocking, redDeer_stocking, tamworthPig_stocking, exmoor_stocking,
#     reproduce_bison, bison_gain_from_grass, bison_gain_from_Trees, bison_gain_from_Scrub, bison_gain_from_Saplings, bison_gain_from_YoungScrub,
#     reproduce_elk, elk_gain_from_grass, elk_gain_from_Trees, elk_gain_from_Scrub, elk_gain_from_Saplings, elk_gain_from_YoungScrub,
#     reproduce_reindeer, reindeer_gain_from_grass, reindeer_gain_from_Trees, reindeer_gain_from_Scrub, reindeer_gain_from_Saplings, reindeer_gain_from_YoungScrub,
#     width = 25, height = 18, max_time = 184, reintroduction = True,
#     introduce_euroBison = True, introduce_elk = False, introduce_reindeer = False)

# # model.run_model()

# # # remember the results of the model (dominant conditions, # of agents)
# # results2 = model.datacollector.get_agent_vars_dataframe()

# # # # put it into an excel sheet
# # results2.to_excel("heatmap_single_exp1.xlsx")

# results2 = pd.read_excel('heatmap_single_exp1.xlsx')

# # now track 3 individuals for each species (ones that survive at least 10yrs): roe and habitat 
# three_species = results2.loc[(results2["AgentID"] <= 450) | 
# # roe deer
# (results2["AgentID"] == 464) |
# # fallow deer
# (results2["AgentID"] == 546) |
# # red deer
# (results2["AgentID"] == 966) |
# # exmoor pony
# (results2["AgentID"] == 493) |
# # longhorn cattle
# (results2["AgentID"] == 551) |
# # tamworth pig
# (results2["AgentID"] == 575)]

# g = sns.FacetGrid(three_species,  col="Breed", col_wrap = 4)
# g.map(
#     sns.histplot,'X', 'Y', 
#     bins = [np.arange(0,25,1),np.arange(0,18,1)], 
#     thresh=None,
#     cbar=True,
#     cbar_kws=dict(shrink=.75),
#     )

# g.fig.suptitle('Individual consumer behaviour with low amounts of food')
# g.set_titles('{col_name}')
# plt.tight_layout()
# plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/locations/facetGrid.png')
# plt.show()