import random
class Tile:
    def __init__(self,assigned_name):
        self.name = assigned_name
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self.neighbors = {"North": self.north, "South": self.south, "East": self.east, "West": self.west}
        self.void = False
        self.pheromone = 1
        # keeps track of how long a square is left alone.
        self.tics_since_last_update = 0

    # so apparently it is pythonic to not have getters and setters?
    # This feels weird.

    # ants cannot travel through a void square. This is modeled by it having no chance
    # in the ant's lottery of choices.

    def get_pheromone(self):
        if self.void:
            return 0
        else:
            return self.pheromone
    # HOWEVER, connections are maintained internally because
    # I want voids to come and go. So I can disrupt trails and
    # open new possibilities at my leisure.
    def toggle_void(self):
        self.void = not self.void

    def lay_pheromone(self, pheromone_to_add):
        self.pheromone += pheromone_to_add
        self.tics_since_last_update = 0

    def update_links(self):
        self.neighbors = {"North": self.north, "South": self.south, "East": self.east, "West": self.west}
    # purely the algorithm. time check conducted outside this.
    # currently it is a simple linear decay for debugging purposes.
    # later it'll be some kinda polynomial
    def decay_pheromone(self):
        self.pheromone -= 1

        # if less than 1, fix it. 1 is the bottom because otherwise
        # it is ignored completely in decision to travel.
        if self.pheromone < 1:
            print("{name} pheromone was less than 1. correcting".format(name=self.name))
            self.pheromone = 1

    # this controls when to decay.

    def time_for_decay(self,frequency):
        if(self.tics_since_last_update % frequency == frequency - 1):
            old_value = self.pheromone
            self.decay_pheromone()
            # check if there was a change. If yes, reset update counter.
            if old_value != self.pheromone:
                self.tics_since_last_update = -1
                # -1 because method always increments when called.
                # net result is it is reset to 0
        self.tics_since_last_update += 1

    # Primary reasoning: everything collapses to a single call. easier to iterate. Prettier.
    # secondary reasoning: some tiles will never be visited. walls, distant corners nowhere near food etc.
    # thus, this also sees if this tile has pheromone. Could be done by checking if the pheromone is 1 or not
    # but I've added a time delay before "shelving" it.

    def update(self):
        idle_tic_limit = 100
        check_frequency = 25 # personal recommendation: keep at idle_tic_limit // 4
        if self.tics_since_last_update <= idle_tic_limit:
            self.time_for_decay(check_frequency)

class Grid:
    def __init__(self, x, y=None):
        # Assume square unless otherwise said
        if (y is None):
            y = x

        self.x = x
        self.y = y
        tiny_array = []
        for row in range(0, x):
            new_row = []
            for column in range(0, y):
                its_name = "{x},{y}".format(x=row, y=column)
                #print(its_name)
                new_tile = Tile(its_name)
                new_row.append(new_tile)
            tiny_array.append(new_row)
        self.grid = tiny_array
        self.nest_x = self.x//2
        self.nest_y = self.y//2
        self.nest = self.grid[self.nest_x][self.nest_y] # middle

    # grid_name.get_pheromone(0,0) vs grid_name.grid[0][0].get_pheromone()
    # marginally better I suppose.
    # ALL should start with x,y followed by other parameters
    def get_pheromone(self,x,y):
        return self.grid[x][y].get_pheromone()

    def toggle_void(self,x,y):
        self.grid[x][y].toggle_void()

    def lay_pheromone(self, x, y, pheromone_to_add):
        self.grid[x][y].lay_pheromone(pheromone_to_add)

    # not important, but available. time_to_decay calls the decay_pheromone in its call
    def decay_pheromone(self, x, y):
        self.grid[x][y].decay_pheromone()
    #time_to_decay
    def decay(self,x,y,frequency):
        self.grid[x][y].time_for_decay(frequency)

    def update(self,x,y):
        self.grid[x][y].update()
    # determine if a link can indeed exist, and making them.

    def get_neighbors(self,x,y):
        return self.grid[x][y].neighbors

    def link(self,x,y):
        max_x = self.x -1
        max_y = self.y -1
        if(x-1 >= 0):
            self.grid[x][y].north = self.grid[x-1][y]
        if(x+1 <= max_x):
            self.grid[x][y].south = self.grid[x+1][y]
        if(y-1 >= 0):
            self.grid[x][y].west  = self.grid[x][y-1]
        if(y+1 <= max_y):
            self.grid[x][y].east  = self.grid[x][y+1]
        self.grid[x][y].update_links()
        #   for my own thinking.
        #   0,0 0,1 0,2
        #
        #   1,0 1,1 1,2
        #
        #   2,0 2,1 2,2


    def gen_links(self):
        max_x = self.x
        max_y = self.y
        for x in range(0,max_x):
            for y in range(0,max_y):
                print("{x},{y}".format(x = x, y = y))
                self.link(x,y)

class Ant:
    the_grid = None  # must be changed after grid creation
    def __init__(self, nest_x, nest_y,grid):
        # initializes to the nest.
        self.grid = grid
        self.nest_x = nest_x
        self.nest_y = nest_y
        self.x_pos = nest_x
        self.y_pos = nest_y
        self.stomach_capacity = 10 #How much food can an ant hold
        self.stomach_contents = 0 #Init to 0. may be bad if starvation added
        # self.social_stomach_capacity = 6 # Reminder that I eventually want more realistic feeding behavior

    # so ugly
    def sniff(self):
        adjacent_pheromone = {}
        try:
            adjacent_pheromone["North"] = self.grid.get_pheromone(self.x_pos-1,self.y_pos)
        except IndexError:
            adjacent_pheromone["North"] = 0

        try:
            adjacent_pheromone["South"] = self.grid.get_pheromone(self.x_pos+1,self.y_pos)
        except IndexError:
            adjacent_pheromone["South"] = 0

        try:
            adjacent_pheromone["West"] = self.grid.get_pheromone(self.x_pos,self.y_pos-1)
        except IndexError:
            adjacent_pheromone["West"] = 0

        try:
            adjacent_pheromone["East"] = self.grid.get_pheromone(self.x_pos,self.y_pos+1)
        except IndexError:
            adjacent_pheromone["East"] = 0

        return adjacent_pheromone

    def move_decide(self):
        adjacent_pheromone = self.sniff()
        lotto_bag = []
        for direction in adjacent_pheromone:
            while adjacent_pheromone[direction] >=1:
                lotto_bag.append("{direction}".format(direction = direction))
                adjacent_pheromone[direction] -= 1
        decision = random.choice(lotto_bag)
        return decision



def debug():
    grid = Grid(3)
    grid.gen_links()
    for x in range(0,3):
        for y in range(0,3):
            for value in grid.grid[x][y].neighbors:
                print(grid.grid[x][y].neighbors[value])
    debug_ant = Ant(grid.nest_x,grid.nest_y,grid)
    for x in range(0,10):
        print(debug_ant.move_decide())

debug()

