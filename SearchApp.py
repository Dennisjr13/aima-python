#!/usr/bin/env python3

__author__ = "Kemari Evans, Stephen Jendritz, Alexander Gu, and Dennis Juhasz"
__copyright__ = "Copyright 2023, Worcester Polytechnic Institute"
__credits__ = ["Kemari Evans", "Stephen Jendritz", "Alexander Gu", "Dennis Juhasz"]

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dennis Juhasz"
__email__ = "drjuhasz@wpi.edu"
__status__ = "Production"

from search import RandomGraph
from ProblemSolvingAgent import ProblemSolvingAgent, CustomGraph


def main():
    finished = False
    while not finished:
        # modification RandomGraph instead of romania_map
        rg = CustomGraph()
        print("Node coordinates: ")
        print(rg.locations)
        print("Node links / weights: ")
        print(rg.graph_dict)
        print()

        # create the Agent object
        psa = ProblemSolvingAgent(rg.nodes()[0], rg.nodes()[99], rg)

        # call the solver for all algorithms
        psa.solver()

        # Prompt the user if they'd like to continue
        #finished = prompt_for_continue()
        finished = True

    print("Thank You for Using Our App")


def prompt_for_continue():
    """ Returns true if the user requests to stop """
    while True:
        continue_prompt = input("Would you like to find the best path between another two nodes? ")

        # check if answer is valid
        if continue_prompt in ("No", "no"):
            return True
        elif continue_prompt in ("Yes", "yes"):
            return False


if __name__ == "__main__":
    main()
