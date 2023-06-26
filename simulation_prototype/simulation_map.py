import pygame


class Map:
    def __init__(self, env, agent, screen_size=(500, 500)):
        pygame.init()
        self.env = env
        self.agent = agent
        self.screen = pygame.display.set_mode(screen_size)
        self.surface = pygame.Surface(screen_size)
        self.surface.fill((0, 0, 0))

    def update(self):
        for point in self.agent.visible_points:
            pygame.draw.line(self.surface, (255, 255, 255), self.agent.rect.center, point)

    def draw_agent(self):
        pygame.draw.circle(self.surface, (0, 0, 255),
                           (int(self.agent.rect.centerx),
                            int(self.agent.rect.centery)),
                           self.agent.size)

    def draw_target(self):
        if self.agent.goal_found:
            pygame.draw.circle(self.surface, (0, 255, 0), (int(self.env.goal[0]), int(self.env.goal[1])), 5)

    def draw_path(self):
        for i in range(1, len(self.agent.path)):
            pygame.draw.line(self.surface, (0, 255, 0), self.agent.path[i - 1], self.agent.path[i])

    def draw_obstacle_highlights(self):
        for point in self.agent.obstacle_points:
            pygame.draw.circle(self.surface, (255, 0, 0), point, 2)

    def draw(self):
        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()
