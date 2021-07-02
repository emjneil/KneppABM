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

    def __init__(self, pos, model, moore=True):
        '''
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        '''
        super().__init__(pos, model)
        self.pos = pos
        self.moore = moore

    # def random_move(self):
    #     '''
    #     Step one cell in any allowable direction.
    #     '''
    #     # Pick the next cell from the adjacent cells.
    #     next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
    #     next_move = random.choice(next_moves)
    #     # Now move:
    #     self.model.grid.move_agent(self, next_move)

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
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)
