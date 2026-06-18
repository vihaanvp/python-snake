"""
Nokia-Style Snake Game — Extended Edition
==========================================
A faithful recreation of the classic Nokia Snake with added features:
  - Main menu with mode selection
  - Normal Mode (wrap-around walls, no wall death)
  - Classic Mode (wall collision = death, original Nokia feel)
  - Maze Levels (pre-designed obstacle courses)
  - Persistent high scores
  - Progressive difficulty
"""

import pygame
import random
import sys
import json
import os
from dataclasses import dataclass, field, asdict
from typing import List, Tuple, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
GRID_SIZE = 20
COLS = WINDOW_WIDTH // GRID_SIZE
ROWS = WINDOW_HEIGHT // GRID_SIZE

# Colours
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

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game settings
INITIAL_SPEED = 5
SPEED_INCREMENT = 0.5
MAX_SPEED = 28

# Scoring
POINTS_PER_FOOD = 10

# File for persistent scores
SCORES_FILE = "snake_scores.json"

# --- Maze level definitions -------------------------------------------------
# Each maze is a 2D list (rows × cols) where:
#   0 = empty, 1 = wall/obstacle
# The snake starts at (start_col, start_row) moving right.

MAZE_LEVELS = [
    {   # Level 1: Open arena (no walls)
        "name": "Open Field",
        "maze": None,  # special: no walls
        "start": (COLS // 2, ROWS // 2),
        "wrap": True,
    },
    {   # Level 2: Border walls
        "name": "Bordered",
        "maze": None,  # no inner obstacles, but outer walls kill
        "start": (COLS // 2, ROWS // 2),
        "wrap": False,
    },
    {   # Level 3: Simple pillars
        "name": "Pillars",
        "maze": [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ],
        "start": (5, 12),
        "wrap": False,
    },
    {   # Level 4: Corridors
        "name": "Corridors",
        "maze": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ],
        "start": (5, 12),
        "wrap": False,
    },
    {   # Level 5: Spiral
        "name": "Spiral",
        "maze": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        ],
        "start": (2, 12),
        "wrap": False,
    },
    {   # Level 6: Crossfire
        "name": "Crossfire",
        "maze": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ],
        "start": (5, 12),
        "wrap": False,
    },
]


# ---------------------------------------------------------------------------
# High-score persistence
# ---------------------------------------------------------------------------

@dataclass
class ScoreEntry:
    score: int
    mode: str         # "Normal", "Classic", or level name
    length: int = 0

class ScoreKeeper:
    """Loads and saves high scores to a JSON file."""

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
            pass  # silently fail — not critical

    def add_score(self, entry: ScoreEntry):
        self.scores.append(entry)
        self.scores.sort(key=lambda e: e.score, reverse=True)
        self.scores = self.scores[:20]  # keep top 20
        self.save()

    def get_best(self, mode: str) -> int:
        """Return the highest score for a given mode."""
        for entry in self.scores:
            if entry.mode == mode:
                return entry.score
        return 0

    def get_top_scores(self, limit: int = 10) -> List[ScoreEntry]:
        return self.scores[:limit]


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def draw_cell(surface, colour, col, row, inset=1):
    """Draw a single grid-aligned rectangle."""
    rect = pygame.Rect(
        col * GRID_SIZE + inset,
        row * GRID_SIZE + inset,
        GRID_SIZE - 2 * inset,
        GRID_SIZE - 2 * inset,
    )
    pygame.draw.rect(surface, colour, rect)


def draw_text(surface, text, size, colour, center_x, center_y, bold=False):
    """Render centred text."""
    font = pygame.font.SysFont("monospace", size, bold=bold)
    rendered = font.render(text, True, colour)
    rect = rendered.get_rect(center=(center_x, center_y))
    surface.blit(rendered, rect)


def draw_text_left(surface, text, size, colour, x, y, bold=False):
    """Render left-aligned text."""
    font = pygame.font.SysFont("monospace", size, bold=bold)
    rendered = font.render(text, True, colour)
    surface.blit(rendered, (x, y))


