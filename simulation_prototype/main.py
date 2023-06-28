from agent import Agent
from environment import Environment
from simulation import Simulation
from obstacles import list_of_obstacles


"""
Continuous, dynamic environment. Field of view added and improved physics.
Timer functionality added. SLAM added.
"""


def main():
    obstacles = list_of_obstacles
    goal = (400, 400)  # Coordinates of the goal (what the agent is looking for).
    env = Environment((500, 500), obstacles, goal)
    agent = Agent(env, (250, 250))  # Starting at the center of the screen
    sim = Simulation(env, agent)

    sim.run()


if __name__ == '__main__':
    main()
