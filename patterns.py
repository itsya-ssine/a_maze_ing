"""Module to stamp the 42 pattern onto a maze."""

from maze import Maze


def apply_42_pattern(
    maze: Maze,
    entry: tuple[int, int],
    exit_pt: tuple[int, int],
) -> None:
    """Close all walls of cells forming a '42' pattern.

    Args:
        maze: The Maze instance to stamp on.
        entry: Entry coordinates.
        exit_pt: Exit coordinates.

    Raises:
        RuntimeError: If entry or exit overlaps the pattern.
    """
    cx = maze.width // 2 - 4
    cy = maze.height // 2 - 2

    pattern = [
        (0, 0), (0, 1), (0, 2),
        (1, 2),
        (2, 2), (2, 3), (2, 4),

        (4, 0), (5, 0), (6, 0),
        (6, 1), (6, 2),
        (4, 2), (5, 2),
        (4, 3), (4, 4),
        (5, 4), (6, 4),
    ]

    pattern_cells = {(cx + dx, cy + dy) for dx, dy in pattern}

    if entry in pattern_cells:
        raise RuntimeError(
            f"ENTRY {entry} lies inside the 42 pattern."
        )

    if exit_pt in pattern_cells:
        raise RuntimeError(
            f"EXIT {exit_pt} lies inside the 42 pattern."
        )

    for x, y in pattern_cells:
        if maze.inside(x, y):
            cell = maze.cell(x, y)
            cell.walls = 0xF
            cell.visited = True
