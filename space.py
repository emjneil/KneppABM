import mesa
import mesa_geo as mg
from agents import FieldAgent
from typing import Dict


class FieldSpace(mg.GeoSpace):
    _id_region_map: Dict[str, FieldAgent]
    num_people: int

    def __init__(self):
        super().__init__(crs="epsg:27700")
        self._id_region_map = {}
        self.num_people = 0

    def add_fields(self, agents):
        super().add_agents(agents)
        for agent in agents:
            self._id_region_map[agent.unique_id] = agent
    
    def add_herbivore_agent(self, herbivore, field_id):
        herbivore.field_id = field_id
        herbivore.geometry = self._id_region_map[field_id].random_point()
        super().add_agents(herbivore)
        self.num_people += 1

    def remove_herbivore_agent(self, person):
        person.field_id = None
        super().remove_agent(person)
        self.num_people -= 1

    def get_region_by_id(self, unique_id) -> FieldAgent:
        return self._id_region_map.get(unique_id)

    def move_agent(self, agent, field) -> None:
        # pos = self.torus_adj(pos)
        self.remove_herbivore_agent(agent)
        self.add_herbivore_agent(agent, field_id=field.unique_id)