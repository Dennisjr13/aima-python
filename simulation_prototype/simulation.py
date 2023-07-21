import pygame
import time
from grid_map import GridMap
from RRT_agent import RRTAgent
from AStar_agent import AStarAgent
from JPS_agent import JPSAgent
from updated_astar_agent import AStarAgent as TempAStarAgent
from draw import Draw
from math import dist
from utils import append_to_csv


class Simulation:
    def __init__(self, env, agent, file_name):
        # boilerplate
        pygame.init()
        pygame.display.set_caption(file_name)
        self.env = env

        self.file_name = file_name
        self.screen_size = self.env.size
        self.window_size = (2*self.screen_size[0], self.screen_size[1])

        self.agent = agent

        self.inflated_obstacles = self.inflate_obstacles(self.agent.collision_distance)
        self.grid = GridMap(self, 40, 40)
        self.rrt_agent = RRTAgent(self)
        self.astar_agent = AStarAgent(self)
        self.jps_agent = JPSAgent(self)

        self.temp_astar_agent = TempAStarAgent(self)  # !!! temporary

        self.solution_path = []

        self.screen = pygame.display.set_mode(self.window_size)
        self.draw = Draw(self)

        # configurable
        self.fps = 60  # refresh rate of the simulation
        font_size = 36  # size of text on screen
        self.font = pygame.font.Font(None, font_size)  # boilerplate

        self.has_solution = False

    def inflate_obstacles(self, threshold):
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

    def rrt_experiment(self, event):
        """
        Not needed for simulation to run.

        Automates the data collection process.
        Outputs both raw and aggregate data.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # press [S] to solve
                if self.has_solution:
                    return

                csv_name = self.file_name + ".csv"

                headers = ['Trial No.', 'Distance Threshold', 'Rate', 'Path Cost', 'Iterations', 'Time Cost']
                append_to_csv(csv_name, headers)

                thresholds = [10, 50, 100]
                rates = [0, 0.25, 0.5, 0.75]

                trials = 30

                for t in thresholds:
                    for r in rates:
                        print(f"Threshold: {t}, Rate: {r}")
                        total_p = total_i = total_time = 0
                        for trial_number in range(1, trials + 1):
                            path_cost, iterations, time_cost = self.rrt_trial(trial_number, t, r, csv_name)
                            total_p += path_cost
                            total_i += iterations
                            total_time += time_cost
                        avg_p = total_p/trials
                        avg_i = total_i/trials
                        avg_t = total_time/trials

                        summarized_data = [self.file_name, t, r, avg_p, avg_i, avg_t]
                        # append_to_csv("RRT Experimental Data/rrt_summary.csv", summarized_data)
                        # disabled, it has served its purpose
                self.has_solution = True
                print("Done.")

    def astar_experiment(self, event):
        pass

    def rrt_trial(self, trial_number, distance_threshold, rate, file_name):
        """
        Not needed for simulation to run.

        Helper method for experiment data collection.
        """
        # Test the function
        # path_agent = RRTAgent(self)

        initial_time = time.time()
        self.solution_path = path_agent.solve()
        final_time = time.time()

        time_cost = final_time - initial_time  # in seconds
        path_cost = path_agent.path_cost
        iterations = path_agent.iterations

        data = [trial_number, distance_threshold, rate, path_cost, iterations, time_cost]
        append_to_csv(file_name, data)
        return path_cost, iterations, time_cost

    def plan_path(self, event):
        """
        Change the method called below to swap algorithms.
        """
        # self.general_solve(event, self.rrt_agent, reverse=True)
        # self.general_solve(event, self.astar_agent)
        # self.rrt_experiment(event)  # do not use this

        self.general_solve(event, self.jps_agent)
        # self.general_solve(event, self.temp_astar_agent)
        # self.compare_astar(event)

    def general_solve(self, event, solver_agent, reverse=False):
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
                    print(f"Solved! It took {elapsed_time} seconds to find "
                          f"a path with cost {solver_agent.path_cost:2f}")
                    if reverse:
                        self.solution_path.reverse()
                    self.has_solution = True
            if event.key == pygame.K_m:  # press [M] to move agent along the path
                if self.has_solution:
                    print("Moving...")
                    for action in self.solution_path:
                        self.agent.queue_action(action)

    def compare_astar(self, event):
        """
        Testing to see whether A* or JPS is better.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # press [S] to solve
                self.compare_print(self.astar_agent)
                self.compare_print(self.temp_astar_agent)
                self.compare_print(self.jps_agent)
                self.compare_print(self.rrt_agent)

    def compare_print(self, solver_agent):
        print("Solving...")
        initial_time = time.time()
        self.solution_path = solver_agent.solve()
        final_time = time.time()
        elapsed_time = final_time - initial_time  # in seconds
        print(f"Solved! It took {elapsed_time} seconds to find "
              f"a path with cost {solver_agent.path_cost:2f}")

        if solver_agent.name == "RRT":
            metric = solver_agent.iterations
        else:
            metric = solver_agent.explored_nodes

        print(f"{solver_agent.name}: {metric} "
              f"nodes explored, path cost is {solver_agent.path_cost}.")

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
