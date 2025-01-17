from math import dist
from utils import Node
from queue import PriorityQueue


class AStarAgent:
    """ An agent class for A-Star Pathfinding """

    def __init__(self, sim, allow_diagonal_movement=False):
        self.agent = sim.agent
        self.grid_map = sim.grid
        self.obstacles = sim.inflated_obstacles
        self.max_iterations = 10 ** 6
        self.iterations = 0

        self.adjacent_nodes = ((0, -1), (0, 1), (-1, 0), (1, 0))
        if allow_diagonal_movement:
            self.adjacent_nodes = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1))

        # Use PriorityQueue and a set for the open list
        self.open_list = PriorityQueue()
        self.open_dict = {}
        self.closed_list = set()

        self.path_cost = 0
        self.explored_nodes = 0
        self.name = "A-Star"
        if allow_diagonal_movement:
            self.name = "Diagonal-" + self.name

    def solve(self):
        # Create start and goal node
        start_node = Node(self.grid_map.get_cell_idx(*self.agent.pos), None)
        start_node.g = start_node.h = start_node.f = 0
        goal_node = Node(self.grid_map.goal_location, None)
        goal_node.g = goal_node.h = goal_node.f = 0

        # Add the initial start node
        self.open_list.put((start_node.f, start_node))
        self.open_dict[start_node] = start_node.f

        # Loop until you find the end or reach max_iterations
        current_node = None
        while not self.open_list.empty():
            self.iterations += 1

            if self.iterations > self.max_iterations:
                # return the current path so far
                print("Too many iterations, unable to find solution")
                return self.build_path(current_node)

            # Get the current node
            current_node = self.open_list.get()[1]

            # Pop current off open list, add to closed list
            del self.open_dict[current_node]
            self.closed_list.add(current_node)

            self.explored_nodes += 1

            # Found the goal
            if self.grid_map.is_goal(current_node.coordinates[0], current_node.coordinates[1]):
                return self.build_path(current_node)

            # Generate children
            children = []
            for new_position in self.adjacent_nodes:
                # Get node position
                node_position = (
                    current_node.coordinates[0] + new_position[0], current_node.coordinates[1] + new_position[1])

                # Make sure point is within range of canvas
                if node_position[0] > self.grid_map.width or node_position[0] < 0 or \
                        node_position[1] > self.grid_map.height or node_position[1] < 0:
                    continue

                # Make sure point is not in an obstacle
                if self.grid_map.is_obstacle(node_position[0], node_position[1]):
                    continue

                # Create and append new node
                new_node = Node(node_position, current_node)
                children.append(new_node)

            # Loop through the children
            for child in children:
                # Check if child is on the closed list
                if child in self.closed_list:
                    continue

                # Create the f, g, and h values
                child.g = current_node.g + (((child.coordinates[0] - child.parent.coordinates[0]) ** 2) + (
                        (child.coordinates[1] - child.parent.coordinates[1]) ** 2)) ** 0.5
                child.h = (((child.coordinates[0] - goal_node.coordinates[0]) ** 2) + (
                        (child.coordinates[1] - goal_node.coordinates[1]) ** 2)) ** 0.5
                child.f = child.g + child.h

                # We check for the presence of a child in the open list by checking the open_dict
                if child in self.open_dict:
                    open_node = child  # the child is the node in open_list
                    if child.g < open_node.g:
                        # We replace the node's g value in open_dict
                        self.open_dict[child] = child.g

                        # We cannot update the node in open_list, so we add it again
                        self.open_list.put((child.f, child))
                    continue

                # Add the child to the open list
                self.open_list.put((child.f, child))
                self.open_dict[child] = child.f
                self.grid_map.set_cell_value(1, child.coordinates[0], child.coordinates[1])

        print("Couldn't get a path to destination")

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
        return path[::-1]  # Return reversed path


# for debugging purposes
if __name__ == '__main__':
    pass
