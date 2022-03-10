# graph the runs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from KneppModel_ABM import KneppModel 
import numpy as np
import pandas as pd
from scipy.stats import linregress


def optimizer_fails():

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
        

        # keep track of my parameters
        parameters_used = [
            run_number,
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
            pigs_impactGrass, pigs_saplingsEaten, pigs_youngScrubEaten 
            ]

        # append to dataframe
        final_parameters.append(parameters_used)

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

    # grouping variable
    grouping_variable = np.repeat(final_results['run_number'], 10)
    # y values
    y_values = final_results.drop(['run_number', 'Time'], axis=1).values.flatten()
    # species list. this should be +1 the number of simulations
    species_list = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 185*number_simulations) 
    # indices
    indices = np.repeat(final_results['Time'], 10)
    final_df = pd.DataFrame(
    {'Abundance %': y_values, 'runNumber': grouping_variable, 'Ecosystem Element': species_list, 'Time': indices})
    
    # calculate median 
    m = final_df.groupby(['Time', 'Ecosystem Element'])[['Abundance %']].apply(np.median)
    m.name = 'Median'
    final_df = final_df.join(m, on=['Time', 'Ecosystem Element'])
    # calculate quantiles
    perc1 = final_df.groupby(['Time','Ecosystem Element'])['Abundance %'].quantile(.95)
    perc1.name = 'ninetyfivePerc'
    final_df = final_df.join(perc1, on=['Time','Ecosystem Element'])
    perc2 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(.05)
    perc2.name = "fivePerc"
    final_df = final_df.join(perc2, on=['Time','Ecosystem Element'])
    colors = ["#6788ee", "#e26952", "#3F9E4D"]

    # first graph: counterfactual & forecasting
    g = sns.FacetGrid(final_df, col="Ecosystem Element", palette = colors, col_wrap=4, sharey = False)
    g.map(sns.lineplot, 'Time', 'Median')
    g.map(sns.lineplot, 'Time', 'fivePerc')
    g.map(sns.lineplot, 'Time', 'ninetyfivePerc')
    for ax in g.axes.flat:
        ax.fill_between(ax.lines[1].get_xdata(),ax.lines[1].get_ydata(), ax.lines[2].get_ydata(), color = '#6788ee', alpha =0.2)
        ax.set_ylabel('Abundance')
    # add subplot titles
    axes = g.axes.flatten()
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
    # add filter lines
    g.axes[0].vlines(x=50,ymin=6,ymax=40, color='r')
    g.axes[6].vlines(x=50,ymin=49,ymax=90, color='r')
    g.axes[7].vlines(x=50,ymin=7,ymax=27, color='r')
    g.axes[8].vlines(x=50,ymin=1,ymax=21, color='r')
    # plot post-reintro lines: April 2015
    g.axes[1].vlines(x=123,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=123,ymin=104,ymax=127, color='r')
    g.axes[5].vlines(x=123,ymin=20,ymax=24, color='r')
    # May 2015
    g.axes[3].vlines(x=124,ymin=116,ymax=142, color='r')
    g.axes[5].vlines(x=124,ymin=13,ymax=15, color='r')
    g.axes[1].vlines(x=124,ymin=9,ymax=11, color='r')
    # June 2015
    g.axes[3].vlines(x=125,ymin=116,ymax=142, color='r')
    g.axes[1].vlines(x=125,ymin=9,ymax=11, color='r')
    g.axes[5].vlines(x=125,ymin=13,ymax=15, color='r')
    # July 2015
    g.axes[3].vlines(x=126,ymin=116,ymax=142, color='r')
    g.axes[1].vlines(x=126,ymin=9,ymax=11, color='r')
    g.axes[5].vlines(x=126,ymin=13,ymax=15, color='r')
    # Aug 2015
    g.axes[3].vlines(x=127,ymin=116,ymax=142, color='r')
    g.axes[1].vlines(x=127,ymin=9,ymax=11, color='r')
    g.axes[5].vlines(x=127,ymin=13,ymax=15, color='r')
    # Sept 2015
    g.axes[3].vlines(x=128,ymin=117,ymax=143, color='r')
    g.axes[1].vlines(x=128,ymin=9,ymax=11, color='r')
    g.axes[5].vlines(x=128,ymin=13,ymax=15, color='r')
    # Oct 2015
    g.axes[3].vlines(x=129,ymin=82,ymax=100, color='r')
    g.axes[1].vlines(x=129,ymin=9,ymax=11, color='r')
    g.axes[5].vlines(x=129,ymin=13,ymax=15, color='r')
    # Nov 2015
    g.axes[3].vlines(x=130,ymin=82,ymax=100, color='r')
    g.axes[1].vlines(x=130,ymin=9,ymax=11, color='r')
    g.axes[5].vlines(x=130,ymin=12,ymax=14, color='r')
    # Dec 2015
    g.axes[3].vlines(x=131,ymin=77,ymax=94, color='r')
    g.axes[1].vlines(x=131,ymin=9,ymax=11, color='r')
    g.axes[5].vlines(x=131,ymin=12,ymax=14, color='r')
    # Jan 2016
    g.axes[3].vlines(x=132,ymin=77,ymax=94, color='r')
    g.axes[1].vlines(x=132,ymin=9,ymax=11, color='r')
    g.axes[5].vlines(x=132,ymin=9,ymax=11, color='r')
    # Feb 2016
    g.axes[1].vlines(x=133,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=133,ymin=77,ymax=94, color='r')
    g.axes[5].vlines(x=133,ymin=7,ymax=9, color='r')
    # March 2016
    g.axes[1].vlines(x=134,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=134,ymin=77,ymax=94, color='r')
    g.axes[2].vlines(x=134,ymin=126,ymax=154, color='r')
    g.axes[4].vlines(x=134,ymin=23,ymax=29, color='r')
    g.axes[5].vlines(x=134,ymin=8,ymax=10, color='r')
    # April 2016
    g.axes[1].vlines(x=135,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=135,ymin=93,ymax=113, color='r')
    g.axes[5].vlines(x=135,ymin=8,ymax=10, color='r')
    # May 2016
    g.axes[1].vlines(x=136,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=136,ymin=97,ymax=119, color='r')
    g.axes[5].vlines(x=136,ymin=15,ymax=19, color='r')
    # June 2016
    g.axes[1].vlines(x=137,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=137,ymin=80,ymax=98, color='r')
    g.axes[5].vlines(x=137,ymin=15,ymax=19, color='r')
    # July 2016
    g.axes[1].vlines(x=138,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=138,ymin=78,ymax=96, color='r')
    g.axes[5].vlines(x=138,ymin=15,ymax=19, color='r')
    # Aug 2016
    g.axes[1].vlines(x=139,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=139,ymin=78,ymax=96, color='r')
    g.axes[5].vlines(x=139,ymin=15,ymax=19, color='r')
    # Sept 2016
    g.axes[1].vlines(x=140,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=140,ymin=87,ymax=107, color='r')
    g.axes[5].vlines(x=140,ymin=15,ymax=19, color='r')
    # Oct 2016
    g.axes[1].vlines(x=141,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=141,ymin=87,ymax=107, color='r')
    g.axes[5].vlines(x=141,ymin=15,ymax=19, color='r')
    # Nov 2016
    g.axes[1].vlines(x=142,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=142,ymin=83,ymax=101, color='r')
    g.axes[5].vlines(x=142,ymin=15,ymax=19, color='r')
    # Dec 2016
    g.axes[1].vlines(x=143,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=143,ymin=71,ymax=87, color='r')
    g.axes[5].vlines(x=143,ymin=12,ymax=14, color='r')
    # Jan 2017
    g.axes[1].vlines(x=144,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=144,ymin=71,ymax=87, color='r')
    g.axes[5].vlines(x=144,ymin=8,ymax=10, color='r')
    # Feb 2017
    g.axes[1].vlines(x=145,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=145,ymin=71,ymax=87, color='r')
    g.axes[5].vlines(x=145,ymin=6,ymax=8, color='r')
    # March 2017
    g.axes[1].vlines(x=146,ymin=9,ymax=11, color='r')
    g.axes[2].vlines(x=146,ymin=149,ymax=182, color='r')
    g.axes[3].vlines(x=146,ymin=71,ymax=87, color='r')
    g.axes[5].vlines(x=146,ymin=6,ymax=8, color='r')
    # April 2017
    g.axes[1].vlines(x=147,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=147,ymin=90,ymax=110, color='r')
    g.axes[5].vlines(x=147,ymin=20,ymax=24, color='r')
    # May 2017
    g.axes[1].vlines(x=148,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=148,ymin=98,ymax=120, color='r')
    g.axes[5].vlines(x=148,ymin=20,ymax=24, color='r')
    # June 2017
    g.axes[1].vlines(x=149,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=149,ymin=85,ymax=103, color='r')
    g.axes[5].vlines(x=149,ymin=20,ymax=24, color='r')
    # July 2017
    g.axes[1].vlines(x=150,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=150,ymin=85,ymax=103, color='r')
    g.axes[5].vlines(x=150,ymin=20,ymax=24, color='r')
    # Aug 2017
    g.axes[1].vlines(x=151,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=151,ymin=85,ymax=103, color='r')
    g.axes[5].vlines(x=151,ymin=20,ymax=24, color='r')
    # Sept 2017
    g.axes[1].vlines(x=152,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=152,ymin=81,ymax=99, color='r')
    g.axes[5].vlines(x=152,ymin=20,ymax=24, color='r')
    # Oct 2017
    g.axes[1].vlines(x=153,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=153,ymin=79,ymax=97, color='r')
    g.axes[5].vlines(x=153,ymin=20,ymax=24, color='r')
    # Nov 2017
    g.axes[1].vlines(x=154,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=154,ymin=79,ymax=97, color='r')
    g.axes[5].vlines(x=154,ymin=20,ymax=24, color='r')
    # Dec 2017
    g.axes[1].vlines(x=155,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=155,ymin=79,ymax=97, color='r')
    g.axes[5].vlines(x=155,ymin=16,ymax=20, color='r')
    # Jan 2018
    g.axes[1].vlines(x=156,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=156,ymin=79,ymax=97, color='r')
    g.axes[5].vlines(x=156,ymin=10,ymax=12, color='r')
    # Feb 2018
    g.axes[1].vlines(x=157,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=157,ymin=79,ymax=97, color='r')
    g.axes[5].vlines(x=157,ymin=14,ymax=18, color='r')
    # March 2018
    g.axes[1].vlines(x=158,ymin=8,ymax=10, color='r')
    g.axes[2].vlines(x=158,ymin=226,ymax=276, color='r')
    g.axes[3].vlines(x=158,ymin=79,ymax=97, color='r')
    g.axes[4].vlines(x=158,ymin=22,ymax=26, color='r')
    g.axes[5].vlines(x=158,ymin=14,ymax=18, color='r')
    # April 2018
    g.axes[1].vlines(x=159,ymin=8,ymax=10, color='r')
    g.axes[3].vlines(x=159,ymin=91,ymax=111, color='r')
    g.axes[5].vlines(x=159,ymin=14,ymax=18, color='r')
    # May 2018
    g.axes[1].vlines(x=160,ymin=8,ymax=10, color='r')
    g.axes[3].vlines(x=160,ymin=105,ymax=129, color='r')
    g.axes[5].vlines(x=160,ymin=21,ymax=25, color='r')
    # June 2018
    g.axes[1].vlines(x=161,ymin=8,ymax=10, color='r')
    g.axes[3].vlines(x=161,ymin=93,ymax=113, color='r')
    g.axes[5].vlines(x=161,ymin=21,ymax=25, color='r')
    # July 2018
    g.axes[1].vlines(x=162,ymin=8,ymax=10, color='r')
    g.axes[3].vlines(x=162,ymin=93,ymax=113, color='r')
    g.axes[5].vlines(x=162,ymin=20,ymax=24, color='r')
    # Aug 2018
    g.axes[3].vlines(x=163,ymin=92,ymax=112, color='r')
    g.axes[5].vlines(x=163,ymin=20,ymax=24, color='r')
    # Sept 2018
    g.axes[3].vlines(x=164,ymin=95,ymax=117, color='r')
    g.axes[5].vlines(x=164,ymin=20,ymax=24, color='r')
    # Oct 2018
    g.axes[3].vlines(x=165,ymin=91,ymax=111, color='r')
    g.axes[5].vlines(x=165,ymin=19,ymax=23, color='r')
    # Nov 2018
    g.axes[3].vlines(x=166,ymin=84,ymax=102, color='r')
    g.axes[5].vlines(x=166,ymin=8,ymax=10, color='r')
    # Dec 2018
    g.axes[3].vlines(x=167,ymin=80,ymax=98, color='r')
    g.axes[5].vlines(x=167,ymin=8,ymax=10, color='r')
    # Jan 2019
    g.axes[3].vlines(x=168,ymin=80,ymax=98, color='r')
    g.axes[5].vlines(x=168,ymin=8,ymax=10, color='r')
    # Feb 2019
    g.axes[3].vlines(x=169,ymin=78,ymax=96, color='r')
    g.axes[5].vlines(x=169,ymin=9,ymax=11, color='r')
    # March 2019
    g.axes[2].vlines(x=170,ymin=250,ymax=306, color='r')
    g.axes[3].vlines(x=170,ymin=78,ymax=96, color='r')
    g.axes[4].vlines(x=170,ymin=33,ymax=41, color='r')
    g.axes[5].vlines(x=170,ymin=8,ymax=10, color='r')
    # April 2019
    g.axes[3].vlines(x=171,ymin=91,ymax=111, color='r')
    g.axes[5].vlines(x=171,ymin=7,ymax=9, color='r')
    # May 2019
    g.axes[3].vlines(x=172,ymin=99,ymax=121, color='r')
    g.axes[5].vlines(x=172,ymin=7,ymax=9, color='r')
    # June 2019
    g.axes[3].vlines(x=173,ymin=80,ymax=98, color='r')
    g.axes[5].vlines(x=173,ymin=7,ymax=9, color='r')
    # July 2019
    g.axes[3].vlines(x=174,ymin=82,ymax=100, color='r')
    g.axes[5].vlines(x=174,ymin=8,ymax=10, color='r')
    # Aug 2019
    g.axes[3].vlines(x=175,ymin=82,ymax=100, color='r')
    g.axes[5].vlines(x=175,ymin=8,ymax=10, color='r')  
    # Sept 2019
    g.axes[3].vlines(x=176,ymin=84,ymax=102, color='r')
    g.axes[5].vlines(x=176,ymin=8,ymax=10, color='r')
    # Oct 2019
    g.axes[3].vlines(x=177,ymin=79,ymax=97, color='r')
    g.axes[5].vlines(x=177,ymin=8,ymax=10, color='r')
    # Nov 2019
    g.axes[3].vlines(x=178,ymin=78,ymax=96, color='r')
    g.axes[5].vlines(x=178,ymin=8,ymax=10, color='r')
    # Dec 2019
    g.axes[3].vlines(x=179,ymin=72,ymax=88, color='r')
    g.axes[5].vlines(x=179,ymin=9,ymax=11, color='r')
    # Jan 2020
    g.axes[3].vlines(x=180,ymin=72,ymax=88, color='r')
    g.axes[5].vlines(x=180,ymin=9,ymax=11, color='r')
    # Feb 2020
    g.axes[3].vlines(x=181,ymin=71,ymax=87, color='r')
    g.axes[5].vlines(x=181,ymin=7,ymax=9, color='r')
    # March 2020
    g.axes[2].vlines(x=182,ymin=222,ymax=272, color='r')
    g.axes[4].vlines(x=182,ymin=32,ymax=39, color='r')
    g.axes[3].vlines(x=182,ymin=73,ymax=89, color='r')
    g.axes[5].vlines(x=182,ymin=6,ymax=8, color='r')
    # April 2020
    g.axes[1].vlines(x=183,ymin=14,ymax=17, color='r')
    g.axes[3].vlines(x=183,ymin=73,ymax=89, color='r')
    g.axes[5].vlines(x=183,ymin=6,ymax=8, color='r')
    # plot next set of filter lines
    g.axes[0].vlines(x=184,ymin=20,ymax=40, color='r')
    g.axes[1].vlines(x=184,ymin=14,ymax=17, color='r')
    g.axes[3].vlines(x=184,ymin=73,ymax=89, color='r')
    g.axes[5].vlines(x=184,ymin=17,ymax=21, color='r')
    g.axes[6].vlines(x=184,ymin=49,ymax=69, color='r')
    g.axes[7].vlines(x=184,ymin=9,ymax=29, color='r')
    g.axes[8].vlines(x=184,ymin=21,ymax=35, color='r')

    # stop the plots from overlapping
    plt.tight_layout()
    plt.savefig('optimizerFails_extended.png')
    plt.show()


    # SENSITIVITY TEST
    sensitivity_results_list = []
    sensitivity_parameters = []
    run_number  = 0
    # choose my percent above/below number
    perc_aboveBelow = [-0.025, -0.01,-0.005, 0, 0.005, 0.01, 0.025]
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
            roeDeer_impactGrass = final_parameters_temp.values[22]
            roeDeer_saplingsEaten = final_parameters_temp.values[23]
            roeDeer_youngScrubEaten = final_parameters_temp.values[24]
            roeDeer_treesEaten = final_parameters_temp.values[25]
            roeDeer_scrubEaten = final_parameters_temp.values[26]
            ponies_gain_from_grass = final_parameters_temp.values[27]
            ponies_gain_from_Trees = final_parameters_temp.values[28]
            ponies_gain_from_Scrub = final_parameters_temp.values[29]
            ponies_gain_from_Saplings = final_parameters_temp.values[30]
            ponies_gain_from_YoungScrub = final_parameters_temp.values[31]
            ponies_impactGrass = final_parameters_temp.values[32]
            ponies_saplingsEaten = final_parameters_temp.values[33]
            ponies_youngScrubEaten = final_parameters_temp.values[34]
            ponies_treesEaten = final_parameters_temp.values[35]
            ponies_scrubEaten = final_parameters_temp.values[36]
            cows_reproduce = final_parameters_temp.values[37]
            cows_gain_from_grass = final_parameters_temp.values[38]
            cows_gain_from_Trees = final_parameters_temp.values[39]
            cows_gain_from_Scrub = final_parameters_temp.values[40]
            cows_gain_from_Saplings = final_parameters_temp.values[41]
            cows_gain_from_YoungScrub = final_parameters_temp.values[42]
            cows_impactGrass = final_parameters_temp.values[43]
            cows_saplingsEaten = final_parameters_temp.values[44]
            cows_youngScrubEaten = final_parameters_temp.values[45]
            cows_treesEaten = final_parameters_temp.values[46]
            cows_scrubEaten = final_parameters_temp.values[47]
            fallowDeer_reproduce = final_parameters_temp.values[48]
            fallowDeer_gain_from_grass = final_parameters_temp.values[49]
            fallowDeer_gain_from_Trees = final_parameters_temp.values[50]
            fallowDeer_gain_from_Scrub = final_parameters_temp.values[51]
            fallowDeer_gain_from_Saplings = final_parameters_temp.values[52]
            fallowDeer_gain_from_YoungScrub = final_parameters_temp.values[53]
            fallowDeer_impactGrass = final_parameters_temp.values[54]
            fallowDeer_saplingsEaten = final_parameters_temp.values[55]
            fallowDeer_youngScrubEaten = final_parameters_temp.values[56]
            fallowDeer_treesEaten = final_parameters_temp.values[57]
            fallowDeer_scrubEaten = final_parameters_temp.values[58]
            redDeer_reproduce = final_parameters_temp.values[59]
            redDeer_gain_from_grass = final_parameters_temp.values[60]
            redDeer_gain_from_Trees = final_parameters_temp.values[61]
            redDeer_gain_from_Scrub = final_parameters_temp.values[62]
            redDeer_gain_from_Saplings = final_parameters_temp.values[63]
            redDeer_gain_from_YoungScrub = final_parameters_temp.values[64]
            redDeer_impactGrass = final_parameters_temp.values[65]
            redDeer_saplingsEaten = final_parameters_temp.values[66]
            redDeer_youngScrubEaten = final_parameters_temp.values[67]
            redDeer_treesEaten = final_parameters_temp.values[68]
            redDeer_scrubEaten = final_parameters_temp.values[69]
            pigs_reproduce = final_parameters_temp.values[70]
            pigs_gain_from_grass = final_parameters_temp.values[71]
            pigs_gain_from_Saplings = final_parameters_temp.values[72]
            pigs_gain_from_YoungScrub = final_parameters_temp.values[73]
            pigs_impactGrass = final_parameters_temp.values[74]
            pigs_saplingsEaten = final_parameters_temp.values[75]
            pigs_youngScrubEaten = final_parameters_temp.values[76]

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
            sensitivity_results_unfiltered = model_2.datacollector.get_model_vars_dataframe()
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
    merged_dfs.to_excel("all_parameter_changes.xlsx")

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
    plt.savefig('sensitivity_roe.png')
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
    plt.savefig('sensitivity_fallow.png')
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
    plt.savefig('sensitivity_red.png')
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
    plt.savefig('sensitivity_cattle.png')
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
    plt.savefig('sensitivity_pig.png')
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
    plt.savefig('sensitivity_pony.png')
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
    plt.savefig('sensitivity_grass.png')
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
    plt.savefig('sensitivity_scrub.png')
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
    plt.savefig('sensitivity_woodland.png')
    plt.show()


optimizer_fails()