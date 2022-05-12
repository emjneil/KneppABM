# graph the runs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from KneppModel_ABM import KneppModel 
import numpy as np
import pandas as pd
from scipy.stats import linregress


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
# initial_grassland = 0.8
# initial_woodland = 0.14
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


# # keep track of my parameters
# final_parameters = [
#     chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
#     chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
#     roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
#     ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
#     cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
#     fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
#     redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
#     pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Trees, pigs_gain_from_Scrub, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub
#     ]

# variables = [
#     # habitat variables
#     "chance_reproduceSapling", # this is to initialize the initial dominant condition
#     "chance_reproduceYoungScrub",  # this is to initialize the initial dominant condition
#     "chance_regrowGrass", # this is to initialize the initial dominant condition
#     "chance_saplingBecomingTree",
#     "chance_youngScrubMatures",
#     "chance_scrubOutcompetedByTree", # if tree matures, chance of scrub decreasing
#     "chance_grassOutcompetedByTree",
#     "chance_grassOutcompetedByScrub",
#     "chance_saplingOutcompetedByTree",
#     "chance_saplingOutcompetedByScrub",
#     "chance_youngScrubOutcompetedByScrub",
#     "chance_youngScrubOutcompetedByTree",

#     # roe deer variables
#     "roeDeer_reproduce",
#     "roeDeer_gain_from_grass",
#     "roeDeer_gain_from_Trees",
#     "roeDeer_gain_from_Scrub",
#     "roeDeer_gain_from_Saplings", 
#     "roeDeer_gain_from_YoungScrub", 
#     # Exmoor pony variables
#     "ponies_gain_from_grass", 
#     "ponies_gain_from_Trees", 
#     "ponies_gain_from_Scrub", 
#     "ponies_gain_from_Saplings", 
#     "ponies_gain_from_YoungScrub", 
#     # Cow variables
#     "cows_reproduce", 
#     "cows_gain_from_grass", 
#     "cows_gain_from_Trees", 
#     "cows_gain_from_Scrub", 
#     "cows_gain_from_Saplings", 
#     "cows_gain_from_YoungScrub", 
#     # Fallow deer variables
#     "fallowDeer_reproduce", 
#     "fallowDeer_gain_from_grass", 
#     "fallowDeer_gain_from_Trees", 
#     "fallowDeer_gain_from_Scrub", 
#     "fallowDeer_gain_from_Saplings", 
#     "fallowDeer_gain_from_YoungScrub", 
#     # Red deer variables
#     "redDeer_reproduce", 
#     "redDeer_gain_from_grass", 
#     "redDeer_gain_from_Trees", 
#     "redDeer_gain_from_Scrub", 
#     "redDeer_gain_from_Saplings", 
#     "redDeer_gain_from_YoungScrub", 
#     # Pig variables
#     "pigs_reproduce", 
#     "pigs_gain_from_grass", 
#     "pigs_gain_from_Trees", 
#     "pigs_gain_from_Scrub",
#     "pigs_gain_from_Saplings", 
#     "pigs_gain_from_YoungScrub"
#     ]


# # check out the parameters used
# final_parameters = pd.DataFrame(data=[final_parameters], columns=variables)

