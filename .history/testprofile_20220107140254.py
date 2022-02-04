from KneppModel_ABM import KneppModel 

model = KneppModel(
        0.1, 0.1, 0.1, 0.1, 0.1, 
        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
        0.1, 0.1, 0.1, 0.1, 
        0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
        0.1, 0.1, 0.1, 0.1, 0.1, 
        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
        0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
        width = 25, height = 18, 
        max_time = 185, reintroduction = False, 
        RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)

model.run_model()
# results = model.datacollector.get_model_vars_dataframe()
# print(results)

# run these files (run the second once the first one is done)
    # python3 -m cProfile -o temp.dat testprofile.py
    # /Users/emilyneil/Library/Python/3.8/bin/snakeviz temp.dat