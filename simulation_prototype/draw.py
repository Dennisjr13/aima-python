import pygame
from utils import create_surface
from copy import deepcopy


class Draw:
    def __init__(self, simulation):
        self.sim = simulation
        self.screen = self.sim.screen
        self.size = self.sim.screen_size
        self.agent = self.sim.agent

        # increase computational efficiency (boilerplate)
        self.agent_surface = create_surface(self.size)
        self.goal_surface = create_surface(self.size)
        self.obstacle_surface = create_surface(self.size)
        self.hit_box_surface = create_surface(self.size)
        self.stopping_bounds_surface = create_surface(self.size)
        self.grid_surface = create_surface(self.size)

        self.path_surface = create_surface(self.size)
        self.tree_surface = create_surface(self.size)

        # debugging
        self.point_surface = create_surface(self.size)
        self.inflated_obstacles_surface = create_surface(self.size)

    def draw_everything(self):
        self.screen.fill((211, 211, 211))  # color of free space

        self.draw_inflated_obstacles()  # for debugging

        self.draw_agent()
        self.draw_obstacles()

        # self.draw_hit_box()

        # self.draw_stopping_bounds()  # for debugging

        self.draw_goal()

        self.draw_tree()
        self.draw_path()

        # self.draw_path_cost()
        # self.draw_collision_time()
        # self.draw_obs_point()  # for debugging

        self.draw_grid(self.size[0], 0)

    def draw_inflated_obstacles(self):
        # debugging
        self.inflated_obstacles_surface.fill((0, 0, 0, 0))
        color = (255, 0, 0, 100)
        for obstacle in self.sim.inflated_obstacles:
            pygame.draw.rect(self.inflated_obstacles_surface, color, obstacle)
        self.screen.blit(self.inflated_obstacles_surface, (0, 0))

    def draw_agent(self):
        self.agent_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(self.agent_surface, (0, 0, 255),
                           self.agent.rect.center, self.agent.size)
        self.screen.blit(self.agent_surface, (0, 0))

    def draw_goal(self):
        self.goal_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(self.goal_surface, (0, 180, 0), self.sim.env.goal, 5)
        self.screen.blit(self.goal_surface, (0, 0))

    def draw_obstacles(self):
        self.obstacle_surface.fill((0, 0, 0, 0))
        for obstacle in self.sim.env.obstacles:
            pygame.draw.rect(self.obstacle_surface, (169, 169, 169), obstacle)
        self.screen.blit(self.obstacle_surface, (0, 0))

    def draw_path_cost(self):
        text = self.sim.font.render(f'Path Cost: {self.sim.agent.path_cost_so_far:.2f}', True, (0, 0, 0))
        self.screen.blit(text, (0, 0))

    def draw_collision_time(self):
        text = self.sim.font.render(f'Collision Time: {self.agent.total_collision_time / 60:.2f}s', True, (0, 0, 0))
        self.screen.blit(text, (0, 25))

    def draw_hit_box(self):
        self.hit_box_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(self.hit_box_surface, (255, 0, 0),
                           self.agent.rect.center,
                           self.agent.collision_distance, 1)  # Draw a red circle with a thickness of 1 pixel
        self.screen.blit(self.hit_box_surface, (0, 0))

    def draw_stopping_bounds(self):
        """For debugging purposes."""
        self.stopping_bounds_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(self.stopping_bounds_surface, (255, 0, 255),
                           self.agent.rect.center,
                           max(self.agent.stopping_distance, 10), 1)  # Draw a red circle with a thickness of 1 pixel
        self.screen.blit(self.stopping_bounds_surface, (0, 0))

    def draw_obs_point(self):
        """For debugging purposes."""
        self.point_surface.fill((0, 0, 0, 0))
        point = self.agent.closest_obs_point
        if point is None:
            return
        pygame.draw.circle(self.point_surface, pygame.Color(255, 255, 0), point, 5)
        self.screen.blit(self.point_surface, (0, 0))

    def draw_grid(self, x=-999, y=-999):
        """Draws the discrete version of the map.
        This is used for graph search."""
        if x == -999:
            x = 0
        if y == -999:
            y = self.size[1]

        self.grid_surface.fill((255, 255, 255, 255))
        grid = self.sim.grid

        width = grid.cell_width
        height = grid.cell_height

        for i in range(grid.width):
            for j in range(grid.height):
                # fill with a color corresponding to cell status
                color = grid.cell_color(i, j)
                pygame.draw.rect(self.grid_surface, color,
                                 (i*width, j*height, width, height))

        # draw grid outlines
        bt = 1  # border thickness of grid lines

        for i in range(grid.width + 1):
            pygame.draw.line(self.grid_surface, pygame.Color(0, 0, 0, 255),
                             (i * width, 0), (i * width, self.size[1]), bt)

        for j in range(grid.height + 1):
            pygame.draw.line(self.grid_surface, pygame.Color(0, 0, 0, 255),
                             (0, j * height), (self.size[0], j * height), bt)

        self.screen.blit(self.grid_surface, (x, y))

    def draw_path(self):
        if not self.sim.has_solution:
            return
        self.path_surface.fill((0, 0, 0, 0))

        path_copy = deepcopy(self.sim.solution_path)
        path_copy.reverse()
        previous = path_copy.pop()
        while path_copy:
            current = path_copy.pop()
            pygame.draw.line(self.path_surface, pygame.Color(0, 0, 255), current, previous)
            previous = current
        self.screen.blit(self.path_surface, (0, 0))

    def draw_tree(self):
        self.tree_surface.fill((0, 0, 0, 0))

        self.draw_node(self.sim.rrt_agent.root)

        self.screen.blit(self.tree_surface, (0, 0))

    def draw_node(self, node):
        if node.parent is not None:
            pygame.draw.line(self.tree_surface, pygame.Color(255, 255, 0),
                             (node.x, node.y), (node.parent.x, node.parent.y))
        for child in node.children:
            self.draw_node(child)
