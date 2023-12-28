"""Scraper for http://sofifa.com."""
import re
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

import pandas as pd
from lxml import html

from ._common import BaseRequestsReader, standardize_colnames
from ._config import DATA_DIR, NOCACHE, NOSTORE, TEAMNAME_REPLACEMENTS

SO_FIFA_DATADIR = DATA_DIR / "SoFIFA"
SO_FIFA_API = "https://sofifa.com"


class SoFIFA(BaseRequestsReader):
    """Provides pd.DataFrames from data at http://sofifa.com.

    Data will be downloaded as necessary and cached locally in
    ``~/soccerdata/data/SoFIFA``.

    Parameters
    ----------
    leagues : string or iterable, optional
        IDs of leagues to include.
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
        data_dir: Path = SO_FIFA_DATADIR,
    ):
        """Initialize SoFIFA reader."""
        super().__init__(
            leagues=leagues,
            proxy=proxy,
            no_cache=no_cache,
            no_store=no_store,
            data_dir=data_dir,
        )
        self.rate_limit = 2
        self.seasons = seasons  # type: ignore

    def read_leagues(self) -> pd.DataFrame:
        """Retrieve selected leagues from the datasource.

        Returns
        -------
        pd.DataFrame
        """
        # read html page (overview)
        filepath = self.data_dir / "leagues.html"
        reader = self.get(SO_FIFA_API, filepath)

        # extract league links
        leagues = []
        tree = html.parse(reader)
        for node in tree.xpath("//select[@id='choices-lg']/optgroup/option"):
            leagues.append(
                {
                    "league_id": int(node.get("value")),
                    "league": node.text,
                }
            )
        df = pd.DataFrame(leagues).pipe(self._translate_league).set_index("league").sort_index()
        return df[df.index.isin(self._selected_leagues.keys())]

    def read_teams(self) -> pd.DataFrame:
        """Retrieve teams from the datasource for the selected leagues.

        Returns
        -------
        pd.DataFrame
        """
        # build url
        urlmask = SO_FIFA_API + "/teams?lg={}&v={}"
        filemask = "teams_{}_{}.html"

        # get league IDs
        leagues = self.read_leagues()

        # collect teams
        teams = []
        for lkey, _ in self._selected_leagues.items():
            league_id = leagues.at[lkey, "league_id"]
            for skey in self.seasons:
                # read html page (league overview)
                season_id = skey[:2]
                filepath = self.data_dir / filemask.format(lkey, skey)
                url = urlmask.format(league_id, season_id)
                reader = self.get(url, filepath)

                # extract team links
                tree = html.parse(reader)
                pat_team = re.compile(r"\/team\/(\d+)\/[\w-]+\/")
                for node in tree.xpath("//a[contains(@href,'/team/')]"):
                    # extract team IDs from links
                    teams.append(
                        {
                            "team_id": int(
                                re.search(pat_team, node.get("href")).group(1)  # type: ignore
                            ),
                            "team": node.xpath(".//div")[0].text,
                            "league": lkey,
                            "season": skey,
                        }
                    )

        # return data frame
        df = (
            pd.DataFrame(teams)
            .replace({"team": TEAMNAME_REPLACEMENTS})
            .set_index(["league", "season", "team"])
            .sort_index()
        )
        return df

    def read_players(self) -> pd.DataFrame:
        """Retrieve players from the datasource for the selected leagues.

        Returns
        -------
        pd.DataFrame
        """
        # build url
        urlmask = SO_FIFA_API + "/team/{}?v={}"
        filemask = str(self.data_dir / "players_{}_{}.html")

        # get team IDs
        teams = self.read_teams().reset_index()

        # collect players
        players = []
        for _, team in teams.iterrows():
            season_id = team.season[:2]
            team_name = team.team
            # read html page (team overview)
            filepath = self.data_dir / filemask.format(team_name, season_id)
            url = urlmask.format(team["team_id"], season_id)
            reader = self.get(url, filepath)

            # extract player links
            tree = html.parse(reader)
            pat_player = re.compile(r"\/player\/(\d+)\/[\w-]+\/")
            for node in tree.xpath("//a[contains(@href,'/player/') and @title]"):
                # extract player IDs from links
                # extract player names from links
                players.append(
                    {
                        "player_id": int(
                            re.search(pat_player, node.get("href")).group(1)  # type: ignore
                        ),
                        "player": node.get("title"),
                        "team": team_name,
                        "league": team.league,
                        "season": team.season,
                    }
                )

        # return data frame
        df = pd.DataFrame(players).set_index(["league", "season", "team", "player"]).sort_index()
        return df

    def read_ratings(self) -> pd.DataFrame:
        """Retrieve ratings from the datasource for the selected leagues.

        Returns
        -------
        pd.DataFrame
        """
        # build url
        urlmask = SO_FIFA_API + "/player/{}?v={}"
        filemask = "player_{}_{}.html"

        # get player IDs
        players = self.read_players().reset_index()

        # prepare empty data frame
        ratings = []

        # define labels to use for score extraction from player profile pages
        score_labels = [
            "Overall Rating",
            "Potential",
            "Crossing",
            "Finishing",
            "Heading Accuracy",
            "Short Passing",
            "Volleys",
            "Dribbling",
            "Curve",
            "FK Accuracy",
            "Long Passing",
            "Ball Control",
            "Acceleration",
            "Sprint Speed",
            "Agility",
            "Reactions",
            "Balance",
            "Shot Power",
            "Jumping",
            "Stamina",
            "Strength",
            "Long Shots",
            "Aggression",
            "Interceptions",
            "Positioning",
            "Vision",
            "Penalties",
            "Composure",
            "Marking",
            "Standing Tackle",
            "Sliding Tackle",
            "GK Diving",
            "GK Handling",
            "GK Kicking",
            "GK Positioning",
            "GK Reflexes",
        ]

        for _, player in players.iterrows():
            # read html page (player overview)
            player_name = player.player
            filepath = self.data_dir / filemask.format(player_name, player.season)
            url = urlmask.format(player["player_id"], player.season[:2])
            reader = self.get(url, filepath)

            # extract scores one-by-one
            tree = html.parse(reader)
            scores = {
                "player": player_name,
                "league": player.league,
                "season": player.season,
            }
            for s in score_labels:
                nodes = tree.xpath(
                    "(//li[not(self::script)] | //div)"
                    f"[.//text()[contains(.,'{s}')]]"
                    "/span[contains(@class, 'tag')]"
                )
                # for multiple matches, only accept first match
                if len(nodes) >= 1:
                    scores[s] = nodes[0].text.strip()
                # if there's no match, put NA
                else:
                    scores[s] = None
            ratings.append(scores)
        # return data frame
        df = (
            pd.DataFrame(ratings)
            .pipe(standardize_colnames)
            .set_index(["league", "season", "player"])
            .sort_index()
        )
        return df
