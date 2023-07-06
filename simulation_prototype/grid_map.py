from pygame import Color
from utils import bound


class GridMap:
    def __init__(self, agent, size, width=100, height=100):
        """
        For example: a map with a screen size 500x500 pixels
        can be converted into a grid map with 100x100 cells,
        where each cell represents a 5x5 pixels area.
        """

        self.agent = agent

        self.size = size  # size of map
        self.width = width  # width of grid (in cells)
        self.height = height  # height of grid (in cells)

        self.cell_width = self.size[0]/self.width
        self.cell_height = self.size[1]/self.height

        # node weights corresponding to each cell status/value
        self.UN = 0  # unexplored
        self.FR = 1  # free space
        self.OB = 2  # obstacle

        self.graph = self.initialize_graph()
        self.obstacle_locations = set()

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

    def initialize_graph(self):
        # graph[i][j] corresponds to the cell
        # on the ith row, jth column
        graph = [[self.UN for _ in range(self.height)]
                 for _ in range(self.width)]
        return graph

    def cell_color(self, i, j):
        """Returns the color corresponding to the status of the cell."""
        status = self.graph[i][j]
        if status == self.UN:
            return Color(0, 0, 0, 255)
        elif status == self.FR:
            return Color(255, 255, 255, 255)
        else:  # status == self.OB
            return Color(255, 0, 0, 255)

    def update_cell_values(self):
        for point in self.agent.non_obstacle_points:
            x_idx, y_idx = self.get_cell_idx(*point)
            self.update_cell_value(self.FR, x_idx, y_idx)

        for point in self.agent.obstacle_points:
            x_idx, y_idx = self.get_cell_idx(*point)
            self.update_cell_value(self.OB, x_idx, y_idx)
            self.obstacle_locations.update((x_idx, y_idx))

    def update_cell_value(self, new_value, x_idx, y_idx):
        """Helper method, updates value of a single cell."""
        try:
            self.graph[x_idx][y_idx] = new_value
        except:
            print(x_idx, y_idx)


# for debugging purposes
if __name__ == '__main__':
    gmap = GridMap((500, 500), 10, 10)
    for row in gmap.graph:
        print(row)
