from maze import Maze


def write_hex_maze(maze: Maze, path: str) -> None:
    try:
        with open(path, "w", encoding="utf-8") as file:
            for row in maze.grid:
                line = " ".join(f"{cell.walls:X}" for cell in row)
                file.write(line + "\n")
    except OSError as exc:
        raise RuntimeError(f"Cannot write maze file: {exc}") from exc
