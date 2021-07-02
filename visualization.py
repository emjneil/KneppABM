# # # Visualizing the Knepp ABC/ABM model # # #
from run_model import run_model
from KneppModel_ABM import roeDeer_agent, habitatAgent
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
        portrayal["scale"] = 0.5
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

    return portrayal

canvas_element = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
chart_element = ChartModule([{"Label": "Roe deer", "Color": "#666666"},
                             {"Label": "Grassland", "Color": "#68A063"},
                             {"Label": "Bare ground", "Color": "#560000"},
                             {"Label": "Thorny Scrubland", "Color": "#F0DB4F"},
                             {"Label": "Woodland", "Color": "#3C873A"},
                             ])


server = ModularServer(run_model, [canvas_element, chart_element])
                    #    "KneppModel", {"chance_reproduceSapling":0.5, "chance_reproduceYoungScrub":0.5, "chance_regrowGrass":0.5, "chance_saplingBecomingTree":0.5, "chance_youngScrubMatures":0.5,
                    #     "chance_scrubOutcompetedByTree":0.5, "chance_grassOutcompetedByTreeScrub":0.5, "chance_saplingOutcompetedByTree":0.5, "chance_saplingOutcompetedByScrub":0.5, "chance_youngScrubOutcompetedByScrub":0.5, "chance_youngScrubOutcompetedByTree":0.5,
                    #     "initial_roeDeer":10, "initial_grassland":71, "initial_woodland":12, "initial_scrubland":1,
                    #     "roeDeer_reproduce":0.5, "roeDeer_gain_from_grass":0.005, "roeDeer_gain_from_Trees":0.005, "roeDeer_gain_from_Scrub":0.005, "roeDeer_gain_from_Saplings":0.005, "roeDeer_gain_from_YoungScrub":0.005, 
                    #     "roeDeer_impactGrass": 5, "roeDeer_saplingsEaten":100, "roeDeer_youngScrubEaten":100, "roeDeer_treesEaten":10, "roeDeer_scrubEaten":10,
                    #     "width":10, "height":10})

server.port = 8521 # The default
server.launch()