# graph the runs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from KneppModel_ABM import KneppModel 
import numpy as np
import pandas as pd
from scipy.stats import linregress


# define number of simulations
number_simulations =  1
# make list of variables
final_results_list = []
final_parameters = []
run_number = 0

for _ in range(number_simulations):
    # keep track of the runs
    run_number +=1
    # habitats
    chance_reproduceSapling = 0.01599083
    chance_reproduceYoungScrub = 0.05596995
    chance_regrowGrass = 0.0841251
    chance_saplingBecomingTree = 0.00212349
    chance_youngScrubMatures = 0.01186857
    chance_scrubOutcompetedByTree = 0.00880328
    chance_grassOutcompetedByTree = 0.17032938
    chance_grassOutcompetedByScrub = 0.17482715
    chance_saplingOutcompetedByTree = 0.06540329
    chance_saplingOutcompetedByScrub = 0.02308093
    chance_youngScrubOutcompetedByScrub = 0.06625781
    chance_youngScrubOutcompetedByTree = 0.06854397
    # initial values
    initial_roeDeer = 0.12
    initial_grassland = 0.8
    initial_woodland = 0.14
    initial_scrubland = 0.01
    # roe deer
    roeDeer_reproduce = 0.18321307
    roeDeer_gain_from_grass = 0.91357378
    roeDeer_gain_from_Trees = 0.86834529
    roeDeer_gain_from_Scrub = 0.93482336
    roeDeer_gain_from_Saplings = 0.13490778
    roeDeer_gain_from_YoungScrub = 0.11024164
    # Fallow deer
    fallowDeer_reproduce = 0.37292093
    fallowDeer_gain_from_grass = 0.91237466
    fallowDeer_gain_from_Trees = 0.87144027
    fallowDeer_gain_from_Scrub = 0.86708181
    fallowDeer_gain_from_Saplings = 0.10743504
    fallowDeer_gain_from_YoungScrub = 0.10073944
    # Red deer
    redDeer_reproduce = 0.39482522
    redDeer_gain_from_grass = 0.92850426
    redDeer_gain_from_Trees = 0.92358395
    redDeer_gain_from_Scrub = 0.91620809
    redDeer_gain_from_Saplings = 0.11779972
    redDeer_gain_from_YoungScrub =0.09440902
    # Exmoor ponies
    ponies_gain_from_grass = 0.90086234
    ponies_gain_from_Trees = 0.87800124
    ponies_gain_from_Scrub = 0.8764282
    ponies_gain_from_Saplings = 0.07381227
    ponies_gain_from_YoungScrub = 0.09842013
    # Longhorn cattle
    cows_reproduce = 0.19456058
    cows_gain_from_grass = 0.89778476
    cows_gain_from_Trees = 0.89226723
    cows_gain_from_Scrub = 0.87588117
    cows_gain_from_Saplings = 0.09952247
    cows_gain_from_YoungScrub = 0.06801822
    # Tamworth pigs
    pigs_reproduce = 0.26223023
    pigs_gain_from_grass = 0.81523531
    pigs_gain_from_Trees =0.87275063
    pigs_gain_from_Scrub = 0.89307688
    pigs_gain_from_Saplings = 0.11723434
    pigs_gain_from_YoungScrub = 0.08835914

    max_start_saplings = 0.1
    max_start_youngScrub = 0.1

    # keep track of my parameters
    parameters_used = [
        run_number,
        chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
        chance_scrubOutcompetedByTree, chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
        initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland, 
        roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
        ponies_gain_from_grass, ponies_gain_from_Trees, ponies_gain_from_Scrub, ponies_gain_from_Saplings, ponies_gain_from_YoungScrub, 
        cows_reproduce, cows_gain_from_grass, cows_gain_from_Trees, cows_gain_from_Scrub, cows_gain_from_Saplings, cows_gain_from_YoungScrub, 
        fallowDeer_reproduce, fallowDeer_gain_from_grass, fallowDeer_gain_from_Trees, fallowDeer_gain_from_Scrub, fallowDeer_gain_from_Saplings, fallowDeer_gain_from_YoungScrub, 
        redDeer_reproduce, redDeer_gain_from_grass, redDeer_gain_from_Trees, redDeer_gain_from_Scrub, redDeer_gain_from_Saplings, redDeer_gain_from_YoungScrub, 
        pigs_reproduce, pigs_gain_from_grass, pigs_gain_from_Trees, pigs_gain_from_Scrub, pigs_gain_from_Saplings, pigs_gain_from_YoungScrub
        ]

    # append to dataframe
    final_parameters.append(parameters_used)


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
    results['run_number'] = run_number
    final_results_list.append(results)

# append to dataframe
final_results = pd.concat(final_results_list)

