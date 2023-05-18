# run experiments on the accepted parameter sets
from model import KneppModel 
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from shapely.geometry import Polygon
import shapefile as shp
from shapely import wkt
import geopandas as gpd
from geopandas import GeoDataFrame


# first, no food - REMEMBER to set the initial habitat values in agents.py to zero
def reality_no_food():

    accepted_parameters = pd.read_csv('combined_accepted_parameters.csv') 
    accepted_parameters.drop(['Unnamed: 0'], axis=1, inplace=True)

    # run the counterfactual: what would have happened if rewilding hadn't occurred?
    final_results_list = []
    run_number = 0


    # take the accepted parameters, and go row by row, running the model
    for _, row in accepted_parameters.iterrows():

        chance_reproduceSapling = 0
        chance_reproduceYoungScrub =  0
        chance_regrowGrass =  0
        chance_saplingBecomingTree =  row["chance_saplingBecomingTree"]
        chance_youngScrubMatures =  row["chance_youngScrubMatures"]
        chance_scrubOutcompetedByTree =  row["chance_scrubOutcompetedByTree"]
        chance_grassOutcompetedByTree =  row["chance_grassOutcompetedByTree"]
        chance_grassOutcompetedByScrub = row["chance_grassOutcompetedByScrub"]
        initial_roe = 12
        fallowDeer_stocking = 247
        cattle_stocking = 81
        redDeer_stocking = 35
        tamworthPig_stocking = 7
        exmoor_stocking = 15

        roe_deer_reproduce = row["roe_deer_reproduce"]
        roe_deer_gain_from_grass =  row["roe_deer_gain_from_grass"]
        roe_deer_gain_from_trees =  row["roe_deer_gain_from_trees"]
        roe_deer_gain_from_scrub =  row["roe_deer_gain_from_scrub"]
        roe_deer_gain_from_saplings =  row["roe_deer_gain_from_saplings"]
        roe_deer_gain_from_young_scrub =  row["roe_deer_gain_from_young_scrub"]
        ponies_gain_from_grass =  row["ponies_gain_from_grass"]
        ponies_gain_from_trees =  row["ponies_gain_from_trees"]
        ponies_gain_from_scrub =  row["ponies_gain_from_scrub"]
        ponies_gain_from_saplings =  row["ponies_gain_from_saplings"]
        ponies_gain_from_young_scrub =  row["ponies_gain_from_young_scrub"]
        cattle_reproduce =  row["cattle_reproduce"]
        cows_gain_from_grass =  row["cows_gain_from_grass"]
        cows_gain_from_trees =  row["cows_gain_from_trees"]
        cows_gain_from_scrub =  row["cows_gain_from_scrub"]
        cows_gain_from_saplings =  row["cows_gain_from_saplings"]
        cows_gain_from_young_scrub =  row["cows_gain_from_young_scrub"]
        fallow_deer_reproduce =  row["fallow_deer_reproduce"]
        fallow_deer_gain_from_grass =  row["fallow_deer_gain_from_grass"]
        fallow_deer_gain_from_trees =  row["fallow_deer_gain_from_trees"]
        fallow_deer_gain_from_scrub =  row["fallow_deer_gain_from_scrub"]
        fallow_deer_gain_from_saplings =  row["fallow_deer_gain_from_saplings"]
        fallow_deer_gain_from_young_scrub =  row["fallow_deer_gain_from_young_scrub"]   
        red_deer_reproduce =  row["red_deer_reproduce"]
        red_deer_gain_from_grass =  row["red_deer_gain_from_grass"]
        red_deer_gain_from_trees =  row["red_deer_gain_from_trees"]
        red_deer_gain_from_scrub =  row["red_deer_gain_from_scrub"]
        red_deer_gain_from_saplings =  row["red_deer_gain_from_saplings"]
        red_deer_gain_from_young_scrub =  row["red_deer_gain_from_young_scrub"]
        tamworth_pig_reproduce =  row["tamworth_pig_reproduce"]
        tamworth_pig_gain_from_grass =  row["tamworth_pig_gain_from_grass"]
        tamworth_pig_gain_from_trees = row["tamworth_pig_gain_from_trees"]
        tamworth_pig_gain_from_scrub = row["tamworth_pig_gain_from_scrub"]
        tamworth_pig_gain_from_saplings =  row["tamworth_pig_gain_from_saplings"]
        tamworth_pig_gain_from_young_scrub =  row["tamworth_pig_gain_from_young_scrub"]

        # euro bison parameters
        european_bison_reproduce = 0
        # bison should have higher impact than any other consumer
        european_bison_gain_from_grass =  0
        european_bison_gain_from_trees =0
        european_bison_gain_from_scrub =0
        european_bison_gain_from_saplings = 0
        european_bison_gain_from_young_scrub = 0  
        # euro elk parameters
        european_elk_reproduce = 0
        # bison should have higher impact than any other consumer
        european_elk_gain_from_grass =  0
        european_elk_gain_from_trees = 0
        european_elk_gain_from_scrub = 0
        european_elk_gain_from_saplings =  0
        european_elk_gain_from_young_scrub =  0
        # reindeer parameters
        reindeer_reproduce = 0
        # reindeer should have impacts between red and fallow deer
        reindeer_gain_from_grass = 0
        reindeer_gain_from_trees =0
        reindeer_gain_from_scrub =0
        reindeer_gain_from_saplings = 0
        reindeer_gain_from_young_scrub = 0
        # forecasting parameters
        fallowDeer_stocking_forecast = 247
        cattle_stocking_forecast = 81
        redDeer_stocking_forecast = 35
        tamworthPig_stocking_forecast = 7
        exmoor_stocking_forecast = 15
        introduced_species_stocking_forecast = 0

        chance_scrub_saves_saplings = row["chance_scrub_saves_saplings"]

        random.seed(1)
        np.random.seed(1)

        model = KneppModel(initial_roe, roe_deer_reproduce, roe_deer_gain_from_saplings, roe_deer_gain_from_trees, roe_deer_gain_from_scrub, roe_deer_gain_from_young_scrub, roe_deer_gain_from_grass,
                            chance_youngScrubMatures, chance_saplingBecomingTree, chance_reproduceSapling,chance_reproduceYoungScrub, chance_regrowGrass, 
                            chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_scrubOutcompetedByTree, 
                            ponies_gain_from_saplings, ponies_gain_from_trees, ponies_gain_from_scrub, ponies_gain_from_young_scrub, ponies_gain_from_grass, 
                            cattle_reproduce, cows_gain_from_grass, cows_gain_from_trees, cows_gain_from_scrub, cows_gain_from_saplings, cows_gain_from_young_scrub, 
                            fallow_deer_reproduce, fallow_deer_gain_from_saplings, fallow_deer_gain_from_trees, fallow_deer_gain_from_scrub, fallow_deer_gain_from_young_scrub, fallow_deer_gain_from_grass,
                            red_deer_reproduce, red_deer_gain_from_saplings, red_deer_gain_from_trees, red_deer_gain_from_scrub, red_deer_gain_from_young_scrub, red_deer_gain_from_grass,
                            tamworth_pig_reproduce, tamworth_pig_gain_from_saplings,tamworth_pig_gain_from_trees,tamworth_pig_gain_from_scrub,tamworth_pig_gain_from_young_scrub,tamworth_pig_gain_from_grass,
                            european_bison_reproduce, european_bison_gain_from_grass, european_bison_gain_from_trees, european_bison_gain_from_scrub, european_bison_gain_from_saplings, european_bison_gain_from_young_scrub,
                            european_elk_reproduce, european_elk_gain_from_grass, european_elk_gain_from_trees, european_elk_gain_from_scrub, european_elk_gain_from_saplings, european_elk_gain_from_young_scrub,
                            reindeer_reproduce, reindeer_gain_from_grass, reindeer_gain_from_trees, reindeer_gain_from_scrub, reindeer_gain_from_saplings, reindeer_gain_from_young_scrub,
                            fallowDeer_stocking, cattle_stocking, redDeer_stocking, tamworthPig_stocking, exmoor_stocking,
                            fallowDeer_stocking_forecast, cattle_stocking_forecast, redDeer_stocking_forecast, tamworthPig_stocking_forecast, exmoor_stocking_forecast, introduced_species_stocking_forecast,
                            chance_scrub_saves_saplings,
                            max_time = 10, reintroduction = True, introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)


        model.reset_randomizer(seed=1)
        model.run_model()

        run_number +=1
        print(run_number)

        results = model.datacollector.get_model_vars_dataframe()
        results['run_number'] = run_number
        final_results_list.append(results)


    # append to dataframe
    forecasting = pd.concat(final_results_list)

    palette=['#009e73', '#f0e442', '#0072b2','#cc79a7']

    # graph that
    final_df =  pd.DataFrame(
                    (forecasting[["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland","Woodland", "Thorny Scrub","Bare ground"]].values.flatten()), columns=['Abundance %'])
    final_df["runNumber"] = pd.DataFrame(np.concatenate([np.repeat(forecasting['run_number'], 10)], axis=0))
    final_df["Time"] = pd.DataFrame(np.concatenate([np.repeat(forecasting['Time'], 10)], axis=0))
    final_df["Ecosystem Element"] = pd.DataFrame(np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], len(forecasting)))

    # calculate median 
    m = final_df.groupby(['Time', 'Ecosystem Element'])[['Abundance %']].apply(np.median)
    m.name = 'Median'
    final_df = final_df.join(m, on=['Time','Ecosystem Element'])
    # calculate quantiles - try graphing smaller percentiles on top 
    perc1 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(1) 
    perc1.name = 'onehundperc'
    final_df = final_df.join(perc1, on=['Time', 'Ecosystem Element'])
    perc2 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(0) 
    perc2.name = "zeroperc"
    final_df = final_df.join(perc2, on=['Time', 'Ecosystem Element'])
    # now show more quantiles, 95th
    perc3 = final_df.groupby(['Time',  'Ecosystem Element'])['Abundance %'].quantile(0.975) 
    perc3.name = 'ninetyfiveperc'
    final_df = final_df.join(perc3, on=['Time',  'Ecosystem Element'])
    perc4 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(0.025)
    perc4.name = "fiveperc"
    final_df = final_df.join(perc4, on=['Time', 'Ecosystem Element'])
    # and 80th
    perc5 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(0.9)
    perc5.name = 'eightyperc'
    final_df = final_df.join(perc5, on=['Time',  'Ecosystem Element'])
    perc6 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(0.1)
    perc6.name = "twentyperc"
    final_df = final_df.join(perc6, on=['Time', 'Ecosystem Element'])

    final_df = final_df.reset_index(drop=True)
    final_df.to_csv("RC_no_food.csv")

    f = sns.FacetGrid(final_df, col="Ecosystem Element", palette = palette, col_wrap=4, sharey = False)
    f.map(sns.lineplot, 'Time', 'Median')
    f.map(sns.lineplot, 'Time', 'onehundperc')
    f.map(sns.lineplot, 'Time', 'zeroperc')
    # now other percentiles
    f.map(sns.lineplot, 'Time', 'Median')
    f.map(sns.lineplot, 'Time', 'ninetyfiveperc')
    f.map(sns.lineplot, 'Time', 'fiveperc')
    # now other percentiles
    f.map(sns.lineplot, 'Time', 'Median')
    f.map(sns.lineplot, 'Time', 'eightyperc')
    f.map(sns.lineplot, 'Time', 'twentyperc')

    for ax in f.axes.flat:
        ax.fill_between(ax.lines[1].get_xdata(),ax.lines[1].get_ydata(), ax.lines[2].get_ydata(),  color="blue",alpha =0.2)
        # 95 perc
        ax.fill_between(ax.lines[4].get_xdata(),ax.lines[4].get_ydata(), ax.lines[5].get_ydata(),  color="yellow",alpha =0.2)
        # 80 perc
        ax.fill_between(ax.lines[7].get_xdata(),ax.lines[7].get_ydata(), ax.lines[8].get_ydata(),  color="green",alpha =0.2)
        ax.set_ylabel('Abundance')
        ax.set_xlabel('Time (Months)')

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

    f.fig.suptitle('Reality Check: Herbivores should decline if no food available')
    plt.tight_layout()
    plt.savefig('RC_no_food.png')
    plt.show()






