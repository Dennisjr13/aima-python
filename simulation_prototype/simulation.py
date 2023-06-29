import pygame
from utils import create_surface


class Simulation:
    def __init__(self, env, agent):
        # boilerplate
        pygame.init()
        self.env = env
        self.agent = agent
        self.map = self.agent.map

        self.screen_size = self.env.size
        self.window_size = (2*self.screen_size[0], self.screen_size[1])

        self.screen = pygame.display.set_mode(self.window_size)

        # increase computational efficiency
        self.agent_surface = create_surface(self.screen_size)
        self.goal_surface = create_surface(self.screen_size)
        self.obstacle_surface = create_surface(self.screen_size)
        self.fov_surface = create_surface(self.screen_size)
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

    def draw_map(self):
        """Draws the SLAM on the right half of the window."""
        self.map.draw_explored()
        self.agent.map.draw_agent()
        self.agent.map.draw_goal()
        self.agent.map.draw_path()
        self.agent.map.draw_obstacle_highlights()
        self.screen.blit(self.agent.map.surface, (self.screen_size[0], 0))

    def draw_everything(self):
        self.agent.get_field_of_view()
        self.draw_field_of_view()
        self.draw_hit_box()

        self.draw_agent()
        self.draw_goal()
        self.draw_obstacles()

        self.draw_map()

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

            # Displays the timers.
            self.draw_timer()
            self.draw_collision_time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse click events
                    if pygame.mouse.get_pos()[0] <= self.screen_size[0]:
                        self.agent.move_to(event.pos)  # Move the agent to the clicked position

            # if the simulation is not over, the agent can move
            if not self.agent.goal_found:
                self.agent.move()  # updates the state of the agent

            else:
                self.agent.vel = 0

            # Limit the frame rate (frames per second)
            clock.tick(self.fps)

            # Update the display
            pygame.display.flip()

        pygame.quit()