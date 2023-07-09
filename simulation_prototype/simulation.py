import pygame
import time
from grid_map import GridMap
from RRT_agent import RRTAgent
from AStar_agent import AStarAgent
from draw import Draw
from math import dist
from copy import deepcopy


class Simulation:
    def __init__(self, env, agent):
        # boilerplate
        pygame.init()
        self.env = env

        self.screen_size = self.env.size
        self.window_size = (2 * self.screen_size[0], self.screen_size[1])

        self.agent = agent

        self.adjusted_obstacles = self.adjust_obstacles(self.agent.collision_distance)
        self.grid = GridMap(self)
        self.rrt_agent = RRTAgent(self)
        self.astar_agent = AStarAgent(self)
        self.solution_path = []

        self.screen = pygame.display.set_mode(self.window_size)
        self.draw = Draw(self)

        # configurable
        self.fps = 60  # refresh rate of the simulation
        font_size = 36  # size of text on screen
        self.font = pygame.font.Font(None, font_size)  # boilerplate

        self.has_solution = False

    def adjust_obstacles(self, threshold):
        """
        Helper method. Essentially prevents the agent from entering within
        a certain distance from any obstacle.
        """
        obstacles = self.env.obstacles
        output = []
        for obstacle in obstacles:
            x, y, w, h = obstacle
            new_x = x - threshold
            new_y = y - threshold
            new_width = w + threshold * 2
            new_height = h + threshold * 2
            output.append(pygame.Rect(new_x, new_y, new_width, new_height))
        return output

    def plan_path(self, event):
        """
        Change the method called below to swap algorithms.
        """
        # self.rrt_solve(event)
        # self.astar_solve(event)
        self.general_solve(event, self.astar_agent)

    def general_solve(self, event, solver_agent):
        """
        Plans a path from start to goal using the given solver_agent.
        Press [S] to solve. Press [M] to move the agent along the path.

        NOTE: solver_agent MUST have
            1.) a .solve() method that returns
                a solution path (a stack of coordinates
                where the starting coordinates of the agent is on top of the stack)
            2.) a .path_cost attribute that keeps track of the path cost of the
                returned solution
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # press [S] to solve
                if not self.has_solution:
                    print("Solving...")
                    initial_time = time.time()
                    self.solution_path = solver_agent.solve()
                    final_time = time.time()
                    elapsed_time = final_time - initial_time  # in seconds
                    print(f"Solved! It took {elapsed_time} seconds to find a path with cost {solver_agent.path_cost:2f}")
                    self.has_solution = True
            if event.key == pygame.K_m:  # press [M] to move agent along the path
                if self.has_solution:
                    print("Moving...")
                    path_copy = deepcopy(self.solution_path)
                    path_copy.pop()  # remove the starting position
                    while path_copy:
                        self.agent.queue_action(path_copy.pop())

    def move_agent_with_mouse(self, event):
        """For debugging."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            within_x_bound = pygame.mouse.get_pos()[0] <= self.screen_size[0]
            within_y_bound = pygame.mouse.get_pos()[1] <= self.screen_size[1]
            if within_x_bound and within_y_bound:
                self.agent.queue_action(event.pos)  # move agent towards mouse
                self.agent.queue_action(event.pos)  # move agent towards mouse

    def run(self):
        running = True
        clock = pygame.time.Clock()
        displayed_found = False

        while running:
            # draws things
            self.draw.draw_everything()

            # if the agent reaches the goal, the simulation stops
            dist_from_goal = dist(self.agent.pos, self.env.goal)
            goal_threshold = self.agent.size * 2
            if dist_from_goal < goal_threshold:
                self.agent.goal_found = True
                if not displayed_found:
                    print("Found!")
                    displayed_found = True

            # mouseclick events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # closes the simulation window
                # self.move_agent_with_mouse(event)
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
