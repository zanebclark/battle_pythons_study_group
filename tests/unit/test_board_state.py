import uuid

import pytest

from battle_python.BoardState import BoardState
from battle_python.GameState import GameState
from battle_python.SnakeState import SnakeState
from battle_python.api_types import (
    Coord,
    SnakeRequest,
    Game,
    Ruleset,
    Board,
)
from mocks.get_mock_board_state import get_mock_board_state
from mocks.get_mock_snake_state import get_mock_snake_state

from mocks.mock_api_types import get_mock_snake


@pytest.mark.parametrize(
    "coord, expected",
    [
        # Left Border
        (Coord(x=0, y=10), [Coord(x=1, y=10), Coord(x=0, y=9)]),
        (Coord(x=0, y=0), [Coord(x=1, y=0), Coord(x=0, y=1)]),
        # Right Border
        (Coord(x=10, y=10), [Coord(x=9, y=10), Coord(x=10, y=9)]),
        (Coord(x=10, y=0), [Coord(x=9, y=0), Coord(x=10, y=1)]),
        # Bottom Border
        (Coord(x=0, y=0), [Coord(x=0, y=1), Coord(x=1, y=0)]),
        (Coord(x=10, y=0), [Coord(x=10, y=1), Coord(x=9, y=0)]),
        # Top Border
        (Coord(x=0, y=10), [Coord(x=0, y=9), Coord(x=1, y=10)]),
        (Coord(x=10, y=10), [Coord(x=10, y=9), Coord(x=9, y=10)]),
        # Two Options
        (Coord(x=1, y=10), [Coord(x=0, y=10), Coord(x=1, y=9), Coord(x=2, y=10)]),
        # Three Options
        (
            Coord(x=1, y=9),
            [Coord(x=1, y=10), Coord(x=0, y=9), Coord(x=1, y=8), Coord(x=2, y=9)],
        ),
    ],
)
def test_board_state_get_legal_adjacent_coords(coord: Coord, expected: list[Coord]):
    board = get_mock_board_state(
        board_height=11,
        board_width=11,
    )
    legal_adjacent_coords = board.get_legal_adjacent_coords(coord=coord)
    assert sorted(legal_adjacent_coords) == sorted(expected)


