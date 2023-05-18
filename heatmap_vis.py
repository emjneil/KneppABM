# ------ ABM of the Knepp Estate (2005-2046) --------
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


# # # # Run the model # # # # 

def run_heatmap():

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
                        max_time = 185, reintroduction = False, introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)

    model.reset_randomizer(seed=1)
    model.run_model()


    # remember the results of the model (dominant conditions, # of agents)
    results2 = model.datacollector.get_agent_vars_dataframe()


    results_3 = model.datacollector.get_model_vars_dataframe()

    filtered = results_3.loc[(results_3['Time'] == 183)]

    print(filtered)
    print(filtered.iloc[0]['Thorny Scrub'])
    print(filtered.iloc[0]['Woodland'])
    print(filtered.iloc[0]['Grassland'])
    print(filtered.iloc[0]['Roe deer'])


    woodland_from_scrub = results_3["Woodland regenerated in scrub"].sum()
    woodland_from_other = results_3["Woodland regenerated elsewhere"].sum()
    total_regeneration = woodland_from_scrub + woodland_from_other

    print("from scrub", woodland_from_scrub/total_regeneration, "from other", woodland_from_other/total_regeneration, total_regeneration )


    # first extract the habitats (polygons)
    habitats_only_pol = results2.loc[(results2['Breed'] == 'grassland') | (results2['Breed'] =='woodland') | (results2['Breed'] =='thorny_scrubland') | (results2['Breed'] =='bare_ground')]
    # count how many times per species    
    habitats_only_pol.Geometry= habitats_only_pol.Geometry.astype(str)
    new_habs = habitats_only_pol.groupby(['Geometry','Breed'])["ID"].count().reset_index(name="count")
    # convert to geodataframe
    new_habs['geometry'] = new_habs['Geometry'].apply(wkt.loads)
    new_habs = GeoDataFrame(new_habs, crs="EPSG:3015")



    # now plot it, wrapped by vegetation type
    sf = gpd.read_file('cleaned_shp.shp', crs="EPSG:3015")


    fig, axes = plt.subplots(1, new_habs.Breed.nunique(), figsize=(18,4), sharex=True, sharey=True)

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
    plt.savefig('heatmap_counter.png')
    plt.show()




run_heatmap()




def check_dominant_condition():

    accepted_parameters = pd.read_csv('combined_accepted_parameters.csv') 

    woodland_from_scrub = []
    woodland_from_other = []
    total_regeneration = []

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
                            max_time = 185, reintroduction = True, introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)


        model.reset_randomizer(seed=1)

        model.run_model()

        run_number +=1
        print(run_number)

        results_3 = model.datacollector.get_model_vars_dataframe()
        woodland_from_scrub.append(results_3["Woodland regenerated in scrub"].sum())
        woodland_from_other.append(results_3["Woodland regenerated elsewhere"].sum())
        total_regeneration.append((results_3["Woodland regenerated in scrub"].sum()) + (results_3["Woodland regenerated elsewhere"].sum()))
    
    
    print("average from scrub", ((sum(woodland_from_scrub)/run_number))/(sum(total_regeneration)/run_number))
    print("average from other", ((sum(woodland_from_other)/run_number))/(sum(total_regeneration)/run_number))



# check_dominant_condition()