variables = [
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
    # Exmoor pony variables
    "ponies_gain_from_grass", 
    "ponies_gain_from_Trees", 
    "ponies_gain_from_Scrub", 
    "ponies_gain_from_Saplings", 
    "ponies_gain_from_YoungScrub", 
    # Cow variables
    "cows_reproduce", 
    "cows_gain_from_grass", 
    "cows_gain_from_Trees", 
    "cows_gain_from_Scrub", 
    "cows_gain_from_Saplings", 
    "cows_gain_from_YoungScrub", 
    # Fallow deer variables
    "fallowDeer_reproduce", 
    "fallowDeer_gain_from_grass", 
    "fallowDeer_gain_from_Trees", 
    "fallowDeer_gain_from_Scrub", 
    "fallowDeer_gain_from_Saplings", 
    "fallowDeer_gain_from_YoungScrub", 
    # Red deer variables
    "redDeer_reproduce", 
    "redDeer_gain_from_grass", 
    "redDeer_gain_from_Trees", 
    "redDeer_gain_from_Scrub", 
    "redDeer_gain_from_Saplings", 
    "redDeer_gain_from_YoungScrub", 
    # Pig variables
    "pigs_reproduce", 
    "pigs_gain_from_grass", 
    "pigs_gain_from_Trees", 
    "pigs_gain_from_Scrub",
    "pigs_gain_from_Saplings", 
    "pigs_gain_from_YoungScrub"
    ]

# check out the parameters used
final_parameters = pd.DataFrame(data=final_parameters, columns=variables)

