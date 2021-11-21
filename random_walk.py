# Generalized behavior for random walking, one grid cell at a time
# Guided by randomWalker from https://github.com/projectmesa/mesa-examples/tree/master/examples/WolfSheep/wolf_sheep 

import random
from mesa import Agent

def get_month(self):
    return (self.schedule.time % 12) + 1
    
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
        move towards areas with most undergrowth (saplings and thorny scrub)
        '''
        # move: look at my neighbors
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_in_neighborhood = list(map(self.model.grid.get_cell_list_contents, next_moves)) 
        # are any of the adjoining habitats woodland or scrubland?  
        only_habitats = [obj[0] for obj in next_in_neighborhood if obj[0].condition != None]
        # I want the one with maximum undergrowth (saplings/young scrub)
        maximum = (max(node.edibles["saplings"] + node.edibles["youngScrub"] for node in only_habitats))
        my_choice = [i for i in only_habitats if i.edibles["saplings"] + i.edibles["youngScrub"] == maximum]
        next_move = my_choice[0].pos
        # Now move:
        self.model.grid.move_agent(self, next_move)

        # my_choices = [i for i in only_habitats if i.condition == "woodland" or i.condition == "thorny_scrubland"]
        # if len(my_choices) > 0:
        #     # if yes, pick one of those at random
        #     my_next_patch = random.choice(my_choices)
        #     next_move = my_next_patch.pos
        # # otherwise, pick any one at random
        # else:
        #     next_move = random.choice(next_moves)
        # # Now move:
        # self.model.grid.move_agent(self, next_move)

    
    def browser_move(self):
        '''
        move in any direction regardless of habitat type (they like anything)
        '''
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)


    def grazer_move(self):
        '''
        move towards grass
        '''
        # move: look at my neighbors
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_in_neighborhood = list(map(self.model.grid.get_cell_list_contents, next_moves)) 
        # where is there mostly grass?
        only_habitats = [obj[0] for obj in next_in_neighborhood if obj[0].condition != None]
        maximum = (max(node.edibles["grass"] for node in only_habitats))
        my_choice = [i for i in only_habitats if i.edibles["grass"] == maximum]
        next_move = my_choice[0].pos
        # Now move:
        self.model.grid.move_agent(self, next_move)



    def mixedDiet_move(self):
        '''
        move towards grass in spring/summer, any habitat in autumn/winter
        '''
        # if grass is available, and it's summer (March-Aug; 3-8), go there
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        # if it's spring/summer (March-Aug):
        if (3 <= self.model.get_month() < 9):
            next_in_neighborhood = list(map(self.model.grid.get_cell_list_contents, next_moves)) 
            # where is there the most grass?
            only_habitats = [obj[0] for obj in next_in_neighborhood if obj[0].condition != None]
            maximum = (max(node.edibles["grass"] for node in only_habitats))
            my_choice = [i for i in only_habitats if i.edibles["grass"] == maximum]
            next_move = my_choice[0].pos
            # Now move:
            self.model.grid.move_agent(self, next_move)
        else:
            next_move = random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)
