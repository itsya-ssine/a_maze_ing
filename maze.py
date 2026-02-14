"""Maze module containing the Maze grid class."""

from typing import List
from cell import Cell


class Maze:
    """Represent a 2D grid of cells forming a maze."""

    def __init__(self, width: int, height: int) -> None:
        """Initialise a maze with all walls closed.

        Args:
            width: Number of columns.
            height: Number of rows.
        """
        self.width = width
        self.height = height
        self.grid: List[List[Cell]] = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]

    def inside(self, x: int, y: int) -> bool:
        """Check if coordinates are within bounds.

        Args:
            x: Column index.
            y: Row index.

        Returns:
            True if (x, y) is inside the grid.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def cell(self, x: int, y: int) -> Cell:
        """Return the cell at position (x, y).

        Args:
            x: Column index.
            y: Row index.

        Returns:
            The Cell object at that position.
        """
        return self.grid[y][x]

    def remove_wall(
        self, x: int, y: int, wall: int
    ) -> None:
        """Remove a wall from the cell at (x, y).

        Args:
            x: Column index.
            y: Row index.
            wall: Bitmask of the wall to remove.
        """
        self.cell(x, y).walls &= ~wall