@pytest.mark.parametrize(
    "board, expected",
    [
        (
            get_mock_board_state(
                snake_states=[
                    get_mock_snake_state(
                        snake_id="Left Border: Up -> Right",
                        is_self=True,
                        body_coords=[
                            Coord(x=0, y=10),
                            Coord(x=0, y=9),
                            Coord(x=0, y=8),
                        ],
                        health=100,
                    )
                ]
            ),
            [
                get_mock_snake_state(
                    snake_id="Left Border: Up -> Right",
                    is_self=True,
                    body_coords=[
                        Coord(x=1, y=10),
                        Coord(x=0, y=10),
                        Coord(x=0, y=9),
                    ],
                    health=99,
                )
            ],
        ),
        (
            get_mock_board_state(
                snake_states=[
                    get_mock_snake_state(
                        snake_id="Left Border: Down -> Right",
                        is_self=True,
                        body_coords=[
                            Coord(x=0, y=0),
                            Coord(x=0, y=1),
                            Coord(x=0, y=2),
                        ],
                        health=100,
                    )
                ]
            ),
            [
                get_mock_snake_state(
                    snake_id="Left Border: Down -> Right",
                    is_self=True,
                    body_coords=[
                        Coord(x=1, y=0),
                        Coord(x=0, y=0),
                        Coord(x=0, y=1),
                    ],
                    health=99,
                )
            ],
        ),
        (
            get_mock_board_state(
                snake_states=[
                    get_mock_snake_state(
                        snake_id="Right Border: Up -> Left",
                        is_self=True,
                        body_coords=[
                            Coord(x=10, y=10),
                            Coord(x=10, y=9),
                            Coord(x=10, y=8),
                        ],
                        health=100,
                    )
                ]
            ),
            [
                get_mock_snake_state(
                    snake_id="Right Border: Up -> Left",
                    is_self=True,
                    body_coords=[
                        Coord(x=9, y=10),
                        Coord(x=10, y=10),
                        Coord(x=10, y=9),
                    ],
                    health=99,
                )
            ],
        ),
        (
            get_mock_board_state(
                snake_states=[
                    get_mock_snake_state(
                        snake_id="Right Border: Down -> Left",
                        is_self=True,
                        body_coords=[
                            Coord(x=10, y=0),
                            Coord(x=10, y=1),
                            Coord(x=10, y=2),
                        ],
                        health=100,
                    )
                ]
            ),
            [
                get_mock_snake_state(
                    snake_id="Right Border: Down -> Left",
                    is_self=True,
                    body_coords=[
                        Coord(x=9, y=0),
                        Coord(x=10, y=0),
                        Coord(x=10, y=1),
                    ],
                    health=99,
                )
            ],
        ),
        (
            get_mock_board_state(
                snake_states=[
                    get_mock_snake_state(
                        snake_id="Bottom Border: Left -> Up",
                        is_self=True,
                        body_coords=[
                            Coord(x=0, y=0),
                            Coord(x=1, y=0),
                            Coord(x=2, y=0),
                        ],
                        health=100,
                    )
                ]
            ),
            [
                get_mock_snake_state(
                    snake_id="Bottom Border: Left -> Up",
                    is_self=True,
                    body_coords=[
                        Coord(x=0, y=1),
                        Coord(x=0, y=0),
                        Coord(x=1, y=0),
                    ],
                    health=99,
                )
            ],
        ),
        (
            get_mock_board_state(
                snake_states=[
                    get_mock_snake_state(
                        snake_id="Bottom Border: Right -> Up",
                        is_self=True,
                        body_coords=[
                            Coord(x=10, y=0),
                            Coord(x=9, y=0),
                            Coord(x=8, y=0),
                        ],
                        health=100,
                    )
                ]
            ),
            [
                get_mock_snake_state(
                    snake_id="Bottom Border: Right -> Up",
                    is_self=True,
                    body_coords=[
                        Coord(x=10, y=1),
                        Coord(x=10, y=0),
                        Coord(x=9, y=0),
                    ],
                    health=99,
                )
            ],
        ),
        (
            get_mock_board_state(
                snake_states=[
                    get_mock_snake_state(
                        snake_id="Top Border: Left -> Down",
                        is_self=True,
                        body_coords=[
                            Coord(x=0, y=10),
                            Coord(x=1, y=10),
                            Coord(x=2, y=10),
                        ],
                        health=100,
                    )
                ]
            ),
            [
                get_mock_snake_state(
                    snake_id="Top Border: Left -> Down",
                    is_self=True,
                    body_coords=[
                        Coord(x=0, y=9),
                        Coord(x=0, y=10),
                        Coord(x=1, y=10),
                    ],
                    health=99,
                )
            ],
        ),
        (
            get_mock_board_state(
                snake_states=[
                    get_mock_snake_state(
                        snake_id="TopBorder:  Right -> Down",
                        is_self=True,
                        body_coords=[
                            Coord(x=10, y=10),
                            Coord(x=9, y=10),
                            Coord(x=8, y=10),
                        ],
                        health=100,
                    )
                ]
            ),
            [
                get_mock_snake_state(
                    snake_id="TopBorder:  Right -> Down",
                    is_self=True,
                    body_coords=[
                        Coord(x=10, y=9),
                        Coord(x=10, y=10),
                        Coord(x=9, y=10),
                    ],
                    health=99,
                )
            ],
        ),
        (
            get_mock_board_state(
                snake_states=[
                    get_mock_snake_state(
                        snake_id="Two Options",
                        is_self=True,
                        body_coords=[
                            Coord(x=1, y=10),
                            Coord(x=2, y=10),
                            Coord(x=3, y=10),
                        ],
                        health=100,
                    )
                ]
            ),
            [
                get_mock_snake_state(
                    snake_id="Two Options",
                    is_self=True,
                    state_prob=float(1 / 2),
                    body_coords=[
                        Coord(x=1, y=9),
                        Coord(x=1, y=10),
                        Coord(x=2, y=10),
                    ],
                    health=99,
                ),
                get_mock_snake_state(
                    snake_id="Two Options",
                    is_self=True,
                    state_prob=float(1 / 2),
                    body_coords=[
                        Coord(x=0, y=10),
                        Coord(x=1, y=10),
                        Coord(x=2, y=10),
                    ],
                    health=99,
                ),
            ],
        ),
        (
            get_mock_board_state(
                snake_states=[
                    get_mock_snake_state(
                        snake_id="Three Options",
                        is_self=True,
                        body_coords=[
                            Coord(x=1, y=9),
                            Coord(x=2, y=9),
                            Coord(x=3, y=9),
                        ],
                        health=100,
                    )
                ]
            ),
            [
                get_mock_snake_state(
                    snake_id="Three Options",
                    is_self=True,
                    state_prob=float(1 / 3),
                    body_coords=[
                        Coord(x=1, y=8),
                        Coord(x=1, y=9),
                        Coord(x=2, y=9),
                    ],
                    health=99,
                ),
                get_mock_snake_state(
                    snake_id="Three Options",
                    is_self=True,
                    state_prob=float(1 / 3),
                    body_coords=[
                        Coord(x=0, y=9),
                        Coord(x=1, y=9),
                        Coord(x=2, y=9),
                    ],
                    health=99,
                ),
                get_mock_snake_state(
                    snake_id="Three Options",
                    is_self=True,
                    state_prob=float(1 / 3),
                    body_coords=[
                        Coord(x=1, y=10),
                        Coord(x=1, y=9),
                        Coord(x=2, y=9),
                    ],
                    health=99,
                ),
            ],
        ),
        (
            get_mock_board_state(
                snake_states=[
                    get_mock_snake_state(
                        snake_id="Ouroboros",
                        is_self=True,
                        body_coords=[
                            Coord(x=0, y=10),
                            Coord(x=0, y=9),
                            Coord(x=1, y=9),
                            Coord(x=1, y=10),
                        ],
                        health=100,
                    )
                ]
            ),
            [
                get_mock_snake_state(
                    snake_id="Ouroboros",
                    is_self=True,
                    body_coords=[
                        Coord(x=1, y=10),
                        Coord(x=0, y=10),
                        Coord(x=0, y=9),
                        Coord(x=1, y=9),
                    ],
                    health=99,
                )
            ],
        ),
    ],
)  # TODO: Test no health prob
def test_board_state_get_next_states(
    board: BoardState,
    expected: list[SnakeState],
):
    snake: SnakeState | None = None
    for potential_snake in board.snake_states:
        if potential_snake.is_self:
            snake = potential_snake
            break

    if snake is None:
        raise Exception()

    next_states = board.get_next_states(board=board)

    assert len(next_states) == len(expected)
    for next_state in next_states:
        expected_state: SnakeState | None = None
        for some_expected_state in expected:
            if (
                some_expected_state.snake_id == next_state.snake_id
                and some_expected_state.body == next_state.body
            ):
                expected_state = some_expected_state
                break

        if expected_state is None:
            raise Exception()

        assert next_state.state_prob == expected_state.state_prob
        assert next_state.health == expected_state.health
        assert next_state.body == expected_state.body
        assert next_state.head == expected_state.head
        assert next_state.length == expected_state.length
        assert next_state.prev_state == snake


