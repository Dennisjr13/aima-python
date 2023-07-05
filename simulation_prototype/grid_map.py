#


class GridMap:
    def __init__(self, size=(500, 500), width=100, height=100):
        """
        For example: a map with a screen size 500x500 pixels
        can be converted into a grid map with 100x100 cells,
        where each cell represents a 5x5 pixels area.
        """

        self.size = size  # size of map
        self.width = width  # width of grid (in cells)
        self.height = height  # height of grid (in cells)

        self.cell_width = self.size[0]/self.width
        self.cell_height = self.size[1]/self.height
        self.graph = self.initialize_graph()

        """
        0 -> unexplored
        1 -> free space
        2 -> obstacle
        """

    def get_cell_idx(self, x_coordinate, y_coordinate):
        """
        input: map coordinates (continuous)
        output: grid's idx coordinates (discrete)
        """
        # note: a // b  is equivalent to  floor(a/b)
        x_idx = x_coordinate // self.cell_width
        y_idx = y_coordinate // self.cell_height
        return x_idx, y_idx

    def initialize_graph(self):
        # graph[i][j] corresponds to the cell
        # on the ith row, jth column
        default_value = 0
        graph = [[default_value for j in range(self.height)]
                 for i in range(self.width)]
        return graph


# for debugging purposes
if __name__ == '__main__':
    gmap = GridMap((500, 500), 10, 10)
    for row in gmap.graph:
        print(row)
