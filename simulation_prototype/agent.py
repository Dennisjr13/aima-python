import pygame
from simulation_map import Map


class Agent:
    def __init__(self, env, pos=(0, 0), size=5):
        # boilerplate
        self.env = env
        self.rect = pygame.Rect(*pos, size, size)
        self.surface = pygame.Surface(env.size)
        self.map = Map(env, self)
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)

        # needed for moveTo
        self.current_action = None
        self.action_queue = []

        # configurable settings for the agent
        self.max_speed = 10  # max speed to prevent the agent from going too fast
        self.acceleration_coefficient = 2
        self.friction = 0.5  # friction factor (between 0 and 1)

        self.view_distance = 75  # distance the agent can see
        self.view_resolution = 720  # number of rays to cast within field of view

        self.path_resolution = 10  # minimum distance between points on the recorded path

        self.pos = pos  # position of the agent
        self.size = size  # size of the agent body
        self.collision_distance = self.size * 2  # the agent's hit box
        self.stopping_distance = 20  # to ensure that the agent slows down and doesn't overshoot

        # knowledge base
        self.visible_points = []  # shows what the agent currently sees
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

    def get_field_of_view(self):
        """Computes what the agent can see."""
        if self.vel == 0:
            return  # no need to recalculate the field of view when the agent is stationary
        visible_points = []
        for i in range(self.view_resolution):
            # Angle of the ray
            angle = (360 * i / self.view_resolution)
            # Create a unit vector in the direction of the ray
            direction = pygame.Vector2(1, 0).rotate(-angle)
            # Scale the vector to the view distance
            ray = direction * self.view_distance
            # Position of the end of the ray
            end_pos = pygame.Vector2(self.rect.center) + ray
            # Check if the ray hits any obstacles
            closest_intersection_point = None
            closest_distance = float('inf')
            for obstacle in self.env.obstacles:
                # Calculate the intersection of the line with the obstacle
                intersection_points = obstacle.clipline(self.rect.center, end_pos)
                for point in intersection_points:
                    # Calculate the distance from the agent to the intersection point
                    distance = (pygame.Vector2(point) - pygame.Vector2(self.rect.center)).length()
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_intersection_point = point
            if closest_intersection_point is None:
                self.non_obstacle_points.append(end_pos)
            else:
                end_pos = pygame.Vector2(closest_intersection_point)
                self.obstacle_points.append(end_pos)
            # Store the end position of the ray
            visible_points.append(end_pos)
        # Store the points in the agent's field of view
        self.visible_points = visible_points

    def move(self):
        """Decides how the agent should move."""

        if self.current_action is None:
            if self.action_queue:
                self.current_action = self.action_queue.pop(0)
        else:
            # Calculate the direction vector to the target location
            direction = self.current_action - pygame.Vector2(self.rect.center)
            distance = direction.length()
            # Normalize the direction vector and scale it to the desired force
            force = direction
            if distance != 0:  # vectors of length can't be normalized
                force = force.normalize() * self.acceleration_coefficient
            self.apply_force(force)
            # If the agent is close to the target location, stop moving
            if distance < self.stopping_distance:
                self.current_action = None

        self.vel += self.acc
        if self.vel.length() > self.max_speed:  # if velocity exceeds max_speed
            self.vel.scale_to_length(self.max_speed)  # limit it
        new_rect = self.rect.move(self.vel.x, self.vel.y)
        if self.valid_pos(new_rect):
            self.rect = new_rect
        else:
            self.vel = pygame.Vector2(0, 0)  # Stop if we bump into something
        if self.vel.length() > 0:  # Only apply friction if the agent is moving
            direction = self.vel.normalize()  # Get the direction of movement
            self.vel -= direction * self.friction  # Apply friction in the direction of movement
            if self.current_action is None:
                self.vel *= self.friction
                # agent slows down more when destination is within stopping distance
        self.acc *= 0

        if self.near_obstacle():
            self.total_collision_time += 1

        # if (distance from last point in self.path is greater than threshold, add new point to path)
        path_vector = pygame.Vector2(self.rect.center) - pygame.Vector2(self.path[-1])
        if path_vector.length() > self.path_resolution:
            self.path.append(self.rect.center)

    def apply_force(self, force):
        """Helper method, accelerates the agent."""
        self.acc += force

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
            if agent_pos.distance_to(closest_point_on_obstacle) \
                    <= self.collision_distance:
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
