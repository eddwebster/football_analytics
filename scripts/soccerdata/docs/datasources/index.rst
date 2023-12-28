.. soccerdata package index documentation toctree
.. _datasources:

.. currentmodule:: soccerdata
.. highlight:: python

========================
Overview of Data Sources
========================

Currently, the following data sources are supported.

.. rst-class:: datasources

-----

ClubElo
    `URL <http://clubelo.com>`__ |
    :doc:`Example usage <ClubElo>` |
    :doc:`API reference </reference/clubelo>`

    .. code::

      from soccerdata import ClubElo

    Team's relative strengths as Elo ratings, for most European leagues. Recalculated after every round, includes history.

-----

ESPN
    `URL <https://www.espn.com/soccer/>`__ |
    :doc:`Example usage <ESPN>` |
    :doc:`API reference </reference/espn>`

    .. code::

      from soccerdata import ESPN

    Historical results, statistics and lineups.

-----

FBref
    `URL <https://fbref.com/en/>`__ |
    :doc:`Example usage <FBref>` |
    :doc:`API reference </reference/fbref>`

    .. code::

      from soccerdata import FBref

    Historical results, lineups, and detailed aggregated statistics for teams and individual players based on Stats Perform data.

-----

FiveThirtyEight
    `URL <https://projects.fivethirtyeight.com/soccer-predictions/>`__ |
    :doc:`Example usage <FiveThirtyEight>` |
    :doc:`API reference </reference/fivethirtyeight>`

    .. code::

      from soccerdata import FiveThirtyEight

    Team's relative strengths as SPI ratings, predictions and results for the top European and American leagues.

-----

Football-Data.co.uk
    `URL <https://www.football-data.co.uk/data.php>`__ |
    :doc:`Example usage <MatchHistory>` |
    :doc:`API reference </reference/matchhistory>`

    .. code::

      from soccerdata import MatchHistory

    Historical results, betting odds and match statistics. Level of detail depends on league.

-----

SoFIFA
    `URL <https://sofifa.com/>`__ |
    :doc:`Example usage <SoFIFA>` |
    :doc:`API reference </reference/sofifa>`

    .. code::

      from soccerdata import SoFIFA

    Detailed scores on all player's abilities from EA Sports FIFA.

-----

WhoScored
    `URL <https://www.whoscored.com/>`__ |
    :doc:`Example usage <WhoScored>` |
    :doc:`API reference </reference/whoscored>`

    .. code::

      from soccerdata import WhoScored

    Historical results, match preview data and detailed Opta event stream data for major leagues.

.. toctree::
   :hidden:

   ClubElo
   ESPN
   FBref
   FiveThirtyEight
   MatchHistory
   SoFIFA
   WhoScored
