import pygame
from math import dist
from random import randint
from math import inf
from random import random


class Node:
    def __init__(self, coordinates: tuple, parent=None):
        self.x, self.y = coordinates
        self.parent = parent
        self.children = []
        if self.parent is not None:
            self.parent.extend(self)

    def extend(self, child):
        self.children.append(child)


class RRTAgent:

    def __init__(self, agent):
        self.agent = agent
        self.goal = agent.env.goal
        self.screen_size = self.agent.env.size
        self.root = Node(self.agent.pos)  # root of tree

        self.goal_found = False
        self.iterations = 0

        # the distance between two nodes cannot exceed this
        self.distance_threshold = 20  # self.agent.size*10

        # how close a node needs to be to the goal for the goal
        # to be considered found
        self.goal_threshold = 10  # self.agent.size
        self.last_node_added = self.root
        self.rate = 0.5  # how often the tree will try to expand towards the goal

        # accumulators for internal methods
        self.point = None
        self.closest_node = None
        self.best_score = inf  # the lower, the better

    def solve(self):
        while not self.goal_found:
            self.next_move()
            last_node = self.last_node_added
            self.is_goal_reached((last_node.x, last_node.y))
        return self.build_path()

    def next_move(self):
        if random() < self.rate:
            self.point = self.goal
        else:
            self.point = self.random_point()
        self.best_score = inf
        self.find_closest_node(self.root)
        node = self.closest_node
        self.grow_tree(node)

    def random_point(self):
        """Choose a random point."""
        random_x = randint(0, self.screen_size[0])
        random_y = randint(0, self.screen_size[1])
        return random_x, random_y

    def find_closest_node(self, node):
        """Find the node on the tree closest to the chosen point."""
        current_node_score = dist((node.x, node.y), self.point)

        if current_node_score < self.best_score:
            self.best_score = current_node_score
            self.closest_node = node

        for child in node.children:
            self.find_closest_node(child)

    def grow_tree(self, node):
        """
        node - should be the closest node

        If there are no obstacles in the way,
        expand from the closest node.
        """
        if node is None:
            return
        node_position = (node.x, node.y)

        # if there are obstacles between the closest
        # node and the randomly-chosen point, do nothing
        for obstacle in self.agent.env.obstacles:
            if obstacle.clipline(node_position, self.point):
                return

        vector = (pygame.Vector2(self.point) - pygame.Vector2(node_position))
        distance = vector.length()

        if distance > self.distance_threshold:
            vector.scale_to_length(self.distance_threshold)

        new_x = node.x + vector.x
        new_y = node.y + vector.y

        self.last_node_added = Node((new_x, new_y), node)
        self.iterations += 1

    def is_goal_reached(self, point):
        if dist(point, self.goal) < self.goal_threshold:
            self.goal_found = True

    def build_path(self):
        path = []  # will be treated as a stack
        node = self.last_node_added
        while node is not None:
            path.append((node.x, node.y))
            node = node.parent
        return path


# for debugging purposes
if __name__ == '__main__':
    point1 = (0, 0)
    point2 = (3, 0)
    point3 = (6, 0)

    dist1 = dist(point1, point2)
    dist2 = dist(point1, point3)

    print(dist1, dist2)
