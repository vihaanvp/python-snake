import pygame
import random
import sys
import json
import os
import math
from collections import deque
from dataclasses import dataclass, asdict
from typing import List, Tuple, Optional

BASE_CELL_SIZE = 20
COLS = 32
ROWS = 24
CELL_SIZE = BASE_CELL_SIZE
WINDOW_WIDTH = CELL_SIZE * COLS
WINDOW_HEIGHT = CELL_SIZE * ROWS
SCALE = 1.0
def s(n): return max(1, int(n * SCALE))
def sf(n): return max(8, int(n * SCALE))

def update_display(cell_size):
    global CELL_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, SCALE
    CELL_SIZE = cell_size
    WINDOW_WIDTH = CELL_SIZE * COLS
    WINDOW_HEIGHT = CELL_SIZE * ROWS
    SCALE = CELL_SIZE / BASE_CELL_SIZE

BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
LIGHT_GREEN = (100, 255, 100)
WHITE = (200, 200, 200)
GREY = (60, 60, 60)
DARK_GREY = (30, 30, 30)
RED = (200, 30, 30)
YELLOW = (255, 220, 50)
BLUE = (50, 120, 220)
ORANGE = (255, 140, 50)
PURPLE = (180, 80, 200)
CYAN = (0, 200, 200)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

INITIAL_SPEED = 5
SPEED_INCREMENT = 0.5
MAX_SPEED = 28
POINTS_PER_FOOD = 10
SCORES_FILE = "snake_scores.json"

def _parse_maze(rows):
    return [[int(c) for c in row] for row in rows]

