from KneppModel_ABM import KneppModel, roeDeer_agent, habitatAgent
import numpy as np
import random
import pandas as pd
import timeit


# # # ----- Create a model with agents and run it for 10 steps -----

def run_model():

    # time the program
    start = timeit.default_timer()

    # define number of simulationsz
    number_simulations = 10
    # time for first ODE (2005-2009, ~ 48 months)
    time_firstModel = 48
    # make list of variables

    final_results_list = []
    final_parameters = []
    run_number = 0

    # run the model for 48 months, 10 times
    for _ in range(number_simulations):
        # keep track of the runs
        run_number +=1
        # define parameters
        initial_roeDeer = random.randint(1, 12)
        initial_grassland = random.randint(70, 90)
        initial_woodland = random.randint(9, 19)
        initial_scrubland = random.randint(0, 2)
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
        roeDeer_saplingsEaten = random.randint(0,1000)
        roeDeer_youngScrubEaten = random.randint(0,1000)
        roeDeer_treesEaten = random.randint(0,100)
        roeDeer_scrubEaten = random.randint(0,100)

        # parameters = generate_parameters()
        parameters_used = [
            run_number,
            chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
            chance_scrubOutcompetedByTree, chance_grassOutcompetedByTreeScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
            initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland,
            roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub, 
            roeDeer_impactGrass, roeDeer_saplingsEaten, roeDeer_youngScrubEaten, roeDeer_treesEaten, roeDeer_scrubEaten
            ]
        # remember parameters used 
        final_parameters.append(parameters_used)


        # run the model 
        model = KneppModel(
            chance_reproduceSapling, chance_reproduceYoungScrub, chance_regrowGrass, chance_saplingBecomingTree, chance_youngScrubMatures, 
            chance_scrubOutcompetedByTree, chance_grassOutcompetedByTreeScrub, chance_saplingOutcompetedByTree, chance_saplingOutcompetedByScrub, chance_youngScrubOutcompetedByScrub, chance_youngScrubOutcompetedByTree,
            initial_roeDeer, initial_grassland, initial_woodland, initial_scrubland,
            roeDeer_reproduce, roeDeer_gain_from_grass, roeDeer_gain_from_Trees, roeDeer_gain_from_Scrub, roeDeer_gain_from_Saplings, roeDeer_gain_from_YoungScrub,
            roeDeer_impactGrass, roeDeer_saplingsEaten, roeDeer_youngScrubEaten, roeDeer_treesEaten, roeDeer_scrubEaten,
            width = 10, height = 10)
        
        # run for 48 months (2005-2009)
        for _ in range(time_firstModel): 
            # run the model
            model.step()

        # remember the results
        results = model.datacollector.get_model_vars_dataframe()
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
        "roeDeer_scrubEaten"
        ]

    final_parameters = pd.DataFrame(data=final_parameters, columns=variables)

    # filter those with the correct parameters in 2009
    accepted_runs = final_results[(final_results["Time"] == 48) & 
                                (final_results["Roe deer"] <= 40) & (final_results["Roe deer"] >= 12) &
                                (final_results["Grassland"] <= 80) & (final_results["Grassland"] >= 49) &
                                (final_results["Woodland"] <= 27) & (final_results["Woodland"] >= 7) &
                                (final_results["Thorny Scrub"] <= 21) & (final_results["Thorny Scrub"] >= 1)
                                ]

    with pd.option_context('display.max_columns',None):
        print(final_results[(final_results["Time"] == 48)])

    with pd.option_context('display.max_rows',None):
        print("accepted_runs: \n", accepted_runs)

    # with pd.option_context('display.max_columns',None):
    #     print(final_parameters)

    # calculate the time it takes to run
    stop = timeit.default_timer()

    print('Total time (min): ', (stop - start)/60)
        


run_model()