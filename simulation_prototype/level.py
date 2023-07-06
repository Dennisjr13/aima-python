import json
import os


"""Stores information about the obstacles in the environment."""


class JSONParser:
    def __init__(self, filename):
        if filename[-5:] == ".json":
            filename = filename[:-5]
        file_dir = os.getcwd() + f'\\levels\\{filename}.json'
        with open(file_dir, 'r') as file:
            data = json.load(file)
            self.screen_size = tuple(data['screen_size'])
            self.agent_start = tuple(data['agent_start'])
            self.goal = tuple(data['goal'])
            self.obstacles = data['obstacles']

            # Obstacles for the edge of the simulated space.
            edge_width = 5  # edge border width
            self.obstacles.append([-edge_width, 0, edge_width, self.screen_size[0]])
            self.obstacles.append([0, -edge_width, self.screen_size[1], edge_width])
            self.obstacles.append([self.screen_size[0], 0, edge_width, self.screen_size[1]])
            self.obstacles.append([0, self.screen_size[1], self.screen_size[0], edge_width])


def main():
    file_name = 'new_level'
    parser = JSONParser(file_name)
    print(parser.obstacles)


# for debugging purposes
if __name__ == '__main__':
    main()
