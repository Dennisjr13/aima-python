import json
import os


"""Stores information about the obstacles in the environment."""


class JSONParser:
    def __init__(self, filename):
        file_dir = os.getcwd() + f'\\levels\\{filename}.json'
        with open(file_dir, 'r') as file:
            data = json.load(file)
            self.screen_size = tuple(data['screen_size'])
            self.agent_start = tuple(data['agent_start'])
            self.goal = tuple(data['goal'])
            self.obstacles = [list(map(tuple, obstacle)) for obstacle in data['obstacles']]


def main():
    file_name = 'default'
    parser = JSONParser(file_name)
    print(parser.screen_size)


if __name__ == '__main__':
    main()