final_results = final_results[["Time", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground", "run_number"]]

# SENSITIVITY TEST
sensitivity_results_list = []
sensitivity_parameters = []
run_number  = 0
# choose my percent above/below number
perc_aboveBelow = [-0.1, -0.05,-0.01, 0, 0.01, 0.05, 0.1]
final_parameters = final_parameters.iloc[0,1:78]
# organized = final_parameters.iloc[0:1]
# loop through each one, changing one cell at a time
for index, row in final_parameters.iteritems():
    for perc_number in perc_aboveBelow:
        final_parameters_temp = final_parameters
        run_number += 1
        ifor_val = row + (row*perc_number)
        # make sure they're ints where applicable
        if ifor_val > 1:
            ifor_val = round(ifor_val)
        final_parameters_temp.at[index] = ifor_val
        print(run_number)
        # choose my parameters 
        chance_reproduceSapling = final_parameters_temp.values[0]
        chance_reproduceYoungScrub = final_parameters_temp.values[1]
        chance_regrowGrass = final_parameters_temp.values[2]
        chance_saplingBecomingTree = final_parameters_temp.values[3]
        chance_youngScrubMatures = final_parameters_temp.values[4]
        chance_scrubOutcompetedByTree = final_parameters_temp.values[5]
        chance_grassOutcompetedByTree = final_parameters_temp.values[6]
        chance_grassOutcompetedByScrub = final_parameters_temp.values[7]
        chance_saplingOutcompetedByTree = final_parameters_temp.values[8]
        chance_saplingOutcompetedByScrub = final_parameters_temp.values[9]
        chance_youngScrubOutcompetedByScrub = final_parameters_temp.values[10]
        chance_youngScrubOutcompetedByTree = final_parameters_temp.values[11]
        initial_roeDeer = final_parameters_temp.values[12]
        initial_grassland = final_parameters_temp.values[13]
        initial_woodland = final_parameters_temp.values[14]
        initial_scrubland = final_parameters_temp.values[15]
        roeDeer_reproduce = final_parameters_temp.values[16]
        roeDeer_gain_from_grass = final_parameters_temp.values[17]
        roeDeer_gain_from_Trees = final_parameters_temp.values[18]
        roeDeer_gain_from_Scrub = final_parameters_temp.values[19]
        roeDeer_gain_from_Saplings = final_parameters_temp.values[20]
        roeDeer_gain_from_YoungScrub = final_parameters_temp.values[21]

        ponies_gain_from_grass = final_parameters_temp.values[27]
        ponies_gain_from_Trees = final_parameters_temp.values[28]
        ponies_gain_from_Scrub = final_parameters_temp.values[29]
        ponies_gain_from_Saplings = final_parameters_temp.values[30]
        ponies_gain_from_YoungScrub = final_parameters_temp.values[31]
        
        cows_reproduce = final_parameters_temp.values[37]
        cows_gain_from_grass = final_parameters_temp.values[38]
        cows_gain_from_Trees = final_parameters_temp.values[39]
        cows_gain_from_Scrub = final_parameters_temp.values[40]
        cows_gain_from_Saplings = final_parameters_temp.values[41]
        cows_gain_from_YoungScrub = final_parameters_temp.values[42]
        
        fallowDeer_reproduce = final_parameters_temp.values[48]
        fallowDeer_gain_from_grass = final_parameters_temp.values[49]
        fallowDeer_gain_from_Trees = final_parameters_temp.values[50]
        fallowDeer_gain_from_Scrub = final_parameters_temp.values[51]
        fallowDeer_gain_from_Saplings = final_parameters_temp.values[52]
        fallowDeer_gain_from_YoungScrub = final_parameters_temp.values[53]
        
        redDeer_reproduce = final_parameters_temp.values[59]
        redDeer_gain_from_grass = final_parameters_temp.values[60]
        redDeer_gain_from_Trees = final_parameters_temp.values[61]
        redDeer_gain_from_Scrub = final_parameters_temp.values[62]
        redDeer_gain_from_Saplings = final_parameters_temp.values[63]
        redDeer_gain_from_YoungScrub = final_parameters_temp.values[64]
        
        pigs_reproduce = final_parameters_temp.values[70]
        pigs_gain_from_grass = final_parameters_temp.values[71]
        pigs_gain_from_Trees = 
        pigs_gain_from_Scrub =
        pigs_gain_from_Saplings = final_parameters_temp.values[72]
        pigs_gain_from_YoungScrub = final_parameters_temp.values[73]


        # run model
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
        sensitivity_results_unfiltered = model.datacollector.get_model_vars_dataframe()
        sensitivity_results = sensitivity_results_unfiltered[(sensitivity_results_unfiltered["Time"] == 184)]
        sensitivity_results_list.append(sensitivity_results)
        # and the parameter changed
        sensitivity_parameters.append([index, final_parameters_temp.at[index]])

# append to dataframe
final_sensitivity_results = pd.concat(sensitivity_results_list)
final_sensitivity_parameters = pd.DataFrame(sensitivity_parameters)
final_sensitivity_parameters.columns = ['Parameter_Changes', 'Parameter_Value']
final_sensitivity_results = final_sensitivity_results.reset_index(drop=True)
merged_dfs = pd.concat([final_sensitivity_parameters, final_sensitivity_results], axis=1)
merged_dfs = merged_dfs.drop('Time', 1)
# print("merged", merged_dfs)
merged_dfs.to_excel("/Users/emilyneil/Desktop/KneppABM/many_outputs2/all_parameter_changes.xlsx")

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
top_ten.to_excel("final_df_gradients_roeDeer.xlsx")
# plot those
top_ten_roe = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
ro = sns.relplot(data=top_ten_roe, x='Parameter_Value', y='Roe deer', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
ro.fig.suptitle('Roe deer gradients')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/many_outputs2/sensitivity_roe.png')
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
top_ten.to_excel("final_df_gradients_fallowDeer.xlsx")
# plot those
top_ten_fallow = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
ro = sns.relplot(data=top_ten_fallow, x='Parameter_Value', y='Fallow deer', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
ro.fig.suptitle('Fallow deer gradients')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/many_outputs2/sensitivity_fallow.png')
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
top_ten.to_excel("final_df_gradients_redDeer.xlsx")
# plot those
top_ten_red = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
ro = sns.relplot(data=top_ten_roe, x='Parameter_Value', y='Red deer', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
ro.fig.suptitle('Red deer gradients')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/many_outputs2/sensitivity_red.png')
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
top_ten.to_excel("final_df_gradients_cattle.xlsx")
# plot those
top_ten_cattle = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
ro = sns.relplot(data=top_ten_cattle, x='Parameter_Value', y='Longhorn cattle', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
ro.fig.suptitle('Cattle gradients')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/many_outputs2/sensitivity_cattle.png')
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
top_ten.to_excel("final_df_gradients_pig.xlsx")
# plot those
top_ten_pig = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
ro = sns.relplot(data=top_ten_pig, x='Parameter_Value', y='Tamworth pigs', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
ro.fig.suptitle('Tamworth pig gradients')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/many_outputs2/sensitivity_pig.png')
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
top_ten.to_excel("final_df_gradients_pony.xlsx")
# plot those
top_ten_pony = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
ro = sns.relplot(data=top_ten_pony, x='Parameter_Value', y='Exmoor pony', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
ro.fig.suptitle('Exmoor pony gradients')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/many_outputs2/sensitivity_pony.png')
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
top_ten.to_excel("final_df_gradients_grass.xlsx")
# plot those
top_ten_grass = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
ro = sns.relplot(data=top_ten_grass, x='Parameter_Value', y='Grassland', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
ro.fig.suptitle('Grassland gradients')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/many_outputs2/sensitivity_grass.png')
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
top_ten.to_excel("final_df_gradients_scrub.xlsx")
# plot those
top_ten_scrub = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
ro = sns.relplot(data=top_ten_scrub , x='Parameter_Value', y='Thorny Scrub', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
ro.fig.suptitle('Scrub gradients')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/many_outputs2/sensitivity_scrub.png')
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
top_ten.to_excel("final_df_gradients_woodland.xlsx")
# plot those
top_ten_woodland = merged_dfs[merged_dfs['Parameter_Changes'].isin(top_ten['Parameter_names'])]
ro = sns.relplot(data=top_ten_woodland, x='Parameter_Value', y='Woodland', col='Parameter_Changes', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
ro.fig.suptitle('Woodland gradients')
plt.tight_layout()
plt.savefig('/Users/emilyneil/Desktop/KneppABM/many_outputs2/sensitivity_woodland.png')
plt.show()


