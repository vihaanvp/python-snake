# Changelog

All notable changes to this project will be documented in this file.

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
