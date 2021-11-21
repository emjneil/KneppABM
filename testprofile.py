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
        0.1, 0.1, 0.1, 0.1, 
        width = 50, height = 36, 
        max_time = 185, reintroduction = False)

model.run_model()
# results = model.datacollector.get_model_vars_dataframe()
# print(results)

# run these files (run the second once the first one is done)
    # python3 -m cProfile -o temp.dat testprofile.py
    # /Users/emilyneil/Library/Python/3.8/bin/snakeviz temp.dat