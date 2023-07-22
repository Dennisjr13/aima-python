from math import dist
from utils import Node
from queue import PriorityQueue

class JPSAgent:
    def __init__(self, sim):
        self.agent = sim.agent
        self.grid_map = sim.grid
        self.obstacles = sim.inflated_obstacles
        self.max_iterations = 10**6

        self.adjacent_nodes = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1))

        self.open_list = PriorityQueue()
        self.open_dict = {}
        self.closed_list = set()

        self.path_cost = 0
        self.explored_nodes = 0
        self.name = "JPS"

    def solve(self):
        start_node = Node(self.grid_map.get_cell_idx(*self.agent.pos), None)
        start_node.g = start_node.h = start_node.f = 0
        goal_node = Node(self.grid_map.goal_location, None)
        goal_node.g = goal_node.h = goal_node.f = 0

        self.open_list.put((start_node.f, start_node))
        self.open_dict[start_node] = start_node.f

        iterations = 0
        current_node = None
        while not self.open_list.empty():
            iterations += 1

            if iterations > self.max_iterations:
                print("Too many iterations, unable to find solution")
                return self.build_path(current_node)

            current_node = self.open_list.get()[1]

            del self.open_dict[current_node]
            self.closed_list.add(current_node)

            self.explored_nodes += 1

            if current_node.coordinates == goal_node.coordinates:
                return self.build_path(current_node)

            children = self.get_successors(current_node, goal_node)

            for child in children:
                if child in self.closed_list:
                    continue

                child.g = current_node.g + dist(child.coordinates, current_node.coordinates)
                child.h = dist(child.coordinates, goal_node.coordinates)
                child.f = child.g + child.h

                if child in self.open_dict:
                    open_node = child
                    if child.g < open_node.g:
                        self.open_dict[child] = child.g
                        self.open_list.put((child.f, child))
                    continue

                self.open_list.put((child.f, child))
                self.open_dict[child] = child.f
                self.grid_map.set_cell_value(1, child.coordinates[0], child.coordinates[1])

        print("Couldn't get a path to destination")

    def get_successors(self, current_node, goal_node):
        successors = []
        for direction in self.adjacent_nodes:
            next_coordinates = tuple(map(sum, zip(current_node.coordinates, direction)))
            if self.grid_map.is_valid(*next_coordinates) and not self.grid_map.is_obstacle(*next_coordinates):
                jump_node = self.jump(next_coordinates, direction, current_node)
                if jump_node is not None:
                    successors.append(jump_node)
        return successors

    def jump(self, current_coordinates, direction, parent_node):
        next_coordinates = current_coordinates
        while True:
            next_coordinates = tuple(map(sum, zip(next_coordinates, direction)))
            if not self.grid_map.is_valid(*next_coordinates) or self.grid_map.is_obstacle(*next_coordinates):
                return None
            if self.grid_map.is_goal(*next_coordinates):
                return Node(next_coordinates, parent_node)
            if self.is_forced(next_coordinates, direction):
                return Node(next_coordinates, parent_node)
            if direction[0] != 0 and direction[1] != 0:
                if self.jump(next_coordinates, (direction[0], 0), parent_node) is not None or \
                   self.jump(next_coordinates, (0, direction[1]), parent_node) is not None:
                    return Node(next_coordinates, parent_node)

        return Node(next_coordinates, parent_node)

    def is_forced(self, node_position, direction):
        dx, dy = direction
        if dx != 0:
            return ((self.grid_map.is_valid(node_position[0] + dx, node_position[1] + 1) and
                     self.grid_map.is_obstacle(node_position[0], node_position[1] + 1)) or
                    (self.grid_map.is_valid(node_position[0] + dx, node_position[1] - 1) and
                     self.grid_map.is_obstacle(node_position[0], node_position[1] - 1)))
        else:
            return ((self.grid_map.is_valid(node_position[0] + 1, node_position[1] + dy) and
                     self.grid_map.is_obstacle(node_position[0] + 1, node_position[1])) or
                    (self.grid_map.is_valid(node_position[0] - 1, node_position[1] + dy) and
                     self.grid_map.is_obstacle(node_position[0] - 1, node_position[1])))

    def build_path(self, last_node_added):
        path = []
        current = last_node_added
        while current is not None:
            cur_coords = self.grid_map.get_center(current.coordinates[0], current.coordinates[1])
            path.append(cur_coords)
            if current.parent is not None:
                par_coords = self.grid_map.get_center(current.parent.coordinates[0], current.parent.coordinates[1])
                self.path_cost += dist((cur_coords[0], cur_coords[1]), (par_coords[0], par_coords[1]))
            current = current.parent
        return path[::-1]


if __name__ == '__main__':
    pass
