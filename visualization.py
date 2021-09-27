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
                       "KneppModel", {"chance_reproduceSapling":0.5, "chance_reproduceYoungScrub":0.5, "chance_regrowGrass":0.5, "chance_saplingBecomingTree":0.001, "chance_youngScrubMatures":0.01,
                        "chance_scrubOutcompetedByTree":0.5, "chance_grassOutcompetedByTree":0.5, "chance_grassOutcompetedByScrub":0.5, "chance_saplingOutcompetedByTree":0.5, "chance_saplingOutcompetedByScrub":0.5, "chance_youngScrubOutcompetedByScrub":0.5, "chance_youngScrubOutcompetedByTree":0.5,
                        "initial_roeDeer":12, "initial_grassland":71, "initial_woodland":12, "initial_scrubland":1, 
                        "roeDeer_reproduce":0.05, "roeDeer_gain_from_grass":0.5, "roeDeer_gain_from_Trees":0.25, "roeDeer_gain_from_Scrub":0.25, "roeDeer_gain_from_Saplings":0.15, "roeDeer_gain_from_YoungScrub":0.15, 
                        "roeDeer_impactGrass": 5, "roeDeer_saplingsEaten":100, "roeDeer_youngScrubEaten":100, "roeDeer_treesEaten":10, "roeDeer_scrubEaten":10,
                        "ponies_gain_from_grass": 0.5, "ponies_gain_from_Trees": 0.5, "ponies_gain_from_Scrub": 0.5, "ponies_gain_from_Saplings": 0.5, "ponies_gain_from_YoungScrub": 0.5, 
                        "ponies_impactGrass": 25, "ponies_saplingsEaten": 5, "ponies_youngScrubEaten": 5, "ponies_treesEaten": 5, "ponies_scrubEaten": 5, 
                        "cows_reproduce": 0.5, "cows_gain_from_grass": 0.5, "cows_gain_from_Trees": 0.5, "cows_gain_from_Scrub": 0.5, "cows_gain_from_Saplings": 0.5, "cows_gain_from_YoungScrub": 0.5, 
                        "cows_impactGrass": 10, "cows_saplingsEaten": 10, "cows_youngScrubEaten": 10, "cows_treesEaten": 10, "cows_scrubEaten": 10, 
                        "fallowDeer_reproduce": 0.5, "fallowDeer_gain_from_grass": 0.5, "fallowDeer_gain_from_Trees": 0.5, "fallowDeer_gain_from_Scrub": 0.5, "fallowDeer_gain_from_Saplings": 0.5, "fallowDeer_gain_from_YoungScrub": 0.5, 
                        "fallowDeer_impactGrass": 5, "fallowDeer_saplingsEaten": 5, "fallowDeer_youngScrubEaten": 5, "fallowDeer_treesEaten": 5, "fallowDeer_scrubEaten": 5,
                        "redDeer_reproduce": 0.5, "redDeer_gain_from_grass": 0.5, "redDeer_gain_from_Trees": 0.5, "redDeer_gain_from_Scrub": 0.5, "redDeer_gain_from_Saplings": 0.5, "redDeer_gain_from_YoungScrub": 0.5, 
                        "redDeer_impactGrass": 5, "redDeer_saplingsEaten": 5, "redDeer_youngScrubEaten": 5, "redDeer_treesEaten": 5, "redDeer_scrubEaten": 5, 
                        "pigs_reproduce": 0.5, "pigs_gain_from_grass": 0.5, "pigs_gain_from_Saplings": 0.5, "pigs_gain_from_YoungScrub": 0.5, 
                        "pigs_impactGrass": 75, "pigs_saplingsEaten": 5, "pigs_youngScrubEaten": 5, "width":50, "height":36})

server.port = 8521 # The default
server.launch()