"""Scraper for http://fbref.com."""
import itertools
import warnings
from datetime import date, datetime
from functools import reduce
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

import pandas as pd
from lxml import etree, html

from ._common import (
    BaseRequestsReader,
    make_game_id,
    season_code,
    standardize_colnames,
)
from ._config import DATA_DIR, NOCACHE, NOSTORE, TEAMNAME_REPLACEMENTS, logger

FBREF_DATADIR = DATA_DIR / "FBref"
FBREF_API = "https://fbref.com"

BIG_FIVE_DICT = {
    "Serie A": "ITA-Serie A",
    "Ligue 1": "FRA-Ligue 1",
    "La Liga": "ESP-La Liga",
    "Premier League": "ENG-Premier League",
    "Bundesliga": "GER-Bundesliga",
}


class FBref(BaseRequestsReader):
    """Provides pd.DataFrames from data at http://fbref.com.

    Data will be downloaded as necessary and cached locally in
    ``~/soccerdata/data/FBref``.

    Parameters
    ----------
    leagues : string or iterable, optional
        IDs of leagues to include. For efficiently reading data from the Top-5
        European leagues, use "Big 5 European Leagues Combined".
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
        data_dir: Path = FBREF_DATADIR,
    ):
        """Initialize FBref reader."""
        super().__init__(
            leagues=leagues,
            proxy=proxy,
            no_cache=no_cache,
            no_store=no_store,
            data_dir=data_dir,
        )
        self.rate_limit = 3
        self.seasons = seasons  # type: ignore
        # check if all top 5 leagues are selected
        if set(BIG_FIVE_DICT.values()).issubset(self.leagues):
            warnings.warn(
                "You are trying to scrape data for all of the Big 5 European leagues. "
                "This can be done more efficiently by setting "
                "leagues='Big 5 European Leagues Combined'.",
                stacklevel=1,
            )

    @property
    def leagues(self) -> List[str]:
        """Return a list of selected leagues."""
        selected_leagues = set(self._leagues_dict.keys())
        if "Big 5 European Leagues Combined" in selected_leagues:
            selected_leagues -= set(BIG_FIVE_DICT.values())
        return list(selected_leagues)

    @classmethod
    def _all_leagues(cls) -> Dict[str, str]:
        """Return a dict mapping all canonical league IDs to source league IDs."""
        res = super()._all_leagues()
        res.update({"Big 5 European Leagues Combined": "Big 5 European Leagues Combined"})
        return res

    def _is_complete(self, league: str, season: str) -> bool:
        """Check if a season is complete."""
        if league == "Big 5 European Leagues Combined":
            season_ends = date(datetime.strptime(season[-2:], "%y").year, 7, 1)
            return date.today() >= season_ends
        return super()._is_complete(league, season)

    def read_leagues(self) -> pd.DataFrame:
        """Retrieve selected leagues from the datasource.

        Returns
        -------
        pd.DataFrame
        """
        url = f"{FBREF_API}/en/comps/"
        filepath = self.data_dir / "leagues.html"
        reader = self.get(url, filepath)

        # extract league links
        leagues = []
        tree = html.parse(reader)
        for table in tree.xpath("//table[contains(@id, 'comps')]"):
            df_table = pd.read_html(etree.tostring(table, method="html"))[0]
            df_table["url"] = table.xpath(".//th[@data-stat='league_name']/a/@href")
            leagues.append(df_table)
        df = (
            pd.concat(leagues)
            .pipe(standardize_colnames)
            .rename(columns={"competition_name": "league"})
            .pipe(self._translate_league)
            .drop_duplicates(subset="league")
            .set_index("league")
            .sort_index()
        )
        df["first_season"] = df["first_season"].apply(season_code)
        df["last_season"] = df["last_season"].apply(season_code)
        df["country"] = df["country"].apply(
            lambda x: x.split(" ")[1] if isinstance(x, str) else None
        )
        return df[df.index.isin(self.leagues)]

    def read_seasons(self) -> pd.DataFrame:
        """Retrieve the selected seasons for the selected leagues.

        Returns
        -------
        pd.DataFrame
        """
        filemask = "seasons_{}.html"
        df_leagues = self.read_leagues()

        seasons = []
        for lkey, league in df_leagues.iterrows():
            url = FBREF_API + league.url
            filepath = self.data_dir / filemask.format(lkey)
            reader = self.get(url, filepath)

            # extract season links
            tree = html.parse(reader)
            df_table = pd.read_html(etree.tostring(tree), attrs={"id": "seasons"})[0]
            df_table["url"] = tree.xpath(
                "//table[@id='seasons']//th[@data-stat='year_id' or @data-stat='year']/a/@href"
            )
            # Override the competition name or add if missing
            df_table["Competition Name"] = lkey
            # Some tournaments have a "year" column instead of "season"
            if "Year" in df_table.columns:
                df_table.rename(columns={"Year": "Season"}, inplace=True)
            # Get the competition format
            if "Final" in df_table.columns:
                df_table["Format"] = "elimination"
            else:
                df_table["Format"] = "round-robin"
            seasons.append(df_table)

        df = pd.concat(seasons).pipe(standardize_colnames)
        df = df.rename(columns={"competition_name": "league"})
        df["season"] = df["season"].apply(season_code)
        # if both a 20xx and 19xx season are available, drop the 19xx season
        df.drop_duplicates(subset=["league", "season"], keep="first", inplace=True)
        df = df.set_index(["league", "season"]).sort_index()
        return df.loc[
            df.index.isin(itertools.product(self.leagues, self.seasons)), ["format", "url"]
        ]

    def read_team_season_stats(  # noqa: C901
        self, stat_type: str = "standard", opponent_stats: bool = False
    ) -> pd.DataFrame:
        """Retrieve teams from the datasource for the selected leagues.

        The following stat types are available:
            * 'standard'
            * 'keeper'
            * 'keeper_adv'
            * 'shooting'
            * 'passing'
            * 'passing_types'
            * 'goal_shot_creation'
            * 'defense'
            * 'possession'
            * 'playing_time'
            * 'misc'

        Parameters
        ----------
        stat_type: str
            Type of stats to retrieve.
        opponent_stats: bool
            If True, will retrieve opponent stats.

        Raises
        ------
        TypeError
            If ``stat_type`` is not valid.

        Returns
        -------
        pd.DataFrame
        """
        team_stats = [
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
        ]

        filemask = "teams_{}_{}_{}.html"

        if stat_type not in team_stats:
            raise TypeError(f"Invalid argument: stat_type should be in {team_stats}")

        if stat_type == "standard":
            page = "stats"
        elif stat_type == "keeper":
            page = "keepers"
        elif stat_type == "keeper_adv":
            page = "keepersadv"
        elif stat_type == "goal_shot_creation":
            page = "gca"
            stat_type = "gca"
        elif stat_type == "playing_time":
            page = "playingtime"
        else:
            page = stat_type

        if opponent_stats:
            stat_type += "_against"
        else:
            stat_type += "_for"

        # get league IDs
        seasons = self.read_seasons()

        # collect teams
        teams = []
        for (lkey, skey), season in seasons.iterrows():
            big_five = lkey == "Big 5 European Leagues Combined"
            tournament = season["format"] == "elimination"
            # read html page (league overview)
            filepath = self.data_dir / filemask.format(
                lkey, skey, stat_type if big_five else "all"
            )
            url = (
                FBREF_API
                + "/".join(season.url.split("/")[:-1])
                + (f"/{page}/squads/" if big_five else f"/{page}/" if tournament else "/")
                + season.url.split("/")[-1]
            )
            reader = self.get(url, filepath)

            # parse HTML and select table
            tree = html.parse(reader).xpath(
                f"//table[@id='stats_teams_{stat_type}' or @id='stats_squads_{stat_type}']"
            )[0]
            # remove icons
            for elem in tree.xpath("//span"):
                elem.getparent().remove(elem)
            # parse table
            df_table = pd.read_html(etree.tostring(tree))[0]
            df_table["league"] = lkey
            df_table["season"] = skey
            df_table["url"] = tree.xpath(".//*[@data-stat='team']/a/@href")
            if big_five:
                df_table["league"] = (
                    df_table.xs("Comp", axis=1, level=1).squeeze().map(BIG_FIVE_DICT)
                )
                df_table.drop("Comp", axis=1, level=1, inplace=True)
                df_table.drop("Rk", axis=1, level=1, inplace=True)
            teams.append(df_table)

        # return data frame
        df = (
            _concat(teams)
            .rename(columns={"Squad": "team"})
            .replace({"team": TEAMNAME_REPLACEMENTS})
            .set_index(["league", "season", "team"])
            .sort_index()
        )
        return df

    def read_player_season_stats(self, stat_type: str = "standard") -> pd.DataFrame:  # noqa: C901
        """Retrieve players from the datasource for the selected leagues.

        The following stat types are available:
            * 'standard'
            * 'shooting'
            * 'passing'
            * 'passing_types'
            * 'goal_shot_creation'
            * 'defense'
            * 'possession'
            * 'playing_time'
            * 'misc'
            * 'keeper'
            * 'keeper_adv'

        Parameters
        ----------
        stat_type :str
            Type of stats to retrieve.

        Raises
        ------
        TypeError
            If ``stat_type`` is not valid.

        Returns
        -------
        pd.DataFrame
        """
        player_stats = [
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
        ]

        filemask = "players_{}_{}_{}.html"

        if stat_type not in player_stats:
            raise TypeError(f"Invalid argument: stat_type should be in {player_stats}")

        if stat_type == "standard":
            page = "stats"
        elif stat_type == "goal_shot_creation":
            page = "gca"
            stat_type = "gca"
        elif stat_type == "playing_time":
            page = "playingtime"
        elif stat_type == "keeper":
            page = "keepers"
        elif stat_type == "keeper_adv":
            page = "keepersadv"
        else:
            page = stat_type

        # get league IDs
        seasons = self.read_seasons()

        # collect players
        players = []
        for (lkey, skey), season in seasons.iterrows():
            big_five = lkey == "Big 5 European Leagues Combined"
            filepath = self.data_dir / filemask.format(lkey, skey, stat_type)
            url = (
                FBREF_API
                + "/".join(season.url.split("/")[:-1])
                + f"/{page}"
                + ("/players/" if big_five else "/")
                + season.url.split("/")[-1]
            )
            reader = self.get(url, filepath)
            tree = html.parse(reader)
            # remove icons
            for elem in tree.xpath("//td[@data-stat='comp_level']//span"):
                elem.getparent().remove(elem)
            if big_five:
                df_table = pd.read_html(etree.tostring(tree))[0]
                df_table[("Unnamed: league", "league")] = (
                    df_table.xs("Comp", axis=1, level=1).squeeze().map(BIG_FIVE_DICT)
                )
                df_table[("Unnamed: season", "season")] = skey
                df_table.drop("Comp", axis=1, level=1, inplace=True)
            else:
                el = tree.xpath(f"//comment()[contains(.,'div_stats_{stat_type}')]")[0]
                df_table = pd.read_html(el.text, attrs={"id": f"stats_{stat_type}"})[0]
                df_table[("Unnamed: league", "league")] = lkey
                df_table[("Unnamed: season", "season")] = skey

            if not ("Unnamed: 2_level_0", "Nation") in df_table.columns:
                df_table.loc[:, (slice(None), "Squad")] = (
                    df_table.xs("Squad", axis=1, level=1)
                    .squeeze()
                    .apply(
                        lambda x: x.split(" ")[1] if isinstance(x, str) and x != "Squad" else None
                    )
                )
                df_table.insert(
                    2,
                    ("Unnamed: nation", "Nation"),
                    df_table.xs("Squad", axis=1, level=1).squeeze(),
                )
            else:
                df_table.loc[:, (slice(None), "Nation")] = (
                    df_table.xs("Nation", axis=1, level=1)
                    .squeeze()
                    .apply(
                        lambda x: x.split(" ")[1] if isinstance(x, str) and x != "Nation" else None
                    )
                )

            players.append(df_table)

        # return dataframe
        df = _concat(players)
        df = df[df.Player != "Player"]
        df = (
            df.drop("Matches", axis=1, level=0)
            .drop("Rk", axis=1, level=0)
            .rename(columns={"Player": "player", "Squad": "team"})
            .replace({"team": TEAMNAME_REPLACEMENTS})
            .set_index(["league", "season", "team", "player"])
            .sort_index()
        )

        return df

    def read_schedule(self, force_cache: bool = False) -> pd.DataFrame:
        """Retrieve the game schedule for the selected leagues and seasons.

        Parameters
        ----------
        force_cache : bool
             By default no cached data is used for the current season.
             If True, will force the use of cached data anyway.

        Returns
        -------
        pd.DataFrame
        """
        # get league IDs
        seasons = self.read_seasons()

        # collect teams
        schedule = []
        for (lkey, skey), season in seasons.iterrows():
            # read html page (league overview)
            url_stats = FBREF_API + season.url
            filepath_stats = self.data_dir / f"teams_{lkey}_{skey}.html"
            reader = self.get(url_stats, filepath_stats)
            tree = html.parse(reader)

            url_fixtures = FBREF_API + tree.xpath("//a[text()='Scores & Fixtures']")[0].get("href")
            filepath_fixtures = self.data_dir / f"schedule_{lkey}_{skey}.html"
            current_season = not self._is_complete(lkey, skey)
            reader = self.get(
                url_fixtures, filepath_fixtures, no_cache=current_season and not force_cache
            )
            tree = html.parse(reader)
            table = tree.xpath("//table[contains(@id, 'sched')]")[0]
            df_table = pd.read_html(etree.tostring(table))[0]
            df_table["Match Report"] = [
                mlink.xpath("./a/@href")[0]
                if mlink.xpath("./a") and mlink.xpath("./a")[0].text == "Match Report"
                else None
                for mlink in table.xpath(".//td[@data-stat='match_report']")
            ]
            df_table["league"] = lkey
            df_table["season"] = skey
            df_table = df_table.dropna(how="all")
            schedule.append(df_table)
        df = (
            pd.concat(schedule)
            .rename(
                columns={
                    "Wk": "week",
                    "Home": "home_team",
                    "Away": "away_team",
                    "xG": "home_xg",
                    "xG.1": "away_xg",
                }
            )
            .replace(
                {
                    "home_team": TEAMNAME_REPLACEMENTS,
                    "away_team": TEAMNAME_REPLACEMENTS,
                }
            )
            .pipe(standardize_colnames)
        )
        df["date"] = pd.to_datetime(df["date"]).ffill()
        df["game"] = df.apply(make_game_id, axis=1)
        df.loc[~df.match_report.isna(), "game_id"] = (
            df.loc[~df.match_report.isna(), "match_report"].str.split("/").str[3]
        )
        df = df.set_index(["league", "season", "game"]).sort_index()
        return df

    def _parse_teams(self, tree: etree.ElementTree) -> List[Dict]:
        """Parse the teams from a match summary page.

        Parameters
        ----------
        tree : etree.ElementTree
            The match summary page.

        Returns
        -------
        list of dict
        """
        team_nodes = tree.xpath("//div[@class='scorebox']//strong/a")[:2]
        teams = []
        for team in team_nodes:
            teams.append({"id": team.get("href").split("/")[3], "name": team.text.strip()})
        return teams

    def read_lineup(
        self, match_id: Optional[Union[str, List[str]]] = None, force_cache: bool = False
    ) -> pd.DataFrame:
        """Retrieve lineups for the selected leagues and seasons.

        Parameters
        ----------
        match_id : int or list of int, optional
            Retrieve the lineup for a specific game.
        force_cache : bool
            By default no cached data is used to scrape the list of available
            games for the current season. If True, will force the use of
            cached data anyway.

        Raises
        ------
        ValueError
            If no games with the given IDs were found for the selected seasons and leagues.

        Returns
        -------
        pd.DataFrame.
        """
        urlmask = FBREF_API + "/en/matches/{}"
        filemask = "match_{}.html"

        # Retrieve games for which a match report is available
        df_schedule = self.read_schedule(force_cache).reset_index()
        df_schedule = df_schedule[~df_schedule.game_id.isna() & ~df_schedule.match_report.isnull()]
        # Select requested games if available
        if match_id is not None:
            iterator = df_schedule[
                df_schedule.game_id.isin([match_id] if isinstance(match_id, str) else match_id)
            ]
            if len(iterator) == 0:
                raise ValueError("No games found with the given IDs in the selected seasons.")
        else:
            iterator = df_schedule

        lineups = []
        for i, game in iterator.iterrows():
            url = urlmask.format(game["game_id"])
            # get league and season
            logger.info(
                "[%s/%s] Retrieving game with id=%s", i + 1, len(iterator), game["game_id"]
            )
            filepath = self.data_dir / filemask.format(game["game_id"])
            reader = self.get(url, filepath)
            tree = html.parse(reader)
            teams = self._parse_teams(tree)
            tables = tree.xpath("//div[@class='lineup']")
            for i, table in enumerate(tables):
                df_table = pd.read_html(etree.tostring(table))[0]
                df_table.columns = ["jersey_number", "player"]
                df_table["team"] = teams[i]["name"]
                if "Bench" in df_table.jersey_number.values:
                    bench_idx = df_table.index[df_table.jersey_number == "Bench"][0]
                    df_table.loc[:bench_idx, "is_starter"] = True
                    df_table.loc[bench_idx:, "is_starter"] = False
                    df_table["game"] = game["game"]
                    df_table["league"] = game["league"]
                    df_table["season"] = game["season"]
                    df_table["game"] = game["game"]
                    df_table.drop(bench_idx, inplace=True)
                lineups.append(df_table)
        df = pd.concat(lineups).set_index(["league", "season", "game", "team", "player"])
        # TODO: sub in, sub out, position
        return df

    def read_player_match_stats(
        self,
        stat_type: str = "summary",
        match_id: Optional[Union[str, List[str]]] = None,
        force_cache: bool = False,
    ) -> pd.DataFrame:
        """Retrieve the match stats for the selected leagues and seasons.

        The following stat types are available:
            * 'summary'
            * 'keepers'
            * 'passing'
            * 'passing_types'
            * 'defense'
            * 'possession'
            * 'misc'

        Parameters
        ----------
        stat_type : str
            Type of stats to retrieve.
        match_id : int or list of int, optional
            Retrieve the event stream for a specific game.
        force_cache : bool
            By default no cached data is used to scrape the list of available
            games for the current season. If True, will force the use of
            cached data anyway.

        Raises
        ------
        ValueError
            If no games with the given IDs were found for the selected seasons and leagues.
        TypeError
            If ``stat_type`` is not valid.

        Returns
        -------
        pd.DataFrame
        """
        match_stats = [
            "summary",
            "keepers",
            "passing",
            "passing_types",
            "defense",
            "possession",
            "misc",
        ]

        urlmask = FBREF_API + "/en/matches/{}"
        filemask = "match_{}.html"

        if stat_type not in match_stats:
            raise TypeError(f"Invalid argument: stat_type should be in {match_stats}")

        # Retrieve games for which a match report is available
        df_schedule = self.read_schedule(force_cache).reset_index()
        df_schedule = df_schedule[~df_schedule.game_id.isna() & ~df_schedule.match_report.isnull()]
        # Selec requested games if available
        if match_id is not None:
            iterator = df_schedule[
                df_schedule.game_id.isin([match_id] if isinstance(match_id, str) else match_id)
            ]
            if len(iterator) == 0:
                raise ValueError("No games found with the given IDs in the selected seasons.")
        else:
            iterator = df_schedule

        stats = []
        for i, game in iterator.iterrows():
            url = urlmask.format(game["game_id"])
            # get league and season
            logger.info(
                "[%s/%s] Retrieving game with id=%s", i + 1, len(iterator), game["game_id"]
            )
            filepath = self.data_dir / filemask.format(game["game_id"])
            reader = self.get(url, filepath)
            tree = html.parse(reader)
            (home_team, away_team) = self._parse_teams(tree)
            if stat_type == "keepers":
                id_format = "keeper_stats_{}"
            else:
                id_format = "stats_{}_" + stat_type
            table = tree.xpath("//table[@id='" + id_format.format(home_team["id"]) + "']")[0]
            df_table = pd.read_html(etree.tostring(table))[0]
            df_table["team"] = home_team["name"]
            df_table["game"] = game["game"]
            df_table["league"] = game["league"]
            df_table["season"] = game["season"]
            df_table["game_id"] = game["game_id"]
            stats.append(df_table)
            table = tree.xpath("//table[@id='" + id_format.format(away_team["id"]) + "']")[0]
            df_table = pd.read_html(etree.tostring(table))[0]
            df_table["team"] = away_team["name"]
            df_table["game"] = game["game"]
            df_table["league"] = game["league"]
            df_table["season"] = game["season"]
            df_table["game_id"] = game["game_id"]
            stats.append(df_table)

        df = _concat(stats)
        df = df[~df.Player.str.contains(r"^\d+\sPlayers$")]
        df = (
            df.rename(columns={"Player": "player"})
            .replace({"team": TEAMNAME_REPLACEMENTS})
            .set_index(["league", "season", "game", "team", "player"])
            .sort_index()
        )
        return df

    def read_shot_events(
        self, match_id: Optional[Union[str, List[str]]] = None, force_cache: bool = False
    ) -> pd.DataFrame:
        """Retrieve shooting data for the selected seasons or selected matches.

        The data returned includes who took the shot, when, with which body
        part and from how far away. Additionally, the player creating the
        chance and also the creation before this are included in the data.

        Parameters
        ----------
        match_id : int or list of int, optional
            Retrieve the lineup for a specific game.
        force_cache : bool
            By default no cached data is used to scrape the list of available
            games for the current season. If True, will force the use of
            cached data anyway.

        Raises
        ------
        ValueError
            If no games with the given IDs were found for the selected seasons and leagues.

        Returns
        -------
        pd.DataFrame.
        """
        urlmask = FBREF_API + "/en/matches/{}"
        filemask = "match_{}.html"

        # Retrieve games for which a match report is available
        df_schedule = self.read_schedule(force_cache).reset_index()
        df_schedule = df_schedule[~df_schedule.game_id.isna() & ~df_schedule.match_report.isnull()]
        # Selec requested games if available
        if match_id is not None:
            iterator = df_schedule[
                df_schedule.game_id.isin([match_id] if isinstance(match_id, str) else match_id)
            ]
            if len(iterator) == 0:
                raise ValueError("No games found with the given IDs in the selected seasons.")
        else:
            iterator = df_schedule

        shots = []
        for i, game in iterator.iterrows():
            url = urlmask.format(game["game_id"])
            # get league and season
            logger.info(
                "[%s/%s] Retrieving game with id=%s", i + 1, len(iterator), game["game_id"]
            )
            filepath = self.data_dir / filemask.format(game["game_id"])
            reader = self.get(url, filepath)
            tree = html.parse(reader)
            df_table = pd.read_html(etree.tostring(tree), attrs={"id": "shots_all"})[0]
            df_table["league"] = game["league"]
            df_table["season"] = game["season"]
            df_table["game"] = game["game"]
            shots.append(df_table)

        df = (
            _concat(shots)
            .rename(columns={"Squad": "team"})
            .replace({"team": TEAMNAME_REPLACEMENTS})
            .pipe(
                standardize_colnames,
                cols=["Outcome", "Minute", "Distance", "Player", "Body Part", "Notes", "Event"],
            )
            .set_index(["league", "season", "game", "team", "player"])
            .sort_index()
            .dropna(how="all")
        )
        return df


def _concat(dfs: List[pd.DataFrame]) -> pd.DataFrame:
    """Merge matching tables scraped from different pages.

    The level 0 headers are not consitent across seasons and leagues, this
    function tries to determine uniform column names.

    Parameters
    ----------
    dfs : list(pd.DataFrame)
        Input dataframes.

    Returns
    -------
    pd.DataFrame
        Concatenated dataframe with uniform column names.
    """
    # Look for the most complete level 0 columns
    all_columns = []
    for df in dfs:
        columns = pd.DataFrame(df.columns.tolist())
        # Move missing columns to level 0
        columns.replace({"": None}, inplace=True)
        mask = pd.isnull(columns[1])
        columns.loc[mask, [0, 1]] = columns.loc[mask, [1, 0]].values
        # Rename unnamed columns
        mask = columns[0].str.startswith("Unnamed:").fillna(False)
        columns.loc[mask, 0] = None
        all_columns.append(columns)
    columns = reduce(lambda left, right: left.combine_first(right), all_columns)

    # Move the remaining missing columns back to level 1 and replace with empyt string
    mask = pd.isnull(columns[0])
    columns.loc[mask, [0, 1]] = columns.loc[mask, [1, 0]].values
    columns.loc[mask, 1] = ""

    for df in dfs:
        df.columns = pd.MultiIndex.from_tuples(columns.to_records(index=False).tolist())

    return pd.concat(dfs)
