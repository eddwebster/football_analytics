"""Unittests for class soccerdata.FiveThirtyEight."""

import pandas as pd
import pytest

from soccerdata.fivethirtyeight import FiveThirtyEight


def test_read_leagues(five38_laliga: FiveThirtyEight) -> None:
    df = five38_laliga.read_leagues()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.loc['ESP-La Liga', 'long_name'] == 'La Liga'


def test_read_games(five38_laliga: FiveThirtyEight) -> None:
    assert isinstance(five38_laliga.read_games(), pd.DataFrame)


def test_read_forecasts(five38_laliga: FiveThirtyEight) -> None:
    assert isinstance(five38_laliga.read_forecasts(), pd.DataFrame)


def test_read_clinches(five38_laliga: FiveThirtyEight) -> None:
    assert isinstance(five38_laliga.read_clinches(), pd.DataFrame)


def test_filter_leagues(five38: FiveThirtyEight) -> None:
    assert len(five38._selected_leagues) == len(five38.read_leagues())
    assert set(five38._selected_leagues) == set(five38.read_games().reset_index()['league'])
    assert set(five38._selected_leagues) == set(five38.read_forecasts().reset_index()['league'])
    assert set(five38._selected_leagues) == set(five38.read_clinches().reset_index()['league'])


def test_init_league_value_error() -> None:
    with pytest.raises(ValueError):
        FiveThirtyEight('xxx')


def test_init_league_type_error() -> None:
    with pytest.raises(TypeError):
        FiveThirtyEight(1)  # type: ignore
