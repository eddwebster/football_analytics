"""Unittests for class soccerdata.SoFIFA."""
import pandas as pd
import pytest

from soccerdata.sofifa import SoFIFA


@pytest.mark.fails_gha
def test_read_team_ratings(sofifa_bundesliga: SoFIFA) -> None:
    assert isinstance(sofifa_bundesliga.read_team_ratings(), pd.DataFrame)


@pytest.mark.fails_gha
def test_read_player_ratings(sofifa_bundesliga: SoFIFA) -> None:
    assert isinstance(sofifa_bundesliga.read_player_ratings(player=189596), pd.DataFrame)
