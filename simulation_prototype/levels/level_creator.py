import pygame
import json
import random


"""
The app allows you to design a level with just mouse clicks.
Exit the app when you're done assigning coordinates, then give a file name.
Information about the level will be exported as a JSON file.

Middle Mouse Button - first vertex of a new obstacle
Left Click - adds a new vertex to the current obstacle
First Right Click - assigns the agent's starting position
Second Right Click - assigns the goal's position

The size of screen can be adjusted in the code before you run
the level creator app (the screen size will automatically be
saved in the JSON file).
"""


# Configurable
size_of_screen = (500, 500)


class ObstacleCreator:
    def __init__(self, screen_size=(500, 500)):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.obstacles = []
        self.current_obstacle = []
        self.agent_start = None
        self.goal = None

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        # Add a point to the current obstacle
                        if self.current_obstacle:
                            self.current_obstacle.append(event.pos)
                    elif event.button == 2:  # Middle mouse button
                        # Start a new obstacle
                        if self.current_obstacle:
                            self.obstacles.append(self.current_obstacle)
                        self.current_obstacle = [event.pos]
                    elif event.button == 3:  # Right mouse button
                        if self.agent_start is None:
                            self.agent_start = event.pos
                        elif self.goal is None:
                            self.goal = event.pos
            self.screen.fill((255, 255, 255))
            # Draw the agent start, goal, and obstacles
            if self.agent_start is not None:
                pygame.draw.circle(self.screen, (0, 0, 255), self.agent_start, 5)
            if self.goal is not None:
                pygame.draw.circle(self.screen, (0, 255, 0), self.goal, 5)
            for obstacle in self.obstacles:
                if len(obstacle) > 2:
                    pygame.draw.polygon(self.screen, (0, 0, 0), obstacle)
            if len(self.current_obstacle) > 2:
                pygame.draw.polygon(self.screen, (0, 0, 0), self.current_obstacle)
            pygame.display.flip()
        # Add the current obstacle to the list of obstacles if it's not empty
        if self.current_obstacle:
            self.obstacles.append(self.current_obstacle)
        pygame.quit()


def write_file(obstacle_creator):
    # Save the agent start, goal, and obstacles to a text file when the user closes the window

    name_of_file = input("Name of file: ")
    if name_of_file == "":
        random_number = random.randint(0, 999)
        name_of_file = f"Level {random_number:03d}"


    with open(name_of_file, 'w') as file:
        json.dump({
            'screen_size': obstacle_creator.screen_size,
            'agent_start': obstacle_creator.agent_start,
            'goal': obstacle_creator.goal,
            'obstacles': obstacle_creator.obstacles
        }, file)


def main():
    creator = ObstacleCreator()
    creator.run()
    write_file(creator)


if __name__ == '__main__':
    main()
