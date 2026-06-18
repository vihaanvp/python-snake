# AGENTS.md — snake-game

Single-file Python (`main.py`) Nokia-style Snake game with pygame-ce.

## Commands

```bash
pip install pygame-ce          # only dependency; use pygame-ce NOT pygame
python main.py                 # run the game
pyinstaller --onefile --windowed --name snake --icon=icons/snake_logo.ico --distpath builds main.py
```

EXE lands in `builds/` (gitignored). No tests, no linter, no CI.

## Architecture

- **Entrypoint**: `main()` at bottom of `main.py`, called via `if __name__ == "__main__"`
- **Grid**: 32 columns × 24 rows. `CELL_SIZE` calculated from display resolution at startup.
- **Scaling helpers**: `s(n)` scales pixel sizes, `sf(n)` scales font sizes, both based on `SCALE = CELL_SIZE / 20`. Every hardcoded visual size in the code uses these.
- **Maze data**: Embedded as strings in `MAZE_LEVELS` list, parsed by `_parse_maze()`. Each string row `'1'` = wall, `'0'` = open. 11 levels total.
- **Direction input**: Buffered via `collections.deque` (max 3 entries) so rapid key presses are not lost.
- **High scores**: `snake_scores.json` (auto-created, gitignored). Top 20 entries kept.

## Controls (not in README)

| Key | Action |
|-----|--------|
| `ESC` | Pause / Resume (not `P`) |
| `F11` | Toggle fullscreen ↔ windowed |
| In pause | `↑↓` navigate, `Enter/Space` select |

Game starts in fullscreen. Resolution is detected automatically; windowed mode falls back to 640×480 (20px cells).

## File layout

Only `main.py` matters. `icons/snake_logo.ico` needed for PyInstaller builds. `generate_icon.py` can recreate icon files.

## Gotchas

- `pygame` (without `-ce`) has no prebuilt wheel for Python 3.14 and fails to compile. Always install `pygame-ce`.
- Module-level globals `CELL_SIZE`, `WINDOW_WIDTH`, `WINDOW_HEIGHT`, `SCALE` are reassigned at startup and on `F11` toggle. Code that reads them after import gets the updated values.
- Maze level names and order in `README.md` features list must match `MAZE_LEVELS` array order exactly.
- Version string is hardcoded in three places: `main.py` line (version display), `README.md` badge, `CHANGELOG.md` header.
