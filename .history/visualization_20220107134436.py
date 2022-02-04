# # # Visualizing the Knepp ABC/ABM model # # #
from KneppModel_ABM import KneppModel, roeDeer_agent, habitatAgent, fallowDeer, redDeer, tamworthPigs, exmoorPony, longhornCattle
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
        portrayal["scale"] = 0.8
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
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"

    if type(agent) is redDeer:
        portrayal["Shape"] = "redDeerShape.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"
        
    if type(agent) is exmoorPony:
        portrayal["Shape"] = "ponyShape.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"

    if type(agent) is fallowDeer:
        portrayal["Shape"] = "fallowDeerShape.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"

    if type(agent) is tamworthPigs:
        portrayal["Shape"] = "pigShape.png"
        portrayal["scale"] = 0.8
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"
        
    return portrayal


canvas_element = CanvasGrid(agent_portrayal, 50, 36, 750, 540)
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
                       "KneppModel", {"chance_reproduceSapling":0.26, "chance_reproduceYoungScrub":0.61, "chance_regrowGrass":0.76, "chance_saplingBecomingTree":0.00002, "chance_youngScrubMatures":0.0011,
                        "chance_scrubOutcompetedByTree":0.84, "chance_grassOutcompetedByTree":0.34, "chance_grassOutcompetedByScrub":0.24, "chance_saplingOutcompetedByTree":0.13, "chance_saplingOutcompetedByScrub":0.31, "chance_youngScrubOutcompetedByScrub":0.041, "chance_youngScrubOutcompetedByTree":0.086,
                        "initial_roeDeer":0.12, "initial_grassland":0.71, "initial_woodland":0.12, "initial_scrubland":0.01, 
                        "roeDeer_reproduce":0.051, "roeDeer_gain_from_grass":0.015, "roeDeer_gain_from_Trees":0.032, "roeDeer_gain_from_Scrub":0.059, "roeDeer_gain_from_Saplings":0.0012, "roeDeer_gain_from_YoungScrub":0.0032, 
                        "ponies_gain_from_grass": 0.5, "ponies_gain_from_Trees": 0.5, "ponies_gain_from_Scrub": 0.5, "ponies_gain_from_Saplings": 0.5, "ponies_gain_from_YoungScrub": 0.5, 
                        "cows_reproduce": 0.5, "cows_gain_from_grass": 0.5, "cows_gain_from_Trees": 0.5, "cows_gain_from_Scrub": 0.5, "cows_gain_from_Saplings": 0.5, "cows_gain_from_YoungScrub": 0.5, 
                        "fallowDeer_reproduce": 0.5, "fallowDeer_gain_from_grass": 0.5, "fallowDeer_gain_from_Trees": 0.5, "fallowDeer_gain_from_Scrub": 0.5, "fallowDeer_gain_from_Saplings": 0.5, "fallowDeer_gain_from_YoungScrub": 0.5, 
                        "redDeer_reproduce": 0.5, "redDeer_gain_from_grass": 0.5, "redDeer_gain_from_Trees": 0.5, "redDeer_gain_from_Scrub": 0.5, "redDeer_gain_from_Saplings": 0.5, "redDeer_gain_from_YoungScrub": 0.5, 
                        "pigs_reproduce": 0.5, "pigs_gain_from_grass": 0.5, "pigs_gain_from_Saplings": 0.5, "pigs_gain_from_YoungScrub": 0.5, 
                        "width":25, "height":18, 
                        "max_time": 141, "reintroduction": False, 
                        "RC1_noFood": False, "RC2_noTreesScrub": False, "RC3_noTrees": False, "RC4_noScrub": False})

server.port = 8521 # The default
server.launch()