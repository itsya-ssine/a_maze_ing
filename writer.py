"""Write the maze to a hex-encoded output file."""

from typing import List, Tuple

from maze import Maze

Point = Tuple[int, int]

_DIRECTION_LETTER = {
    (0, -1): "N",
    (1, 0): "E",
    (0, 1): "S",
    (-1, 0): "W",
}


def _path_to_directions(
    path: List[Point],
) -> str:
    """Convert a list of points to NESW direction string.

    Args:
        path: Ordered list of (x, y) coordinates.

    Returns:
        A string of N, E, S, W characters.
    """
    parts: List[str] = []
    for i in range(len(path) - 1):
        dx = path[i + 1][0] - path[i][0]
        dy = path[i + 1][1] - path[i][1]
        parts.append(_DIRECTION_LETTER[(dx, dy)])
    return "".join(parts)


def write_hex_maze(
    maze: Maze,
    path: str,
    entry: Point,
    exit_pt: Point,
    solution: List[Point],
) -> None:
    """Write maze to file in hexadecimal wall format.

    Args:
        maze: The Maze to serialise.
        path: Output file path.
        entry: Entry cell coordinates.
        exit_pt: Exit cell coordinates.
        solution: Shortest path as a list of points.

    Raises:
        RuntimeError: If the file cannot be written.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            for row in maze.grid:
                line = " ".join(
                    f"{cell.walls:X}" for cell in row
                )
                f.write(line + "\n")
            f.write("\n")
            f.write(
                f"{entry[0]},{entry[1]}\n"
            )
            f.write(
                f"{exit_pt[0]},{exit_pt[1]}\n"
            )
            f.write(
                _path_to_directions(solution) + "\n"
            )
    except OSError as exc:
        raise RuntimeError(
            f"Cannot write maze file: {exc}"
        ) from exc
