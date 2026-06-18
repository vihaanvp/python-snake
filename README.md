# 🐍 Snake — Nokia Classic Extended

A faithful recreation of the classic Nokia Snake game with modern enhancements. Built with Python and pygame-ce.

> **Latest version: v1.2.0** — [View Changelog](CHANGELOG.md)

## Features

- **Main Menu** — Choose your game mode before playing
- **Normal Mode** — Snake wraps around the screen edges (no wall death)
- **Classic Mode** — Wall collision ends the game, just like the original Nokia phone
- **6 Maze Levels** — Pre-designed obstacle courses with increasing difficulty:
  1. Open Field
  2. Bordered
  3. Pillars
  4. Corridors
  5. Spiral
  6. Crossfire
- **Persistent High Scores** — Top 15 scores saved locally across sessions
- **Progressive Difficulty** — Snake speeds up as you eat more food
- **Retro Aesthetic** — Green-on-black monochrome style with pixel-perfect rendering
- **Custom Icon** — Pixel-art snake logo included as a multi-resolution Windows icon
- **MIT Licensed** — Free to use, modify, and distribute

## How to Play

### Controls

| Key | Action |
|-----|--------|
| `↑` / `W` | Move up |
| `↓` / `S` | Move down |
| `←` / `A` | Move left |
| `→` / `D` | Move right |
| `Enter` / `Space` | Select menu item / Restart |
| `Esc` | Return to menu (after game over) |
| `↑` / `↓` | Navigate menus |

### Objective

Guide the snake to eat red food pellets. Each pellet grows the snake by one segment and increases your score by 10 points. The game ends if you collide with a wall (in Classic/Maze modes), an obstacle, or your own tail. In Normal Mode, the snake passes through walls and reappears on the opposite side.

## Installation

### Option 1: Run from source (Python required)

1. **Install Python 3.10+**
2. **Install dependencies:**
   ```bash
   pip install pygame-ce
   ```
3. **Run the game:**
   ```bash
   python snake.py
   ```

### Option 2: Portable EXE (no Python required)

Download the latest `snake.exe` from the [Releases](https://github.com/vihaanvp/python-snake/releases) page and run it directly.

## Building the EXE yourself

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name snake --icon=icons/snake_logo.ico --distpath builds snake.py
```

The executable will be placed in the `builds/` folder.

## Project Structure

```
snake-game/
├── icons/                      # Icon files
│   ├── snake_logo.png
│   └── snake_logo.ico
├── snake.py                    # Main game source code
├── generate_icon.py            # Icon generation script
├── README.md                   # This file
├── CHANGELOG.md                # Version history
├── LICENSE                     # MIT License
└── .gitignore                  # Git ignore rules
```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
