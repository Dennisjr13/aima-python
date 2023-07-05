import pygame
from utils import create_surface

from search import UndirectedGraph
from grid_map import GridMap
from utils import create_surface
import numpy as np


class Simulation:
    def __init__(self, env, agent):
        # boilerplate
        pygame.init()
        self.env = env

        self.screen_size = self.env.size
        self.window_size = (2 * self.screen_size[0], self.screen_size[1])

        self.agent = agent
        self.grid = GridMap(self.screen_size)
        self.screen = pygame.display.set_mode(self.window_size)

        # increase computational efficiency (boilerplate)
        self.agent_surface = create_surface(self.screen_size)
        self.goal_surface = create_surface(self.screen_size)
        self.obstacle_surface = create_surface(self.screen_size)
        self.fov_surface = create_surface(self.screen_size)
        self.fov_points_surface = create_surface(self.screen_size)
        self.hit_box_surface = create_surface(self.screen_size)

        # configurable
        self.fps = 60  # refresh rate of the simulation
        font_size = 36  # size of text on screen
        self.font = pygame.font.Font(None, font_size)  # boilerplate

        # timer
        self.timer_start = None
        self.timer_end = None  # time when the agent finds the goal

    def draw_agent(self):
        self.agent_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(self.agent_surface, (0, 0, 255),
                           self.agent.rect.center, self.agent.size)
        self.screen.blit(self.agent_surface, (0, 0))

    def draw_goal(self):
        self.goal_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(self.goal_surface, (0, 255, 0), self.env.goal, 5)
        self.screen.blit(self.goal_surface, (0, 0))

    def draw_obstacles(self):
        self.obstacle_surface.fill((0, 0, 0, 0))
        for obstacle in self.env.obstacles:
            pygame.draw.rect(self.obstacle_surface, (169, 169, 169), obstacle)
        self.screen.blit(self.obstacle_surface, (0, 0))

    def draw_field_of_view(self):
        self.fov_surface.fill((0, 0, 0, 0))
        if len(self.agent.visible_points) > 2:
            # Draw the field of view as a polygon with transparency
            pygame.draw.polygon(self.fov_surface, pygame.Color(255, 255, 255, 100), self.agent.visible_points)
        self.screen.blit(self.fov_surface, (0, 0))

    def draw_field_of_view_points(self):
        """For debugging purposes."""
        self.fov_points_surface.fill((0, 0, 0, 0))
        for point in self.agent.visible_points:
            pygame.draw.circle(self.fov_points_surface, pygame.Color(0, 0, 255, 255), point, 1)
        self.screen.blit(self.fov_points_surface, (0, 0))

    def draw_timer(self):
        if self.timer_start is not None:
            elapsed_time = pygame.time.get_ticks() - self.timer_start
            if self.timer_end is not None:
                elapsed_time = self.timer_end - self.timer_start
            text = self.font.render(f'Time: {elapsed_time / 1000:.2f}s', True, (0, 0, 0))
            self.screen.blit(text, (0, 0))

    def draw_collision_time(self):
        text = self.font.render(f'Collision Time: {self.agent.total_collision_time / 60:.2f}s', True, (0, 0, 0))
        self.screen.blit(text, (0, 25))

    def draw_hit_box(self):
        self.hit_box_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(self.screen, (255, 0, 0), self.agent.rect.center, self.agent.collision_distance,
                           1)  # Draw a red circle with a thickness of 1 pixel
        self.screen.blit(self.hit_box_surface, (0, 0))

    def draw_map(self, x='a', y='a'):
        """Draws the SLAM on the right half of the window."""
        self.agent.map.draw()
        if x == 'a':
            x = self.screen_size[0]
        if y == 'a':
            y = 0
        self.screen.blit(self.agent.map.surface, (x, y))

    def draw_grid(self, x='a', y='a'):
        """Draws the discrete version of the map.
        This is used for graph search."""
        pass

    def draw_everything(self):
        self.agent.get_field_of_view()
        self.draw_field_of_view()
        self.draw_hit_box()

        self.draw_agent()
        self.draw_goal()
        self.draw_obstacles()
        self.draw_timer()
        self.draw_collision_time()

        self.draw_field_of_view_points()  # for debugging

        self.draw_map()

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
        self.timer_start = pygame.time.get_ticks()

        while running:
            self.screen.fill((211, 211, 211))  # color of free space

            # draws things
            self.draw_everything()

            # Stop the timer if the goal is in the agent's field of view
            if self.timer_end is None and any(
                    pygame.Vector2(self.env.goal).distance_squared_to(point) <= self.agent.size ** 2 for point in
                    self.agent.visible_points):
                self.timer_end = pygame.time.get_ticks()
                self.agent.goal_found = True

            # mouseclick events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # closes the simulation window
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    within_x_bound = pygame.mouse.get_pos()[0] <= self.screen_size[0]
                    within_y_bound = pygame.mouse.get_pos()[1] <= self.screen_size[1]
                    if within_x_bound and within_y_bound:
                        self.agent.queue_action(event.pos)  # move agent towards mouse

            # the agent can't move when the goal is found
            if not self.agent.goal_found:
                self.agent.move()
            else:
                self.agent.vel = 0

            # Limit the frame rate (frames per second)
            clock.tick(self.fps)

            # Update the display
            pygame.display.flip()

            # Creates a valid graph for ProblemSolvingAgent
            graph = self.points_to_graph()

            # TODO: use an algorithm to determine next move

        pygame.quit()
