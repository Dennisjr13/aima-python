import pygame
from agent import Agent
from environment import Environment
from simulation import Simulation
from level import JSONParser


"""
Continuous, dynamic environment. Field of view added and improved physics.
Timer functionality added. SLAM added.
"""


def main():
    parser = JSONParser("new_level")

    obstacles = list(map(lambda x: pygame.Rect(*x), parser.obstacles))

    goal = parser.goal  # Coordinates of the goal (what the agent is looking for).
    env = Environment(parser.screen_size, obstacles, goal)
    agent = Agent(env, parser.agent_start)  # Starting at the center of the screen
    sim = Simulation(env, agent, parser.screen_size)

    sim.run()


if __name__ == '__main__':
    main()
