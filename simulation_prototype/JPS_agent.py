from math import dist
from utils import Node
from queue import PriorityQueue


class JPSAgent:
    def __init__(self, sim):
        self.agent = sim.agent
        self.grid_map = sim.grid
        self.max_iterations = 10**6
        self.iterations = 0

        self.path_cost = 0
        self.explored_nodes = 0
        self.name = "JPS"

        # --------------------------

        self.TL = (-1, -1)  # top left
        self.T = (0, -1)  # top
        self.TR = (1, -1)  # top right
        self.L = (-1, 0)  # left
        self.R = (1, 0)  # right
        self.BL = (-1, 1)  # bottom left
        self.B = (0, 1)  # bottom
        self.BR = (1, 1)  # bottom right
        self.adjacent_nodes = (self.TL, self.T, self.TR, self.L,
                               self.R, self.BL, self.B, self.BR)

        self.open_list = PriorityQueue()
        self.open_dict = {}
        self.closed_list = set()

        # internal accumulators
        self.start_node = None
        self.goal_node = None

        self.current_node = None

    def solve(self):

        # boiler plate
        self.start_node = Node(self.grid_map.agent_location, None)
        self.goal_node = Node(self.grid_map.goal_location, None)

        self.open_list.put((self.start_node.f, self.start_node))
        self.open_dict[self.start_node] = self.start_node.f

        self.iterations = 0
        self.current_node = None

        # algorithm
        while not self.open_list.empty():

            self.iteration_update()
            current_node = self.load_next_node()

            if current_node == self.goal_node:
                return self.build_path(current_node)

            children = self.get_successors(current_node)
            # print(f"{len(children)} successors found for {current_node.coordinates}.")

            for child in children:
                if child in self.closed_list:
                    continue

                child.g = current_node.g + dist(child.coordinates, current_node.coordinates)
                child.h = dist(child.coordinates, self.goal_node.coordinates)
                child.f = child.g + child.h

                if child in self.open_dict:
                    open_node = child
                    if child.g < open_node.g:
                        self.open_dict[child] = child.g
                        self.open_list.put((child.f, child))
                    continue

                self.open_list.put((child.f, child))
                self.open_dict[child] = child.f
                # mark as explored
                self.grid_map.set_cell_value(1, child.coordinates[0], child.coordinates[1])

        print("Couldn't get a path to destination")

    def get_successors(self, current_node):
        successors = []
        for direction in self.adjacent_nodes:
            is_valid = self.is_valid(*current_node.coordinates)
            if is_valid:
                jump_node = self.jump(current_node.coordinates, direction, current_node)
                if jump_node is not None:
                    successors.append(jump_node)
        return successors

    def jump(self, current_coordinates, direction, parent_node):
        self.iteration_update()
        # print(f"Jump: {current_coordinates} | {direction}")
        next_coordinates = current_coordinates
        while True:
            next_coordinates = tuple(map(sum, zip(next_coordinates, direction)))
            if not self.is_valid(*next_coordinates):
                # print(f"D.E.: {next_coordinates} | {direction}")
                return None
            # self.grid_map.set_cell_value(self.grid_map.SO, *next_coordinates)  # !!! visual
            if self.grid_map.is_goal(*next_coordinates):
                # print("GOAL FOUND!!!")
                return Node(next_coordinates, parent_node)
            if self.is_forced(next_coordinates, direction):
                # print(f"Forced Obstacle: {next_coordinates} | {direction}")
                return Node(next_coordinates, parent_node)
            if direction[0] != 0 and direction[1] != 0:  # if diagonal
                horizontal_successor = self.jump(next_coordinates, (direction[0], 0), parent_node)
                vertical_successor = self.jump(next_coordinates, (0, direction[1]), parent_node)

                successor_in_horizontal = horizontal_successor is not None
                successor_in_vertical = vertical_successor is not None

                if successor_in_horizontal or successor_in_vertical:
                    # print(f"Successor found in diagonal {direction}")
                    return Node(next_coordinates, parent_node)

    def is_forced(self, node_position, direction):
        x, y = node_position
        dx, dy = direction

        if dx != 0:  # if moving left or right
            return ((self.is_valid(x + dx, y + 1) and self.is_obstacle(x, y + 1)) or
                    (self.is_valid(x + dx, y - 1) and self.is_obstacle(x, y - 1)))
        else:  # if moving strictly up or down
            return ((self.is_valid(x + 1, y + dy) and self.is_obstacle(x + 1, y)) or
                    (self.is_valid(x - 1, y + dy) and self.is_obstacle(x - 1, y)))

    def build_path(self, last_node_added):
        path = []
        current = last_node_added
        while current is not None:
            current_coordinates = self.grid_map.get_center(current.coordinates[0], current.coordinates[1])
            path.append(current_coordinates)
            if current.parent is not None:
                parent_coordinates = self.grid_map.get_center(current.parent.coordinates[0],
                                                              current.parent.coordinates[1])
                self.path_cost += dist((current_coordinates[0], current_coordinates[1]),
                                       (parent_coordinates[0], parent_coordinates[1]))
            current = current.parent
        return path[::-1]

    def iteration_update(self):
        self.iterations += 1
        if self.iterations > self.max_iterations:
            print("Too many iterations, unable to find solution")
            return None  # self.build_path(current_node)

    def load_next_node(self):
        self.current_node = self.open_list.get()[1]
        current_node = self.current_node

        del self.open_dict[current_node]
        self.closed_list.add(current_node)

        self.explored_nodes += 1

        return self.current_node

    def is_valid(self, i, j):
        """Returns whether the cell is valid.
        A cell is valid when it is within the grid and
        when the cell is not an obstacle."""
        return self.grid_map.is_valid(i, j)

    def is_obstacle(self, i, j):
        """Returns whether the cell is an obstacle."""
        return self.grid_map.is_obstacle(i, j)


if __name__ == '__main__':
    pass
