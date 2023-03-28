from model import KneppModel 

model = KneppModel(
        12, 0.1, 0.1, 0.1, 0.1, 
        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
        0.1, 0.1, 0.1, 0.1, 
        0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
        0.1, 0.1, 0.1, 0.1, 0.1, 
        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
        0.1, 0.1, 0.1, 0.1, 0.1, 1, 1, 1,
        1, 1, 1, 1, 10, 10, 10, 
        10,
        max_time = 185, 
        reintroduction = True, introduce_euroBison = False, introduce_elk = False, introduce_reindeer = False)

model.run_model()

# run these files (run the second once the first one is done)
    # python3 -m cProfile -o temp.dat profiler_test.py
    # /Users/emilyneil/Library/Python/3.8/bin/snakeviz temp.dat