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

    def __init__(self, agent):
        self.agent = agent
        self.goal = agent.env.goal
        self.start = self.agent.pos
        self.screen_size = self.agent.env.size

        self.path_cost = 0

    def solve(self):
        # Create start and goal node
        start_node = Node(self.start, None)
        start_node.g = start_node.h = start_node.f = 0
        goal_node = Node(self.goal, None)
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
            if current_node == goal_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.coordinates)
                    current = current.parent
                return path[::-1]  # Return reversed path

            # Generate children with adjacent squares
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

                # Get node position
                node_position = (current_node.coordinates[0] + new_position[0], current_node.coordinates[1] + new_position[1])

                # Make sure point is within range of canvas
                if node_position[0] > self.screen_size[0] or node_position[0] < 0 or node_position[1] > self.screen_size[1] or node_position[1] < 0:
                    continue

                # Make sure point is not in an obstacle
                collide_point = False
                for obstacle in self.agent.env.obstacles:
                    if obstacle.collidepoint(node_position):
                        collide_point = True
                if collide_point:
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
