"""Integration tests for soccerdata package."""

import pandas as pd
import pytest

import soccerdata as foo

# TODO: integration tests
# Names of common leagues equal for all classes
# Number of clubs equal for all common leagues over classes
# Clubnames equal for all common leagues over classes
# Number of games equal for all common leagues/seasons over classes
# Scores per game equal for all common leagues over classes


@pytest.mark.e2e
def test_five38_vs_elo():
    """We should be able to retrieve the Elo history for all teams in these leagues."""
    league_sel = [
        'ENG-Premier League',
        'ESP-La Liga',
        'FRA-Ligue 1',
        'GER-Bundesliga',
        'ITA-Serie A',
    ]

    five38 = foo.FiveThirtyEight(leagues=league_sel, seasons='1819')
    five38_games = five38.read_games()

    elo = foo.ClubElo()
    elo_hist = pd.concat([elo.read_team_history(team) for team in set(five38_games['home_team'])])

    assert set(five38_games['home_team']) - set(elo_hist['team']) == set()
