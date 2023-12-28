"""Unittests for class soccerdata.WhoScored."""
import pandas as pd
import pytest

# Unittests -------------------------------------------------------------------


@pytest.mark.fails_gha
def test_whoscored_missing_players(whoscored):
    assert isinstance(whoscored.read_missing_players(1485184), pd.DataFrame)


@pytest.mark.fails_gha
def test_whoscored_events(whoscored):
    assert isinstance(whoscored.read_events(1485184), pd.DataFrame)