# ---------------------------------------------------------------------------
# Menu system
# ---------------------------------------------------------------------------

class MenuItem:
    def __init__(self, label, action, x, y, colour=GREEN):
        self.label = label
        self.action = action
        self.x = x
        self.y = y
        self.colour = colour
        self.font = pygame.font.SysFont("monospace", 28, bold=True)

    def draw(self, surface, selected=False):
        colour = YELLOW if selected else self.colour
        text = self.font.render(self.label, True, colour)
        rect = text.get_rect(center=(self.x, self.y))
        if selected:
            # Draw a little pointer
            pointer = self.font.render(">", True, YELLOW)
            ptr_rect = pointer.get_rect(midright=(rect.left - 15, rect.centery))
            surface.blit(pointer, ptr_rect)
        surface.blit(text, rect)

    def get_rect(self):
        text = self.font.render(self.label, True, WHITE)
        rect = text.get_rect(center=(self.x, self.y))
        return rect.inflate(40, 10)


class Menu:
    """A simple vertical menu with keyboard navigation."""

    def __init__(self, title: str, items: List[MenuItem], subtitle: str = ""):
        self.title = title
        self.subtitle = subtitle
        self.items = items
        self.selected = 0

    def handle_event(self, event) -> Optional[str]:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.items)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.items)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.items[self.selected].action
        return None

    def draw(self, surface):
        surface.fill(BLACK)
        # Title
        title_font = pygame.font.SysFont("monospace", 42, bold=True)
        title_text = title_font.render(self.title, True, GREEN)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
        surface.blit(title_text, title_rect)

        # Subtitle
        if self.subtitle:
            sub_font = pygame.font.SysFont("monospace", 16)
            sub_text = sub_font.render(self.subtitle, True, GREY)
            sub_rect = sub_text.get_rect(center=(WINDOW_WIDTH // 2, 115))
            surface.blit(sub_text, sub_rect)

        # Items
        for i, item in enumerate(self.items):
            item.draw(surface, selected=(i == self.selected))


# ---------------------------------------------------------------------------
# Maze / level rendering
# ---------------------------------------------------------------------------

def get_maze_walls(maze_data: List[List[int]]) -> List[Tuple[int, int]]:
    """Convert a 2D maze array into a list of (col, row) wall positions."""
    if maze_data is None:
        return []
    walls = []
    for row in range(len(maze_data)):
        for col in range(len(maze_data[row])):
            if maze_data[row][col] == 1:
                walls.append((col, row))
    return walls


def draw_maze(surface, maze_data: List[List[int]]):
    """Draw maze walls onto the surface."""
    if maze_data is None:
        return
    for row in range(len(maze_data)):
        for col in range(len(maze_data[row])):
            if maze_data[row][col] == 1:
                draw_cell(surface, BLUE, col, row, inset=0)


# ---------------------------------------------------------------------------
# Game modes
# ---------------------------------------------------------------------------

class GameMode:
    NORMAL = "Normal"
    CLASSIC = "Classic"
    LEVEL = "Level"


# ---------------------------------------------------------------------------
# Game state
# ---------------------------------------------------------------------------

class SnakeGame:
    """Encapsulates the entire game state and logic."""

    def __init__(self, score_keeper: ScoreKeeper):
        self.score_keeper = score_keeper
        self.mode = GameMode.NORMAL
        self.maze_data = None
        self.walls: List[Tuple[int, int]] = []
        self.wrap = True  # wrap-around walls by default
        self.reset()

    def setup_mode(self, mode: str, level_index: int = -1):
        """Configure the game for the chosen mode/level."""
        self.mode = mode
        if mode == GameMode.NORMAL:
            self.maze_data = None
            self.walls = []
            self.wrap = True
        elif mode == GameMode.CLASSIC:
            self.maze_data = None
            self.walls = []
            self.wrap = False
        elif mode == GameMode.LEVEL:
            level = MAZE_LEVELS[level_index]
            self.maze_data = level["maze"]
            self.walls = get_maze_walls(level["maze"])
            self.wrap = level["wrap"]
            self._start_pos = level["start"]
        self.reset()

    def reset(self):
        """Start a fresh game."""
        if hasattr(self, '_start_pos'):
            start_x, start_y = self._start_pos
        else:
            start_x = COLS // 2
            start_y = ROWS // 2
        self.body = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y),
        ]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.food = self._find_food()
        self.score = 0
        self.speed = INITIAL_SPEED
        self.game_over = False
        self.won = False

    def _find_food(self) -> Tuple[int, int]:
        """Find a valid food position not in snake body or walls."""
        occupied = set(self.body) | set(self.walls)
        # If there's no free cell, the player has won!
        free_cells = COLS * ROWS - len(occupied)
        if free_cells <= 0:
            self.won = True
            return (-1, -1)
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in occupied:
                return pos

    def change_direction(self, new_dir):
        """Queue a direction change (prevents 180-degree reversal)."""
        opposite = {
            UP: DOWN, DOWN: UP,
            LEFT: RIGHT, RIGHT: LEFT,
        }
        if new_dir != opposite.get(self.direction):
            self.next_direction = new_dir

    def tick(self):
        """Advance the game by one step."""
        if self.game_over or self.won:
            return

        self.direction = self.next_direction

        head = self.body[0]
        dx, dy = self.direction
        new_head = (head[0] + dx, head[1] + dy)

        # --- Wall handling ---
        if self.wrap:
            # Wrap around
            new_head = (new_head[0] % COLS, new_head[1] % ROWS)
        else:
            # Wall collision = death
            if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
                self.game_over = True
                return

        # Maze wall collision
        if new_head in self.walls:
            self.game_over = True
            return

        # Self collision
        if new_head in self.body:
            self.game_over = True
            return

        # Move
        self.body.insert(0, new_head)

        # Food check
        if new_head == self.food:
            self.score += POINTS_PER_FOOD
            self.food = self._find_food()
            self.speed = min(self.speed + SPEED_INCREMENT, MAX_SPEED)
            # Check win condition
            if self.won:
                return
        else:
            self.body.pop()

    def get_mode_name(self) -> str:
        """Return the display name for the current mode/level."""
        if self.mode == GameMode.NORMAL:
            return "Normal Mode"
        elif self.mode == GameMode.CLASSIC:
            return "Classic Mode"
        elif self.mode == GameMode.LEVEL:
            # Find the level by matching walls
            for i, level in enumerate(MAZE_LEVELS):
                if level["maze"] == self.maze_data:
                    return f"Level {i+1}: {level['name']}"
            return "Level"
        return "Unknown"

    def draw(self, surface):
        """Render the entire game onto *surface*."""
        surface.fill(BLACK)

        # --- Grid (subtle) ---
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(surface, DARK_GREY, (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(surface, DARK_GREY, (0, y), (WINDOW_WIDTH, y), 1)

        # --- Maze walls ---
        draw_maze(surface, self.maze_data)

        # --- Food ---
        if not self.won and self.food != (-1, -1):
            # Draw a blinking-ish food with a bright centre
            draw_cell(surface, RED, self.food[0], self.food[1], inset=2)
            draw_cell(surface, ORANGE, self.food[0], self.food[1], inset=4)

        # --- Snake body ---
        for i, (col, row) in enumerate(self.body):
            if i == 0:
                # Head
                draw_cell(surface, LIGHT_GREEN, col, row, inset=1)
                # Simple eyes in the direction of movement
                eye_size = 3
                cx = col * GRID_SIZE + GRID_SIZE // 2
                cy = row * GRID_SIZE + GRID_SIZE // 2
                dx, dy = self.direction
                if dx != 0:
                    pygame.draw.circle(surface, BLACK, (cx + dx * 4, cy - 3), eye_size)
                    pygame.draw.circle(surface, BLACK, (cx + dx * 4, cy + 3), eye_size)
                else:
                    pygame.draw.circle(surface, BLACK, (cx - 3, cy + dy * 4), eye_size)
                    pygame.draw.circle(surface, BLACK, (cx + 3, cy + dy * 4), eye_size)
            else:
                # Body — fade from green to dark green along the tail
                body_colour = (
                    0,
                    max(60, 180 - i * 3),
                    max(0, 100 - i * 2),
                )
                draw_cell(surface, body_colour, col, row, inset=1)

        # --- HUD ---
        font = pygame.font.SysFont("monospace", 16, bold=True)
        score_text = font.render(f"SCORE: {self.score}", True, GREEN)
        surface.blit(score_text, (10, 10))

        mode_text = font.render(self.get_mode_name(), True, GREY)
        surface.blit(mode_text, (WINDOW_WIDTH - mode_text.get_width() - 10, 10))

        # Length indicator
        len_text = font.render(f"LEN: {len(self.body)}", True, GREY)
        surface.blit(len_text, (10, 30))

        # High score for this mode
        best = self.score_keeper.get_best(self.get_mode_name())
        if best > 0:
            best_text = font.render(f"BEST: {best}", True, YELLOW)
            surface.blit(best_text, (WINDOW_WIDTH - best_text.get_width() - 10, 30))

        # --- Win overlay ---
        if self.won:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            surface.blit(overlay, (0, 0))

            draw_text(surface, "YOU WIN!", 52, YELLOW,
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)
            draw_text(surface, f"Score: {self.score}  Press SPACE to continue",
                      20, WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30)

        # --- Game over overlay ---
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))

            draw_text(surface, "GAME OVER", 48, RED,
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)

            draw_text(surface, f"Score: {self.score}",
                      24, WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10)

            draw_text(surface, "Press SPACE to restart  |  ESC for menu",
                      18, WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)


