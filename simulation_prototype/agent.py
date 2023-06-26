import pygame
from simulation_map import Map


class Agent:
    def __init__(self, env, pos=(0, 0), size=5):
        self.env = env
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(*pos, size, size)

        self.goal_found = False

        self.target_location = None
        self.total_collision_time = 0
        self.collision_distance = self.size*2

        self.vel = pygame.Vector2(0, 0)  # initialize velocity
        self.acc = pygame.Vector2(0, 0)  # initialize acceleration
        self.max_speed = 10  # max speed to prevent the agent from going too fast
        self.acceleration_coefficient = 0.1
        self.friction = 0.5  # Friction factor

        self.view_distance = 75  # Distance the agent can see
        self.view_resolution = 720  # Number of rays to cast within field of view
        self.visible_points = []

        self.surface = pygame.Surface(env.size)
        self.path = [pos]
        self.obstacle_points = []
        self.map = Map(env, self, env.size)

    def apply_force(self, force):
        self.acc += force

    def move(self):
        if self.target_location is not None:
            # Calculate the direction vector to the target location
            direction = self.target_location - pygame.Vector2(self.rect.center)
            distance = direction.length()
            # Normalize the direction vector and scale it to the desired force
            force = direction
            if direction.length() != 0:
                # normalize can't be given vectors of length 0
                force = force.normalize()
            force = direction * distance * self.acceleration_coefficient
            self.apply_force(force)
            # If the agent is close to the target location, stop moving
            if direction.length() < 50 and self.vel.length() == 0:
                self.target_location = None

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
        self.acc *= 0

        if self.near_obstacle():  # safe distance around agent
            self.total_collision_time += 1

        self.path.append(self.rect.center)

    def move_to(self, target_location):
        self.target_location = pygame.Vector2(target_location)  # Set the target position

    def near_obstacle(self):

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
        # Check boundaries
        if new_rect.left < 0 or new_rect.top < 0 or \
                new_rect.right > self.env.size[0] or new_rect.bottom > self.env.size[1]:
            return False

        # Check obstacles
        for obstacle in self.env.obstacles:
            if new_rect.colliderect(obstacle):
                return False

        return True

    def get_field_of_view(self):
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
            if closest_intersection_point is not None:
                end_pos = pygame.Vector2(closest_intersection_point)
                self.obstacle_points.append(end_pos)
            # Store the end position of the ray
            visible_points.append(end_pos)
        # Store the points in the agent's field of view
        self.visible_points = visible_points