# second, no herbivory. Run it for fifty years
def reality_no_herbivory():

    accepted_parameters = pd.read_csv('combined_accepted_parameters.csv') 
    accepted_parameters.drop(['Unnamed: 0'], axis=1, inplace=True)

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

        initial_roe = 0
        fallowDeer_stocking = 0
        cattle_stocking = 0
        redDeer_stocking = 0
        tamworthPig_stocking = 0
        exmoor_stocking = 0

        roe_deer_reproduce = row["roe_deer_reproduce"]
        roe_deer_gain_from_grass =  row["roe_deer_gain_from_grass"]
        roe_deer_gain_from_trees =  row["roe_deer_gain_from_trees"]
        roe_deer_gain_from_scrub =  row["roe_deer_gain_from_scrub"]
        roe_deer_gain_from_saplings =  row["roe_deer_gain_from_saplings"]
        roe_deer_gain_from_young_scrub =  row["roe_deer_gain_from_young_scrub"]
        ponies_gain_from_grass =  row["ponies_gain_from_grass"]
        ponies_gain_from_trees =  row["ponies_gain_from_trees"]
        ponies_gain_from_scrub =  row["ponies_gain_from_scrub"]
        ponies_gain_from_saplings =  row["ponies_gain_from_saplings"]
        ponies_gain_from_young_scrub =  row["ponies_gain_from_young_scrub"]
        cattle_reproduce =  row["cattle_reproduce"]
        cows_gain_from_grass =  row["cows_gain_from_grass"]
        cows_gain_from_trees =  row["cows_gain_from_trees"]
        cows_gain_from_scrub =  row["cows_gain_from_scrub"]
        cows_gain_from_saplings =  row["cows_gain_from_saplings"]
        cows_gain_from_young_scrub =  row["cows_gain_from_young_scrub"]
        fallow_deer_reproduce =  row["fallow_deer_reproduce"]
        fallow_deer_gain_from_grass =  row["fallow_deer_gain_from_grass"]
        fallow_deer_gain_from_trees =  row["fallow_deer_gain_from_trees"]
        fallow_deer_gain_from_scrub =  row["fallow_deer_gain_from_scrub"]
        fallow_deer_gain_from_saplings =  row["fallow_deer_gain_from_saplings"]
        fallow_deer_gain_from_young_scrub =  row["fallow_deer_gain_from_young_scrub"]   
        red_deer_reproduce =  row["red_deer_reproduce"]
        red_deer_gain_from_grass =  row["red_deer_gain_from_grass"]
        red_deer_gain_from_trees =  row["red_deer_gain_from_trees"]
        red_deer_gain_from_scrub =  row["red_deer_gain_from_scrub"]
        red_deer_gain_from_saplings =  row["red_deer_gain_from_saplings"]
        red_deer_gain_from_young_scrub =  row["red_deer_gain_from_young_scrub"]
        tamworth_pig_reproduce =  row["tamworth_pig_reproduce"]
        tamworth_pig_gain_from_grass =  row["tamworth_pig_gain_from_grass"]
        tamworth_pig_gain_from_trees = row["tamworth_pig_gain_from_trees"]
        tamworth_pig_gain_from_scrub = row["tamworth_pig_gain_from_scrub"]
        tamworth_pig_gain_from_saplings =  row["tamworth_pig_gain_from_saplings"]
        tamworth_pig_gain_from_young_scrub =  row["tamworth_pig_gain_from_young_scrub"]

        # euro bison parameters
        european_bison_reproduce = 0
        # bison should have higher impact than any other consumer
        european_bison_gain_from_grass =  0
        european_bison_gain_from_trees =0
        european_bison_gain_from_scrub =0
        european_bison_gain_from_saplings = 0
        european_bison_gain_from_young_scrub = 0  
        # euro elk parameters
        european_elk_reproduce = 0
        # bison should have higher impact than any other consumer
        european_elk_gain_from_grass =  0
        european_elk_gain_from_trees = 0
        european_elk_gain_from_scrub = 0
        european_elk_gain_from_saplings =  0
        european_elk_gain_from_young_scrub =  0
        # reindeer parameters
        reindeer_reproduce = 0
        # reindeer should have impacts between red and fallow deer
        reindeer_gain_from_grass = 0
        reindeer_gain_from_trees =0
        reindeer_gain_from_scrub =0
        reindeer_gain_from_saplings = 0
        reindeer_gain_from_young_scrub = 0
        # forecasting parameters
        fallowDeer_stocking_forecast = 247
        cattle_stocking_forecast = 81
        redDeer_stocking_forecast = 35
        tamworthPig_stocking_forecast = 7
        exmoor_stocking_forecast = 15
        introduced_species_stocking_forecast = 0

        chance_scrub_saves_saplings = row["chance_scrub_saves_saplings"]

        random.seed(1)
        np.random.seed(1)

        model = KneppModel(initial_roe, roe_deer_reproduce, roe_deer_gain_from_saplings, roe_deer_gain_from_trees, roe_deer_gain_from_scrub, roe_deer_gain_from_young_scrub, roe_deer_gain_from_grass,
                            chance_youngScrubMatures, chance_saplingBecomingTree, chance_reproduceSapling,chance_reproduceYoungScrub, chance_regrowGrass, 
                            chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_scrubOutcompetedByTree, 
                            ponies_gain_from_saplings, ponies_gain_from_trees, ponies_gain_from_scrub, ponies_gain_from_young_scrub, ponies_gain_from_grass, 
                            cattle_reproduce, cows_gain_from_grass, cows_gain_from_trees, cows_gain_from_scrub, cows_gain_from_saplings, cows_gain_from_young_scrub, 
                            fallow_deer_reproduce, fallow_deer_gain_from_saplings, fallow_deer_gain_from_trees, fallow_deer_gain_from_scrub, fallow_deer_gain_from_young_scrub, fallow_deer_gain_from_grass,
                            red_deer_reproduce, red_deer_gain_from_saplings, red_deer_gain_from_trees, red_deer_gain_from_scrub, red_deer_gain_from_young_scrub, red_deer_gain_from_grass,
                            tamworth_pig_reproduce, tamworth_pig_gain_from_saplings,tamworth_pig_gain_from_trees,tamworth_pig_gain_from_scrub,tamworth_pig_gain_from_young_scrub,tamworth_pig_gain_from_grass,
                            european_bison_reproduce, european_bison_gain_from_grass, european_bison_gain_from_trees, european_bison_gain_from_scrub, european_bison_gain_from_saplings, european_bison_gain_from_young_scrub,
                            european_elk_reproduce, european_elk_gain_from_grass, european_elk_gain_from_trees, european_elk_gain_from_scrub, european_elk_gain_from_saplings, european_elk_gain_from_young_scrub,
                            reindeer_reproduce, reindeer_gain_from_grass, reindeer_gain_from_trees, reindeer_gain_from_scrub, reindeer_gain_from_saplings, reindeer_gain_from_young_scrub,
                            fallowDeer_stocking, cattle_stocking, redDeer_stocking, tamworthPig_stocking, exmoor_stocking,
                            fallowDeer_stocking_forecast, cattle_stocking_forecast, redDeer_stocking_forecast, tamworthPig_stocking_forecast, exmoor_stocking_forecast, introduced_species_stocking_forecast,
                            chance_scrub_saves_saplings,
                            max_time = 600, reintroduction = False, introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)


        model.reset_randomizer(seed=1)
        model.run_model()

        run_number +=1
        print(run_number)

        results = model.datacollector.get_model_vars_dataframe()
        results['run_number'] = run_number
        final_results_list.append(results)


    # append to dataframe
    forecasting = pd.concat(final_results_list)

    palette=['#009e73', '#f0e442', '#0072b2','#cc79a7']

    # graph that
    final_df =  pd.DataFrame(
                    (forecasting[["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland","Woodland", "Thorny Scrub","Bare ground"]].values.flatten()), columns=['Abundance %'])
    final_df["runNumber"] = pd.DataFrame(np.concatenate([np.repeat(forecasting['run_number'], 10)], axis=0))
    final_df["Time"] = pd.DataFrame(np.concatenate([np.repeat(forecasting['Time'], 10)], axis=0))
    final_df["Ecosystem Element"] = pd.DataFrame(np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], len(forecasting)))

    # calculate median 
    m = final_df.groupby(['Time', 'Ecosystem Element'])[['Abundance %']].apply(np.median)
    m.name = 'Median'
    final_df = final_df.join(m, on=['Time','Ecosystem Element'])
    # calculate quantiles - try graphing smaller percentiles on top 
    perc1 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(1) 
    perc1.name = 'onehundperc'
    final_df = final_df.join(perc1, on=['Time', 'Ecosystem Element'])
    perc2 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(0) 
    perc2.name = "zeroperc"
    final_df = final_df.join(perc2, on=['Time', 'Ecosystem Element'])
    # now show more quantiles, 95th
    perc3 = final_df.groupby(['Time',  'Ecosystem Element'])['Abundance %'].quantile(0.975) 
    perc3.name = 'ninetyfiveperc'
    final_df = final_df.join(perc3, on=['Time',  'Ecosystem Element'])
    perc4 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(0.025)
    perc4.name = "fiveperc"
    final_df = final_df.join(perc4, on=['Time', 'Ecosystem Element'])
    # and 80th
    perc5 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(0.9)
    perc5.name = 'eightyperc'
    final_df = final_df.join(perc5, on=['Time',  'Ecosystem Element'])
    perc6 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(0.1)
    perc6.name = "twentyperc"
    final_df = final_df.join(perc6, on=['Time', 'Ecosystem Element'])

    final_df = final_df.reset_index(drop=True)
    final_df.to_csv("RC_no_herbivory.csv")

    f = sns.FacetGrid(final_df, col="Ecosystem Element", palette = palette, col_wrap=4, sharey = False)
    f.map(sns.lineplot, 'Time', 'Median')
    f.map(sns.lineplot, 'Time', 'onehundperc')
    f.map(sns.lineplot, 'Time', 'zeroperc')
    # now other percentiles
    f.map(sns.lineplot, 'Time', 'Median')
    f.map(sns.lineplot, 'Time', 'ninetyfiveperc')
    f.map(sns.lineplot, 'Time', 'fiveperc')
    # now other percentiles
    f.map(sns.lineplot, 'Time', 'Median')
    f.map(sns.lineplot, 'Time', 'eightyperc')
    f.map(sns.lineplot, 'Time', 'twentyperc')

    for ax in f.axes.flat:
        ax.fill_between(ax.lines[1].get_xdata(),ax.lines[1].get_ydata(), ax.lines[2].get_ydata(),  color="blue",alpha =0.2)
        # 95 perc
        ax.fill_between(ax.lines[4].get_xdata(),ax.lines[4].get_ydata(), ax.lines[5].get_ydata(),  color="yellow",alpha =0.2)
        # 80 perc
        ax.fill_between(ax.lines[7].get_xdata(),ax.lines[7].get_ydata(), ax.lines[8].get_ydata(),  color="green",alpha =0.2)
        ax.set_ylabel('Abundance')
        ax.set_xlabel('Time (Months)')

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

    f.fig.suptitle('Reality Check: Vegetation dynamics with no herbivores present')
    plt.tight_layout()
    plt.savefig('RC_no_herbivory.png')
    plt.show()


