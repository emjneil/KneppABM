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
        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
        width = 25, height = 18, 
        max_time = 185, reintroduction = True, 
        RC1_noFood = False, RC2_noTreesScrub = False, RC3_noTrees = False, RC4_noScrub = False)

model.run_model()

# run these files (run the second once the first one is done)
    # python3 -m cProfile -o temp.dat profiler_test.py
    # /Users/emilyneil/Library/Python/3.8/bin/snakeviz temp.dat