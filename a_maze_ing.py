"""A-Maze-ing: maze generator and terminal visualiser."""

import os
import sys
from typing import NoReturn, Tuple, cast

from config import read_config
from maze import Maze
from generator import MazeGenerator
from patterns import apply_42_pattern
from renderer import MazeRenderer
from solver import shortest_path
from writer import write_hex_maze


def _out_of_bounds(
    pos: Tuple[int, int], w: int, h: int
) -> bool:
    """Return True if *pos* is outside the maze.

    Args:
        pos: (x, y) coordinates to check.
        w: Maze width.
        h: Maze height.

    Returns:
        True if the position is out of bounds.
    """
    x, y = pos
    return x < 0 or x >= w or y < 0 or y >= h


def main() -> NoReturn:
    """Entry point: parse config, generate and display maze."""
    try:
        if len(sys.argv) != 2:
            raise RuntimeError(
                "Usage: python3 a_maze_ing.py <config>"
            )

        config = read_config(sys.argv[1])

        width = cast(int, config["WIDTH"])
        height = cast(int, config["HEIGHT"])
        small = width < 7 or height < 5

        entry = cast(Tuple[int, int], config["ENTRY"])
        exit_pt = cast(Tuple[int, int], config["EXIT"])
        output = cast(str, config["OUTPUT_FILE"])

        if _out_of_bounds(entry, width, height):
            raise RuntimeError(
                f"ENTRY {entry} out of range "
                f"for {width}x{height} maze."
            )

        if _out_of_bounds(exit_pt, width, height):
            raise RuntimeError(
                f"EXIT {exit_pt} out of range "
                f"for {width}x{height} maze."
            )

        renderer = MazeRenderer()
        show_path = False

        while True:
            maze = Maze(width, height)
            if not small:
                apply_42_pattern(maze, entry, exit_pt)

            seed = cast(
                int, config.get("SEED")
            ) if config.get("SEED") is not None else None
            generator = MazeGenerator(maze, seed)
            if config["PERFECT"]:
                generator.generate_perfect(entry)
            else:
                generator.generate_imperfect(entry)
            generator.enforce_borders()

            path = shortest_path(maze, entry, exit_pt)

            write_hex_maze(
                maze, output, entry, exit_pt, path
            )

            while True:
                os.system(
                    "cls" if os.name == "nt"
                    else "clear"
                )
                renderer.render(
                    maze,
                    entry,
                    exit_pt,
                    path if show_path else None,
                )

                if small:
                    print(
                        "Maze too small for 42 pattern!"
                    )

                print("A-Maze-ing")
                print("1. Re-generate a new maze")
                print("2. Show/Hide path")
                print("3. Rotate wall colours")
                print("4. Quit")

                try:
                    choice = input(
                        "Choice? (1-4): "
                    ).strip()
                except KeyboardInterrupt:
                    print("\nGoodbye!")
                    sys.exit(0)

                if choice == "1":
                    break
                if choice == "2":
                    show_path = not show_path
                elif choice == "3":
                    renderer.cycle_wall_color()
                elif choice == "4":
                    sys.exit(0)

    except RuntimeError as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
