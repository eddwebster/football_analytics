"""Unittests for class soccerdata.ClubElo."""
import json
from datetime import datetime, timedelta
from importlib import reload

import pandas as pd
import pytest

from soccerdata import ClubElo
from soccerdata import _config as conf


def test_read_by_date(elo: ClubElo) -> None:
    """It should return a dataframe with the ELO ratings for all clubs at the specified date."""
    assert isinstance(elo.read_by_date(), pd.DataFrame)
    assert isinstance(elo.read_by_date('2017-04-01'), pd.DataFrame)
    assert isinstance(elo.read_by_date(datetime(2017, 4, 1)), pd.DataFrame)


def test_read_by_date_bad_params(elo: ClubElo) -> None:
    """It should raise an error if the parameters are invalid."""
    with pytest.raises(ValueError):
        elo.read_by_date('2017')
    with pytest.raises(TypeError):
        elo.read_by_date(1 / 4)  # type: ignore


def test_read_club_history(elo: ClubElo) -> None:
    """It should return a dataframe with the ELO history for the specified club."""
    assert isinstance(elo.read_team_history('Feyenoord'), pd.DataFrame)
    assert isinstance(elo.read_team_history('Feyenoord', 2), pd.DataFrame)
    assert isinstance(elo.read_team_history('Feyenoord', timedelta(days=2)), pd.DataFrame)


def test_read_club_history_max_age(elo: ClubElo) -> None:
    """It should not use cached data if it is older than max_age."""
    max_age = timedelta(milliseconds=1)
    assert isinstance(elo.read_team_history('Feyenoord', max_age), pd.DataFrame)


@pytest.mark.fails_gha
def test_read_club_history_replacement(monkeypatch, tmp_path) -> None:  # type: ignore
    """It should use the replacement names from teamname_replacements.json."""
    monkeypatch.setenv('SOCCERDATA_DIR', str(tmp_path))
    # no teamname_replacements.json
    reload(conf)
    assert not conf.TEAMNAME_REPLACEMENTS
    fp = tmp_path / "config" / "teamname_replacements.json"
    with open(fp, 'w', encoding='utf8') as outfile:
        json.dump({"Manchester City": ["Man City"]}, outfile)
    # correctly parse teamname_replacements.json
    reload(conf)
    elo = ClubElo()
    assert isinstance(elo.read_team_history('Manchester City'), pd.DataFrame)


def test_read_club_history_bad_params(elo: ClubElo) -> None:
    """It should raise an error if the parameters are invalid."""
    with pytest.raises(ValueError):
        elo.read_team_history('FC Knudde')  # no data for team
    with pytest.raises(TypeError):
        elo.read_team_history('Feyenoord', datetime.now())  # type: ignore
