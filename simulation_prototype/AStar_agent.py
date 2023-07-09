import heapq
from math import dist


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

    def __init__(self, sim, allow_diagonal_movement=False):
        self.agent = sim.agent
        self.grid_map = sim.grid
        # self.grid_map = GridMap(sim, 50, 50)
        self.obstacles = sim.inflated_obstacles
        # self.max_iterations = self.grid_map.width * self.grid_map.height
        self.max_iterations = 10**6  # TODO: pick a reasonable value for this

        self.adjacent_nodes = ((0, -1), (0, 1), (-1, 0), (1, 0))
        if allow_diagonal_movement:
            self.adjacent_nodes = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1))

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
        heapq.heapify(open_list)
        heapq.heappush(open_list, start_node)

        # Loop until you find the end or reach max_iterations
        iterations = 0
        while len(open_list) > 0:
            iterations += 1

            if iterations > self.max_iterations:
                # return the current path so far
                print("Too many iterations, unable to find solution")
                return self.build_path(current_node)

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
                return self.build_path(current_node)

            # Generate children with adjacent squares
            children = []
            for new_position in self.adjacent_nodes:

                # Get node position
                node_position = (
                    current_node.coordinates[0] + new_position[0], current_node.coordinates[1] + new_position[1])

                # Make sure point is within range of canvas
                canvas = self.agent.env.size
                if node_position[0] > self.grid_map.width or node_position[0] < 0 or node_position[
                    1] > self.grid_map.height or node_position[1] < 0:
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
                child.g = current_node.g + (((child.coordinates[0] - child.parent.coordinates[0]) ** 2) + (
                        (child.coordinates[1] - child.parent.coordinates[1]) ** 2)) ** 0.5
                child.h = (((child.coordinates[0] - goal_node.coordinates[0]) ** 2) + (
                        (child.coordinates[1] - goal_node.coordinates[1]) ** 2)) ** 0.5
                child.f = child.g + child.h

                # Check if child is already on the open list
                if self.child_in_open_list(child, open_list):
                    continue

                # Add the child to the open list
                open_list.append(child)
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

    def child_in_open_list(self, child, open_list):
        index = None
        for i in range(0, len(open_list)):
            if child == open_list[i]:
                index = i
                break

        if index:
            if child.g >= open_list[index].g:
                return True
            else:
                open_list[index] = open_list[-1]
                open_list.pop()
                if index < len(open_list):
                    heapq._siftup(open_list, index)
                    heapq._siftdown(open_list, 0, index)
        return False


# for debugging purposes
if __name__ == '__main__':
    pass
