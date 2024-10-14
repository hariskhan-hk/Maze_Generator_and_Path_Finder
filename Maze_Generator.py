import random
import time
import pygame
import heapq

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY = (46, 49, 49, 1)

# Pygame initialization
pygame.init()
pygame.mixer.init()

# A* pathfinding heuristic
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* pathfinding algorithm
def astar(start, end, grid):
    heap = [(0, start)]
    visited = set()
    g_values = {start: 0}
    path = {}

    while heap:
        (cost, current) = heapq.heappop(heap)

        if current == end:
            break

        if current in visited:
            continue

        visited.add(current)

        for neighbor in get_neighbors(current, grid):
            new_cost = g_values[current] + 1
            if neighbor not in g_values or new_cost < g_values[neighbor]:
                g_values[neighbor] = new_cost
                heapq.heappush(heap, (new_cost + heuristic(end, neighbor), neighbor))
                path[neighbor] = current

    return path

# Function to get neighboring cells
def get_neighbors(cell, grid):
    x, y = cell
    neighbors = [(x + cell_width, y), (x - cell_width, y), (x, y + cell_width), (x, y - cell_width)]
    return [neighbor for neighbor in neighbors if neighbor in grid]

# Function to visualize the path
def visualize_path(path):
    for cell in path:
        path_tracker(cell[0], cell[1])
        time.sleep(0.01)

# Function to get user input for maze dimensions
def get_user_input():
    width = int(input("Enter the width of the maze: "))
    height = int(input("Enter the height of the maze: "))
    return width, height

# Default dimensions
width, height = 1680, 1050

# Pygame window setup
pygame.display.set_caption("Maze generator")
win = pygame.display.set_mode((width, height))
win.fill(WHITE)
pygame.display.update()

fps = 30
clock = pygame.time.Clock()

# Maze cell dimensions
cell_width = 40

# Maze generation variables
grid = [] 
stack_list = []
closed_list = []

# Pathfinding variable
path = {}

# Pause for 2 seconds before maze generation
time.sleep(2)

# Function to build the maze grid
def build_grid(width, height, cell_width=cell_width):
    for n in range(height):
        x = cell_width
        y = n * cell_width
        for m in range(width):
            pygame.draw.line(win, BLACK, [x + cell_width, y], [x + cell_width, y + cell_width], 2)
            pygame.draw.line(win, BLACK, [x, y], [x, y + cell_width], 2)
            pygame.draw.line(win, BLACK, [x, y], [x + cell_width, y], 2)
            pygame.draw.line(win, BLACK, [x, y + cell_width], [x + cell_width, y + cell_width], 2)

            grid.append((x, y))
            x += cell_width

    pygame.display.update()

def knockdown_east_wall(x, y):
    pygame.draw.rect(win, YELLOW, (x + 1, y + 1, 79, 39), 0)
    pygame.display.update()

def knockdown_west_wall(x, y):
    pygame.draw.rect(win, YELLOW, (x - cell_width + 1, y + 1, 79, 39), 0)
    pygame.display.update()

def knockdown_north_wall(x, y):
    pygame.draw.rect(win, YELLOW, (x + 1, y - cell_width + 1, 39, 79), 0)
    pygame.display.update()

def knockdown_south_wall(x, y):
    pygame.draw.rect(win, YELLOW, (x + 1, y + 1, 39, 79), 0)
    pygame.display.update()

def single_cell(x, y):
    pygame.draw.rect(win, BLUE, (x + 1, y + 1, 38, 38), 0)
    pygame.display.update()

def backtracking_cell(x, y):
    pygame.draw.rect(win, YELLOW, (x + 1, y + 1, 38, 38), 0)
    pygame.display.update()

def path_tracker(x, y):
    pygame.draw.rect(win, GREEN, (x + 8, y + 8, 10, 10), 0)
    pygame.display.update()

def maze(x, y, end_x, end_y):
    single_cell(x, y)
    stack_list.append((x, y))
    closed_list.append((x, y))

    while len(stack_list) > 0:
        cell = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        neighbors = [(x + cell_width, y), (x - cell_width, y), (x, y + cell_width), (x, y - cell_width)]
        random.shuffle(neighbors)  # Randomize the order of neighbors

        for nx, ny in neighbors:
            if (nx, ny) not in closed_list and (nx, ny) in grid:
                cell.append((nx, ny))

        if len(cell) > 0:
            current_cell = random.choice(cell)
            nx, ny = current_cell

            if nx > x:
                knockdown_east_wall(x, y)
            elif nx < x:
                knockdown_west_wall(x, y)
            elif ny > y:
                knockdown_south_wall(x, y)
            elif ny < y:
                knockdown_north_wall(x, y)

            path[(nx, ny)] = x, y
            x, y = nx, ny
            closed_list.append((x, y))
            stack_list.append((x, y))
            single_cell(x, y)

        else:
            x, y = stack_list.pop()
            backtracking_cell(x, y)

        pygame.display.update()

if __name__ == "__main__":
    
    width, height = get_user_input()
    build_grid(width, height, cell_width)
    start_x, start_y = 40, 40
    end_x, end_y = width * cell_width - cell_width, height * cell_width - cell_width
    maze(start_x, start_y, end_x, end_y)

    # Mark the start and end points after maze generation
    pygame.draw.rect(win, RED, (start_x + 1, start_y + 1, 38, 38), 0)
    pygame.draw.rect(win, GREEN, (end_x + 1, end_y + 1, 38, 38), 0)
    pygame.display.update()

    # Trace the path from the start to the end
    x, y = end_x, end_y
    while (x, y) != (start_x, start_y):
        x, y = path[x, y]
        path_tracker(x, y)
        time.sleep(0.01)  # Reduced sleep time

    # Mark the start point in the maze
    pygame.draw.rect(win, GREEN, (start_x + 1, start_y + 1, 38, 38), 0)
    pygame.display.update()

    run = True
    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False