"""Unittests for soccerdata._common."""

import datetime

import pandas as pd
import pytest
import time_machine

import soccerdata
from soccerdata._common import (
    BaseRequestsReader,
    make_game_id,
    season_code,
    standardize_colnames,
)

# _download_and_save


def test_download_and_save_not_cached(tmp_path):
    reader = BaseRequestsReader()
    url = "http://api.clubelo.com/Barcelona"
    filepath = tmp_path / "Barcelona.csv"
    data = reader._download_and_save(url, filepath)
    assert isinstance(pd.read_csv(data), pd.DataFrame)


def test_download_and_save_cached(tmp_path):
    reader = BaseRequestsReader()
    url = "http://api.clubelo.com/Barcelona"
    filepath = tmp_path / "Barcelona.csv"
    data = reader._download_and_save(url, filepath)
    data = reader._download_and_save(url, filepath)
    assert isinstance(pd.read_csv(data), pd.DataFrame)


def test_download_and_save_no_cache(tmp_path):
    reader = BaseRequestsReader(no_cache=True)
    url = "http://api.clubelo.com/Barcelona"
    filepath = tmp_path / "Barcelona.csv"
    filepath.write_text("bogus")
    data = reader._download_and_save(url, filepath)
    assert len(pd.read_csv(data)) > 1


def test_download_and_save_no_store_no_filepath():
    reader = BaseRequestsReader(no_store=True)
    url = "http://api.clubelo.com/Barcelona"
    data = reader._download_and_save(url, filepath=None)
    assert isinstance(pd.read_csv(data), pd.DataFrame)


def test_download_and_save_no_cache_filepath(tmp_path):
    reader = BaseRequestsReader(no_store=True)
    url = "http://api.clubelo.com/Barcelona"
    filepath = tmp_path / "Barcelona.csv"
    data = reader._download_and_save(url, filepath)
    assert isinstance(pd.read_csv(data), pd.DataFrame)
    assert not filepath.exists()


# def test_download_and_save_requests_tor(tmp_path):
#     url = "https://check.torproject.org/api/ip"
#     reader = BaseRequestsReader(proxy=None)
#     ip_without_proxy = reader.get(url, tmp_path / "myip.txt")
#     ip_without_proxy = json.load(ip_without_proxy)
#     proxy_reader = BaseRequestsReader(proxy="tor")
#     ip_with_proxy = proxy_reader.get(url, tmp_path / "myproxyip.txt")
#     ip_with_proxy = json.load(ip_with_proxy)
#     assert ip_without_proxy["IP"] != ip_with_proxy["IP"]
#     assert ip_with_proxy["IsTor"]
#
#
# def test_download_and_save_selenium_tor(tmp_path):
#     url = "https://check.torproject.org/api/ip"
#     reader = BaseSeleniumReader(proxy=None).get(url, tmp_path / "myip.txt")
#     ip_without_proxy = html.parse(reader).xpath("//pre")[0].text
#     ip_without_proxy = json.loads(ip_without_proxy)
#     proxy_reader = BaseSeleniumReader(proxy="tor").get(url, tmp_path / "myproxyip.txt")
#     ip_with_proxy = html.parse(proxy_reader).xpath("//pre")[0].text
#     ip_with_proxy = json.loads(ip_with_proxy)
#     assert ip_without_proxy["IP"] != ip_with_proxy["IP"]
#     assert ip_with_proxy["IsTor"]
#

# make_game_id


def test_make_game_id():
    s = pd.Series(
        {
            "date": datetime.datetime(1993, 7, 30),
            "home_team": "Barcelona",
            "away_team": "Real Madrid",
        }
    )
    game_id = make_game_id(s)
    assert game_id == "1993-07-30 Barcelona-Real Madrid"


# standardize_colnames


def test_standardize_colnames():
    df = pd.DataFrame(
        columns=[
            "First Test",
            "SecondTest",
            "thirdTest",
            "Fourthtest",
            "Fifth-test",
            "TestSix",
        ]
    )
    df = standardize_colnames(
        df, cols=["First Test", "SecondTest", "thirdTest", "Fourthtest", "Fifth-test"]
    )
    assert df.columns.tolist() == [
        "first_test",
        "second_test",
        "third_test",
        "fourthtest",
        "fifth_test",
        "TestSix",
    ]


# is_complete


def test_is_complete():
    reader = BaseRequestsReader(no_store=True)
    with time_machine.travel(datetime.datetime(2020, 12, 25, 1, 24)):
        assert reader._is_complete("ENG-Premier League", "1920")
        assert not reader._is_complete("ENG-Premier League", "2021")
    with time_machine.travel(datetime.datetime(2021, 2, 25, 1, 24)):
        assert reader._is_complete("ENG-Premier League", "1920")
        assert not reader._is_complete("ENG-Premier League", "2021")
    with time_machine.travel(datetime.datetime(2021, 7, 1, 1, 24)):
        assert reader._is_complete("ENG-Premier League", "1920")
        assert reader._is_complete("ENG-Premier League", "2021")
        assert not reader._is_complete("ENG-Premier League", "2122")


def test_is_complete_default_value(mocker):
    mocker.patch.object(soccerdata._common, "LEAGUE_DICT", {"FAKE-Dummy League": {}})
    reader = BaseRequestsReader(no_store=True)
    with time_machine.travel(datetime.datetime(2020, 12, 25, 1, 24)):
        assert reader._is_complete("FAKE-Dummy League", "1920")


def test_is_complete_undefined_league(mocker):
    reader = BaseRequestsReader(no_store=True)
    with pytest.raises(ValueError):
        reader._is_complete("FAKE-Dummy League", "1920")


# Season codes
def test_season_pattern1a():
    assert season_code("9495") == "9495"


def test_season_pattern1a_warn():
    with pytest.warns(UserWarning) as record:
        assert season_code("2021") == "2021"

    # check that only one warning was raised
    assert len(record) == 1
    # check that the message matches
    msg = 'Season id "2021" is ambiguous: interpreting as "20-21"'
    assert record[0].message.args[0] == msg  # type: ignore


def test_season_pattern1b():
    my_season = check_post = "1998"
    assert season_code(my_season) == "9899"
    assert my_season == check_post


def test_season_pattern1c():
    assert season_code("1999") == "9900"


def test_season_pattern2():
    assert season_code("11") == "1112"
    assert season_code("99") == "9900"


def test_season_pattern3():
    assert season_code("2011-2012") == "1112"
    assert season_code("1999-2000") == "9900"


def test_season_pattern4():
    assert season_code("2011-12") == "1112"
    assert season_code("1999-00") == "9900"


def test_season_pattern5():
    assert season_code("13-14") == "1314"