# # SENSITIVITY TEST
# sensitivity_results_list = []
# sensitivity_parameters = []
# run_number  = 0
# # choose my percent above/below number
# perc_aboveBelow = [-0.1, -0.05,-0.01, 0, 0.01, 0.05, 0.1]
# final_parameters = final_parameters.iloc[0,0:47]
# # loop through each one, changing one cell at a time
# for index, row in final_parameters.iteritems():
#     for perc_number in perc_aboveBelow:
#         final_parameters_temp = final_parameters
#         run_number += 1
#         ifor_val = row + (row*perc_number)
#         final_parameters_temp.at[index] = ifor_val
#         print(run_number)
#         # choose my parameters 
#         chance_reproduceSapling = final_parameters_temp.values[0]
#         chance_reproduceYoungScrub = final_parameters_temp.values[1]
#         chance_regrowGrass = final_parameters_temp.values[2]
#         chance_saplingBecomingTree = final_parameters_temp.values[3]
#         chance_youngScrubMatures = final_parameters_temp.values[4]
#         chance_scrubOutcompetedByTree = final_parameters_temp.values[5]
#         chance_grassOutcompetedByTree = final_parameters_temp.values[6]
#         chance_grassOutcompetedByScrub = final_parameters_temp.values[7]
#         chance_saplingOutcompetedByTree = final_parameters_temp.values[8]
#         chance_saplingOutcompetedByScrub = final_parameters_temp.values[9]
#         chance_youngScrubOutcompetedByScrub = final_parameters_temp.values[10]
#         chance_youngScrubOutcompetedByTree = final_parameters_temp.values[11]
#         initial_roeDeer = 0.12
#         initial_grassland = 0.8
#         initial_woodland = 0.14
#         initial_scrubland = 0.01
#         roeDeer_reproduce = final_parameters_temp.values[12]
#         roeDeer_gain_from_grass = final_parameters_temp.values[13]
#         roeDeer_gain_from_Trees = final_parameters_temp.values[14]
#         roeDeer_gain_from_Scrub = final_parameters_temp.values[15]
#         roeDeer_gain_from_Saplings = final_parameters_temp.values[16]
#         roeDeer_gain_from_YoungScrub = final_parameters_temp.values[17]
#         ponies_gain_from_grass = final_parameters_temp.values[18]
#         ponies_gain_from_Trees = final_parameters_temp.values[19]
#         ponies_gain_from_Scrub = final_parameters_temp.values[20]
#         ponies_gain_from_Saplings = final_parameters_temp.values[21]
#         ponies_gain_from_YoungScrub = final_parameters_temp.values[22]
#         cows_reproduce = final_parameters_temp.values[23]
#         cows_gain_from_grass = final_parameters_temp.values[24]
#         cows_gain_from_Trees = final_parameters_temp.values[25]
#         cows_gain_from_Scrub = final_parameters_temp.values[26]
#         cows_gain_from_Saplings = final_parameters_temp.values[27]
#         cows_gain_from_YoungScrub = final_parameters_temp.values[28]
#         fallowDeer_reproduce = final_parameters_temp.values[29]
#         fallowDeer_gain_from_grass = final_parameters_temp.values[30]
#         fallowDeer_gain_from_Trees = final_parameters_temp.values[31]
#         fallowDeer_gain_from_Scrub = final_parameters_temp.values[32]
#         fallowDeer_gain_from_Saplings = final_parameters_temp.values[33]
#         fallowDeer_gain_from_YoungScrub = final_parameters_temp.values[34]
#         redDeer_reproduce = final_parameters_temp.values[35]
#         redDeer_gain_from_grass = final_parameters_temp.values[36]
#         redDeer_gain_from_Trees = final_parameters_temp.values[37]
#         redDeer_gain_from_Scrub = final_parameters_temp.values[38]
#         redDeer_gain_from_Saplings = final_parameters_temp.values[39]
#         redDeer_gain_from_YoungScrub = final_parameters_temp.values[40]
#         pigs_reproduce = final_parameters_temp.values[41]
#         pigs_gain_from_grass = final_parameters_temp.values[42]
#         pigs_gain_from_Trees = final_parameters_temp.values[43]
#         pigs_gain_from_Scrub = final_parameters_temp.values[44]
#         pigs_gain_from_Saplings = final_parameters_temp.values[45]
#         pigs_gain_from_YoungScrub = final_parameters_temp.values[46]
#         # # stocking values
#         fallowDeer_stocking = 247
#         cattle_stocking = 81
#         redDeer_stocking = 35
#         tamworthPig_stocking = 7
#         exmoor_stocking = 15
#         # # euro bison parameters
#         reproduce_bison = 0
#         # bison should have higher impact than any other consumer
#         bison_gain_from_grass =  0
#         bison_gain_from_Trees =0
#         bison_gain_from_Scrub =0
#         bison_gain_from_Saplings = 0
#         bison_gain_from_YoungScrub = 0  
#         # euro elk parameters
#         reproduce_elk = 0
#         # bison should have higher impact than any other consumer
#         elk_gain_from_grass =  0
#         elk_gain_from_Trees = 0
#         elk_gain_from_Scrub = 0
#         elk_gain_from_Saplings =  0
#         elk_gain_from_YoungScrub =  0
#         # reindeer parameters
#         reproduce_reindeer = 0
#         # reindeer should have impacts between red and fallow deer
#         reindeer_gain_from_grass = 0
#         reindeer_gain_from_Trees =0
#         reindeer_gain_from_Scrub =0
#         reindeer_gain_from_Saplings = 0
#         reindeer_gain_from_YoungScrub = 0
#         # run model
#         model = KneppModel(
#             chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures,
#             chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
#             initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland,
#             roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
#             ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub,
#             cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub,
#             fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub,
#             redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub,
#             pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Trees, pigs_gain_from_Scrub, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub,
#             fallowDeer_stocking, cattle_stocking, redDeer_stocking, tamworthPig_stocking, exmoor_stocking,
#             reproduce_bison, bison_gain_from_grass, bison_gain_from_Trees, bison_gain_from_Scrub, bison_gain_from_Saplings, bison_gain_from_YoungScrub,
#             reproduce_elk, elk_gain_from_grass, elk_gain_from_Trees, elk_gain_from_Scrub, elk_gain_from_Saplings, elk_gain_from_YoungScrub,
#             reproduce_reindeer, reindeer_gain_from_grass, reindeer_gain_from_Trees, reindeer_gain_from_Scrub, reindeer_gain_from_Saplings, reindeer_gain_from_YoungScrub,
#             width = 25, height = 18, max_time = 184, reintroduction = True,
#             introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)
#         model.run_model()

