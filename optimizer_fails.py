# graph the runs
from typing import final
from run_experiments import run_counterfactual
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from KneppModel_ABM import KneppModel 
from geneticAlgorithm import run_optimizer
import numpy as np
import random
import pandas as pd
from scipy.stats import linregress



def optimizer_fails():
    output_parameters = run_optimizer()

    # define number of simulations
    number_simulations =  1
    # make list of variables
    final_results_list = []
    final_parameters = []
    run_number = 0

    # choose my percent above/below number
    perc_aboveBelow = [-0.05, 0, 0.05]

    for _ in range(number_simulations):
        # keep track of the runs
        run_number +=1
        print(run_number)
        # choose my parameters 
        initial_roeDeer = random.randint(6, 18)
        initial_grassland = random.randint(75, 85)
        initial_woodland = random.randint(9, 19)
        initial_scrubland = random.randint(0, 6)

        # habitats
        chance_reproduceSapling = output_parameters["variable"][0]
        chance_reproduceYoungScrub = output_parameters["variable"][1]
        chance_regrowGrass = output_parameters["variable"][2]
        chance_saplingBecomingTree = output_parameters["variable"][3]
        chance_youngScrubMatures = output_parameters["variable"][4]
        chance_scrubOutcompetedByTree = output_parameters["variable"][5]
        chance_grassOutcompetedByTree = output_parameters["variable"][6]
        chance_grassOutcompetedByScrub = output_parameters["variable"][7]
        chance_saplingOutcompetedByTree = output_parameters["variable"][8]
        chance_saplingOutcompetedByScrub = output_parameters["variable"][9]
        chance_youngScrubOutcompetedByScrub = output_parameters["variable"][10]
        chance_youngScrubOutcompetedByTree = output_parameters["variable"][11]
        # roe deer
        roeDeer_reproduce = output_parameters["variable"][12]
        roeDeer_gain_from_grass = output_parameters["variable"][13]
        roeDeer_gain_from_Trees = output_parameters["variable"][14]
        roeDeer_gain_from_Scrub = output_parameters["variable"][15]
        roeDeer_gain_from_Saplings = output_parameters["variable"][16]
        roeDeer_gain_from_YoungScrub = output_parameters["variable"][17]
        # Fallow deer
        fallowDeer_reproduce = output_parameters["variable"][18]
        fallowDeer_gain_from_grass = output_parameters["variable"][19]
        fallowDeer_gain_from_Trees = output_parameters["variable"][20]
        fallowDeer_gain_from_Scrub = output_parameters["variable"][21]
        fallowDeer_gain_from_Saplings = output_parameters["variable"][22]
        fallowDeer_gain_from_YoungScrub = output_parameters["variable"][23]
         # Red deer
        redDeer_reproduce = output_parameters["variable"][24]
        redDeer_gain_from_grass = output_parameters["variable"][25]
        redDeer_gain_from_Trees = output_parameters["variable"][26]
        redDeer_gain_from_Scrub = output_parameters["variable"][27]
        redDeer_gain_from_Saplings = output_parameters["variable"][28]
        redDeer_gain_from_YoungScrub = output_parameters["variable"][29]
        # Exmoor ponies
        ponies_gain_from_grass = output_parameters["variable"][30]
        ponies_gain_from_Trees = output_parameters["variable"][31]
        ponies_gain_from_Scrub = output_parameters["variable"][32]
        ponies_gain_from_Saplings = output_parameters["variable"][33]
        ponies_gain_from_YoungScrub = output_parameters["variable"][34]
        # Longhorn cattle
        cows_reproduce = output_parameters["variable"][35]
        cows_gain_from_grass = output_parameters["variable"][36]
        cows_gain_from_Trees = output_parameters["variable"][37]
        cows_gain_from_Scrub = output_parameters["variable"][38]
        cows_gain_from_Saplings = output_parameters["variable"][39]
        cows_gain_from_YoungScrub = output_parameters["variable"][40]
        # Tamworth pigs
        pigs_reproduce = output_parameters["variable"][41]
        pigs_gain_from_grass = output_parameters["variable"][42]
        pigs_gain_from_Saplings = output_parameters["variable"][43]
        pigs_gain_from_YoungScrub = output_parameters["variable"][44]
        # impact grass
        roeDeer_impactGrass = round(output_parameters["variable"][45])
        fallowDeer_impactGrass = round(output_parameters["variable"][46])
        redDeer_impactGrass = round(output_parameters["variable"][47])
        ponies_impactGrass = round(output_parameters["variable"][48])
        cows_impactGrass = round(output_parameters["variable"][49])
        pigs_impactGrass = round(output_parameters["variable"][50])
        # impact saplings
        roeDeer_saplingsEaten = round(output_parameters["variable"][51])
        fallowDeer_saplingsEaten = round(output_parameters["variable"][52])
        redDeer_saplingsEaten = round(output_parameters["variable"][53])
        ponies_saplingsEaten = round(output_parameters["variable"][54])
        cows_saplingsEaten =  round(output_parameters["variable"][55])
        pigs_saplingsEaten = round(output_parameters["variable"][56])
        # impact young scrub
        roeDeer_youngScrubEaten = round(output_parameters["variable"][57])
        fallowDeer_youngScrubEaten = round(output_parameters["variable"][58])
        redDeer_youngScrubEaten = round(output_parameters["variable"][59])
        ponies_youngScrubEaten = round(output_parameters["variable"][60])
        cows_youngScrubEaten = round(output_parameters["variable"][61])
        pigs_youngScrubEaten = round(output_parameters["variable"][62])
        # impact scrub
        roeDeer_scrubEaten = round(output_parameters["variable"][63])
        fallowDeer_scrubEaten = round(output_parameters["variable"][64])
        redDeer_scrubEaten = round(output_parameters["variable"][65])
        ponies_scrubEaten = round(output_parameters["variable"][66])
        cows_scrubEaten = round(output_parameters["variable"][67])
        # impact trees
        roeDeer_treesEaten = round(output_parameters["variable"][68])
        fallowDeer_treesEaten = round(output_parameters["variable"][69])
        redDeer_treesEaten = round(output_parameters["variable"][70])
        ponies_treesEaten = round(output_parameters["variable"][71])
        cows_treesEaten =  round(output_parameters["variable"][72])

        
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
    plt.savefig('optimizerFails.png')
    plt.show()


    # SENSITIVITY TEST
    sensitivity_results_list = []
    sensitivity_parameters = []
    run_number  = 0
    # choose my percent above/below number
    perc_aboveBelow = [-0.05, 0.05, 0]
    # choose my percent above/below number
    final_parameters = final_parameters.iloc[0,1:78]
    # organized = final_parameters.iloc[0:5]
    # loop through each one, changing one cell at a time
    for index, row in final_parameters.iteritems():
        for perc_number in perc_aboveBelow:
            run_number += 1
            ifor_val = row + (row*perc_number)
            # make sure they're ints where applicable
            if ifor_val > 1:
                ifor_val = round(ifor_val)
            print(run_number, final_parameters.at[index])
            final_parameters.at[index] = ifor_val
            # choose my parameters 
            chance_reproduceSapling = final_parameters.values[0]
            chance_reproduceYoungScrub = final_parameters.values[1]
            chance_regrowGrass = final_parameters.values[2]
            chance_saplingBecomingTree = final_parameters.values[3]
            chance_youngScrubMatures = final_parameters.values[4]
            chance_scrubOutcompetedByTree = final_parameters.values[5]
            chance_grassOutcompetedByTree = final_parameters.values[6]
            chance_grassOutcompetedByScrub = final_parameters.values[7]
            chance_saplingOutcompetedByTree = final_parameters.values[8]
            chance_saplingOutcompetedByScrub = final_parameters.values[9]
            chance_youngScrubOutcompetedByScrub = final_parameters.values[10]
            chance_youngScrubOutcompetedByTree = final_parameters.values[11]
            initial_roeDeer = int(final_parameters.values[12])
            initial_grassland = int(final_parameters.values[13])
            initial_woodland = int(final_parameters.values[14])
            initial_scrubland = int(final_parameters.values[15])
            roeDeer_reproduce = final_parameters.values[16]
            roeDeer_gain_from_grass = final_parameters.values[17]
            roeDeer_gain_from_Trees = final_parameters.values[18]
            roeDeer_gain_from_Scrub = final_parameters.values[19]
            roeDeer_gain_from_Saplings = final_parameters.values[20]
            roeDeer_gain_from_YoungScrub = final_parameters.values[21]
            roeDeer_impactGrass = final_parameters.values[22]
            roeDeer_saplingsEaten = final_parameters.values[23]
            roeDeer_youngScrubEaten = final_parameters.values[24]
            roeDeer_treesEaten = final_parameters.values[25]
            roeDeer_scrubEaten = final_parameters.values[26]
            ponies_gain_from_grass = final_parameters.values[27]
            ponies_gain_from_Trees = final_parameters.values[28]
            ponies_gain_from_Scrub = final_parameters.values[29]
            ponies_gain_from_Saplings = final_parameters.values[30]
            ponies_gain_from_YoungScrub = final_parameters.values[31]
            ponies_impactGrass = final_parameters.values[32]
            ponies_saplingsEaten = final_parameters.values[33]
            ponies_youngScrubEaten = final_parameters.values[34]
            ponies_treesEaten = final_parameters.values[35]
            ponies_scrubEaten = final_parameters.values[36]
            cows_reproduce = final_parameters.values[37]
            cows_gain_from_grass = final_parameters.values[38]
            cows_gain_from_Trees = final_parameters.values[39]
            cows_gain_from_Scrub = final_parameters.values[40]
            cows_gain_from_Saplings = final_parameters.values[41]
            cows_gain_from_YoungScrub = final_parameters.values[42]
            cows_impactGrass = final_parameters.values[43]
            cows_saplingsEaten = final_parameters.values[44]
            cows_youngScrubEaten = final_parameters.values[45]
            cows_treesEaten = final_parameters.values[46]
            cows_scrubEaten = final_parameters.values[47]
            fallowDeer_reproduce = final_parameters.values[48]
            fallowDeer_gain_from_grass = final_parameters.values[49]
            fallowDeer_gain_from_Trees = final_parameters.values[50]
            fallowDeer_gain_from_Scrub = final_parameters.values[51]
            fallowDeer_gain_from_Saplings = final_parameters.values[52]
            fallowDeer_gain_from_YoungScrub = final_parameters.values[53]
            fallowDeer_impactGrass = final_parameters.values[54]
            fallowDeer_saplingsEaten = final_parameters.values[55]
            fallowDeer_youngScrubEaten = final_parameters.values[56]
            fallowDeer_treesEaten = final_parameters.values[57]
            fallowDeer_scrubEaten = final_parameters.values[58]
            redDeer_reproduce = final_parameters.values[59]
            redDeer_gain_from_grass = final_parameters.values[60]
            redDeer_gain_from_Trees = final_parameters.values[61]
            redDeer_gain_from_Scrub = final_parameters.values[62]
            redDeer_gain_from_Saplings = final_parameters.values[63]
            redDeer_gain_from_YoungScrub = final_parameters.values[64]
            redDeer_impactGrass = final_parameters.values[65]
            redDeer_saplingsEaten = final_parameters.values[66]
            redDeer_youngScrubEaten = final_parameters.values[67]
            redDeer_treesEaten = final_parameters.values[68]
            redDeer_scrubEaten = final_parameters.values[69]
            pigs_reproduce = final_parameters.values[70]
            pigs_gain_from_grass = final_parameters.values[71]
            pigs_gain_from_Saplings = final_parameters.values[72]
            pigs_gain_from_YoungScrub = final_parameters.values[73]
            pigs_impactGrass = final_parameters.values[74]
            pigs_saplingsEaten = final_parameters.values[75]
            pigs_youngScrubEaten = final_parameters.values[76]

            my_parameters = [chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
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
            pigs_impactGrass, pigs_saplingsEaten, pigs_youngScrubEaten]

            # run model
            model_2 = KneppModel(
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
            model_2.run_model()

            # remember the results of the model (dominant conditions, # of agents)
            sensitivity_results = model_2.datacollector.get_model_vars_dataframe()
            sensitivity_results_list.append(sensitivity_results)
            # and the parameters used
            sensitivity_parameters.append(my_parameters)

    # append to dataframe
    final_sensitivity_results = pd.concat(sensitivity_results_list)
    final_sensitivity_parameters = pd.DataFrame(data=sensitivity_parameters, columns=variables[1:78])
    print("params", final_sensitivity_parameters)
    final_sensitivity_results = final_sensitivity_results[(final_sensitivity_results["Time"] == 184)]
    final_sensitivity_results = final_sensitivity_results.reset_index(drop=True)
    merged_dfs = pd.concat([final_sensitivity_parameters, final_sensitivity_results], axis=1)

    # print(merged_dfs) 3 * paraneters x 88 cols

    # ROE DEER
    roe_gradients = []
    column_names = []
    column_values = []
    populations = []
    gradients = []
    
    # find the gradient
    for column in merged_dfs.iloc[:,0:77]:
        res = linregress(merged_dfs[column], merged_dfs["Roe deer"])
        roe_gradient = [column, res.slope]
        roe_gradients.append(roe_gradient)
        # append column name & values, populations and gradients 
        column_names.append([column]*3*77)
         #  print("column names", [column]*3) len = 3
        column_values.append(merged_dfs[column].to_list())
        #  print("values", merged_dfs[column].to_list()) len = 3 * parameters
        populations.append(merged_dfs["Roe deer"].to_list())
        #  print('pop', merged_dfs["Roe deer"].to_list()) len = 3 x parameters 
        gradients.append([res.slope]*3*77)

    # organize the data
    roe_gradients = pd.DataFrame(data=roe_gradients, columns = ['Parameter name', 'Gradient'])
    all_values_roe = pd.DataFrame()
    flat_column_names = [item for sublist in column_names for item in sublist]
    flat_column_values = [item for sublist in column_values for item in sublist]
    flat_populations = [item for sublist in populations for item in sublist]
    flat_gradients = [item for sublist in gradients for item in sublist]
    all_values_roe['Parameter_names'] = flat_column_names
    all_values_roe['Parameter_values'] = flat_column_values
    all_values_roe['Population'] = flat_populations
    all_values_roe['Gradient'] = flat_gradients
    # take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
    roe_gradients['Gradient'] = roe_gradients['Gradient'].abs()
    roe_gradients = roe_gradients.sort_values(['Gradient'], ascending=[False])
    top_ten = roe_gradients.iloc[0:10,:]
    print(top_ten)
    top_ten_combined = all_values_roe.where(all_values_roe.Parameter_names.isin(top_ten['Parameter name']))
    top_ten_combined = top_ten_combined[top_ten_combined['Parameter_names'].notna()]
    print(top_ten_combined)
    top_ten_combined.to_excel("final_df_gradients_roeDeer.xlsx")
    # graph it
    ro = sns.relplot(data=top_ten_combined, x='Parameter_values', y='Population', col='Parameter_names', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
    ro.fig.suptitle('Roe deer gradients')
    plt.tight_layout()
    plt.savefig('sensitivity_roe.png')
    plt.show()


    # # FALLOW DEER
    fallow_gradients = []
    column_names_fallow = []
    column_values_fallow = []
    populations_fallow = []
    gradients_fallow = []
    
    # find the gradient
    for column in merged_dfs.iloc[:,0:77]:
        res = linregress(merged_dfs[column], merged_dfs["Fallow deer"])
        fallow_gradient = [column, res.slope]
        fallow_gradients.append(fallow_gradient)
        # append column name & values, populations and gradients 
        column_names_fallow.append([column]*3*77)
        column_values_fallow.append(merged_dfs[column].to_list())
        populations_fallow.append(merged_dfs["Fallow deer"].to_list())
        gradients_fallow.append([res.slope]*3*77)

    # organize the data
    fallow_gradients = pd.DataFrame(data=fallow_gradients, columns = ['Parameter name', 'Gradient'])
    all_values_fallow = pd.DataFrame()
    flat_column_names_fallow = [item for sublist in column_names_fallow for item in sublist]
    flat_column_values_fallow = [item for sublist in column_values_fallow for item in sublist]
    flat_populations_fallow = [item for sublist in populations_fallow for item in sublist]
    flat_gradients_fallow = [item for sublist in gradients_fallow for item in sublist]
    all_values_fallow['Parameter_names'] = flat_column_names_fallow
    all_values_fallow['Parameter_values'] = flat_column_values_fallow
    all_values_fallow['Population'] = flat_populations_fallow
    all_values_fallow['Gradient'] = flat_gradients_fallow
    # take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
    fallow_gradients['Gradient'] = fallow_gradients['Gradient'].abs()
    fallow_gradients = fallow_gradients.sort_values(['Gradient'], ascending=[False])
    top_ten_fallow = fallow_gradients.iloc[0:10,:]
    print(top_ten_fallow)
    top_ten_combined_fallow = all_values_fallow.where(all_values_fallow.Parameter_names.isin(top_ten_fallow['Parameter name']))
    top_ten_combined_fallow = top_ten_combined_fallow[top_ten_combined_fallow['Parameter_names'].notna()]
    print(top_ten_combined_fallow)
    top_ten_combined_fallow.to_excel("final_df_gradients_fallowDeer.xlsx")
    # graph it
    f = sns.relplot(data=top_ten_combined_fallow, x='Parameter_values', y='Population', col='Parameter_names', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
    f.fig.suptitle('Fallow deer gradients')
    plt.tight_layout()
    plt.savefig('sensitivity_fallow.png')
    plt.show()


    # # RED DEER
    red_gradients = []
    column_names_red = []
    column_values_red = []
    populations_red = []
    gradients_red = []
    
    # find the gradient
    for column in merged_dfs.iloc[:,0:77]:
        res = linregress(merged_dfs[column], merged_dfs["Red deer"])
        red_gradient = [column, res.slope]
        red_gradients.append(red_gradient)
        # append column name & values, populations and gradients 
        column_names_red.append([column]*3*77)
        column_values_red.append(merged_dfs[column].to_list())
        populations_red.append(merged_dfs["Red deer"].to_list())
        gradients_red.append([res.slope]*3*77)

    # organize the data
    red_gradients = pd.DataFrame(data=red_gradients, columns = ['Parameter name', 'Gradient'])
    all_values_red = pd.DataFrame()
    flat_column_names_red = [item for sublist in column_names_red for item in sublist]
    flat_column_values_red = [item for sublist in column_values_red for item in sublist]
    flat_populations_red = [item for sublist in populations_red for item in sublist]
    flat_gradients_red = [item for sublist in gradients_red for item in sublist]
    all_values_red['Parameter_names'] = flat_column_names_red
    all_values_red['Parameter_values'] = flat_column_values_red
    all_values_red['Population'] = flat_populations_red
    all_values_red['Gradient'] = flat_gradients_red
    # take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
    red_gradients['Gradient'] = red_gradients['Gradient'].abs()
    red_gradients = red_gradients.sort_values(['Gradient'], ascending=[False])
    top_ten_red = red_gradients.iloc[0:10,:]
    print(top_ten_red)
    top_ten_combined_red = all_values_red.where(all_values_red.Parameter_names.isin(top_ten_red['Parameter name']))
    top_ten_combined_red = top_ten_combined_red[top_ten_combined_red['Parameter_names'].notna()]
    print(top_ten_combined_red)
    top_ten_combined_red.to_excel("final_df_gradients_redDeer.xlsx")
    # graph it
    r = sns.relplot(data=top_ten_combined_red, x='Parameter_values', y='Population', col='Parameter_names', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
    r.fig.suptitle('Red deer gradients')
    plt.tight_layout()
    plt.savefig('sensitivity_red.png')
    plt.show()



    # # LONGHORN CATTLE
    cattle_gradients = []
    column_names_cattle = []
    column_values_cattle= []
    populations_cattle = []
    gradients_cattle = []
    
    # find the gradient
    for column in merged_dfs.iloc[:,0:77]:
        res = linregress(merged_dfs[column], merged_dfs["Longhorn cattle"])
        cattle_gradient = [column, res.slope]
        cattle_gradients.append(cattle_gradient)
        # append column name & values, populations and gradients 
        column_names_cattle.append([column]*3*77)
        column_values_cattle.append(merged_dfs[column].to_list())
        populations_cattle.append(merged_dfs["Longhorn cattle"].to_list())
        gradients_cattle.append([res.slope]*3*77)

    # organize the data
    cattle_gradients = pd.DataFrame(data=cattle_gradients, columns = ['Parameter name', 'Gradient'])
    all_values_cattle = pd.DataFrame()
    flat_column_names_cattle = [item for sublist in column_names_cattle for item in sublist]
    flat_column_values_cattle= [item for sublist in column_values_cattle for item in sublist]
    flat_populations_cattle = [item for sublist in populations_cattle for item in sublist]
    flat_gradients_cattle = [item for sublist in gradients_cattle for item in sublist]
    all_values_cattle['Parameter_names'] = flat_column_names_cattle
    all_values_cattle['Parameter_values'] = flat_column_values_cattle
    all_values_cattle['Population'] = flat_populations_cattle
    all_values_cattle['Gradient'] = flat_gradients_cattle
    # take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
    cattle_gradients['Gradient'] = cattle_gradients['Gradient'].abs()
    cattle_gradients = cattle_gradients.sort_values(['Gradient'], ascending=[False])
    top_ten_cattle = cattle_gradients.iloc[0:10,:]
    print(top_ten_cattle)
    top_ten_combined_cattle = all_values_cattle.where(all_values_cattle.Parameter_names.isin(top_ten_cattle['Parameter name']))
    top_ten_combined_cattle = top_ten_combined_cattle[top_ten_combined_cattle['Parameter_names'].notna()]
    print(top_ten_combined_cattle)
    top_ten_combined_cattle.to_excel("final_df_gradients_cattle.xlsx")
    # graph it
    l = sns.relplot(data=top_ten_combined_cattle, x='Parameter_values', y='Population', col='Parameter_names', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
    l.fig.suptitle('Longhorn cattle gradients')
    plt.tight_layout()
    plt.savefig('sensitivity_cattle.png')
    plt.show()


    # # TAMWORTH PIG
    pig_gradients = []
    column_names_pig = []
    column_values_pig= []
    populations_pig = []
    gradients_pig = []
    
    # find the gradient
    for column in merged_dfs.iloc[:,0:77]:
        res = linregress(merged_dfs[column], merged_dfs["Tamworth pigs"])
        pig_gradient = [column, res.slope]
        pig_gradients.append(pig_gradient)
        # append column name & values, populations and gradients 
        column_names_pig.append([column]*3*77)
        column_values_pig.append(merged_dfs[column].to_list())
        populations_pig.append(merged_dfs["Tamworth pigs"].to_list())
        gradients_pig.append([res.slope]*3*77)

    # organize the data
    pig_gradients = pd.DataFrame(data=pig_gradients, columns = ['Parameter name', 'Gradient'])
    all_values_pig = pd.DataFrame()
    flat_column_names_pig = [item for sublist in column_names_pig for item in sublist]
    flat_column_values_pig= [item for sublist in column_values_pig for item in sublist]
    flat_populations_pig = [item for sublist in populations_pig for item in sublist]
    flat_gradients_pig = [item for sublist in gradients_pig for item in sublist]
    all_values_pig['Parameter_names'] = flat_column_names_pig
    all_values_pig['Parameter_values'] = flat_column_values_pig
    all_values_pig['Population'] = flat_populations_pig
    all_values_pig['Gradient'] = flat_gradients_pig
    # take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
    pig_gradients['Gradient'] = pig_gradients['Gradient'].abs()
    pig_gradients = pig_gradients.sort_values(['Gradient'], ascending=[False])
    top_ten_pig = pig_gradients.iloc[0:10,:]
    print(top_ten_pig)
    top_ten_combined_pig = all_values_pig.where(all_values_pig.Parameter_names.isin(top_ten_pig['Parameter name']))
    top_ten_combined_pig = top_ten_combined_pig[top_ten_combined_pig['Parameter_names'].notna()]
    print(top_ten_combined_pig)
    top_ten_combined_pig.to_excel("final_df_gradients_pig.xlsx")
    # graph it
    t = sns.relplot(data=top_ten_combined_pig, x='Parameter_values', y='Population', col='Parameter_names', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
    t.fig.suptitle('Tamworth pig gradients')
    plt.tight_layout()
    plt.savefig('sensitivity_pigs.png')
    plt.show()


    # # EXMOOR PONY
    pony_gradients = []
    column_names_pony = []
    column_values_pony= []
    populations_pony= []
    gradients_pony = []
    
    # find the gradient
    for column in merged_dfs.iloc[:,0:77]:
        res = linregress(merged_dfs[column], merged_dfs["Exmoor pony"])
        pony_gradient = [column, res.slope]
        pony_gradients.append(pony_gradient)
        # append column name & values, populations and gradients 
        column_names_pony.append([column]*3*77)
        column_values_pony.append(merged_dfs[column].to_list())
        populations_pony.append(merged_dfs["Exmoor pony"].to_list())
        gradients_pony.append([res.slope]*3*77)

    # organize the data
    pony_gradients = pd.DataFrame(data=pony_gradients, columns = ['Parameter name', 'Gradient'])
    all_values_pony = pd.DataFrame()
    flat_column_names_pony = [item for sublist in column_names_pony for item in sublist]
    flat_column_values_pony= [item for sublist in column_values_pony for item in sublist]
    flat_populations_pony = [item for sublist in populations_pony for item in sublist]
    flat_gradients_pony = [item for sublist in gradients_pony for item in sublist]
    all_values_pony['Parameter_names'] = flat_column_names_pony
    all_values_pony['Parameter_values'] = flat_column_values_pony
    all_values_pony['Population'] = flat_populations_pony
    all_values_pony['Gradient'] = flat_gradients_pony
    # take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
    pony_gradients['Gradient'] = pony_gradients['Gradient'].abs()
    pony_gradients = pony_gradients.sort_values(['Gradient'], ascending=[False])
    top_ten_pony = pony_gradients.iloc[0:10,:]
    print(top_ten_pony)
    top_ten_combined_pony = all_values_pony.where(all_values_pony.Parameter_names.isin(top_ten_pony['Parameter name']))
    top_ten_combined_pony = top_ten_combined_pony[top_ten_combined_pony['Parameter_names'].notna()]
    print(top_ten_combined_pony)
    top_ten_combined_pony.to_excel("final_df_gradients_pony.xlsx")
    # graph it
    p = sns.relplot(data=top_ten_combined_pony, x='Parameter_values', y='Population', col='Parameter_names', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
    p.fig.suptitle('Exmoor pony gradients')
    plt.tight_layout()
    plt.savefig('sensitivity_pony.png')
    plt.show()



    # # GRASSLAND
    grassland_gradients = []
    column_names_grassland = []
    column_values_grassland= []
    populations_grassland= []
    gradients_grassland= []
    
    # find the gradient
    for column in merged_dfs.iloc[:,0:77]:
        res = linregress(merged_dfs[column], merged_dfs["Grassland"])
        grassland_gradient = [column, res.slope]
        grassland_gradients.append(grassland_gradient)
        # append column name & values, populations and gradients 
        column_names_grassland.append([column]*3*77)
        column_values_grassland.append(merged_dfs[column].to_list())
        populations_grassland.append(merged_dfs["Grassland"].to_list())
        gradients_grassland.append([res.slope]*3*77)

    # organize the data
    grassland_gradients = pd.DataFrame(data=grassland_gradients, columns = ['Parameter name', 'Gradient'])
    all_values_grassland = pd.DataFrame()
    flat_column_names_grassland = [item for sublist in column_names_grassland for item in sublist]
    flat_column_values_grassland= [item for sublist in column_values_grassland for item in sublist]
    flat_populations_grassland = [item for sublist in populations_grassland for item in sublist]
    flat_gradients_grassland = [item for sublist in gradients_grassland for item in sublist]
    all_values_grassland['Parameter_names'] = flat_column_names_grassland
    all_values_grassland['Parameter_values'] = flat_column_values_grassland
    all_values_grassland['Population'] = flat_populations_grassland
    all_values_grassland['Gradient'] = flat_gradients_grassland
    # take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
    grassland_gradients['Gradient'] = grassland_gradients['Gradient'].abs()
    grassland_gradients = grassland_gradients.sort_values(['Gradient'], ascending=[False])
    top_ten_grassland = grassland_gradients.iloc[0:10,:]
    print(top_ten_grassland)
    top_ten_combined_grassland = all_values_grassland.where(all_values_grassland.Parameter_names.isin(top_ten_grassland['Parameter name']))
    top_ten_combined_grassland = top_ten_combined_grassland[top_ten_combined_grassland['Parameter_names'].notna()]
    print(top_ten_combined_grassland)
    top_ten_combined_grassland.to_excel("final_df_gradients_grassland.xlsx")
    # graph it
    g = sns.relplot(data=top_ten_combined_grassland, x='Parameter_values', y='Population', col='Parameter_names', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
    g.fig.suptitle('Grassland gradients')
    plt.tight_layout()
    plt.savefig('sensitivity_grass.png')
    plt.show()


    # # THORNY SCRUB
    scrub_gradients = []
    column_names_scrub = []
    column_values_scrub= []
    populations_scrub= []
    gradients_scrub= []
    
    # find the gradient
    for column in merged_dfs.iloc[:,0:77]:
        res = linregress(merged_dfs[column], merged_dfs["Thorny Scrub"])
        scrub_gradient = [column, res.slope]
        scrub_gradients.append(scrub_gradient)
        # append column name & values, populations and gradients 
        column_names_scrub.append([column]*3*77)
        column_values_scrub.append(merged_dfs[column].to_list())
        populations_scrub.append(merged_dfs["Thorny Scrub"].to_list())
        gradients_scrub.append([res.slope]*3*77)

    # organize the data
    scrub_gradients = pd.DataFrame(data=scrub_gradients, columns = ['Parameter name', 'Gradient'])
    all_values_scrub = pd.DataFrame()
    flat_column_names_scrub = [item for sublist in column_names_scrub for item in sublist]
    flat_column_values_scrub= [item for sublist in column_values_scrub for item in sublist]
    flat_populations_scrub = [item for sublist in populations_scrub for item in sublist]
    flat_gradients_scrub= [item for sublist in gradients_scrub for item in sublist]
    all_values_scrub['Parameter_names'] = flat_column_names_scrub
    all_values_scrub['Parameter_values'] = flat_column_values_scrub
    all_values_scrub['Population'] = flat_populations_scrub
    all_values_scrub['Gradient'] = flat_gradients_scrub
    # take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
    scrub_gradients['Gradient'] = scrub_gradients['Gradient'].abs()
    scrub_gradients = scrub_gradients.sort_values(['Gradient'], ascending=[False])
    top_ten_scrub = scrub_gradients.iloc[0:10,:]
    print(top_ten_scrub)
    top_ten_combined_scrub = all_values_scrub.where(all_values_scrub.Parameter_names.isin(top_ten_scrub['Parameter name']))
    top_ten_combined_scrub = top_ten_combined_scrub[top_ten_combined_scrub['Parameter_names'].notna()]
    print(top_ten_combined_scrub)
    top_ten_combined_scrub.to_excel("final_df_gradients_scrub.xlsx")
    # graph it
    s = sns.relplot(data=top_ten_combined_scrub, x='Parameter_values', y='Population', col='Parameter_names', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
    s.fig.suptitle('Thorny scrub gradients')
    plt.tight_layout()
    plt.savefig('sensitivity_scrub.png')
    plt.show()



    # # WOODLAND
    woodland_gradients = []
    column_names_woodland = []
    column_values_woodland= []
    populations_woodland= []
    gradients_woodland= []
    
    # find the gradient
    for column in merged_dfs.iloc[:,0:77]:
        res = linregress(merged_dfs[column], merged_dfs["Woodland"])
        woodland_gradient = [column, res.slope]
        woodland_gradients.append(woodland_gradient)
        # append column name & values, populations and gradients 
        column_names_woodland.append([column]*3*77)
        column_values_woodland.append(merged_dfs[column].to_list())
        populations_woodland.append(merged_dfs["Woodland"].to_list())
        gradients_woodland.append([res.slope]*3*77)

    # organize the data
    woodland_gradients = pd.DataFrame(data=woodland_gradients, columns = ['Parameter name', 'Gradient'])
    all_values_woodland = pd.DataFrame()
    flat_column_names_woodland = [item for sublist in column_names_woodland for item in sublist]
    flat_column_values_woodland= [item for sublist in column_values_woodland for item in sublist]
    flat_populations_woodland = [item for sublist in populations_woodland for item in sublist]
    flat_gradients_woodland = [item for sublist in gradients_woodland for item in sublist]
    all_values_woodland['Parameter_names'] = flat_column_names_woodland
    all_values_woodland['Parameter_values'] = flat_column_values_woodland
    all_values_woodland['Population'] = flat_populations_woodland
    all_values_woodland['Gradient'] = flat_gradients_woodland
    # take the top 10 most important ones; make sure to turn the negative ones positive when organizing them
    woodland_gradients['Gradient'] = woodland_gradients['Gradient'].abs()
    woodland_gradients = woodland_gradients.sort_values(['Gradient'], ascending=[False])
    top_ten_woodland = woodland_gradients.iloc[0:10,:]
    print(top_ten_woodland)
    top_ten_combined_woodland= all_values_woodland.where(all_values_woodland.Parameter_names.isin(top_ten_woodland['Parameter name']))
    top_ten_combined_woodland= top_ten_combined_woodland[top_ten_combined_woodland['Parameter_names'].notna()]
    print(top_ten_combined_woodland)
    top_ten_combined_woodland.to_excel("final_df_gradients_woodland.xlsx")
    # graph it
    w = sns.relplot(data=top_ten_combined_woodland, x='Parameter_values', y='Population', col='Parameter_names', col_wrap=5, kind='scatter',facet_kws={'sharey': False, 'sharex': False})
    w.fig.suptitle('Woodland gradients')
    plt.tight_layout()
    plt.savefig('sensitivity_woodland.png')
    plt.show()


optimizer_fails()