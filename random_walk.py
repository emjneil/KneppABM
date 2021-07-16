# Generalized behavior for random walking, one grid cell at a time
# Guided by randomWalker from https://github.com/projectmesa/mesa-examples/tree/master/examples/WolfSheep/wolf_sheep 

import random
from mesa import Agent


class RandomWalker(Agent):
    '''
    Class implementing random walker methods in a generalized manner.
    Not indended to be used on its own, but to inherit its methods to multiple
    other agents.
    '''
    grid = None
    x = None
    y = None
    moore = True

    def __init__(self, unique_id, pos, model, moore=True):
        '''
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        '''
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def random_move(self):
        '''
        Step one cell in any allowable direction.
        '''
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)


    def roe_move(self):
        '''
        move towards woodland and scrub
        '''
        # move: look at my neighbors
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_in_neighborhood = list(map(self.model.grid.get_cell_list_contents, next_moves)) 
        # are any of the adjoining habitats woodland or scrubland?  
        available_woodScrubCells = [obj for obj in next_in_neighborhood if (isinstance(x, habitatAgent) for x in obj)]
        only_habitats = [item[0] for item in available_woodScrubCells]
        my_choices = [i for i in only_habitats if i.condition == "woodland" or i.condition == "thorny_scrubland"]
        if len(my_choices) > 0:
            # if yes, pick one of those at random
            my_next_patch = random.choice(my_choices)
            next_move = my_next_patch.pos
        # otherwise, pick any one at random
        else:
            next_move = random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)

    
    def browser_move(self):
        '''
        move in any direction regardless of habitat type (they like anything)
        '''
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)


    def grazer_move(self):
        '''
        move towards grassland
        '''
        # move: look at my neighbors
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_in_neighborhood = list(map(self.model.grid.get_cell_list_contents, next_moves)) 
        # are any of the adjoining habitats woodland or scrubland?  
        available_grassCells = [obj for obj in next_in_neighborhood if (isinstance(x, habitatAgent) for x in obj)]
        only_habitats = [item[0] for item in available_grassCells]
        my_choices = [i for i in only_habitats if i.condition == "grassland"]
        if len(my_choices) > 0:
            # if yes, pick one of those at random
            my_next_patch = random.choice(my_choices)
            next_move = my_next_patch.pos
        # otherwise, pick any one at random
        else:
            next_move = random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)



    def mixedDiet_move(self):
        '''
        move towards grassland in spring/summer, any habitat in autumn/winter
        '''
        # if grass is available, and it's summer (March-Aug; 3-8), go there
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        # if it's spring/summer (March-Aug):
        if (3 <= self.model.schedule.time < 9 or 15 <= self.model.schedule.time < 21 or 27 <= self.model.schedule.time < 33 or 39 <= self.model.schedule.time < 45 or 51 <= self.model.schedule.time < 57 or 63 <= self.model.schedule.time < 69 or 75 <= self.model.schedule.time < 81 or 87 <= self.model.schedule.time < 93 or 99 <= self.model.schedule.time < 105 or 111 <= self.model.schedule.time < 117 or 123 <= self.model.schedule.time < 129 or 135 <= self.model.schedule.time < 141 or 147 <= self.model.schedule.time < 153 or 159 <= self.model.schedule.time < 165 or 171 <= self.model.schedule.time < 177 or 183 <= self.model.schedule.time < 189 or 195 <= self.model.schedule.time < 201 or 207 <= self.model.schedule.time < 213 or 219 <= self.model.schedule.time < 225 or 231 <= self.model.schedule.time < 237 or 243 <= self.model.schedule.time < 249 or 255 <= self.model.schedule.time < 261 or 267 <= self.model.schedule.time < 273 or 279 <= self.model.schedule.time < 285 or 291 <= self.model.schedule.time < 297):
            next_in_neighborhood = list(map(self.model.grid.get_cell_list_contents, next_moves)) 
            # is there grass near me?
            available_grassCells = [obj for obj in next_in_neighborhood if (isinstance(x, habitatAgent) for x in obj)]
            only_habitats = [item[0] for item in available_grassCells]
            my_choices = [i for i in only_habitats if i.condition == "grassland"]
            if len(my_choices) > 0:
                # if yes, pick one of those at random
                my_next_patch = random.choice(my_choices)
                next_move = my_next_patch.pos
            else:
                next_move = random.choice(next_moves)
        else:
            next_move = random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)
