"""BFS solver to find the shortest path through a maze."""

from collections import deque
from typing import Dict, List, Tuple

from maze import Maze
from cell import TOP, RIGHT, BOTTOM, LEFT

Point = Tuple[int, int]


def shortest_path(
    maze: Maze, start: Point, end: Point
) -> List[Point]:
    """Return the shortest path from start to end.

    Args:
        maze: The Maze to solve.
        start: Starting cell coordinates.
        end: Target cell coordinates.

    Returns:
        Ordered list of (x, y) points on the path.
    """
    queue: deque[Point] = deque([start])
    came_from: Dict[Point, Point | None] = {
        start: None
    }

    while queue:
        x, y = queue.popleft()

        if (x, y) == end:
            break

        cell = maze.cell(x, y)
        for dx, dy, wall in (
            (0, -1, TOP),
            (1, 0, RIGHT),
            (0, 1, BOTTOM),
            (-1, 0, LEFT),
        ):
            nx, ny = x + dx, y + dy
            if not maze.inside(nx, ny):
                continue
            if cell.walls & wall:
                continue
            if (nx, ny) not in came_from:
                came_from[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    path: List[Point] = []
    cur: Point | None = end
    while cur:
        path.append(cur)
        cur = came_from.get(cur)
    path.reverse()

    return path
