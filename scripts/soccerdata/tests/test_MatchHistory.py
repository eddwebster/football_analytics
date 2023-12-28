"""Unittests for class soccerdata.MatchHistory."""

import pandas as pd

from soccerdata.match_history import MatchHistory


def test_read_games(match_epl_2y: MatchHistory) -> None:
    """It should return a DataFrame with all games from the selected leagues and seasons."""
    df = match_epl_2y.read_games()
    assert isinstance(df, pd.DataFrame)
    assert len(df.index.get_level_values("season").unique()) == 2
    assert len(df) == 760
