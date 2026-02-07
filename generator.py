import random
from typing import Tuple, List

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
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.rng = random.Random()

    def generate_perfect(self, start: Tuple[int, int]) -> None:
        self._dfs(start[0], start[1])

    def _dfs(self, x: int, y: int) -> None:
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