# reality_no_herbivory()









# third, high herbivory.
def reality_high_herbivory():

    accepted_parameters = pd.read_csv('combined_accepted_parameters.csv') 
    accepted_parameters.drop(['Unnamed: 0'], axis=1, inplace=True)

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
        initial_roe = 12
        fallowDeer_stocking = 247
        cattle_stocking = 81
        redDeer_stocking = 35
        tamworthPig_stocking = 7
        exmoor_stocking = 15

        roe_deer_reproduce = row["roe_deer_reproduce"]
        roe_deer_gain_from_grass =  row["roe_deer_gain_from_grass"]
        roe_deer_gain_from_trees =  row["roe_deer_gain_from_trees"]
        roe_deer_gain_from_scrub =  row["roe_deer_gain_from_scrub"]
        roe_deer_gain_from_saplings =  row["roe_deer_gain_from_saplings"]
        roe_deer_gain_from_young_scrub =  row["roe_deer_gain_from_young_scrub"]
        ponies_gain_from_grass =  row["ponies_gain_from_grass"]
        ponies_gain_from_trees =  row["ponies_gain_from_trees"]
        ponies_gain_from_scrub =  row["ponies_gain_from_scrub"]
        ponies_gain_from_saplings =  row["ponies_gain_from_saplings"]
        ponies_gain_from_young_scrub =  row["ponies_gain_from_young_scrub"]
        cattle_reproduce =  row["cattle_reproduce"]
        cows_gain_from_grass =  row["cows_gain_from_grass"]
        cows_gain_from_trees =  row["cows_gain_from_trees"]
        cows_gain_from_scrub =  row["cows_gain_from_scrub"]
        cows_gain_from_saplings =  row["cows_gain_from_saplings"]
        cows_gain_from_young_scrub =  row["cows_gain_from_young_scrub"]
        fallow_deer_reproduce =  row["fallow_deer_reproduce"]
        fallow_deer_gain_from_grass =  row["fallow_deer_gain_from_grass"]
        fallow_deer_gain_from_trees =  row["fallow_deer_gain_from_trees"]
        fallow_deer_gain_from_scrub =  row["fallow_deer_gain_from_scrub"]
        fallow_deer_gain_from_saplings =  row["fallow_deer_gain_from_saplings"]
        fallow_deer_gain_from_young_scrub =  row["fallow_deer_gain_from_young_scrub"]   
        red_deer_reproduce =  row["red_deer_reproduce"]
        red_deer_gain_from_grass =  row["red_deer_gain_from_grass"]
        red_deer_gain_from_trees =  row["red_deer_gain_from_trees"]
        red_deer_gain_from_scrub =  row["red_deer_gain_from_scrub"]
        red_deer_gain_from_saplings =  row["red_deer_gain_from_saplings"]
        red_deer_gain_from_young_scrub =  row["red_deer_gain_from_young_scrub"]
        tamworth_pig_reproduce =  row["tamworth_pig_reproduce"]
        tamworth_pig_gain_from_grass =  row["tamworth_pig_gain_from_grass"]
        tamworth_pig_gain_from_trees = row["tamworth_pig_gain_from_trees"]
        tamworth_pig_gain_from_scrub = row["tamworth_pig_gain_from_scrub"]
        tamworth_pig_gain_from_saplings =  row["tamworth_pig_gain_from_saplings"]
        tamworth_pig_gain_from_young_scrub =  row["tamworth_pig_gain_from_young_scrub"]

        # euro bison parameters
        european_bison_reproduce = 0
        # bison should have higher impact than any other consumer
        european_bison_gain_from_grass =  0
        european_bison_gain_from_trees =0
        european_bison_gain_from_scrub =0
        european_bison_gain_from_saplings = 0
        european_bison_gain_from_young_scrub = 0  
        # euro elk parameters
        european_elk_reproduce = 0
        # bison should have higher impact than any other consumer
        european_elk_gain_from_grass =  0
        european_elk_gain_from_trees = 0
        european_elk_gain_from_scrub = 0
        european_elk_gain_from_saplings =  0
        european_elk_gain_from_young_scrub =  0
        # reindeer parameters
        reindeer_reproduce = 0
        # reindeer should have impacts between red and fallow deer
        reindeer_gain_from_grass = 0
        reindeer_gain_from_trees =0
        reindeer_gain_from_scrub =0
        reindeer_gain_from_saplings = 0
        reindeer_gain_from_young_scrub = 0
        # forecasting parameters
        fallowDeer_stocking_forecast = 247*5
        cattle_stocking_forecast = 81*5
        redDeer_stocking_forecast = 35*5
        tamworthPig_stocking_forecast = 7*5
        exmoor_stocking_forecast = 15*5
        introduced_species_stocking_forecast = 0

        chance_scrub_saves_saplings = row["chance_scrub_saves_saplings"]

        random.seed(1)
        np.random.seed(1)

        model = KneppModel(initial_roe, roe_deer_reproduce, roe_deer_gain_from_saplings, roe_deer_gain_from_trees, roe_deer_gain_from_scrub, roe_deer_gain_from_young_scrub, roe_deer_gain_from_grass,
                            chance_youngScrubMatures, chance_saplingBecomingTree, chance_reproduceSapling,chance_reproduceYoungScrub, chance_regrowGrass, 
                            chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_scrubOutcompetedByTree, 
                            ponies_gain_from_saplings, ponies_gain_from_trees, ponies_gain_from_scrub, ponies_gain_from_young_scrub, ponies_gain_from_grass, 
                            cattle_reproduce, cows_gain_from_grass, cows_gain_from_trees, cows_gain_from_scrub, cows_gain_from_saplings, cows_gain_from_young_scrub, 
                            fallow_deer_reproduce, fallow_deer_gain_from_saplings, fallow_deer_gain_from_trees, fallow_deer_gain_from_scrub, fallow_deer_gain_from_young_scrub, fallow_deer_gain_from_grass,
                            red_deer_reproduce, red_deer_gain_from_saplings, red_deer_gain_from_trees, red_deer_gain_from_scrub, red_deer_gain_from_young_scrub, red_deer_gain_from_grass,
                            tamworth_pig_reproduce, tamworth_pig_gain_from_saplings,tamworth_pig_gain_from_trees,tamworth_pig_gain_from_scrub,tamworth_pig_gain_from_young_scrub,tamworth_pig_gain_from_grass,
                            european_bison_reproduce, european_bison_gain_from_grass, european_bison_gain_from_trees, european_bison_gain_from_scrub, european_bison_gain_from_saplings, european_bison_gain_from_young_scrub,
                            european_elk_reproduce, european_elk_gain_from_grass, european_elk_gain_from_trees, european_elk_gain_from_scrub, european_elk_gain_from_saplings, european_elk_gain_from_young_scrub,
                            reindeer_reproduce, reindeer_gain_from_grass, reindeer_gain_from_trees, reindeer_gain_from_scrub, reindeer_gain_from_saplings, reindeer_gain_from_young_scrub,
                            fallowDeer_stocking, cattle_stocking, redDeer_stocking, tamworthPig_stocking, exmoor_stocking,
                            fallowDeer_stocking_forecast, cattle_stocking_forecast, redDeer_stocking_forecast, tamworthPig_stocking_forecast, exmoor_stocking_forecast, introduced_species_stocking_forecast,
                            chance_scrub_saves_saplings,
                            max_time = 485, reintroduction = True, introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)


        model.reset_randomizer(seed=1)
        model.run_model()

        run_number +=1
        print(run_number)

        results = model.datacollector.get_model_vars_dataframe()
        results['run_number'] = run_number
        final_results_list.append(results)


    # append to dataframe
    forecasting = pd.concat(final_results_list)

    palette=['#009e73', '#f0e442', '#0072b2','#cc79a7']

    # graph that
    final_df =  pd.DataFrame(
                    (forecasting[["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland","Woodland", "Thorny Scrub","Bare ground"]].values.flatten()), columns=['Abundance %'])
    final_df["runNumber"] = pd.DataFrame(np.concatenate([np.repeat(forecasting['run_number'], 10)], axis=0))
    final_df["Time"] = pd.DataFrame(np.concatenate([np.repeat(forecasting['Time'], 10)], axis=0))
    final_df["Ecosystem Element"] = pd.DataFrame(np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], len(forecasting)))

    # calculate median 
    m = final_df.groupby(['Time', 'Ecosystem Element'])[['Abundance %']].apply(np.median)
    m.name = 'Median'
    final_df = final_df.join(m, on=['Time','Ecosystem Element'])
    # calculate quantiles - try graphing smaller percentiles on top 
    perc1 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(1) 
    perc1.name = 'onehundperc'
    final_df = final_df.join(perc1, on=['Time', 'Ecosystem Element'])
    perc2 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(0) 
    perc2.name = "zeroperc"
    final_df = final_df.join(perc2, on=['Time', 'Ecosystem Element'])
    # now show more quantiles, 95th
    perc3 = final_df.groupby(['Time',  'Ecosystem Element'])['Abundance %'].quantile(0.975) 
    perc3.name = 'ninetyfiveperc'
    final_df = final_df.join(perc3, on=['Time',  'Ecosystem Element'])
    perc4 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(0.025)
    perc4.name = "fiveperc"
    final_df = final_df.join(perc4, on=['Time', 'Ecosystem Element'])
    # and 80th
    perc5 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(0.9)
    perc5.name = 'eightyperc'
    final_df = final_df.join(perc5, on=['Time',  'Ecosystem Element'])
    perc6 = final_df.groupby(['Time', 'Ecosystem Element'])['Abundance %'].quantile(0.1)
    perc6.name = "twentyperc"
    final_df = final_df.join(perc6, on=['Time', 'Ecosystem Element'])

    final_df = final_df.reset_index(drop=True)
    final_df.to_csv("RC_high_herbivory.csv")

    f = sns.FacetGrid(final_df, col="Ecosystem Element", palette = palette, col_wrap=4, sharey = False)
    f.map(sns.lineplot, 'Time', 'Median')
    f.map(sns.lineplot, 'Time', 'onehundperc')
    f.map(sns.lineplot, 'Time', 'zeroperc')
    # now other percentiles
    f.map(sns.lineplot, 'Time', 'Median')
    f.map(sns.lineplot, 'Time', 'ninetyfiveperc')
    f.map(sns.lineplot, 'Time', 'fiveperc')
    # now other percentiles
    f.map(sns.lineplot, 'Time', 'Median')
    f.map(sns.lineplot, 'Time', 'eightyperc')
    f.map(sns.lineplot, 'Time', 'twentyperc')

    for ax in f.axes.flat:
        ax.fill_between(ax.lines[1].get_xdata(),ax.lines[1].get_ydata(), ax.lines[2].get_ydata(),  color="blue",alpha =0.2)
        # 95 perc
        ax.fill_between(ax.lines[4].get_xdata(),ax.lines[4].get_ydata(), ax.lines[5].get_ydata(),  color="yellow",alpha =0.2)
        # 80 perc
        ax.fill_between(ax.lines[7].get_xdata(),ax.lines[7].get_ydata(), ax.lines[8].get_ydata(),  color="green",alpha =0.2)
        ax.set_ylabel('Abundance')
        ax.set_xlabel('Time (Months)')

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

    f.fig.suptitle('Reality Check: Vegetation dynamics with high herbivory')
    plt.tight_layout()
    plt.savefig('RC_high_herbivory.png')
    plt.show()



