import math
from queue import PriorityQueue


class Node:
    def __init__(self, row, col, total_rows):
        self.row = row
        self.col = col
        self.color = 0
        self.neighbors = []
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == 5

    def is_open(self):
        return self.color == 4

    def is_barrier(self):
        return self.color == 1

    def is_start(self):
        return self.color == 2

    def is_end(self):
        return self.color == 3

    def reset(self):
        self.color = 0

    def make_start(self):
        self.color = 2

    def make_closed(self):
        self.color = 5

    def make_open(self):
        self.color = 4

    def make_barrier(self):
        self.color = 1

    def make_end(self):
        self.color = 3

    def make_path(self):
        self.color = 6

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])


class AStarAgent0:
    def __init__(self, sim):
        self.path_cost = 0
        self.grid_map = sim.grid
        self.width = self.grid_map.width
        self.grid = self.make_grid(self.grid_map.graph)
        self.start = self.set_start(self.grid_map.agent_location)
        self.end = self.set_end(self.grid_map.goal_location)

    def set_start(self, start_pos):
        row, col = start_pos
        if (0 <= row < len(self.grid)) and (0 <= col < self.width):
            self.start = Node(row, col, self.width)  # Create new node
            self.start.make_start()  # Set its color
            self.grid[row][col] = self.start  # Replace node in the grid
            self.update_neighbors()  # Update neighbors
        else:
            raise ValueError(f"Invalid start position: {start_pos}")

    def set_end(self, end_pos):
        row, col = end_pos
        if (0 <= row < len(self.grid)) and (0 <= col < self.width):
            self.end = Node(row, col, self.width)  # Create new node
            self.end.make_end()  # Set its color
            self.grid[row][col] = self.end  # Replace node in the grid
            self.update_neighbors()  # Update neighbors
        else:
            raise ValueError(f"Invalid end position: {end_pos}")

    def update_neighbors(self):
        for row in self.grid:
            for node in row:
                node.update_neighbors(self.grid)

    def make_node(self, row, col, node_type):
        if node_type == 2:
            node = Node(row, col, self.width)
            node.make_barrier()
        else:
            node = Node(row, col, self.width)
        return node

    def make_grid(self, input_grid):
        grid = []
        for i in range(len(input_grid)):
            grid.append([])
            for j in range(len(input_grid[i])):
                node = self.make_node(i, j, input_grid[i][j])
                grid[i].append(node)
        return grid

    def h(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            current = came_from[current]
            path.append(current.get_pos())
            self.path_cost += 1
        path.reverse()
        return path

    def solve(self):
        for row in self.grid:
            for node in row:
                node.update_neighbors(self.grid)

        path = self.algorithm(self.start, self.end)
        return path

    def algorithm(self, start, end):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {node: float("inf") for row in self.grid for node in row}
        g_score[start] = 0
        f_score = {node: float("inf") for row in self.grid for node in row}
        f_score[start] = self.h(start, end)

        open_set_hash = {start}

        while not open_set.empty():
            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                path = self.reconstruct_path(came_from, end)
                return path

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.h(neighbor.get_pos(), end.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            if current != start:
                current.make_closed()

        return False
