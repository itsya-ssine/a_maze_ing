from typing import List
from cell import Cell


class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid: List[List[Cell]] = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]

    def inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def cell(self, x: int, y: int) -> Cell:
        return self.grid[y][x]

    def remove_wall(self, x: int, y: int, wall: int) -> None:
        self.cell(x, y).walls &= ~wall
