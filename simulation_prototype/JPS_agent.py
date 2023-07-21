import heapq
from math import dist
from utils import Node


class JPSAgent:
    """ An agent class for JPS Pathfinding """
    def __init__(self, sim, allow_diagonal_movement=False):
        self.agent = sim.agent
        self.grid_map = sim.grid
        self.obstacles = sim.inflated_obstacles
        self.max_iterations = 10**6

        self.adjacent_nodes = ((0, -1), (0, 1), (-1, 0), (1, 0))
        if allow_diagonal_movement:
            self.adjacent_nodes = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1))

        self.open_list = []
        self.closed_list = set()

        self.path_cost = 0
        self.explored_nodes = 0
        self.name = "JPS"

    def solve(self):
        start_node = Node(self.grid_map.get_cell_idx(*self.agent.pos), None)
        start_node.g = start_node.h = start_node.f = 0
        goal_node = Node(self.grid_map.goal_location, None)
        goal_node.g = goal_node.h = goal_node.f = 0

        heapq.heapify(self.open_list)
        heapq.heappush(self.open_list, start_node)

        iterations = 0
        current_node = None
        while len(self.open_list) > 0:
            iterations += 1

            if iterations > self.max_iterations:
                print("Too many iterations, unable to find solution")
                return self.build_path(current_node)

            current_node = heapq.heappop(self.open_list)
            self.closed_list.add(current_node)

            self.explored_nodes += 1

            if self.grid_map.is_goal(current_node.coordinates[0], current_node.coordinates[1]):
                return self.build_path(current_node)

            children = self.get_successors(current_node, goal_node)

            for child in children:
                if child in self.closed_list:
                    continue

                child.g = current_node.g + dist(child.coordinates, current_node.coordinates)
                child.h = dist(child.coordinates, goal_node.coordinates)
                child.f = child.g + child.h

                if self.child_in_open_list(child):
                    continue

                heapq.heappush(self.open_list, child)
                self.grid_map.set_cell_value(1, child.coordinates[0], child.coordinates[1])

        print("Couldn't get a path to destination")

    def get_successors(self, current_node, goal_node):
        successors = []
        for direction in self.adjacent_nodes:
            next_node = self.jump(current_node.coordinates, direction, goal_node, current_node)
            if next_node:
                successors.append(next_node)
        return successors

    def jump(self, node_position, direction, goal_node, parent_node):
        while True:
            next_position = (node_position[0] + direction[0], node_position[1] + direction[1])

            if next_position[0] > self.grid_map.width or next_position[0] < 0 or \
                    next_position[1] > self.grid_map.height or next_position[1] < 0 or \
                    self.grid_map.is_obstacle(next_position[0], next_position[1]):
                return None

            if self.grid_map.is_goal(next_position[0], next_position[1]):
                return Node(next_position, parent_node)

            if self.is_forced(next_position, direction):
                return Node(next_position, parent_node)

            node_position = next_position

    def is_forced(self, node_position, direction):
        dx, dy = direction
        if dx != 0:
            if (self.grid_map.is_valid(node_position[0], node_position[1] + 1) and
                not self.grid_map.is_obstacle(node_position[0] - dx, node_position[1] + 1)) or \
                    (self.grid_map.is_valid(node_position[0], node_position[1] - 1) and
                     not self.grid_map.is_obstacle(node_position[0] - dx, node_position[1] - 1)):
                return True
        else:
            if (self.grid_map.is_valid(node_position[0] + 1, node_position[1]) and
                not self.grid_map.is_obstacle(node_position[0] + 1, node_position[1] - dy)) or \
                    (self.grid_map.is_valid(node_position[0] - 1, node_position[1]) and
                     not self.grid_map.is_obstacle(node_position[0] - 1, node_position[1] - dy)):
                return True
        return False

    def build_path(self, last_node_added):
        path = []
        current = last_node_added
        while current is not None:
            cur_coords = self.grid_map.get_center(current.coordinates[0],
                                                  current.coordinates[1])
            path.append(cur_coords)
            if current.parent is not None:
                par_coords = self.grid_map.get_center(current.parent.coordinates[0],
                                                      current.parent.coordinates[1])
                self.path_cost += dist((cur_coords[0], cur_coords[1]),
                                       (par_coords[0], par_coords[1]))

            current = current.parent
        return path[::-1]

    def child_in_open_list(self, child):
        for open_node in self.open_list:
            if child == open_node:
                if child.g < open_node.g:
                    open_node.g = child.g
                    open_node.f = child.f
                    open_node.h = child.h
                return True
        return False


if __name__ == '__main__':
    pass
