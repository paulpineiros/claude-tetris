# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Classic Tetris implemented in vanilla JavaScript with HTML5 Canvas and CSS. No dependencies, no build tools, no package.json. README and code comments are in Spanish.

## Running / testing

There is no build or test suite. To run the game:

```bash
open index.html                # macOS, opens directly in browser
python3 -m http.server 8000    # or serve locally, then visit http://localhost:8000
```

There is no linter or test runner configured. Verify changes by opening the page in a browser and playing.

## Architecture

Three files, all logic lives in `game.js` (~300 lines, single global scope, no modules):

- `index.html` — DOM structure: `#board` canvas (300×600, 10×20 cells of 30px), `#next-canvas` preview (120×120), HUD spans (`#score`, `#lines`, `#level`), and `#overlay` for pause/game-over.
- `style.css` — dark/retro visual theme.
- `game.js` — game state and loop, described below.

### Core state

Single set of module-level `let` variables (`board`, `current`, `next`, `score`, `lines`, `level`, `paused`, `gameOver`, `dropInterval`, etc.) mutated in place — not encapsulated in a class or object. `init()` resets all of them and is also the restart handler.

### Key mechanics

- **Board**: `ROWS × COLS` matrix, each cell `0` (empty) or `1–7` (color index identifying the piece type that placed it).
- **Pieces**: `PIECES` array holds the 7 tetromino shapes as square matrices. `rotateCW` rotates via transpose + row reversal; there's no piece object model beyond `{ type, shape, x, y }`.
- **Collision** (`collide`): checks board bounds and existing filled cells.
- **Wall kicks** (`tryRotate`): after rotating, tries offsets `[0, -1, 1, -2, 2]` until one doesn't collide, else the rotation is discarded.
- **Game loop** (`loop`): driven by `requestAnimationFrame`; accumulates elapsed time (`dropAccum`) and drops the piece one row when `dropInterval` is exceeded, otherwise calls `lockPiece()`.
- **Line clearing** (`clearLines`): scans bottom-to-top, `splice`s full rows out and `unshift`s empty rows in; re-checks the same row index after removing one (`r++` inside the loop).
- **Scoring**: `LINE_SCORES = [0, 100, 300, 500, 800]` × current `level`; hard drop adds 2 pts/cell dropped, soft drop adds 1 pt/row.
- **Leveling/speed**: level = `floor(lines / 10) + 1`; `dropInterval = max(100, 1000 - (level - 1) * 90)` ms.
- **Ghost piece** (`ghostY`): projects `current` straight down until collision, drawn at `globalAlpha = 0.2`.

### Tunable constants (top of `game.js`)

`COLS`, `ROWS`, `BLOCK`, `COLORS`, `LINE_SCORES`, initial `dropInterval`. If `COLS`/`ROWS`/`BLOCK` change, the `#board` canvas `width`/`height` in `index.html` must be updated to match (`COLS × BLOCK`, `ROWS × BLOCK`).

### Input

All keyboard handling is a single `keydown` listener at the bottom of `game.js` (arrow keys, `X` to rotate, `Space` for hard drop, `P` for pause). `P` works even when paused/game over; other keys are ignored in those states.
