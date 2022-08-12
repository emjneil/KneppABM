# run experiments on the accepted parameter sets
# from run_model import run_all_models
# from run_model_linux import run_all_models
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

def run_counterfactual(accepted_parameters):
    number_simulations = 100000

    # run the counterfactual: what would have happened if rewilding hadn't occurred?
    final_results_list = []
    run_number = 0

    # take the accepted parameters, and go row by row, running the model
    for _, row in accepted_parameters.iterrows():
        chance_reproduceSapling = row["chance_reproduceSapling"]
        chance_reproduceYoungScrub =  row["chance_reproduceYoungScrub"]
        chance_regrowGrass =  row["chance_regrowGrass"]
        chance_saplingBecomingTree =  row["chance_saplingBecomingTree"]
        chance_youngScrubMatures =  row["chance_youngScrubMatures"]
        chance_scrubOutcompetedByTree =  row["chance_scrubOutcompetedByTree"]
        chance_grassOutcompetedByTree =  row["chance_grassOutcompetedByTree"]
        chance_grassOutcompetedByScrub = row["chance_grassOutcompetedByScrub"]
        chance_saplingOutcompetedByTree =  row["chance_saplingOutcompetedByTree"]
        chance_saplingOutcompetedByScrub =  row["chance_saplingOutcompetedByScrub"]
        chance_youngScrubOutcompetedByScrub =  row["chance_youngScrubOutcompetedByScrub"]
        chance_youngScrubOutcompetedByTree =  row["chance_youngScrubOutcompetedByTree"]
        initial_roeDeer = row["initial_roeDeer"]
        initial_grassland =  row["initial_grassland"]
        initial_woodland =  row["initial_woodland"]
        initial_scrubland =  row["initial_scrubland"]
        roeDeer_reproduce =  row["roeDeer_reproduce"]
        roeDeer_gain_from_grass =  row["roeDeer_gain_from_grass"]
        roeDeer_gain_from_Trees =  row["roeDeer_gain_from_Trees"]
        roeDeer_gain_from_Scrub =  row["roeDeer_gain_from_Scrub"]
        roeDeer_gain_from_Saplings =  row["roeDeer_gain_from_Saplings"]
        roeDeer_gain_from_YoungScrub =  row["roeDeer_gain_from_YoungScrub"]
        ponies_gain_from_grass =  row["ponies_gain_from_grass"]
        ponies_gain_from_Trees =  row["ponies_gain_from_Trees"]
        ponies_gain_from_Scrub =  row["ponies_gain_from_Scrub"]
        ponies_gain_from_Saplings =  row["ponies_gain_from_Saplings"]
        ponies_gain_from_YoungScrub =  row["ponies_gain_from_YoungScrub"]
        cows_reproduce =  row["cows_reproduce"]
        cows_gain_from_grass =  row["cows_gain_from_grass"]
        cows_gain_from_Trees =  row["cows_gain_from_Trees"]
        cows_gain_from_Scrub =  row["cows_gain_from_Scrub"]
        cows_gain_from_Saplings =  row["cows_gain_from_Saplings"]
        cows_gain_from_YoungScrub =  row["cows_gain_from_YoungScrub"]
        fallowDeer_reproduce =  row["fallowDeer_reproduce"]
        fallowDeer_gain_from_grass =  row["fallowDeer_gain_from_grass"]
        fallowDeer_gain_from_Trees =  row["fallowDeer_gain_from_Trees"]
        fallowDeer_gain_from_Scrub =  row["fallowDeer_gain_from_Scrub"]
        fallowDeer_gain_from_Saplings =  row["fallowDeer_gain_from_Saplings"]
        fallowDeer_gain_from_YoungScrub =  row["fallowDeer_gain_from_YoungScrub"]
        redDeer_reproduce =  row["redDeer_reproduce"]
        redDeer_gain_from_grass =  row["redDeer_gain_from_grass"]
        redDeer_gain_from_Trees =  row["redDeer_gain_from_Trees"]
        redDeer_gain_from_Scrub =  row["redDeer_gain_from_Scrub"]
        redDeer_gain_from_Saplings =  row["redDeer_gain_from_Saplings"]
        redDeer_gain_from_YoungScrub =  row["redDeer_gain_from_YoungScrub"]
        pigs_reproduce =  row["pigs_reproduce"]
        pigs_gain_from_grass =  row["pigs_gain_from_grass"]
        pigs_gain_from_Trees = row["pigs_gain_from_Trees"]
        pigs_gain_from_Scrub = row["pigs_gain_from_Scrub"]
        pigs_gain_from_Saplings =  row["pigs_gain_from_Saplings"]
        pigs_gain_from_YoungScrub =  row["pigs_gain_from_YoungScrub"]
        # stocking values
        fallowDeer_stocking = row["fallowDeer_stocking"]
        cattle_stocking = row["cattle_stocking"]
        redDeer_stocking =  row["redDeer_stocking"]
        tamworthPig_stocking = row["tamworthPig_stocking"]
        exmoor_stocking = row["exmoor_stocking"]
        # euro bison parameters
        reproduce_bison =  row["reproduce_bison"] # make this between the min/max consumer values 
        # bison should have higher impact than any other consumer
        bison_gain_from_grass =  row['bison_gain_from_grass']
        bison_gain_from_Trees = row["bison_gain_from_Trees"]
        bison_gain_from_Scrub = row["bison_gain_from_Scrub"]
        bison_gain_from_Saplings = row["bison_gain_from_Saplings"]
        bison_gain_from_YoungScrub = row["bison_gain_from_YoungScrub"]
        # euro elk parameters
        reproduce_elk = row["reproduce_elk"] # make this between the min/max consumer values 
        # bison should have higher impact than any other consumer
        elk_gain_from_grass = row["elk_gain_from_grass"]
        elk_gain_from_Trees =row["elk_gain_from_Trees"]
        elk_gain_from_Scrub = row["elk_gain_from_Scrub"]
        elk_gain_from_Saplings =  row["elk_gain_from_Saplings"]
        elk_gain_from_YoungScrub = row["elk_gain_from_YoungScrub"]
        # reindeer parameters
        reproduce_reindeer = row["reproduce_reindeer"] # make this between the min/max consumer values 
        # reindeer should have impacts between red and fallow deer
        reindeer_gain_from_grass =  row["reindeer_gain_from_grass"]
        reindeer_gain_from_Trees = row["reindeer_gain_from_Trees"]
        reindeer_gain_from_Scrub = row["reindeer_gain_from_Scrub"]
        reindeer_gain_from_Saplings =  row["reindeer_gain_from_Saplings"]
        reindeer_gain_from_YoungScrub = row["reindeer_gain_from_YoungScrub"] 
        fallowDeer_stocking_forecast = 247
        cattle_stocking_forecast = 81
        redDeer_stocking_forecast = 35
        tamworthPig_stocking_forecast = 7
        exmoor_stocking_forecast = 15
        roeDeer_stocking_forecast = 0
        reindeer_stocking_forecast = 0

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
            width = 25, height = 18, max_time = 184, reintroduction = False,
            introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False, cull_roe = False)

        model.run_model()

        run_number +=1
        print(run_number)

        results = model.datacollector.get_model_vars_dataframe()
        results['run_number'] = run_number
        final_results_list.append(results)
    # append to dataframe
    counterfactual = pd.concat(final_results_list)
    counterfactual['accepted?'] = "noReintro"
    counterfactual.to_csv("combined_counterfactual.csv")

    return counterfactual








