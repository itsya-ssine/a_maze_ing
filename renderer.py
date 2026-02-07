from typing import Iterable, Tuple

from maze import Maze
from cell import TOP, RIGHT, BOTTOM, LEFT

Point = Tuple[int, int]


class Colors:
    WALL = "\033[97m"
    PATH = "\033[92m"
    ENTRY = "\033[95m"
    EXIT = "\033[91m"
    FORTY_TWO = "\033[90m"
    RESET = "\033[0m"


class MazeRenderer:
    def __init__(self) -> None:
        self.wall_color = Colors.WALL

    def cycle_wall_color(self) -> None:
        colors = [
            "\033[97m", "\033[94m", "\033[93m",
            "\033[92m", "\033[91m",
        ]
        self.wall_color = colors[
            (colors.index(self.wall_color) + 1) % len(colors)
        ]

    def render(
        self,
        maze: Maze,
        entry: Point,
        exit_: Point,
        path: Iterable[Point] | None = None,
    ) -> None:
        path_set = set(path) if path else set()

        print("\033[H\033[J", end="")

        top_border = self.wall_color + "+" + ("---+" * maze.width) + Colors.RESET
        print(top_border)

        for y in range(maze.height):
            top = self.wall_color + "|" + Colors.RESET
            bottom = self.wall_color + "+" + Colors.RESET

            for x in range(maze.width):
                cell = maze.cell(x, y)

                if (x, y) == entry:
                    top += Colors.ENTRY + " E " + Colors.RESET
                elif (x, y) == exit_:
                    top += Colors.EXIT + " X " + Colors.RESET
                elif (x, y) in path_set:
                    top += Colors.PATH + " · " + Colors.RESET
                elif cell.walls == 0xF:
                    top += Colors.FORTY_TWO + "███" + Colors.RESET
                else:
                    top += "   "

                top += (
                    self.wall_color + "|" + Colors.RESET
                    if cell.walls & RIGHT
                    else " "
                )

                wall_segment = self.wall_color + "---" + Colors.RESET if cell.walls & BOTTOM else "   "
                corner_segment = self.wall_color + "+" + Colors.RESET
                bottom += wall_segment + corner_segment

            print(top)
            print(bottom)
