# run experiments on the accepted parameter sets
# from run_model import run_all_models
from run_model_linux import run_all_models
from KneppModel_ABM import KneppModel
from mesa import Model
from mesa.datacollection import DataCollector
import numpy as np
import random
import pandas as pd
from schedule import RandomActivationByBreed
from mesa.space import MultiGrid
import seaborn as sns
import matplotlib.pyplot as plt



                                # # # # ------ Define the model ------ # # # #

def run_counterfactual():
    number_simulations, final_results, accepted_parameters = run_all_models()
    # run the counterfactual: what would have happened if rewilding hadn't occurred?
    final_results_list = []
    run_number = 0

    # take the accepted parameters, and go row by row, running the model
    for _, row in accepted_parameters.iterrows():

        chance_reproduceSapling = row[0]
        chance_reproduceYoungScrub =  row[1]
        chance_regrowGrass =  row[2]
        chance_saplingBecomingTree =  row[3]
        chance_youngScrubMatures =  row[4]
        chance_scrubOutcompetedByTree =  row[5]
        chance_grassOutcompetedByTree =  row[6]
        chance_grassOutcompetedByScrub = row[7]
        chance_saplingOutcompetedByTree =  row[8]
        chance_saplingOutcompetedByScrub =  row[9]
        chance_youngScrubOutcompetedByScrub =  row[10]
        chance_youngScrubOutcompetedByTree =  row[11]
        initial_roeDeer = row[12]
        initial_grassland =  row[13]
        initial_woodland =  row[14]
        initial_scrubland =  row[15]
        roeDeer_reproduce =  row[16]
        roeDeer_gain_from_grass =  row[17]
        roeDeer_gain_from_Trees =  row[18]
        roeDeer_gain_from_Scrub =  row[19]
        roeDeer_gain_from_Saplings =  row[20]
        roeDeer_gain_from_YoungScrub =  row[21]
        ponies_gain_from_grass =  row[22]
        ponies_gain_from_Trees =  row[23]
        ponies_gain_from_Scrub =  row[24]
        ponies_gain_from_Saplings =  row[25]
        ponies_gain_from_YoungScrub =  row[26]
        cows_reproduce =  row[27]
        cows_gain_from_grass =  row[28]
        cows_gain_from_Trees =  row[29]
        cows_gain_from_Scrub =  row[30]
        cows_gain_from_Saplings =  row[31]
        cows_gain_from_YoungScrub =  row[32]
        fallowDeer_reproduce =  row[33]
        fallowDeer_gain_from_grass =  row[34]
        fallowDeer_gain_from_Trees =  row[35]
        fallowDeer_gain_from_Scrub =  row[36]
        fallowDeer_gain_from_Saplings =  row[37]
        fallowDeer_gain_from_YoungScrub =  row[38]
        redDeer_reproduce =  row[39]
        redDeer_gain_from_grass =  row[40]
        redDeer_gain_from_Trees =  row[41]
        redDeer_gain_from_Scrub =  row[42]
        redDeer_gain_from_Saplings =  row[43]
        redDeer_gain_from_YoungScrub =  row[44]
        pigs_reproduce =  row[45]
        pigs_gain_from_grass =  row[46]
        pigs_gain_from_Trees = row[47]
        pigs_gain_from_Scrub = row[48]
        pigs_gain_from_Saplings =  row[49]
        pigs_gain_from_YoungScrub =  row[50]
        # stocking values
        fallowDeer_stocking = row[51]
        cattle_stocking = row[52]
        redDeer_stocking = row[53]
        tamworthPig_stocking = row[54]
        exmoor_stocking = row[55]

        # euro bison parameters
        reproduce_bison =  row[56] # make this between the min/max consumer values 
        # bison should have higher impact than any other consumer
        bison_gain_from_grass =  row[57]
        bison_gain_from_Trees = row[58]
        bison_gain_from_Scrub = row[59]
        bison_gain_from_Saplings = row[60]
        bison_gain_from_YoungScrub = row[61]
        # euro elk parameters
        reproduce_elk = row[62] # make this between the min/max consumer values 
        # bison should have higher impact than any other consumer
        elk_gain_from_grass = row[63]
        elk_gain_from_Trees =row[64]
        elk_gain_from_Scrub = row[65]
        elk_gain_from_Saplings =  row[66]
        elk_gain_from_YoungScrub = row[67]
        # reindeer parameters
        reproduce_reindeer = row[68] # make this between the min/max consumer values 
        # reindeer should have impacts between red and fallow deer
        reindeer_gain_from_grass =  row[69]
        reindeer_gain_from_Trees = row[70]
        reindeer_gain_from_Scrub = row[71]
        reindeer_gain_from_Saplings =  row[72]
        reindeer_gain_from_YoungScrub = row[73] 

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
            width = 25, height = 18, max_time = 184, reintroduction = False,
            introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)

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



