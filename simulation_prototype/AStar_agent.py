from math import dist

from simulation_prototype.grid_map import GridMap


class Node:
    def __init__(self, coordinates: tuple, parent=None):
        self.coordinates = coordinates
        self.parent = parent

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.coordinates == other.coordinates


class AStarAgent:

    def __init__(self, sim):
        self.agent = sim.agent
        self.grid_map = sim.grid
        #self.grid_map = GridMap(sim, 50, 50)
        self.obstacles = sim.inflated_obstacles

        self.path_cost = 0

    def solve(self):
        # Create start and goal node
        start_node = Node(self.grid_map.get_cell_idx(*self.agent.pos), None)
        start_node.g = start_node.h = start_node.f = 0
        goal_node = Node(self.grid_map.goal_location, None)
        goal_node.g = goal_node.h = goal_node.f = 0

        # Initialize both the open and closed list
        open_list = []
        closed_list = []

        # Add the initial start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if self.grid_map.is_goal(current_node.coordinates[0], current_node.coordinates[1]):
                path = []
                current = current_node
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

            # Generate children with adjacent squares
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

                # Get node position
                node_position = (current_node.coordinates[0] + new_position[0], current_node.coordinates[1] + new_position[1])

                # Make sure point is within range of canvas
                canvas = self.agent.env.size
                if node_position[0] > self.grid_map.width or node_position[0] < 0 or node_position[1] > self.grid_map.height or node_position[1] < 0:
                    continue

                # Make sure point is not in an obstacle
                if self.grid_map.is_obstacle(node_position[0], node_position[1]):
                    continue

                # Create new node
                new_node = Node(node_position, current_node)

                # Append
                children.append(new_node)

            # Loop through the children
            for child in children:

                # Check if child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.coordinates[0] - goal_node.coordinates[0]) ** 2) + ((child.coordinates[1] - goal_node.coordinates[1]) ** 2)
                child.f = child.g + child.h

                # Check if child is already on the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)


# for debugging purposes
if __name__ == '__main__':
    pass
