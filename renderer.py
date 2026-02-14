"""Terminal-based ASCII maze renderer."""

from typing import Iterable, Tuple

from maze import Maze
from cell import RIGHT, BOTTOM

Point = Tuple[int, int]


class Colors:
    """ANSI colour escape sequences."""

    WALL = "\033[97m"
    PATH = "\033[92m"
    ENTRY = "\033[95m"
    EXIT = "\033[91m"
    FORTY_TWO = "\033[90m"
    RESET = "\033[0m"


class MazeRenderer:
    """Render a maze in the terminal with colours."""

    def __init__(self) -> None:
        """Set the default wall colour."""
        self.wall_color = Colors.WALL

    def cycle_wall_color(self) -> None:
        """Rotate to the next wall colour.

        Cycles through white, blue, yellow,
        green and red.
        """
        colors = [
            "\033[97m", "\033[94m", "\033[93m",
            "\033[92m", "\033[91m",
        ]
        idx = colors.index(self.wall_color)
        self.wall_color = colors[
            (idx + 1) % len(colors)
        ]

    def render(
        self,
        maze: Maze,
        entry: Point,
        exit_: Point,
        path: Iterable[Point] | None = None,
    ) -> None:
        """Print the maze to stdout.

        Args:
            maze: The Maze to render.
            entry: Entry cell coordinates.
            exit_: Exit cell coordinates.
            path: Optional path to highlight.
        """
        path_set = set(path) if path else set()

        print("\033[H\033[J", end="")

        wc = self.wall_color
        rst = Colors.RESET
        top_border = (
            wc + "+" + ("---+" * maze.width) + rst
        )
        print(top_border)

        for y in range(maze.height):
            top = wc + "|" + rst
            bottom = wc + "+" + rst

            for x in range(maze.width):
                cell = maze.cell(x, y)

                if (x, y) == entry:
                    body = Colors.ENTRY + " E " + rst
                elif (x, y) == exit_:
                    body = Colors.EXIT + " X " + rst
                elif (x, y) in path_set:
                    body = Colors.PATH + " · " + rst
                elif cell.walls == 0xF:
                    ft = Colors.FORTY_TWO
                    body = ft + "███" + rst
                else:
                    body = "   "
                top += body

                top += (
                    wc + "|" + rst
                    if cell.walls & RIGHT
                    else " "
                )

                has_bottom = cell.walls & BOTTOM
                wall_seg = (
                    wc + "---" + rst
                    if has_bottom
                    else "   "
                )
                corner = wc + "+" + rst
                bottom += wall_seg + corner

            print(top)
            print(bottom)
