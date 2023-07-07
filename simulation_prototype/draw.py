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
        self.fov_surface = create_surface(self.size)
        self.fov_points_surface = create_surface(self.size)
        self.hit_box_surface = create_surface(self.size)
        self.stopping_bounds_surface = create_surface(self.size)
        self.grid_surface = create_surface(self.size)

        self.path_surface = create_surface(self.size)
        self.tree_surface = create_surface(self.size)

    def draw_everything(self):
        self.screen.fill((211, 211, 211))  # color of free space

        # self.agent.get_field_of_view()
        # self.draw_field_of_view()

        self.draw_agent()
        self.draw_obstacles()

        self.draw_hit_box()

        # self.draw_field_of_view_points()  # for debugging
        # self.draw_stopping_bounds()  # for debugging

        self.draw_goal()

        self.draw_tree()
        self.draw_path()

        self.draw_path_cost()
        self.draw_collision_time()  # not relevant anymore

        # self.draw_map()
        # self.draw_grid(self.size[0], 0)

    def draw_agent(self):
        self.agent_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(self.agent_surface, (0, 0, 255),
                           self.agent.rect.center, self.agent.size)
        self.screen.blit(self.agent_surface, (0, 0))

    def draw_goal(self):
        self.goal_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(self.goal_surface, (0, 255, 0), self.sim.env.goal, 5)
        self.screen.blit(self.goal_surface, (0, 0))

    def draw_obstacles(self):
        self.obstacle_surface.fill((0, 0, 0, 0))
        for obstacle in self.sim.env.obstacles:
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

    def draw_path_cost(self):
        text = self.sim.font.render(f'Path Cost: {self.sim.rrt_agent.path_cost:.2f}', True, (0, 0, 0))
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
        print(self.agent.stopping_distance)
        self.screen.blit(self.stopping_bounds_surface, (0, 0))

    def draw_map(self, x=-999, y=-999):
        """Draws the SLAM on the right half of the window."""
        self.agent.map.draw()
        if x == -999:
            x = self.size[0]
        if y == -999:
            y = 0
        self.screen.blit(self.agent.map.surface, (x, y))

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
        path_length = len(self.sim.solution_path)
        if not self.sim.has_solution:
            return
        self.path_surface.fill((0, 0, 0, 0))

        path_copy = deepcopy(self.sim.solution_path)
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
