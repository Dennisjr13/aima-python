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
    file_name = "test_1.json"

    parser = JSONParser(file_name, "e")
    # if you want to access levels from "evaluation_levels",
    # add a second parameter "e" to the JSONParser call above

    obstacles = list(map(lambda x: pygame.Rect(*x), parser.obstacles))

    goal = parser.goal  # Coordinates of the goal (what the agent is looking for).
    env = Environment(parser.screen_size, obstacles, goal)
    agent = Agent(env, parser.agent_start)  # Starting at the center of the screen
    sim = Simulation(env, agent, file_name[:-5])

    sim.run()


if __name__ == '__main__':
    main()
