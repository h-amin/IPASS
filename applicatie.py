import pygame
import math

# Color definement
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)  # MAIN PLANT
RED = (255, 0, 0)  # FIRST ENCAPSULATION
YELLOW = (255, 255, 0)  # SECOND ENCAPSULATION (?)

# This sets the WIDTH and HEIGHT of each grid cube
WIDTH = 30  # 30 cm dus 0.3 m
LENGTH = 30  # 30 cm dus 0.3 m

# This sets the WIDTH and HEIGHT in meters
WIDTH_in_m = WIDTH / 100
LENGTH_in_m = LENGTH / 100

# This sets the margin between each cell
MARGIN = 5

# Create a 2 dimensional array.
grid = []

# Input function, so the user can input their own garden width and length.
garden_width = float(input("What is the WIDTH of your garden in meters? [number must be ≥ 1] "))
garden_length = float(input("What is the LENGTH of your garden in meters? [number must be ≥ 1] "))

# Equation to show how many cubes there reside in one row and one column.
cubes_in_row = garden_length / WIDTH_in_m
cubes_in_column = garden_width / LENGTH_in_m

# These variables indicate the amount of cubes that are within each row/column.
row_size = math.ceil(cubes_in_row)
column_size = math.ceil(cubes_in_column)

for row in range(row_size):
    # Add an empty array that will hold each cell in this row.
    grid.append([])
    for column in range(column_size):
        grid[row].append(0)  # Append a cell

# Initialize pygame
pygame.init()

cube_pixel_width = row_size * (WIDTH + MARGIN) + 5
cube_pixel_length = column_size * (WIDTH + MARGIN) + 5

# Set the LENGTH and WIDTH of the screen
WINDOW_SIZE = [cube_pixel_length, cube_pixel_width]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Garden Grid")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            print(pos)
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (LENGTH + MARGIN)
            # Set that location to one
            grid[row][column] = 1
            print("Click ", pos, "Grid coordinates: ", row, column)

    # Set the screen background
    screen.fill(BLACK)

    # Draw the grid
    for row in range(row_size):
        for column in range(column_size):
            color = WHITE

            # Bottom row without diagonals
            if row == row_size - 1 and column not in (0, column_size - 1):
                left            = grid[row][column - 1]
                top_left        = grid[row - 1][column - 1]
                top             = grid[row - 1][column]
                top_right       = grid[row - 1][column + 1]
                right           = grid[row][column + 1]
                if grid[row][column] == 1:
                    color = GREEN
                elif left or top_left or top or top_right or right:
                    color = RED

            # Top row without diagonals
            elif row == 0 and column not in (0, column_size - 1):
                left            = grid[row][column - 1]
                right           = grid[row][column + 1]
                bottom_right    = grid[row + 1][column + 1]
                bottom          = grid[row + 1][column]
                bottom_left     = grid[row + 1][column - 1]
                if grid[row][column] == 1:
                    color = GREEN
                elif left or right or bottom_right or bottom or bottom_left:
                    color = RED

            # Right column without diagonals
            elif row not in (0, row_size - 1) and column == column_size - 1:
                left            = grid[row][column - 1]
                top_left        = grid[row - 1][column - 1]
                top             = grid[row - 1][column]
                bottom          = grid[row + 1][column]
                bottom_left     = grid[row + 1][column - 1]
                if grid[row][column] == 1:
                    color = GREEN
                elif left or top_left or top or bottom or bottom_left:
                    color = RED

            # Left column without diagonals
            elif row not in (0, row_size - 1) and column == 0:
                top             = grid[row - 1][column]  # -1, 0
                top_right       = grid[row - 1][column + 1]  # -1, +1
                right           = grid[row][column + 1]  # 0, +1
                bottom_right    = grid[row + 1][column + 1]  # +1, +1
                bottom          = grid[row + 1][column]  # +1, 0
                if grid[row][column] == 1:
                    color = GREEN
                elif top or top_right or right or bottom_right or bottom:
                    color = RED

            # Bottom right diagonals
            elif row == row_size - 1 and column == column_size - 1:
                left            = grid[row][column - 1]  # 0, -1
                top_left        = grid[row - 1][column - 1]  # -1, -1
                top             = grid[row - 1][column]  # -1, 0
                if grid[row][column] == 1:
                    color = GREEN
                elif left or top_left or top:
                    color = RED

            # Bottom left diagonals
            elif row == row_size - 1 and column == 0:
                top             = grid[row - 1][column]  # -1, 0
                top_right       = grid[row - 1][column + 1]  # -1, +1
                right           = grid[row][column + 1]  # 0, +1
                if grid[row][column] == 1:
                    color = GREEN
                elif top or top_right or right:
                    color = RED

            # Top left diagonals
            elif row == 0 and column == 0:
                right           = grid[row][column + 1]  # 0, +1
                bottom_right    = grid[row + 1][column + 1]  # +1, +1
                bottom          = grid[row + 1][column]  # +1, 0
                if grid[row][column] == 1:
                    color = GREEN
                elif right or bottom_right or bottom:
                    color = RED

            # Top right diagonals
            elif row == 0 and column == column_size - 1:
                left            = grid[row][column - 1]  # 0, -1
                bottom          = grid[row + 1][column]  # +1, 0
                bottom_left     = grid[row + 1][column - 1]  # +1, -1
                if grid[row][column] == 1:
                    color = GREEN
                elif left or bottom or bottom_left:
                    color = RED

            else:
                left            = grid[row][column - 1]  # 0, -1
                top_left        = grid[row - 1][column - 1]  # -1, -1
                top             = grid[row - 1][column]  # -1, 0
                top_right       = grid[row - 1][column + 1]  # -1, +1
                right           = grid[row][column + 1]  # 0, +1
                bottom_right    = grid[row + 1][column + 1]  # +1, +1
                bottom          = grid[row + 1][column]  # +1, 0
                bottom_left     = grid[row + 1][column - 1]  # +1, -1
                if grid[row][column] == 1:
                    color = GREEN
                elif left or top_left or top or top_right or right or bottom_right or bottom or bottom_left:
                    color = RED

            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + LENGTH) * row + MARGIN,
                              WIDTH,
                              LENGTH])

    # Limit frames to 60.
    clock.tick(60)

    pygame.display.flip()

pygame.quit()
