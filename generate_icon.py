"""
Generate a retro pixel-art snake logo in PNG and ICO formats.
Run:  python generate_icon.py
"""

from PIL import Image, ImageDraw, ImageFont
import os

SIZE = 256
OUTPUT_DIR = "icons"
OUTPUT_PNG = os.path.join(OUTPUT_DIR, "snake_logo.png")
OUTPUT_ICO = os.path.join(OUTPUT_DIR, "snake_logo.ico")

# Colours (same retro palette as the game)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
LIGHT_GREEN = (100, 255, 100)
WHITE = (200, 200, 200)
DARK_GREEN = (0, 100, 0)
RED = (220, 30, 30)
ORANGE = (255, 160, 50)
GREY = (60, 60, 60)

img = Image.new("RGBA", (SIZE, SIZE), BLACK)
draw = ImageDraw.Draw(img)

# =========================================================
# Pixel-art snake head (centre)
# =========================================================
# We'll draw using a grid of 16x16 "pixels" (each 16x16 real pixels)
# Grid: 16 cols x 16 rows, each cell = 16x16 px

P = 16  # pixel size
CX, CY = 8, 8  # grid centre roughly

def rect(col, row, w=1, h=1):
    """Draw a filled rectangle in grid coordinates."""
    x1 = col * P
    y1 = row * P
    x2 = x1 + w * P
    y2 = y1 + h * P
    return (x1, y1, x2, y2)

# --- Snake head (8x8 grid, roughly centred at 4,4) ---
# Eyes
draw.ellipse(rect(6, 6), fill=WHITE)
draw.ellipse(rect(8, 6), fill=WHITE)
draw.ellipse(rect(6, 6, 1, 1), fill=WHITE)
draw.ellipse(rect(8, 6, 1, 1), fill=WHITE)

# Pupils
draw.ellipse(rect(7, 6), fill=BLACK)
draw.ellipse(rect(9, 6), fill=BLACK)

# Head body
for y in range(5, 11):
    for x in range(4, 12):
        if y == 5 and x < 5 or y == 5 and x > 10:
            continue
        if y == 10 and x < 5 or y == 10 and x > 10:
            continue
        if y == 5 and (x == 5 or x == 10):
            draw.rectangle(rect(x, y), fill=LIGHT_GREEN)
        elif y >= 6 and y <= 9:
            draw.rectangle(rect(x, y), fill=LIGHT_GREEN)
        elif y == 10 and (x == 5 or x == 10):
            draw.rectangle(rect(x, y), fill=GREEN)

# Nostrils
draw.rectangle(rect(6, 8), fill=DARK_GREEN)
draw.rectangle(rect(9, 8), fill=DARK_GREEN)

# Tongue (forked)
draw.rectangle(rect(7, 4), fill=RED)
draw.rectangle(rect(8, 4), fill=RED)
draw.rectangle(rect(7, 3), fill=RED)
draw.rectangle(rect(8, 3), fill=RED)

# --- Apple / Food (top-right area) ---
draw.rectangle(rect(12, 2), fill=RED)
draw.rectangle(rect(13, 2), fill=RED)
draw.rectangle(rect(12, 3), fill=RED)
draw.rectangle(rect(13, 3), fill=RED)
# Stem
draw.rectangle(rect(12, 1), fill=DARK_GREEN)
# Highlight
draw.rectangle(rect(13, 2), fill=ORANGE)

# --- Score numbers as decoration ---
# "10" near the apple
def draw_number(n, start_col, start_row, colour=WHITE):
    """Crude 5x3 pixel number drawing."""
    digits = {
        '1': [(0,0),(0,1),(0,2),(0,3)],
        '0': [(0,0),(1,0),(2,0),(0,1),(2,1),(0,2),(2,2),(0,3),(1,3),(2,3)],
    }
    for ch in str(n):
        if ch in digits:
            for dx, dy in digits[ch]:
                draw.rectangle(rect(start_col + dx, start_row + dy), fill=colour)
        start_col += 4

# Draw "10" next to apple
draw_number(1, 14, 4, WHITE)
draw_number(0, 14, 8, WHITE)

# =========================================================
# Text: "SNAKE" at the bottom
# =========================================================
try:
    # Try to get a monospace font at reasonable size
    font = ImageFont.truetype("C:\\Windows\\Fonts\\lucon.ttf", 36)
except (IOError, OSError):
    font = ImageFont.load_default()

# "SNAKE" title
title = "SNAKE"
bbox = draw.textbbox((0, 0), title, font=font)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
tx = (SIZE - tw) // 2
ty = 200
draw.text((tx, ty), title, fill=GREEN, font=font)

# Subtitle
sub = "NOKIA CLASSIC"
bbox2 = draw.textbbox((0, 0), sub, font=ImageFont.truetype("C:\\Windows\\Fonts\\lucon.ttf", 16))
tw2 = bbox2[2] - bbox2[0]
tx2 = (SIZE - tw2) // 2
draw.text((tx2, ty + 40), sub, fill=GREY,
          font=ImageFont.truetype("C:\\Windows\\Fonts\\lucon.ttf", 16))

# Save PNG
img.save(OUTPUT_PNG)
print(f"Saved {OUTPUT_PNG} ({SIZE}x{SIZE})")

# Save ICO with multiple sizes for Windows
ico_sizes = [16, 24, 32, 48, 64, 128, 256]
img.save(OUTPUT_ICO, sizes=[(s, s) for s in ico_sizes])
print(f"Saved {OUTPUT_ICO} with sizes: {ico_sizes}")

print("Done!")
