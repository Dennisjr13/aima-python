import pygame


class Map:
    def __init__(self, env, agent):
        # boilerplate
        self.env = env
        self.agent = agent

        self.screen_size = env.size
        self.screen = pygame.display.set_mode(self.screen_size)
        self.surface = pygame.Surface(self.screen_size)

        # configurable
        self.surface.fill((0, 0, 0))  # background color of the SLAM

    def draw_explored(self):
        # self.explored_surface.fill((0, 0, 0, 0))
        for point in self.agent.visible_points:
            pygame.draw.line(self.surface, (255, 255, 255), self.agent.rect.center, point)

    def draw_agent(self):
        pygame.draw.circle(self.surface, (0, 0, 255),
                           (int(self.agent.rect.centerx),
                            int(self.agent.rect.centery)),
                           self.agent.size)

    def draw_goal(self):
        if self.agent.goal_found:
            pygame.draw.circle(self.surface, (0, 255, 0), (int(self.env.goal[0]), int(self.env.goal[1])), 5)

    def draw_path(self):
        """Draws a visual of where the agent has been."""
        for i in range(1, len(self.agent.path)):
            pygame.draw.line(self.surface, (0, 255, 0), self.agent.path[i - 1], self.agent.path[i])

    def draw_obstacle_highlights(self):
        """Shows points that have been identified as part of an obstacle."""
        for point in self.agent.obstacle_points:
            pygame.draw.circle(self.surface, (255, 0, 0), point, 2)

    def draw(self):
        """Displays the updated SLAM for the user to see."""
        self.draw_explored()
        self.draw_agent()
        self.draw_goal()
        self.draw_path()
        self.draw_obstacle_highlights()
