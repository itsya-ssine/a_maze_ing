"""Cell module defining the Cell dataclass and wall constants."""

from dataclasses import dataclass


TOP: int = 1
RIGHT: int = 2
BOTTOM: int = 4
LEFT: int = 8


@dataclass
class Cell:
    """Represent a single maze cell with walls and visited state."""

    walls: int = TOP | RIGHT | BOTTOM | LEFT
    visited: bool = False
