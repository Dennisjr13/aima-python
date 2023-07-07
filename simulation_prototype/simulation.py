import pygame
from search import UndirectedGraph
from grid_map import GridMap
import numpy as np
from RRT_agent import RRTAgent
import copy
from draw import Draw
from math import dist


class Simulation:
    def __init__(self, env, agent):
        # boilerplate
        pygame.init()
        self.env = env

        self.screen_size = self.env.size
        self.window_size = (self.screen_size[0], self.screen_size[1])

        self.agent = agent
        self.rrt_agent = RRTAgent(self.agent)
        self.solution_path = []

        self.grid = GridMap(self.agent, self.screen_size)
        self.screen = pygame.display.set_mode(self.window_size)
        self.draw = Draw(self)

        # configurable
        self.fps = 60  # refresh rate of the simulation
        font_size = 36  # size of text on screen
        self.font = pygame.font.Font(None, font_size)  # boilerplate

        self.has_solution = False

    def rrt_solve(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # press [S] to solve
                if not self.has_solution:
                    print("Solving...")
                    self.solution_path = self.rrt_agent.solve()
                    print("Solved!")
                    self.has_solution = True
            if event.key == pygame.K_m:  # press [M] to move agent along the path
                if self.has_solution:
                    print("Moving...")
                    path_copy = copy.deepcopy(self.solution_path)
                    path_copy.pop()  # remove the starting position
                    while path_copy:
                        self.agent.queue_action(path_copy.pop())

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

            # Stop the timer if the goal is in the agent's field of view
            # if any(pygame.Vector2(self.env.goal).distance_squared_to(point)
            #       <= self.agent.size ** 2 for point in self.agent.visible_points):
            if dist(self.agent.pos, self.env.goal) < self.agent.size:
                self.agent.goal_found = True

            # mouseclick events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # closes the simulation window
                """elif event.type == pygame.MOUSEBUTTONDOWN:
                    within_x_bound = pygame.mouse.get_pos()[0] <= self.screen_size[0]
                    within_y_bound = pygame.mouse.get_pos()[1] <= self.screen_size[1]
                    if within_x_bound and within_y_bound:
                        self.agent.queue_action(event.pos)  # move agent towards mouse"""
                self.rrt_solve(event)

            # the agent can't move when the goal is found
            if not self.agent.goal_found:
                self.grid.update_cell_values()
                self.agent.move()
            else:
                self.agent.vel = 0
            # Limit the frame rate (frames per second)
            clock.tick(self.fps)

            # Update the display
            pygame.display.flip()

            # Creates a valid graph for ProblemSolvingAgent
            # graph = self.points_to_graph()

            # TODO: use an algorithm to determine next move

        pygame.quit()
