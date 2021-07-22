
# ------ ABM of the Knepp Estate (2005-2046) --------
from KneppModel_ABM import KneppModel 
import numpy as np
import random
import pandas as pd
import timeit
# import seaborn as sns
# import numpy.matlib
# import matplotlib.pyplot as plt
# from scipy import stats


# time the program
start = timeit.default_timer()



                                                    # # # # Run the model # # # # 


def run_all_models():
    # define number of simulations
    number_simulations =  1
    # make list of variables
    final_results_list = []
    final_parameters = []
    run_number = 0


    for _ in range(number_simulations):
        # choose my parameters 
        initial_roeDeer = random.randint(6, 18)
        initial_grassland = random.randint(70, 90)
        initial_woodland = random.randint(4, 24)
        initial_scrubland = random.randint(0, 11)
        # habitats
        chance_reproduceSapling = np.random.uniform(0,1)
        chance_reproduceYoungScrub = np.random.uniform(0,1)
        chance_regrowGrass = np.random.uniform(0,1)
        chance_saplingBecomingTree = np.random.uniform(0,1)
        chance_youngScrubMatures = np.random.uniform(0,1)
        chance_scrubOutcompetedByTree = np.random.uniform(0,1) 
        chance_grassOutcompetedByTreeScrub = np.random.uniform(0,1)
        chance_saplingOutcompetedByTree = np.random.uniform(0,1)
        chance_saplingOutcompetedByScrub = np.random.uniform(0,1)
        chance_youngScrubOutcompetedByScrub = np.random.uniform(0,1)
        chance_youngScrubOutcompetedByTree = np.random.uniform(0,1)
        # roe deer
        roeDeer_reproduce = np.random.uniform(0,1)
        roeDeer_gain_from_grass = np.random.uniform(0,1)
        roeDeer_gain_from_Trees = np.random.uniform(0,1)
        roeDeer_gain_from_Scrub = np.random.uniform(0,1)
        roeDeer_gain_from_Saplings = np.random.uniform(0,1)
        roeDeer_gain_from_YoungScrub = np.random.uniform(0,1)
        roeDeer_impactGrass = random.randint(0,100)
        roeDeer_saplingsEaten = random.randint(0,100)
        roeDeer_youngScrubEaten = random.randint(0,100)
        roeDeer_treesEaten = random.randint(0,10)
        roeDeer_scrubEaten = random.randint(0,10)
        # Fallow deer
        fallowDeer_reproduce = np.random.uniform(0,1)
        fallowDeer_gain_from_grass = np.random.uniform(0,1)
        fallowDeer_gain_from_Trees = np.random.uniform(0,1)
        fallowDeer_gain_from_Scrub = np.random.uniform(0,1)
        fallowDeer_gain_from_Saplings = np.random.uniform(0,1)
        fallowDeer_gain_from_YoungScrub = np.random.uniform(0,1)
        fallowDeer_impactGrass = random.randint(roeDeer_impactGrass,100)
        fallowDeer_saplingsEaten = random.randint(roeDeer_saplingsEaten,100)
        fallowDeer_youngScrubEaten = random.randint(roeDeer_youngScrubEaten,100)
        fallowDeer_treesEaten = random.randint(roeDeer_treesEaten,10)
        fallowDeer_scrubEaten = random.randint(roeDeer_scrubEaten,10)
        # Red deer
        redDeer_reproduce = np.random.uniform(0,1)
        redDeer_gain_from_grass = np.random.uniform(0,1)
        redDeer_gain_from_Trees = np.random.uniform(0,1)
        redDeer_gain_from_Scrub = np.random.uniform(0,1)
        redDeer_gain_from_Saplings = np.random.uniform(0,1)
        redDeer_gain_from_YoungScrub = np.random.uniform(0,1)
        redDeer_impactGrass = random.randint(fallowDeer_impactGrass,100)
        redDeer_saplingsEaten = random.randint(fallowDeer_saplingsEaten,100)
        redDeer_youngScrubEaten = random.randint(fallowDeer_youngScrubEaten,100)
        redDeer_treesEaten = random.randint(fallowDeer_treesEaten,10)
        redDeer_scrubEaten = random.randint(fallowDeer_scrubEaten,10)
        # Exmoor ponies
        ponies_gain_from_grass = np.random.uniform(0,1)
        ponies_gain_from_Trees = np.random.uniform(0,1)
        ponies_gain_from_Scrub = np.random.uniform(0,1)
        ponies_gain_from_Saplings = np.random.uniform(0,1)
        ponies_gain_from_YoungScrub = np.random.uniform(0,1)
        ponies_impactGrass = random.randint(redDeer_impactGrass,100)
        ponies_saplingsEaten = random.randint(redDeer_saplingsEaten,100)
        ponies_youngScrubEaten = random.randint(redDeer_youngScrubEaten,100)
        ponies_treesEaten = random.randint(redDeer_treesEaten,10)
        ponies_scrubEaten = random.randint(redDeer_scrubEaten,10)
        # Longhorn cattle
        cows_reproduce = np.random.uniform(0,1)
        cows_gain_from_grass = np.random.uniform(0,1)
        cows_gain_from_Trees = np.random.uniform(0,1)
        cows_gain_from_Scrub = np.random.uniform(0,1)
        cows_gain_from_Saplings = np.random.uniform(0,1)
        cows_gain_from_YoungScrub = np.random.uniform(0,1)
        cows_impactGrass = random.randint(ponies_impactGrass,100)
        cows_saplingsEaten = random.randint(ponies_saplingsEaten,100)
        cows_youngScrubEaten = random.randint(ponies_youngScrubEaten,100)
        cows_treesEaten = random.randint(ponies_treesEaten,10)
        cows_scrubEaten = random.randint(ponies_scrubEaten,10)
        # Tamworth pigs
        pigs_reproduce = np.random.uniform(0,1)
        pigs_gain_from_grass = np.random.uniform(0,1)
        pigs_gain_from_Saplings = np.random.uniform(0,1)
        pigs_gain_from_YoungScrub = np.random.uniform(0,1)
        pigs_impactGrass = random.randint(cows_impactGrass,100)
        pigs_saplingsEaten = random.randint(cows_saplingsEaten,100)
        pigs_youngScrubEaten = random.randint(cows_youngScrubEaten,100)

        # keep track of my parameters
        parameters_used = [
            run_number,
            chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
            chance_scrubOutcompetedByTree, chance_grassOutcompetedByTreeScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
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
            pigs_impactGrass, pigs_saplingsEaten, pigs_youngScrubEaten 
            ]
        # append to dataframe
        final_parameters.append(parameters_used)

        # keep track of the runs
        run_number +=1
        print(run_number)
        model = KneppModel(
            chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
            chance_scrubOutcompetedByTree, chance_grassOutcompetedByTreeScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
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
        "chance_grassOutcompetedByTreeScrub",
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
    final_parameters = pd.DataFrame(data=final_parameters, columns=variables)

    # accepted runs are those that made it to year 184, plus this last filtering criteria
    all_accepted_runs = final_results[(final_results["Time"] == 185)
                                # (final_results["Roe deer"] <= 40) & (final_results["Roe deer"] >= 20)
                                # (final_results["Grassland"] <= 69) & (final_results["Grassland"] >= 49) &
                                # (final_results["Woodland"] <= 35) & (final_results["Woodland"] >= 21) &
                                # (final_results["Thorny Scrub"] <= 29) & (final_results["Thorny Scrub"] >= 9)
                                ]

    # accepted parameters
    accepted_parameters = final_parameters[final_parameters['run_number'].isin(all_accepted_runs['run_number'])]

    with pd.option_context('display.max_columns',None):
        print(final_results[(final_results["Time"] == 185)])

    with pd.option_context('display.max_rows',None, 'display.max_columns',None):
        print("accepted_years: \n", all_accepted_runs)
        
    return number_simulations, final_results, accepted_parameters, all_accepted_runs, variables

run_all_models()

# def graph_runs():
#     number_simulations, final_results, accepted_parameters, all_accepted_runs, variables = run_all_models()
#     # reshape dataframe
#     # accepted_shape = np.repeat(final_runs['accepted?'], len(8))
#     grouping_variable = np.repeat(all_accepted_runs['run_number'], len(8))
#     y_values = all_accepted_runs.drop(['run_number', 'Time'], axis=1).values.flatten()
#     species_list = np.tile(8, 185*number_simulations)
#     indices = np.repeat(all_accepted_runs['Time'],len(8))
#     final_df = pd.DataFrame(
#     {'Abundance %': y_values, 'runNumber': grouping_variable, 'Ecosystem Element': species_list, 'Time': indices})
#     # calculate median 
#     m = final_df.groupby(['Time', 'Ecosystem Element'])[['Abundance %']].apply(np.median)
#     m.name = 'Median'
#     final_df = final_df.join(m, on=['Time', 'Ecosystem Element'])
#     # calculate quantiles
#     perc1 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(.95)
#     perc1.name = 'ninetyfivePerc'
#     final_df = final_df.join(perc1, on=['Time', 'Ecosystem Element'])
#     perc2 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(.05)
#     perc2.name = "fivePerc"
#     final_df = final_df.join(perc2, on=['Time','Ecosystem Element'])

#     # graph results
#     colors = ["#6788ee", "#e26952", "#3F9E4D"]
#     g = sns.FacetGrid(final_df, col="Ecosystem Element", hue = "runType", palette = colors, col_wrap=4, sharey = False)
#     g.map(sns.lineplot, 'Time', 'Median')
#     g.map(sns.lineplot, 'Time', 'fivePerc')
#     g.map(sns.lineplot, 'Time', 'ninetyfivePerc')
#     for ax in g.axes.flat:
#         ax.fill_between(ax.lines[3].get_xdata(),ax.lines[3].get_ydata(), ax.lines[6].get_ydata(), color = '#6788ee', alpha =0.2)
#         ax.fill_between(ax.lines[4].get_xdata(),ax.lines[4].get_ydata(), ax.lines[7].get_ydata(), color = '#e26952', alpha=0.2)
#         ax.fill_between(ax.lines[5].get_xdata(),ax.lines[5].get_ydata(), ax.lines[8].get_ydata(), color = "#3F9E4D", alpha=0.2)
#         ax.set_ylabel('Abundance')
#         # ax.set_xticklabels(ax.get_xticklabels(), rotation=40)
#     # add subplot titles
#     axes = g.axes.flatten()
#     # fill between the quantiles
#     axes[0].set_title("European bison")
#     axes[1].set_title("Exmoor ponies")
#     axes[2].set_title("Fallow deer")
#     axes[3].set_title("Grassland & parkland")
#     axes[4].set_title("Longhorn cattle")
#     axes[5].set_title("Organic carbon")
#     axes[6].set_title("Red deer")
#     axes[7].set_title("Roe deer")
#     axes[8].set_title("Tamworth pigs")
#     axes[9].set_title("Thorny scrubland")
#     axes[10].set_title("Woodland")
#     # add filter lines
#     g.axes[3].vlines(x=2009,ymin=0.68,ymax=1, color='r')
#     g.axes[5].vlines(x=2009,ymin=1,ymax=2.1, color='r')
#     g.axes[7].vlines(x=2009,ymin=1,ymax=3.3, color='r')
#     g.axes[9].vlines(x=2009,ymin=1,ymax=19, color='r')
#     g.axes[10].vlines(x=2009,ymin=0.85,ymax=1.6, color='r')
#     # plot next set of filter lines
#     g.axes[3].vlines(x=2021,ymin=0.61,ymax=0.86, color='r')
#     g.axes[5].vlines(x=2021,ymin=1.7,ymax=2.2, color='r')
#     g.axes[7].vlines(x=2021,ymin=1.7,ymax=3.3, color='r')
#     g.axes[9].vlines(x=2021,ymin=19,ymax=31.9, color='r')
#     g.axes[10].vlines(x=2021,ymin=1,ymax=1.7, color='r')
#     # make sure they all start from 0
#     g.axes[4].set(ylim =(0,None))
#     g.axes[6].set(ylim =(0,None))
#     g.axes[9].set(ylim =(0,None))
#     # stop the plots from overlapping
#     plt.tight_layout()
#     plt.legend(labels=['Reintroductions', 'No reintroductions', 'European bison \n reintroduction'],bbox_to_anchor=(2.2, 0),loc='lower right', fontsize=12)
#     plt.savefig('reintroNoReintro_ps25.png')
#     # plt.show()



# calculate the time it takes to run per node, currently 8.5min for 1k runs
stop = timeit.default_timer()
print('Total time: ', (stop - start))