import pygame
import numpy as np
from search import UndirectedGraph
from grid_map import GridMap
from RRT_agent import RRTAgent
from draw import Draw
from math import dist
from copy import deepcopy

class Simulation:
    def __init__(self, env, agent):
        # boilerplate
        pygame.init()
        self.env = env

        self.screen_size = self.env.size
        self.window_size = (self.screen_size[0], self.screen_size[1])

        self.agent = agent
        self.rrt_agent = RRTAgent(self.agent)
        # !!! [insert A* problem solving agent here]
        self.solution_path = []

        self.grid = GridMap(self.agent, self.screen_size)
        self.screen = pygame.display.set_mode(self.window_size)
        self.draw = Draw(self)

        # configurable
        self.fps = 60  # refresh rate of the simulation
        font_size = 36  # size of text on screen
        self.font = pygame.font.Font(None, font_size)  # boilerplate

        self.has_solution = False

    def plan_path(self, event):
        """
        Change the method called below to swap algorithms.
        """
        self.rrt_solve(event)
        # self.astar_solve(event)
        # self.insert_method_solve(event)

    def rrt_solve(self, event):
        """
        Plans a path from start to goal using RRT.
        Press [S] to solve. Press [M] to move the agent along the path.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # press [S] to solve
                if not self.has_solution:
                    print("Solving...")
                    self.solution_path = self.rrt_agent.solve()
                    print(f"Solved! Found with with path cost {self.rrt_agent.path_cost:2f}")
                    self.has_solution = True
            if event.key == pygame.K_m:  # press [M] to move agent along the path
                if self.has_solution:
                    print("Moving...")
                    path_copy = deepcopy(self.solution_path)
                    path_copy.pop()  # remove the starting position
                    while path_copy:
                        self.agent.queue_action(path_copy.pop())

    def astar_solve(self, event):
        """[...]"""
        # note: this is where you can put your code for interfacing with
        # the A* solving agent
        # it should return a path of coordinates that the agent can follow.
        pass

    def insert_method_solve(self, event):
        # Creates a valid graph for ProblemSolvingAgent
        # graph = self.points_to_graph()
        # TODO: use an algorithm to determine next move
        pass

    def points_to_graph(self):
        """ Create a new UndirectedGraph from the visible points on the map.
            g[0] is the current location """
        g = UndirectedGraph()
        g.locations = {0: (float(self.agent.pos[0]), float(self.agent.pos[1]))}  # current position
        for idx, point in enumerate(self.agent.visible_points, 1):
            g.locations[idx] = (point.x, point.y)

        # current node coordinates
        cur_node = g.locations[0]

        # make connections from current node to all other visible nodes
        for node_id, node_coords in g.locations.items():
            if node_id != 0:
                distance = np.linalg.norm([cur_node[0] - node_coords[0], cur_node[1] - node_coords[1]])
                g.connect(0, node_id, distance)  # TODO: should this instead make connections bi-directional?
        return g

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            # draws things
            self.draw.draw_everything()

            # if the agent reaches the goal, the simulation stops
            dist_from_goal = dist(self.agent.pos, self.env.goal)
            goal_threshold = self.agent.size * 2
            if dist_from_goal < goal_threshold:
                self.agent.goal_found = True

            # mouseclick events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # closes the simulation window

                # Path-Planning Algorithm
                self.plan_path(event)

            # the agent can't move when the goal is found
            if not self.agent.goal_found:
                self.agent.move()
            # Limit the frame rate (frames per second)
            clock.tick(self.fps)

            # Update the display
            pygame.display.flip()

        pygame.quit()
