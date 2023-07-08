import pygame
import json
import random


"""
The app allows you to design a level with just mouse clicks.
Exit the app when you're done assigning coordinates, then give a file name.
Information about the level will be exported as a JSON file.

Left Click and Drag -> create a new Rectangle obstacle

Right Click -> cycles between assigning the agent's starting position and the goal's position

[R] -> remove the most recently added obstacle

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
        self.screen_size = screen_size
        self.obstacles = []
        self.current_obstacle = None
        self.dragging = False
        self.agent_start = None
        self.goal = None
        self.agent_assigned = False

    def obstacle_correction(self):
        # direction correction
        point1 = self.current_obstacle[0]
        point2 = self.current_obstacle[1]
        p1x, p1y = point1[0], point1[1]
        p2x, p2y = point2[0], point2[1]
        if p2x > p1x and p2y > p1y:
            return self.current_obstacle
        elif p1x > p2x and p1y > p2y:
            return [point2, point1]
        elif p1x > p2x:
            return [(p2x, p1y), (p1x, p2y)]
        else:
            return [(p1x, p2y), (p2x, p1y)]

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        # Start dragging for a new rectangle
                        self.current_obstacle = [event.pos, event.pos]
                        self.dragging = True
                    elif event.button == 3:  # Right mouse button
                        if not self.agent_assigned:
                            self.agent_start = event.pos
                            self.agent_assigned = True
                        else:
                            self.goal = event.pos
                            self.agent_assigned = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left mouse button
                        # End dragging for the current rectangle
                        self.dragging = False
                        if self.current_obstacle is not None:
                            self.obstacles.append(self.obstacle_correction())
                        self.current_obstacle = None
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging:
                        # Update the second point of the rectangle
                        self.current_obstacle[1] = event.pos
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if self.obstacles:
                            self.obstacles.pop()

            self.screen.fill((255, 255, 255))

            # Draw the agent start, goal, and obstacles
            if self.agent_start is not None:
                pygame.draw.circle(self.screen, (0, 0, 255), self.agent_start, 5)
            if self.goal is not None:
                pygame.draw.circle(self.screen, (0, 255, 0), self.goal, 5)
            for obstacle in self.obstacles:
                pygame.draw.rect(self.screen, (0, 0, 0),
                                 pygame.Rect(*obstacle[0],
                                             *(obstacle[1][0] - obstacle[0][0], obstacle[1][1] - obstacle[0][1])))
            if self.current_obstacle is not None:
                ob = self.obstacle_correction()
                pygame.draw.rect(self.screen, (0, 0, 0),
                                 pygame.Rect(*ob[0], *(ob[1][0] - ob[0][0], ob[1][1] - ob[0][1])))

            pygame.display.flip()

        pygame.quit()


def write_file(obstacle_creator):
    # Save the agent start, goal, and obstacles to a text file when the user closes the window

    name_of_file = input("Name of file: ") + '.json'
    if name_of_file == "":
        random_number = random.randint(0, 999)
        name_of_file = f"Level {random_number:03d}"

    rectangle_coordinates = []

    for rectangle in obstacle_creator.obstacles:
        width = rectangle[1][0] - rectangle[0][0]
        height = rectangle[1][1] - rectangle[0][1]
        if width != 0 and height != 0:
            ls = [*rectangle[0], width, height]
            rectangle_coordinates.append(ls)

    with open(name_of_file, 'w') as file:
        json.dump({
            'screen_size': obstacle_creator.screen_size,
            'agent_start': obstacle_creator.agent_start,
            'goal': obstacle_creator.goal,
            'obstacles': rectangle_coordinates
        }, file)


def main():
    creator = ObstacleCreator()
    creator.run()
    write_file(creator)


if __name__ == '__main__':
    main()
