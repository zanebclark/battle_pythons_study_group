import json
import os
from unittest import mock

import pytest

from battle_python import api
from tests.mocks.mock_api_types import (
    get_mock_battlesnake,
    get_mock_gamestate,
)
from ..mocks.MockLambdaContext import MockLambdaContext
from ..mocks.api_gateway_event import get_mock_api_gateway_event
from aws_lambda_powertools.utilities.typing import LambdaContext


@pytest.fixture()
def lambda_context() -> LambdaContext:
    return MockLambdaContext()  # type: ignore


def test_populated_battlesnake_details(lambda_context):
    env_vars = {
        "BATTLESNAKE_AUTHOR": "testauthor",
        "BATTLESNAKE_COLOR": "#888888",
        "BATTLESNAKE_HEAD": "all-seeing",
        "BATTLESNAKE_TAIL": "curled",
        "BATTLESNAKE_VERSION": "testversion",
    }
    with mock.patch.dict(os.environ, env_vars, clear=True):
        apigw_event = get_mock_api_gateway_event(method="GET", path="/")
        response = api.lambda_handler(event=apigw_event, context=lambda_context)  # type: ignore
        data = json.loads(response["body"])

        assert response["statusCode"] == 200
        assert data["apiversion"] == "1"
        assert (
            data["author"] == env_vars["BATTLESNAKE_AUTHOR"]
        )  # TODO: Do I need to assert that none of the values are null?
        assert data["color"] == env_vars["BATTLESNAKE_COLOR"]
        assert data["head"] == env_vars["BATTLESNAKE_HEAD"]
        assert data["tail"] == env_vars["BATTLESNAKE_TAIL"]
        assert data["version"] == env_vars["BATTLESNAKE_VERSION"]


def test_game_started(lambda_context):
    body = get_mock_gamestate(
        turn=0,
        food_coords=[(1, 1), (10, 10)],
        snakes=[
            get_mock_battlesnake(is_self=True, body_coords=[(0, 0), (0, 1), (0, 2)]),
        ],
    )
    apigw_event = get_mock_api_gateway_event(method="POST", path="/start", body=body)
    response = api.lambda_handler(event=apigw_event, context=lambda_context)  # type: ignore
    assert response["statusCode"] == 200


def test_move(lambda_context):
    body = get_mock_gamestate(
        turn=100,
        food_coords=[(1, 1), (10, 10)],
        snakes=[
            get_mock_battlesnake(is_self=True, body_coords=[(0, 0), (0, 1), (0, 2)]),
        ],
    )
    apigw_event = get_mock_api_gateway_event(method="POST", path="/move", body=body)
    response = api.lambda_handler(event=apigw_event, context=lambda_context)  # type: ignore
    assert response["statusCode"] == 200


def test_end(lambda_context):
    body = get_mock_gamestate(
        turn=200,
        food_coords=[(1, 1), (10, 10)],
        snakes=[
            get_mock_battlesnake(is_self=True, body_coords=[(0, 0), (0, 1), (0, 2)]),
        ],
    )
    apigw_event = get_mock_api_gateway_event(method="POST", path="/end", body=body)
    response = api.lambda_handler(event=apigw_event, context=lambda_context)  # type: ignore
    assert response["statusCode"] == 200
