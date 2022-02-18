# ------ ABM of the Knepp Estate (2005-2046) --------
from KneppModel_ABM import KneppModel 
from differentialEvolution import run_optimizer
import numpy as np
import random
import pandas as pd


# # # # Run the model # # # # 


def run_all_models():
    output_parameters = run_optimizer()

    # define number of simulations
    number_simulations =  10
    # make list of variables
    final_results_list = []
    final_parameters = []
    run_number = 0


    for _ in range(number_simulations):
        # keep track of the runs
        run_number +=1
        print(run_number)
        # choose my percent above/below number
        perc_aboveBelow = 0.1
        
        # habitats
        # define the parameters
        chance_reproduceSapling =output_parameters[0]
        chance_reproduceYoungScrub = output_parameters[1]
        chance_regrowGrass =output_parameters[2]
        chance_saplingBecomingTree = output_parameters[3]
        chance_youngScrubMatures = output_parameters[4]
        chance_scrubOutcompetedByTree =output_parameters[5]
        chance_grassOutcompetedByTree =output_parameters[6]
        chance_grassOutcompetedByScrub = output_parameters[7]
        chance_saplingOutcompetedByTree = output_parameters[8]
        chance_saplingOutcompetedByScrub = output_parameters[9]
        chance_youngScrubOutcompetedByScrub =output_parameters[10]
        chance_youngScrubOutcompetedByTree =output_parameters[11]
        # initial values
        initial_roeDeer = 0.12
        initial_grassland = 0.8
        initial_woodland = 0.14
        initial_scrubland = 0.01
        roeDeer_reproduce = output_parameters[12]
        roeDeer_gain_from_grass = output_parameters[13]
        roeDeer_gain_from_Trees = output_parameters[14]
        roeDeer_gain_from_Scrub = output_parameters[15]
        roeDeer_gain_from_Saplings =output_parameters[16]
        roeDeer_gain_from_YoungScrub =output_parameters[17]
        fallowDeer_reproduce = output_parameters[18]
        fallowDeer_gain_from_grass = output_parameters[19]
        fallowDeer_gain_from_Trees =output_parameters[20]
        fallowDeer_gain_from_Scrub = output_parameters[21]
        fallowDeer_gain_from_Saplings = output_parameters[22]
        fallowDeer_gain_from_YoungScrub = output_parameters[23]
        redDeer_reproduce =output_parameters[24]
        redDeer_gain_from_grass = output_parameters[25]
        redDeer_gain_from_Trees = output_parameters[26]
        redDeer_gain_from_Scrub = output_parameters[27]
        redDeer_gain_from_Saplings = output_parameters[28]
        redDeer_gain_from_YoungScrub = output_parameters[29]
        ponies_gain_from_grass = output_parameters[30]
        ponies_gain_from_Trees = output_parameters[31]
        ponies_gain_from_Scrub = output_parameters[32]
        ponies_gain_from_Saplings = output_parameters[33]
        ponies_gain_from_YoungScrub = output_parameters[34]
        cows_reproduce = output_parameters[35]
        cows_gain_from_grass = output_parameters[36]
        cows_gain_from_Trees = output_parameters[37]
        cows_gain_from_Scrub = output_parameters[38]
        cows_gain_from_Saplings = output_parameters[39]
        cows_gain_from_YoungScrub = output_parameters[40]
        pigs_reproduce = output_parameters[41]
        pigs_gain_from_grass = output_parameters[42]
        pigs_gain_from_Trees = output_parameters[43]
        pigs_gain_from_Scrub = output_parameters[44]
        pigs_gain_from_Saplings =output_parameters[45]
        pigs_gain_from_YoungScrub =output_parameters[46]
        max_start_saplings = 0.1
        max_start_youngScrub = 0.1


        chance_reproduceSapling = random.uniform(output_parameters["variable"][0]-(output_parameters["variable"][0]*perc_aboveBelow), output_parameters["variable"][0]+(output_parameters["variable"][0]*perc_aboveBelow))
        chance_reproduceYoungScrub = random.uniform(output_parameters["variable"][1]-(output_parameters["variable"][1]*perc_aboveBelow), output_parameters["variable"][1]+(output_parameters["variable"][1]*perc_aboveBelow))
        chance_regrowGrass = random.uniform(output_parameters["variable"][2]-(output_parameters["variable"][2]*perc_aboveBelow), output_parameters["variable"][2]+(output_parameters["variable"][2]*perc_aboveBelow))
        chance_saplingBecomingTree = random.uniform(output_parameters["variable"][3]-(output_parameters["variable"][3]*perc_aboveBelow), output_parameters["variable"][3]+(output_parameters["variable"][3]*perc_aboveBelow))
        chance_youngScrubMatures = random.uniform(output_parameters["variable"][4]-(output_parameters["variable"][4]*perc_aboveBelow), output_parameters["variable"][4]+(output_parameters["variable"][4]*perc_aboveBelow))
        chance_scrubOutcompetedByTree = random.uniform(output_parameters["variable"][5]-(output_parameters["variable"][5]*perc_aboveBelow), output_parameters["variable"][5]+(output_parameters["variable"][5]*perc_aboveBelow))
        chance_grassOutcompetedByTree = random.uniform(output_parameters["variable"][6]-(output_parameters["variable"][6]*perc_aboveBelow),output_parameters["variable"][6]+(output_parameters["variable"][6]*perc_aboveBelow))
        chance_grassOutcompetedByScrub = random.uniform(output_parameters["variable"][7]-(output_parameters["variable"][7]*perc_aboveBelow), output_parameters["variable"][7]+(output_parameters["variable"][7]*perc_aboveBelow))
        chance_saplingOutcompetedByTree = random.uniform(output_parameters["variable"][8]-(output_parameters["variable"][8]*perc_aboveBelow), output_parameters["variable"][8]+(output_parameters["variable"][8]*perc_aboveBelow))
        chance_saplingOutcompetedByScrub = random.uniform(output_parameters["variable"][9]-(output_parameters["variable"][9]*perc_aboveBelow), output_parameters["variable"][9]+(output_parameters["variable"][9]*perc_aboveBelow))
        chance_youngScrubOutcompetedByScrub = random.uniform(output_parameters["variable"][10]-(output_parameters["variable"][10]*perc_aboveBelow), output_parameters["variable"][10]+(output_parameters["variable"][10]*perc_aboveBelow))
        chance_youngScrubOutcompetedByTree = random.uniform(output_parameters["variable"][11]-(output_parameters["variable"][11]*perc_aboveBelow), output_parameters["variable"][11]+(output_parameters["variable"][11]*perc_aboveBelow))
        # roe deer
        roeDeer_reproduce = random.uniform((output_parameters["variable"][12]-(output_parameters["variable"][12]*perc_aboveBelow)), (output_parameters["variable"][12]+(output_parameters["variable"][12]*perc_aboveBelow)))
        roeDeer_gain_from_grass = random.uniform((output_parameters["variable"][13]-(output_parameters["variable"][13]*perc_aboveBelow)), (output_parameters["variable"][13]+(output_parameters["variable"][13]*perc_aboveBelow)))
        roeDeer_gain_from_Trees = random.uniform((output_parameters["variable"][14]-(output_parameters["variable"][14]*perc_aboveBelow)), (output_parameters["variable"][14]+(output_parameters["variable"][14]*perc_aboveBelow)))
        roeDeer_gain_from_Scrub = random.uniform((output_parameters["variable"][15]-(output_parameters["variable"][15]*perc_aboveBelow)), (output_parameters["variable"][15]+(output_parameters["variable"][15]*perc_aboveBelow)))
        roeDeer_gain_from_Saplings = random.uniform((output_parameters["variable"][16]-(output_parameters["variable"][16]*perc_aboveBelow)), (output_parameters["variable"][16]+(output_parameters["variable"][16]*perc_aboveBelow)))
        roeDeer_gain_from_YoungScrub = random.uniform((output_parameters["variable"][17]-(output_parameters["variable"][17]*perc_aboveBelow)), (output_parameters["variable"][17]+(output_parameters["variable"][17]*perc_aboveBelow)))
        # Fallow deer
        fallowDeer_reproduce = random.uniform((output_parameters["variable"][18]-(output_parameters["variable"][18]*perc_aboveBelow)), (output_parameters["variable"][18]+(output_parameters["variable"][18]*perc_aboveBelow)))
        fallowDeer_gain_from_grass = random.uniform((output_parameters["variable"][19]-(output_parameters["variable"][19]*perc_aboveBelow)), (output_parameters["variable"][19]+(output_parameters["variable"][19]*perc_aboveBelow)))
        fallowDeer_gain_from_Trees = random.uniform((output_parameters["variable"][20]-(output_parameters["variable"][20]*perc_aboveBelow)), (output_parameters["variable"][20]+(output_parameters["variable"][20]*perc_aboveBelow)))
        fallowDeer_gain_from_Scrub = random.uniform((output_parameters["variable"][21]-(output_parameters["variable"][21]*perc_aboveBelow)), (output_parameters["variable"][21]+(output_parameters["variable"][21]*perc_aboveBelow)))
        fallowDeer_gain_from_Saplings = random.uniform((output_parameters["variable"][22]-(output_parameters["variable"][22]*perc_aboveBelow)), (output_parameters["variable"][22]+(output_parameters["variable"][22]*perc_aboveBelow)))
        fallowDeer_gain_from_YoungScrub = random.uniform((output_parameters["variable"][23]-(output_parameters["variable"][23]*perc_aboveBelow)), (output_parameters["variable"][23]+(output_parameters["variable"][23]*perc_aboveBelow)))
         # Red deer
        redDeer_reproduce = random.uniform((output_parameters["variable"][24]-(output_parameters["variable"][24]*perc_aboveBelow)), (output_parameters["variable"][24]+(output_parameters["variable"][24]*perc_aboveBelow)))
        redDeer_gain_from_grass = random.uniform((output_parameters["variable"][25]-(output_parameters["variable"][25]*perc_aboveBelow)), (output_parameters["variable"][25]+(output_parameters["variable"][25]*perc_aboveBelow)))
        redDeer_gain_from_Trees = random.uniform((output_parameters["variable"][26]-(output_parameters["variable"][26]*perc_aboveBelow)), (output_parameters["variable"][26]+(output_parameters["variable"][26]*perc_aboveBelow)))
        redDeer_gain_from_Scrub = random.uniform((output_parameters["variable"][27]-(output_parameters["variable"][27]*perc_aboveBelow)), (output_parameters["variable"][27]+(output_parameters["variable"][27]*perc_aboveBelow)))
        redDeer_gain_from_Saplings = random.uniform((output_parameters["variable"][28]-(output_parameters["variable"][28]*perc_aboveBelow)), (output_parameters["variable"][28]+(output_parameters["variable"][28]*perc_aboveBelow)))
        redDeer_gain_from_YoungScrub = random.uniform((output_parameters["variable"][29]-(output_parameters["variable"][29]*perc_aboveBelow)), (output_parameters["variable"][29]+(output_parameters["variable"][29]*perc_aboveBelow)))
        # Exmoor ponies
        ponies_gain_from_grass = random.uniform((output_parameters["variable"][30]-(output_parameters["variable"][30]*perc_aboveBelow)), (output_parameters["variable"][30]+(output_parameters["variable"][30]*perc_aboveBelow)))
        ponies_gain_from_Trees = random.uniform((output_parameters["variable"][31]-(output_parameters["variable"][31]*perc_aboveBelow)), (output_parameters["variable"][31]+(output_parameters["variable"][31]*perc_aboveBelow)))
        ponies_gain_from_Scrub = random.uniform((output_parameters["variable"][32]-(output_parameters["variable"][32]*perc_aboveBelow)), (output_parameters["variable"][32]+(output_parameters["variable"][32]*perc_aboveBelow)))
        ponies_gain_from_Saplings = random.uniform((output_parameters["variable"][33]-(output_parameters["variable"][33]*perc_aboveBelow)), (output_parameters["variable"][33]+(output_parameters["variable"][33]*perc_aboveBelow)))
        ponies_gain_from_YoungScrub = random.uniform((output_parameters["variable"][34]-(output_parameters["variable"][34]*perc_aboveBelow)), (output_parameters["variable"][34]+(output_parameters["variable"][34]*perc_aboveBelow)))
        # Longhorn cattle
        cows_reproduce = random.uniform((output_parameters["variable"][35]-(output_parameters["variable"][35]*perc_aboveBelow)), (output_parameters["variable"][35]+(output_parameters["variable"][35]*perc_aboveBelow)))
        cows_gain_from_grass = random.uniform((output_parameters["variable"][36]-(output_parameters["variable"][36]*perc_aboveBelow)), (output_parameters["variable"][36]+(output_parameters["variable"][36]*perc_aboveBelow)))
        cows_gain_from_Trees = random.uniform((output_parameters["variable"][37]-(output_parameters["variable"][37]*perc_aboveBelow)), (output_parameters["variable"][37]+(output_parameters["variable"][37]*perc_aboveBelow)))
        cows_gain_from_Scrub = random.uniform((output_parameters["variable"][38]-(output_parameters["variable"][38]*perc_aboveBelow)), (output_parameters["variable"][38]+(output_parameters["variable"][38]*perc_aboveBelow)))
        cows_gain_from_Saplings = random.uniform((output_parameters["variable"][39]-(output_parameters["variable"][39]*perc_aboveBelow)), (output_parameters["variable"][39]+(output_parameters["variable"][39]*perc_aboveBelow)))
        cows_gain_from_YoungScrub = random.uniform((output_parameters["variable"][40]-(output_parameters["variable"][40]*perc_aboveBelow)), (output_parameters["variable"][40]+(output_parameters["variable"][40]*perc_aboveBelow)))
        # Tamworth pigs
        pigs_reproduce = random.uniform((output_parameters["variable"][41]-(output_parameters["variable"][41]*perc_aboveBelow)), (output_parameters["variable"][41]+(output_parameters["variable"][41]*perc_aboveBelow)))
        pigs_gain_from_grass = random.uniform((output_parameters["variable"][42]-(output_parameters["variable"][42]*perc_aboveBelow)), (output_parameters["variable"][42]+(output_parameters["variable"][42]*perc_aboveBelow)))
        pigs_gain_from_Saplings = random.uniform((output_parameters["variable"][43]-(output_parameters["variable"][43]*perc_aboveBelow)), (output_parameters["variable"][43]+(output_parameters["variable"][43]*perc_aboveBelow)))
        pigs_gain_from_YoungScrub = random.uniform((output_parameters["variable"][44]-(output_parameters["variable"][44]*perc_aboveBelow)), (output_parameters["variable"][44]+(output_parameters["variable"][44]*perc_aboveBelow)))
        # impact grass
        roeDeer_impactGrass = random.randint(round(output_parameters["variable"][45]-(output_parameters["variable"][45]*perc_aboveBelow)), round(output_parameters["variable"][45]+(output_parameters["variable"][45]*perc_aboveBelow)))
        fallowDeer_impactGrass = random.randint(round(output_parameters["variable"][46]-(output_parameters["variable"][46]*perc_aboveBelow)),round(output_parameters["variable"][46]+(output_parameters["variable"][46]*perc_aboveBelow)))
        redDeer_impactGrass = random.randint(round(output_parameters["variable"][47]-(output_parameters["variable"][47]*perc_aboveBelow)), round(output_parameters["variable"][47]+(output_parameters["variable"][47]*perc_aboveBelow)))
        ponies_impactGrass = random.randint(round(output_parameters["variable"][48]-(output_parameters["variable"][48]*perc_aboveBelow)), round(output_parameters["variable"][48]+(output_parameters["variable"][48]*perc_aboveBelow)))
        cows_impactGrass = random.randint(round(output_parameters["variable"][49]-(output_parameters["variable"][49]*perc_aboveBelow)), round(output_parameters["variable"][49]+(output_parameters["variable"][49]*perc_aboveBelow)))
        pigs_impactGrass = random.randint(round(output_parameters["variable"][50]-(output_parameters["variable"][50]*perc_aboveBelow)), round(output_parameters["variable"][50]+(output_parameters["variable"][50]*perc_aboveBelow)))
        # impact saplings
        roeDeer_saplingsEaten = random.randint(round(output_parameters["variable"][51]-(output_parameters["variable"][51]*perc_aboveBelow)), round(output_parameters["variable"][51]+(output_parameters["variable"][51]*perc_aboveBelow)))
        fallowDeer_saplingsEaten = random.randint(round(output_parameters["variable"][52]-(output_parameters["variable"][52]*perc_aboveBelow)), round(output_parameters["variable"][52]+(output_parameters["variable"][52]*perc_aboveBelow)))
        redDeer_saplingsEaten = random.randint(round(output_parameters["variable"][53]-(output_parameters["variable"][53]*perc_aboveBelow)), round(output_parameters["variable"][53]+(output_parameters["variable"][53]*perc_aboveBelow)))
        ponies_saplingsEaten = random.randint(round(output_parameters["variable"][54]-(output_parameters["variable"][54]*perc_aboveBelow)), round(output_parameters["variable"][54]+(output_parameters["variable"][54]*perc_aboveBelow)))
        cows_saplingsEaten =  random.randint(round(output_parameters["variable"][55]-(output_parameters["variable"][55]*perc_aboveBelow)), round(output_parameters["variable"][55]+(output_parameters["variable"][55]*perc_aboveBelow)))
        pigs_saplingsEaten = random.randint(round(output_parameters["variable"][56]-(output_parameters["variable"][56]*perc_aboveBelow)), round(output_parameters["variable"][56]+(output_parameters["variable"][56]*perc_aboveBelow)))
        # impact young scrub
        roeDeer_youngScrubEaten = random.randint(round(output_parameters["variable"][57]-(output_parameters["variable"][57]*perc_aboveBelow)), round(output_parameters["variable"][57]+(output_parameters["variable"][57]*perc_aboveBelow)))
        fallowDeer_youngScrubEaten = random.randint(round(output_parameters["variable"][58]-(output_parameters["variable"][58]*perc_aboveBelow)), round(output_parameters["variable"][58]+(output_parameters["variable"][58]*perc_aboveBelow)))
        redDeer_youngScrubEaten = random.randint(round(output_parameters["variable"][59]-(output_parameters["variable"][59]*perc_aboveBelow)), round(output_parameters["variable"][59]+(output_parameters["variable"][59]*perc_aboveBelow)))
        ponies_youngScrubEaten = random.randint(round(output_parameters["variable"][60]-(output_parameters["variable"][60]*perc_aboveBelow)), round(output_parameters["variable"][60]+(output_parameters["variable"][60]*perc_aboveBelow)))
        cows_youngScrubEaten = random.randint(round(output_parameters["variable"][61]-(output_parameters["variable"][61]*perc_aboveBelow)), round(output_parameters["variable"][61]+(output_parameters["variable"][61]*perc_aboveBelow)))
        pigs_youngScrubEaten = random.randint(round(output_parameters["variable"][62]-(output_parameters["variable"][62]*perc_aboveBelow)), round(output_parameters["variable"][62]+(output_parameters["variable"][62]*perc_aboveBelow)))
        # impact scrub
        roeDeer_scrubEaten = random.randint(round(output_parameters["variable"][63]-(output_parameters["variable"][63]*perc_aboveBelow)), round(output_parameters["variable"][63]+(output_parameters["variable"][63]*perc_aboveBelow)))
        fallowDeer_scrubEaten = random.randint(round(output_parameters["variable"][64]-(output_parameters["variable"][64]*perc_aboveBelow)), round(output_parameters["variable"][64]+(output_parameters["variable"][64]*perc_aboveBelow)))
        redDeer_scrubEaten = random.randint(round(output_parameters["variable"][65]-(output_parameters["variable"][65]*perc_aboveBelow)), round(output_parameters["variable"][65]+(output_parameters["variable"][65]*perc_aboveBelow)))
        ponies_scrubEaten = random.randint(round(output_parameters["variable"][66]-(output_parameters["variable"][66]*perc_aboveBelow)), round(output_parameters["variable"][66]+(output_parameters["variable"][66]*perc_aboveBelow)))
        cows_scrubEaten = random.randint(round(output_parameters["variable"][67]-(output_parameters["variable"][67]*perc_aboveBelow)), round(output_parameters["variable"][67]+(output_parameters["variable"][67]*perc_aboveBelow)))
        # impact trees
        roeDeer_treesEaten = random.randint(round(output_parameters["variable"][68]-(output_parameters["variable"][68]*perc_aboveBelow)), round(output_parameters["variable"][68]+(output_parameters["variable"][68]*perc_aboveBelow)))
        fallowDeer_treesEaten = random.randint(round(output_parameters["variable"][69]-(output_parameters["variable"][69]*perc_aboveBelow)), round(output_parameters["variable"][69]+(output_parameters["variable"][69]*perc_aboveBelow)))
        redDeer_treesEaten = random.randint(round(output_parameters["variable"][70]-(output_parameters["variable"][70]*perc_aboveBelow)), round(output_parameters["variable"][70]+(output_parameters["variable"][70]*perc_aboveBelow)))
        ponies_treesEaten = random.randint(round(output_parameters["variable"][71]-(output_parameters["variable"][71]*perc_aboveBelow)), round(output_parameters["variable"][71]+(output_parameters["variable"][71]*perc_aboveBelow)))
        cows_treesEaten =  random.randint(round(output_parameters["variable"][72]-(output_parameters["variable"][72]*perc_aboveBelow)), round(output_parameters["variable"][72]+(output_parameters["variable"][72]*perc_aboveBelow)))

        
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

    # filter the runs and tag the dataframe
    # pre-reintroduction model
    accepted_preReintro = final_results[(final_results["Time"] == 49) &
    (final_results["Roe deer"] <= 40) & (final_results["Roe deer"] >= 6) &
    (final_results["Grassland"] <= 90) & (final_results["Grassland"] >= 49) & 
    (final_results["Woodland"] <= 27) & (final_results["Woodland"] >= 7) & 
    (final_results["Thorny Scrub"] <= 21) & (final_results["Thorny Scrub"] >= 1)]
    print("number passed pre-reintro filters:", len(accepted_preReintro))
    filtered_preReintro = final_results[final_results['run_number'].isin(accepted_preReintro['run_number'])]
    # April 2015
    accepted_April2015 = filtered_preReintro[(filtered_preReintro["Time"] == 123) &
    (filtered_preReintro["Exmoor pony"] <= 11) & (filtered_preReintro["Exmoor pony"] >= 9)]
    # (filtered_preReintro["Longhorn cattle"] <= 127) & (filtered_preReintro["Longhorn cattle"] >= 104) &
    # (filtered_preReintro["Tamworth pigs"] <= 24) & (filtered_preReintro["Tamworth pigs"] >= 20)]
    print("number passed April 2015 filters:", len(accepted_April2015))
    filtered_April2015 = filtered_preReintro[filtered_preReintro['run_number'].isin(accepted_April2015['run_number'])]
    # May 2015
    accepted_May2015 = filtered_April2015[(filtered_April2015["Time"] == 124) &
    # (filtered_April2015["Longhorn cattle"] <= 142) & (filtered_April2015["Longhorn cattle"] >= 116) &
    # (filtered_April2015["Tamworth pigs"] <= 15) & (filtered_April2015["Tamworth pigs"] >= 13) &
    (filtered_April2015["Exmoor pony"] <= 11) & (filtered_April2015["Exmoor pony"] >= 9)]
    print("number passed May 2015 filters:", len(accepted_May2015))
    filtered_May2015 = filtered_April2015[filtered_April2015['run_number'].isin(accepted_May2015['run_number'])]
    # June 2015
    accepted_June2015 = filtered_May2015[(filtered_May2015["Time"] == 125) &
    # (filtered_May2015["Longhorn cattle"] <= 142) & (filtered_May2015["Longhorn cattle"] >= 116) &
    (filtered_May2015["Exmoor pony"] <= 11) & (filtered_May2015["Exmoor pony"] >= 9)]
    # (filtered_May2015["Tamworth pigs"] <= 15) & (filtered_May2015["Tamworth pigs"] >= 13)]
    print("number passed June 2015 filters:", len(accepted_June2015))
    filtered_June2015 = filtered_May2015[filtered_May2015['run_number'].isin(accepted_June2015['run_number'])]
    # July 2015
    accepted_July2015 = filtered_June2015[(filtered_June2015["Time"] == 126) &
    # (filtered_June2015["Longhorn cattle"] <= 142) & (filtered_June2015["Longhorn cattle"] >= 116) &
    (filtered_June2015["Exmoor pony"] <= 11) & (filtered_June2015["Exmoor pony"] >= 9)]
    # (filtered_June2015["Tamworth pigs"] <= 15) & (filtered_June2015["Tamworth pigs"] >= 13)]
    print("number passed July 2015 filters:", len(accepted_July2015))
    filtered_July2015 = filtered_June2015[filtered_June2015['run_number'].isin(accepted_July2015['run_number'])]
    # Aug 2015
    accepted_Aug2015 = filtered_July2015[(filtered_July2015["Time"] == 127) &
    # (filtered_July2015["Longhorn cattle"] <= 142) & (filtered_July2015["Longhorn cattle"] >= 116) &
    (filtered_July2015["Exmoor pony"] <= 11) & (filtered_July2015["Exmoor pony"] >= 9)]
    # (filtered_July2015["Tamworth pigs"] <= 15) & (filtered_July2015["Tamworth pigs"] >= 13)]
    print("number passed Aug 2015 filters:", len(accepted_Aug2015))
    filtered_Aug2015 = filtered_July2015[filtered_July2015['run_number'].isin(accepted_Aug2015['run_number'])]
    # Sept 2015
    accepted_Sept2015 = filtered_Aug2015[(filtered_Aug2015["Time"] == 128) &
    # (filtered_Aug2015["Longhorn cattle"] <= 143) & (filtered_Aug2015["Longhorn cattle"] >= 117) &
    (filtered_Aug2015["Exmoor pony"] <= 11) & (filtered_Aug2015["Exmoor pony"] >= 9)]
    # (filtered_Aug2015["Tamworth pigs"] <= 15) & (filtered_Aug2015["Tamworth pigs"] >= 13)]
    print("number passed Sept 2015 filters:", len(accepted_Sept2015))
    filtered_Sept2015 = filtered_Aug2015[filtered_Aug2015['run_number'].isin(accepted_Sept2015['run_number'])]
    # Oct 2015
    accepted_Oct2015 = filtered_Sept2015[(filtered_Sept2015["Time"] == 129) &
    # (filtered_Sept2015["Longhorn cattle"] <= 100) & (filtered_Sept2015["Longhorn cattle"] >= 82) &
    (filtered_Sept2015["Exmoor pony"] <= 11) & (filtered_Sept2015["Exmoor pony"] >= 9)]
    # (filtered_Sept2015["Tamworth pigs"] <= 15) & (filtered_Sept2015["Tamworth pigs"] >= 13)]
    print("number passed Oct 2015 filters:", len(accepted_Oct2015))
    filtered_Oct2015 = filtered_Sept2015[filtered_Sept2015['run_number'].isin(accepted_Oct2015['run_number'])]
    # Nov 2015
    accepted_Nov2015 = filtered_Oct2015[(filtered_Oct2015["Time"] == 130) &
    # (filtered_Oct2015["Longhorn cattle"] <= 100) & (filtered_Oct2015["Longhorn cattle"] >= 82) &
    (filtered_Oct2015["Exmoor pony"] <= 11) & (filtered_Oct2015["Exmoor pony"] >= 9)]
    # (filtered_Oct2015["Tamworth pigs"] <= 14) & (filtered_Oct2015["Tamworth pigs"] >= 12)]
    print("number passed Nov 2015 filters:", len(accepted_Nov2015))
    filtered_Nov2015 = filtered_Oct2015[filtered_Oct2015['run_number'].isin(accepted_Nov2015['run_number'])]
    # Dec 2015
    accepted_Dec2015 = filtered_Nov2015[(filtered_Nov2015["Time"] == 131) &
    # (filtered_Nov2015["Longhorn cattle"] <= 94) & (filtered_Nov2015["Longhorn cattle"] >= 77) &
    (filtered_Nov2015["Exmoor pony"] <= 11) & (filtered_Nov2015["Exmoor pony"] >= 9)]
    # (filtered_Nov2015["Tamworth pigs"] <= 14) & (filtered_Nov2015["Tamworth pigs"] >= 12)]
    print("number passed Dec 2015 filters:", len(accepted_Dec2015))
    filtered_Dec2015 = filtered_Nov2015[filtered_Nov2015['run_number'].isin(accepted_Dec2015['run_number'])]
    # Jan 2016
    accepted_Jan2016 = filtered_Dec2015[(filtered_Dec2015["Time"] == 132) &
    # (filtered_Dec2015["Longhorn cattle"] <= 94) & (filtered_Dec2015["Longhorn cattle"] >= 77) &
    (filtered_Dec2015["Exmoor pony"] <= 11) & (filtered_Dec2015["Exmoor pony"] >= 9)]
    # (filtered_Dec2015["Tamworth pigs"] <= 11) & (filtered_Dec2015["Tamworth pigs"] >= 9)]
    print("number passed Jan 2016 filters:", len(accepted_Jan2016))
    filtered_Jan2016 = filtered_Dec2015[filtered_Dec2015['run_number'].isin(accepted_Jan2016['run_number'])]
    # Feb 2016
    accepted_Feb2016 = filtered_Jan2016[(filtered_Jan2016["Time"] == 133) &
    (filtered_Jan2016["Exmoor pony"] <= 11) & (filtered_Jan2016["Exmoor pony"] >= 9)]
    # (filtered_Jan2016["Longhorn cattle"] <= 94) & (filtered_Jan2016["Longhorn cattle"] >= 77) &
    # (filtered_Jan2016["Tamworth pigs"] <= 9) & (filtered_Jan2016["Tamworth pigs"] >= 7)]
    print("number passed February 2016 filters:", len(accepted_Feb2016))
    filtered_Feb2016 = filtered_Jan2016[filtered_Jan2016['run_number'].isin(accepted_Feb2016['run_number'])]
    # March 2016
    accepted_March2016 = filtered_Feb2016[(filtered_Feb2016["Time"] == 134) &
    (filtered_Feb2016["Exmoor pony"] <= 12) & (filtered_Feb2016["Exmoor pony"] >= 10) &
    # (filtered_Feb2016["Longhorn cattle"] <= 94) & (filtered_Feb2016["Longhorn cattle"] >= 77) &
    (filtered_Feb2016["Fallow deer"] <= 154) & (filtered_Feb2016["Fallow deer"] >= 126) &
    (filtered_Feb2016["Red deer"] <= 29) & (filtered_Feb2016["Red deer"] >= 23)]
    # (filtered_Feb2016["Tamworth pigs"] <= 10) & (filtered_Feb2016["Tamworth pigs"] >= 8)]
    print("number passed March 2016 filters:", len(accepted_March2016))
    filtered_March2016 = filtered_Feb2016[filtered_Feb2016['run_number'].isin(accepted_March2016['run_number'])]
    # April 2016
    accepted_April2016 = filtered_March2016[(filtered_March2016["Time"] == 135) &
    (filtered_March2016["Exmoor pony"] <= 12) & (filtered_March2016["Exmoor pony"] >= 10)]
    # (filtered_March2016["Longhorn cattle"] <= 113) & (filtered_March2016["Longhorn cattle"] >= 93) &
    # (filtered_March2016["Tamworth pigs"] <= 10) & (filtered_March2016["Tamworth pigs"] >= 8)]
    print("number passed April 2016 filters:", len(accepted_April2016))
    filtered_April2016 = filtered_March2016[filtered_March2016['run_number'].isin(accepted_April2016['run_number'])]
    # May 2016
    accepted_May2016 = filtered_April2016[(filtered_April2016["Time"] == 136) &
    (filtered_April2016["Exmoor pony"] <= 12) & (filtered_April2016["Exmoor pony"] >= 10)]
    # (filtered_April2016["Longhorn cattle"] <= 119) & (filtered_April2016["Longhorn cattle"] >= 97) &
    # (filtered_April2016["Tamworth pigs"] <= 19) & (filtered_April2016["Tamworth pigs"] >= 15)]
    print("number passed May 2016 filters:", len(accepted_May2016))
    filtered_May2016 = filtered_April2016[filtered_April2016['run_number'].isin(accepted_May2016['run_number'])]
    # June 2016
    accepted_June2016 = filtered_May2016[(filtered_May2016["Time"] == 137) &
    (filtered_May2016["Exmoor pony"] <= 12) & (filtered_May2016["Exmoor pony"] >= 10)]
    # (filtered_May2016["Longhorn cattle"] <= 98) & (filtered_May2016["Longhorn cattle"] >= 80) &
    # (filtered_May2016["Tamworth pigs"] <= 19) & (filtered_May2016["Tamworth pigs"] >= 15)]
    print("number passed June 2016 filters:", len(accepted_June2016))
    filtered_June2016 = filtered_May2016[filtered_May2016['run_number'].isin(accepted_June2016['run_number'])]
    # July 2016
    accepted_July2016 = filtered_June2016[(filtered_June2016["Time"] == 138) &
    (filtered_June2016["Exmoor pony"] <= 12) & (filtered_June2016["Exmoor pony"] >= 10)]
    # (filtered_June2016["Longhorn cattle"] <= 96) & (filtered_June2016["Longhorn cattle"] >= 78) &
    # (filtered_June2016["Tamworth pigs"] <= 19) & (filtered_June2016["Tamworth pigs"] >= 15)]
    print("number passed July 2016 filters:", len(accepted_July2016))
    filtered_July2016 = filtered_June2016[filtered_June2016['run_number'].isin(accepted_July2016['run_number'])]
    # Aug 2016
    accepted_Aug2016 = filtered_July2016[(filtered_July2016["Time"] == 139) &
    (filtered_July2016["Exmoor pony"] <= 12) & (filtered_July2016["Exmoor pony"] >= 10)]
    # (filtered_July2016["Longhorn cattle"] <= 96) & (filtered_July2016["Longhorn cattle"] >= 78) &
    # (filtered_July2016["Tamworth pigs"] <= 19) & (filtered_July2016["Tamworth pigs"] >= 15)]
    print("number passed Aug 2016 filters:", len(accepted_Aug2016))
    filtered_Aug2016 = filtered_July2016[filtered_July2016['run_number'].isin(accepted_Aug2016['run_number'])]
    # Sept 2016
    accepted_Sept2016 = filtered_Aug2016[(filtered_Aug2016["Time"] == 140) &
    (filtered_Aug2016["Exmoor pony"] <= 12) & (filtered_Aug2016["Exmoor pony"] >= 10)]
    # (filtered_Aug2016["Longhorn cattle"] <= 107) & (filtered_Aug2016["Longhorn cattle"] >= 87) &
    # (filtered_Aug2016["Tamworth pigs"] <= 19) & (filtered_Aug2016["Tamworth pigs"] >= 15)]
    print("number passed Sept 2016 filters:", len(accepted_Sept2016))
    filtered_Sept2016 = filtered_Aug2016[filtered_Aug2016['run_number'].isin(accepted_Sept2016['run_number'])]
    # Oct 2016
    accepted_Oct2016 = filtered_Sept2016[(filtered_Sept2016["Time"] == 141) &
    (filtered_Sept2016["Exmoor pony"] <= 12) & (filtered_Sept2016["Exmoor pony"] >= 10)]
    # (filtered_Sept2016["Longhorn cattle"] <= 107) & (filtered_Sept2016["Longhorn cattle"] >= 87) &
    # (filtered_Sept2016["Tamworth pigs"] <= 19) & (filtered_Sept2016["Tamworth pigs"] >= 15)]
    print("number passed Oct 2016 filters:", len(accepted_Oct2016))
    filtered_Oct2016 = filtered_Aug2016[filtered_Aug2016['run_number'].isin(accepted_Oct2016['run_number'])]
    # Nov 2016
    accepted_Nov2016 = filtered_Oct2016[(filtered_Oct2016["Time"] == 142) &
    (filtered_Oct2016["Exmoor pony"] <= 12) & (filtered_Oct2016["Exmoor pony"] >= 10)]
    # (filtered_Oct2016["Longhorn cattle"] <= 101) & (filtered_Oct2016["Longhorn cattle"] >= 83) &
    # (filtered_Oct2016["Tamworth pigs"] <= 19) & (filtered_Oct2016["Tamworth pigs"] >= 15)]
    print("number passed Nov 2016 filters:", len(accepted_Nov2016))
    filtered_Nov2016 = filtered_Oct2016[filtered_Oct2016['run_number'].isin(accepted_Nov2016['run_number'])]
    # Dec 2016
    accepted_Dec2016 = filtered_Nov2016[(filtered_Nov2016["Time"] == 143) &
    (filtered_Nov2016["Exmoor pony"] <= 12) & (filtered_Nov2016["Exmoor pony"] >= 10)]
    # (filtered_Nov2016["Longhorn cattle"] <= 87) & (filtered_Nov2016["Longhorn cattle"] >= 71) &
    # (filtered_Nov2016["Tamworth pigs"] <= 14) & (filtered_Nov2016["Tamworth pigs"] >= 12)]
    print("number passed Dec 2016 filters:", len(accepted_Dec2016))
    filtered_Dec2016 = filtered_Nov2016[filtered_Nov2016['run_number'].isin(accepted_Dec2016['run_number'])]
    # Jan 2017
    accepted_Jan2017= filtered_Dec2016[(filtered_Dec2016["Time"] == 144) &
    (filtered_Dec2016["Exmoor pony"] <= 12) & (filtered_Dec2016["Exmoor pony"] >= 10)]
    # (filtered_Dec2016["Longhorn cattle"] <= 87) & (filtered_Dec2016["Longhorn cattle"] >= 71) &
    # (filtered_Dec2016["Tamworth pigs"] <= 10) & (filtered_Dec2016["Tamworth pigs"] >= 8)]
    print("number passed Jan 2017 filters:", len(accepted_Jan2017))
    filtered_Jan2017 = filtered_Dec2016[filtered_Dec2016['run_number'].isin(accepted_Jan2017['run_number'])]
    # Feb 2017
    accepted_Feb2017 = filtered_Jan2017[(filtered_Jan2017["Time"] == 145) &
    (filtered_Jan2017["Exmoor pony"] <= 12) & (filtered_Jan2017["Exmoor pony"] >= 10)]
    # (filtered_Jan2017["Longhorn cattle"] <= 87) & (filtered_Jan2017["Longhorn cattle"] >= 71) &
    # (filtered_Jan2017["Tamworth pigs"] <= 8) & (filtered_Jan2017["Tamworth pigs"] >= 6)]
    print("number passed Feb 2017 filters:", len(accepted_Feb2017))
    filtered_Feb2017 = filtered_Jan2017[filtered_Jan2017['run_number'].isin(accepted_Feb2017['run_number'])]
    # March 2017
    accepted_March2017 = filtered_Feb2017[(filtered_Feb2017["Time"] == 146) &
    (filtered_Feb2017["Exmoor pony"] <= 11) & (filtered_Feb2017["Exmoor pony"] >= 9) &
    (filtered_Feb2017["Fallow deer"] <= 182) & (filtered_Feb2017["Fallow deer"] >= 149)]
    # (filtered_Feb2017["Longhorn cattle"] <= 87) & (filtered_Feb2017["Longhorn cattle"] >= 71) &
    # (filtered_Feb2017["Tamworth pigs"] <= 8) & (filtered_Feb2017["Tamworth pigs"] >= 6)]
    print("number passed March 2017 filters:", len(accepted_March2017))
    filtered_March2017 = filtered_Feb2017[filtered_Feb2017['run_number'].isin(accepted_March2017['run_number'])]
    # April 2017
    accepted_April2017 = filtered_March2017[(filtered_March2017["Time"] == 147) &
    (filtered_March2017["Exmoor pony"] <= 11) & (filtered_March2017["Exmoor pony"] >= 9)]
    # (filtered_March2017["Longhorn cattle"] <= 110) & (filtered_March2017["Longhorn cattle"] >= 90) &
    # (filtered_March2017["Tamworth pigs"] <= 24) & (filtered_March2017["Tamworth pigs"] >= 20)]
    print("number passed April 2017 filters:", len(accepted_April2017))
    filtered_April2017 = filtered_March2017[filtered_March2017['run_number'].isin(accepted_April2017['run_number'])]
    # May 2017
    accepted_May2017 = filtered_April2017[(filtered_April2017["Time"] == 148) &
    (filtered_April2017["Exmoor pony"] <= 11) & (filtered_April2017["Exmoor pony"] >= 9)]
    # (filtered_April2017["Longhorn cattle"] <= 120) & (filtered_April2017["Longhorn cattle"] >= 98) &
    # (filtered_April2017["Tamworth pigs"] <= 24) & (filtered_April2017["Tamworth pigs"] >= 20)]
    print("number passed May 2017 filters:", len(accepted_May2017))
    filtered_May2017 = filtered_April2017[filtered_April2017['run_number'].isin(accepted_May2017['run_number'])]
    # June 2017
    accepted_June2017 = filtered_May2017[(filtered_May2017["Time"] == 149) &
    (filtered_May2017["Exmoor pony"] <= 11) & (filtered_May2017["Exmoor pony"] >= 9)]
    # (filtered_May2017["Longhorn cattle"] <= 103) & (filtered_May2017["Longhorn cattle"] >= 85) &
    # (filtered_May2017["Tamworth pigs"] <= 24) & (filtered_May2017["Tamworth pigs"] >= 20)]
    print("number passed June 2017 filters:", len(accepted_June2017))
    filtered_June2017 = filtered_May2017[filtered_May2017['run_number'].isin(accepted_June2017['run_number'])]
    # July 2017
    accepted_July2017 = filtered_June2017[(filtered_June2017["Time"] == 150) &
    (filtered_June2017["Exmoor pony"] <= 11) & (filtered_June2017["Exmoor pony"] >= 9)]
    # (filtered_June2017["Longhorn cattle"] <= 103) & (filtered_June2017["Longhorn cattle"] >= 85) &
    # (filtered_June2017["Tamworth pigs"] <= 24) & (filtered_June2017["Tamworth pigs"] >= 20)]
    print("number passed July 2017 filters:", len(accepted_July2017))
    filtered_July2017 = filtered_June2017[filtered_June2017['run_number'].isin(accepted_July2017['run_number'])]
    # Aug 2017
    accepted_Aug2017 = filtered_July2017[(filtered_July2017["Time"] == 151) &
    (filtered_July2017["Exmoor pony"] <= 11) & (filtered_July2017["Exmoor pony"] >= 9)]
    # (filtered_July2017["Longhorn cattle"] <= 103) & (filtered_July2017["Longhorn cattle"] >= 85) &
    # (filtered_July2017["Tamworth pigs"] <= 24) & (filtered_July2017["Tamworth pigs"] >= 20)]
    print("number passed Aug 2017 filters:", len(accepted_Aug2017))
    filtered_Aug2017 = filtered_July2017[filtered_July2017['run_number'].isin(accepted_Aug2017['run_number'])]
    # Sept 2017
    accepted_Sept2017 = filtered_Aug2017[(filtered_Aug2017["Time"] == 152) &
    (filtered_Aug2017["Exmoor pony"] <= 11) & (filtered_Aug2017["Exmoor pony"] >= 9)]
    # (filtered_Aug2017["Longhorn cattle"] <= 99) & (filtered_Aug2017["Longhorn cattle"] >= 81) &
    # (filtered_Aug2017["Tamworth pigs"] <= 24) & (filtered_Aug2017["Tamworth pigs"] >= 20)]
    print("number passed Sept 2017 filters:", len(accepted_Sept2017))
    filtered_Sept2017 = filtered_Aug2017[filtered_Aug2017['run_number'].isin(accepted_Sept2017['run_number'])]
    # Oct 2017
    accepted_Oct2017 = filtered_Sept2017[(filtered_Sept2017["Time"] == 153) &
    (filtered_Sept2017["Exmoor pony"] <= 11) & (filtered_Sept2017["Exmoor pony"] >= 9)]
    # (filtered_Sept2017["Longhorn cattle"] <= 97) & (filtered_Sept2017["Longhorn cattle"] >= 79) &
    # (filtered_Sept2017["Tamworth pigs"] <= 24) & (filtered_Sept2017["Tamworth pigs"] >= 20)]
    print("number passed Oct 2017 filters:", len(accepted_Oct2017))
    filtered_Oct2017 = filtered_Sept2017[filtered_Sept2017['run_number'].isin(accepted_Oct2017['run_number'])]
    # Nov 2017
    accepted_Nov2017 = filtered_Oct2017[(filtered_Oct2017["Time"] == 154) &
    (filtered_Oct2017["Exmoor pony"] <= 11) & (filtered_Oct2017["Exmoor pony"] >= 9)]
    # (filtered_Oct2017["Longhorn cattle"] <= 97) & (filtered_Oct2017["Longhorn cattle"] >= 79) &
    # (filtered_Oct2017["Tamworth pigs"] <= 24) & (filtered_Oct2017["Tamworth pigs"] >= 20)]
    print("number passed Nov 2017 filters:", len(accepted_Nov2017))
    filtered_Nov2017 = filtered_Oct2017[filtered_Oct2017['run_number'].isin(accepted_Nov2017['run_number'])]
    # Dec 2017
    accepted_Dec2017 = filtered_Nov2017[(filtered_Nov2017["Time"] == 155) &
    (filtered_Nov2017["Exmoor pony"] <= 11) & (filtered_Nov2017["Exmoor pony"] >= 9)]
    # (filtered_Nov2017["Longhorn cattle"] <= 97) & (filtered_Nov2017["Longhorn cattle"] >= 79) &
    # (filtered_Nov2017["Tamworth pigs"] <= 20) & (filtered_Nov2017["Tamworth pigs"] >= 16)]
    print("number passed Dec 2017 filters:", len(accepted_Dec2017))
    filtered_Dec2017 = filtered_Nov2017[filtered_Nov2017['run_number'].isin(accepted_Dec2017['run_number'])]
    # January 2018
    accepted_Jan2018 = filtered_Dec2017[(filtered_Dec2017["Time"] == 156) &
    (filtered_Dec2017["Exmoor pony"] <= 11) & (filtered_Dec2017["Exmoor pony"] >= 9)]
    # (filtered_Dec2017["Longhorn cattle"] <= 97) & (filtered_Dec2017["Longhorn cattle"] >= 79) &
    # (filtered_Dec2017["Tamworth pigs"] <= 12) & (filtered_Dec2017["Tamworth pigs"] >= 10)]
    print("number passed January 2018 filters:", len(accepted_Jan2018))
    filtered_Jan2018 = filtered_Dec2017[filtered_Dec2017['run_number'].isin(accepted_Jan2018['run_number'])]
    # February 2018
    accepted_Feb2018 = filtered_Jan2018[(filtered_Jan2018["Time"] == 157) &
    (filtered_Jan2018["Exmoor pony"] <= 11) & (filtered_Jan2018["Exmoor pony"] >= 9)]
    # (filtered_Jan2018["Longhorn cattle"] <= 97) & (filtered_Jan2018["Longhorn cattle"] >= 79) &
    # (filtered_Jan2018["Tamworth pigs"] <= 18) & (filtered_Jan2018["Tamworth pigs"] >= 14)]
    print("number passed Feb 2018 filters:", len(accepted_Feb2018)) 
    filtered_Feb2018 = filtered_Jan2018[filtered_Jan2018['run_number'].isin(accepted_Feb2018['run_number'])]
    # March 2018
    accepted_March2018 = filtered_Feb2018[(filtered_Feb2018["Time"] == 158) &
    (filtered_Feb2018["Exmoor pony"] <= 10) & (filtered_Feb2018["Exmoor pony"] >= 8) &
    (filtered_Feb2018["Fallow deer"] <= 276) & (filtered_Feb2018["Fallow deer"] >= 226) &
    # (filtered_Feb2018["Longhorn cattle"] <= 97) & (filtered_Feb2018["Longhorn cattle"] >= 79) &
    (filtered_Feb2018["Red deer"] <= 26) & (filtered_Feb2018["Red deer"] >= 22)]
    # (filtered_Feb2018["Tamworth pigs"] <= 18) & (filtered_Feb2018["Tamworth pigs"] >= 14)]
    print("number passed March 2018 filters:", len(accepted_March2018)) 
    filtered_March2018 = filtered_Feb2018[filtered_Feb2018['run_number'].isin(accepted_March2018['run_number'])]
    # April 2018
    accepted_April2018 = filtered_March2018[(filtered_March2018["Time"] == 159) &
    (filtered_March2018["Exmoor pony"] <= 10) & (filtered_March2018["Exmoor pony"] >= 8)]
    # (filtered_March2018["Longhorn cattle"] <= 111) & (filtered_March2018["Longhorn cattle"] >= 91) &
    # (filtered_March2018["Tamworth pigs"] <= 18) & (filtered_March2018["Tamworth pigs"] >= 14)]
    print("number passed April 2018 filters:", len(accepted_April2018)) 
    filtered_April2018 = filtered_March2018[filtered_March2018['run_number'].isin(accepted_April2018['run_number'])]
    # May 2018
    accepted_May2018 = filtered_April2018[(filtered_April2018["Time"] == 160) &
    (filtered_April2018["Exmoor pony"] <= 10) & (filtered_April2018["Exmoor pony"] >= 8)]
    # (filtered_April2018["Longhorn cattle"] <= 129) & (filtered_April2018["Longhorn cattle"] >= 105) &
    # (filtered_April2018["Tamworth pigs"] <= 25) & (filtered_April2018["Tamworth pigs"] >= 21)]
    print("number passed May 2018 filters:", len(accepted_May2018)) 
    filtered_May2018 = filtered_April2018[filtered_April2018['run_number'].isin(accepted_May2018['run_number'])]
    # June 2018
    accepted_June2018 = filtered_May2018[(filtered_May2018["Time"] == 161) &
    (filtered_May2018["Exmoor pony"] <= 10) & (filtered_May2018["Exmoor pony"] >= 8)]
    # (filtered_May2018["Longhorn cattle"] <= 113) & (filtered_May2018["Longhorn cattle"] >= 93) &
    # (filtered_May2018["Tamworth pigs"] <= 25) & (filtered_May2018["Tamworth pigs"] >= 21)]
    print("number passed June 2018 filters:", len(accepted_June2018)) 
    filtered_June2018 = filtered_May2018[filtered_May2018['run_number'].isin(accepted_June2018['run_number'])]
    # July 2018
    accepted_July2018 = filtered_June2018[(filtered_June2018["Time"] == 162) &
    (filtered_June2018["Exmoor pony"] <= 10) & (filtered_June2018["Exmoor pony"] >= 8)]
    # (filtered_June2018["Longhorn cattle"] <= 113) & (filtered_June2018["Longhorn cattle"] >= 93) &
    # (filtered_June2018["Tamworth pigs"] <= 24) & (filtered_June2018["Tamworth pigs"] >= 20)]
    print("number passed July 2018 filters:", len(accepted_July2018)) 
    filtered_July2018 = filtered_June2018[filtered_June2018['run_number'].isin(accepted_July2018['run_number'])]
    # Aug 2018
    accepted_Aug2018 = filtered_July2018[(filtered_July2018["Time"] == 163)]
    # (filtered_July2018["Longhorn cattle"] <= 112) & (filtered_July2018["Longhorn cattle"] >= 92) &
    # (filtered_July2018["Tamworth pigs"] <= 24) & (filtered_July2018["Tamworth pigs"] >= 20)]
    print("number passed Aug 2018 filters:", len(accepted_Aug2018)) 
    filtered_Aug2018 = filtered_July2018[filtered_July2018['run_number'].isin(accepted_Aug2018['run_number'])]
    # Sept 2018
    accepted_Sept2018 = filtered_Aug2018[(filtered_Aug2018["Time"] == 164)]
    # (filtered_Aug2018["Longhorn cattle"] <= 117) & (filtered_Aug2018["Longhorn cattle"] >= 95) &
    # (filtered_Aug2018["Tamworth pigs"] <= 24) & (filtered_Aug2018["Tamworth pigs"] >= 20)]
    print("number passed Sept 2018 filters:", len(accepted_Sept2018)) 
    filtered_Sept2018 = filtered_Aug2018[filtered_Aug2018['run_number'].isin(accepted_Sept2018['run_number'])]
    # Oct 2018
    accepted_Oct2018 = filtered_Sept2018[(filtered_Sept2018["Time"] == 165)]
    # (filtered_Sept2018["Longhorn cattle"] <= 111) & (filtered_Sept2018["Longhorn cattle"] >= 91) &
    # (filtered_Sept2018["Tamworth pigs"] <= 23) & (filtered_Sept2018["Tamworth pigs"] >= 19)]
    print("number passed Oct 2018 filters:", len(accepted_Oct2018))
    filtered_Oct2018 = filtered_Sept2018[filtered_Sept2018['run_number'].isin(accepted_Oct2018['run_number'])]
    # Nov 2018
    accepted_Nov2018 = filtered_Oct2018[(filtered_Oct2018["Time"] == 166)]
    # (filtered_Oct2018["Longhorn cattle"] <= 102) & (filtered_Oct2018["Longhorn cattle"] >= 84) &
    # (filtered_Oct2018["Tamworth pigs"] <= 10) & (filtered_Oct2018["Tamworth pigs"] >= 8)]
    print("number passed Nov 2018 filters:", len(accepted_Nov2018)) 
    filtered_Nov2018 = filtered_Oct2018[filtered_Oct2018['run_number'].isin(accepted_Nov2018['run_number'])]
    # Dec 2018
    accepted_Dec2018 = filtered_Nov2018[(filtered_Nov2018["Time"] == 167)]
    # (filtered_Nov2018["Longhorn cattle"] <= 98) & (filtered_Nov2018["Longhorn cattle"] >= 80) &
    # (filtered_Nov2018["Tamworth pigs"] <= 10) & (filtered_Nov2018["Tamworth pigs"] >= 8)]
    print("number passed Dec 2018 filters:", len(accepted_Dec2018)) 
    filtered_Dec2018 = filtered_Nov2018[filtered_Nov2018['run_number'].isin(accepted_Dec2018['run_number'])]
    # # Jan 2019
    accepted_Jan2019 = filtered_Dec2018[(filtered_Dec2018["Time"] == 168)]
    # (filtered_Dec2018["Longhorn cattle"] <= 98) & (filtered_Dec2018["Longhorn cattle"] >= 80) &
    # (filtered_Dec2018["Tamworth pigs"] <= 10) & (filtered_Dec2018["Tamworth pigs"] >= 8)]
    print("number passed Jan 2019 filters:", len(accepted_Jan2019)) 
    filtered_Jan2019 = filtered_Dec2018[filtered_Dec2018['run_number'].isin(accepted_Jan2019['run_number'])]
    # Feb 2019
    accepted_Feb2019 = filtered_Jan2019[(filtered_Jan2019["Time"] == 169)]
    # (filtered_Jan2019["Longhorn cattle"] <= 96) & (filtered_Jan2019["Longhorn cattle"] >= 78) &
    # (filtered_Jan2019["Tamworth pigs"] <= 11) & (filtered_Jan2019["Tamworth pigs"] >= 9)]
    print("number passed Feb 2019 filters:", len(accepted_Feb2019)) 
    filtered_Feb2019 = filtered_Jan2019[filtered_Jan2019['run_number'].isin(accepted_Feb2019['run_number'])]
    # March 2019
    accepted_March2019 = filtered_Feb2019[(filtered_Feb2019["Time"] == 170) &
    (filtered_Feb2019["Fallow deer"] <= 306) & (filtered_Feb2019["Fallow deer"] >= 250) &
    (filtered_Feb2019["Longhorn cattle"] <= 96) & (filtered_Feb2019["Longhorn cattle"] >= 78) &
    (filtered_Feb2019["Red deer"] <= 41) & (filtered_Feb2019["Red deer"] >= 33)]
    # (filtered_Feb2019["Tamworth pigs"] <= 10) & (filtered_Feb2019["Tamworth pigs"] >= 8)]
    print("number passed March 2019 filters:", len(accepted_March2019)) 
    filtered_March2019 = filtered_Feb2019[filtered_Feb2019['run_number'].isin(accepted_March2019['run_number'])]
    # April 2019
    accepted_April2019 = filtered_March2019[(filtered_March2019["Time"] == 171) &
    (filtered_March2019["Longhorn cattle"] <= 111) & (filtered_March2019["Longhorn cattle"] >= 91) &
    (filtered_March2019["Tamworth pigs"] <= 9) & (filtered_March2019["Tamworth pigs"] >= 7)]
    print("number passed April 2019 filters:", len(accepted_April2019)) 
    filtered_April2019 = filtered_March2019[filtered_March2019['run_number'].isin(accepted_April2019['run_number'])]
    # May 2019
    accepted_May2019 = filtered_April2019[(filtered_April2019["Time"] == 172) &
    (filtered_April2019["Longhorn cattle"] <= 121) & (filtered_April2019["Longhorn cattle"] >= 99) &
    (filtered_April2019["Tamworth pigs"] <= 9) & (filtered_April2019["Tamworth pigs"] >= 7)]
    print("number passed May 2019 filters:", len(accepted_May2019))
    filtered_May2019 = filtered_April2019[filtered_April2019['run_number'].isin(accepted_May2019['run_number'])]
    # June 2019
    accepted_June2019 = filtered_May2019[(filtered_May2019["Time"] == 173) &
    (filtered_May2019["Longhorn cattle"] <= 98) & (filtered_May2019["Longhorn cattle"] >= 80) &
    (filtered_May2019["Tamworth pigs"] <= 9) & (filtered_May2019["Tamworth pigs"] >= 7)]
    print("number passed June 2019 filters:", len(accepted_June2019)) 
    filtered_June2019 = filtered_May2019[filtered_May2019['run_number'].isin(accepted_June2019['run_number'])]
    # July 2019
    accepted_July2019 = filtered_June2019[(filtered_June2019["Time"] == 174) &
    (filtered_June2019["Longhorn cattle"] <= 100) & (filtered_June2019["Longhorn cattle"] >= 82) &
    (filtered_June2019["Tamworth pigs"] <= 10) & (filtered_June2019["Tamworth pigs"] >= 8)]
    print("number passed July 2019 filters:", len(accepted_July2019)) 
    filtered_July2019 = filtered_June2019[filtered_June2019['run_number'].isin(accepted_July2019['run_number'])]
    # Aug 2019
    accepted_Aug2019 = filtered_July2019[(filtered_July2019["Time"] == 175) &
    (filtered_July2019["Longhorn cattle"] <= 100) & (filtered_July2019["Longhorn cattle"] >= 82) &
    (filtered_July2019["Tamworth pigs"] <= 10) & (filtered_July2019["Tamworth pigs"] >= 8)]
    print("number passed Aug 2019 filters:", len(accepted_Aug2019)) 
    filtered_Aug2019 = filtered_July2019[filtered_July2019['run_number'].isin(accepted_Aug2019['run_number'])]
    # Sept 2019
    accepted_Sept2019 = filtered_Aug2019[(filtered_Aug2019["Time"] == 176) &
    (filtered_Aug2019["Longhorn cattle"] <= 102) & (filtered_Aug2019["Longhorn cattle"] >= 84) &
    (filtered_Aug2019["Tamworth pigs"] <= 10) & (filtered_Aug2019["Tamworth pigs"] >= 8)]
    print("number passed Sept 2019 filters:", len(accepted_Sept2019)) 
    filtered_Sept2019 = filtered_Aug2019[filtered_Aug2019['run_number'].isin(accepted_Sept2019['run_number'])]
    # Oct 2019
    accepted_Oct2019 = filtered_Sept2019[(filtered_Sept2019["Time"] == 177) &
    (filtered_Sept2019["Longhorn cattle"] <= 97) & (filtered_Sept2019["Longhorn cattle"] >= 79) &
    (filtered_Sept2019["Tamworth pigs"] <= 10) & (filtered_Sept2019["Tamworth pigs"] >= 8)]
    print("number passed Oct 2019 filters:", len(accepted_Oct2019)) 
    filtered_Oct2019 = filtered_Sept2019[filtered_Sept2019['run_number'].isin(accepted_Oct2019['run_number'])]
    # Nov 2019
    accepted_Nov2019 = filtered_Oct2019[(filtered_Oct2019["Time"] == 178) &
    (filtered_Oct2019["Longhorn cattle"] <= 96) & (filtered_Oct2019["Longhorn cattle"] >= 78) &
    (filtered_Oct2019["Tamworth pigs"] <= 10) & (filtered_Oct2019["Tamworth pigs"] >= 8)]
    print("number passed Nov 2019 filters:", len(accepted_Nov2019)) 
    filtered_Nov2019 = filtered_Oct2019[filtered_Oct2019['run_number'].isin(accepted_Nov2019['run_number'])]
    # Dec 2019
    accepted_Dec2019 = filtered_Nov2019[(filtered_Nov2019["Time"] == 179) &
    (filtered_Nov2019["Longhorn cattle"] <= 88) & (filtered_Nov2019["Longhorn cattle"] >= 72) &
    (filtered_Nov2019["Tamworth pigs"] <= 11) & (filtered_Nov2019["Tamworth pigs"] >= 9)]
    print("number passed Dec 2019 filters:", len(accepted_Dec2019))
    filtered_Dec2019 = filtered_Nov2019[filtered_Nov2019['run_number'].isin(accepted_Dec2019['run_number'])]
    # Jan 2020
    accepted_Jan2020 = filtered_Dec2019[(filtered_Dec2019["Time"] == 180) &
    (filtered_Dec2019["Longhorn cattle"] <= 88) & (filtered_Dec2019["Longhorn cattle"] >= 72) &
    (filtered_Dec2019["Tamworth pigs"] <= 11) & (filtered_Dec2019["Tamworth pigs"] >= 9)]
    print("number passed Jan 2020 filters:", len(accepted_Jan2020))
    filtered_Jan2020 = filtered_Dec2019[filtered_Dec2019['run_number'].isin(accepted_Jan2020['run_number'])]
    # Feb 2020
    accepted_Feb2020 = filtered_Jan2020[(filtered_Jan2020["Time"] == 181) &
    (filtered_Jan2020["Longhorn cattle"] <= 87) & (filtered_Jan2020["Longhorn cattle"] >= 71) &
    (filtered_Jan2020["Tamworth pigs"] <= 9) & (filtered_Jan2020["Tamworth pigs"] >= 7)]
    print("number passed Feb 2020 filters:", len(accepted_Feb2020))
    filtered_Feb2020 = filtered_Jan2020[filtered_Jan2020['run_number'].isin(accepted_Feb2020['run_number'])]
    # March 2020
    accepted_March2020 = filtered_Feb2020[(filtered_Feb2020["Time"] == 182) &
    (filtered_Feb2020["Fallow deer"] <= 272) & (filtered_Feb2020["Fallow deer"] >= 222) &
    (filtered_Feb2020["Red deer"] <= 39) & (filtered_Feb2020["Red deer"] >= 32) &
    (filtered_Feb2020["Longhorn cattle"] <= 89) & (filtered_Feb2020["Longhorn cattle"] >= 73) &
    (filtered_Feb2020["Tamworth pigs"] <= 8) & (filtered_Feb2020["Tamworth pigs"] >= 6)]
    print("number passed March 2020 filters:", len(accepted_March2020)) 
    filtered_March2020 = filtered_Feb2020[filtered_Feb2020['run_number'].isin(accepted_March2020['run_number'])]
    # April 2020
    accepted_April2020 = filtered_March2020[(filtered_March2020["Time"] == 183) &
    (filtered_March2020["Exmoor pony"] <= 17) & (filtered_March2020["Exmoor pony"] >= 14) &
    (filtered_March2020["Longhorn cattle"] <= 89) & (filtered_March2020["Longhorn cattle"] >= 73) &
    (filtered_March2020["Tamworth pigs"] <= 8) & (filtered_March2020["Tamworth pigs"] >= 6)]
    print("number passed April 2020 filters:", len(accepted_April2020)) 
    filtered_April2020 = filtered_March2020[filtered_March2020['run_number'].isin(accepted_April2020['run_number'])]
    # May 2020
    all_accepted_runs = filtered_April2020[(filtered_April2020["Time"] == 184) &
    (filtered_April2020["Tamworth pigs"] <= 21) & (filtered_April2020["Tamworth pigs"] >= 17) &
    (filtered_April2020["Exmoor pony"] <= 17) & (filtered_April2020["Exmoor pony"] >= 14) &
    (filtered_April2020["Longhorn cattle"] <= 89) & (filtered_April2020["Longhorn cattle"] >= 73) &
    (filtered_April2020["Roe deer"] <= 40) & (filtered_April2020["Roe deer"] >= 20) & 
    (filtered_April2020["Grassland"] <= 69) & (filtered_April2020["Grassland"] >= 49) & 
    (filtered_April2020["Thorny Scrub"] <= 45) & (filtered_April2020["Thorny Scrub"] >= 11) &
    (filtered_April2020["Woodland"] <= 29) & (filtered_April2020["Woodland"] >= 9)]
    print("number passed all filters:", len(all_accepted_runs))

    # accepted parameters
    accepted_parameters = final_parameters[final_parameters['run_number'].isin(all_accepted_runs['run_number'])]
    # tag the accepted simulations
    final_results['accepted?'] = np.where(final_results['run_number'].isin(accepted_parameters['run_number']), 'Accepted', 'Rejected')

    with pd.option_context('display.max_columns',None):
        print(final_results[(final_results["Time"] == 184)])
    
    with pd.option_context('display.max_rows',None, 'display.max_columns',None):
        print("accepted_years: \n", all_accepted_runs)

    # save to excel sheet
    final_parameters.to_excel("all_parameters_Exmoor_Fallow.xlsx")
    accepted_parameters.to_excel("accepted_parameters_Exmoor_Fallow.xlsx")



    return number_simulations, final_results, accepted_parameters

