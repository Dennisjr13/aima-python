class Environment:
    def __init__(self, size, obstacles, goal):
        """Can ignore, just boilerplate."""
        self.size = size  # (width, height) of simulation
        self.obstacles = obstacles  # List of pygame.Rect
        self.goal = goal  # Tuple
