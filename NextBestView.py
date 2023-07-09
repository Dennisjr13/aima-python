import random
import time

import pygame

#################
#################### Stopped working this because of new approach/methodology
##################################################################################

# Pygame constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
GRID_SIZE = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class NextBestViewEnvironment():
    def __init__(self):
        pass

    def unseen_environment(self, position):
        pass


class FOV():
    def __init__(self):
        pass

    def pos(self):
        pass

    def move(self):
        pass


def draw_grid(screen):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def draw_target(screen, x, y):
    pygame.draw.rect(screen, RED, (x, y, CELL_SIZE, CELL_SIZE))


def move(screen, x_pos, y_pos):
    pygame.draw.rect(screen, GREEN, (x_pos * CELL_SIZE, y_pos * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def get_next_move(lst,current_x,current_y):
    nextmove = []
    explored = True
    while explored:
        move_index = random.randint(1,4)
        if move_index == 1:
            next_x = current_x + 1
            next_y = current_y
            if [next_x,next_y] not in lst:
                nextmove.append([next_x, next_y])
                #explored = True
                return nextmove
        elif move_index == 2:
            next_x = current_x
            next_y = current_y+1
            if [next_x, next_y] not in lst:
                nextmove.append([next_x, next_y])
                return nextmove
        elif move_index == 3:
            next_x = current_x-1
            next_y = current_y
            if [next_x, next_y] not in lst:
                nextmove.append([next_x, next_y])
                return nextmove
        elif move_index == 4:
            next_x = current_x
            next_y = current_y-1
            if [next_x, next_y] not in lst:
                nextmove.append([next_x, next_y])
                return nextmove
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    moves_x = [1, 2, 3, 4, 5]
    moves_y = [1, 2, 3, 4, 5]
    starting_x = 3
    starting_y = 3
    running = True
    target_x = random.randint(1, 30) * CELL_SIZE
    target_y = random.randint(1, 30) * CELL_SIZE
    screen.fill(WHITE)
    draw_grid(screen)
    print(target_y)
    draw_target(screen, target_x, target_y)
    pygame.display.update()
    seen = [[starting_x,starting_y]]
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos[0], pos[1])
        next_move = get_next_move(seen,starting_x,starting_y)
        move(screen, next_move[0][0], next_move[0][1])
        seen.append([next_move[0][0], next_move[0][1]])
        pygame.display.update()
        starting_x = next_move[0][0]
        starting_y = next_move[0][1]
        time.sleep(1)
    pygame.quit()


if __name__ == "__main__":
    main()
