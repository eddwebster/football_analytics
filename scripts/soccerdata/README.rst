.. image:: https://raw.githubusercontent.com/probberechts/soccerdata/master/docs/_static/logo2.png
   :align: center
   :alt: SoccerData
   :width: 600px

.. badges-begin

|Downloads| |PyPI| |Python Version| |License| |Read the Docs| |Tests| |Codecov| |pre-commit| |Black|

.. |Downloads| image:: https://static.pepy.tech/badge/soccerdata/month
   :target: https://pepy.tech/project/soccerdata
   :alt: Downloads Per Month
.. |PyPI| image:: https://img.shields.io/pypi/v/soccerdata.svg
   :target: https://pypi.org/project/soccerdata/
   :alt: PyPI
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/soccerdata
   :target: https://pypi.org/project/soccerdata
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/soccerdata.svg
   :target: https://opensource.org/licenses/Apache-2.0
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/soccerdata/latest.svg?label=Read%20the%20Docs
   :target: https://soccerdata.readthedocs.io/
   :alt: Read the documentation at https://soccerdata.readthedocs.io/
.. |Tests| image:: https://github.com/probberechts/soccerdata/workflows/CI/badge.svg
   :target: https://github.com/probberechts/soccerdata/actions?workflow=CI
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/probberechts/soccerdata/branch/master/graph/badge.svg
   :target: https://app.codecov.io/gh/probberechts/soccerdata
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black

.. badges-end

SoccerData is a collection of scrapers to gather soccer data from popular
websites, including `Club Elo`_, `ESPN`_, `FBref`_, `FiveThirtyEight`_,
`Football-Data.co.uk`_, `SoFIFA`_ and `WhoScored`_. You get Pandas DataFrames
with sensible, matching column names and identifiers across datasets. Data is
downloaded when needed and cached locally.

.. code:: python

   import soccerdata as sd

   # Create a scraper class instance for the 2018/19 Premier League
   five38 = sd.FiveThirtyEight('ENG-Premier League', '1819')

   # Fetch data
   games = five38.read_games()
   forecasts = five38.read_forecasts()
   clinches = five38.read_clinches()

To learn how to install, configure and use SoccerData, see the
`Quickstart guide <https://soccerdata.readthedocs.io/en/latest/intro.html>`__. For documentation on each of the
supported data sources, see the `example notebooks <https://soccerdata.readthedocs.io/en/latest/datasources/>`__
and `API reference <https://soccerdata.readthedocs.io/en/latest/reference/>`__.

.. _Club Elo: https://www.clubelo.com/
.. _ESPN: https://www.espn.com/soccer/
.. _FBref: https://www.fbref.com/en/
.. _FiveThirtyEight: https://fivethirtyeight.com/soccer-predictions/
.. _Football-Data.co.uk: https://www.football-data.co.uk/
.. _SoFIFA: https://sofifa.com/
.. _WhoScored: https://www.whoscored.com/

**Disclaimer:** As soccerdata relies on web scraping, any changes to the
scraped websites will break the package. Hence, do not expect that all code
will work all the time. If you spot any bugs, then please `fork it and start
a pull request <https://github.com/probberechts/soccerdata/blob/master/CONTRIBUTING.rst>`__.
