===========================
How to add custom leagues
===========================

SoccerData has built-in support to scrape data from the top-5 European leagues
and the major international tournaments. The leagues available for each source
can be listed with the :meth:`~soccerdata.FBref.available_leagues` class method.

.. code:: python

  import soccerdata as sd
  sd.FBref.available_leagues()
  >>> ['ENG-Premier League', 'ESP-La Liga', 'FRA-Ligue 1', 'GER-Bundesliga', 'ITA-Serie A']

This documentation explains how to add custom leagues.


.. warning::

  Note that you might encounter errors when trying to scrape data for the
  leagues you added yourself. This is because the data provided for these
  leagues might have a different structure. If you encounter such an error,
  please do not open an issue on GitHub, but try to fix it yourself.



Adding a new league
-------------------

Additional leagues can configured in ``SOCCERDATA_DIR/config/league_dict.json``.
This file should contain a mapping between a generic name for the league and
the identifier used internally by each data source (see below) that you want
to support. For example, for the Dutch Eredivisie this would be:

.. code-block:: json

  {
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
    }
  }

The ``season_end`` and ``season_start`` fields are optional. This should be
the month in which the last game and first game of a season are played,
respectively. If they are not provided, June is used as the last month of the
season and July as the first one.

Now, restart your Python session and check whether it is added to available
leagues by running the command below.

.. code:: python

  >>> import soccerdata as sd
  >>> sd.FBref.available_leagues()
  [..., 'NED-Eredivisie', ...]



Internal identifiers
--------------------

Below are instructions on how to find the internal identifiers for each data
source.

**ClubElo**
  The internal identifier has the format ``{country_code}_{level}``. The get
  the country code, go to https://clubelo.com/, click on the league you want
  to add and take the three-letter code in the URL. For example, the URL for
  the Dutch Eredivisie is http://clubelo.com/NED which means that the country
  identifier is ``NED``. The level is the number of the league, starting with
  1 for the top league. The internal identifier for the Dutch Eredivisie is
  therefore ``NED_1``.

**MatchHistory**
  The internal identifier has the format ``{country_code}{level}``. Download
  the CSV file corresponding corresponding to the league you would like to add
  from https://www.football-data.co.uk/data.php and take the value in the
  ``Div`` column.

**SoFIFA**
  The internal identifier has the format ``[{region}] {league name}``. Go to
  https://sofifa.com/api/league to get the list of available leagues. The
  ``{region}`` corresponds to the ``nationName`` field in the JSON response. The
  ``{league name}`` corresponds to the ``value`` field.

**FBref**
  Go to https://fbref.com/en/comps/ and take the value in the ``Competition
  Name`` column.

**ESPN**
  The internal identifier has the format ``{country_code}.{level}``. Go to
  https://www.espn.com/soccer/competitions, click on the league you want
  to add and take the value in the URL after ``/league/_/name/``.

**FiveThirtyEight**
  Go to https://projects.fivethirtyeight.com/soccer-predictions/, select the
  relevant league and take the value in the URL after
  ``/soccer-predictions/``.

**WhoScored**
  Go to https://www.whoscored.com and use the JavaScript console to get the
  value of the ``allRegions`` variable. The internal identifier has the format
  ``{region name} - {league name}``.

Troubleshooting
---------------

If you add a new league and it doesn't show up in the list of available leagues,
there are a few things you can do to debug the problem.

1. Make sure to reload the soccerdata module after you modify the
   ``league_dict.json`` file. The most straightforward way to do this is to
   restart your notebook or Python interpreter.

2. Check whether your ``league_dict.json`` file is at the correct location. If
   so, you should see this appear in the log messages when importing the
   soccerdata library.

   .. code:: python

     >>> import soccerdata as sd
     [11/25/22 11:49:12] INFO     Custom team name replacements loaded from <path>/teamname_replacements.json.                                                                                                _config.py:83
                         INFO     Custom league dict loaded from <path>/league_dict.json.                                                                                                                    _config.py:153


3. Check whether the content of your ``league_dict.json`` file is valid JSON.
   You can check the file's syntax using Python's built-in ``json.tool``
   module.

   .. code:: sh

      $ cat config/league_dict.json | python -m json.tool
      Expecting ',' delimiter: line 1 column 10 (char 9)
