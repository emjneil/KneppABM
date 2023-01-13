from model import KneppModel
import mesa
import mesa_geo as mg
from mesa.visualization.modules import ChartModule
from agents import FieldAgent, roe_deer_agent, exmoor_pony_agent, longhorn_cattle_agent, fallow_deer_agent, red_deer_agent, tamworth_pig_agent, european_bison_agent, european_elk_agent, reindeer_agent

# visualise 
def schelling_draw(agent):
    portrayal = dict()
    if isinstance(agent, FieldAgent):
        if agent.condition == "grassland":
            portrayal["color"] = "#3C873A"
        if agent.condition == "thorny_scrubland":
            portrayal["color"] = "#FFD43B"
        if agent.condition == "woodland":
            portrayal["color"] = "Blue"        
        if agent.condition == "bare_ground":
            portrayal["color"] = "Brown"
    elif isinstance(agent, roe_deer_agent):
        portrayal["radius"] = 1
        portrayal["shape"] = "circle"
        portrayal["color"] = "Red"
    elif isinstance(agent, exmoor_pony_agent):
        portrayal["radius"] = 1
        portrayal["shape"] = "circle"
        portrayal["color"] = "Purple"
    elif isinstance(agent, longhorn_cattle_agent):
        portrayal["radius"] = 1
        portrayal["shape"] = "circle"
        portrayal["color"] = "#4B8BBE"
    elif isinstance(agent, fallow_deer_agent):
        portrayal["radius"] = 1
        portrayal["shape"] = "circle"
        portrayal["color"] = "#F16529"
    elif isinstance(agent, red_deer_agent):
        portrayal["radius"] = 1
        portrayal["shape"] = "circle"
        portrayal["color"] = "#BC473A"
    elif isinstance(agent, tamworth_pig_agent):
        portrayal["radius"] = 1
        portrayal["shape"] = "circle"
        portrayal["color"] = "Black"
    return portrayal

map_element = mg.visualization.MapModule(schelling_draw, [50.971, -0.376], 14)

chart_element = ChartModule([{"Label": "Roe deer", "Color": "Red"}, 
                            {"Label": "Exmoor pony", "Color": "Purple"},
                            {"Label": "Fallow deer", "Color": "#F16529"},
                            {"Label": "Longhorn cattle", "Color": "#4B8BBE"},
                            {"Label": "Red deer", "Color": "#BC473A"},
                            {"Label": "Tamworth pigs", "Color": "Black"},
                             {"Label": "Grassland", "Color": "#3C873A"},
                             {"Label": "Bare ground", "Color": "#560000"},
                             {"Label": "Thorny Scrub", "Color": "#FFD43B"},
                             {"Label": "Woodland", "Color": "Blue"}])

server = mesa.visualization.ModularServer(
    KneppModel, 
    [map_element, chart_element],
    "Knepp Estate", {"roe_deer_reproduce":0.18, "roe_deer_gain_from_saplings":0.25,"roe_deer_gain_from_trees":0.7, "roe_deer_gain_from_scrub":0.5,"roe_deer_gain_from_young_scrub":0.25, "roe_deer_gain_from_grass":0.75,
                    "chance_youngScrubMatures":0.05, "chance_saplingBecomingTree":0.01, "chance_reproduceSapling":0.25,"chance_reproduceYoungScrub":0.35, "chance_regrowGrass":0.9, 
                    "chance_grassOutcompetedByTree": 0.5, "chance_grassOutcompetedByScrub":0.5,"chance_scrubOutcompetedByTree":0.5, "chance_saplingOutcompetedByTree": 0.5, "chance_saplingOutcompetedByScrub": 0.5, "chance_youngScrubOutcompetedByTree":0.5, "chance_youngScrubOutcompetedByScrub":0.5, 
                    "ponies_gain_from_saplings": 0.7, "ponies_gain_from_trees":0.5, "ponies_gain_from_scrub":0.6, "ponies_gain_from_young_scrub":0.7, "ponies_gain_from_grass":0.8, 
                    "cattle_reproduce":0.25, "cows_gain_from_grass":0.75, "cows_gain_from_trees":0.5, "cows_gain_from_scrub":0.5, "cows_gain_from_saplings":0.25, "cows_gain_from_young_scrub":0.25,
                    "fallow_deer_reproduce":0.3, "fallow_deer_gain_from_saplings":0.25, "fallow_deer_gain_from_trees":0.5, "fallow_deer_gain_from_scrub":0.5, "fallow_deer_gain_from_young_scrub":0.25, "fallow_deer_gain_from_grass":0.8,
                    "red_deer_reproduce":0.2, "red_deer_gain_from_saplings":0.1, "red_deer_gain_from_trees":0.5, "red_deer_gain_from_scrub":0.6, "red_deer_gain_from_young_scrub":0.1, "red_deer_gain_from_grass":0.7,
                    "tamworth_pig_reproduce":0.3, "tamworth_pig_gain_from_saplings":0.1,"tamworth_pig_gain_from_trees":0.5,"tamworth_pig_gain_from_scrub":0.7,"tamworth_pig_gain_from_young_scrub":0.2,"tamworth_pig_gain_from_grass":0.7,
                    "european_bison_reproduce":0.2, "european_bison_gain_from_grass":0.8, "european_bison_gain_from_trees":0.5, "european_bison_gain_from_scrub":0.5, "european_bison_gain_from_saplings":0.2, "european_bison_gain_from_young_scrub":0.2,
                    "european_elk_reproduce":0.2, "european_elk_gain_from_grass":0.8, "european_elk_gain_from_trees":0.5, "european_elk_gain_from_scrub":0.5, "european_elk_gain_from_saplings":0.2, "european_elk_gain_from_young_scrub":0.2,
                    "reindeer_reproduce":0.2, "reindeer_gain_from_grass":0.8, "reindeer_gain_from_trees":0.5, "reindeer_gain_from_scrub":0.5, "reindeer_gain_from_saplings":0.2, "reindeer_gain_from_young_scrub":0.2,
                    "fallowDeer_stocking":100, "cattle_stocking":100, "redDeer_stocking":100, "tamworthPig_stocking":100, "exmoor_stocking":100,
                    "fallowDeer_stocking_forecast":100, "cattle_stocking_forecast":50, "redDeer_stocking_forecast":35, "tamworthPig_stocking_forecast":50, "exmoor_stocking_forecast":10, "introduced_species_stocking_forecast":50, 
                    "max_time": 300, "reintroduction": True, "introduce_euroBison": False, "introduce_elk": False, "introduce_reindeer": False
}
)

server.port = 8521 # The default
server.launch()