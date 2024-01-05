from __future__ import annotations

from dataclasses import dataclass
from battle_python.types import (
    BattlesnakeCustomizations,
    Coord,
    MoveDirection,
)


@dataclass
class Battlesnake:
    id: str
    name: str
    health: int
    body: list[Coord]
    latency: str
    head: Coord
    length: int
    shout: str
    customizations: BattlesnakeCustomizations
    is_self: bool = False
    board_width: int = 0
    board_height: int = 0
    turn: int = 0

    def tail_will_move(self) -> bool:
        if self.turn == 0:
            return True
        return self.health != 100

    def get_moves(self) -> dict[Coord, MoveDirection]:
        return {
            Coord(self.head.x, self.head.y + 1): "up",
            Coord(self.head.x, self.head.y - 1): "down",
            Coord(self.head.x - 1, self.head.y): "left",
            Coord(self.head.x + 1, self.head.y): "right",
        }

    def get_safe_moves(self) -> dict[Coord, MoveDirection]:
        moves = self.get_moves()

        for coord in list(moves.keys()):
            if (
                coord.x < 0  # Avoid moving out of bounds
                or coord.x > self.board_width - 1  # Avoid moving out of bounds
                or coord.y < 0  # Avoid moving out of bounds
                or coord.y > self.board_height - 1  # Avoid moving out of bounds
                or coord in self.body[0:-1]  # Avoid self collision.
            ):
                del moves[coord]
                continue

            # Avoid your tail if it won't move
            if coord == self.body[-1] and not self.tail_will_move():
                del moves[coord]
                continue

        return moves

    def get_coord_prob_dict(self) -> dict[Coord, dict[str, int]]:
        coord_prob_dict: dict[Coord, dict[str, int]] = {
            coord: {} for coord in self.body
        }

        for coord in self.body:
            prob = 100
            # The tail might not be there. If the snake just ate food (health = 100), it will remain.
            # The snake's health will be at 100 at the beginning of the game, so omit that condition.
            if coord == self.body[-1]:
                if self.tail_will_move():
                    prob = 100
                else:
                    prob = 0

            coord_prob_dict[coord][self.id] = prob

        safe_moves = self.get_safe_moves()
        prob = round(100 / len(safe_moves.keys()))
        for coord in safe_moves.keys():
            pass

        return coord_prob_dict


def get_combined_coord_prob_dict(
    snakes: list[Battlesnake],
) -> dict[Coord, dict[str, int]]:
    coord_prob_dicts: list[dict[Coord, dict[str, int]]] = [
        snake.get_coord_prob_dict() for snake in snakes
    ]
    return {
        coord: prob_dict
        for coord_prob_dict in coord_prob_dicts
        for coord, prob_dict in coord_prob_dict.items()
    }