# reality_high_herbivory()





## finally, look at spatial movements of herbivores within habitat types
def reality_space():

    # visualise the best run
    accepted_parameters = pd.read_csv('best_parameter_set.csv') 
    accepted_parameters.drop(['Unnamed: 0'], axis=1, inplace=True)

    # take the accepted parameters, and go row by row, running the model

    chance_reproduceSapling = accepted_parameters["chance_reproduceSapling"].item()
    chance_reproduceYoungScrub =  accepted_parameters["chance_reproduceYoungScrub"].item()
    chance_regrowGrass =  accepted_parameters["chance_regrowGrass"].item()
    chance_saplingBecomingTree =  accepted_parameters["chance_saplingBecomingTree"].item()
    chance_youngScrubMatures =  accepted_parameters["chance_youngScrubMatures"].item()
    chance_scrubOutcompetedByTree =  accepted_parameters["chance_scrubOutcompetedByTree"].item()
    chance_grassOutcompetedByTree =  accepted_parameters["chance_grassOutcompetedByTree"].item()
    chance_grassOutcompetedByScrub = accepted_parameters["chance_grassOutcompetedByScrub"].item()

    initial_roe = 12
    fallowDeer_stocking = 247
    cattle_stocking = 81
    redDeer_stocking = 35
    tamworthPig_stocking = 7
    exmoor_stocking = 15

    roe_deer_reproduce = accepted_parameters["roe_deer_reproduce"].item()
    roe_deer_gain_from_grass =  accepted_parameters["roe_deer_gain_from_grass"].item()
    roe_deer_gain_from_trees =  accepted_parameters["roe_deer_gain_from_trees"].item()
    roe_deer_gain_from_scrub =  accepted_parameters["roe_deer_gain_from_scrub"].item()
    roe_deer_gain_from_saplings =  accepted_parameters["roe_deer_gain_from_saplings"].item()
    roe_deer_gain_from_young_scrub =  accepted_parameters["roe_deer_gain_from_young_scrub"].item()
    ponies_gain_from_grass =  accepted_parameters["ponies_gain_from_grass"].item()
    ponies_gain_from_trees =  accepted_parameters["ponies_gain_from_trees"].item()
    ponies_gain_from_scrub =  accepted_parameters["ponies_gain_from_scrub"].item()
    ponies_gain_from_saplings =  accepted_parameters["ponies_gain_from_saplings"].item()
    ponies_gain_from_young_scrub =  accepted_parameters["ponies_gain_from_young_scrub"].item()
    cattle_reproduce =  accepted_parameters["cattle_reproduce"].item()
    cows_gain_from_grass =  accepted_parameters["cows_gain_from_grass"].item()
    cows_gain_from_trees =  accepted_parameters["cows_gain_from_trees"].item()
    cows_gain_from_scrub =  accepted_parameters["cows_gain_from_scrub"].item()
    cows_gain_from_saplings =  accepted_parameters["cows_gain_from_saplings"].item()
    cows_gain_from_young_scrub =  accepted_parameters["cows_gain_from_young_scrub"].item()
    fallow_deer_reproduce =  accepted_parameters["fallow_deer_reproduce"].item()
    fallow_deer_gain_from_grass =  accepted_parameters["fallow_deer_gain_from_grass"].item()
    fallow_deer_gain_from_trees =  accepted_parameters["fallow_deer_gain_from_trees"].item()
    fallow_deer_gain_from_scrub =  accepted_parameters["fallow_deer_gain_from_scrub"].item()
    fallow_deer_gain_from_saplings =  accepted_parameters["fallow_deer_gain_from_saplings"].item()
    fallow_deer_gain_from_young_scrub =  accepted_parameters["fallow_deer_gain_from_young_scrub"] .item()  
    red_deer_reproduce =  accepted_parameters["red_deer_reproduce"].item()
    red_deer_gain_from_grass =  accepted_parameters["red_deer_gain_from_grass"].item()
    red_deer_gain_from_trees =  accepted_parameters["red_deer_gain_from_trees"].item()
    red_deer_gain_from_scrub =  accepted_parameters["red_deer_gain_from_scrub"].item()
    red_deer_gain_from_saplings =  accepted_parameters["red_deer_gain_from_saplings"].item()
    red_deer_gain_from_young_scrub =  accepted_parameters["red_deer_gain_from_young_scrub"].item()
    tamworth_pig_reproduce =  accepted_parameters["tamworth_pig_reproduce"].item()
    tamworth_pig_gain_from_grass =  accepted_parameters["tamworth_pig_gain_from_grass"].item()
    tamworth_pig_gain_from_trees = accepted_parameters["tamworth_pig_gain_from_trees"].item()
    tamworth_pig_gain_from_scrub = accepted_parameters["tamworth_pig_gain_from_scrub"].item()
    tamworth_pig_gain_from_saplings =  accepted_parameters["tamworth_pig_gain_from_saplings"].item()
    tamworth_pig_gain_from_young_scrub =  accepted_parameters["tamworth_pig_gain_from_young_scrub"].item()


    # euro bison parameters
    european_bison_reproduce = random.uniform(cattle_reproduce-(cattle_reproduce*0.1), cattle_reproduce+(cattle_reproduce*0.1))
    # bison should have higher impact than any other consumer
    european_bison_gain_from_grass = random.uniform(cows_gain_from_grass, cows_gain_from_grass+(cows_gain_from_grass*0.1))
    european_bison_gain_from_trees =random.uniform(cows_gain_from_trees, cows_gain_from_trees+(cows_gain_from_trees*0.1))
    european_bison_gain_from_scrub =random.uniform(cows_gain_from_scrub, cows_gain_from_scrub+(cows_gain_from_scrub*0.1))
    european_bison_gain_from_saplings = random.uniform(cows_gain_from_saplings, cows_gain_from_saplings+(cows_gain_from_saplings*0.1))
    european_bison_gain_from_young_scrub = random.uniform(cows_gain_from_young_scrub, cows_gain_from_young_scrub+(cows_gain_from_young_scrub*0.1))
    # euro elk parameters
    european_elk_reproduce = random.uniform(red_deer_reproduce-(red_deer_reproduce*0.1), red_deer_reproduce+(red_deer_reproduce*0.1))
    # bison should have higher impact than any other consumer
    european_elk_gain_from_grass =  random.uniform(red_deer_gain_from_grass-(red_deer_gain_from_grass*0.1), red_deer_gain_from_grass)
    european_elk_gain_from_trees = random.uniform(red_deer_gain_from_trees-(red_deer_gain_from_trees*0.1), red_deer_gain_from_trees)
    european_elk_gain_from_scrub = random.uniform(red_deer_gain_from_scrub-(red_deer_gain_from_scrub*0.1), red_deer_gain_from_scrub)
    european_elk_gain_from_saplings =  random.uniform(red_deer_gain_from_saplings-(red_deer_gain_from_saplings*0.1), red_deer_gain_from_saplings)
    european_elk_gain_from_young_scrub =  random.uniform(red_deer_gain_from_young_scrub-(red_deer_gain_from_young_scrub*0.1), red_deer_gain_from_young_scrub)
    # reindeer parameters
    reindeer_reproduce = 0
    # reindeer should have impacts between red and fallow deer
    reindeer_gain_from_grass = 0
    reindeer_gain_from_trees =0
    reindeer_gain_from_scrub =0
    reindeer_gain_from_saplings = 0
    reindeer_gain_from_young_scrub = 0
    # forecasting parameters
    fallowDeer_stocking_forecast = 247
    cattle_stocking_forecast = 81
    redDeer_stocking_forecast = 35
    tamworthPig_stocking_forecast = 7
    exmoor_stocking_forecast = 15
    introduced_species_stocking_forecast = 0
    chance_scrub_saves_saplings = accepted_parameters["chance_scrub_saves_saplings"].item()

    random.seed(1)
    np.random.seed(1)


    model = KneppModel(initial_roe, roe_deer_reproduce, roe_deer_gain_from_saplings, roe_deer_gain_from_trees, roe_deer_gain_from_scrub, roe_deer_gain_from_young_scrub, roe_deer_gain_from_grass,
                        chance_youngScrubMatures, chance_saplingBecomingTree, chance_reproduceSapling,chance_reproduceYoungScrub, chance_regrowGrass, 
                        chance_grassOutcompetedByTree, chance_grassOutcompetedByScrub, chance_scrubOutcompetedByTree, 
                        ponies_gain_from_saplings, ponies_gain_from_trees, ponies_gain_from_scrub, ponies_gain_from_young_scrub, ponies_gain_from_grass, 
                        cattle_reproduce, cows_gain_from_grass, cows_gain_from_trees, cows_gain_from_scrub, cows_gain_from_saplings, cows_gain_from_young_scrub, 
                        fallow_deer_reproduce, fallow_deer_gain_from_saplings, fallow_deer_gain_from_trees, fallow_deer_gain_from_scrub, fallow_deer_gain_from_young_scrub, fallow_deer_gain_from_grass,
                        red_deer_reproduce, red_deer_gain_from_saplings, red_deer_gain_from_trees, red_deer_gain_from_scrub, red_deer_gain_from_young_scrub, red_deer_gain_from_grass,
                        tamworth_pig_reproduce, tamworth_pig_gain_from_saplings,tamworth_pig_gain_from_trees,tamworth_pig_gain_from_scrub,tamworth_pig_gain_from_young_scrub,tamworth_pig_gain_from_grass,
                        european_bison_reproduce, european_bison_gain_from_grass, european_bison_gain_from_trees, european_bison_gain_from_scrub, european_bison_gain_from_saplings, european_bison_gain_from_young_scrub,
                        european_elk_reproduce, european_elk_gain_from_grass, european_elk_gain_from_trees, european_elk_gain_from_scrub, european_elk_gain_from_saplings, european_elk_gain_from_young_scrub,
                        reindeer_reproduce, reindeer_gain_from_grass, reindeer_gain_from_trees, reindeer_gain_from_scrub, reindeer_gain_from_saplings, reindeer_gain_from_young_scrub,
                        fallowDeer_stocking, cattle_stocking, redDeer_stocking, tamworthPig_stocking, exmoor_stocking,
                        fallowDeer_stocking_forecast, cattle_stocking_forecast, redDeer_stocking_forecast, tamworthPig_stocking_forecast, exmoor_stocking_forecast, introduced_species_stocking_forecast,
                        chance_scrub_saves_saplings,
                        max_time = 185, reintroduction = True, introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)

    model.reset_randomizer(seed=1)
    model.run_model()


    # remember the results of the model (dominant conditions, # of agents)
    results2 = model.datacollector.get_agent_vars_dataframe()


    # first extract the habitats (polygons)
    habitats_only_pol = results2.loc[(results2['Breed'] == 'grassland') | (results2['Breed'] =='woodland') | (results2['Breed'] =='thorny_scrubland') | (results2['Breed'] =='bare_ground')]
    # count how many times per species    
    habitats_only_pol.Geometry= habitats_only_pol.Geometry.astype(str)
    new_habs = habitats_only_pol.groupby(['Geometry','Breed'])["ID"].count().reset_index(name="count")
    # convert to geodataframe
    new_habs['geometry'] = new_habs['Geometry'].apply(wkt.loads)
    new_habs.Breed.dtype
    new_habs = GeoDataFrame(new_habs, crs="EPSG:3015")


    # now consumers
    consumers_only = results2.loc[(results2['Breed'] == 'roe_deer_agent') | (results2['Breed'] =='exmoor_pony_agent') | (results2['Breed'] =='longhorn_cattle_agent') | (results2['Breed'] =='tamworth_pig_agent') | (results2['Breed'] =='fallow_deer_agent') | (results2['Breed'] =='red_deer_agent')]
        
    # count how many times per species    
    # consumers_only.Geometry= consumers_only.Geometry.astype(str)
    # new_consumers = consumers_only.groupby(['Geometry','Breed'])["ID"].count().reset_index(name="count")
    # convert to geodataframe
    # new_consumers['geometry'] = new_consumers['Geometry'].apply(wkt.loads)
    consumers_only['geometry'] = consumers_only['Geometry']
    # new_consumers = GeoDataFrame(new_consumers, crs="EPSG:3015")
    new_consumers = GeoDataFrame(consumers_only, crs="EPSG:3015")


    # concat
    combined_dfs = pd.concat([new_habs, new_consumers])


    # now plot it, wrapped by vegetation type
    sf = gpd.read_file('cleaned_shp.shp', crs="EPSG:3015")


    fig, axes = plt.subplots(1,3, figsize=(18,4), sharex=True, sharey=False)

    for (breed, group), ax in zip(new_habs.groupby(new_habs.Breed), axes.flatten()):
        sf.plot(ax=ax, color='white', edgecolor='black')
        group.plot(column='count',
                    cmap='Blues', 
                    ax=ax, 
                    legend=True)
        ax.axis('off'),
        ax.set_title(breed)
    plt.suptitle("Model vegetation composition from 2005-2020, without reintroductions")
    plt.tight_layout()
    plt.savefig('heatmap_veg.png')
    plt.show()


    fig, axes = plt.subplots(2,3, figsize=(18,12), sharex=True, sharey=False)
    for (breed, group), ax in zip(new_consumers.groupby(new_consumers.Breed), axes.flatten()):
        sf.plot(ax=ax, color='white', edgecolor='black')
        group.plot("geometry", 
            cmap='Blues', 
            ax=ax, 
            legend=False)
        ax.axis('off'),
        ax.set_title(breed)
    plt.suptitle("Consumer locations from 2005-2020")
    plt.tight_layout()
    plt.savefig('heatmap_consumers.png')
    plt.show()


# reality_space()