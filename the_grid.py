class Grid:
    def __init__(self, x, y=None):
        # Assume square unless otherwise said

        if (y is None):
            y = x
        tiny_array = []
        for column in range(0, x):
            new_column = []
            for row in range(0, y):
                its_name = "My name is {x},{y}".format(x=column, y=row)
                print(its_name)
                new_tile = TinyTile(its_name)
                new_column.append(new_tile)
            tiny_array.append(new_column)
        self.grid = tiny_array