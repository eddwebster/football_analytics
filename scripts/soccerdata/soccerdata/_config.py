"""Configurations."""

import json
import logging
import logging.config
import os
import sys
from pathlib import Path

import pretty_errors  # NOQA: F401 (imported but unused)
from rich.logging import RichHandler

# Configuration
NOCACHE = os.environ.get("SOCCERDATA_NOCACHE", 'False').lower() in ('true', '1', 't')
NOSTORE = os.environ.get("SOCCERDATA_NOSTORE", 'False').lower() in ('true', '1', 't')
LOGLEVEL = os.environ.get('SOCCERDATA_LOGLEVEL', 'INFO').upper()

# Directories
BASE_DIR = Path(os.environ.get("SOCCERDATA_DIR", Path.home() / "soccerdata"))
LOGS_DIR = Path(BASE_DIR, "logs")
DATA_DIR = Path(BASE_DIR, "data")
CONFIG_DIR = Path(BASE_DIR, "config")

# Create dirs
LOGS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# Logger
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "minimal": {"format": "%(message)s"},
        "detailed": {
            "format": "%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d]\n%(message)s\n"  # noqa: E501
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "minimal",
            "level": logging.DEBUG,
        },
        "info": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "info.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.INFO,
        },
        "error": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "error.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.ERROR,
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console", "info", "error"],
            "level": LOGLEVEL,
            "propagate": True,
        },
    },
}
logging.config.dictConfig(logging_config)
logger = logging.getLogger("root")
logger.handlers[0] = RichHandler(markup=True)

# Team name replacements
TEAMNAME_REPLACEMENTS = {}
_f_custom_teamnname_replacements = CONFIG_DIR / "teamname_replacements.json"
if _f_custom_teamnname_replacements.is_file():
    with open(_f_custom_teamnname_replacements, encoding='utf8') as json_file:
        for team, to_replace_list in json.load(json_file).items():
            for to_replace in to_replace_list:
                TEAMNAME_REPLACEMENTS[to_replace] = team
    logger.info("Custom team name replacements loaded from %s.", _f_custom_teamnname_replacements)
else:
    logger.info(
        "No custom team name replacements found. You can configure these in %s.",
        _f_custom_teamnname_replacements,
    )


# League dict
LEAGUE_DICT = {
    "ENG-Premier League": {
        "ClubElo": "ENG_1",
        "MatchHistory": "E0",
        "FiveThirtyEight": "premier-league",
        "FBref": "Premier League",
        "ESPN": "eng.1",
        "SoFIFA": "English Premier League (1)",
        "WhoScored": "England - Premier League",
        "season_start": "Aug",
        "season_end": "May",
    },
    "ESP-La Liga": {
        "ClubElo": "ESP_1",
        "MatchHistory": "SP1",
        "FiveThirtyEight": "la-liga",
        "FBref": "La Liga",
        "ESPN": "esp.1",
        "SoFIFA": "Spain Primera Division (1)",
        "WhoScored": "Spain - LaLiga",
        "season_start": "Aug",
        "season_end": "May",
    },
    "ITA-Serie A": {
        "ClubElo": "ITA_1",
        "MatchHistory": "I1",
        "FiveThirtyEight": "serie-a",
        "FBref": "Serie A",
        "ESPN": "ita.1",
        "SoFIFA": " Italian Serie A (1)",
        "WhoScored": "Italy - Serie A",
        "season_start": "Aug",
        "season_end": "May",
    },
    "GER-Bundesliga": {
        "ClubElo": "GER_1",
        "MatchHistory": "D1",
        "FiveThirtyEight": "bundesliga",
        "FBref": "Fußball-Bundesliga",
        "ESPN": "ger.1",
        "SoFIFA": "German 1. Bundesliga (1)",
        "WhoScored": "Germany - Bundesliga",
        "season_start": "Aug",
        "season_end": "May",
    },
    "FRA-Ligue 1": {
        "ClubElo": "FRA_1",
        "MatchHistory": "F1",
        "FiveThirtyEight": "ligue-1",
        "FBref": "Ligue 1",
        "ESPN": "fra.1",
        "SoFIFA": "French Ligue 1 (1)",
        "WhoScored": "France - Ligue 1",
        "season_start": "Aug",
        "season_end": "May",
    },
    "INT-World Cup": {
        "FBref": "FIFA World Cup",
        "WhoScored": "International - FIFA World Cup",
    },
    "NED-Eredivisie": {
        "ClubElo": "NED_1",
        "MatchHistory": "N1",
        "SoFIFA": "[Netherlands] Eredivisie",
        "FBref": "Eredivisie",
        "ESPN": "ned.1",
        "FiveThirtyEight": "eredivisie",
        "WhoScored": "Netherlands - Eredivisie",
        "season_start": "Aug",
        "season_end": "May"
    },
    "ENG-Championship": {
        "ClubElo": "ENG_1",
        "MatchHistory": "E1",
        "SoFIFA": "English Championship (1)",
        "FBref": "Championship",
        "ESPN": "eng.2",
        "FiveThirtyEight": "championship",
        "WhoScored": "England - Championship",
        "season_start": "Aug",
        "season_end": "May"
    },
    "POR-Primeira Liga": {
        "ClubElo": "POR_1",
        "MatchHistory": "P1",
        "SoFIFA": "Portuguese Primera Liga (1)",
        "FBref": "Primeira Liga",
        "ESPN": "por.1",
        "FiveThirtyEight": "primeira-liga",
        "WhoScored": "Portugal - Liga Portugal",
        "season_start": "Aug",
        "season_end": "May"
    },
    "BEL-Pro League": {
        "ClubElo": "BEL_1",
        "MatchHistory": "B1",
        "SoFIFA": "Belgian Pro League (1)",
        "FBref": "Belgian Pro League",
        "ESPN": "bel.1",
        "FiveThirtyEight": "first-division-a",
        "WhoScored": "Belgium - Jupiler Pro League",
        "season_start": "Aug",
        "season_end": "May"
    },
}
_f_custom_league_dict = CONFIG_DIR / "league_dict.json"
if _f_custom_league_dict.is_file():
    with open(_f_custom_league_dict, encoding='utf8') as json_file:
        LEAGUE_DICT = {**LEAGUE_DICT, **json.load(json_file)}
    logger.info("Custom league dict loaded from %s.", _f_custom_league_dict)
else:
    logger.info(
        "No custom league dict found. You can configure additional leagues in %s.",
        _f_custom_league_dict,
    )
