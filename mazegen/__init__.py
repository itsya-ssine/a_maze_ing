"""mazegen — Reusable maze generator package.

A standalone Python package for generating and solving 2D mazes using
a recursive backtracker (DFS) algorithm.

Quick start
-----------

.. code-block:: python

    from mazegen import Maze, MazeGenerator, shortest_path

    # 1. Create a grid
    maze = Maze(20, 15)

    # 2. Generate (seed is optional, for reproducibility)
    gen = MazeGenerator(maze, seed=42)
    gen.generate_perfect((0, 0))   # or gen.generate_imperfect((0, 0))
    gen.enforce_borders()

    # 3. Solve
    path = shortest_path(maze, (0, 0), (19, 14))
    print(path)  # [(0,0), (1,0), ...]

    # 4. Inspect any cell
    cell = maze.cell(5, 3)
    print(cell.walls)  # bitmask: TOP=1, RIGHT=2, BOTTOM=4, LEFT=8

Custom parameters
-----------------
- **Size**: ``Maze(width, height)``
- **Seed**: ``MazeGenerator(maze, seed=123)`` — omit or pass ``None``
  for a random maze.
- **Perfect / imperfect**: call ``generate_perfect(start)`` or
  ``generate_imperfect(start)``.

Accessing the structure
-----------------------
- ``maze.cell(x, y).walls`` — bitmask of closed walls
  (TOP=1, RIGHT=2, BOTTOM=4, LEFT=8).
- ``maze.grid`` — 2-D list of ``Cell`` objects (row-major).
- ``maze.width`` / ``maze.height`` — grid dimensions.

Accessing a solution
--------------------
- ``shortest_path(maze, start, end)`` — returns a list of ``(x, y)``
  tuples representing the shortest path, or an empty list if none exists.
"""

from .cell import Cell, TOP, RIGHT, BOTTOM, LEFT
from .maze import Maze
from .generator import MazeGenerator
from .solver import shortest_path

__all__ = [
    "Cell",
    "Maze",
    "MazeGenerator",
    "shortest_path",
    "TOP",
    "RIGHT",
    "BOTTOM",
    "LEFT",
]

__version__ = "1.0.0"
