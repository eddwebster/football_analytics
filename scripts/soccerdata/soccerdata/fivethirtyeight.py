"""Scraper for https://projects.fivethirtyeight.com/soccer-predictions."""
import itertools
import json
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

import pandas as pd

from ._common import BaseRequestsReader, make_game_id, standardize_colnames
from ._config import DATA_DIR, NOCACHE, NOSTORE, TEAMNAME_REPLACEMENTS

FIVETHIRTYEIGHT_DATA_DIR = DATA_DIR / "FiveThirtyEight"
FIVETHIRTYEIGHT_API = "https://projects.fivethirtyeight.com/soccer-predictions"


class FiveThirtyEight(BaseRequestsReader):
    """Provides pd.DataFrames from fivethirtyeight's "Club Soccer Predictions" project.

    Data will be downloaded as necessary and cached locally in
    ``~/soccerdata/data/FiveThirtyEight``.

    Original project and background info:
    https://projects.fivethirtyeight.com/soccer-predictions/ and
    https://fivethirtyeight.com/features/how-our-club-soccer-projections-work/


    Parameters
    ----------
    leagues : string or iterable, optional
        IDs of Leagues to include.
    seasons : string, int or list, optional
        Seasons to include. Supports multiple formats.
        Examples: '16-17'; 2016; '2016-17'; [14, 15, 16]
    proxy : 'tor' or dict or list(dict) or callable, optional
        Use a proxy to hide your IP address. Valid options are:
            - "tor": Uses the Tor network. Tor should be running in
              the background on port 9050.
            - dict: A dictionary with the proxy to use. The dict should be
              a mapping of supported protocols to proxy addresses. For example::

                  {
                      'http': 'http://10.10.1.10:3128',
                      'https': 'http://10.10.1.10:1080',
                  }

            - list(dict): A list of proxies to choose from. A different proxy will
              be selected from this list after failed requests, allowing rotating
              proxies.
            - callable: A function that returns a valid proxy. This function will
              be called after failed requests, allowing rotating proxies.
    no_cache : bool
        If True, will not use cached data.
    no_store : bool
        If True, will not store downloaded data.
    data_dir : Path
        Path to directory where data will be cached.
    """

    def __init__(
        self,
        leagues: Optional[Union[str, List[str]]] = None,
        seasons: Optional[Union[str, int, List]] = None,
        proxy: Optional[
            Union[str, Dict[str, str], List[Dict[str, str]], Callable[[], Dict[str, str]]]
        ] = None,
        no_cache: bool = NOCACHE,
        no_store: bool = NOSTORE,
        data_dir: Path = FIVETHIRTYEIGHT_DATA_DIR,
    ):
        """Initialize a new FiveThirtyEight reader."""
        super().__init__(
            leagues=leagues, proxy=proxy, no_cache=no_cache, no_store=no_store, data_dir=data_dir
        )
        self.seasons = seasons  # type: ignore
        self._data = {}

        url = f"{FIVETHIRTYEIGHT_API}/data.json"
        filepath = self.data_dir / "latest.json"
        reader = self.get(url, filepath)

        for k, v in json.load(reader).items():
            self._data[k] = v

    def read_leagues(self) -> pd.DataFrame:
        """Retrieve the selected leagues from the datasource.

        Returns
        -------
        pd.DataFrame
        """
        df = (
            pd.DataFrame.from_dict(self._data["leagues"])
            .rename(columns={"slug": "league", "id": "league_id"})
            .pipe(self._translate_league)
            .pipe(standardize_colnames)
            .drop(columns=["overview_column", "custom_template", "skip_cols"])
            .set_index("league")
            .loc[self._selected_leagues.keys()]
            .sort_index()
        )
        return df

    def read_games(self) -> pd.DataFrame:
        """Retrieve all games for the selected leagues.

        Returns
        -------
        pd.DataFrame
        """
        col_rename = {
            "adj_score1": "adj_score_home",
            "adj_score2": "adj_score_away",
            "chances1": "chances_home",
            "chances2": "chances_away",
            "datetime": "date",
            "moves1": "moves_home",
            "moves2": "moves_away",
            "prob1": "prob_home",
            "prob2": "prob_away",
            "probtie": "prob_tie",
            "score1": "score_home",
            "score2": "score_away",
            "team1": "home_team",
            "team1_code": "home_code",
            "team1_id": "home_id",
            "team1_sdr_id": "home_sdr_id",
            "team2": "away_team",
            "team2_code": "away_code",
            "team2_id": "away_id",
            "team2_sdr_id": "away_sdr_id",
        }

        filemask = "matches_{}_{}.csv"
        urlmask = FIVETHIRTYEIGHT_API + "/forecasts/20{}_{}_matches.json"
        data = []
        for lkey, skey in itertools.product(self._selected_leagues.values(), self.seasons):
            filepath = self.data_dir / filemask.format(lkey, skey)
            url = urlmask.format(skey[:2], lkey)
            reader = self.get(url, filepath)
            data.extend([{"league": lkey, "season": skey, **d} for d in json.load(reader)])

        df = (
            pd.DataFrame.from_dict(data)
            .rename(columns=col_rename)
            .assign(date=lambda x: pd.to_datetime(x["date"]))
            .replace(
                {
                    "home_team": TEAMNAME_REPLACEMENTS,
                    "away_team": TEAMNAME_REPLACEMENTS,
                }
            )
            .drop("id", axis=1)
            .drop("league_id", axis=1)
            .replace("None", float("nan"))
            .pipe(self._translate_league)
        )

        df = df[~df.date.isna()]
        df["game"] = df.apply(make_game_id, axis=1)
        df.set_index(["league", "season", "game"], inplace=True)
        df.sort_index(inplace=True)
        return df

    def read_forecasts(self) -> pd.DataFrame:
        """Retrieve the forecasted results for the selected leagues.

        Returns
        -------
        pd.DataFrame
        """
        filemask = "forecasts_{}_{}.csv"
        urlmask = FIVETHIRTYEIGHT_API + "/forecasts/20{}_{}_forecast.json"
        data = []
        for lkey, skey in itertools.product(self._selected_leagues.values(), self.seasons):
            filepath = self.data_dir / filemask.format(lkey, skey)
            url = urlmask.format(skey[:2], lkey)
            reader = self.get(url, filepath)

            forecasts = json.load(reader)
            for f in forecasts["forecasts"]:
                for t in f["teams"]:
                    data.append(
                        {
                            "league": lkey,
                            "season": skey,
                            "last_updated": f["last_updated"],
                            **t,
                        }
                    )
        df = (
            pd.DataFrame.from_dict(data)
            .rename(columns={"name": "team"})
            .replace({"team": TEAMNAME_REPLACEMENTS})
            .replace("None", float("nan"))
            .pipe(self._translate_league)
            .set_index(["league", "season", "last_updated", "team"])
            .sort_index()
        )
        return df

    def read_clinches(self) -> pd.DataFrame:
        """Retrieve clinches for the selected leagues.

        Returns
        -------
        pd.DataFrame
        """
        filemask = "clinches_{}_{}.csv"
        urlmask = FIVETHIRTYEIGHT_API + "/forecasts/20{}_{}_clinches.json"
        data = []
        for lkey, skey in itertools.product(self._selected_leagues.values(), self.seasons):
            filepath = self.data_dir / filemask.format(lkey, skey)
            url = urlmask.format(skey[:2], lkey)
            reader = self.get(url, filepath)
            data.extend([{"league": lkey, "season": skey, **c} for c in json.load(reader)])

        teams = (
            self.read_games()[["home_team", "home_id"]]
            .drop_duplicates()
            .rename(columns={"home_team": "team", "home_id": "team_id"})
        )
        df = (
            pd.DataFrame.from_dict(data)
            .assign(date=lambda x: pd.to_datetime(x["dt"]))
            .merge(teams, on="team_id", how="left")
            .replace({"team": TEAMNAME_REPLACEMENTS})
            .drop("dt", axis=1)
            .drop("league_id", axis=1)
            .drop("team_id", axis=1)
            .pipe(self._translate_league)
            .set_index(["league", "season", "date"])
            .sort_index()
        )
        return df
