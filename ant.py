class Ant:
    def __init__(self, nest_x, nest_y):
        # initializes to the nest.
        self.x_pos = nest_x
        self.y_pos = nest_y
        self.stomach_capacity = 10 #How much food can an ant hold
        self.stomach_contents = 0 #Init to 0. may be bad if starvation added
        # self.social_stomach_capacity = 6 # Reminder that I eventually want more realistic feeding behavior

    def go_somewhere(self):
        return None