def forecasting():

    accepted_parameters = pd.read_csv('combined_accepted_parameters.csv') 
    accepted_parameters.drop(['Unnamed: 0', 'run_number', 'accepted?'], axis=1, inplace=True)
    # accepted_parameters = accepted_parameters[0:3]

    # run the counterfactual: what would have happened if rewilding hadn't occurred?
    final_results_list = []
    run_number = 0

    # look at these stocking densities
    perc_aboveBelow = [-0.5,0,0.5]

    for i in perc_aboveBelow:

        # take the accepted parameters, and go row by row, running the model
        for _, row in accepted_parameters.iterrows():

            chance_reproduceSapling = row["chance_reproduceSapling"]
            chance_reproduceYoungScrub =  row["chance_reproduceYoungScrub"]
            chance_regrowGrass =  row["chance_regrowGrass"]
            chance_saplingBecomingTree =  row["chance_saplingBecomingTree"]
            chance_youngScrubMatures =  row["chance_youngScrubMatures"]
            chance_scrubOutcompetedByTree =  row["chance_scrubOutcompetedByTree"]
            chance_grassOutcompetedByTree =  row["chance_grassOutcompetedByTree"]
            chance_grassOutcompetedByScrub = row["chance_grassOutcompetedByScrub"]
            chance_saplingOutcompetedByTree =  row["chance_saplingOutcompetedByTree"]
            chance_saplingOutcompetedByScrub =  row["chance_saplingOutcompetedByScrub"]
            chance_youngScrubOutcompetedByScrub =  row["chance_youngScrubOutcompetedByScrub"]
            chance_youngScrubOutcompetedByTree =  row["chance_youngScrubOutcompetedByTree"]
            initial_roeDeer = row["initial_roeDeer"]
            initial_grassland =  row["initial_grassland"]
            initial_woodland =  row["initial_woodland"]
            initial_scrubland =  row["initial_scrubland"]
            roeDeer_reproduce =  row["roeDeer_reproduce"]
            roeDeer_gain_from_grass =  row["roeDeer_gain_from_grass"]
            roeDeer_gain_from_Trees =  row["roeDeer_gain_from_Trees"]
            roeDeer_gain_from_Scrub =  row["roeDeer_gain_from_Scrub"]
            roeDeer_gain_from_Saplings =  row["roeDeer_gain_from_Saplings"]
            roeDeer_gain_from_YoungScrub =  row["roeDeer_gain_from_YoungScrub"]
            ponies_gain_from_grass =  row["ponies_gain_from_grass"]
            ponies_gain_from_Trees =  row["ponies_gain_from_Trees"]
            ponies_gain_from_Scrub =  row["ponies_gain_from_Scrub"]
            ponies_gain_from_Saplings =  row["ponies_gain_from_Saplings"]
            ponies_gain_from_YoungScrub =  row["ponies_gain_from_YoungScrub"]
            cows_reproduce =  row["cows_reproduce"]
            cows_gain_from_grass =  row["cows_gain_from_grass"]
            cows_gain_from_Trees =  row["cows_gain_from_Trees"]
            cows_gain_from_Scrub =  row["cows_gain_from_Scrub"]
            cows_gain_from_Saplings =  row["cows_gain_from_Saplings"]
            cows_gain_from_YoungScrub =  row["cows_gain_from_YoungScrub"]
            fallowDeer_reproduce =  row["fallowDeer_reproduce"]
            fallowDeer_gain_from_grass =  row["fallowDeer_gain_from_grass"]
            fallowDeer_gain_from_Trees =  row["fallowDeer_gain_from_Trees"]
            fallowDeer_gain_from_Scrub =  row["fallowDeer_gain_from_Scrub"]
            fallowDeer_gain_from_Saplings =  row["fallowDeer_gain_from_Saplings"]
            fallowDeer_gain_from_YoungScrub =  row["fallowDeer_gain_from_YoungScrub"]
            redDeer_reproduce =  row["redDeer_reproduce"]
            redDeer_gain_from_grass =  row["redDeer_gain_from_grass"]
            redDeer_gain_from_Trees =  row["redDeer_gain_from_Trees"]
            redDeer_gain_from_Scrub =  row["redDeer_gain_from_Scrub"]
            redDeer_gain_from_Saplings =  row["redDeer_gain_from_Saplings"]
            redDeer_gain_from_YoungScrub =  row["redDeer_gain_from_YoungScrub"]
            pigs_reproduce =  row["pigs_reproduce"]
            pigs_gain_from_grass =  row["pigs_gain_from_grass"]
            pigs_gain_from_Trees = row["pigs_gain_from_Trees"]
            pigs_gain_from_Scrub = row["pigs_gain_from_Scrub"]
            pigs_gain_from_Saplings =  row["pigs_gain_from_Saplings"]
            pigs_gain_from_YoungScrub =  row["pigs_gain_from_YoungScrub"]
            # stocking values
            fallowDeer_stocking = round(row["fallowDeer_stocking"] + (row["fallowDeer_stocking"] * i))
            cattle_stocking = round(row["cattle_stocking"] + (row["cattle_stocking"]*i))
            redDeer_stocking = round(row["redDeer_stocking"]+ (row["redDeer_stocking"]*i))
            tamworthPig_stocking = round(row["tamworthPig_stocking"]+ (row["tamworthPig_stocking"]*i))
            exmoor_stocking = round(row["exmoor_stocking"]+ (row["exmoor_stocking"]*i))
            # euro bison parameters
            reproduce_bison =  row["reproduce_bison"] # make this between the min/max consumer values 
            # bison should have higher impact than any other consumer
            bison_gain_from_grass =  row['bison_gain_from_grass']
            bison_gain_from_Trees = row["bison_gain_from_Trees"]
            bison_gain_from_Scrub = row["bison_gain_from_Scrub"]
            bison_gain_from_Saplings = row["bison_gain_from_Saplings"]
            bison_gain_from_YoungScrub = row["bison_gain_from_YoungScrub"]
            # euro elk parameters
            reproduce_elk = row["reproduce_elk"] # make this between the min/max consumer values 
            # bison should have higher impact than any other consumer
            elk_gain_from_grass = row["elk_gain_from_grass"]
            elk_gain_from_Trees =row["elk_gain_from_Trees"]
            elk_gain_from_Scrub = row["elk_gain_from_Scrub"]
            elk_gain_from_Saplings =  row["elk_gain_from_Saplings"]
            elk_gain_from_YoungScrub = row["elk_gain_from_YoungScrub"]
            # reindeer parameters
            reproduce_reindeer = row["reproduce_reindeer"] # make this between the min/max consumer values 
            # reindeer should have impacts between red and fallow deer
            reindeer_gain_from_grass =  row["reindeer_gain_from_grass"]
            reindeer_gain_from_Trees = row["reindeer_gain_from_Trees"]
            reindeer_gain_from_Scrub = row["reindeer_gain_from_Scrub"]
            reindeer_gain_from_Saplings =  row["reindeer_gain_from_Saplings"]
            reindeer_gain_from_YoungScrub = row["reindeer_gain_from_YoungScrub"] 
            fallowDeer_stocking_forecast = round(row["fallowDeer_stocking"] + (row["fallowDeer_stocking"] * i))
            cattle_stocking_forecast = round(row["cattle_stocking"] + (row["cattle_stocking"]*i))
            redDeer_stocking_forecast = round(row["redDeer_stocking"]+ (row["redDeer_stocking"]*i))
            tamworthPig_stocking_forecast = round(row["tamworthPig_stocking"]+ (row["tamworthPig_stocking"]*i))
            exmoor_stocking_forecast = round(row["exmoor_stocking"]+ (row["exmoor_stocking"]*i))
            reindeer_stocking_forecast = 0
            roeDeer_stocking_forecast = 0

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
                fallowDeer_stocking_forecast, cattle_stocking_forecast, redDeer_stocking_forecast, tamworthPig_stocking_forecast, exmoor_stocking_forecast, roeDeer_stocking_forecast, reindeer_stocking_forecast, 
                width = 25, height = 18, max_time = 784, reintroduction = True,
                introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False, cull_roe = False)

            model.run_model()

            run_number +=1
            print(run_number)

            results = model.datacollector.get_model_vars_dataframe()
            results['run_number'] = run_number
            results['perc_above_below'] = i
            final_results_list.append(results)


    # append to dataframe
    forecasting = pd.concat(final_results_list)

    palette=['#009e73', '#f0e442', '#0072b2','#cc79a7']

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
        ax.fill_between(ax.lines[3].get_xdata(),ax.lines[3].get_ydata(), ax.lines[6].get_ydata(), color="#009e73",alpha =0.2)
        ax.fill_between(ax.lines[4].get_xdata(),ax.lines[4].get_ydata(), ax.lines[7].get_ydata(), color="#f0e442",alpha =0.2)
        ax.fill_between(ax.lines[5].get_xdata(),ax.lines[5].get_ydata(), ax.lines[8].get_ydata(),color="#0072b2",alpha =0.2)
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

    f.fig.suptitle('Forecasting fifty years into the future, with different stocking densities')
    plt.tight_layout()
    plt.legend(labels=['-50%','Current Stocking Density','+50%'],bbox_to_anchor=(2.2, 0), loc='lower right', fontsize=12)
    plt.savefig('forecasting_experiment_test.png')
    plt.show()

    return forecasting, final_df

# forecasting()