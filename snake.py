"""
Classic Nokia-Style Snake Game
===============================
A faithful recreation of the original Snake game found on Nokia phones.
Built with Pygame — no external assets needed.
"""

import pygame
import random
import sys

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Display
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
GRID_SIZE = 20  # 20×20 pixel cells (like the old Nokia grid feel)
COLS = WINDOW_WIDTH // GRID_SIZE
ROWS = WINDOW_HEIGHT // GRID_SIZE

# Colours (Nokia-style green-on-black)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
WHITE = (200, 200, 200)
GREY = (60, 60, 60)
RED = (180, 0, 0)

# Directions as vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game settings (tuned to feel like the original)
INITIAL_SPEED = 8          # frames per second to start (tempo of the original)
SPEED_INCREMENT = 0.5      # speed added per food eaten
MAX_SPEED = 24             # cap so it's still playable

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def random_food_position(snake_body):
    """Return a random grid cell not occupied by the snake."""
    while True:
        pos = (
            random.randint(0, COLS - 1),
            random.randint(0, ROWS - 1),
        )
        if pos not in snake_body:
            return pos


def draw_cell(surface, colour, col, row, inset=1):
    """Draw a single grid-aligned rectangle (with an optional inset for
    the 'chunky pixel' look of the original)."""
    rect = pygame.Rect(
        col * GRID_SIZE + inset,
        row * GRID_SIZE + inset,
        GRID_SIZE - 2 * inset,
        GRID_SIZE - 2 * inset,
    )
    pygame.draw.rect(surface, colour, rect)


# ---------------------------------------------------------------------------
# Game state
# ---------------------------------------------------------------------------

class SnakeGame:
    """Encapsulates the entire game state and logic."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Start a fresh game."""
        # Snake starts in the middle, moving right, length 3
        start_x = COLS // 2
        start_y = ROWS // 2
        self.body = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y),
        ]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.food = random_food_position(self.body)
        self.score = 0
        self.speed = INITIAL_SPEED
        self.game_over = False

    def change_direction(self, new_dir):
        """Queue a direction change (prevents 180-degree reversal)."""
        opposite = {
            UP: DOWN,
            DOWN: UP,
            LEFT: RIGHT,
            RIGHT: LEFT,
        }
        # Don't allow reversing into yourself
        if new_dir != opposite.get(self.direction):
            self.next_direction = new_dir

    def tick(self):
        """Advance the game by one step (called once per frame)."""
        if self.game_over:
            return

        # Apply queued direction
        self.direction = self.next_direction

        # Calculate new head position
        head = self.body[0]
        dx, dy = self.direction
        new_head = (head[0] + dx, head[1] + dy)

        # Wall collision — game over (classic Nokia behaviour)
        if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
            self.game_over = True
            return

        # Self collision
        if new_head in self.body:
            self.game_over = True
            return

        # Move: insert new head
        self.body.insert(0, new_head)

        # Check food
        if new_head == self.food:
            self.score += 1
            self.food = random_food_position(self.body)
            # Increase speed (feels like the original progression)
            self.speed = min(self.speed + SPEED_INCREMENT, MAX_SPEED)
            # Don't remove tail → snake grows
        else:
            # Remove tail → snake stays same length
            self.body.pop()

    def draw(self, surface):
        """Render the entire game onto *surface*."""
        surface.fill(BLACK)

        # --- Grid (subtle) ---
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(surface, GREY, (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(surface, GREY, (0, y), (WINDOW_WIDTH, y), 1)

        # --- Food (blinking pixel look) ---
        draw_cell(surface, RED, self.food[0], self.food[1], inset=2)

        # --- Snake body ---
        for i, (col, row) in enumerate(self.body):
            if i == 0:
                # Head — slightly brighter
                draw_cell(surface, WHITE, col, row, inset=1)
                # Simple eyes
                eye_size = 3
                cx = col * GRID_SIZE + GRID_SIZE // 2
                cy = row * GRID_SIZE + GRID_SIZE // 2
                dx, dy = self.direction
                # Eyes offset in the direction of movement
                if dx != 0:
                    pygame.draw.circle(surface, BLACK, (cx + dx * 4, cy - 3), eye_size)
                    pygame.draw.circle(surface, BLACK, (cx + dx * 4, cy + 3), eye_size)
                else:
                    pygame.draw.circle(surface, BLACK, (cx - 3, cy + dy * 4), eye_size)
                    pygame.draw.circle(surface, BLACK, (cx + 3, cy + dy * 4), eye_size)
            else:
                # Body — classic Nokia green
                draw_cell(surface, GREEN, col, row, inset=1)

        # --- Score ---
        font = pygame.font.SysFont("monospace", 18, bold=True)
        score_text = font.render(f"SCORE: {self.score}", True, GREEN)
        surface.blit(score_text, (10, 10))

        # --- Game over overlay ---
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))

            go_font = pygame.font.SysFont("monospace", 48, bold=True)
            go_text = go_font.render("GAME OVER", True, RED)
            go_rect = go_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            surface.blit(go_text, go_rect)

            sub_font = pygame.font.SysFont("monospace", 20, bold=True)
            sub_text = sub_font.render(f"Score: {self.score}   Press SPACE to restart", True, WHITE)
            sub_rect = sub_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
            surface.blit(sub_text, sub_rect)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    pygame.init()
    pygame.display.set_caption("Snake — Nokia Classic")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    game = SnakeGame()
    running = True

    # How many ms since last game tick (accumulator pattern for fixed-step)
    tick_timer = 0.0

    while running:
        dt = clock.tick(60)  # cap at 60 FPS, returns ms since last frame
        tick_timer += dt

        # --- Input ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game.game_over:
                    if event.key == pygame.K_SPACE:
                        game.reset()
                        tick_timer = 0.0
                else:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        game.change_direction(UP)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        game.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        game.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        game.change_direction(RIGHT)

        # --- Fixed-step update (each tick = one grid step) ---
        tick_interval = 1000.0 / game.speed  # ms per game tick
        while tick_timer >= tick_interval:
            game.tick()
            tick_timer -= tick_interval

        # --- Render ---
        game.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
