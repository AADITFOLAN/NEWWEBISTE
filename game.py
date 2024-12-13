import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Number Match Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.SysFont("Arial", 36)

# Global variables
TIMER_LIMIT = 120  # 2 minutes
GRID_ROWS, GRID_COLS = 5, 5
CELL_SIZE = 80
max_score_file = "max_score.txt"

# Functions
def load_max_score():
    try:
        with open(max_score_file, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_max_score(score):
    with open(max_score_file, "w") as file:
        file.write(str(score))

def generate_grid(rows, cols):
    return [[random.randint(1, 9) for _ in range(cols)] for _ in range(rows)]

def draw_grid(grid, selected_cells):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            cell_x = col * CELL_SIZE
            cell_y = row * CELL_SIZE
            rect = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)

            # Highlight selected cells
            if (row, col) in selected_cells:
                pygame.draw.rect(screen, BLUE, rect)
            else:
                pygame.draw.rect(screen, GRAY, rect)

            pygame.draw.rect(screen, BLACK, rect, 2)  # Cell border
            if grid[row][col] is not None:
                text = font.render(str(grid[row][col]), True, BLACK)
                screen.blit(text, (cell_x + 20, cell_y + 20))

def check_same_number_pair(grid, clicked_cells, target):
    r1, c1 = clicked_cells[0]
    r2, c2 = clicked_cells[1]
    return grid[r1][c1] == target and grid[r2][c2] == target

def check_sum_pair(grid, clicked_cells, target_sum):
    r1, c1 = clicked_cells[0]
    r2, c2 = clicked_cells[1]
    return grid[r1][c1] + grid[r2][c2] == target_sum

def remove_numbers(grid, cells):
    for r, c in cells:
        grid[r][c] = None

def add_new_numbers(grid, rows, cols):
    new_row = [random.randint(1, 9) for _ in range(cols)]
    grid.append(new_row)

def display_text(text, x, y, color=BLACK):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

def run_game():
    # Load max score
    max_score = load_max_score()
    current_score = 0
    level = 1
    start_time = time.time()

    # Level 1 setup
    target_number = random.randint(1, 9)
    grid = generate_grid(GRID_ROWS, GRID_COLS)
    selected_cells = []
    timer = TIMER_LIMIT

    running = True
    while running:
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                col = mouse_x // CELL_SIZE
                row = mouse_y // CELL_SIZE
                if len(selected_cells) < 2:
                    selected_cells.append((row, col))
                if len(selected_cells) == 2:
                    # Check for match
                    if level == 1 and check_same_number_pair(grid, selected_cells, target_number):
                        remove_numbers(grid, selected_cells)
                        current_score += 5
                    elif level == 2 and check_sum_pair(grid, selected_cells, 7):
                        remove_numbers(grid, selected_cells)
                        current_score += 5
                    selected_cells = []

        # Draw grid and UI
        draw_grid(grid, selected_cells)
        display_text(f"Score: {current_score}", 10, SCREEN_HEIGHT - 50)
        display_text(f"Max Score: {max_score}", 200, SCREEN_HEIGHT - 50)
        display_text(f"Level: {level}", SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50)
        display_text(f"Time Left: {timer}", SCREEN_WIDTH - 300, SCREEN_HEIGHT - 50)

        # Timer
        elapsed_time = int(time.time() - start_time)
        timer = TIMER_LIMIT - elapsed_time
        if timer <= 0 or all(all(cell is None for cell in row) for row in grid):
            if level == 1:
                level = 2
                target_number = None  # Reset target
                grid = generate_grid(GRID_ROWS, GRID_COLS)
                start_time = time.time()  # Reset timer
            else:
                running = False  # End game

        pygame.display.flip()
        pygame.time.delay(100)

    # End screen
    if current_score > max_score:
        save_max_score(current_score)
    screen.fill(WHITE)
    display_text(f"Game Over!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, RED)
    display_text(f"Final Score: {current_score}", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, GREEN)
    display_text(f"Press any key to quit.", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, BLUE)
    pygame.display.flip()
    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                wait = False

# Main Menu
def main_menu():
    screen.fill(WHITE)
    display_text("Number Match Game", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, RED)
    display_text("Click anywhere to start!", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, BLUE)
    pygame.display.flip()

    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                wait = False

# Main Execution
main_menu()
run_game()
pygame.quit()
