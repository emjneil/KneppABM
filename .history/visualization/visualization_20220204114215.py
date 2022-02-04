# # # Visualizing the Knepp ABC/ABM model # # #
from ABM_scripts().KneppModel_ABM import KneppModel, roeDeer_agent, habitatAgent, fallowDeer, redDeer, tamworthPigs, exmoorPony, longhornCattle
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule


# define the agents 
def agent_portrayal(agent):
    if agent is None:
        return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true"}

    if type(agent) is roeDeer_agent:
        portrayal["Shape"] = "deerShape.png"
        portrayal["scale"] = 0.25
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"
        
    elif type(agent) is habitatAgent:
        if agent.condition == "woodland":
            portrayal["Shape"] = "treeShape.png"
            portrayal["Layer"] = 1
            portrayal["scale"] = 1
        elif agent.condition == "thorny_scrubland":
            portrayal["Shape"] = "bushShape.png"
            portrayal["Layer"] = 0
            portrayal["scale"] = 1
        elif agent.condition == "grassland":
            portrayal["Shape"] = "grassShape.png"
            portrayal["Layer"] = 0
            portrayal["scale"] = 1
        elif agent.condition == "bare_ground":
            portrayal["Shape"] = "dirtShape.png"
            portrayal["Layer"] = 0
            portrayal["scale"] = 1

    if type(agent) is longhornCattle:
        portrayal["Shape"] = "cowShape.png"
        portrayal["scale"] = 0.5
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"

    if type(agent) is redDeer:
        portrayal["Shape"] = "redDeerShape.png"
        portrayal["scale"] = 0.5
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"
        
    if type(agent) is exmoorPony:
        portrayal["Shape"] = "ponyShape.png"
        portrayal["scale"] = 0.5
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"

    if type(agent) is fallowDeer:
        portrayal["Shape"] = "fallowDeerShape.png"
        portrayal["scale"] = 0.5
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"

    if type(agent) is tamworthPigs:
        portrayal["Shape"] = "pigShape.png"
        portrayal["scale"] = 0.5
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"
        
    return portrayal


canvas_element = CanvasGrid(agent_portrayal, 25, 18, 750, 540)
chart_element = ChartModule([{"Label": "Roe deer", "Color": "#666666"},
                            {"Label": "Red deer", "Color": "#BC473A"},
                            {"Label": "Fallow deer", "Color": "#F16529"},
                            {"Label": "Longhorn cattle", "Color": "#4B8BBE"},
                            {"Label": "Tamworth pig", "Color": "#8E0F7E"},
                            {"Label": "Exmoor pony", "Color": "#1817A2"},
                             {"Label": "Grassland", "Color": "#68A063"},
                             {"Label": "Bare ground", "Color": "#560000"},
                             {"Label": "Thorny Scrub", "Color": "#FFD43B"},
                             {"Label": "Woodland", "Color": "#3C873A"}
                             ])


server = ModularServer(KneppModel, [canvas_element, chart_element],
                       "KneppModel", {"chance_reproduceSapling":0.01662151, "chance_reproduceYoungScrub":0.03339998, "chance_regrowGrass":0.07572306, "chance_saplingBecomingTree":0.00229839, "chance_youngScrubMatures":0.01986841,
                        "chance_scrubOutcompetedByTree":0.01975722, "chance_grassOutcompetedByTree":0.08530632, "chance_grassOutcompetedByScrub":0.08602075, "chance_saplingOutcompetedByTree":0.03287396, "chance_saplingOutcompetedByScrub":0.02622373, "chance_youngScrubOutcompetedByScrub":0.03997985, "chance_youngScrubOutcompetedByTree":0.03022047,
                        "initial_roeDeer":0.12, "initial_grassland":0.71, "initial_woodland":0.12, "initial_scrubland":0.01, 
                        "roeDeer_reproduce":0.19698953, "roeDeer_gain_from_grass":0.59214711, "roeDeer_gain_from_Trees":0.79335842, "roeDeer_gain_from_Scrub":0.78158966, "roeDeer_gain_from_Saplings":0.12919985, "roeDeer_gain_from_YoungScrub":0.12062618, 
                        
                        "ponies_gain_from_grass": 0.9693617, "ponies_gain_from_Trees": 0.47012106, "ponies_gain_from_Scrub": 0.45597684, "ponies_gain_from_Saplings": 0.09740837, "ponies_gain_from_YoungScrub": 0.02663788, 
                        "cows_reproduce": 0.2009648, "cows_gain_from_grass": 0.35508327, "cows_gain_from_Trees": 0.31643717, "cows_gain_from_Scrub": 0.43985099, "cows_gain_from_Saplings": 0.00826741, "cows_gain_from_YoungScrub": 0.11884475, 
                        "fallowDeer_reproduce": 0.3931105, "fallowDeer_gain_from_grass": 0.41489633, "fallowDeer_gain_from_Trees": 0.69958117, "fallowDeer_gain_from_Scrub": 0.24765327, "fallowDeer_gain_from_Saplings": 0.06749797, "fallowDeer_gain_from_YoungScrub": 0.02755626, 
                        "redDeer_reproduce": 0.32813086, "redDeer_gain_from_grass": 0.47033814, "redDeer_gain_from_Trees": 0.47107371, "redDeer_gain_from_Scrub": 0.4028574, "redDeer_gain_from_Saplings": 0.02549839, "redDeer_gain_from_YoungScrub": 0.0782808, 
                        "pigs_reproduce": 0.13234609, "pigs_gain_from_grass": 0.0134285, "pigs_gain_from_Trees": 0.11901308, "pigs_gain_from_Scrub": 0.11901308, "pigs_gain_from_Saplings": 0.02284746, "pigs_gain_from_YoungScrub": 0.02284746,
                        "max_start_saplings": 0.1, "max_start_youngScrub": 0.1,
                        "width":25, "height":18, 
                        "max_time": 185, "reintroduction": True, 
                        "RC1_noFood": False, "RC2_noTreesScrub": False, "RC3_noTrees": False, "RC4_noScrub": False})


#  Objective function:
#  9759.0

#  The best solution found:
#  [0.01662151 0.03339998 0.07572306 0.00229839 0.01986841 0.01975722
#  0.08530632 0.08602075 0.03287396 0.02622373 0.03997985 0.03022047
#  0.19698953 0.59214711 0.79335842 0.78158966 0.12919985 0.12062618]

#  Objective function:
#  2.0

server.port = 8521 # The default
server.launch()