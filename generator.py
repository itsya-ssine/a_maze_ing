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
                ):
                    walls.append((x, y, RIGHT, LEFT))
                if (
                    y < self.maze.height - 1
                    and cell.walls & BOTTOM
                ):
                    walls.append((x, y, BOTTOM, TOP))
        self.rng.shuffle(walls)
        count: int = max(
            1, (self.maze.width * self.maze.height) // 10
        )

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

