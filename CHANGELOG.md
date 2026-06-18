# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] — 2026-06-18

### Added
- Direction input buffer: rapid key presses are no longer dropped
  - Buffers up to 3 direction changes so quick corner turns register correctly
  - Eliminates the "ignored key press" issue during fast play
- 5 new maze levels: Box, Tunnel, Maze, Zigzag, Fortress (total now 11 levels)
- Fullscreen mode with F11 toggle (game starts in fullscreen by default)
- Interactive pause menu with Resume and Quit to Main Menu buttons
  - Navigate with UP/DOWN arrows, select with ENTER/SPACE
- **Resolution-aware rendering**: game now detects the display resolution and
  computes an optimal cell size to fill the screen at native quality
  - All fonts, insets, eye sizes, spacing, and borders are scaled proportionally
  - Text is rendered at the scaled font size directly (not upscaled), so it
    stays crisp and anti-aliased at any display resolution
  - Grid lines, HUD elements, menu items, pause overlay — everything adapts

### Changed
- Pause key changed from P to ESC
- Version updated to v1.2.0
- README.md corrected to reference `main.py` instead of the old `snake.py`

## [1.1.0] — 2026-06-18

### Added
- Main menu with keyboard navigation
- Normal Mode: snake wraps around screen edges (no wall death)
- Classic Mode: wall collision ends the game (original Nokia behaviour)
- 6 maze levels with unique obstacle layouts
- Level selection screen
- Persistent high scores saved to `snake_scores.json`
- High scores display screen (top 15 scores)
- Win condition: filling the entire grid triggers a "YOU WIN!" screen
- Snake body colour gradient (fades along the tail)
- Two-tone food rendering
- HUD showing score, length, mode name, and best score
- Project documentation: `README.md`, `CHANGELOG.md`, `LICENSE` (MIT)
- `.gitignore` with Python, JetBrains, and OS rules
- Icon files and generator script:
  - `icons/snake_logo.png` — retro pixel-art snake logo (256×256)
  - `icons/snake_logo.ico` — multi-resolution Windows icon (16×16 to 256×256)
  - `generate_icon.py` — script to regenerate icons from scratch
- Portable EXE now includes the snake logo icon
- `builds/` folder for pre-compiled executables

### Changed
- Reduced initial snake speed for better early-game feel
- Directory structure reorganised: icons in `icons/`, EXE in `builds/`
- `generate_icon.py` output paths updated to save into `icons/` folder
- Refactored `snake.py` to `main.py` — simplified codebase, removed all comments, compressed maze data using string representation, removed unused code

## [1.0.0] — 2026-06-18

### Added
- Initial release with core Snake gameplay
- Grid-based movement (20×20 pixel cells)
- Green-on-black retro aesthetic
- Snake grows when eating food
- Progressive speed increase
- Wall and self collision detection
- Eyes on the snake head that face the movement direction
- Score display
- Game over overlay with restart option
