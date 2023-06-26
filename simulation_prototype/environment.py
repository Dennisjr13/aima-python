class Environment:
    def __init__(self, size, obstacles, goal):
        self.size = size
        self.obstacles = obstacles  # List of pygame.Rect
        self.goal = goal  # Tuple
