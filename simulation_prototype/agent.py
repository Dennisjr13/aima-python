import pygame
from simulation_map import Map
from math import dist


class Agent:
    def __init__(self, env, pos=(0, 0), size=5):
        # boilerplate
        self.env = env
        self.rect = pygame.Rect(*pos, size, size)
        self.surface = pygame.Surface(env.size)
        self.map = Map(env, self)
        self.vel = pygame.Vector2(0, 0)

        # needed for moveTo
        self.current_action = None
        self.action_queue = []

        # configurable settings for the agent
        self.max_speed = 10

        self.view_distance = 75  # distance the agent can see
        self.view_resolution = 720  # number of rays to cast within field of view

        self.path_resolution = 2  # minimum distance between points on the recorded path
        self.path_cost_so_far = 0  # keeps track of the current path cost

        self.pos = pos  # position of the agent
        self.size = size  # size of the agent body
        self.collision_distance = self.size * 2  # the agent's hit box
        self.stopping_distance = self.size * 2  # to ensure that the agent slows down and doesn't overshoot

        # debugging
        self.closest_obs_point = None

        # knowledge base
        self.path = [pos]  # keeps track of where the agent has been
        self.obstacle_points = []  # keeps track of the edges of obstacles encountered
        self.non_obstacle_points = []  # any points in visible_points that are not in obstacle_points
        self.total_collision_time = 0
        self.goal_found = False

    def queue_action(self, new_action):
        """Tells the agent that it should move
        towards the given coordinates.

        Note: it's on the agent to not queue an action
        for a coordinate in an obstacle."""
        self.action_queue.append(pygame.Vector2(new_action))  # Set the target position

    def move(self):
        """Decides how the agent should move."""

        if self.current_action is None:
            if self.action_queue:
                self.current_action = self.action_queue.pop(0)
                direction = self.current_action - pygame.Vector2(self.rect.center)
                if direction.length() != 0:
                    direction = direction.normalize()
                    self.vel = direction * self.max_speed
        else:
            # Calculate the direction vector to the target location
            direction = self.current_action - pygame.Vector2(self.rect.center)
            distance = direction.length()
            # If the agent is close to the target location, stop moving
            if distance < self.stopping_distance:
                self.current_action = None
                self.vel = pygame.Vector2(0, 0)

        new_rect = self.rect.move(self.vel.x, self.vel.y)
        if self.valid_pos(new_rect):
            self.rect = new_rect
        else:
            self.vel = pygame.Vector2(0, 0)  # Stop if we bump into something

        self.pos = self.rect.center

        if self.near_obstacle():
            self.total_collision_time += 1

        # if (distance from last point in self.path is greater than threshold, add new point to path)
        path_vector = pygame.Vector2(self.rect.center) - pygame.Vector2(self.path[-1])
        if path_vector.length() > self.path_resolution:
            self.path_cost_so_far += dist(self.rect.center, self.path[-1])
            self.path.append(self.rect.center)

    def near_obstacle(self):
        """Returns true if the agent is colliding with an obstacle; i.e.,
        if an obstacle is touching the agent's hit box (indicated by the red circle).
        False otherwise."""
        if self.goal_found:
            return

        # Check if any obstacle is within the given distance from the agent
        agent_pos = pygame.Vector2(self.rect.center)
        for obstacle in self.env.obstacles:
            closest_point_on_obstacle = pygame.Vector2(
                min(max(agent_pos.x, obstacle.left), obstacle.right),
                min(max(agent_pos.y, obstacle.top), obstacle.bottom)
            )
            distance = agent_pos.distance_to(closest_point_on_obstacle)
            if distance <= self.collision_distance:
                self.closest_obs_point = closest_point_on_obstacle
                return True
        return False

    def valid_pos(self, new_rect):
        """Returns false if moving the agent would make it phase into
        an obstacle or past the edge of the available area.
        Returns true otherwise (if the agent can continue moving in
        the direction it's heading towards)."""
        # Check boundaries
        if new_rect.left < 0 or new_rect.top < 0 or \
                new_rect.right > self.env.size[0] or new_rect.bottom > self.env.size[1]:
            return False

        # Check obstacles
        for obstacle in self.env.obstacles:
            if new_rect.colliderect(obstacle):
                return False

        return True