def forecasting():

    accepted_parameters = pd.read_csv('outputs/ten_perc/accepted_parameters_10%.csv')    
    accepted_parameters.drop(['Unnamed: 0', 'run_number'], axis=1, inplace=True)
    accepted_parameters = accepted_parameters[0:3]

    # run the counterfactual: what would have happened if rewilding hadn't occurred?
    final_results_list = []
    run_number = 0

    # look at these stocking densities
    perc_aboveBelow = [-0.5,0,0.5]

    for i in perc_aboveBelow:

        # take the accepted parameters, and go row by row, running the model
        for _, row in accepted_parameters.iterrows():

            chance_reproduceSapling = row[0]
            chance_reproduceYoungScrub =  row[1]
            chance_regrowGrass =  row[2]
            chance_saplingBecomingTree =  row[3]
            chance_youngScrubMatures =  row[4]
            chance_scrubOutcompetedByTree =  row[5]
            chance_grassOutcompetedByTree =  row[6]
            chance_grassOutcompetedByScrub = row[7]
            chance_saplingOutcompetedByTree =  row[8]
            chance_saplingOutcompetedByScrub =  row[9]
            chance_youngScrubOutcompetedByScrub =  row[10]
            chance_youngScrubOutcompetedByTree =  row[11]
            initial_roeDeer = row[12]
            initial_grassland =  row[13]
            initial_woodland =  row[14]
            initial_scrubland =  row[15]
            roeDeer_reproduce =  row[16]
            roeDeer_gain_from_grass =  row[17]
            roeDeer_gain_from_Trees =  row[18]
            roeDeer_gain_from_Scrub =  row[19]
            roeDeer_gain_from_Saplings =  row[20]
            roeDeer_gain_from_YoungScrub =  row[21]
            ponies_gain_from_grass =  row[22]
            ponies_gain_from_Trees =  row[23]
            ponies_gain_from_Scrub =  row[24]
            ponies_gain_from_Saplings =  row[25]
            ponies_gain_from_YoungScrub =  row[26]
            cows_reproduce =  row[27]
            cows_gain_from_grass =  row[28]
            cows_gain_from_Trees =  row[29]
            cows_gain_from_Scrub =  row[30]
            cows_gain_from_Saplings =  row[31]
            cows_gain_from_YoungScrub =  row[32]
            fallowDeer_reproduce =  row[33]
            fallowDeer_gain_from_grass =  row[34]
            fallowDeer_gain_from_Trees =  row[35]
            fallowDeer_gain_from_Scrub =  row[36]
            fallowDeer_gain_from_Saplings =  row[37]
            fallowDeer_gain_from_YoungScrub =  row[38]
            redDeer_reproduce =  row[39]
            redDeer_gain_from_grass =  row[40]
            redDeer_gain_from_Trees =  row[41]
            redDeer_gain_from_Scrub =  row[42]
            redDeer_gain_from_Saplings =  row[43]
            redDeer_gain_from_YoungScrub =  row[44]
            pigs_reproduce =  row[45]
            pigs_gain_from_grass =  row[46]
            pigs_gain_from_Trees = row[47]
            pigs_gain_from_Scrub = row[48]
            pigs_gain_from_Saplings =  row[49]
            pigs_gain_from_YoungScrub =  row[50]

            fallowDeer_stocking = round(row[51] + (row[51] * i))
            cattle_stocking = round(row[52] + (row[52]*i))
            redDeer_stocking = round(row[53]+ (row[53]*i))
            tamworthPig_stocking = round(row[54]+ (row[54]*i))
            exmoor_stocking = round(row[55]+ (row[55]*i))

            # euro bison parameters
            reproduce_bison =  row[56] # make this between the min/max consumer values 
            # bison should have higher impact than any other consumer
            bison_gain_from_grass =  row[57]
            bison_gain_from_Trees = row[58]
            bison_gain_from_Scrub = row[59]
            bison_gain_from_Saplings = row[60]
            bison_gain_from_YoungScrub = row[61]
            # euro elk parameters
            reproduce_elk = row[62] # make this between the min/max consumer values 
            # bison should have higher impact than any other consumer
            elk_gain_from_grass = row[63]
            elk_gain_from_Trees =row[64]
            elk_gain_from_Scrub = row[65]
            elk_gain_from_Saplings =  row[66]
            elk_gain_from_YoungScrub = row[67]
            # reindeer parameters
            reproduce_reindeer = row[68] # make this between the min/max consumer values 
            # reindeer should have impacts between red and fallow deer
            reindeer_gain_from_grass =  row[69]
            reindeer_gain_from_Trees = row[70]
            reindeer_gain_from_Scrub = row[71]
            reindeer_gain_from_Saplings =  row[72]
            reindeer_gain_from_YoungScrub = row[73] 

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
                width = 25, height = 18, max_time = 784, reintroduction = True,
                introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)

            model.run_model()

            run_number +=1
            print(run_number)

            results = model.datacollector.get_model_vars_dataframe()
            results['run_number'] = run_number
            results['perc_above_below'] = i
            final_results_list.append(results)


    # append to dataframe
    forecasting = pd.concat(final_results_list)

    palette=['#db5f57', '#57d3db', '#57db5f','#5f57db', '#db57d3']

    # graph that
    final_results = forecasting[["Time", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground", "perc_above_below", "run_number"]]
    grouping_variable = np.repeat(final_results['run_number'], 10)
    y_values = final_results.drop(['run_number', 'perc_above_below', 'Time'], axis=1).values.flatten()
    accepted_shape = np.repeat(final_results['perc_above_below'], 10)
    species_list = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 785*len(accepted_parameters)*len(perc_aboveBelow))
    indices = np.repeat(final_results['Time'], 10)

    final_df = pd.DataFrame(
    {'Abundance %': y_values, 'runNumber': grouping_variable, 'Ecosystem Element': species_list, 'Time': indices, 'Perc': accepted_shape})
    # calculate median
    m = final_df.groupby(['Time', 'Perc', 'Ecosystem Element'])[['Abundance %']].apply(np.median)
    m.name = 'Median'
    final_df = final_df.join(m, on=['Time', 'Perc', 'Ecosystem Element'])
    # calculate quantiles
    perc1 = final_df.groupby(['Time', 'Perc', 'Ecosystem Element'])['Abundance %'].quantile(.95)
    perc1.name = 'ninetyfivePerc'
    final_df = final_df.join(perc1, on=['Time', 'Perc', 'Ecosystem Element'])
    perc2 = final_df.groupby(['Time', 'Perc', 'Ecosystem Element'])['Abundance %'].quantile(.05)
    perc2.name = "fivePerc"
    final_df = final_df.join(perc2, on=['Time','Perc', 'Ecosystem Element'])

    final_df = final_df.reset_index(drop=True)
    final_df.to_csv("forecasting_experiment.csv")

    counterfactual_graph = final_df.reset_index(drop=True)
    f = sns.FacetGrid(final_df, col="Ecosystem Element", palette = palette, hue = "Perc", col_wrap=4, sharey = False)
    f.map(sns.lineplot, 'Time', 'Median') 
    # 0,1,2,
    f.map(sns.lineplot, 'Time', 'fivePerc') 
    # 3,4,5
    f.map(sns.lineplot, 'Time', 'ninetyfivePerc')
    # 6,7,8
    for ax in f.axes.flat:
        ax.fill_between(ax.lines[3].get_xdata(),ax.lines[3].get_ydata(), ax.lines[6].get_ydata(), color="#db5f57",alpha =0.2)
        ax.fill_between(ax.lines[4].get_xdata(),ax.lines[4].get_ydata(), ax.lines[7].get_ydata(), color="#57d3db",alpha =0.2)
        ax.fill_between(ax.lines[5].get_xdata(),ax.lines[5].get_ydata(), ax.lines[8].get_ydata(),color="#57db5f",alpha =0.2)
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
    plt.legend(labels=['-50%','Current Stocking Density','+50%'],bbox_to_anchor=(2.2, 0), loc='lower right', fontsize=12)
    plt.savefig('forecasting_experiment_test.png')
    plt.show()

    return forecasting, final_df

forecasting()