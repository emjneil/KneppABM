import mesa
import mesa_geo as mg
import geopandas as gpd
import random
import numpy as np
import uuid
from shapely.geometry import Point
from random_walk import RandomWalker


class GeoModel(mesa.Model):
    def __init__(self):
        # first define the space and add the field polygon agents
        self.space = FieldSpace()
        ac = mg.AgentCreator(agent_class=FieldAgent, model=self, crs="epsg:4326")
        fields = ac.from_file("field_grids.shp", unique_id="id")
        self.space.add_agents(fields)

        self.schedule = mesa.time.RandomActivation(self)

        # then add the herbivores as points
        for _ in range(15): # number of roe deer
            field = random.choice(fields) # randomly pick field
            energy = np.random.uniform(0, 1)
            roe = RoeDeerAgent(
                unique_id=uuid.uuid4().int,
                model = self,
                crs=self.space.crs,
                geometry=field.random_point(),
                field_id=field.unique_id,
                energy = energy
                )
            self.space.add_herbivore_agent(roe, field_id=field.unique_id)
            self.schedule.add(roe)
    
    def step(self):
        self.schedule.step()




m = GeoModel()

agent = m.space.agents[0]
print(agent.unique_id)
agent.geometry



# visualise 
def schelling_draw(agent):
    portrayal = dict()
    if isinstance(agent, FieldAgent):
        portrayal["color"] = "Blue"
    elif isinstance(agent, RoeDeerAgent):
        portrayal["radius"] = 1
        portrayal["shape"] = "circle"
        portrayal["color"] = "Red"
    return portrayal

map_element = mg.visualization.MapModule(schelling_draw, [50.971, -0.376], 14)

server = mesa.visualization.ModularServer(
    GeoModel, 
    [map_element],
    "Knepp Estate"
)

server.port = 8521 # The default
server.launch()