MAZE_LEVELS = [
    {"name": "Open Field", "maze": None, "start": (COLS // 2, ROWS // 2), "wrap": True},
    {"name": "Bordered", "maze": None, "start": (COLS // 2, ROWS // 2), "wrap": False},
    {"name": "Box", "maze": _parse_maze([
        "111111111111111111111111111111",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000111111111100000000001",
        "100000000100000000100000000001",
        "100000000100000000100000000001",
        "100000000100000000100000000001",
        "100000000100000000100000000001",
        "100000000100000000100000000001",
        "100000000100000000100000000001",
        "100000000100000000100000000001",
        "100000000100000000100000000001",
        "100000000100000000100000000001",
        "100000000100000000100000000001",
        "100000000100000000100000000001",
        "100000000111111111100000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
    ]), "start": (3, 12), "wrap": False},
    {"name": "Tunnel", "maze": _parse_maze([
        "111111111111111111111111111111",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "111111111110000001111111111111",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "111111111110000001111111111111",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "111111111110000001111111111111",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "111111111110000001111111111111",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "111111111110000001111111111111",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "111111111110000001111111111111",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "111111111110000001111111111111",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
    ]), "start": (3, 12), "wrap": False},
    {"name": "Pillars", "maze": _parse_maze([
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000010000000000000100000001",
        "100000010000000000000100000001",
        "100000010000000000000100000001",
        "100000010000000000000100000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000010000000000000100000001",
        "100000010000000000000100000001",
        "100000010000000000000100000001",
        "100000010000000000000100000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
    ]), "start": (5, 12), "wrap": False},
    {"name": "Corridors", "maze": _parse_maze([
        "111111111111111111111111111111",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100111110000111110000111110001",
        "100100010000100010000100010001",
        "100100010000100010000100010001",
        "100100010000100010000100010001",
        "100111110000111110000111110001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100111000111000111000111000111",
        "100101000101000101000101000101",
        "100101000101000101000101000101",
        "100111000111000111000111000111",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100111110000111110000111110001",
        "100100010000100010000100010001",
        "100100010000100010000100010001",
        "100100010000100010000100010001",
        "100111110000111110000111110001",
        "100000000000000000000000000001",
    ]), "start": (5, 12), "wrap": False},
    {"name": "Maze", "maze": _parse_maze([
        "111111111111111111111111111111",
        "100000000000000000000000000001",
        "101111111111111111111111111101",
        "101000000000000000000000000101",
        "101011111111111011111111110101",
        "101010000000001000000000010101",
        "101010111111101111111110010101",
        "101010100000001000000010010101",
        "101010101111111111111010010101",
        "101010101000000000001010010101",
        "101010101011111111101010010101",
        "101010101010000000101010010101",
        "101010101010111110101010010101",
        "101010101010000010101010010101",
        "101010101011111010101010010101",
        "101010101000000010101010010101",
        "101010101111111110101010010101",
        "101010100000000000101010010101",
        "101010111111111111101010010101",
        "101010000000000000001010010101",
        "101011111111111111111010010101",
        "101000000000000000000000010101",
        "101111111111111111111111110101",
        "100000000000000000000000000001",
    ]), "start": (2, 2), "wrap": False},
    {"name": "Zigzag", "maze": _parse_maze([
        "111111111111111111111111111111",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "111111111111111111100000000001",
        "100000000000000000100000000001",
        "100000000000000000100000000001",
        "100000000000000000111111111111",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "111111111111111111100000000001",
        "100000000000000000100000000001",
        "100000000000000000100000000001",
        "100000000000000000111111111111",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "111111111111111111100000000001",
        "100000000000000000100000000001",
        "100000000000000000100000000001",
        "100000000000000000111111111111",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
    ]), "start": (2, 12), "wrap": False},
    {"name": "Fortress", "maze": _parse_maze([
        "111111111111111111111111111111",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000111111111111111000000001",
        "100000100000000000001000000001",
        "100000100111111110001000000001",
        "100000100100000010001000000001",
        "100000100101111010001000000001",
        "100000100100001010001000000001",
        "100000100101111010001000000001",
        "100000100100000010001000000001",
        "100000100111111110001000000001",
        "100000100000000000001000000001",
        "100000111111111111111000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
    ]), "start": (2, 12), "wrap": False},
    {"name": "Crossfire", "maze": _parse_maze([
        "111111111111111111111111111111",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000111111111000000000001",
        "100000000100000001000000000001",
        "100000000100000001000000000001",
        "100000000100000001000000000001",
        "100000000100000001000000000001",
        "100000000111111111000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
        "100000000000000000000000000001",
    ]), "start": (5, 12), "wrap": False},
    {"name": "Spiral", "maze": _parse_maze([
        "111111111111111111111111111111",
        "100000000000000000000000000001",
        "101111111111111111111111111101",
        "101000000000000000000000001101",
        "101011111111111111111111001101",
        "101010000000000000000011001101",
        "101010111111111111111011001101",
        "101010100000000000001011001101",
        "101010101111111111101011001101",
        "101010101000000001101011001101",
        "101010101011111101101011001101",
        "101010101000001101101011001101",
        "101010101011101101101011001101",
        "101010101000101101101011001101",
        "101010101011101101101011001101",
        "101010101000001101101011001101",
        "101010101011111101101011001101",
        "101010101000000001101011001101",
        "101010101111111111101011001101",
        "101010100000000000001011001101",
        "101010111111111111111011001101",
        "101010000000000000000011001101",
        "101011111111111111111111001101",
        "101000000000000000000000001101",
    ]), "start": (2, 12), "wrap": False},
]

@dataclass
class ScoreEntry:
    score: int
    mode: str
    length: int = 0

class ScoreKeeper:
    def __init__(self, filepath: str = SCORES_FILE):
        self.filepath = filepath
        self.scores: List[ScoreEntry] = []
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    data = json.load(f)
                    self.scores = [ScoreEntry(**entry) for entry in data]
            except (json.JSONDecodeError, IOError):
                self.scores = []

    def save(self):
        try:
            with open(self.filepath, "w") as f:
                data = [asdict(entry) for entry in self.scores]
                json.dump(data, f, indent=2)
        except IOError:
            pass

    def add_score(self, entry: ScoreEntry):
        self.scores.append(entry)
        self.scores.sort(key=lambda e: e.score, reverse=True)
        self.scores = self.scores[:20]
        self.save()

    def get_best(self, mode: str) -> int:
        for entry in self.scores:
            if entry.mode == mode:
                return entry.score
        return 0

    def get_top_scores(self, limit: int = 10) -> List[ScoreEntry]:
        return self.scores[:limit]

def draw_cell(surface, colour, col, row, inset=1):
    ins = s(inset)
    rect = pygame.Rect(col * CELL_SIZE + ins, row * CELL_SIZE + ins, CELL_SIZE - 2 * ins, CELL_SIZE - 2 * ins)
    pygame.draw.rect(surface, colour, rect)

def draw_text(surface, text, size, colour, center_x, center_y, bold=False):
    font = pygame.font.SysFont("monospace", sf(size), bold=bold)
    rendered = font.render(text, True, colour)
    rect = rendered.get_rect(center=(center_x, center_y))
    surface.blit(rendered, rect)

class MenuItem:
    def __init__(self, label, action, x, y, colour=GREEN):
        self.label = label
        self.action = action
        self.x = x
        self.y = y
        self.base_colour = colour
        self.font = pygame.font.SysFont("monospace", sf(28), bold=True)
        self.pulse = 0.0

    def draw(self, surface, selected=False, time=0.0):
        if selected:
            self.pulse = math.sin(time * 3) * 0.3 + 0.7
            r = int(YELLOW[0] * self.pulse + GREEN[0] * (1 - self.pulse))
            g = int(YELLOW[1] * self.pulse + GREEN[1] * (1 - self.pulse))
            b = int(YELLOW[2] * self.pulse + GREEN[2] * (1 - self.pulse))
            colour = (r, g, b)
        else:
            colour = self.base_colour
        text = self.font.render(self.label, True, colour)
        rect = text.get_rect(center=(self.x, self.y))
        if selected:
            decay = (math.sin(time * 6) * 0.5 + 0.5)
            pulse_alpha = int(180 * decay)
            glow_surf = pygame.Surface((rect.width + s(40), rect.height + s(10)), pygame.SRCALPHA)
            glow_rect = glow_surf.get_rect(center=(rect.width // 2 + s(20), rect.height // 2 + s(5)))
            pygame.draw.rect(glow_surf, (YELLOW[0], YELLOW[1], YELLOW[2], pulse_alpha), glow_rect, border_radius=s(8))
            surface.blit(glow_surf, (rect.left - s(20), rect.top - s(5)))
            pointer = self.font.render(">", True, YELLOW)
            ptr_rect = pointer.get_rect(midright=(rect.left - s(15), rect.centery))
            surface.blit(pointer, ptr_rect)
            pointer2 = self.font.render("<", True, YELLOW)
            ptr2_rect = pointer2.get_rect(midleft=(rect.right + s(15), rect.centery))
            surface.blit(pointer2, ptr2_rect)
        surface.blit(text, rect)

class Menu:
    def __init__(self, title: str, items: List[MenuItem], subtitle: str = ""):
        self.title = title
        self.subtitle = subtitle
        self.items = items
        self.selected = 0
        self.time = 0.0

    def handle_event(self, event) -> Optional[str]:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.items)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.items)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.items[self.selected].action
        return None

    def draw_title_border(self, surface):
        for x in range(s(40), WINDOW_WIDTH - s(40), CELL_SIZE):
            draw_cell(surface, DARK_GREEN, x // CELL_SIZE, 1, inset=s(2))
            draw_cell(surface, DARK_GREEN, x // CELL_SIZE, 9, inset=s(2))
        left_col = (WINDOW_WIDTH // 2 - s(140)) // CELL_SIZE
        right_col = (WINDOW_WIDTH // 2 + s(140)) // CELL_SIZE
        for y in range(2, 9):
            draw_cell(surface, DARK_GREEN, left_col, y, inset=s(2))
            draw_cell(surface, DARK_GREEN, right_col, y, inset=s(2))

    def draw_snake_decoration(self, surface, time):
        snake_positions = [
            (0.1, 0.15), (0.15, 0.12), (0.2, 0.1), (0.25, 0.12), (0.3, 0.15),
            (0.35, 0.12), (0.4, 0.1), (0.45, 0.12), (0.5, 0.15), (0.55, 0.12),
            (0.6, 0.1), (0.65, 0.12), (0.7, 0.15), (0.75, 0.12), (0.8, 0.1),
            (0.85, 0.12), (0.9, 0.15),
        ]
        offset = (time * 30) % WINDOW_WIDTH
        for i, (fx, fy) in enumerate(snake_positions):
            x = int((fx * WINDOW_WIDTH + offset) % WINDOW_WIDTH)
            y = int(fy * WINDOW_HEIGHT)
            alpha = max(50, 200 - i * 10)
            if alpha > 50:
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if 0 <= col < COLS and 0 <= row < ROWS:
                    colour = (0, alpha, 0) if i % 3 != 0 else (alpha // 2, alpha, alpha // 2)
                    surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    pygame.draw.rect(surf, colour, (s(1), s(1), CELL_SIZE - s(2), CELL_SIZE - s(2)))
                    surface.blit(surf, (col * CELL_SIZE, row * CELL_SIZE))

    def draw(self, surface):
        surface.fill(BLACK)
        self.draw_snake_decoration(surface, self.time)
        self.draw_title_border(surface)
        title_font = pygame.font.SysFont("monospace", sf(44), bold=True)
        glow_colour = (0, max(100, int(180 + math.sin(self.time * 2) * 60)), 0)
        for dx, dy in [(-s(2),0),(s(2),0),(0,-s(2)),(0,s(2))]:
            glow = title_font.render(self.title, True, (0, max(50, glow_colour[1]//3), 0))
            gr = glow.get_rect(center=(WINDOW_WIDTH // 2 + dx, s(80) + dy))
            surface.blit(glow, gr)
        title_text = title_font.render(self.title, True, LIGHT_GREEN)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, s(80)))
        surface.blit(title_text, title_rect)
        if self.subtitle:
            sub_font = pygame.font.SysFont("monospace", sf(16))
            sub_text = sub_font.render(self.subtitle, True, GREY)
            sub_rect = sub_text.get_rect(center=(WINDOW_WIDTH // 2, s(115)))
            surface.blit(sub_text, sub_rect)
        for i, item in enumerate(self.items):
            item.draw(surface, selected=(i == self.selected), time=self.time)
        version_font = pygame.font.SysFont("monospace", sf(12))
        version_text = version_font.render("v1.2.0", True, DARK_GREEN)
        surface.blit(version_text, (WINDOW_WIDTH - s(60), WINDOW_HEIGHT - s(20)))

def get_maze_walls(maze_data):
    if maze_data is None:
        return []
    walls = []
    for row in range(len(maze_data)):
        for col in range(len(maze_data[row])):
            if maze_data[row][col] == 1:
                walls.append((col, row))
    return walls

def draw_maze(surface, maze_data):
    if maze_data is None:
        return
    for row in range(len(maze_data)):
        for col in range(len(maze_data[row])):
            if maze_data[row][col] == 1:
                draw_cell(surface, BLUE, col, row, inset=0)

NORMAL = "Normal"
CLASSIC = "Classic"
LEVEL = "Level"

class SnakeGame:
    def __init__(self, score_keeper: ScoreKeeper):
        self.score_keeper = score_keeper
        self.mode = NORMAL
        self.maze_data = None
        self.walls: List[Tuple[int, int]] = []
        self.wrap = True
        self.paused = False
        self.dir_buffer: deque = deque()
        self.reset()

    def setup_mode(self, mode: str, level_index: int = -1):
        self.mode = mode
        if mode == NORMAL:
            self.maze_data = None
            self.walls = []
            self.wrap = True
        elif mode == CLASSIC:
            self.maze_data = None
            self.walls = []
            self.wrap = False
        elif mode == LEVEL:
            level = MAZE_LEVELS[level_index]
            self.maze_data = level["maze"]
            self.walls = get_maze_walls(level["maze"])
            self.wrap = level["wrap"]
            self._start_pos = level["start"]
        self.reset()

    def reset(self):
        if hasattr(self, '_start_pos'):
            start_x, start_y = self._start_pos
        else:
            start_x, start_y = COLS // 2, ROWS // 2
        self.body = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        self.direction = RIGHT
        self.dir_buffer.clear()
        self.food = self._find_food()
        self.score = 0
        self.speed = INITIAL_SPEED
        self.game_over = False
        self.won = False
        self.paused = False

    def toggle_pause(self):
        if not self.game_over and not self.won:
            self.paused = not self.paused

    def _find_food(self) -> Tuple[int, int]:
        occupied = set(self.body) | set(self.walls)
        if COLS * ROWS - len(occupied) <= 0:
            self.won = True
            return (-1, -1)
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in occupied:
                return pos

    def change_direction(self, new_dir):
        opposite = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
        last = self.dir_buffer[-1] if self.dir_buffer else self.direction
        if new_dir != opposite.get(last) and len(self.dir_buffer) < 3:
            self.dir_buffer.append(new_dir)

    def tick(self):
        if self.game_over or self.won or self.paused:
            return
        if self.dir_buffer:
            self.direction = self.dir_buffer.popleft()
        head = self.body[0]
        dx, dy = self.direction
        new_head = (head[0] + dx, head[1] + dy)
        if self.wrap:
            new_head = (new_head[0] % COLS, new_head[1] % ROWS)
        elif not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
            self.game_over = True
            return
        if new_head in self.walls:
            self.game_over = True
            return
        if new_head in self.body:
            self.game_over = True
            return
        self.body.insert(0, new_head)
        if new_head == self.food:
            self.score += POINTS_PER_FOOD
            self.food = self._find_food()
            self.speed = min(self.speed + SPEED_INCREMENT, MAX_SPEED)
            if self.won:
                return
        else:
            self.body.pop()

    def get_mode_name(self) -> str:
        if self.mode == NORMAL:
            return "Normal Mode"
        if self.mode == CLASSIC:
            return "Classic Mode"
        if self.mode == LEVEL:
            for i, level in enumerate(MAZE_LEVELS):
                if level["maze"] == self.maze_data:
                    return f"Level {i+1}: {level['name']}"
            return "Level"
        return "Unknown"

    def draw(self, surface):
        surface.fill(BLACK)
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(surface, DARK_GREY, (x, 0), (x, WINDOW_HEIGHT), s(1))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(surface, DARK_GREY, (0, y), (WINDOW_WIDTH, y), s(1))
        draw_maze(surface, self.maze_data)
        if not self.won and self.food != (-1, -1):
            draw_cell(surface, RED, self.food[0], self.food[1], inset=s(2))
            draw_cell(surface, ORANGE, self.food[0], self.food[1], inset=s(4))
        for i, (col, row) in enumerate(self.body):
            if i == 0:
                draw_cell(surface, LIGHT_GREEN, col, row, inset=s(1))
                eye_size = s(3)
                cx = col * CELL_SIZE + CELL_SIZE // 2
                cy = row * CELL_SIZE + CELL_SIZE // 2
                dx, dy = self.direction
                if dx != 0:
                    pygame.draw.circle(surface, BLACK, (cx + dx * s(4), cy - s(3)), eye_size)
                    pygame.draw.circle(surface, BLACK, (cx + dx * s(4), cy + s(3)), eye_size)
                else:
                    pygame.draw.circle(surface, BLACK, (cx - s(3), cy + dy * s(4)), eye_size)
                    pygame.draw.circle(surface, BLACK, (cx + s(3), cy + dy * s(4)), eye_size)
            else:
                draw_cell(surface, (0, max(60, 180 - i * 3), max(0, 100 - i * 2)), col, row, inset=s(1))
        font = pygame.font.SysFont("monospace", sf(16), bold=True)
        left_margin = s(10)
        line_h = sf(16) + s(4)
        surface.blit(font.render(f"SCORE: {self.score}", True, GREEN), (left_margin, s(10)))
        mode_text = font.render(self.get_mode_name(), True, GREY)
        surface.blit(mode_text, (WINDOW_WIDTH - mode_text.get_width() - s(10), s(10)))
        surface.blit(font.render(f"LEN: {len(self.body)}", True, GREY), (left_margin, s(10) + line_h))
        surface.blit(font.render(f"SPD: {self.speed:.0f}", True, GREY), (left_margin, s(10) + line_h * 2))
        best = self.score_keeper.get_best(self.get_mode_name())
        if best > 0:
            surface.blit(font.render(f"BEST: {best}", True, YELLOW), (WINDOW_WIDTH - mode_text.get_width() - s(10), s(10) + line_h))
        if self.won:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            surface.blit(overlay, (0, 0))
            draw_text(surface, "YOU WIN!", sf(52), YELLOW, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - s(30))
            draw_text(surface, f"Score: {self.score}  Press SPACE to continue", sf(20), WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + s(30))
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))
            draw_text(surface, "GAME OVER", sf(48), RED, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - s(30))
            draw_text(surface, f"Score: {self.score}", sf(24), WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + s(10))
            draw_text(surface, "Press SPACE to restart  |  ESC for menu", sf(18), WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + s(50))

def level_select_menu(surface, clock, score_keeper) -> Optional[Tuple[str, int]]:
    items = []
    for i, level in enumerate(MAZE_LEVELS):
        best = score_keeper.get_best(f"Level {i+1}: {level['name']}")
        label = f"Level {i+1} — {level['name']}"
        if best > 0:
            label += f"  (best: {best})"
        items.append(MenuItem(label, ("select", i), WINDOW_WIDTH // 2, s(140) + i * s(32)))
    items.append(MenuItem("Back", "back", WINDOW_WIDTH // 2, s(140) + len(items) * s(32), colour=RED))
    menu = Menu("SELECT LEVEL", items, "Arrow keys to navigate, Enter to select")
    while True:
        dt = clock.tick(30)
        menu.time += dt / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            result = menu.handle_event(event)
            if result == "back":
                return None
            if isinstance(result, tuple) and result[0] == "select":
                return (LEVEL, result[1])
        menu.draw(surface)
        pygame.display.flip()

def high_scores_screen(surface, clock, score_keeper):
    scroll_offset = 0
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN):
                    return
                if event.key == pygame.K_DOWN:
                    scroll_offset = min(scroll_offset + 1, max(0, 15 - 10))
                if event.key == pygame.K_UP:
                    scroll_offset = max(scroll_offset - 1, 0)
        surface.fill(BLACK)
        title_font = pygame.font.SysFont("monospace", sf(38), bold=True)
        title_text = title_font.render("HIGH SCORES", True, GREEN)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, s(50)))
        surface.blit(title_text, title_rect)
        scores = score_keeper.get_top_scores(15)
        if not scores:
            draw_text(surface, "No scores yet. Play a game!", sf(20), GREY, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        else:
            header_font = pygame.font.SysFont("monospace", sf(16), bold=True)
            surface.blit(header_font.render("RANK", True, GREY), (s(120), s(100)))
            surface.blit(header_font.render("SCORE", True, GREY), (s(230), s(100)))
            surface.blit(header_font.render("MODE", True, GREY), (s(350), s(100)))
            score_font = pygame.font.SysFont("monospace", sf(18))
            for i, entry in enumerate(scores):
                y = s(130) + i * s(25)
                colour = YELLOW if i == 0 else WHITE
                surface.blit(score_font.render(f"#{i + 1}", True, colour), (s(130), y))
                surface.blit(score_font.render(str(entry.score), True, colour), (s(230), y))
                surface.blit(score_font.render(entry.mode, True, colour), (s(350), y))
        draw_text(surface, "Press ESC or SPACE to return", sf(16), GREY, WINDOW_WIDTH // 2, WINDOW_HEIGHT - s(30))
        draw_text(surface, "Use UP/DOWN to scroll", sf(12), DARK_GREEN, WINDOW_WIDTH // 2, WINDOW_HEIGHT - s(15))
        pygame.display.flip()

def main_menu(surface, clock, score_keeper) -> Optional[str]:
    items = [
        MenuItem("Normal Mode (No Walls)", "normal", WINDOW_WIDTH // 2, s(170)),
        MenuItem("Classic Mode (Walls Kill)", "classic", WINDOW_WIDTH // 2, s(210)),
        MenuItem("Levels", "levels", WINDOW_WIDTH // 2, s(250)),
        MenuItem("High Scores", "scores", WINDOW_WIDTH // 2, s(290)),
        MenuItem("Quit", "quit", WINDOW_WIDTH // 2, s(330), colour=RED),
    ]
    menu = Menu("SNAKE", items, "The classic Nokia game — extended edition")
    while True:
        dt = clock.tick(30)
        menu.time += dt / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            result = menu.handle_event(event)
            if result:
                return result
        menu.draw(surface)
        pygame.display.flip()

def run_game(surface, clock, game: SnakeGame, score_keeper: ScoreKeeper):
    tick_timer = 0.0
    paused_selection = 0
    while True:
        dt = clock.tick(60)
        tick_timer += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", surface
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    flags = surface.get_flags()
                    is_fs = flags & pygame.FULLSCREEN
                    if is_fs:
                        update_display(BASE_CELL_SIZE)
                        new_flags = 0
                    else:
                        info = pygame.display.Info()
                        cell = max(BASE_CELL_SIZE, min(info.current_w // COLS, info.current_h // ROWS))
                        update_display(cell)
                        new_flags = pygame.FULLSCREEN | pygame.SCALED
                    surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), new_flags)
                    continue
                if game.game_over or game.won:
                    if event.key == pygame.K_SPACE:
                        if game.score > 0:
                            score_keeper.add_score(ScoreEntry(score=game.score, mode=game.get_mode_name(), length=len(game.body)))
                        game.reset()
                        tick_timer = 0.0
                        paused_selection = 0
                    elif event.key == pygame.K_ESCAPE:
                        if game.score > 0:
                            score_keeper.add_score(ScoreEntry(score=game.score, mode=game.get_mode_name(), length=len(game.body)))
                        return "menu", surface
                elif game.paused:
                    if event.key in (pygame.K_UP, pygame.K_DOWN):
                        paused_selection = 1 - paused_selection
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if paused_selection == 0:
                            game.toggle_pause()
                        else:
                            if game.score > 0:
                                score_keeper.add_score(ScoreEntry(score=game.score, mode=game.get_mode_name(), length=len(game.body)))
                            return "menu", surface
                    elif event.key == pygame.K_ESCAPE:
                        game.toggle_pause()
                else:
                    if event.key == pygame.K_ESCAPE:
                        game.toggle_pause()
                        paused_selection = 0
                    if not game.paused:
                        if event.key in (pygame.K_UP, pygame.K_w):
                            game.change_direction(UP)
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            game.change_direction(DOWN)
                        elif event.key in (pygame.K_LEFT, pygame.K_a):
                            game.change_direction(LEFT)
                        elif event.key in (pygame.K_RIGHT, pygame.K_d):
                            game.change_direction(RIGHT)
        if not game.game_over and not game.won:
            if not game.paused:
                tick_interval = 1000.0 / game.speed
                while tick_timer >= tick_interval:
                    game.tick()
                    tick_timer -= tick_interval
        else:
            tick_timer = 0.0
        game.draw(surface)
        if game.paused:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            surface.blit(overlay, (0, 0))
            draw_text(surface, "PAUSED", sf(52), YELLOW, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - s(60))
            pause_items = ["Resume", "Quit to Main Menu"]
            for i, label in enumerate(pause_items):
                y = WINDOW_HEIGHT // 2 - s(10) + i * s(45)
                colour = YELLOW if i == paused_selection else WHITE
                font = pygame.font.SysFont("monospace", sf(28), bold=True)
                if i == paused_selection:
                    glow = pygame.Surface((s(200), s(36)), pygame.SRCALPHA)
                    pulse = math.sin(pygame.time.get_ticks() * 0.006) * 0.3 + 0.7
                    glow_colour = (YELLOW[0], YELLOW[1], YELLOW[2], int(120 * pulse))
                    pygame.draw.rect(glow, glow_colour, glow.get_rect(), border_radius=s(6))
                    surface.blit(glow, (WINDOW_WIDTH // 2 - s(100), y - s(18)))
                    pointer = font.render(">", True, YELLOW)
                    p_rect = pointer.get_rect(midright=(WINDOW_WIDTH // 2 - s(90), y))
                    surface.blit(pointer, p_rect)
                    pointer2 = font.render("<", True, YELLOW)
                    p2_rect = pointer2.get_rect(midleft=(WINDOW_WIDTH // 2 + s(90), y))
                    surface.blit(pointer2, p2_rect)
                text = font.render(label, True, colour)
                rect = text.get_rect(center=(WINDOW_WIDTH // 2, y))
                surface.blit(text, rect)
            hint_font = pygame.font.SysFont("monospace", sf(14))
            hint = hint_font.render("UP/DOWN navigate  |  ENTER select  |  ESC resume", True, GREY)
            surface.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, WINDOW_HEIGHT // 2 + s(80)))
        pygame.display.flip()

def main():
    pygame.init()
    pygame.display.set_caption("Snake — Nokia Classic Extended")
    info = pygame.display.Info()
    cell = max(BASE_CELL_SIZE, min(info.current_w // COLS, info.current_h // ROWS))
    update_display(cell)
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
    clock = pygame.time.Clock()
    score_keeper = ScoreKeeper()
    game = SnakeGame(score_keeper)
    while True:
        action = main_menu(screen, clock, score_keeper)
        if action == "quit":
            break
        elif action == "normal":
            game.setup_mode(NORMAL)
        elif action == "classic":
            game.setup_mode(CLASSIC)
        elif action == "levels":
            selection = level_select_menu(screen, clock, score_keeper)
            if selection is None:
                continue
            game.setup_mode(selection[0], selection[1])
        elif action == "scores":
            high_scores_screen(screen, clock, score_keeper)
            continue
        result, screen = run_game(screen, clock, game, score_keeper)
        if result == "quit":
            break
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
