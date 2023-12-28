"""Pytest fixtures for soccerdata package."""

import pytest

import soccerdata as foo


@pytest.fixture
def five38():
    """Return a correctly initialized instance of FiveThirtyEight."""
    return foo.FiveThirtyEight(seasons="20-21")


@pytest.fixture
def five38_laliga():
    """Return a correctly initialized instance of FiveThirtyEight filtered by league: La Liga."""
    return foo.FiveThirtyEight("ESP-La Liga", "20-21")


@pytest.fixture
def espn_seriea():
    """Return a correctly initialized instance of ESPN filtered by league: Serie A."""
    return foo.ESPN("ITA-Serie A", "20-21")


@pytest.fixture
def sofifa_bundesliga():
    """Return a correctly initialized instance of SoFIFA filtered by league: Bundesliga."""
    return foo.SoFIFA("GER-Bundesliga", versions=[230012])


@pytest.fixture
def fbref_ligue1():
    """Return a correctly initialized instance of FBref filtered by league: Ligue 1."""
    return foo.FBref("FRA-Ligue 1", "20-21")


@pytest.fixture
def elo():
    """Return a correctly initialized ClubElo instance."""
    return foo.ClubElo()


@pytest.fixture
def match_epl_2y():
    """Return a MatchHistory instance for the last 2 years of the EPL."""
    return foo.MatchHistory("ENG-Premier League", list(range(2018, 2020)))


@pytest.fixture
def whoscored():
    """Return a correctly initialized instance of WhoScored."""
    return foo.WhoScored("ENG-Premier League", "20-21")
