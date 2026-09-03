"""
Schotter — after Georg Nees, 1968.

    A star grid that falls apart as it descends. The top row is perfectly ordered;
each row after it is rotated and displaced a little more than the one before.
Nees plotted the original on a Zuse Graphomat; you are about to do it in a
language he did not have, on a machine he would have envied.

Run it:

    python sketch.py

It writes sketch.svg in your home directory. Open that in a browser (or drag it
into VS Code). Nothing to install — this uses only what ships with Python.

Then change one of the numbers below, run it again, and commit. GitHub will show
you the two images side by side.
"""

import random
from pathlib import Path

# ---------------------------------------------------------------------------
# The knobs. These are yours. Change them, run again, look, commit.
# ---------------------------------------------------------------------------

COLS = 12            # hearts across
ROWS = 22            # hearts down — the chaos builds over this many rows
SEED = 55913          # any integer. Same seed = same image, every time, forever.
CHAOS = 1.0            # how fast order collapses. 0 = perfect grid. 2 = rubble.
SQUARE = 40             # size of one heart, in svg units
MARGIN = 60          # breathing room around the grid
HEART_COLOR = "#ff0000"
BACKGROUND = "#faf8f4"
STROKE_WIDTH = 1.4

OUTPUT = Path(__file__).resolve().parent / "sketch.svg"

# ---------------------------------------------------------------------------
# The drawing.
# ---------------------------------------------------------------------------


def heart(x, y, size, angle_deg, dx, dy):
    """One filled heart, rotated about its centre and nudged off its grid slot."""
    cx, cy = x + size / 2, y + size / 2
    return (
        f'  <path d="M {cx:.2f},{cy + size * 0.35:.2f} '
        f'C {cx - size * 0.7:.2f},{cy - size * 0.05:.2f} '
        f'{cx - size * 0.45:.2f},{cy - size * 0.55:.2f} '
        f'{cx:.2f},{cy - size * 0.15:.2f} '
        f'C {cx + size * 0.45:.2f},{cy - size * 0.55:.2f} '
        f'{cx + size * 0.7:.2f},{cy - size * 0.05:.2f} '
        f'{cx:.2f},{cy + size * 0.35:.2f} Z" '
        f'transform="translate({dx:.2f} {dy:.2f}) '
        f'rotate({angle_deg:.2f} {cx:.2f} {cy:.2f})" />'
    )


def draw():
    rng = random.Random(SEED)
    parts = []

    for row in range(ROWS):
        # Disorder grows with depth. Squaring it keeps the top calm and lets the
        # bottom really come apart — the whole point of the piece.
        damage = CHAOS * (row / ROWS) ** 2

        for col in range(COLS):
            x = MARGIN + col * SQUARE
            y = MARGIN + row * SQUARE
            angle = rng.uniform(-1, 1) * damage * 45
            dx = rng.uniform(-1, 1) * damage * SQUARE * 0.5
            dy = rng.uniform(-1, 1) * damage * SQUARE * 0.5
            parts.append(heart(x, y, SQUARE, angle, dx, dy))

    width = COLS * SQUARE + MARGIN * 2
    height = ROWS * SQUARE + MARGIN * 2

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}">',
            f'  <rect width="100%" height="100%" fill="{BACKGROUND}" filter="url(#frosted-background)" />',
            '  <defs>',
            '    <filter id="frosted-background" x="0" y="0" width="100%" height="100%">',
            '      <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" seed="17" result="grain" />',
            '      <feColorMatrix in="grain" type="saturate" values="0" result="gray-grain" />',
            '      <feComponentTransfer in="gray-grain" result="soft-grain">',
            '        <feFuncA type="table" tableValues="0 0.12" />',
            '      </feComponentTransfer>',
            '      <feBlend in="SourceGraphic" in2="soft-grain" mode="multiply" />',
            '    </filter>',
            f'    <linearGradient id="heart-fade" gradientUnits="userSpaceOnUse" '
            f'x1="0" y1="0" x2="0" y2="{height}">',
            '      <stop offset="0%" stop-color="white" />',
            '      <stop offset="100%" stop-color="black" />',
            '    </linearGradient>',
            f'    <mask id="heart-fade-mask" maskUnits="userSpaceOnUse" '
            f'x="0" y="0" width="{width}" height="{height}">',
            f'      <rect width="{width}" height="{height}" fill="url(#heart-fade)" />',
            '    </mask>',
            '    <filter id="heart-shadow" x="-20%" y="-20%" width="140%" height="140%">',
            '      <feDropShadow dx="2" dy="3" stdDeviation="2" flood-color="#000000" flood-opacity="0.28" />',
            '    </filter>',
            '  </defs>',
            f'  <g fill="{HEART_COLOR}" stroke="none" filter="url(#heart-shadow)" mask="url(#heart-fade-mask)">',
            *parts,
            "  </g>",
            "</svg>",
        ]
    )


if __name__ == "__main__":
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(draw())
    print(f"wrote {OUTPUT} — {COLS}x{ROWS} hearts, seed {SEED}, chaos {CHAOS}")
    print("open it in a browser, then change a number and run me again")