# ---------------------------------------------------------------------------
# Level select menu
# ---------------------------------------------------------------------------

def level_select_menu(surface, clock, score_keeper) -> Optional[Tuple[str, int]]:
    """Show level selection. Returns (GameMode.LEVEL, level_index) or None."""
    items = []
    for i, level in enumerate(MAZE_LEVELS):
        best = score_keeper.get_best(f"Level {i+1}: {level['name']}")
        label = f"Level {i+1} — {level['name']}"
        if best > 0:
            label += f"  (best: {best})"
        items.append(MenuItem(label, ("select", i), WINDOW_WIDTH // 2, 160 + i * 40))

    items.append(MenuItem("Back", "back", WINDOW_WIDTH // 2, 160 + len(items) * 40, colour=RED))

    menu = Menu("SELECT LEVEL", items, "Arrow keys to navigate, Enter to select")

    while True:
        dt = clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            result = menu.handle_event(event)
            if result == "back":
                return None
            if isinstance(result, tuple) and result[0] == "select":
                return (GameMode.LEVEL, result[1])

        menu.draw(surface)
        pygame.display.flip()


# ---------------------------------------------------------------------------
# High scores screen
# ---------------------------------------------------------------------------

def high_scores_screen(surface, clock, score_keeper):
    """Display high scores. Returns when user presses Escape."""
    while True:
        dt = clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return

        surface.fill(BLACK)

        title_font = pygame.font.SysFont("monospace", 38, bold=True)
        title_text = title_font.render("HIGH SCORES", True, GREEN)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
        surface.blit(title_text, title_rect)

        scores = score_keeper.get_top_scores(15)
        if not scores:
            draw_text(surface, "No scores yet. Play a game!", 20, GREY,
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        else:
            # Header
            header_font = pygame.font.SysFont("monospace", 16, bold=True)
            surface.blit(header_font.render("RANK", True, GREY), (120, 100))
            surface.blit(header_font.render("SCORE", True, GREY), (230, 100))
            surface.blit(header_font.render("MODE", True, GREY), (350, 100))

            score_font = pygame.font.SysFont("monospace", 18)
            for i, entry in enumerate(scores):
                y = 130 + i * 25
                colour = YELLOW if i == 0 else WHITE
                rank = f"#{i + 1}"
                surface.blit(score_font.render(rank, True, colour), (130, y))
                surface.blit(score_font.render(str(entry.score), True, colour), (230, y))
                surface.blit(score_font.render(entry.mode, True, colour), (350, y))

        draw_text(surface, "Press ESC or SPACE to return", 16, GREY,
                  WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)

        pygame.display.flip()


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------

def main_menu(surface, clock, score_keeper) -> Optional[str]:
    """Show the main menu and return the selected action."""
    items = [
        MenuItem("Normal Mode (No Walls)", "normal", WINDOW_WIDTH // 2, 170),
        MenuItem("Classic Mode (Walls Kill)", "classic", WINDOW_WIDTH // 2, 210),
        MenuItem("Levels", "levels", WINDOW_WIDTH // 2, 250),
        MenuItem("High Scores", "scores", WINDOW_WIDTH // 2, 290),
        MenuItem("Quit", "quit", WINDOW_WIDTH // 2, 330, colour=RED),
    ]

    menu = Menu("SNAKE", items, "The classic Nokia game — extended")

    while True:
        dt = clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            result = menu.handle_event(event)
            if result:
                return result

        menu.draw(surface)
        pygame.display.flip()


# ---------------------------------------------------------------------------
# Game loop
# ---------------------------------------------------------------------------

def run_game(surface, clock, game: SnakeGame, score_keeper: ScoreKeeper):
    """Run the main gameplay loop."""
    tick_timer = 0.0

    while True:
        dt = clock.tick(60)
        tick_timer += dt

        # --- Input ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if game.game_over or game.won:
                    if event.key == pygame.K_SPACE:
                        # Save score & restart same mode
                        if game.score > 0:
                            score_keeper.add_score(ScoreEntry(
                                score=game.score,
                                mode=game.get_mode_name(),
                                length=len(game.body),
                            ))
                        game.reset()
                        tick_timer = 0.0
                    elif event.key == pygame.K_ESCAPE:
                        # Save score & return to menu
                        if game.score > 0:
                            score_keeper.add_score(ScoreEntry(
                                score=game.score,
                                mode=game.get_mode_name(),
                                length=len(game.body),
                            ))
                        return "menu"
                else:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        game.change_direction(UP)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        game.change_direction(DOWN)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        game.change_direction(LEFT)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        game.change_direction(RIGHT)

        # --- Fixed-step update ---
        if not game.game_over and not game.won:
            tick_interval = 1000.0 / game.speed
            while tick_timer >= tick_interval:
                game.tick()
                tick_timer -= tick_interval
        else:
            tick_timer = 0.0

        # --- Render ---
        game.draw(surface)
        pygame.display.flip()


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    pygame.init()
    pygame.display.set_caption("Snake — Nokia Classic Extended")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    score_keeper = ScoreKeeper()
    game = SnakeGame(score_keeper)

    running = True
    while running:
        action = main_menu(screen, clock, score_keeper)

        if action == "quit":
            running = False
            break

        elif action == "normal":
            game.setup_mode(GameMode.NORMAL)
            result = run_game(screen, clock, game, score_keeper)
            if result == "quit":
                running = False
                break

        elif action == "classic":
            game.setup_mode(GameMode.CLASSIC)
            result = run_game(screen, clock, game, score_keeper)
            if result == "quit":
                running = False
                break

        elif action == "levels":
            selection = level_select_menu(screen, clock, score_keeper)
            if selection is None:
                continue
            mode, level_idx = selection
            game.setup_mode(mode, level_idx)
            result = run_game(screen, clock, game, score_keeper)
            if result == "quit":
                running = False
                break

        elif action == "scores":
            high_scores_screen(screen, clock, score_keeper)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
