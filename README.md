*This project has been created as part of the 42 curriculum by abameur, yelmajdo.*

## Description

A-Maze-ing is a maze generator written in Python.  It reads a plain-text
configuration file, builds a random maze (perfect or imperfect), writes
the result to a hex-encoded output file, and renders it as coloured ASCII
in the terminal.  The program stamps a visible "42" pattern of fully
closed cells, computes the shortest path from entry to exit with BFS,
and lets the user interact with the display (regenerate, toggle path,
change wall colours).

## Instructions

### Requirements

- Python 3.10 or later
- A virtual environment is recommended

### Installation

```bash
make install          # creates .venv and installs flake8 + mypy
```

### Running

```bash
make run              # or: python3 a_maze_ing.py config.txt
```

### Debug mode

```bash
make debug            # runs with pdb
```

### Linting

```bash
make lint             # flake8 + mypy (mandatory flags)
make lint-strict      # flake8 + mypy --strict
```

### Cleaning

```bash
make clean            # removes __pycache__, .mypy_cache, .venv, etc.
```

## Configuration file

The configuration file uses one `KEY=VALUE` pair per line.
Lines starting with `#` are comments and are ignored.

| Key | Type | Description | Example |
|-----|------|-------------|---------|
| `WIDTH` | int | Maze width in cells | `WIDTH=20` |
| `HEIGHT` | int | Maze height in cells | `HEIGHT=15` |
| `ENTRY` | x,y | Entry cell coordinates | `ENTRY=0,0` |
| `EXIT` | x,y | Exit cell coordinates | `EXIT=19,14` |
| `OUTPUT_FILE` | string | Path for the output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | bool | If True, generate a perfect maze | `PERFECT=True` |
| `SEED` | int (optional) | RNG seed for reproducibility | `SEED=42` |

Example `config.txt`:

```
# Maze config
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=2,14
OUTPUT_FILE=output.txt
PERFECT=True
SEED=42
```

## Output file format

- One hexadecimal digit per cell, space-separated, one row per line.
- Bit encoding: bit 0 = North, bit 1 = East, bit 2 = South, bit 3 = West.
  A set bit means the wall is **closed**.
- After the grid, an empty line, then three lines:
  1. Entry coordinates `x,y`
  2. Exit coordinates `x,y`
  3. Shortest path as a string of `N`, `E`, `S`, `W` characters

## Maze generation algorithm

### Algorithm chosen: Recursive Backtracker (DFS)

The generator uses depth-first search with random neighbour selection:

1. Start at the entry cell, mark it visited.
2. Pick a random unvisited neighbour, remove the wall between them, move there.
3. If all neighbours are visited, backtrack.
4. Repeat until every cell has been visited.

### Why this algorithm

- **Simplicity** — easy to implement and understand.
- **Guaranteed connectivity** — every cell is visited exactly once, producing a spanning tree (perfect maze).
- **Long corridors** — DFS naturally creates winding paths, which look good visually.
- **Seed support** — using a local `random.Random(seed)` instance makes the output fully deterministic for a given seed.

### Imperfect maze mode

When `PERFECT=False`, the generator first builds a perfect maze, then
removes a limited number of random internal walls (≈ 10 % of the area).
Before each removal it checks that no 3×3 open area is created; if it
would be, the wall is restored and skipped.

## Visual representation

The maze is rendered in the terminal as ASCII:

- `E` marks the entry (magenta).
- `X` marks the exit (red).
- `·` marks the shortest path (green, togglable).
- `███` marks the "42" pattern (dark grey).
- Walls are drawn with `+`, `-`, `|`.

### User interactions

| Key | Action |
|-----|--------|
| `1` | Re-generate a new maze |
| `2` | Show / hide the shortest path |
| `3` | Cycle wall colours (white → blue → yellow → green → red) |
| `4` | Quit |

## Reusable code

The maze generation logic lives in `generator.py` as the `MazeGenerator`
class.  Together with `maze.py`, `cell.py`, and `solver.py`, it can be
imported into any Python project.

### Basic usage example

```python
from maze import Maze
from generator import MazeGenerator
from solver import shortest_path

maze = Maze(20, 15)
gen = MazeGenerator(maze, seed=42)
gen.generate_perfect((0, 0))           # or gen.generate_imperfect((0, 0))
path = shortest_path(maze, (0, 0), (19, 14))

# Access the grid
for y in range(maze.height):
    for x in range(maze.width):
        cell = maze.cell(x, y)
        print(f"({x},{y}) walls={cell.walls:#x}")
```

### Custom parameters

- **Size**: pass `width` and `height` to `Maze(width, height)`.
- **Seed**: pass `seed=<int>` to `MazeGenerator` for reproducibility;
  omit or pass `None` for a random maze.
- **Perfect / imperfect**: call `generate_perfect(start)` or
  `generate_imperfect(start)`.

### Accessing the structure

- `maze.cell(x, y).walls` — bitmask of closed walls (N=1, E=2, S=4, W=8).
- `maze.grid` — 2-D list of `Cell` objects (row-major).
- `shortest_path(maze, start, end)` — returns a list of `(x, y)` tuples.

## Resources

- [Maze generation algorithm — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker explanation — Jamis Buck](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
- [BFS shortest path — GeeksforGeeks](https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/)
- Python documentation: `random`, `collections.deque`, `typing`

### AI usage

AI tools (GitHub Copilot / ChatGPT) were used for:

- **Code review and linting fixes** — spotting flake8 / mypy issues.
- **Docstring generation** — writing Google-style docstrings.
- **Explaining algorithms** — understanding DFS / BFS trade-offs.
- **Config validation logic** — structuring error handling.

All generated code was reviewed, understood, and tested manually before
inclusion.  Core logic (generation, solving, rendering) was written and
debugged by the team.

## Team and project management

### Roles

| Member | Responsibilities |
|--------|-----------------|
| **abameur** | Maze generation, solver, output writer, config parser |
| **yelmajdo** | Renderer, "42" pattern, validations, packaging, README |

### Planning

**Initial plan:**
1. Config parser and basic maze structure
2. DFS maze generator (perfect)
3. BFS solver and output writer
4. Terminal renderer with user interactions
5. Imperfect maze mode, 3×3 constraint, border enforcement
6. "42" pattern stamping
7. Reusable package build
8. Documentation and final linting

**How it evolved:**
The order stayed mostly the same.  The "42" pattern was moved earlier
because it needed to be stamped before generation (cells marked visited
so DFS carves around them).  Border enforcement was simpler than expected.
The 3×3 open-area check required a try-then-undo approach in the
imperfect generator.

### What worked well

- Splitting the project into small, focused modules made testing easy.
- Using a seeded RNG from the start saved time debugging.
- Incremental development (perfect maze first, then imperfect) kept the
  code stable.

### What could be improved

- The DFS is recursive and may hit Python's stack limit on very large
  mazes; an iterative version would be safer.
- More automated tests (pytest) would catch edge cases earlier.

### Tools used

- **Python 3.12**, **flake8**, **mypy** — language and linting.
- **pdb** — debugging.
- **Git** — version control.
- **GitHub Copilot / ChatGPT** — code review and documentation assistance.
- **venv** — dependency isolation.
