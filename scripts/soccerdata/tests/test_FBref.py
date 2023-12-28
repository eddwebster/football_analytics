"""Unittests for class soccerdata.FBref."""
import pandas as pd
import pytest

import soccerdata as sd
from soccerdata.fbref import FBref, _concat


@pytest.mark.parametrize(
    "stat_type",
    [
        "standard",
        "keeper",
        "keeper_adv",
        "shooting",
        "passing",
        "passing_types",
        "goal_shot_creation",
        "defense",
        "possession",
        "playing_time",
        "misc",
    ],
)
def test_read_team_season_stats(fbref_ligue1: FBref, stat_type: str) -> None:
    assert isinstance(fbref_ligue1.read_team_season_stats(stat_type), pd.DataFrame)


@pytest.mark.parametrize(
    "stat_type",
    [
        "schedule",
        "shooting",
        "keeper",
        "passing",
        "passing_types",
        "goal_shot_creation",
        "defense",
        "possession",
        "misc",
    ],
)
def test_read_team_match_stats(fbref_ligue1: FBref, stat_type: str) -> None:
    assert isinstance(fbref_ligue1.read_team_match_stats(stat_type), pd.DataFrame)


@pytest.mark.parametrize(
    "stat_type",
    [
        "standard",
        "shooting",
        "passing",
        "passing_types",
        "goal_shot_creation",
        "defense",
        "possession",
        "playing_time",
        "misc",
        "keeper",
        "keeper_adv",
    ],
)
def test_read_player_season_stats(fbref_ligue1: FBref, stat_type: str) -> None:
    assert isinstance(fbref_ligue1.read_player_season_stats(stat_type), pd.DataFrame)


def test_read_schedule(fbref_ligue1: FBref) -> None:
    assert isinstance(fbref_ligue1.read_schedule(), pd.DataFrame)


@pytest.mark.parametrize(
    "stat_type",
    [
        "summary",
        "keepers",
        "passing",
        "passing_types",
        "defense",
        "possession",
        "misc",
    ],
)
def test_read_player_match_stats(fbref_ligue1: FBref, stat_type: str) -> None:
    assert isinstance(
        fbref_ligue1.read_player_match_stats(stat_type, match_id="796787da"), pd.DataFrame
    )


def test_read_events(fbref_ligue1: FBref) -> None:
    assert isinstance(fbref_ligue1.read_events(match_id="796787da"), pd.DataFrame)


def test_read_shot_events(fbref_ligue1: FBref) -> None:
    assert isinstance(fbref_ligue1.read_shot_events(match_id="796787da"), pd.DataFrame)


def test_read_lineup(fbref_ligue1: FBref) -> None:
    assert isinstance(fbref_ligue1.read_lineup(match_id="796787da"), pd.DataFrame)


def test_concat() -> None:
    df1 = pd.DataFrame(
        columns=pd.MultiIndex.from_tuples(
            [("Unnamed: a", "player"), ("Performance", "Goals"), ("Performance", "Assists")]
        )
    )
    df2 = pd.DataFrame(
        columns=pd.MultiIndex.from_tuples(
            [("Unnamed: a", "player"), ("Unnamed: b", "Goals"), ("Performance", "Assists")]
        )
    )
    df3 = pd.DataFrame(
        columns=pd.MultiIndex.from_tuples(
            [("Unnamed: a", "player"), ("Goals", "Unnamed: b"), ("Performance", "Assists")]
        )
    )
    res = _concat([df1, df2, df3], key=["player"])
    assert res.columns.equals(
        pd.MultiIndex.from_tuples(
            [("player", ""), ("Performance", "Goals"), ("Performance", "Assists")]
        )
    )
    res = _concat([df3, df1, df2], key=["player"])
    assert res.columns.equals(
        pd.MultiIndex.from_tuples(
            [("player", ""), ("Performance", "Goals"), ("Performance", "Assists")]
        )
    )


def test_concat_with_forfeited_game() -> None:
    fbref_seriea = sd.FBref(["ITA-Serie A"], 2021)
    df_1 = fbref_seriea.read_player_match_stats(match_id=["e0a20cfe", "34e95e35"])
    df_2 = fbref_seriea.read_player_match_stats(match_id=["e0a20cfe", "a3e10e13"])
    assert isinstance(df_1, pd.DataFrame)
    assert isinstance(df_2, pd.DataFrame)
    # Regardless of the order in which the matches are read, the result should be the same.
    assert df_1.columns.equals(df_2.columns)


def test_combine_big5() -> None:
    fbref_bigfive = sd.FBref(["Big 5 European Leagues Combined"], 2021)
    assert len(fbref_bigfive.read_leagues(split_up_big5=False)) == 1
    assert len(fbref_bigfive.read_seasons(split_up_big5=False)) == 1
    assert len(fbref_bigfive.read_leagues(split_up_big5=True)) == 5
    assert len(fbref_bigfive.read_seasons(split_up_big5=True)) == 5
    # by default, split_up_big5 should be False
    assert len(fbref_bigfive.read_leagues()) == 1
    assert len(fbref_bigfive.read_seasons()) == 1


@pytest.mark.parametrize(
    "stat_type",
    [
        "standard",
        "keeper",
        # "keeper_adv",  disabled because of inconsistent data on FBref
        "shooting",
        "passing",
        "passing_types",
        "goal_shot_creation",
        "defense",
        "possession",
        "playing_time",
        "misc",
    ],
)
def test_combine_big5_team_season_stats(fbref_ligue1: FBref, stat_type: str) -> None:
    fbref_bigfive = sd.FBref(["Big 5 European Leagues Combined"], 2021)
    ligue1 = fbref_ligue1.read_team_season_stats(stat_type).loc["FRA-Ligue 1"].reset_index()
    bigfive = fbref_bigfive.read_team_season_stats(stat_type).loc["FRA-Ligue 1"].reset_index()
    cols = _concat([ligue1, bigfive], key=["season"]).columns
    ligue1.columns = cols
    bigfive.columns = cols
    pd.testing.assert_frame_equal(
        ligue1,
        bigfive,
    )


@pytest.mark.parametrize(
    "stat_type",
    [
        "standard",
        "shooting",
        "passing",
        "passing_types",
        "goal_shot_creation",
        "defense",
        "possession",
        "playing_time",
        "misc",
        "keeper",
        "keeper_adv",
    ],
)
def test_combine_big5_player_season_stats(fbref_ligue1: FBref, stat_type: str) -> None:
    fbref_bigfive = sd.FBref(["Big 5 European Leagues Combined"], 2021)
    ligue1 = fbref_ligue1.read_player_season_stats(stat_type).loc["FRA-Ligue 1"].reset_index()
    bigfive = fbref_bigfive.read_player_season_stats(stat_type).loc["FRA-Ligue 1"].reset_index()
    cols = _concat([ligue1, bigfive], key=["season"]).columns
    ligue1.columns = cols
    bigfive.columns = cols
    pd.testing.assert_frame_equal(
        ligue1,
        bigfive,
    )
