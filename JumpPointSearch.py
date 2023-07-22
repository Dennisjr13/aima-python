import pygame
import time
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("JPS Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def __str__(self):
        return f"Node([r, c]: [{self.row}, {self.col}], color: {self.color})"

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.y, self.x, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    col = y // gap
    row = x // gap

    return row, col



def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    path_cost = 0
    while current in came_from:
        # print(f"Current: {current}, Came From: {came_from[current]}")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        if current != start:
            current.make_closed()

    return False


def get_end_direction(start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]

    direction = []
    if dy > 0:
        direction.append("right")
    elif dy < 0:
        direction.append("left")
    if dx > 0:
        direction.append("down")
    elif dx < 0:
        direction.append("up")

    direction = '-'.join(direction)

    if direction == "right-down":
        directions = ((1, 1), (0, 1), (1, 0), (0, -1), (-1, 0))
        return directions
    elif direction == "right-up":
        directions = ((-1, 1), (0, 1), (1, 0), (0, -1), (-1, 0))
        return directions
    elif direction == "left-up":
        directions = ((-1, -1), (0, 1), (1, 0), (0, -1), (-1, 0))
        return directions
    elif direction == "left-down":
        directions = ((1, -1), (0, 1), (1, 0), (0, -1), (-1, 0))
        return directions
    elif direction == "right":
        directions = ((0,1),(1,0),(-1,0), (-1, 1),(1,1))
        return directions
    elif direction == "left":
        directions = ((0,-1),(1,0),(-1,0), (1,-1),(-1,-1))
        return directions
    elif direction == "up":
        directions = ((-1,0),(0,-1),(0,1), (-1,-1),(-1,1))
        return directions
    elif direction == "down":
        directions = ((1,0),(0,-1),(0,1),(1,-1),(1,1))
        return directions


def is_jump_point(grid, node, prev):
    x, y = node.get_pos()
    dx, dy = (x - prev.get_pos()[0], y - prev.get_pos()[1])
    # Forced neighbors
    if dx == 0:  # vertical movement
        # Horizontal forced neighbors
        if 0 <= y + 1 < len(grid) and 0 <= x + 1 < len(grid) and not grid[x][y + 1].is_barrier() and grid[x + 1][y].is_barrier():
            return True
        if 0 <= y - 1 < len(grid) and 0 <= x + 1 < len(grid) and not grid[x][y - 1].is_barrier() and grid[x + 1][y].is_barrier():
            return True
    elif dy == 0:  # horizontal movement
        # Vertical forced neighbors
        if 0 <= x + 1 < len(grid) and 0 <= y + 1 < len(grid) and not grid[x + 1][y].is_barrier() and grid[x][y + 1].is_barrier():
            return True
        if 0 <= x - 1 < len(grid) and 0 <= y + 1 < len(grid) and not grid[x - 1][y].is_barrier() and grid[x][y + 1].is_barrier():
            return True
    else:  # diagonal movement
        # Horizontal and vertical forced neighbors
        if (0 <= x - dx < len(grid) and not grid[x - dx][y].is_barrier()) or (0 <= y - dy < len(grid) and not grid[x][y - dy].is_barrier()):
            return True
    # Recursive check for jump points in direction of natural neighbors
    if dx != 0 and (is_jump_point(grid, grid[x + dx][y], node) or is_jump_point(grid, grid[x][y + dy], node)):
        return True
    if dy != 0 and (is_jump_point(grid, grid[x + dx][y], node) or is_jump_point(grid, grid[x][y + dy], node)):
        return True
    return False



def Jump_Point_Search(canvas, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    jump_point = start
    jump_points = {}
    directions = get_end_direction(start.get_pos(), end.get_pos())

    if directions == None:
        raise ValueError("Direction not found")

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            pathcost = 0
            reconstruct_path(came_from, end, canvas)
            end.make_end()
            return True

        for direction in directions:
            temp = current
            moving = True
            while moving:
                x, y = temp.get_pos()
                dx, dy = direction
                if 0 <= x + dx < len(grid) and 0 <= y + dy < len(grid):
                    next_node = grid[x + dx][y + dy]
                    if next_node.is_barrier():
                        break
                    elif next_node == end:
                        came_from[next_node] = temp
                        pathcost = 0
                        end.make_end()
                        reconstruct_path(came_from, end, canvas)
                        return True

                    elif next_node not in open_set_hash:
                        count += 1
                        open_set.put((f_score[temp], count, next_node))
                        open_set_hash.add(next_node)
                        next_node.make_open()
                        g_score[next_node] = g_score[temp] + 1
                        f_score[next_node] = g_score[next_node] + h(next_node.get_pos(), end.get_pos())
                        came_from[next_node] = temp
                else:
                    moving = False
                temp = next_node

    return False




def main(win, width):
    pygame.init()
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None
    path_cost = 0
    run = True
    started = False
    success = False
    draw(win, grid, ROWS, width)
    while run:
        #win.fill(WHITE)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Path Cost: {path_cost}", 1, (10, 10, 10))
        text_rect = text.get_rect(topleft=(10, 10))
        win.blit(text, (10, 10))

        pygame.display.flip()

        if success == True:
            font = pygame.font.Font(None, 36)
            text = font.render("Target Found", 1, (255, 0, 0))
            win.blit(text, (width // 2, 10))
            pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                print(row)
                print(col)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()


                elif node != end and node != start:
                    node.make_barrier()

                draw(win, grid, ROWS, width)

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
                draw(win, grid, ROWS, width)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    #success=algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    success=Jump_Point_Search(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    success = False
                draw(win, grid, ROWS, width)

    pygame.quit()


main(WIN, WIDTH)
