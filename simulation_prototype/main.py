import pygame
from agent import Agent
from environment import Environment
from simulation import Simulation


"""
Continuous, dynamic environment. Field of view added and improved physics.
Timer functionality added. SLAM added.
"""


def main():
    obstacles = [pygame.Rect(50, 50, 100, 100), pygame.Rect(350, 50, 50, 50)]  # List of pygame.Rect
    goal = (400, 400)  # Tuple
    env = Environment((500, 500), obstacles, goal)
    agent = Agent(env, (250, 250))  # Starting at the center of the screen
    sim = Simulation(env, agent)

    sim.run()


if __name__ == '__main__':
    main()