#         # remember the results of the model (dominant conditions, # of agents)
#         sensitivity_results_unfiltered = model.datacollector.get_model_vars_dataframe()
#         sensitivity_results = sensitivity_results_unfiltered[(sensitivity_results_unfiltered["Time"] == 184)]
#         sensitivity_results_list.append(sensitivity_results)
#         # and the parameter changed
#         sensitivity_parameters.append([index, final_parameters_temp.at[index]])

# # append to dataframe
# final_sensitivity_results = pd.concat(sensitivity_results_list)
# final_sensitivity_parameters = pd.DataFrame(sensitivity_parameters)
# final_sensitivity_parameters.columns = ['Parameter_Changes', 'Parameter_Value']
# final_sensitivity_results = final_sensitivity_results.reset_index(drop=True)
# merged_dfs = pd.concat([final_sensitivity_parameters, final_sensitivity_results], axis=1)
# merged_dfs = merged_dfs.drop('Time', 1)
# merged_dfs.to_excel("/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/all_parameter_changes.xlsx")


merged_dfs =  pd.read_excel('/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/all_parameter_changes.xlsx')

# group them by variable name
grouped_dfs = merged_dfs.groupby("Parameter_Changes")

# ROE DEER
roe_gradients = []
# find the gradient
for grouped_name, grouped_data in grouped_dfs:
    res = linregress(grouped_data["Parameter_Value"], grouped_data["Roe deer"])
    roe_gradient = [grouped_name, res.slope]
    roe_gradients.append(roe_gradient)
