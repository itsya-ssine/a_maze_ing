"""Maze generator using recursive backtracker (DFS)."""

import random
from typing import List, Optional, Tuple

from maze import Maze
from cell import TOP, RIGHT, BOTTOM, LEFT


Direction = Tuple[int, int, int, int]
DIRECTIONS: List[Direction] = [
    (0, -1, TOP, BOTTOM),
    (1, 0, RIGHT, LEFT),
    (0, 1, BOTTOM, TOP),
    (-1, 0, LEFT, RIGHT),
]


class MazeGenerator:
    """Generate a perfect maze via recursive backtracking."""

    def __init__(
        self, maze: Maze, seed: Optional[int] = None
    ) -> None:
        """Initialise the generator.

        Args:
            maze: The Maze instance to carve.
            seed: Optional RNG seed for reproducibility.
        """
        self.maze = maze
        self.rng = random.Random(seed)

    def generate_perfect(
        self, start: Tuple[int, int]
    ) -> None:
        """Generate a perfect maze from *start*.

        Args:
            start: (x, y) coordinates to begin from.
        """
        self._dfs(start[0], start[1])

    def generate_imperfect(
        self, start: Tuple[int, int]
    ) -> None:
        """Generate an imperfect maze with loops.

        Builds a perfect maze first, then removes random
        internal walls to create multiple paths.

        Args:
            start: (x, y) coordinates to begin from.
        """
        self.generate_perfect(start)

        walls: List[Tuple[int, int, int, int]] = []
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.cell(x, y)
                if (
                    x < self.maze.width - 1
                    and cell.walls & RIGHT
                    and not cell.marked
                ):
                    nx = x + 1
                    if not self.maze.cell(nx, y).marked:
                        walls.append((x, y, RIGHT, LEFT))
                if (
                    y < self.maze.height - 1
                    and cell.walls & BOTTOM
                    and not cell.marked
                ):
                    ny = y + 1
                    if not self.maze.cell(x, ny).marked:
                        walls.append((x, y, BOTTOM, TOP))
        self.rng.shuffle(walls)
        count: int = max(
            1, (self.maze.width * self.maze.height) // 10
        )

        removed: int = 0
        for i, (x, y, wall, opposite) in enumerate(walls):
            if i >= count:
                break
            nx, ny = x, y
            if wall == RIGHT:
                nx = x + 1
            elif wall == BOTTOM:
                ny = y + 1
            self.maze.remove_wall(x, y, wall)
            self.maze.remove_wall(nx, ny, opposite)
            if self._creates_3x3(x, y, nx, ny):
                self.maze.add_wall(x, y, wall)
                self.maze.add_wall(nx, ny, opposite)
                continue
            removed += 1

    def _has_3x3_open(self, sx: int, sy: int) -> bool:
        """Check if a 3x3 block starting at (sx, sy) is open.

        Args:
            sx: Left column of the 3x3 block.
            sy: Top row of the 3x3 block.

        Returns:
            True if all 12 internal walls are open.
        """
        for dy in range(3):
            for dx in range(3):
                cell = self.maze.cell(sx + dx, sy + dy)
                if dx < 2 and cell.walls & RIGHT:
                    return False
                if dy < 2 and cell.walls & BOTTOM:
                    return False
        return True

    def _creates_3x3(
        self, x1: int, y1: int, x2: int, y2: int
    ) -> bool:
        """Check if removing a wall between two cells created a 3x3.

        Args:
            x1: Column of first cell.
            y1: Row of first cell.
            x2: Column of second cell.
            y2: Row of second cell.

        Returns:
            True if any 3x3 open area now exists nearby.
        """
        min_x: int = max(0, min(x1, x2) - 2)
        min_y: int = max(0, min(y1, y2) - 2)
        max_x: int = min(self.maze.width - 3, max(x1, x2))
        max_y: int = min(self.maze.height - 3, max(y1, y2))
        for sy in range(min_y, max_y + 1):
            for sx in range(min_x, max_x + 1):
                if self._has_3x3_open(sx, sy):
                    return True
        return False

    def enforce_borders(self) -> None:
        """Ensure all outer walls are closed.

        Forces border cells to have their external wall.
        """
        for x in range(self.maze.width):
            self.maze.add_wall(x, 0, TOP)
            self.maze.add_wall(
                x, self.maze.height - 1, BOTTOM
            )
        for y in range(self.maze.height):
            self.maze.add_wall(0, y, LEFT)
            self.maze.add_wall(
                self.maze.width - 1, y, RIGHT
            )

    def _dfs(self, x: int, y: int) -> None:
        """Depth-first search carving passages.

        Args:
            x: Column index.
            y: Row index.
        """
        cell = self.maze.cell(x, y)
        cell.visited = True

        directions = DIRECTIONS[:]
        self.rng.shuffle(directions)

        for dx, dy, wall, opposite in directions:
            nx, ny = x + dx, y + dy
            if not self.maze.inside(nx, ny):
                continue
            neighbor = self.maze.cell(nx, ny)
            if neighbor.visited:
                continue

            self.maze.remove_wall(x, y, wall)
            self.maze.remove_wall(nx, ny, opposite)
            self._dfs(nx, ny)
