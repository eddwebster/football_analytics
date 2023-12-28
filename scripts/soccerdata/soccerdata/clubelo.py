"""Scraper for api.clubelo.com."""
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

import pandas as pd
from unidecode import unidecode

from ._common import BaseRequestsReader, standardize_colnames
from ._config import DATA_DIR, NOCACHE, NOSTORE, TEAMNAME_REPLACEMENTS

CLUB_ELO_DATADIR = DATA_DIR / "ClubElo"
CLUB_ELO_API = "http://api.clubelo.com"


class ClubElo(BaseRequestsReader):
    """Provides pd.DataFrames from CSV API at http://api.clubelo.com.

    Data will be downloaded as necessary and cached locally in
    ``~/soccerdata/data/ClubElo``.

    Since the source does not provide league names, this class will not filter
    by league. League names will be inserted from the other sources where
    available. Leagues that are only covered by clubelo.com will have NaN
    values.

    Parameters
    ----------
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
        proxy: Optional[
            Union[str, Dict[str, str], List[Dict[str, str]], Callable[[], Dict[str, str]]]
        ] = None,
        no_cache: bool = NOCACHE,
        no_store: bool = NOSTORE,
        data_dir: Path = CLUB_ELO_DATADIR,
    ):
        """Initialize a new ClubElo reader."""
        super().__init__(no_cache=no_cache, no_store=no_store, data_dir=data_dir)

    def read_by_date(self, date: Optional[Union[str, datetime]] = None) -> pd.DataFrame:
        """Retrieve ELO scores for all teams at specified date.

        Elo scores are available as early as 1939. Values before 1960 should
        be considered provisional.

        Parameters
        ----------
        date : datetime object or string like 'YYYY-MM-DD'
            Date for which to retrieve ELO scores. If no date is specified,
            get today's scores.

        Returns
        -------
        pd.DataFrame
        """
        if not date:
            date = datetime.today()
        elif isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d")
        else:
            pass  # Assume datetime object

        datestring = date.strftime("%Y-%m-%d")
        filepath = self.data_dir / f"{datestring}.csv"
        url = f"{CLUB_ELO_API}/{datestring}"

        data = self.get(url, filepath)

        df = (
            pd.read_csv(
                data, parse_dates=["From", "To"], infer_datetime_format=True, dayfirst=False
            )
            .pipe(standardize_colnames)
            .rename(columns={"club": "team"})
            .replace({"team": TEAMNAME_REPLACEMENTS})
            .replace("None", float("nan"))
            .assign(rank=lambda x: x["rank"].astype("float"))
            .assign(league=lambda x: x["country"] + "_" + x["level"].astype(str))
            .pipe(self._translate_league)
            .reset_index(drop=True)
            .set_index("team")
        )
        return df

    def read_team_history(
        self, team: str, max_age: Union[int, timedelta] = 1
    ) -> Optional[pd.DataFrame]:
        """Retrieve full ELO history for one club.

        For the exact spelling of a club's name, check the result
        of :func:`~soccerdata.ClubElo.read_by_date` or
        `clubelo.com <http://clubelo.com/Ranking>`__. You can also use
        alternative team names specified in `teamname_replacements.json`.
        Values before 1960 should be considered provisional.

        Parameters
        ----------
        team : str
            The club's name
        max_age : int for age in days, or timedelta object
            The max. age of locally cached file before re-download.

        Raises
        ------
        TypeError
            If max_age is not an integer or timedelta object.
        ValueError
            If no ratings for the given team are available.

        Returns
        -------
        pd.DataFrame
        """
        teams_to_check = [k for k, v in TEAMNAME_REPLACEMENTS.items() if v == team]
        teams_to_check.append(team)

        for i, _ in enumerate(teams_to_check):
            teams_to_check[i] = unidecode(teams_to_check[i])
            teams_to_check[i] = re.sub(r"[\s']", "", teams_to_check[i])

        for _team in teams_to_check:
            filepath = self.data_dir / f"{_team}.csv"
            url = f"{CLUB_ELO_API}/{_team}"
            data = self.get(url, filepath, max_age)

            df = (
                pd.read_csv(
                    data,
                    parse_dates=["From", "To"],
                    infer_datetime_format=True,
                    dayfirst=False,
                )
                .pipe(standardize_colnames)
                .rename(columns={"club": "team"})
                .replace("None", float("nan"))
                .assign(rank=lambda x: x["rank"].astype("float"))
                .set_index("from")
                .sort_index()
            )

            if len(df) > 0:
                # clubelo.com returns a CSV with just a header for nonexistent club
                df.replace({"team": TEAMNAME_REPLACEMENTS}, inplace=True)
                return df

        raise ValueError(f"No data found for team {team}")
