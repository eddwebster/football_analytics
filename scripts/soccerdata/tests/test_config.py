"""Unittests for soccerdata._config."""
import json
import logging
from importlib import reload

from soccerdata import _config as conf


def test_env_soccerdata_dir(monkeypatch, tmp_path):
    monkeypatch.setenv('SOCCERDATA_DIR', str(tmp_path))
    reload(conf)
    assert conf.BASE_DIR == tmp_path


def test_env_nocache(monkeypatch):
    monkeypatch.setenv('SOCCERDATA_NOCACHE', 't')
    reload(conf)
    assert conf.NOCACHE is True

    monkeypatch.setenv('SOCCERDATA_NOCACHE', 'true')
    reload(conf)
    assert conf.NOCACHE is True

    monkeypatch.setenv('SOCCERDATA_NOCACHE', 'f')
    reload(conf)
    assert conf.NOCACHE is False


def test_env_nostore(monkeypatch):
    monkeypatch.setenv('SOCCERDATA_NOSTORE', 't')
    reload(conf)
    assert conf.NOSTORE is True

    monkeypatch.setenv('SOCCERDATA_NOSTORE', 'true')
    reload(conf)
    assert conf.NOSTORE is True

    monkeypatch.setenv('SOCCERDATA_NOSTORE', 'f')
    reload(conf)
    assert conf.NOSTORE is False


def test_env_loglevel(monkeypatch):
    monkeypatch.setenv('SOCCERDATA_LOGLEVEL', 'DEBUG')
    reload(conf)
    assert conf.logger.level == logging.DEBUG


def test_read_teamnname_replacements(monkeypatch, tmp_path):
    monkeypatch.setenv('SOCCERDATA_DIR', str(tmp_path))
    # no teamname_replacements.json
    reload(conf)
    assert conf.TEAMNAME_REPLACEMENTS == {}
    fp = tmp_path / "config" / "teamname_replacements.json"
    with open(fp, 'w', encoding='utf8') as outfile:
        json.dump({"Celta de Vigo": ["Celta Vigo", "Celta"]}, outfile)
    # correctly parse teamname_replacements.json
    reload(conf)
    assert conf.TEAMNAME_REPLACEMENTS == {
        "Celta Vigo": "Celta de Vigo",
        "Celta": "Celta de Vigo",
    }


def test_read_league_dict(monkeypatch, tmp_path):
    monkeypatch.setenv('SOCCERDATA_DIR', str(tmp_path))
    # no league_dict.json
    reload(conf)
    nb_default = len(conf.LEAGUE_DICT)
    fp = tmp_path / "config" / "league_dict.json"
    with open(fp, 'w', encoding='utf8') as outfile:
        json.dump({"ABC-Fake": {"WhoScored": "Fake"}}, outfile)
    # correctly parse league_dict.json
    reload(conf)
    assert len(conf.LEAGUE_DICT) == nb_default + 1
    assert conf.LEAGUE_DICT['ABC-Fake'] == {'WhoScored': 'Fake'}
