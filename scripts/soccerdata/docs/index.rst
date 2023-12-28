=============================
Welcome to SoccerData's docs!
=============================

Release v\ |release|. (``pip install soccerdata``)


.. image:: https://pepy.tech/badge/soccerdata/month
    :target: https://pepy.tech/project/soccerdata
    :alt: SoccerData Downloads Per Month Badge

.. image:: https://img.shields.io/pypi/l/soccerdata.svg
    :target: https://pypi.org/project/soccerdata/
    :alt: License Badge

.. image:: https://img.shields.io/pypi/pyversions/soccerdata.svg
    :target: https://pypi.org/project/soccerdata/
    :alt: Python Version Support Badge


**SoccerData** is a collection of scrapers to gather soccer data from popular
websites, including `Club Elo`_, `ESPN`_, `FBref`_, `FiveThirtyEight`_,
`Football-Data.co.uk`_, `SoFIFA`_ and `WhoScored`_.

.. code:: python

   import soccerdata as sd

   # Create a scraper class instance for the 2018/19 Premier League
   five38 = sd.FiveThirtyEight('ENG-Premier League', '1819')

   # Fetch data
   games = five38.read_games()
   forecasts = five38.read_forecasts()
   clinches = five38.read_clinches()


-------------------

**Main features**

- Access current and historical soccer fixtures, forecasts, detailed match
  stats, event stream data and more.
- All data is provided in the form of Pandas DataFrames with sensible,
  matching column names and identifiers across datasets to make working with
  the data and combining data from multiple sources easy.
- Data is only downloaded when needed and cached locally to speed up your
  analyis scripts.
- Integrates with the `socceraction`_ package to allow analysis of event stream
  data.

Do you like it? :doc:`Let's dive in! <intro>`

.. toctree::
   :hidden:
   :maxdepth: 1

   intro
   datasources/index
   howto/index
   examples/index
   reference/index
   faq
   contributing
   License <license>
   Changelog <https://github.com/probberechts/soccerdata/releases>

.. _socceraction: https://socceraction.readthedocs.io/en/latest/documentation/data/opta.html#whoscored
.. _Club Elo: https://www.clubelo.com/
.. _ESPN: https://www.espn.com/soccer/
.. _FBref: https://www.fbref.com/en/
.. _FiveThirtyEight: https://fivethirtyeight.com/soccer-predictions/
.. _Football-Data.co.uk: https://www.football-data.co.uk/
.. _SoFIFA: https://sofifa.com/
.. _WhoScored: https://www.whoscored.com/