def test_board_state_init():
    you = get_mock_snake(
        body_coords=[
            Coord(x=0, y=0),
            Coord(x=0, y=1),
            Coord(x=0, y=2),
        ]
    )
    snakes = [
        you,
        get_mock_snake(
            body_coords=[
                Coord(x=10, y=0),
                Coord(x=10, y=1),
                Coord(x=10, y=2),
            ]
        ),
    ]

    game = Game(
        id=str(uuid.uuid4()),
        ruleset=Ruleset(
            name="standard",
            version=str(uuid.uuid4()),
            settings={
                "foodSpawnChance": 10,
                "minimumFood": 11,
                "hazardDamagePerTurn": 12,
            },
        ),
        map=str(uuid.uuid4()),
        timeout=123,
        source="league",
    )

    board = Board(
        height=11,
        width=12,
        food=[Coord(x=1, y=1), Coord(x=10, y=10)],
        hazards=[Coord(x=10, y=1), Coord(x=2, y=10)],
        snakes=snakes,
    )

    gs = SnakeRequest(
        game=game,
        turn=12,
        board=board,
        you=you,
    )

    e_gs = GameState.from_payload(payload=gs.model_dump())

    # GameState-level assertions
    assert e_gs.current_turn == gs.turn
    assert len(e_gs.turns) == 1

    # Board-level assertions
    assert e_gs.board_height == board.height
    assert e_gs.board_width == board.width
    assert list(e_gs.turns[0].food_prob.keys()) == board.food
    assert list(e_gs.turns[0].hazard_prob.keys()) == board.hazards
    assert e_gs.turns[0].turn == gs.turn
    assert len(e_gs.snake_defs.keys()) == len(snakes)
    gs_snakes = [*e_gs.turns[0].snake_states]
    for snake in snakes:
        assert e_gs.snake_defs[snake.id].name == snake.name
        assert e_gs.snake_defs[snake.id].customizations == snake.customizations
        assert e_gs.snake_defs[snake.id].is_self == (snake.id == you.id)

        gs_snake: SnakeState | None = None
        for index, some_snake in enumerate(gs_snakes):
            if some_snake.snake_id == snake.id:
                gs_snake = gs_snakes.pop(index)
                break

        if not gs_snake:
            raise Exception(f"snake not found: {snake.id}")

        assert gs_snake.state_prob == 1
        assert gs_snake.death_prob == 0
        assert gs_snake.food_prob == 0
        assert gs_snake.murder_prob == 0
        assert gs_snake.health == snake.health
        assert gs_snake.body == snake.body
        assert gs_snake.latency == int(snake.latency)
        assert gs_snake.head == snake.head
        assert gs_snake.length == snake.length
        assert gs_snake.shout == snake.shout
        assert gs_snake.is_self == (snake.id == you.id)

    # Game-level assertions
    assert e_gs.game == gs.game


