from pygame import Color
from utils import bound


class GridMap:
    def __init__(self, sim, width=100, height=100):
        """
        For example: a map with a screen size 500x500 pixels
        can be converted into a grid map with 100x100 cells,
        where each cell represents a 5x5 pixels area.
        """

        self.agent = sim.agent
        self.obstacles = sim.adjusted_obstacles

        self.size = sim.screen_size  # size of map
        self.width = width  # width of grid (in cells)
        self.height = height  # height of grid (in cells)

        self.cell_width = self.size[0]/self.width
        self.cell_height = self.size[1]/self.height

        # node weights corresponding to each cell status/value
        self.UN = 0  # unexplored free space
        self.EX = 1  # explored free space
        self.OB = 2  # obstacle

        self.graph = self.initialize_graph()
        self.add_obstacle_cells()

        self.goal_location = self.get_cell_idx(*self.agent.env.goal)

    def get_cell_value(self, x_idx, y_idx):
        return self.graph[x_idx][y_idx]

    def set_cell_value(self, new_value, x_idx, y_idx):
        self.graph[x_idx][y_idx] = new_value

    def get_cell_idx(self, x_coordinate, y_coordinate):
        """
        input: map coordinates (continuous)
        output: grid's idx coordinates (discrete)
        """
        # note: a // b  is equivalent to  floor(a/b)
        x_idx = x_coordinate // self.cell_width
        x_idx = bound(x_idx, 0, self.width - 1)

        y_idx = y_coordinate // self.cell_height
        y_idx = bound(y_idx, 0, self.height - 1)

        return int(x_idx), int(y_idx)

    def get_center(self, x_idx, y_idx):
        """
        input: coordinates of a grid cell
        output: center of the region corresponding
        to the given cell
        """
        return (x_idx + 0.5) * self.cell_width, (y_idx + 0.5) * self.cell_height

    def initialize_graph(self):
        # graph[i][j] corresponds to the cell
        # on the ith row, jth column
        graph = [[self.UN for _ in range(self.height)]
                 for _ in range(self.width)]
        return graph

    def cell_color(self, i, j):
        """Returns the color corresponding to the status of the cell."""
        status = self.get_cell_value(i, j)
        if status == self.UN:
            return Color(255, 255, 255, 255)
        elif status == self.EX:
            return Color(0, 0, 255, 255)
        else:  # status == self.OB
            return Color(255, 0, 0, 255)

    def add_obstacle_cells(self):
        for obstacle in self.obstacles:
            x, y, w, h = obstacle
            top_left = self.get_cell_idx(x, y)
            bottom_right = self.get_cell_idx(x + w, y + h)
            low_x, low_y = top_left[0], top_left[1]
            high_x, high_y = bottom_right[0], bottom_right[1]

            for i in range(low_x, high_x + 1):
                for j in range(low_y, high_y + 1):
                    self.update_cell_value(self.OB, i, j)

    def is_obstacle(self, x_idx, y_idx):
        return self.graph[x_idx][y_idx] == self.OB

    def update_cell_value(self, new_value, x_idx, y_idx):
        """Helper method, updates value of a single cell."""
        try:
            self.set_cell_value(new_value, x_idx, y_idx)
        except:
            print(x_idx, y_idx)


# for debugging purposes
if __name__ == '__main__':
    pass