roe_gradients = pd.DataFrame(roe_gradients)
roe_gradients.columns = ['Parameter_names', 'Gradient']
# take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
roe_gradients['Gradient'] = roe_gradients['Gradient'].abs()
roe_gradients = roe_gradients.sort_values(['Gradient'], ascending=[False])
top_ten = roe_gradients.iloc[0:10,:]
top_ten.to_excel("/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/final_df_gradients_roeDeer.xlsx")
# plot those
top_ten_roe = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
sns.set(font_scale=1.5)
ro = sns.relplot(data=top_ten_roe, x='Parameter_Value', y='Roe deer', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
ro.fig.suptitle('Roe deer gradients')
ro.set_titles('{col_name}')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/sensitivity_roe.png')
plt.show()



# # FALLOW DEER
fallow_gradients = []
# find the gradient
for grouped_name, grouped_data in grouped_dfs:
    res = linregress(grouped_data["Parameter_Value"], grouped_data["Fallow deer"])
    fallow_gradient = [grouped_name, res.slope]
    fallow_gradients.append(fallow_gradient)
fallow_gradients = pd.DataFrame(fallow_gradients)
fallow_gradients.columns = ['Parameter_names', 'Gradient']
# take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
fallow_gradients['Gradient'] = fallow_gradients['Gradient'].abs()
fallow_gradients = fallow_gradients.sort_values(['Gradient'], ascending=[False])
top_ten = fallow_gradients.iloc[0:10,:]
top_ten.to_excel("/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/final_df_gradients_fallowDeer.xlsx")
# plot those
top_ten_fallow = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
ro = sns.relplot(data=top_ten_fallow, x='Parameter_Value', y='Fallow deer', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
ro.fig.suptitle('Fallow deer gradients')
ro.set_titles('{col_name}')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/sensitivity_fallow.png')
plt.show()

# # RED DEER
red_gradients = []
# find the gradient
for grouped_name, grouped_data in grouped_dfs:
    res = linregress(grouped_data["Parameter_Value"], grouped_data["Red deer"])
    red_gradient = [grouped_name, res.slope]
    red_gradients.append(red_gradient)
red_gradients = pd.DataFrame(red_gradients)
red_gradients.columns = ['Parameter_names', 'Gradient']
# take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
red_gradients['Gradient'] = red_gradients['Gradient'].abs()
red_gradients = red_gradients.sort_values(['Gradient'], ascending=[False])
top_ten = red_gradients.iloc[0:10,:]
top_ten.to_excel("/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/final_df_gradients_redDeer.xlsx")
# plot those
top_ten_red = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
ro = sns.relplot(data=top_ten_roe, x='Parameter_Value', y='Red deer', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
ro.fig.suptitle('Red deer gradients')
ro.set_titles('{col_name}')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/sensitivity_red.png')
plt.show()



# # LONGHORN CATTLE
cattle_gradients = []
# find the gradient
for grouped_name, grouped_data in grouped_dfs:
    res = linregress(grouped_data["Parameter_Value"], grouped_data["Longhorn cattle"])
    cattle_gradient = [grouped_name, res.slope]
    cattle_gradients.append(cattle_gradient)
cattle_gradients = pd.DataFrame(cattle_gradients)
cattle_gradients.columns = ['Parameter_names', 'Gradient']
# take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
cattle_gradients['Gradient'] = cattle_gradients['Gradient'].abs()
cattle_gradients = cattle_gradients.sort_values(['Gradient'], ascending=[False])
top_ten = cattle_gradients.iloc[0:10,:]
top_ten.to_excel("/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/final_df_gradients_cattle.xlsx")
# plot those
top_ten_cattle = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
ro = sns.relplot(data=top_ten_cattle, x='Parameter_Value', y='Longhorn cattle', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
ro.fig.suptitle('Cattle gradients')
ro.set_titles('{col_name}')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/sensitivity_cattle.png')
plt.show()


# # TAMWORTH PIG
pig_gradients = []
# find the gradient
for grouped_name, grouped_data in grouped_dfs:
    res = linregress(grouped_data["Parameter_Value"], grouped_data["Tamworth pigs"])
    pig_gradient = [grouped_name, res.slope]
    pig_gradients.append(pig_gradient)
pig_gradients = pd.DataFrame(pig_gradients)
pig_gradients.columns = ['Parameter_names', 'Gradient']
# take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
pig_gradients['Gradient'] = pig_gradients['Gradient'].abs()
pig_gradients = pig_gradients.sort_values(['Gradient'], ascending=[False])
top_ten = pig_gradients.iloc[0:10,:]
top_ten.to_excel("/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/final_df_gradients_pig.xlsx")
# plot those
top_ten_pig = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
ro = sns.relplot(data=top_ten_pig, x='Parameter_Value', y='Tamworth pigs', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
ro.fig.suptitle('Tamworth pig gradients')
ro.set_titles('{col_name}')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/sensitivity_pig.png')
plt.show()

# # EXMOOR PONY
pony_gradients = []
# find the gradient
for grouped_name, grouped_data in grouped_dfs:
    res = linregress(grouped_data["Parameter_Value"], grouped_data["Exmoor pony"])
    pony_gradient = [grouped_name, res.slope]
    pony_gradients.append(pony_gradient)
pony_gradients = pd.DataFrame(pony_gradients)
pony_gradients.columns = ['Parameter_names', 'Gradient']
# take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
pony_gradients['Gradient'] = pony_gradients['Gradient'].abs()
pony_gradients = pony_gradients.sort_values(['Gradient'], ascending=[False])
top_ten = pony_gradients.iloc[0:10,:]
top_ten.to_excel("/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/final_df_gradients_pony.xlsx")
# plot those
top_ten_pony = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
ro = sns.relplot(data=top_ten_pony, x='Parameter_Value', y='Exmoor pony', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
ro.fig.suptitle('Exmoor pony gradients')
ro.set_titles('{col_name}')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/sensitivity_pony.png')
plt.show()



# # GRASSLAND
grass_gradients = []
# find the gradient
for grouped_name, grouped_data in grouped_dfs:
    res = linregress(grouped_data["Parameter_Value"], grouped_data["Grassland"])
    grass_gradient = [grouped_name, res.slope]
    grass_gradients.append(grass_gradient)
grass_gradients = pd.DataFrame(grass_gradients)
grass_gradients.columns = ['Parameter_names', 'Gradient']
# take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
grass_gradients['Gradient'] = grass_gradients['Gradient'].abs()
grass_gradients = grass_gradients.sort_values(['Gradient'], ascending=[False])
top_ten = grass_gradients.iloc[0:10,:]
top_ten.to_excel("/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/final_df_gradients_grass.xlsx")
# plot those
top_ten_grass = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
ro = sns.relplot(data=top_ten_grass, x='Parameter_Value', y='Grassland', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
ro.fig.suptitle('Grassland gradients')
ro.set_titles('{col_name}')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/sensitivity_grass.png')
plt.show()


# # THORNY SCRUB
scrub_gradients = []
# find the gradient
for grouped_name, grouped_data in grouped_dfs:
    res = linregress(grouped_data["Parameter_Value"], grouped_data["Thorny Scrub"])
    scrub_gradient = [grouped_name, res.slope]
    scrub_gradients.append(scrub_gradient)
scrub_gradients = pd.DataFrame(scrub_gradients)
scrub_gradients.columns = ['Parameter_names', 'Gradient']
# take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
scrub_gradients['Gradient'] = scrub_gradients['Gradient'].abs()
scrub_gradients = scrub_gradients.sort_values(['Gradient'], ascending=[False])
top_ten = scrub_gradients.iloc[0:10,:]
top_ten.to_excel("/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/final_df_gradients_scrub.xlsx")
# plot those
top_ten_scrub = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
ro = sns.relplot(data=top_ten_scrub , x='Parameter_Value', y='Thorny Scrub', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
ro.fig.suptitle('Scrub gradients')
ro.set_titles('{col_name}')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/sensitivity_scrub.png')
plt.show()



# # WOODLAND
woodland_gradients = []
# find the gradient
for grouped_name, grouped_data in grouped_dfs:
    res = linregress(grouped_data["Parameter_Value"], grouped_data["Woodland"])
    woodland_gradient = [grouped_name, res.slope]
    woodland_gradients.append(woodland_gradient)
woodland_gradients = pd.DataFrame(woodland_gradients)
woodland_gradients.columns = ['Parameter_names', 'Gradient']
# take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
woodland_gradients['Gradient'] = woodland_gradients['Gradient'].abs()
woodland_gradients = woodland_gradients.sort_values(['Gradient'], ascending=[False])
top_ten = woodland_gradients.iloc[0:10,:]
top_ten.to_excel("/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/final_df_gradients_woodland.xlsx")
# plot those
top_ten_woodland = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
ro = sns.relplot(data=top_ten_woodland, x='Parameter_Value', y='Woodland', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
ro.fig.suptitle('Woodland gradients')
ro.set_titles('{col_name}')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/sensitivity/sensitivity_woodland.png')
plt.show()