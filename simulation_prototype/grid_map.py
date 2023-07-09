from pygame import Color
from utils import bound

"""
API for A* Search

get_cell_idx()
is_goal()
is_obstacle()
get_center()
graph()
"""


class GridMap:
    def __init__(self, sim, width=20, height=20):
        """
        For example: a map with a screen size 500x500 pixels
        can be converted into a grid map with 100x100 cells,
        where each cell represents a 5x5 pixels area.
        """

        # boilerplate
        self.agent = sim.agent
        self.obstacles = sim.inflated_obstacles
        self.size = sim.screen_size  # size of map
        self.width = width  # width of grid (in cells)
        self.height = height  # height of grid (in cells)

        # node weights corresponding to each cell status/value
        self.UN = 0  # unexplored free space
        self.EX = 1  # explored free space
        self.OB = 2  # obstacle

        # boilerplate
        self.cell_width = self.size[0]/self.width
        self.cell_height = self.size[1]/self.height
        self.graph = self.initialize_graph()
        self.goal_location = self.get_cell_idx(*self.agent.env.goal)
        self.agent_location = self.get_cell_idx(*self.agent.pos)

        self.add_obstacle_cells()

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

    def is_agent(self, x_idx, y_idx):
        agent_x, agent_y = self.get_cell_idx(*self.agent.pos)
        return x_idx == agent_x and y_idx == agent_y

    def is_goal(self, x_idx, y_idx):
        """Returns whether the given cell has the goal."""
        goal_x, goal_y = self.goal_location[0], self.goal_location[1]
        return x_idx == goal_x and y_idx == goal_y

    def is_obstacle(self, x_idx, y_idx):
        """
        Returns whether the corresponding grid cell has an obstacle.
        """
        return self.get_cell_value(x_idx, y_idx) == self.OB

    def graph(self):
        return self.graph

    def initialize_graph(self):
        """Internal helper method."""
        # graph[i][j] corresponds to the cell
        # on the ith row, jth column
        graph = [[self.UN for _ in range(self.height)]
                 for _ in range(self.width)]
        return graph

    def cell_color(self, i, j):
        """
        Helper for drawing the grid.
        Returns the color corresponding to the status of the cell.
        """
        status = self.get_cell_value(i, j)

        if self.is_agent(i, j):
            return Color(0, 0, 255, 255)

        if self.is_goal(i, j):
            return Color(0, 255, 0, 255)

        if status == self.UN:
            return Color(255, 255, 255, 255)
        elif status == self.EX:
            return Color(0, 0, 255, 255)
        else:  # status == self.OB
            return Color(255, 0, 0, 255)

    def add_obstacle_cells(self):
        """
        Internal helper method.
        """
        for obstacle in self.obstacles:
            x, y, w, h = obstacle
            top_left = self.get_cell_idx(x, y)
            bottom_right = self.get_cell_idx(x + w, y + h)
            low_x, low_y = top_left[0], top_left[1]
            high_x, high_y = bottom_right[0], bottom_right[1]

            for i in range(low_x, high_x + 1):
                for j in range(low_y, high_y + 1):
                    self.set_cell_value(self.OB, i, j)


# for debugging purposes
if __name__ == '__main__':
    pass