@pytest.mark.parametrize(
    "description, board, expected",
    [
        (
            "Equal length snakes. Avoidable body collision and head collision",
            get_mock_board_state(
                board_height=11,
                board_width=11,
                turn=0,
                snake_states=[
                    get_mock_snake_state(
                        is_self=True,
                        snake_id="Up -> Right",
                        body_coords=[
                            Coord(x=0, y=10),
                            Coord(x=0, y=9),
                            Coord(x=0, y=8),
                        ],
                    ),
                    get_mock_snake_state(
                        snake_id="Sidecar",
                        body_coords=[
                            Coord(x=1, y=9),
                            Coord(x=1, y=8),
                            Coord(x=1, y=7),
                        ],
                    ),
                ],
            ),
            get_mock_board_state(
                board_height=11,
                board_width=11,
                turn=1,
                snake_states=[
                    get_mock_snake_state(
                        is_self=True,
                        snake_id="Up -> Right",
                        body_coords=[
                            Coord(x=1, y=10),
                            Coord(x=0, y=10),
                            Coord(x=0, y=9),
                        ],
                    ),
                    get_mock_snake_state(
                        snake_id="Sidecar",
                        body_coords=[
                            Coord(x=2, y=9),
                            Coord(x=1, y=9),
                            Coord(x=1, y=8),
                        ],
                    ),
                ],
            ),
        ),
        # (
        #     "Different length snakes. Avoidable body collision. Allow head collision",
        #     get_mock_enriched_board(
        #         turn=0,
        #         snake_states=[
        #             get_mock_snake_state(
        #                 is_self=True,
        #                 snake_id="Up -> Right",
        #                 body_coords=[
        #                     Coord(x=0, y=10),
        #                     Coord(x=0, y=9),
        #                     Coord(x=0, y=8),
        #                 ],
        #             ),
        #             get_mock_snake_state(
        #                 snake_id="Sidecar",
        #                 body_coords=[
        #                     Coord(x=1, y=9),
        #                     Coord(x=1, y=8),
        #                     Coord(x=1, y=7),
        #                     Coord(x=1, y=6),
        #                 ],
        #             ),
        #         ],
        #     ),
        #     {
        #         "Up -> Right": {
        #             Coord(x=1, y=10): Spam(
        #                 state_prob=100, direction="right", body_index=0
        #             ),
        #             Coord(x=0, y=10): Spam(state_prob=100, body_index=1),
        #             Coord(x=0, y=9): Spam(state_prob=100, body_index=2),
        #         },
        #         "Sidecar": {
        #             Coord(x=2, y=9): Spam(
        #                 state_prob=50, direction="right", body_index=0
        #             ),
        #             Coord(x=1, y=10): Spam(
        #                 state_prob=50, direction="up", body_index=0
        #             ),
        #             Coord(x=1, y=9): Spam(state_prob=100, body_index=1),
        #             Coord(x=1, y=8): Spam(state_prob=100, body_index=2),
        #             Coord(x=1, y=7): Spam(state_prob=100, body_index=3),
        #         },
        #     },
        # ),
        # (
        #     "A ménage à trois. Equal lengths",
        #     get_mock_enriched_board(
        #         turn=0,
        #         snake_states=[
        #             get_mock_snake_state(
        #                 is_self=True,
        #                 snake_id="Up -> Right",
        #                 body_coords=[
        #                     Coord(x=0, y=10),
        #                     Coord(x=0, y=9),
        #                     Coord(x=0, y=8),
        #                 ],
        #             ),
        #             get_mock_snake_state(
        #                 snake_id="Sidecar",
        #                 body_coords=[
        #                     Coord(x=1, y=9),
        #                     Coord(x=1, y=8),
        #                     Coord(x=1, y=7),
        #                 ],
        #                 health=100,
        #             ),
        #             get_mock_snake_state(
        #                 snake_id="Up -> Left",
        #                 body_coords=[
        #                     Coord(x=2, y=10),
        #                     Coord(x=2, y=9),
        #                     Coord(x=2, y=8),
        #                 ],
        #             ),
        #         ],
        #     ),
        #     {
        #         "Up -> Right": {
        #             Coord(x=1, y=10): Spam(
        #                 state_prob=100, direction="right", body_index=0
        #             ),
        #             Coord(x=0, y=10): Spam(state_prob=100, body_index=1),
        #             Coord(x=0, y=9): Spam(state_prob=100, body_index=2),
        #         },
        #         "Sidecar": {
        #             Coord(x=1, y=10): Spam(
        #                 state_prob=100, direction="up", body_index=0
        #             ),
        #             Coord(x=1, y=9): Spam(state_prob=100, body_index=1),
        #             Coord(x=1, y=8): Spam(state_prob=100, body_index=2),
        #         },
        #         "Up -> Left": {
        #             Coord(x=3, y=10): Spam(
        #                 state_prob=100, direction="right", body_index=0
        #             ),
        #             Coord(x=2, y=10): Spam(state_prob=100, body_index=1),
        #             Coord(x=2, y=9): Spam(state_prob=100, body_index=2),
        #         },
        #     },
        # ),
        # (
        #     "A ménage à trois. Allow head collision",
        #     get_mock_enriched_board(
        #         turn=0,
        #         snake_states=[
        #             get_mock_snake_state(
        #                 is_self=True,
        #                 snake_id="Up -> Right",
        #                 body_coords=[
        #                     Coord(x=0, y=10),
        #                     Coord(x=0, y=9),
        #                     Coord(x=0, y=8),
        #                 ],
        #             ),
        #             get_mock_snake_state(
        #                 snake_id="Sidecar",
        #                 body_coords=[
        #                     Coord(x=1, y=9),
        #                     Coord(x=1, y=8),
        #                     Coord(x=1, y=7),
        #                 ],
        #             ),
        #             get_mock_snake_state(
        #                 snake_id="Up -> Left",
        #                 body_coords=[
        #                     Coord(x=2, y=10),
        #                     Coord(x=2, y=9),
        #                     Coord(x=2, y=8),
        #                     Coord(x=2, y=7),
        #                 ],
        #             ),
        #         ],
        #     ),
        #     {
        #         "Up -> Right": {
        #             Coord(x=1, y=10): Spam(
        #                 state_prob=100, direction="right", body_index=0
        #             ),
        #             Coord(x=0, y=10): Spam(state_prob=100, body_index=1),
        #             Coord(x=0, y=9): Spam(state_prob=100, body_index=2),
        #         },
        #         "Sidecar": {
        #             Coord(x=1, y=10): Spam(
        #                 state_prob=100, direction="up", body_index=0
        #             ),
        #             Coord(x=1, y=9): Spam(state_prob=100, body_index=1),
        #             Coord(x=1, y=8): Spam(state_prob=100, body_index=2),
        #         },
        #         "Up -> Left": {
        #             Coord(x=1, y=10): Spam(
        #                 state_prob=50, direction="left", body_index=0
        #             ),
        #             Coord(x=3, y=10): Spam(
        #                 state_prob=50, direction="right", body_index=0
        #             ),
        #             Coord(x=2, y=10): Spam(state_prob=100, body_index=1),
        #             Coord(x=2, y=9): Spam(state_prob=100, body_index=2),
        #             Coord(x=2, y=8): Spam(state_prob=100, body_index=3),
        #         },
        #     },
        # ),
        # (
        #     "One snake. Three options",
        #     get_mock_enriched_board(
        #         board_height=11,
        #         board_width=11,
        #         turn=0,
        #         food_prob=[Coord(x=1, y=1), Coord(x=10, y=10)],
        #         snake_states=[
        #             get_mock_snake_state(
        #                 is_self=True,
        #                 snake_id="Highlander",
        #                 body_coords=[
        #                     Coord(x=1, y=9),
        #                     Coord(x=1, y=8),
        #                     Coord(x=1, y=7),
        #                 ],
        #             ),
        #         ],
        #     ),
        #     {
        #         "Highlander": {
        #             Coord(x=1, y=10): Spam(
        #                 state_prob=float(100 / 3), direction="up", body_index=0
        #             ),
        #             Coord(x=0, y=9): Spam(
        #                 state_prob=float(100 / 3), direction="left", body_index=0
        #             ),
        #             Coord(x=2, y=9): Spam(
        #                 state_prob=float(100 / 3), direction="right", body_index=0
        #             ),
        #             Coord(x=1, y=9): Spam(state_prob=100, body_index=1),
        #             Coord(x=1, y=8): Spam(state_prob=100, body_index=2),
        #         },
        #     },
        # ),
    ],
)
def test_board_state_get_next_board(
    description: str,
    board: BoardState,
    expected: BoardState,
):
    next_board = board.get_next_board()
    assert next_board.turn == expected.turn
    assert next_board.board_height == expected.board_height
    assert next_board.board_width == expected.board_width
    assert sorted(next_board.food_prob) == sorted(expected.food_prob)
    assert sorted(next_board.hazard_prob) == sorted(expected.hazard_prob)
    assert len(next_board.snake_states) == len(expected.snake_states)
    for snake_state in next_board.snake_states:
        expected_state: SnakeState | None = None
        for some_expected_state in expected.snake_states:
            if some_expected_state.snake_id == snake_state.snake_id:
                expected_state = some_expected_state
                break

        if expected_state is None:
            raise Exception()

        assert snake_state.state_prob == expected_state.state_prob
        assert snake_state.health == expected_state.health
        assert snake_state.body == expected_state.body
        assert snake_state.head == expected_state.head
        assert snake_state.length == expected_state.length
        assert snake_state.prev_state == snake_state
