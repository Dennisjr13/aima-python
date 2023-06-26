#!/usr/bin/env python3

__author__ = "Dennis Juhasz"
__copyright__ = "Copyright 2023, Worcester Polytechnic Institute"
__credits__ = ["Dennis Juhasz"]

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dennis Juhasz"
__email__ = "drjuhasz@wpi.edu"
__status__ = "Development"

import sys
import random
import numpy as np

from search import GraphProblem, Node, exp_schedule, greedy_best_first_graph_search, astar_search
from utils import argmin_random_tie, probability


class LocalGraphProblem(GraphProblem):
    distances = {}

    def __init__(self, initial, goal, graph):
        """ Inherit all functions from GraphProblem (which itself inherits Problem) """
        super().__init__(initial, goal, graph)
        self.calc_euclidean_distance()

    def value(self, state):
        """ Overrides Problem's value() function.
        Used for Hill Climb and Simulated Annealing Search
        Value of a state is the Euclidean distance between the state and the goal """
        return self.distances[state][self.goal]

    def calc_euclidean_distance(self):
        # copied / modified from aima-python/gui/tsp.py::main()
        all_cities = []
        for city in self.graph.locations.keys():
            self.distances[city] = {}
            all_cities.append(city)
        all_cities.sort()

        # distances['city1']['city2'] contains Euclidean distance between their coordinates
        for name_1, coordinates_1 in self.graph.locations.items():
            for name_2, coordinates_2 in self.graph.locations.items():
                self.distances[name_1][name_2] = np.linalg.norm(
                    [coordinates_1[0] - coordinates_2[0], coordinates_1[1] - coordinates_2[1]])
                self.distances[name_2][name_1] = np.linalg.norm(
                    [coordinates_1[0] - coordinates_2[0], coordinates_1[1] - coordinates_2[1]])


class SimpleProblemSolvingAgent:
    problem = {}

    def __init__(self, initial, goal, graph):
        self.problem = LocalGraphProblem(initial, goal, graph)

    def hill_climbing_search(self):
        """
        From the initial node, keep choosing the neighbor with the lowest value,
        stopping when no neighbor is better. We've then either arrived at the goal state
         (ie found the "peak"), or failed to find the solution (ie found a "ridge").

        This returns all the states encountered in reaching the goal state.
        """
        current = Node(self.problem.initial)
        while True:
            neighbors = current.expand(self.problem)
            if not neighbors:
                break
            neighbor = argmin_random_tie(neighbors, key=lambda node: self.problem.value(node.state))
            if self.problem.value(neighbor.state) > self.problem.value(current.state):
                break

            current = neighbor
            if self.problem.goal_test(current.state):
                return current

    def simulated_annealing_search(self, schedule=exp_schedule()):
        """
        Instead of picking the best move (like hill_climbing_search), pick a random
        move. If the move improves the situation, it is accepted.
        If it does not improve the situation, the algorithm accepts the move with some
        probability less than 1.

        This returns all the states encountered in reaching the goal state.
        """
        states = []
        current = Node(self.problem.initial)
        for t in range(sys.maxsize):
            states.append(current.state)
            T = schedule(t)
            if T == 0:
                return current
            neighbors = current.expand(self.problem)
            if not neighbors:
                return current
            next_choice = random.choice(neighbors)
            delta_e = self.problem.value(current.state) - self.problem.value(next_choice.state)
            if delta_e > 0 or probability(np.exp(delta_e / T)):
                current = next_choice

            # The above implementation waits for T exhaustion, the below would instead test for the goal state
            # if problem.goal_test(current.state):
            #    return current

    def solver(self):
        """ Runs the solvers """

        # Greedy best-first search is best-first graph search with f(n) = h(n).
        result = greedy_best_first_graph_search(
            self.problem,
            self.problem.h)
        print("Greedy Best-First Search")
        display(self.problem.initial, result)

        # A* search is best-first graph search with f(n) = g(n)+h(n).
        result = astar_search(
            self.problem,
            self.problem.h)
        print("A* Search")
        display(self.problem.initial, result)

        # Hill climbing search
        result = self.hill_climbing_search()
        print("Hill Climbing Search")
        display(self.problem.initial, result)

        # Simulated annealing search
        result = self.simulated_annealing_search()
        print("Simulated Annealing Search")
        display(self.problem.initial, result)


def display(initial, result):
    """ Displays an algorithm result to console """
    print(initial + " → ", end='')
    print(*result.solution(), sep=" → ")
    print("Total Cost: %s" % result.path_cost)
    print()
