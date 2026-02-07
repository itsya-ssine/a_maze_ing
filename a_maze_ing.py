import os
import sys
from typing import NoReturn

from config import read_config
from maze import Maze
from generator import MazeGenerator
from patterns import apply_42_pattern
from renderer import MazeRenderer
from solver import shortest_path


def main() -> NoReturn:
    try:
        if len(sys.argv) != 2:
            raise RuntimeError("Usage: python3 prog.py <config_file>")

        config = read_config(sys.argv[1])

        width = config["WIDTH"]
        height = config["HEIGHT"]
        small = False

        if width < 7 or height < 5:
            small: bool = True

        entry = config["ENTRY"]
        exit_pt = config["EXIT"]

        def is_out_of_bounds(pos: tuple[int, int], w: int, h: int) -> bool:
            x, y = pos
            return x < 0 or x >= w or y < 0 or y >= h

        if is_out_of_bounds(entry, width, height):
            raise RuntimeError(f"ENTRY {entry} is out of valid range for {width}x{height} maze.")
        
        if is_out_of_bounds(exit_pt, width, height):
            raise RuntimeError(f"EXIT {exit_pt} is out of valid range for {width}x{height} maze.")
        
        renderer = MazeRenderer()
        show_path = False

        while True:
            maze = Maze(config["WIDTH"], config["HEIGHT"])
            if not small:
                apply_42_pattern(maze, entry, exit_pt)

            generator = MazeGenerator(maze)
            generator.generate_perfect(config["ENTRY"])

            path = shortest_path(maze, config["ENTRY"], config["EXIT"])

            while True:
                os.system("cls" if os.name == "nt" else "clear")
                renderer.render(
                    maze,
                    config["ENTRY"],
                    config["EXIT"],
                    path if show_path else None,
                )

                if small:
                    print("Maze too small to display 42 pattern!")

                print("A-Maze-ing")
                print("1. Re-generate a new maze")
                print("2. Show/Hide path from entry to exit")
                print("3. Rotate maze colors")
                print("4. Quit")

                try:
                    choice = input("Choice? (1-4): ").strip()
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
