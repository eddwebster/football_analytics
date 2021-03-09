# Edd Webster Football Analytics
This repository is a public space for the football analytics projects by [Edd Webster](https://twitter.com/eddwebster) and a list of publicly available resources published by the football analytics community.

<p align="center">
  <a href="https://www.twitter.com/eddwebster"><img src="img/fifa21eddwebsterbanner.png"></a>
</p>


I am currently rewriting this README to include links not only to my own work, but also to include a concise list of learning resources, data sources, libraries, papers, blogs, podcasts, etc., created by all those that have made contributions to the football analytics community. This is currently in progress and could still do with a bit of editing, but most of the content is now available below. If you can think of any resources that I've missed, feel free to create a pull request or send me a message. Credits to the [Soccer Analytics Handbook](https://github.com/devinpleuler/analytics-handbook) by [Devin Pleuler](https://twitter.com/devinpleuler), the [Awesome Soccer Analytics](https://github.com/matiasmascioto/awesome-soccer-analytics) by [Matias Mascioto](https://twitter.com/matiasmascioto), and [Jan Van Haaren](https://twitter.com/janvanhaaren)'s [Soccer Analytics 2020 Review](https://janvanhaaren.be/2020/12/30/soccer-analytics-review-2020.html), which were all used to plug gaps in the list once it was published.

## About This Repository and Author
Please note, all the work produced in this repository is mine and/or credited to the publicly produced code and libraries used, and is in no way related to the work and analysis I produce for my employers.

For more information about this repository and the author, I'm available through all the following channels:
*    [eddwebster.com](https://www.eddwebster.com/);
*    edd.j.webster@gmail.com;
*    [@eddwebster](https://www.twitter.com/eddwebster);
*    [linkedin.com/in/eddwebster](https://www.linkedin.com/in/eddwebster/);
*    [github/eddwebster](https://github.com/eddwebster/); and
*    [public.tableau.com/profile/edd.webster](https://public.tableau.com/profile/edd.webster).

## Contents:
*    [Notebooks](#notebooks)
*    [Data Visualisation and Tableau](#data--tableau)
*    [Data Sources](#data--sources)
*    [Tutorials](#tutorials)
*    [Libaries (Python and R)](#libraries--r)
*    [GitHub repos (Python and R)](#githubs--r)
*    [Papers](#papers)
*    [Written Pieces](#written--pieces)
*    [Videos](#videos)
*    [Books](#books)
*    [Podcasts](#podcasts)
*    [Notable Figures / Twitter Accounts](#notable--accounts)
*    [Career Advice](#career-advice)
*    [Events and Conferences](#events--conferences)
*    [Competitions](#competitions)
*    [Jobs](#jobs)
*    [Key Concepts](#key--concepts) (TBA)
*    [Miscellaneous](#miscellaneous)
*    [Credits](#credits)

## :composition_notebook: Notebooks
For code, see the notebooks subfolder, in which the workflow is divided into the following:
1.    [Webscraping](https://github.com/eddwebster/football_analytics/tree/master/notebooks/1_data_scraping);
2.    [Data Parsing](https://github.com/eddwebster/football_analytics/tree/master/notebooks/2_data_parsing);
3.    [Data Engineering](https://github.com/eddwebster/football_analytics/tree/master/notebooks/3_data_engineering);
4.    [Machine Learning](https://github.com/eddwebster/football_analytics/tree/master/notebooks/4_machine_learning); and
5.    [Data Analysis](https://github.com/eddwebster/football_analytics/tree/master/notebooks/5_data_analysis_and_projects) - projects include working with [Tracking data](https://github.com/eddwebster/football_analytics/tree/master/notebooks/5_data_analysis_and_projects/tracking_data), constructing [VAEP models](https://github.com/eddwebster/football_analytics/tree/master/notebooks/5_data_analysis_and_projects/vaep) (as introduced by SciSports), building [xG models](https://github.com/eddwebster/football_analytics/tree/master/notebooks/5_data_analysis_and_projects/xg_modeling) using Logistic Regression, Decision Trees and XGBoost, and analysing [player similarity](https://github.com/eddwebster/football_analytics/tree/master/notebooks/5_data_analysis_and_projects/player_similarity) using PCA and Factor Analysis.

## :bar_chart: Data Visualisation and Tableau 
For Tableau dashboards produced using the data engineered in the notebooks in this repository, please see my Tableau Public profile: [public.tableau.com/profile/edd.webster](https://public.tableau.com/profile/edd.webster). 
*    WSL dashboards and analysis [[link](https://public.tableau.com/views/EddWebsterFAWSLAnalysisandDashboard/WSLxGAnalysisDashboard?:language=es&:display_count=y&:origin=viz_share_link)];
*    ‘Big 5’ European leagues dashboards and analysis [[link](https://public.tableau.com/views/EddWebsterBig5EuropeanLeagueAnalysisandDashboards/Big5WaffleChart?:language=es&:display_count=y&:origin=viz_share_link)];
*    EFL dashboards and analysis [[link](https://public.tableau.com/views/EddWebsterEFLAnalysisandDashboards/EFLFullBackRadarDashboard?:language=es&:display_count=y&:origin=viz_share_link)];
*    StrataBet Chance dashboards and analysis [[link](https://public.tableau.com/views/EddWebsterStrataBetChanceAnalysisandDashboards/StrataBetChanceShotMapDashboard?:language=es&:display_count=y&:origin=viz_share_link)]; and
*    Opta [#mcfcanalytics](https://twitter.com/search?q=%23mcfcanalytics) dashboards and analysis [[link](https://public.tableau.com/views/EddWebsterOptaMCFCAnalyticsPL1112AnalysisandDashboards/OptaPlayerDemographicsDashboard?:language=es&:display_count=y&:origin=viz_share_link)].

## :floppy_disk: Data Sources

### Data sources used in this repository
Due to the 100mb file size limitation in GitHub, all engineered datasets prepared in this repository have been exported and made publicly available to view and download in Google Drive. Please see the following [[link](https://drive.google.com/drive/folders/1r2Rf3CPsKnxyxtmDRIHQ2eoW5WwCzBa0?usp=sharing)]. However, all code in this repository should enable you to scrape, parse, and engineer the datasets to the format in which I have analysed and visualised the data in this repo.

Data sources featured in this repository include:
*    [DAVIES](https://samgoldberg1882.shinyapps.io/ShinyAlph/) estimated player evaluation data by [Sam Goldberg](https://twitter.com/SamGoldberg1882) and Mike Imburgio for [American Soccer Analysis](https://www.americansocceranalysis.com/);
*    [ELO club rankings](http://clubelo.com/);
*    [FIFA 15-21 player rating data](https://www.kaggle.com/stefanoleone992/fifa-21-complete-player-dataset) scraped from [SoFIFA](https://sofifa.com/) by Stefano Leone;
*    [KPMG Football Benchmark](https://footballbenchmark.com/home) player valuation data;
*    [Last Row Tracking-like data](https://github.com/Friends-of-Tracking-Data-FoTD/Last-Row) by [Ricardo Tavares](https://twitter.com/rjtavares);
*    [Metrica Sports Sample Tracking and corresponding Event data](https://github.com/metrica-sports/sample-data). For code to work with this data, see the  [`LaurieOnTracking`](https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking) GitHub repo by [Laurie Shaw](https://twitter.com/EightyFivePoint) and the corresponding Friends of Tracking tutorials;
*    [Opta Sports](https://www.optasports.com/) match-by-match aggregated player performance data for the 11/12 season and F24 Event data for a 11/12 match of Manchester City vs. Bolton Wanders [[link](#mcfcanalytics)] as part of the [#mcfcanalytics](https://twitter.com/search?q=%23mcfcanalytics) initiative;
*    [Signality Tracking data](https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython/blob/master/12GetSignalityAPI.py). The password to download the data is not publicly available, but can be found in the Uppsala Mathematical Modelling of Football Slack group [[link](http://mathematicalm-fhj6138.slack.com)]. For access, contact Novosom Salvador [Twitter](@novosomsalvador) and rsalvadords@gmail.com, or feel free to contact myself. Note, that the 2nd half of the Hammarby-Örebro match is incomplete;
*    [SkillCorner broadcast Tracking Open data](https://github.com/SkillCorner/opendata);
*    [StatsBomb Open Event data](https://github.com/statsbomb/open-data);
*    [StatsBomb](https://statsbomb.com/) season-on-season aggregated player performance data scraped via [FBref](https://fbref.com/en/) using [Parth Athale](https://twitter.com/ParthAthale)'s [`Scrape-FBref-data`](https://github.com/parth1902/Scrape-FBref-data) scraper, which in turn was written using code from [Christopher Martin](https://github.com/chmartin)'s [repository](https://github.com/chmartin/FBref_EPL);
*    [Stats Perform](https://www.statsperform.com/) and [Centre Circle](https://canpl.ca/centre-circle-data/) [Canadian Premiere League Event data](https://canpl.ca/centre-circle-data/). See Google Drive [[link](https://drive.google.com/drive/u/0/folders/1ktlkt6f6Ujami53YCS-Lbc9BGGL8BaYA)];
*    [StrataData]() from [StrataBet](http://www.stratagem.co/) Chance shooting data;
*    [TransferMarket](https://www.transfermarkt.com/) player bio and fiscal data scraped using the [`Tyrone Mings`](https://github.com/FCrSTATS/tyrone_mings) Python TransferMarkt webscraper by [FCrSTATS](https://twitter.com/FC_rstats) (I've currently submitted a pull request to fix issues with this library to scrape bio-status data, see my [[TransferMarkt scraping notebook](https://nbviewer.jupyter.org/github/eddwebster/football_analytics/blob/master/notebooks/1_data_scraping/TransferMarkt%20Web%20Scraping.ipynb)] for code with minor fixes to enable code to run);
*    [Understat](https://understat.com/) shooting and meta data including player xG values, scraped using the [`understatr`](https://github.com/ewenme/understatr) R package; 
*    [Wyscout Event data](https://wyscout.com/) Event data for the 17/18 season for the 'Big 5' European leagues, Euro 2016 Chanpionship, and 2018 World Cup made available by [Luca Pappalardo](https://twitter.com/lucpappalard?), Alessio Rossi, and Paolo Cintia. See their  paper [A public data set of spatio-temporal match events in soccer competitions](https://www.nature.com/articles/s41597-019-0247-7).
*    Reference data:
     -    League-wide xT values from the 2017-18 Premier League season (12x8 grid) by [Karun Singh](https://twitter.com/karun1710/) [[link](https://karun.in/blog/data/open_xt_12x8_v1.json)]
     -    EPV grid by [Laurie Shaw](https://twitter.com/EightyFivePoint) [[link](https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking/blob/master/EPV_grid.csv)]
     -    Zones on a pitch for Tableau visualisation by [Rob Carroll](https://twitter.com/thevideoanalyst) [[link](https://drive.google.com/drive/folders/1Se0DFtsjQWmnt-G9Ihn_w8EQE4EZiblD)]
     -    Alphabetic country codes [[link](https://en.wikipedia.org/wiki/Comparison_of_alphabetic_country_codes)]

### All publicly available data sources and datasets
Various websites that provide a wealth of data relating to football, from detailed match statistics, injury records and transfers.

*    [Awesome Football](https://github.com/planetopendata/awesome-football): A collection of awesome football (national teams, clubs, match schedules, players, stadiums, etc.) datasets;
*    [Club Elo](http://clubelo.com/) - European club rankings;
*    [Data Hub Football data](https://datahub.io/collections/football);
*    [DAVIES](https://samgoldberg1882.shinyapps.io/ShinyAlph/) estimated player evaluation data by [Sam Goldberg](https://twitter.com/SamGoldberg1882) and Mike Imburgio for [American Soccer Analysis](https://www.americansocceranalysis.com/);
*    [European Soccer Database](https://www.kaggle.com/hugomathien/soccer/version/10) - 25k+ matches, players & teams attributes for European Professional Football
*    [engsoccerdata](https://github.com/jalapic/engsoccerdata) - English and European soccer results 1871-2017;
*    [FBref](https://fbref.com/en/) (provider of [StatsBomb](https://statsbomb.com/data/) data);
*    [FIFA 15-21 player rating data](https://www.kaggle.com/stefanoleone992/fifa-21-complete-player-dataset) scraped from [SoFIFA](https://sofifa.com/) by Stefano Leone;
*    [FiveThirtyEight Club Ranking](https://projects.fivethirtyeight.com/global-club-soccer-rankings/) - Global Club Soccer Rankings. How 637 international club teams compare by Soccer Power Index;
*    [FiveThirtyEight Soccer Predictions database](https://projects.fivethirtyeight.com/soccer-predictions/) - football prediction data;
*    [`FootballData`](https://github.com/jokecamp/FootballData) - "A hodgepodge of JSON and CSV Football data"
*    [Football-Data.co.uk](https://www.football-data.co.uk/) - free bets and football betting, historical football results and a betting odds archive, live scores, odds comparison, betting advice and betting articles;
*    [`footballcsv`](https://footballcsv.github.io/) - Historical soccer results in CSV format;
*    [football.db](http://openfootball.github.io/) - A free and open public domain football database & schema for use in any (programming) language (e.g. uses plain datasets);
*    [Football Lineups](http://www.football-lineups.com);
*    [Football xG](https://footballxg.com/);
*    [Guide to Football/Soccer data and APIs](https://www.jokecamp.com/blog/guide-to-football-and-soccer-data-and-apis/) by Joe Kampschmidt;
*    [International football results from 1872 to 2020](https://www.kaggle.com/martj42/international-football-results-from-1872-to-2017) by Mart Jürisoo;
*    [KPMG Football Benchmark](https://footballbenchmark.com/home) player valuation data;
*    [Metrica Sports Tracking data](https://github.com/metrica-sports/sample-data);
*    [My Football Facts](http://www.myfootballfacts.com/);
*    [Physio Room](http://physioroom.com/);
*    [PlusMinusData](https://github.com/fmatano/PlusMinusData) - play by play data from espn.com and sofifa.com;
*    [The Price of Football Master Spreadsheet](https://t.co/c1DYrIB14C?amp=1) - data from the finance/business aspect of football by Kieren Maguire
*    [Rec.Sport.Soccer Statistics Foundation](http://www.rsssf.com/nersssf.html) - Historical league tables and football results;
*    [RoboCup Soccer Simulator](http://oliver.obst.eu/data/RoboCupSimData/overview.html) - RoboCup Soccer Simulator Data;
*    [SkillCorner broadcast Tracking data](https://github.com/SkillCorner/opendata);
*    [SofaScore](https://www.sofascore.com/) - live scores, lineups, standings and basic teams, coaches and players data;
*    [Soccer Video and Player Position Dataset](http://home.ifi.uio.no/paalh/dataset/alfheim/) - dataset of elite soccer player movements and corresponding videos. See the accompanying paper [[link](http://home.ifi.uio.no/paalh/publications/files/mmsys2014-dataset.pdf);
*    [Squawka](http://www.squawka.com);
*    [StatsBomb Open Data](https://github.com/statsbomb/open-data) - Competitions and matches (with events);
*    [Stat Bunker](https://www.statbunker.com);
*    [Stats Perform](https://www.statsperform.com/) and [Centre Circle](https://canpl.ca/centre-circle-data/) [Canadian Premiere League Event data](https://canpl.ca/centre-circle-data/). See Google Drive [[link](https://drive.google.com/drive/u/0/folders/1ktlkt6f6Ujami53YCS-Lbc9BGGL8BaYA)];
*    [Transfer League](http://www.transferleague.co.uk);
*    [TransferMarkt](http://www.transfermarkt.co.uk);
*    [Twelve Football](https://twelve.football/);
*    [wosostats](https://github.com/amj2012/wosostats) - Data about women's soccer from around the world;
*    [Understat](https://understat.com/);
*    [WhoScored?](https://www.whoscored.com/); and
*    [Wyscout](https://wyscout.com/) Event data for the 17/18 season for the 'Big 5' European leagues, Euro 2016 Chanpionship, and 2018 World Cup made available by [Luca Pappalardo](https://twitter.com/lucpappalard?), Alessio Rossi, and Paolo Cintia. See their  paper [A public data set of spatio-temporal match events in soccer competitions](https://www.nature.com/articles/s41597-019-0247-7).

### Documentation
[TO ADD HERE]

### Data Companies

#### Data Providers
*    [DataFactory](http://www.datafactory.la/)
*    [InStat](https://instatsport.com/)
*    [K-Sport](http://www.k-sport.tech/)
*    [Opta Sports](https://www.optasports.com/)
*    [smarterscout](https://smarterscout.com/)
*    [Sportlogiq](https://sportlogiq.com/en/)
*    [Sport radar](https://www.sportradar.com/)
*    [STATS PERFORM](https://www.statsperform.com/)
*    [StatsBomb](https://statsbomb.com/data/)
*    [StrataBet](http://www.stratagem.co/) (now defunct)
*    [TransferMarket](https://www.transfermarkt.com/)
*    [understat](https://understat.com/)
*    [WhoScored?](https://www.whoscored.com/) (provider of [Opta Sports](https://www.optasports.com/) data)
*    [Wyscout](https://wyscout.com/es/)

#### Tracking
*    [Catapult](https://www.catapultsports.com/)
*    [ChyronHego](https://chyronhego.com/)
*    [Metrica Sports](https://metrica-sports.com/)
*    [Second Spectrum](https://www.secondspectrum.com/index.html)
*    [Signality](https://www.signality.com/)
*    [SkillCorner](https://www.skillcorner.com/)
*    [STATS SportVU](https://www.stats.com/sportvu-football/)
*    [Kinexon](https://kinexon-sports.com/)
*    [Oliver](https://tryoliver.com/)

#### Video / Performance Analysis
*    [Analytics FC](http://analyticsfc.co.uk/)
*    [dataFootball](https://www.bdatafutbol.com/)
*    [ERIC Sports](http://www.ericsports.net/)
*    [Futbolytics](https://futbolytics.cl/)
*    [hudl](https://www.hudl.com/)
*    [LBi Dynasty](http://www.lbidynasty.com/)
*    [LongoMatch](https://longomatch.com/es/)
*    [MEDIACOACH](https://portal.mediacoach.es/)
*    [nacsport](https://nacsport.com/)
*    [Olocip](http://www.olocip.com/)
*    [SICO](https://www.sicostats.com/)
*    [Wise](http://app.wise4sports.com/home/)

## Tutorials

### Python and R 
*    Friends of Tracking YouTube channel [[link](https://www.youtube.com/channel/UCUBFJYcag8j2rm_9HkrrA7w)] and Mathematical Modelling of Football course by Uppsala University [[link](https://uppsala.instructure.com/courses/28112)]. The GitHub repo with all code featured can be found at the following [[link](https://github.com/Friends-of-Tracking-Data-FoTD)]. Lectures of note include:
     +    Laurie Shaw's Metrica Sports Tracking data series for #FoT - [Introduction](https://www.youtube.com/watch?v=8TrleFklEsE), [Measuring Physical Performance](https://www.youtube.com/watch?v=VX3T-4lB2o0), [Pitch Control modelling](https://www.youtube.com/watch?v=5X1cSehLg6s), and [Valuing Actions](https://www.youtube.com/watch?v=KXSLKwADXKI). See the following for code [[link](https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking)];
     +    Lotte Bransen and Jan Van Haaren's 'Valuating Actions in Football' series for #FoT - [Valuing Actions in Football: Introduction](https://www.youtube.com/watch?v=xyyZLs_N1F0), [Valuing Actions in Football 1: From Wyscout Data to Rating Players](https://www.youtube.com/watch?v=0ol_eLLEQ64), [Valuing Actions in Football 2: Generating Features](https://www.youtube.com/watch?v=Ep9wXQgAFaE&t=42s), [Valuing Actions in Football 3: Training Machine Learning Models](https://www.youtube.com/watch?v=WlORqYIb-Gg), and [Valuing Actions in Football 4: Analyzing Models and Results](https://www.youtube.com/watch?v=w9G0z3eGCj8). See the following for code [[link](https://github.com/SciSports-Labs/fot-valuing-actions)];
     +    David Sumpter's Expected Goals webinars for #FoT - [How to Build An Expected Goals Model 1: Data and Model](https://www.youtube.com/watch?v=bpjLyFyLlXs), [How to Build An Expected Goals Model 2: Statistical fitting](https://www.youtube.com/watch?v=wHOgINJ5g54), and [The Ultimate Guide to Expected Goals](https://www.youtube.com/watch?v=310_eW0hUqQ). See the following for code [3xGModel](https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython/blob/master/3xGModel.py), [4LinearRegression](https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython/blob/master/4LinearRegression.py), [5xGModelFit.py](https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython/blob/master/5xGModelFit.py), and [6MeasuresOfFit](https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython/blob/master/6MeasuresOfFit.py);
     +    Peter McKeever's ['Good practice in data visualisation'](https://www.youtube.com/watch?v=md0pdsWtq_o) webinar for #FoT. See the following for code [[link](https://github.com/petermckeeverPerform/friends-of-tracking-viz-lecture)];;
*    [Soccer Analytics Handbook](https://github.com/devinpleuler/analytics-handbook) by [Devin Pleuler](https://twitter.com/devinpleuler). See tutorial notebooks (also available in Google Colab): [1. Data Extraction & Transformation](https://github.com/devinpleuler/analytics-handbook/blob/master/notebooks/data_extraction_and_transformation.ipynb), [2. Linear Regression](https://github.com/devinpleuler/analytics-handbook/blob/master/notebooks/linear_regression.ipynb), [3. Logistic Regression](https://github.com/devinpleuler/analytics-handbook/blob/master/notebooks/logistic_regression.ipynb), [4. Clustering](https://github.com/devinpleuler/analytics-handbook/blob/master/notebooks/clustering.ipynb), [5. Database Population & Querying](https://github.com/devinpleuler/analytics-handbook/blob/master/notebooks/database_population_and_querying.ipynb), [7. Data Visualization](https://github.com/devinpleuler/analytics-handbook/blob/master/notebooks/data_visualization.ipynb), [8. Non-Negative Matrix](https://github.com/devinpleuler/analytics-handbook/blob/master/notebooks/non_neg_matrix_factorization.ipynb), [9. Pitch Dominance](https://github.com/devinpleuler/analytics-handbook/blob/master/notebooks/pitch_dominance.ipynb), [10. Convolutional Neural Networks](https://github.com/devinpleuler/analytics-handbook/blob/master/notebooks/nn_pass_difficulty.ipynb);
*    [FC Python](https://twitter.com/fc_python) tutorials [[link](https://fcpython.com/)];
*    [FCrSTATS](https://github.com/FCrSTATS) tutorials [[link](http://fcrstats.com/tutorials.html)];
*    DataViz, Python, and matplotlib tutorials by Peter McKeever [[link](http://petermckeever.com/)] - I think his website is currently in redevelopment, with many of the old tutorials not currently available (28/02/2021). Check out his revamped [How to Draw a Football Pitch](http://petermckeever.com/2020/10/how-to-draw-a-football-pitch/) tutorial;
*    [McKay Johns YouTube channel](https://www.youtube.com/channel/UCmqincDKps3syxvD4hbODSg);
*    [soccer_analytics GitHub repo](https://github.com/CleKraus/soccer_analytics) by CleKraus - a Python project that facilitates the starting point for analytics 
*    [Python for Fantasy Football series](http://www.fantasyfutopia.com/python-for-fantasy-football-introduction/) by [Fantasy Futopia](https://twitter.com/FantasyFutopia) ([Thomas Whelan](https://twitter.com/tom_whelan)). This series covers the basics of working with data in Python, working with APIs and parsing StatsBomb JSON data, scraping data using Beautifulsoup and Selenium, and Machine Learning with scikit-learn and XGBoost,  See GitHub repo for all code [[link](https://github.com/twhelan22/python-for-fantasy-football)]; and
*    [Tech how-to: build your own Expected Goals model](https://www.scisports.com/tech-how-to-build-your-own-expected-goals-model/) by Jan Van Haaren and SciSports.

### Tableau
For a YouTube playlist of Tableau-football videos and tutorials that I have collated from various sources including the Tableau Football User Group, Rob Carroll, and Tom Goodall, see the following [[link](https://www.youtube.com/watch?v=Rx7FWugmBC4&list=PL38nJNjpNpH__B0QzZ3BA0B3AxGzt0FAl&ab_channel=TableauSoftware)].

*    Tableau Football User Group [[link](https://usergroups.tableau.com/footballtableauusergroup)] - featuring [Eva Murray](https://twitter.com/TriMyData), Oscar Hall, [James Smith](https://twitter.com/sportschord), [Rob Carroll](https://twitter.com/thevideoanalyst), [Tom Goodall](https://twitter.com/TomG26), [Ravi Mistry](https://twitter.com/Scribblr_42),  Adam Cook, Hannah Roberts, Chris Baker, Rusty Parker, Ruud van Elk, Johannes Riegger, and Sebastien Coustou;
*    [Tableau for Sport](https://thevideoanalyst.com/tableau-sport/) by [Rob Carroll](https://twitter.com/thevideoanalyst) - completely free tutorials for using football data in Tableau, including creating shot maps, pass maps, pass matrxces, xG race-chart timelines. See also his YouTube playlist [[link](https://www.youtube.com/playlist?list=PLchE8bhmmIxK94imJ4QZncXrbld_NGoiW)];
*    [Tom Goodall's Tactics, Training & Tableau: Football Tableau User Group](https://www.youtube.com/watch?v=Hy0tHU7yYHs&t=1702s). Check out his Football Tableau training courses [[link](https://www.touchlineanalytics.co.uk/). Check out also as an unrolled Twitter thread, how he uses Tableau to create an opposition report for Burton vs. Gillingham on 9th January 2021 [[link](https://threadreaderapp.com/thread/1346186082510110720.html)];
*    [Visually Analysing Direct Set Pieces in Football using StatsBomb Data, R and Tableau](https://www.biztory.com/blog/visually-analysing-direct-set-pieces-in-football-using-statsbomb-data-r-and-tableau) by James Smith;
*    [CJ Mayes](https://cj-mayes.com/)'s Tableau blog, with posts including how to make a [Radial Tournament Bracket](https://cj-mayes.com/2021/02/24/radial-tournament-bracket-2/);
*    [Tableau Tunnel series](https://ninad06.medium.com/welcome-to-thetableau-tunnel-4cd6f564ab48) by [Ninad Barbadikar](https://twitter.com/ninadb_06). Check out his Twitter thread [[link](https://twitter.com/NinadB_06/status/1348738404989558787)];
*    Medium blog posts by Sagnik Das - [Tableau Guide #1: Making Shot Maps](https://sagnikdas1.medium.com/tabguide-1-making-shot-maps-1c030f08393e), [Tableau Guide #2: Making Pass Maps](https://sagnikdas1.medium.com/tabguide-2-making-pass-maps-bad2d541b8ed), [Tableau Guide #3: Convex Hulls](https://sagnikdas1.medium.com/tableau-guide-3-convex-hulls-c7edc31a9921), [Tableau Guide #4 : Football Radars](https://sagnikdas1.medium.com/tableau-guide-4-football-radars-8cdac85ba1fc)
*    Medium blog posts by Rahul Iyer - [Guide to Creating Passing Networks in Tableau
](https://raahulbi103.medium.com/guide-to-creating-passing-networks-in-tableau-be8847420297), [Guide to Creating Pass Sonars in Tableau](https://raahulbi103.medium.com/guide-to-creating-pass-sonars-in-tableau-3361801d65aa);
*    [How to create Football Pitches/Goals as Backgrounds in Tableau](https://medium.com/analytics-vidhya/how-to-create-football-pitches-goals-as-backgrounds-in-tableau-7b1a7800ae1c)

### Other Sports
*    Twitter thread by [Measureables](https://twitter.com/MeasurablesPod) ([Brendan Kent](https://twitter.com/brendankent)) [[link](https://twitter.com/MeasurablesPod/status/1217499782631043072)]

## Libaries (Python and R)
*    [`codeball`](https://github.com/metrica-sports/codeball/) - data driven tactical and video analysis of soccer games;
*    [`Football Packing`](https://github.com/samirak93/Football-packing) - a Python package to calculate packing rate for a given pass in football by Samira Kumar. This is a variation of the metric created by Impect;
*    [`ggsoccer`](https://github.com/Torvaney/ggsoccer) - a soccer visualisation library in R from [Ben Torvaney](https://twitter.com/Torvaney);
*    [`kloppy`](https://github.com/PySport/kloppy) - a Python package providing (de)serializers for soccer tracking- and event data, standardized data models, filters, and transformers designed to make working with different tracking- and event data like a breeze;
*    [`matplotsoccer`](https://github.com/TomDecroos/matplotsoccer) - a Python library for visualising soccer event data by [Tom Decroos](https://twitter.com/TomDecroos);
*    [`mplsoccer`](https://github.com/andrewRowlinson/mplsoccer) - a Python library for drawing soccer/football pitches in Matplotlib and loading StatsBomb open-data by [Andrew Rowlinson](https://twitter.com/numberstorm);
*    [`nayra`](https://github.com/DonsetPG/narya) - API that allows you track soccer player from camera inputs, and evaluate them with an Expected Discounted Goal (EDG) Agent. See the [Evaluating Soccer Player](https://arxiv.org/pdf/2101.05388.pdf) paper by Paul Garnier and [Théophane Gregoir](https://twitter.com/_TheoGreg);
*    [`northpitch`](https://github.com/devinpleuler/northpitch) - a Python football plotting library that sits on top of Matplotlib by [Devin Pleuler](https://twitter.com/devinpleuler);
*    [`PCA_Player_Finder`](https://github.com/parth1902/PCA_Player_Finder) by [Parth Athale](https://twitter.com/ParthAthale);
*    [`PySport`](https://opensource.pysport.org/) including [`PySport Soccer`](https://opensource.pysport.org/?sports=Soccer) - collection of open-source sport packages including many of those mentioned in this section, by [Koen Vossen](https://twitter.com/mr_le_fox);
*    [`PyWaffle`](https://github.com/petermckeeverPerform/PyWaffle) - an open source, MIT-licensed Python package for plotting waffle charts by Peter McKeever;
*    [`Scrape-FBref-data`](https://github.com/parth1902/Scrape-FBref-data) - Python library to scrape StatsBomb data via FBref by [Parthe Athale](https://twitter.com/ParthAthale), which in turn was updated from [Christopher Martin](https://github.com/chmartin)'s [repository](https://github.com/chmartin/FBref_EPL);
*    [`statsbombapi`](https://github.com/Torvaney/statsbombapi) - a Python API wrapper and dataclasses for Statsbomb data;
*    [`statsbombpy`](https://github.com/statsbomb/statsbombpy) - a Python library written by Francisco Goitia to access StatsBomb data;
*    [`statsbomb-parser`](https://github.com/imrankhan17/statsbomb-parser) - Python library to convert StatsBomb's JSON data into easy-to-use CSV format;
*    [`socceraction`](https://github.com/ML-KULeuven/socceraction) - a Python library for valuing the individual actions performed by soccer players. Includes an Expected Threat (xT) implementation by Tom Decroos](https://twitter.com/TomDecroos) et. al.;
*    [`soccermix`](https://github.com/ML-KULeuven/soccermix) - a soft clustering technique based on mixture models that decomposes event stream data into a number of prototypical actions of a specific type, location, and direction by Tom Deccoos and ML-KULeuven;
*    [`soccer_xg`](https://github.com/ML-KULeuven/soccer_xg) - a Python package for training and analyzing expected goals (xG) models in football;
*    [`soccerplots`](https://github.com/Slothfulwave612/soccerplots) -  a Python package that can be used for making visualizations for football analytics by Slothfulwave;
*    [`sync.soccer`](https://github.com/huffyhenry/sync.soccer) - a Python package to synchronise football datasets, so that an event in one dataset is matched to the corresponding event or snapshot in the other by Marek Kwiatkowski. This repository contains an implementation that aligns Opta's (now STATS Perform's) F24 feeds to ChyronHego's Tracab files. More formats may be added in the future. See the following blog post for methodology [[link](https://kwiatkowski.io/sync.soccer)];
*    [`https://github.com/znstrider/tmscrape`](https://github.com/znstrider/tmscrape) - a Python TransferMarkt webscraper by [danzn1](https://twitter.com/danzn1);
*    [`Tyrone Mings`](https://github.com/FCrSTATS/tyrone_mings) - a Python TransferMarkt webscraper by [FCrSTATS](https://twitter.com/FC_rstats); and
*    [`understatr`](https://github.com/ewenme/understatr) - a R package to scrape data from Understat.

## GitHub repos (Python and R)
*    [`Google Research Football`](https://github.com/google-research/football);
*    [`Friends-of-Tracking-Data-FoTD`](https://github.com/Friends-of-Tracking-Data-FoTD);
*    [`SoccermaticsForPython`](https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython) - repo by David Sumpter dedicated for people getting started with Python using the concepts derived from the book Soccermatics 
*    [`LaurieOnTracking`](https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking) by [Laurie Shaw](https://twitter.com/EightyFivePoint) - Python code for working with Metrica tracking data;
*    [`FoundationsInR`](https://github.com/Friends-of-Tracking-Data-FoTD/FoundationsInR) by [Sudarshan Golaladesikan](https://twitter.com/suds_g) - getting started with R using the StatsBomb dataset;
*    [`Exploring spatio-temporal soccer events using public event data`](https://github.com/Friends-of-Tracking-Data-FoTD/mapping-match-events-in-Python) by [Luca Pappalardo](https://twitter.com/lucpappalard?), Alessio Rossi, and Paolo Cintia. See the paper: [A public data set of spatio-temporal match events in soccer competitions](https://doi.org/10.1038/s41597-019-0247-7);
*    [`Valuing actions in football`](https://github.com/SciSports-Labs/fot-valuing-actions) by Lotte Bransen and Jan Van Haaren of SciSports;
*    [`analytics-handbook`](https://github.com/devinpleuler/analytics-handbook) by [Devin Pleuler](https://twitter.com/devinpleuler)
*    [`soccer_analytics`](https://github.com/CleKraus/soccer_analytics) by CleKraus - a Python project trying to facilitate and being a starting point for analytics projects in soccer including EDA of Event data, goal kick analysis, passing analysis, xG modelling, and an introduction to Tracking data;
*    [`soccerAnimate`](https://github.com/Dato-Futbol/soccerAnimate) - an R package to create 2D animations of soccer tracking data;
*    [`Expected Goals Thesis`](https://github.com/andrewRowlinson/expected-goals-thesis) by [Andrew Rowlinson](https://twitter.com/numberstorm)
*    [`footballcsv`](https://footballcsv.github.io/) - Historical soccer results in CSV format;
*    [`Pass-Flow`](https://github.com/opengoalapp/Pass-Flow) - create animated flow velocity fields using passing data by Open Goal App;
*    [`passing-networks-in-python`](https://github.com/Friends-of-Tracking-Data-FoTD/passing-networks-in-python) - repository for building customizable passing networks with Matplotlib as part of the "Friends of Tracking" series. The code is prepared to use both eventing (StatsBomb) and tracking data (Metrica Sports);
*    [`football-crunching`](https://github.com/rjtavares/football-crunching) by Ricardo Tavares. Accompanying Medium posts [[link](https://medium.com/football-crunching)]; and
*    [`soccermatics`](https://github.com/JoGall/soccermatics) - an R package for the visualisation and analysis of soccer tracking and event data by [Joe Gallagher](https://twitter.com/joedgallagher).

## Apps
*    [ALPHONSO 2.0](https://samgoldberg1882.shinyapps.io/ShinyAlph/) by Sam Goldberg and Mike Imburgio for American Soccer Analysis; and
*    [Soccer Analytics Library](https://larsmaurath.shinyapps.io/soccer-analytics-library/)] by Lars Maurath.

## Papers
The following Shiny App from Lars Maurath is a great tool for looking up publications [[link](https://larsmaurath.shinyapps.io/soccer-analytics-library/)].

### 2021
*    [Evaluating Soccer Player: from Live Camera to Deep Reinforcement Learning](https://arxiv.org/pdf/2101.05388.pdf) (2021) by Paul Garnier and [Théophane Gregoir](https://twitter.com/_TheoGreg). See the [`nayra`](https://github.com/DonsetPG/narya) library for code;

### 2020
*    [Automatic Pass Annotation from Soccer Video Streams based on Object Detection and LSTM](https://arxiv.org/abs/2007.06475) (2020) by Danilo Sorano, Fabio Carrara, Paolo Cintia, Fabrizio Falchi and [Luca Pappalardo](https://twitter.com/lucpappalard?);
*    [A Framework for the Fine-Grained Evaluation of the Instantaneous Expected Value of Soccer Possessions](https://arxiv.org/abs/2011.09426) (2020) by Javier Fernández, Luke Bornn and Daniel Cervone;
*    [A new look into Off-ball Scoring Opportunity: taking into account the continuous nature of the game](https://sportstomorrow.fcbarcelona.com/wp-content/uploads/2020/11/A_new_look_into_Off-ball_Scoring_Opportunity_taking_into_account_the_continuous_nature_of_the_game.pdf) (2020) by [Hugo M. R. Rios-Neto](https://twitter.com/hugoriosneto), Wagner Meira Jr., Pedro O. S. Vaz-de-Melo;
*    [Cracking the Black Box: Distilling Deep Sports Analytics](https://arxiv.org/abs/2006.04551) (2020) by Xiangyu Sun, Jack Davis, Oliver Schulte and Guiliang Liu;
*    [Deep Soccer Analytics: Learning an Action-Value Function for Evaluating Soccer Players](https://www.researchgate.net/profile/Guiliang_Liu/publication/343122623_Deep_soccer_analytics_learning_an_action-value_function_for_evaluating_soccer_players/links/5f1f24d2a6fdcc9626b9cb41/Deep-soccer-analytics-learning-an-action-value-function-for-evaluating-soccer-players.pdf) (2020) by Guiliang Liu, Yudong Luo, Oliver Schulte and Tarak Kharrat;
*    [Game Plan: What AI can do for Football, and What Football can do for AI](https://arxiv.org/pdf/2011.09192.pdf) (2020) by Karl Tuyls, Shayegan Omidshafiei, Paul Muller, Zhe Wang, Jerome Connor, Daniel Hennes, Ian Graham, Will Spearman, Tim Waskett, and Dafydd Steele, Pauline Luc, Adria Recasens, Alexandre Galashov, Gregory Thornton, Romuald Elie, Pablo Sprechmann, Pol Moreno, Kris Cao, Marta Garnelo, Praneet Dutta, Michal Valko, Nicolas Heess, Alex Bridgland, Julien P´erolat, Bart De Vylder, Ali Eslami, Mark Rowland, Andrew Jaegle, Remi Munos, Trevor Back, Razia Ahamed, Simon Bouton, Nathalie Beauguerlange, Jackson Broshear, Thore Graepel, and Demis Hassabis;
*    [Google Research Football: A Novel Reinforcement Learning Environment](https://arxiv.org/pdf/1907.11180.pdf) (2020) by Karol Kurach, Anton Raichuk, Piotr Stańczyk, Michał Zając, Olivier Bachem, Lasse Espeholt, Carlos Riquelme, Damien Vincent, Marcin Michalski, Olivier Bousquet, Sylvain Gelly. See the GitHub repo [[link](https://github.com/google-research/football)];
*    [Group Activity Detection From Trajectory and Video Data in Soccer](https://arxiv.org/abs/2004.10299) (2020) by Ryan Sanford, Siavash Gorji, Luiz Hafemann, Bahareh Pourbabaee and Mehrsan Javan;
*    [Interpretable Prediction of Goals in Soccer](https://tomdecroos.github.io/reports/interpret_vaep.pdf) (2020) by Tom Decroos and Jesse Davis;
*    [Inverse Reinforcement Learning for Team Sports: Valuing Actions and Players](https://www.ijcai.org/Proceedings/2020/0464.pdf) (2020) by Yudong Luo, Oliver Schulte and Pascal Poupart. See the code [[link](https://github.com/miyunluo/IRL-icehockey)];
*    [Learning the Value of Teamwork to Form Efficient Teams](https://aaai.org/ojs/index.php/AAAI/article/view/6192/6048) (2020) by Ryan Beal, Narayan Changder, Timothy Norman, Sarvapali Ramchurn;
*    [Player Chemistry: Striving for a Perfectly Balanced Soccer Team](https://arxiv.org/abs/2003.01712) (2020) by [Lotte Bransen](https://twitter.com/LotteBransen). See the accompanying Friends of Tracking video tutorials [[link](https://github.com/SciSports-Labs/fot-valuing-actions)] and chapter 4 of the Barca Innovation Hub Football Analytics 2021 publication, titled: 'How does context affect player performance in football?' by Lotte Bransen, Pieter Robberechts, Jesse Davis, Tom Decroos, and Jan Van Haaren [[link](https://sportstomorrow.fcbarcelona.com/wp-content/uploads/2020/11/Barca_Innovation_Hub_FOOTBALL_ANALYTICS_2021.pdf)];
*    [Ready Player Run: Off-ball run identification and classification](https://static.capabiliaserver.com/frontend/clients/barca/wp_prod/wp-content/uploads/2020/01/40ba07f4-ready-player-run-barcelona.pdf) (2020) by [Sam Gregory](https://twitter.com/GregorydSam);
*    [The Right Place at the Right Time: Advanced Off-Ball Metrics for Exploiting an Opponent’s Spatial Weakenesses in Soccer](https://global-uploads.webflow.com/5f1af76ed86d6771ad48324b/5f6a69841d1ac99fa3a71a41_Llana_The-right-place-at-the-right-time.pdf) (2020) by Sergio Llana, Pau Madrero and Javier Fernández;
*    [Optimising Game Tactics for Football](https://arxiv.org/abs/2003.10294) (2020) by Ryan Beal, Georgios Chalkiadakis, Timothy Norman and Sarvapali Ramchurn;
*    [Routine Inspection: A Playbook for Corner Kicks](https://www.springerprofessional.de/en/routine-inspection-a-playbook-for-corner-kicks/18671052) (2020) by [Laurie Shaw](https://twitter.com/EightyFivePoint) and Sudarshan 'Suds' Gopaladesikan. See accompanying presentation at NESSIS 2020 [[link](https://www.youtube.com/watch?v=yfPC1O_g-I8)];
*    [Seeing in to the future: using self-propelled particle models to aid player decision-making in soccer](https://global-uploads.webflow.com/5f1af76ed86d6771ad48324b/5f6a6920624a527f2e4ac845_SLOAN-Peralta-Final-submission.pdf) (2020) by [Fran Peralta](https://twitter.com/PeraltaFran23), Pablo Piñones Arce, David Sumpter and [Javier Fernández](https://twitter.com/JaviOnData);
*    [SoccerMap: A Deep Learning Architecture for Visually-Interpretable Analysis in Soccer](https://arxiv.org/pdf/2010.10202.pdf) (2020) by [Javier Fernández](https://twitter.com/JaviOnData) and [Luke Bornn](https://twitter.com/LukeBornn);
*    [SoccerMix: Representing Soccer Actions with Mixture Models](https://tomdecroos.github.io/reports/ecml_2020.pdf) (2020) by Tom Decroos, Maaike Van Roy and Jesse Davis;
*    [Soccer Analytics Meets Artificial Intelligence: Learning Value and Style from Soccer Event Stream Data](https://tomdecroos.github.io/reports/thesis_tomdecroos.pdf) (2020) by Tom Decroos
*    [The Tactics of Successful Attacks in Professional Association Football: Large-Scale Spatiotemporal Analysis of Dynamic Subgroups Using Position Tracking Data](https://www.tandfonline.com/doi/pdf/10.1080/02640414.2020.1834689) (2020) by Floris Goes, Michel Brink, Marije Elferink-Gemser, Matthias Kempe and Koen Lemmink
*    [Using Player’s Body-Orientation to Model Pass Feasibility in Soccer](https://arxiv.org/abs/2004.07209) (2020) by Adrià Arbués-Sangüesa, Adrián Martín, Javier Fernández, Coloma Ballester and Gloria Haro;
*    [Valuing On-the-Ball Actions in Soccer: A Critical Comparison of xT and VAEP](https://tomdecroos.github.io/reports/xt_vs_vaep.pdf) (2020) by Maaike Van Roy, Pieter Robberechts, Tom Decroos and Jesse Davis;

### 2019
*    [Actions Speak Louder Than Goals: Valuing Player Actions in Soccer](https://arxiv.org/abs/1802.07127) (2019) by [Tom Decroos](https://twitter.com/TomDecroos), [Lotte Bransen](https://twitter.com/LotteBransen), [Jan Van Haaren](https://twitter.com/JanVanHaaren), and [Jesse Davis](https://twitter.com/jessejdavis1). See accompany presentation at SIGKDD 2019 by Tom Decroos [[link](https://www.youtube.com/watch?v=UtG9FNEcdKI)];
*    [Decomposing the Immeasurable Sport: A deep learning expected possession value framework for soccer](https://www.semanticscholar.org/paper/Decomposing-the-Immeasurable-Sport%3A-A-deep-learning-Fern%C3%A1ndez/fc78b144a531a8ffdf3216a677f3a65e70dad3c7) (2019) by [Javier Fernández](https://twitter.com/JaviOnData), [Bornn](https://twitter.com/LukeBornn), and [Dan Cervone](https://twitter.com/dcervone0). Accompanying talks - [SSAC19](https://www.youtube.com/watch?v=JIa7Td3YXxI), [StatsBomb conference](https://www.youtube.com/watch?v=nfPEEbKJbpM);
*    [Dynamic Analysis of Team Strategy in Professional Football](https://static.capabiliaserver.com/frontend/clients/barca/wp_prod/wp-content/uploads/2020/01/56ce723e-barca-conference-paper-laurie-shaw.pdf) (2019) by [Laurie Shaw](https://twitter.com/EightyFivePoint) and [Mark Glickman](https://twitter.com/glicko);
*    [Measuring soccer players’ contributions to chance creation by valuing their passes](https://repub.eur.nl/pub/115732/Repub_115732.pdf) (2019) by [Lotte Bransen](https://twitter.com/LotteBransen), [Jan Van Haaren](https://twitter.com/JanVanHaaren), and Michel van de Velden.
*    [Modelling the Collective Movement of Football Players](http://uu.diva-portal.org/smash/get/diva2:1365788/FULLTEXT01.pdf) (2019) by [Fran Peralta](https://twitter.com/PeraltaFran23); and
*    [Player Vectors: Characterizing Soccer Players’ Playing Style from Match Event Streams](https://tomdecroos.github.io/reports/ecml19_tomd.pdf) (2019) by [Tom Decroos](https://twitter.com/TomDecroos) and [Jesse Davis](https://twitter.com/jessejdavis1).

### 2018
*    [Beyond Expected Goals](https://www.researchgate.net/profile/William_Spearman/publication/327139841_Beyond_Expected_Goals/links/5b7c3023a6fdcc5f8b5932f7/Beyond-Expected-Goals.pdf) (2018) by [Will Spearman](https://twitter.com/the_spearman);
*    [Chance involvement in goal scoring in football](https://link.springer.com/article/10.1007%2Fs12662-018-0518-z#citeas) (2018) by Martin Lames
*    [Predicting football results using machine learning techniques](https://www.imperial.ac.uk/media/imperial-college/faculty-of-engineering/computing/public/1718-ug-projects/Corentin-Herbinet-Using-Machine-Learning-techniques-to-predict-the-outcome-of-profressional-football-matches.pdf) (2018) by Corentin Herbinet
*    [Replaying the NBA](http://www.lukebornn.com/papers/sandholtz_ssac_2018.pdf) (2018) by Luke Bornn
*    [Wide Open Spaces: A statistical technique for measuring space creation in professional soccer](https://www.researchgate.net/publication/324942294_Wide_Open_Spaces_A_statistical_technique_for_measuring_space_creation_in_professional_soccer) (2018) by [Javier Fernandez](https://twitter.com/JaviOnData) and [Luke Bornn](https://twitter.com/LukeBornn);
*    [Spatial analysis of shots in MLS: A model for expected goals and fractal dimensionality](https://content.iospress.com/articles/journal-of-sports-analytics/jsa207) (2018) by Alexandera Fairchild, Konstantinos Pelechrinis, Mariosa Kokkodis; and
*    [High-resolution shot capture reveals systematic biases and an improved method for shooter evaluation](https://global-uploads.webflow.com/5f1af76ed86d6771ad48324b/5ff4ad56b18b323042079f8e_An%20improved%20method%20for%20shooter%20evaluation.pdf) (2018) by Rachel Marty.

### 2017
*    [Physics-Based	Modeling	of Pass	Probabilities	in	Soccer](https://www.researchgate.net/publication/315166647_Physics-Based_Modeling_of_Pass_Probabilities_in_Soccer) (2017) by [Will Spearman](https://twitter.com/the_spearman), Austin Basye, Greg Dick, Ryan Hotovy, and Paul Pop;
*    [Data-Driven	Ghosting	using	Deep	Imitation	Learning](http://www.yisongyue.com/publications/ssac2017_ghosting.pdf) (2017) by [Hoang	M. Le](https://twitter.com/HoangMinhLe),	Peter	Carr,	Yisong	Yue,	and	[Patrick	Lucey](https://twitter.com/patricklucey);
*    [Valuing passes in football using ball event data](https://thesis.eur.nl/pub/41346/Bransen.pdf) (2017) by Lotte Bransen;
*    [“The Leicester City Fairytale?”: Utilizing New Soccer Analytics Tools to Compare Performance in the 15/16 & 16/17 EPL Seasons (2017)](https://userpages.umbc.edu/~nroy/courses/fall2018/cmisr/papers/soccer_analytics.pdf) by Hector Ruiz, Paul Power, Xinyu Wei, and Patrick Lucey;
*    [Not all passes are created equal: objectively measuring the risk and reward of passes in soccer from tracking data](http://library.usc.edu.ph/ACM/KKD%202017/pdfs/p1605.pdf) (2017) by Paul Power, Hector Ruiz, Xinyu Wei, and Patrick Lucey. See Paul Power's talk [[link](https://dl.acm.org/action/downloadSupplement?doi=10.1145%2F3097983.3098051&file=power_tracking_data.mp4&download=true)] (downloadable MP4), and the webpage [[link](https://dl.acm.org/doi/10.1145/3097983.3098051)];
*    [Plus-Minus Player Ratings for Soccer](https://arxiv.org/pdf/1706.04943.pdf) (2017) by Tarak Kharrat, Javier Pena, and Ian McHale
*    [An examination of expected goals and shot efficiency in soccer](https://www.redalyc.org/pdf/3010/301052437005.pdf) (2017) by Alex Rathke; and
*    [Predicting goal probabilities for possessions in football](https://www.math.vu.nl/~sbhulai/papers/paper-mackay.pdf) (2017) by Nils Mackay.

### 2016
*    [Spatio-Temporal Analysis of Team Sports – A Survey](https://arxiv.org/pdf/1602.06994.pdf) (2016) by Joachim Gudmundsson and Michael Horton;
*    [Valuing Individual Player Involvements in Norwegian Association Football](https://brage.bibsys.no/xmlui/bitstream/handle/11250/2433841/15584_FULLTEXT.pdf?sequence=1&isAllowed=y) (2016) by Olav Nørstebø, Vegard Rødseth Bjertnes, and Eirik Vabo; and
*    [Expected Goals in Soccer](https://pure.tue.nl/ws/files/46945853/855660-1.pdf) (2016) by Harm Eggels.

### 2015
*    [“Quality vs Quantity”: Improved Shot Prediction in Soccer using Strategic Features from Spatiotemporal Data](https://s3-us-west-1.amazonaws.com/disneyresearch/wp-content/uploads/20150308192147/Quality-vs-Quantity%E2%80%9D-Improved-Shot-Prediction-in-Soccer-using-Strategic-Features-from-Spatiotemporal-Data-Paper.pdf) (2015) by Patrick Lucey, Alina Bialkowski, Mathew Monfort, Peter Carr, and Iain Matthews;
*    [Quantifying Shot Quality in the NBA](http://www.sloansportsconference.com/wp-content/uploads/2014/02/2014-SSAC-Quantifying-Shot-Quality-in-the-NBA.pdf) by ; and 
*    [Soccer video and player position dataset](http://home.ifi.uio.no/paalh/publications/files/mmsys2014-dataset.pdf) (2015) by S. A. Pettersen, D. Johansen, H. Johansen, V. Berg-Johansen, V. R. Gaddam, A. Mortensen, R. Langseth, C. Griwodz, H. K. Stensland, and P. Halvorsen. See the accompanying webpage [[link](https://datasets.simula.no/alfheim/)].

### 2014
*    [Large-Scale Analysis of Soccer Matches using Spatiotemporal Tracking Data](https://s3-us-west-1.amazonaws.com/disneyresearch/wp-content/uploads/20141211131038/Large-Scale-Analysis-of-Soccer-Matches-using-Spatiotemporal-Tracking-Data-Paper.pdf) (2014) by Alina Bialkowski, Patrick Lucey, Peter Carr, Yisong Yue, Sridha Sridharan, and Iain Matthews.

### 2011
*    [A Framework for Tactical Analysis and Individual Offensive Production Assessment in Soccer Using Markov Chains](http://nessis.org/nessis11/rudd.pdf) (2011) by [Sarah Rudd](https://twitter.com/srudd_ok). Accompanying NESSIS talk on Metacafe [[link](https://www.metacafe.com/watch/7337475/2011_nessis_talk_by_sarah_rudd/)]; and
*    [An Extension of the Pythagorean Expectation for Association Football](https://www.soccermetrics.net/wp-content/uploads/2013/08/football-pythagorean-article.pdf) (2011) by [Howard Hamilton](https://twitter.com/soccermetrics).

## :books: Written Pieces

### Highly Rated and Recommended Pieces
Many of these blog posts are recommended in [Sam Gregory](https://twitter.com/GregorydSam)'s [Best Football Analytics Pieces](https://medium.com/@GregorydSam/best-football-analytics-pieces-e532844b12e) piece and [Tom Worville](https://twitter.com/Worville)'s [“What’s the best Football Analytics piece you’ve ever read?”](https://medium.com/@worville/whats-the-best-football-analytics-piece-you-ve-ever-read-815c0bf50ccf).

*    [Assessing	The	Performance	of Premier League Goalscorers](https://opta.kota.co.uk/news-analysis/assessing-the-performance-of-premier-league-goalscorers/) by [Sam Green](https://twitter.com/aSamGreen);
*    [Counting Across Borders](https://www.statsperform.com/resource/counting-across-borders/) by [Ben Torvaney](https://twitter.com/Torvaney);
*    [Defending Your Patch](https://deepxg.com/2016/02/07/defending-your-patch/) by [Thom Lawrence](https://twitter.com/lemonwatcher);
*    [The DePO Models: Bringing Moneyball to Professional Soccer](https://www.americansocceranalysis.com/home/2020/10/26/the-depo-models-bringing-moneyball-to-professional-soccer) by Sam Goldberg and Mike Imburgio;
*    [Using Data to Analyse Team Formations](https://eightyfivepoints.blogspot.com/2019/11/using-data-to-analyse-team-formations.html) by [Laurie Shaw](https://twitter.com/EightyFivePoint);
*    [Structure in football: putting formations into context](https://eightyfivepoints.blogspot.com/2020/12/structure-in-football-putting.html) by [Laurie Shaw](https://twitter.com/EightyFivePoint);
*    [Inside Arsenal’s Attack: In-Depth Analysis Of Arteta’s Problems & Possible Solutions](https://worldfootballindex.com/2021/01/arsenal-attack-in-depth-analysis-arteta-tactics-problems-solutions/) by Ashwin Raman;
*    [Premier League Projections and New Expected Goals](https://cartilagefreecaptain.sbnation.com/2015/10/19/9295905/premier-league-projections-and-new-expected-goals) by [Michael Caley](https://twitter.com/MC_of_A);
*    [Introducing Passing Combinations](https://wawrzynow.wordpress.com/2021/01/06/introducing-passing-combinations/) by [Piotr Wawrzynów](https://twitter.com/pwawrzynow);
*    [Pass Footedness in the Premier League](https://statsbomb.com/2019/04/pass-footedness-in-the-premier-league/) by [James Yorke](https://twitter.com/jair1970);
*    [Messi Walks Better Than Most Players Run](https://fivethirtyeight.com/features/messi-walks-better-than-most-players-run/) by [Bobby Gardiner](https://twitter.com/BobbyGardiner);
*    [Soccer Analytics 101](https://www.mlssoccer.com/soccer-analytics-guide/2020/soccer-analytics-101) by Kevin Minkus;
*    [An Introduction to Soccer Analytics](https://spacespacespaceletter.com/an-introduction-to-soccer-analytics/) by [John Muller](https://twitter.com/johnspacemuller);
*    [Valuing On-the-Ball Actions in Soccer: A Critical Comparison of xT and VAEP](https://dtai.cs.kuleuven.be/sports/blog/valuing-on-the-ball-actions-in-soccer-a-critical-comparison-of-xt-and-vaep) by Jesse Davis, Tom Decroos, Pieter Robberechts, Maaike Van Roy;
*    [Game of Throw-Ins](https://www.americansocceranalysis.com/home/2018/11/27/game-of-throw-ins) by [Eliot McKinley](https://twitter.com/etmckinley);
*    [Expected Threat](https://karun.in/blog/expected-threat.html) by [Karun Singh](https://twitter.com/karun1710). Check out also as an unrolled Twitter thread [[link](https://threadreaderapp.com/thread/1361695899131387909.html)] Karun's Twitter thread for the many resources out there around this topic, including: [Episode 19 of The Football Fanalytics Podcast](https://open.spotify.com/episode/0HvcNPxg8Ux6zJB2nGp3VK?si=AOkxcH3KTue4jeEIA6kpWw&nd=1), Karun's StatsBomb conference presentation [[link](https://www.youtube.com/watch?v=mE3sUVCIwfA)] and slides [[link](https://docs.google.com/presentation/d/1tu603CdONhI17AZTrd3mdf1UAf7k-rHwwCLSU_tCx6g/edit#slide=id.p)], [Rob Hickman](https://twitter.com/robwhickman)'s StatsBomb conference presentation where he extended xT to take defensive risk into account [[link](https://twitter.com/robwhickman)], [Last Row View](https://twitter.com/lastrowview) ([Ricardo Tavares](https://twitter.com/rjtavares))'s blog post for evaluating off-the-ball player movements by combining xT and tracking data, and Karun's xT values as a 12x8 grid to download as a JSON file [[link](https://t.co/IoZdCa2BbX?amp=1)];
*    [Lionel Messi’s ten stages of greatness](https://theathletic.co.uk/1880554/2020/08/07/lionel-messi-barcelona-la-liga-champions-league/) by Michael Cox and [Tom Worville](https://twitter.com/Worville);
*    [Passing Out at the Back](https://www.statsperform.com/resource/passing-out-at-the-back/) by [Will Gürpinar-Morgan](https://twitter.com/WillTGM);
*    [The 10 Commandments of Football Analytics](https://theathletic.co.uk/1692489/2020/03/23/the-10-commandments-of-football-analytics/) by [Tom Worville](https://twitter.com/Worville);
*    [Breaking Down Set Pieces: Picks, Packs, Stacks and More](https://statsbomb.com/2019/05/breaking-down-set-pieces-picks-packs-stacks-and-more/) by [Euan Dewar](https://twitter.com/EuanDewar);
*    [Data Based Coaching: How to Incorporate Data-Driven Decision into Your Coaching Workflow](https://www.americansocceranalysis.com/home/2020/3/19/data-based-coaching-how-to-incorporate-data-driven-decisions-into-your-coaching-workflow) by [Kieran Doyle](https://twitter.com/KierDoyle); and
*    [Coaches Reward Goalscorers. But Should They?](https://www.americansocceranalysis.com/home/2020/3/30/coaches-reward-goalscorers-they-shouldnt) by [Eliot McKinley](https://twitter.com/etmckinley) and [John Muller](https://twitter.com/johnspacemuller).

### Blogs and Data Analytics Websites
*    [11tegen11](https://11tegen11.com/)
*    [21st Club](https://www.21stclub.com/insight/) - blog posts available in hard-copy form in their [Changing the Conversation](https://www.amazon.co.uk/Changing-Conversation-Presents-Collection-Boardrooms/) series;
*    [2+2=11](https://2plus2equals11.com/) by [Will Gürpinar-Morgan](https://twitter.com/WillTGM);
*    [5 Added Minutes](https://5addedminutes.com/) by [Omar Chaudhuri](https://twitter.com/OmarChaudhuri) (last updated 03/09/2016);
*    [8 Yards 8 Feet](https://8yards8feet.wordpress.com/author/simonlock1993/) by [Simon Lock](https://twitter.com/8Yards8Feet);
*    [All Things Football](https://allthingsfootballonline.blogspot.com/);
*    [Absolute Unit](https://absoluteunit.substack.com/);
*    [American Soccer Analysis](https://www.americansocceranalysis.com/);
*    [Analyse Football](https://analysefootball.com/) by [Ravi Ramineni](https://twitter.com/analyseFooty) (last updated 06//04/2015);
*    [Analytics FC](https://attackingcentreback.wordpress.com/);
*    [Attacking Center-back](https://attackingcentreback.wordpress.com/) by [JP Quinn](https://twitter.com/AttackingCB);
*    [Barça Innovation Hub](https://barcainnovationhub.com/category/blog/);
*    [Brendan Kent](https://brendankent.com/). Check out his [Sports Analytics 101 series](https://brendankent.com/sports-analytics-101/);
*    [Carey Analytics](https://careyanalytics.wordpress.com/) by [Mark Carey](https://twitter.com/MarkCarey93);
*    [DeepxG](https://deepxg.com/) by [Thom Lawrence](https://twitter.com/lemonwatcher) (last updated 29/11/2017);
*    [Differentgame](https://differentgame.wordpress.com/) by [Paul Riley](https://twitter.com/footballfactman);
*    [DTAI Sports Analytics Lab](https://dtai.cs.kuleuven.be/sports/) by KU Leuven;
*    [The Economics of Sport](http://www.sportseconomics.org/);
*    [EFL Numbers](https://eflnumbers.wordpress.com/) by [EFL Numbers](https://twitter.com/eflnumbers);
*    [EightyFivePoints](http://eightyfivepoints.blogspot.com/) by [Laurie Shaw](https://twitter.com/EightyFivePoint);
*    [Experimental 361](https://experimental361.com/) by [Ben Mayhew](https://twitter.com/experimental361);
*    [FC Python](https://fcpython.com/category/blog) by [FC Python](https://twitter.com/FC_Python);
*    [FiveThirtyEight Sports](https://fivethirtyeight.com/sports/);
*    [Football Crunching](https://medium.com/football-crunching) by [Ricardo Tavares](https://twitter.com/rjtavares);
*    [Football Data Science](http://business-analytic.co.uk/blog/home-page/) by [Dr. Garry Gelade](https://twitter.com/GarryGelade);
*    [Football Philosophy](http://footballphilosophy.org/) by Joost van der Leij;
*    [Football Science](https://www.footballscience.net/) by Michael C. Rumpf;
*    [Football Whispers](https://www.footballwhispers.com/);
*    [The Futebolist](https://medium.com/@thefutebolist) by [Ashwin Raman](https://twitter.com/AshwinRaman_);
*    [Get Goalside!](https://getgoalside.substack.com/);
*    [The Harvard Sports Analysis Collective](http://harvardsportsanalysis.org/topics/soccer/);
*    [Hockey Graphs](https://hockey-graphs.com/);
*    [Hudl](https://www.hudl.com/blog/);
*    [James W Grayson](https://jameswgrayson.wordpress.com/) by [James W Grayson](https://twitter.com/JamesWGrayson);
*    [Jan Van Haaren](https://janvanhaaren.be/) by [Jan Van Haaren](https://twitter.com/janvanhaaren);
*    [jogall.github.io](https://jogall.github.io/) by [Joe Gallagher](https://twitter.com/joedgallagher);
*    [Karun Singh](https://karun.in/blog/) by [Karun Singh](https://twitter.com/karun1710);
*    [kubamichalczyk.github.io](https://kubamichalczyk.github.io/) by [Kuba Michalczyk](https://twitter.com/kubamichalczyk)
*    [kwiatkowski.io](https://www.kwiatkowski.io/) by [Marek Kwiatkowski](https://twitter.com/statlurker);
*    [LukeBornn.com](http://www.lukebornn.com/) by [Luke Bornn](https://twitter.com/LukeBornn);
*    [Mackay Analytics](https://www.northyardanalytics.com/blog/) by [Nils Mackay](https://twitter.com/NilsMackay);
*    [Mackinaw Stats](https://mackayanalytics.nl/) by [Mackinaw Stats](https://twitter.com/mackinawstats);
*    [Mark's Notebook](https://marksnotebook.substack.com/) by [Mark Thompson](https://twitter.com/EveryTeam_Mark);
*    [MRKT Insights](https://mrktinsights.com/index.php/blog/);
*    [Ninad Barbadikar Medium blog](https://ninad06.medium.com/) by [Ninad Barbadikar](https://twitter.com/ninadb_06);
*    [North Yard Analytics](https://www.northyardanalytics.com/blog/) by [Dan Altman](https://twitter.com/NYAsports);
*    [openGoal](https://www.opengoalapp.com/) by [Charles William](https://twitter.com/openGoalCharles);
*    Opta Pro - old blogs removed by available using Wayback Machine;
*    [patricklucey.com](http://patricklucey.com/index.html) by [Patrick Lucey](https://twitter.com/patricklucey);
*    [Penal.lt/y](http://pena.lt/y/) by [Martin Eastwood](https://twitter.com/penaltyblog);
*    [Piotr Wawrzynów – Football Analysis](https://wawrzynow.wordpress.com/) by [Piotr Wawrzynów](https://twitter.com/pwawrzynow);
*    [Proform AFC](https://proformanalytics.wordpress.com/) by [Proform Analytics](https://twitter.com/ProformAFC) ([Mladen Sormaz](https://twitter.com/Mladen_Sormaz) and [Dan Nichol](https://twitter.com/D4N__));
*    [Ravi Mistry's Medium blog](https://scribblr42.medium.com/);
*    [SaddlersStats](https://www.saddlersstats.co.uk/);
*    [Sam Gregory Medium blog](https://medium.com/@GregorydSam);
*    [SciSports](https://www.scisports.com/);
*    [Soccermatics Medium blog](https://www.soccermetrics.net/blog) by [David Sumpter](https://www.soccermetrics.net/blog);
*    [soccerNurds](https://soccernurds.com/blog/);
*    [space space space](https://spacespacespaceletter.com/);
*    [StatDNA](https://web.archive.org/web/20110707064735/https:/blog.statdna.com/) (last updated 01/06/2011 before Arsenal bought the company);
*    [StatsBomb](https://statsbomb.com/articles/);
*    [Stats Perform](https://www.statsperform.com/resources/);
*    [Stats and snakeoil](http://www.statsandsnakeoil.com/) by [Ben Torvaney](https://twitter.com/Torvaney);
*    [The Last Man Analytics](https://thelastmananalytics.home.blog/) by [The Last Man Anayltics](https://twitter.com/tlmanalytics) ([Ciaran Grant](https://twitter.com/Ciaran_Grant));
*    [The Power of Goals](https://thepowerofgoals.blogspot.com/);
*    [Training Ground Guru](https://trainingground.guru/). Check out their accompanying podcast [[link](https://open.spotify.com/show/1Kn9l6LifZ2AWmZri9XWHn)];
*    [Tom Worville Medium blog](https://medium.com/@worville) by Tom Worville (last updated 14/08/2017). Tom now writes for The Athletic [[link](https://theathletic.co.uk/author/tom-worville/)];
*    [winningwithanalytics.com](https://winningwithanalytics.com/) by [Bill Gerrard](https://twitter.com/bill_gerrard_);
*    [Wooly Jumpers for Goal Posts](https://winningwithanalytics.com/) by [The Woolster](https://twitter.com/The_Woolster);
*    [Wyscout](https://blog.wyscout.com/);
*    [xG per Shot](https://xgpershot.wordpress.com/) by [Parthe Athale](https://twitter.com/ParthAthale); and
*    [Zonal Marking](http://www.zonalmarking.net/). by Michael Cox. Michael now writes for The Athletic [[link](https://theathletic.com/author/michael-cox/)].

### Newsletters
*    [21st Club](https://www.21stclub.com/insight/);
*    [Absolute Unit](https://absoluteunit.substack.com/);
*    [Get Goalside!](https://getgoalside.substack.com/);
*    [geom_mark](http://geommark.space/);
*    [Grace on Football](https://onfootball.substack.com/) by [Grace Robertson](https://twitter.com/graceonfootball);
*    [Looks Good on Paper](https://looksgoodonpaper.substack.com/) by [Felix Pate](https://twitter.com/lgopfelix);
*    [Measureables](https://www.measurablespod.com/newsletter) by [Brendan Kent](https://twitter.com/brendankent);
*    [No Grass in the Clouds](https://nograssintheclouds.substack.com/);
*    [Soccer Analytics Newsletter](https://socceranalytics.substack.com/);
*    [space space space](https://spacespacespaceletter.com/author/johnmuller/) by [John Muller](https://twitter.com/johnspacemuller); and
*    [Stats Perform](https://www.statsperform.com/).

### :newspaper: News Articles
*    [Data experts are becoming football's best signings](https://www.bbc.co.uk/news/business-56164159) (05/03/2021) by Justin Harper for BBC News;
*    [How a Celtic blogger nurtured by Brendan Rodgers is now lifting Leicester City](https://www.thetimes.co.uk/article/how-a-celtic-blogger-nurtured-by-brendan-rodgers-is-now-lifting-leicester-city-9hhchpnfp) (27/02/2021) by Tom Roddy for The Times;
*    [17-Year-Old Man Lands Dream Job Of Getting Paid To Watch Football All Day](https://www.sportbible.com/football/news-17-year-old-man-lands-dream-job-of-getting-paid-to-watch-football-20210204) bt Adnan Riaz for Sport Bible;
*    [Aged 17 and getting paid to watch football all day](https://www.bbc.co.uk/news/newsbeat-55816277) (04/02/2021) by Manish Pandey for BBC News;
*    [Man City’s Big Winter Signing Is a Former Hedge Fund Brain](https://www.bloombergquint.com/markets/man-city-s-big-winter-signing-is-a-former-hedge-fund-brain) (31/01/2021) by David Dellier and Adam Blenford for Bloomberg;
*    [How data is pushing Twitter scouts and bloggers into football's big time](https://www.theguardian.com/football/2021/feb/27/how-data-is-pushing-twitter-scouts-and-bloggers-into-footballs-big-time) (27/02/2021) by [Paul MacInnes](https://twitter.com/PaulMac) for The Guardian;
*    [Revealed: expected goals being used in football's war against match-fixing](https://www.theguardian.com/football/2021/feb/13/expected-goals-being-used-in-football-war-against-match-fixing-data) (13/02/2021) by Sean Ingle for The Guardian;
*    ['What we do isn't rocket science': how Midtjylland started football's data revolution](https://www.theguardian.com/football/2020/oct/25/what-we-do-isnt-rocket-science-how-fc-midtjylland-started-footballs-data-revolution) (25/10/2020) by Sean Ingle for The Guardian;
*    [How a teenager from Bangalore became a performance analyst for Dundee United](https://www.telegraph.co.uk/football/2020/12/23/teenager-bangalore-became-performance-analyst-dundee-united/) (23/12/2020) by Tim Wigmore for The Telegraph;
*    [How the volunteers of data website Transfermarkt became influential players at European top football clubs](https://www.ftm.nl/artikelen/transfermarkt-volunteers-european-football) (18/12/2020) by Pepihn Keppel and Tom Claessens;
*    [How analysts have used lockdown to unearth football’s next hidden gems](https://www.thetimes.co.uk/article/how-analysts-have-used-lockdown-to-unearth-footballs-next-hidden-gems-hmjn6fdf3) (17/07/2020) by Dan Clark in The Times;
*    [Behind the Badge: The physicist who leads Liverpool's data department](https://www.liverpoolfc.com/news/behind-the-badge/398645-ian-graham-liverpool-fc-behind-the-badge) (15/06/2020) by Sam Williams for LiverpoolFC.com;
*    [How Soccer Scouting Has Changed, And Why It’s Never Going Back](https://www.forbes.com/sites/robertkidd/2020/05/15/how-soccer-scouting-has-changed-and-why-its-never-going-back/?sh=2a13b9421a1d) (15/05/2020) by Robert Kidd for Forbes;
*    [‘Expected threat’, ‘width per sequence’ – the statistical metrics you haven’t heard of](https://www.thetimes.co.uk/article/expected-threat-width-per-sequence-the-statistical-metrics-you-havent-heard-of-jgwk3cdsq) (13/02/2020) by Dan Clark for The Times;
*    [How Brentford flipped the script and staged a data revolution to become England’s smartest club](https://talksport.com/football/fa-cup/659667/brentford-data-revolution-england-smartest-club-championship-leicester-fa-cup/) (24/01/2020) by Sean Ingle for Talksport;
*    [How Data (and Some Breathtaking Soccer) Brought Liverpool to the Cusp of Glory](https://www.nytimes.com/2019/05/22/magazine/soccer-data-liverpool.html) (22/05/2019) by Bruce Schoenfeld for The New York Times;
*    [Brexit Could Drastically Change English Soccer](https://fivethirtyeight.com/features/brexit-could-drastically-change-english-soccer/) (11/12/2018) by Laurie Shaw for FiveThirtyEight;
*    [Soccer's Moneyball Moment: How Enhanced Analytics Are Changing The Game](https://www.forbes.com/sites/robertkidd/2018/11/19/soccers-moneyball-moment-how-enhanced-analytics-are-changing-the-game/?sh=2033f6bf76b2) (19/11/2018) by Robert Kidd for Forbes;
*    [2018 World Cup: Prediction Time; Up Against The Machine](https://www.forbes.com/sites/bobbymcmahon/2018/06/13/2018-world-cup-prediction-time-me-against-the-machine/#7394956b61fd) (13/06/2018) by Bobby McMahon for Forbes;
*    [Home advantage, unconscious bias and the boisterous crowds who influence referees](https://inews.co.uk/sport/football/liverpool-vs-roma-home-advantage-referee-bias-147212) (23/04/2018) by Tim Wigmore for iNews;
*    [The Premier League is losing its competitive balance – that should be cause for concern](https://inews.co.uk/sport/football/premier-league-competitive-balance-123119) (02/02/2018) by Tim Wigmore for iNews;
*    [Expected goals and Big Football Data: the statistics revolution that is here to stay](https://www.theguardian.com/football/2017/mar/30/expected-goals-big-football-data-leicester-city-norwich) (03/03/2017) by [Paul MacInnes](https://twitter.com/PaulMac) in The Guardian;
*    [How computer analysts took over at Britain's top football clubs](https://www.theguardian.com/football/2014/mar/09/premier-league-football-clubs-computer-analysts-managers-data-winning) (09/03/2014) by Tim Lewis for The Observer;
*    [How data analysis helps football clubs make better signings](https://www.ft.com/content/84aa8b5e-c1a9-11e8-84cd-9e601db069b8) (01/11/2018) by 
John Burn-Murdoch for The FT; and
*    [A football revolution](https://www.ft.com/content/9471db52-97bb-11e0-9c37-00144feab49a) (17/07/2011) in The FT [pay wall].

## Videos
For a YouTube playlist of over 800 Sports Analytics / Data Science videos that I have collated into one single playlist, originally for my own viewing but it may be useful to you, see [[link](https://www.youtube.com/watch?v=lLcXH_4rwr4&list=PL38nJNjpNpH9OSeTgnnVeKkzHsQUJDb70&ab_channel=FourFourTwo)]. For Football-specific Data Science lectures and seminars, see [[link](https://www.youtube.com/playlist?list=PL38nJNjpNpH-l59NupDBW7oG7CmWBgp7Y)]. For a Tableau Football specific playlist, see [[link](https://www.youtube.com/watch?v=Rx7FWugmBC4&list=PL38nJNjpNpH__B0QzZ3BA0B3AxGzt0FAl&ab_channel=TableauSoftware)].

### Webinars and Lectures
*    Laurie Shaw's Metrica Sports Tracking data series for #FoT - [Introduction](https://www.youtube.com/watch?v=8TrleFklEsE), [Measuring Physical Performance](https://www.youtube.com/watch?v=VX3T-4lB2o0), [Pitch Control modelling](https://www.youtube.com/watch?v=5X1cSehLg6s), and [Valuing Actions](https://www.youtube.com/watch?v=KXSLKwADXKI). See the following for code [[link](https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking)];
*    Lotte Bransen and Jan Van Haaren's 'Valuating Actions in Football' series for #FoT - [Valuing Actions in Football: Introduction](https://www.youtube.com/watch?v=xyyZLs_N1F0), [Valuing Actions in Football 1: From Wyscout Data to Rating Players](https://www.youtube.com/watch?v=0ol_eLLEQ64), [Valuing Actions in Football 2: Generating Features](https://www.youtube.com/watch?v=Ep9wXQgAFaE&t=42s), [Valuing Actions in Football 3: Training Machine Learning Models](https://www.youtube.com/watch?v=WlORqYIb-Gg), and [Valuing Actions in Football 4: Analyzing Models and Results](https://www.youtube.com/watch?v=w9G0z3eGCj8). See the following for code [[link](https://github.com/SciSports-Labs/fot-valuing-actions)];
*    David Sumpter's Expected Goals webinars for #FoT - [How to Build An Expected Goals Model 1: Data and Model](https://www.youtube.com/watch?v=bpjLyFyLlXs), [How to Build An Expected Goals Model 2: Statistical fitting](https://www.youtube.com/watch?v=wHOgINJ5g54), and [The Ultimate Guide to Expected Goals](https://www.youtube.com/watch?v=310_eW0hUqQ). See the following for code [3xGModel](https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython/blob/master/3xGModel.py), [4LinearRegression](https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython/blob/master/4LinearRegression.py), [5xGModelFit.py](https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython/blob/master/5xGModelFit.py), and [6MeasuresOfFit](https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython/blob/master/6MeasuresOfFit.py);
*    Peter McKeever's ['Good practice in data visualisation'](https://www.youtube.com/watch?v=md0pdsWtq_o) webinar for #FoT. See the following for code [[link](https://github.com/petermckeeverPerform/friends-of-tracking-viz-lecture)];
*    StatsPerform AI in Sport series - [Overview](https://vimeo.com/473259469/3d56393c68), [AI in Basketball](), [AI In Soccer](https://vimeo.com/515977363/be3de09fc1), and [AI in Tennis]();
*    [Google Research Football](https://www.youtube.com/watch?v=esQvSg2qeS0) by Piotr Stanczyk;
*    [Will Spearman's masterclass in Pitch Control](https://www.youtube.com/watch?v=X9PrwPyolyU&list=PL38nJNjpNpH-l59NupDBW7oG7CmWBgp7Y)] for Friends of Tracking;
*    [How Tracking Data is Used in Football and What are the Future Challenges](https://www.youtube.com/watch?v=kHTq9cwdkGA) with Javier Fernández, Sudarshan 'Suds' Gopaladesikan, Laurie Shaw, Will Spearman and David Sumpter for Friends of Tracking;
*    [Why Do Clubs Need to Embrace Analytics to Stay Competitive?](https://www.youtube.com/watch?v=kWBpxxxxLWQ) with Vosse de Boode, David Sumpter, Adrien Tarascon and Javier Fernández for Barca Innovation Hub;
*    [Valuing Actions in Football: Introduction](https://www.youtube.com/watch?v=xyyZLs_N1F0) with Lotte Bransen and Jan Van Haaren for Friends of Tracking;
*    [Routine Inspection: Measuring Playbooks for Corner Kicks](https://www.youtube.com/watch?v=yfPC1O_g-I8) by Laurie Shaw and Sudarshan 'Suds' Gopaladsikan;
*    [Tactical Insight Through Team Personas](https://www.youtube.com/watch?v=lQifhUGsDYY) by David Perdomo Meza and Daniel Girela. See accompanying blog post [[link](https://www.twenty3.sport/tactical-insight-through-team-personas-an-optapro-presentation/)];
*    [Christmas Lectures 2019: How to Get Lucky](https://youtu.be/_q4DrUHKC0Q?t=1666) with Hannah Fry. Small segment with [Tim Waskett](https://twitter.com/StoneBakedGames) @ 27mins;
*    [I’m in a Wide Open Space: Creating Opportunities at Set Pieces](https://www.youtube.com/watch?v=F_C5V9bykAg) by Dan Barnett;
*    [Long or Short? How the New Short Goal Kick Rule Is Impacting Football](https://www.youtube.com/watch?v=tKwLjkjtecA) by Tom Worville;
*    [Learning to Watch Football: Self-Supervised Representations](https://vimeo.com/398489039/80d8dcfb58) for Tracking Data by Karun Singh. See accompanying blog post [[link](https://karun.in/blog/ssr-tracking-data.html)];
*    [Identifying and Evaluating Strategies to Break down a Low Block Defence](https://vimeo.com/404694721/21fa93ada1)https://vimeo.com/404694721/21fa93ada1 by Vignesh Jayanth. See accompanying blog post [[link](https://medium.com/@VigneshJayanth1/a-case-study-of-identifying-low-blocks-and-strategies-in-football-with-fc-nordsj%C3%A6lland-294ff655fd3)];
*    [Seeing in to the Future: Modelling Football Player Movements](https://www.youtube.com/watch?v=iD-EE4nUbwI) by David Sumpter;
*    [Learning Value and Style from Soccer Event Stream Data](https://www.youtube.com/watch?v=YXsG455zYKc) by Tom Decroo;
*    Marcelo Bielsa's infamous 'Spygate PowerPoint presentation of Derby County [[link](https://www.youtube.com/watch?v=9NW985SUUEU)];
*    [Tom Goodall's Tactics, Training & Tableau: Football Tableau User Group](https://www.youtube.com/watch?v=Hy0tHU7yYHs&t=1702s). Check out his Football Tableau training courses [[link](https://www.touchlineanalytics.co.uk/);
*    [Data Robot Opening Remarks & Keynote: Making Better Decisions, Faster](https://www.datarobot.com/recordings/ai-experience-emea-on-demand/ai-experience-opening-remarks-keynote/watch/090a6990db580257e9e6046fc48ab035/) with [Brian Prestidge](https://twitter.com/brianprestidge);
*    [A Framework for Tactical Analysis and Individual Offensive Production Assessment in Soccer Using Markov Chains](https://www.metacafe.com/watch/7337475/2011_nessis_talk_by_sarah_rudd/) by [Sarah Rudd](https://twitter.com/srudd_ok). Accompanying slides [[link](http://nessis.org/nessis11/rudd.pdf)];
*    [Demystifying Tracking data Sportlogiq webinar](https://www.youtube.com/watch?v=miEWHSTYvX4) by Sam Gregory and Devin Pleuler;
*    [Data Analytics in Soccer](https://www.youtube.com/watch?v=WukQprQGbcY) by Dan Fradley;
*    [How Hammarby create the mathematically perfect pressing game](https://www.youtube.com/watch?v=s6bpn3Uox7M) by David Sumpter
*    [Hudl Presents: Performance Analysis in 2020](https://www.hudl.com/elite/events/performance-analysis-2020/watch)
*    [Self-Supervised Representations for Tracking Data](https://player.vimeo.com/video/398489039) by Karun Singh;
*    [An American Analyst in London](https://www.youtube.com/watch?v=LA9-V6_ZIUg) at SSAC 2019 with StatsBomb CEO [Ted Knutson](https://twitter.com/mixedknuts) and Houston Rockets GM Daryl Morey;
*    [Beyond the Baseline](https://www.youtube.com/watch?v=o9IjocHyBLE) by Marek Kwiatkowski;
*    [Some Things Aren't Shots](https://www.youtube.com/watch?v=5j-Ij5_3Cs8) by Thom Lawrence;
*    [Beyond Save Percentage](https://www.youtube.com/watch?v=V9_20e2ut14&t=1s) by [Derrick Yam](https://twitter.com/YAMiAM9)
*    [Expected goals demonstration](https://youtu.be/Ab4yngjjYME) by Sander Ijtsma
*    [Goals change games](https://youtu.be/IvWT7iE1iUs) by [Garry Gelade](https://twitter.com/GarryGelade)
*    [Expected goals](https://youtu.be/3rsDCxszCD0) by Dan Altman

### Ted Talks
*    [What Football Analytics can Teach Successful Organisation](https://www.youtube.com/watch?v=Sy2vc9lW5r0) by [Rasmus Ankersen](https://twitter.com/RasmusAnkersen);
*    [Soccermatics: how maths explains football](https://www.youtube.com/watch?v=Nv7JYtVbzvI) by [David Sumpter](https://twitter.com/Soccermatics)
*    [Changing the soccer transfer market with big data](https://www.youtube.com/watch?v=UMeDP-lIBD8) by [Giels Brouwer](https://twitter.com/gielsbrouwer)

### Documentaries
*    [The Numbers Game: How Data Is Changing Football](https://www.youtube.com/watch?v=lLcXH_4rwr4) - FourFourTwo Documentary;
*    [How Stats Won Football: From Moneyball to FC Midtjylland](https://www.youtube.com/watch?v=s6UcNGzE8sU) – COPA90 Stories Documentary;

### Match Highlights
*    [Footballia](https://footballia.net/) - historical matches and highlights

### Others
*    [Jeff Stelling xG rant](https://facebook.com/SoccerAM/videos/1740454985978128/); and
*    [Craig Burley xG rant](https://www.youtube.com/watch?v=JBWKGij9Y5A).

## YouTube Channels
*    [Friends of Tracking](https://www.youtube.com/channel/UCUBFJYcag8j2rm_9HkrrA7w) with David Sumpter, Javier Fernández, Laurie Shawm, Suds Gopaladesikan, Pascal Bauer, and Fran Peralta
*    [McKay Johns](https://www.youtube.com/channel/UCmqincDKps3syxvD4hbODSg)
*    [Barça Innovation Hub](https://www.youtube.com/channel/UC58nLq78KZGqxfSNFNRCgsQ) (English and Spanish)
*    [Mark Glickman](https://www.youtube.com/channel/UC-gtC2WYRAr_4eYRIUb4ovg) – for NESSIS talks, uploaded to his personal channel. Old talks are available on his [Metacafe channel](https://www.metacafe.com/channels/Mark%20Glickman/). See the official website [[link](http://www.nessis.org/)]
*    [42 Analytics](https://www.youtube.com/user/42analytics) – for SSAC conferences
*    [CMU Statistics](https://www.youtube.com/channel/UCu8Pv6IJsbQdGzRlZ5OipUg)
*    [StatsBomb](https://www.youtube.com/channel/UCmZ2ArreL9muPvH49Gaw0Bw)
*    [Opta](https://www.youtube.com/user/optasports) - including Opta Pro Forum talks
*    [STATS Insights](https://www.youtube.com/user/BloombergSports)
*    [Tifo Football](https://www.youtube.com/channel/UCGYYNGmyhZ_kwBF_lqqXdAQ)
*    [Football Whispers](https://www.youtube.com/channel/UCKrQ1kewgRUbrwl_LcqJ6pQ)
*    [Football Player Ratings](https://www.youtube.com/channel/UC64jAkIQX-hD3pSnnOmr2MA) by [Lars Magnus Hvattum](https://twitter.com/FLSimulator)
*    [The Coaches’ Voice](https://www.youtube.com/channel/UCuR-ZdVJtF3muYhYUQ-he-Q)

## Books
*    [Moneyball: The Art of Winning an Unfair Game](https://www.amazon.co.uk/Moneyball-Art-Winning-Unfair-Game/) by Michael Lewis;
*    [The Numbers Game](https://www.amazon.co.uk/Numbers-Game-Everything-About-Football/) by [Chris Anderson](https://twitter.com/soccerquant) and [David Sally](https://twitter.com/DavidSally6);
*    [Football Hackers](https://www.amazon.co.uk/Football-Hackers-Science-Data-Revolution/) by [Christoph Biermann](https://twitter.com/chbiermann);
*    [Soccermatics](https://www.amazon.co.uk/Soccermatics-Mathematical-Adventures-Pro-Bloomsbury/dp/1472924142/ref=tmm_pap_swatch_0?_encoding=UTF8&qid=&sr=) by [David Sumpter](https://twitter.com/Soccermatics);
*    [Soccernomics](https://www.amazon.co.uk/Soccernomics-England-Germany-France-Finally/) by Simon Kuper and [Stefan Szymanski](https://twitter.com/sszy);
*    [Money and Football: A Soccernomics Guide ](https://www.amazon.co.uk/dp/B06XCKCVQR/) by Simon Kuper and [Stefan Szymanski](https://twitter.com/sszy);
*    [Mathletics: How Gamblers, Managers, and Sports Enthusiasts Use Mathematics in Baseball, Basketball, and Football](https://www.amazon.co.uk/Mathletics-Gamblers-Enthusiasts-Mathematics-Basketball/) by Wayne Winston;
*    [Data Analytics in Football](https://www.amazon.co.uk/Data-Analytics-Football-Daniel-Memmert/) by [Daniel Memmert](https://twitter.com/DMemmert) and Dominik Raabe;
*    [Changing the Conversation](https://www.amazon.co.uk/Changing-Conversation-Presents-Collection-Boardrooms/) series by 21st Club;
*    [Sports Analytics: A Guide for Coaches, Managers, and Other Decision Makers](https://www.amazon.co.uk/Sports-Analytics-Coaches-Managers-Decision/) by [Ben Alamar](https://twitter.com/bencalamar);
*    [Outside the Box](https://www.amazon.co.uk/Outside-Box-Statistical-Journey-Football/) by [Duncan Alexander](https://twitter.com/oilysailor);
*    [Zonal Marking: The Making of Modern European Football](https://www.amazon.co.uk/Zonal-Marking-Making-European-Football/) by [Michael Cox](https://twitter.com/Zonal_Marking);
*    [The Mixer: The Story of Premier League Tactics, from Route One to False Nines](https://www.amazon.co.uk/Mixer-Story-Premier-League-Tactics/) by [Michael Cox](https://twitter.com/Zonal_Marking);
*    [Inverting the Pyramid](https://www.amazon.co.uk/Inverting-Pyramid-History-Football-Tactics/) by [Jonathan Wilson](https://twitter.com/jonawils);
*    [Sprawlball: A Visual Tour of the New Era of the NBA](https://www.amazon.co.uk/Sprawlball-Visual-Tour-New-Era/dp/1328767515/) by [Kirk Goldsberry](https://twitter.com/kirkgoldsberry); and
*    [Numbers Don't Lie: New Adventures in Counting and What Counts in Basketball Analytics](https://www.amazon.co.uk/Numbers-Dont-Lie-Adventures-Basketball/) by Yago Colás.

## Podcasts 
Spotify and YouTube links used where available.

### Football Analytics Podcasts
*    [All Stats Aren't We](https://open.spotify.com/show/22eR0UCjDdVXY2JTtjD3OI?si=kt_lY1m2QKukOvKvmWpsPA) with Jon Mackenzie and Josh Hobbs (Leeds United Podcast)
*    [American Soccer Analysis](https://www.americansocceranalysis.com/podcasts);
*    [Analytics FC Podcast](https://analyticsfc.co.uk/podcast/);
*    [Big Data Sports](https://open.spotify.com/show/3Kv1yl0tCt1JDpD0AxtxZ7) (Spanish) by [Marcelo Gantman](https://twitter.com/marcelogantman) and Agustin Mario Gimenez;
*    [The Dan & Omar Show](https://open.spotify.com/show/0mT1mtMmydvs6fmrOF4GZD?si=Dv_Pm99kSd2HD603Wc1ZOg) with Daniel Geey and [Omar Chaudhuri](https://twitter.com/OmarChaudhuri)
*    [Double Pivot Podcast](https://open.spotify.com/show/4lBU3spHZaQWJyUcCUbkY8);
*    [Differentgame - The Football Analytics Podcast](https://open.spotify.com/show/0EHSv20UxlqnOjaUNzdiGN?si=rc48L2eFRLCLXZyROU8GSw) by [Paul Riley](https://twitter.com/footballfactman) and Richard Shephard;
*    [Expected Value](https://open.spotify.com/show/5xFeWbaaLFepY5n73SfWwr);
*    [Fanalytics](https://open.spotify.com/show/3G3LWoSWZdHW4Gg6igjIHU) with [Mike Lewis](https://twitter.com/FanalyticsMike);
*    [First Time Finish Podcast](https://open.spotify.com/show/0qYuP8igBfNgTVvgmNvEgP) with Tom Underhill, Bence Bocsak, and [Ninad Barbadikar](https://twitter.com/ninadb_06);
*    [The Football Fanalytics Podacst](https://open.spotify.com/show/6JwWRPMaHfGicFBtl7nI3V?si=IwQ00tyTRPaBcW-0XLwS4w&nd=1);
*    [Football Today](https://open.spotify.com/show/1WRaXZgVlksph0IjsTNBaG?si=0zyUX59sTKqCRnq92SEylQ&nd=1);
*    [Laptop Gurus](https://open.spotify.com/show/3sPI2CtmRJeaShdqNjrGRH?si=1NRk7exnRWaNbqbDO0B72w);
*    [Looks Good on Paper podcast](https://open.spotify.com/show/7iJoF537QKPgDgQe7bblV2?si=QwiAfM2ZS0-Z4M74RESiKQ&nd=1) by [Felix Pate](https://twitter.com/lgopfelix);
*    [MRKT Insights](https://open.spotify.com/show/3q32QkmAXwth5VJwU8uzWt?si=8_vyLb6WQd2wTJt5MxdBoA);
*    [Measurables Podcast](https://open.spotify.com/show/1B2KCrfMM6sDfNICsyVDlW) by [Brendan Kent](https://twitter.com/brendankent);
*    [Open Source Sports](https://open.spotify.com/show/3vTtH2JJXbjrzOtEfjrqc4?si=HqpAZAmRTkGFwurl965thA) with Ron Yurko;
*    [The Scouted Football Podcast](https://open.spotify.com/show/4qYVKC8RlHCJrwrRCx0w6H?si=M6xgCGtdTjiy0wEl1e2CJw);
*    [smarterscout: The Why in Analytics](https://open.spotify.com/show/2QP4KXajJ5xOfW1ny78nAf?si=NQAf_4XtSFeQXAZi1bbupQ) by Dan Altman;
*    [Squawka Talker Football Podcast](https://open.spotify.com/show/7xqylrPDX54uo01n4erZQZ?si=XpMNQ43aQxKUa6QuB0dp2w);
*    [StatsBomb](https://open.spotify.com/show/2EgxEas2CUsGpuH5AGWnAO?si=yvTrhRLGSBm7XanWZnd7lA);
*    [Target Scouting](https://open.spotify.com/show/2SJENgKp4BrmeufJPKC2TH?si=hq4tXC3sSKGkej4VU8w40w) by Luke Griffin;
*    [Tifo Podcast](https://open.spotify.com/show/06QIGhqK31Qw1UvfHzRIDA?si=eJzpmtMeSPWUDP9fQ-5pqA);
*    [Training Ground Guru](https://open.spotify.com/show/1Kn9l6LifZ2AWmZri9XWHn);
*    [Three At The Back](https://open.spotify.com/show/4NbunP2podS7hIPD2BVlYF?si=OFwVjOucQP6LWZmnGmGqjg) by Opta Pro; and
*    [Zonal Marking](https://open.spotify.com/show/1o2ZogNQQmPKCntcdKnXPT).

### Noteable Episodes (including non-football-data-specific podcasts)
*    [All Stats Aren't We](https://open.spotify.com/show/22eR0UCjDdVXY2JTtjD3OI?si=kt_lY1m2QKukOvKvmWpsPA):
     +    [Bonus Episode: David Sumpter - The Ten Equations that Rule the World](https://open.spotify.com/episode/2aWNiGHVH29qnXdrw12Iet?si=gU5__QfvRsCCxjE7XjcRhQ)
     +    [The Weekly - Ep. 12 - Barnsley Debrief and Derby Preview](https://open.spotify.com/episode/1mJinsb8PJNlpghcGz0p4g?si=f5P51NayTJClOYscU3vTqA) with Ram Srinivas
*    [Analytics FC Podcast](https://analyticsfc.co.uk/podcast/):
     +    [Episode 27: David Sumpter](https://open.spotify.com/episode/6gG4VY5hRlIio0smhgTnWh?si=meS7GqPxR4WXf2PGMPATZw)
*    [Big Data Sports](https://open.spotify.com/show/3Kv1yl0tCt1JDpD0AxtxZ7) (Spanish) by [Marcelo Gantman](https://twitter.com/marcelogantman) and Agustin Mario Gimenez:
     +    [87: No es Moneyball: es Brentford](https://open.spotify.com/episode/3b8lnFZjm27ag2R0SUZRdZ?si=CI_LfzetQSCs2yLiQ5HMMg)
     +    [66: Tres Libros Sobre Sports Analytics Más Allá De Moneyball](https://open.spotify.com/episode/3nebrUaTswrXGtztoulM3S?si=2IvLTxFpQ9CfPPiGPyov3g)
     +    [65: Métrica Sports: La máquina de entender el juego](https://open.spotify.com/episode/5egzgcesbAzMlzZBxMmMIK?si=V7pTj8n7R9OWhNmMV62-wA) withg Bruno Dagnino
     +    [56: STATS PERFORM: Cómo es el nuevo gigante de los datos del fútbol](https://open.spotify.com/episode/0KoAJxa7bEE1qtIiw3e34y?si=Dkxu0pwHToiF5kmh5Vx6Iw)
     +    [47: Wyscout: 550 Mil Futbolistas "concentrados" En Un Software](https://open.spotify.com/episode/7vI1qM7KoJHkFoe11iX3Nj?si=v4BaWwBaSc61y-PM9F-75w)
     +    [35: Big Data Sports - 35: Analistas: Los nuevos "cracks" del fútbol ](https://open.spotify.com/episode/1e8KEFHNvLb5T0HUZS57gN?si=9XlTI81mSaKGYuSK4ADvfQ)
     +    [33: Google + IA = Fútbol en Real Time](https://open.spotify.com/episode/1e8KEFHNvLb5T0HUZS57gN?si=DDGSzoxIQaKnPoaULtMbjQ)
*    [Challengers Podcast](https://challengerspodcast.tumblr.com/):
     +    Expected goals (2016)
*    [The Conor J Show](https://open.spotify.com/show/2VeRpUoHzC7KN9zxB5N2iz?si=oSMPSpwbR7-IgxSzqlk6Ig):
     +    [The Role Mathematics plays in Sports and Politics (Part 1) | David Sumpter | TCJS #11 (1/2)](https://open.spotify.com/episode/7BBAToNN9Mt0Ol8c9bDtGS?si=5YNtRObXQMu7xYBEgLgmbQ)
     +    [Is Fake News Efficacious (Part 2) | David Sumpter | TCJS #11 (2/2)](https://open.spotify.com/episode/2BC0GxAIU96aYSqMlRUcuQ?si=dPSAmciQR3KIJG5ivx1uEg)
*    [The Derby County BlogCast](https://open.spotify.com/show/6JgsZlXILOQpIKvknAgQDA?si=sjgzZ2D3QbWezG9slwWHeQ)
     +    [January window preview](https://open.spotify.com/episode/6BPle4s00x3ZM85mcDV7Ip?si=eNATcAJUTX-2E8RDA7IDOg) with Ram Srinivas (MRKT Insights)
*    [Expected Value](https://open.spotify.com/show/5xFeWbaaLFepY5n73SfWwr?si=yn23mqUpQa-mvcL6CYWpgA)
     +    [Tyler Heaps](https://open.spotify.com/episode/3OQimhf73WILGLTKXnav2M?si=L3KjerEfRryp50MQv6fzXg)
     +    [Ben Mackriell](https://open.spotify.com/episode/0tVtnFljEX5Pkn7hSApPo7?si=ldLi3xi4TuehvpawJ7NQ0g)
     +    [Ravi Ramineni](https://open.spotify.com/episode/5CPu9WFvM5iqfCX2I1m3mR?si=MQKTbjZpSiq26WgQ198gNg)
     +    [Tom Worville](https://open.spotify.com/episode/0H11EE4Bv930scxKRqf9Ci?si=0JJ-Nq3TQMWYJwy7kHpKAw)
     +    [Opta Pro Forum with Karun Sign, David Perdomo Meza, Will Gurpinar-Morgan, Vignesh Jayanth](https://open.spotify.com/episode/3dkq9a0o2WcI10AIfCfhjN?si=z7pJF-yYSYOxtUa6JE_kcA)
     +    [Mike Goodman](https://open.spotify.com/episode/4dCaPFQgb1nRdYv6TB0ckf?si=_5dbscy_QeOrOuOYvD1DMw)
     +    [NESSIS, Part 1 - Ron Yurko & Dani Chu](https://open.spotify.com/episode/3pRxs7LYPX4LP9jGcFXudz?si=V7G5JpJxRZiMhqlPwblrWQ)
     +    [NESSIS, Part 2 - Laurie Shaw & Sam Gregory](https://open.spotify.com/episode/42z1UFcfgpx17acCCg5rip?si=Pyu8gFJxRiej9fE15Gs89A)
*    [Explore Explain](https://open.spotify.com/show/7khS5ikdwhW9kyE7GIcfdw?si=Wl1Nhh35RAehtJ_5w5p-Hw) with [Andy Kirk](https://twitter.com/visualisingdata):
     +    [S2E4 - Tom Worville](https://open.spotify.com/episode/7yqrJlGLbn1af9XSFbWPLK?si=SR0Ux69_SA-Uw-qW9cHNow)
*    [Fanalytics](https://open.spotify.com/show/3G3LWoSWZdHW4Gg6igjIHU?si=9v83huJIR-GUxAnKRyXLRA) with Mike Lewis:
     +    [Getting Your Foot in the Door](https://soundcloud.com/fanalytics/sports-analytics-getting-your-foot-in-the-door) with Sean Steffen
*    [Freakonomics](https://open.spotify.com/show/6z4NLXyHPga1UmSJsPK7G1?si=Nl7mbhOeRh64w3tp7alyyg) by Stephen J. Dubner:
     +    [Can Britain Get Its “Great” Back? (Ep. 393)](https://open.spotify.com/episode/7hh4DaXBCQtLZ17Lv9Lwg6?si=2F5C3k-IQLeIuaQMfkULMA) featuring Dr. Ian Graham @ 41m25s;
*    [Football CFB Podcast](https://open.spotify.com/show/2jTKOVU0uAND8DwprMPlC8?si=C-fBu4FHTaK9wuSgyniYjw):
     +    [Daniel Geey](https://open.spotify.com/episode/0zKYxeZ3WFI1l2wihjFNoQ?si=VpgfDIviRXGRcsOUD1BMhQ)
     +    [Football CFB with… Kieran Maguire](https://open.spotify.com/episode/1KvvfS84xGw4KFB2nwr9Fv?si=s2p3SQD3RbKy6pLqBYjimg)
*    [The Football Collective Podcast](https://open.spotify.com/show/3fqNuhWi6hkagJ1U0UDJfe?si=e10JT2ACS86A3JXyO1AzGQ):
     +    [S3 E1 | Sarthak Mondal speaks to Laurie Shaw about the advent of Data Science in Football The Football Collective Podcast](https://open.spotify.com/episode/1gJXuovD1L6VMimN5BtukS?si=Y-Ot43T8TluU7UEiSvReyg)
*    [The Football Pod](https://open.spotify.com/show/3QhwCTOvJN3AZqNalgjtnO?si=173ZCWfsTs-jktoS7Bz9XQ):
     +    [Episode 3 with David Sumpter](https://open.spotify.com/episode/4mnDHbUo097JuC2lQiFijo?si=7abgc4_vRM21jSKff04rWg)
*    [Football Today](https://open.spotify.com/show/1WRaXZgVlksph0IjsTNBaG?si=0zyUX59sTKqCRnq92SEylQ&nd=1)
     +    [Manchester City Enters Data Arms Race With Liverpool](https://open.spotify.com/episode/311rLza8goz2b2SBORBORn?si=aqZX6ooOSfGkY3312jJozA)
     +    [How Safe is Football's Data](https://open.spotify.com/episode/5DnpiT8dtVcQK8YDtBIgnz?si=XweL-JQCQbCMdTArB0X1LA)
     +    [Who Owns Football's Data](https://open.spotify.com/episode/5Cw5ovQ9qH3LEkOhawUXV7?si=jxLNeCXwTL6Z41o6xvDUzw)
     +    Can Data Save Manchester United? Featuring Tom Worville
     +    [Tony Bloom: The Betting Guru Running Brighton](https://open.spotify.com/episode/2N2EMqiyqEjwqdPM6zApIw?si=uhE9VWawSo6jPQfTaIeFCQ)
*    [Modern Soccer Coach Podcast](https://open.spotify.com/show/0mxCm5xfR1dH72GBQ5pl6t?si=P-BAw6ePR52yLGCukJyOGg) with Gary Curneen:
     +    [Ted Knutson: StatsBomb, Liverpool and the Data Revolution](https://open.spotify.com/episode/6L1qdBitr8s19qIXbgMuIQ?si=FoqAeTxdQiK_tmH_EubETw)
*    [Not The Top 20 Podcast](https://open.spotify.com/show/19Vn2WZiSZOeanPFDHYIb8?si=baqjrom8Sbyc0cYMtttMEQ):
     +    [Recruitment Chat with Jay Socik (Blades Analytic) & Introducing FIVEYARDS](https://open.spotify.com/episode/30ARjrCcCiUHAc5oD3eaqE?si=6OPTiLkPQCiobeVLG193hg)
*    [The Nutmegged Arena](https://open.spotify.com/show/5ZRtcboNN80YL8ohGA6Wos?si=oyRGiCxTSSmIM5KSWaXCOA) by The Nutmeg Assist:
     +    [Tuchel & Chelsea, Quality in the EFL bumping up & more](https://open.spotify.com/episode/0SvrUT6wlGYLbV1zcrk1JL?si=0NSd2eJ9SU6ffeGQxubbEw) with Ram Srinivas
     +    [#67 Manchester United's return to the top with Ninad Barbadikar](https://open.spotify.com/episode/7noFBqjF6U5iea1QMFsHsV?si=BUW2tRqaQqaeTMuoXaLmfA)
*    [Open Source Sports](https://open.spotify.com/show/3vTtH2JJXbjrzOtEfjrqc4?si=HqpAZAmRTkGFwurl965thA) with Ron Yurko;
     +    [Player Chemistry in Soccer](https://anchor.fm/open-source-sports/episodes/Player-Chemistry-in-Soccer-with-Lotte-Bransen-ejils5) with Lotte Bransen
*    [The Ornstein & Chapman Podcast](https://open.spotify.com/show/69AAB4ojTuK7gwy3ZdQdB9?si=ciYED_kESKqfa2K505QsrQ) with David Ornstein and Mark Chapman:
*    +    [Football Club Ownership: Data, Decisions & Competitive Edge](https://open.spotify.com/episode/6v739L7LR13BZs4sPmDeGD?si=3TRs_IunT6-pVhA78ZPgGw)
*    [The PinkUn Norwich City Podcast](https://open.spotify.com/show/4NU35xCqwl8kyUG9v8Sx2A?si=3AgoCZRRT5en1zaNVIEI-Q):
     +    [232: 'Analysing Norwich City's Recruitment' - The Rebound #3 - Ft. Data Analyst Ram Srinivas](https://open.spotify.com/episode/7idmp92m0Pfv2XiW8vOzZU?si=NCc6-ZDWSdWgum1WfVv-VA)
*    [Pinnacle Podcast](https://open.spotify.com/show/091oYrS0glFhP81fq32bpE?si=TmR79XGnRAm5987Zj33ImA):
*    +    [Serious About Betting: David Sumpter](https://open.spotify.com/episode/6Bt5L7wXDGvrSezYL2FU2O?si=IgQB1TArR9CBTnecZxb6qA)
*    [The Process](https://open.spotify.com/show/5H0uUcZGr6zw7AHRuLKP6D?si=7XUIxepzTYyVRS3fEwG7Lw) with James Allcott:
     +    [#16 The Future of Football with Ted Knutson (StatsBomb)](https://open.spotify.com/episode/4KKWkT6tAn2puAe2IqOtLq?si=Br5HbR_lRvCsO5oFf0sqOw)
*    [The Scouted Football Podcast](https://open.spotify.com/show/4qYVKC8RlHCJrwrRCx0w6H?si=hBYRN1GgSc2eSIDUMiwDfA&nd=1):
     +    [#26 Recruitment, Data and Sheffield United with Blades Analytic](https://open.spotify.com/episode/1EeM7PCLq5fBngMGdVROkN?si=7W6-FrhASsafAKvbmdY6DQ)
     +    [#56 Standout Stats: Premier League](https://open.spotify.com/episode/37SlOJmtoviAKgNanq7Fxq?si=JzBDUt7iRHCKhTPomuVjAA) with Mark Carey
*    Soccer Player Development Podcast:
     +    Episode 12 with Rasmus Ankersen - [YouTube](https://www.youtube.com/watch?v=S0iHetgqQpE)
*    [Squawka Talker Football Podcast](https://open.spotify.com/show/7xqylrPDX54uo01n4erZQZ?si=XpMNQ43aQxKUa6QuB0dp2w):
     +    [BIG interview with David Sumpter: Putting GPS trackers on under 10s football teams](https://open.spotify.com/episode/6c6vOWNhvUah7Mz01oiCgt?si=t7Sc0W8WRUS0ZnVWTaGt0g)
*    [Tifo Podcast](https://open.spotify.com/show/06QIGhqK31Qw1UvfHzRIDA?si=eJzpmtMeSPWUDP9fQ-5pqA):
     +    The Transfer Market & 21st Club withj [Omar Chaudhuri](https://twitter.com/OmarChaudhuri) - [Spotify](https://open.spotify.com/episode/4C21F4d5RedaQjYHCv451k?si=ca8BN8KaSdCwGUTaiaFEfw) and [YouTube](https://www.youtube.com/watch?v=A5psEy_V8YM)
     +    How Memphis Depay Used Data to Find His Next Club with [Giels Brouwer](https://twitter.com/Gielsbrouwer) - [Spotify](https://open.spotify.com/episode/0RpLcIdqdD81Z4vyVPgw5w?si=YFR38EX3QvOReG1xWEl7rw) and [YouTube](https://www.youtube.com/watch?v=wP7HH_ucwzo)
     +    How Do Football Clubs Actually Use Statistics? - [YouTube](https://www.youtube.com/watch?v=ktk-ocn2AMo)
     +    JJ Bull: Tactical Analysis & Coaching Badges - [Spotify](https://open.spotify.com/episode/4vOxLy5WINc40ApWW8PvI1?si=C4URrqf_SyCPMg4QaUUM1A) and [YouTube](https://www.youtube.com/watch?v=cYThVZO3RJ0)
     +    A Day in the Life Of: A Football Recruitment Analyst - [Spotify](https://open.spotify.com/episode/6lkHrtOP9IsJkV6i1hyAhL?si=phub1dNLSgSK2pfBDQuB4w) and [YouTube](https://www.youtube.com/watch?v=dq6C2okqZm4)
     +    Liverpool: Pressing, xG Concerns, and Klopp’s Future - [Spotify](https://open.spotify.com/episode/4AqlZZ0deXtY9a2Wh6wGWw?si=_beiVWuFQyq3GzL2Ngt0jg) and [YouTube](https://www.youtube.com/watch?v=o4ED05PJQFI)
     +    Understanding Stats in Football with [Nikos Overheul](https://twitter.com/noverheul) - [Spotify](https://open.spotify.com/episode/1vI6Go2NhNVwZ9w5CaPDTo?si=ZT_cUwhAQaiSK_ddH57tjw) and [YouTube]()
     +    Steve Morison: Tactical Insight & Football Psychology - [Spotify](https://open.spotify.com/episode/5n5mng71oIDM69LzGRG09O?si=7sgzhL8AQMKPCepNPiBz5g) and [YouTube](https://www.youtube.com/watch?v=0d0zMg3tD-Q)
     +    Football Tactics with [Michael Cox](https://twitter.com/Zonal_Marking) (Zonal Marking) - [Spotify](https://open.spotify.com/episode/5rzLuewrS9q8ueQToqhhI2?si=7GO64KzOQ6ulkFaVAH7tRA) and [YouTube](https://www.youtube.com/watch?v=46FRcn11RFQ)
     +    Football, Tactics & History with [Jonathan Wilson](https://twitter.com/jonawils) - [Spotify](https://open.spotify.com/episode/2d072VAbRxGmwPFJDYimut?si=7Bha0Gf6QGqdqD4pPZXJFA) and [YouTube]()
     +    The Future of Stats: xG, xA - [Spotify](https://open.spotify.com/episode/7fPpKZSt2o9SSNynayROwd?si=WxuV2PFCQ7yRdNSE-QOZ6g) and [YouTube](https://www.youtube.com/watch?v=sNCeA27sDvI)
*    [The Totally Football Show](https://open.spotify.com/show/30pUHuXuSQBSf7EfZQuEvS?si=3NahWL3IR-CBAKdXzQ9cGA) with James Richardson
     +    [03/07/2019: Football Hackers](https://open.spotify.com/episode/00lwcYEV82Pz639PPadlCf?si=2SZQOpIySw-zSsN6wczQwA) with Christoph Biermann
*    [Total Soccer Show](https://open.spotify.com/show/4bDhkcGQjbNqIGszh371y1?si=Bww9nrROTTmLT8AM__7NTg):
     +    Soccer stats and analytics with Ted Knutson (@mixedknuts) (in which Ted explains Expected Goals to Daryl) - [YouTube](https://www.youtube.com/watch?v=abPYPmgMPso)
     +    Mike L. Goodman (@TheM_L_G) talks USMNT tactical options, EPL trends, Expected Goals - [YouTube](https://www.youtube.com/watch?v=uxaQwMC0EYY)
     +    Everton Premier League preview: Mike L. Goodman (@TheM_L_G) talks Silva's style, Moise Kean, and replacing - [YouTube](https://www.youtube.com/watch?v=Fb94W2-THG0)
*    [Trademate Sports](https://open.spotify.com/show/2LPzUrtsWvz5iSayEGeEQK?si=prrlKqiwQ7-bKIUtbemkeQ):
     +    [Ep 19: Freelance Football Writer talks Data Analysis, Liverpool & Betting](https://open.spotify.com/episode/1wDpG7biQ5PxYfm45NNgaF?si=NwKrXzkKSVqzROhD-58Vsw) with Andrew Beasley
     +    [Ep 87: Mathematics Professor David Sumpter & Trademate CEO Marius Norheim - Using Mathematics in...](https://open.spotify.com/episode/6jYhTHxujga5D9j37uQbLt?si=3gwKy27dRcOgVij5bYpGzA)
*    [UCN/USF Sport Management - Sports Business Podcast](https://soundcloud.com/user-736114890):
     +    [Kenneth Cortsen talks to Laurie Shaw from Harvard University](https://soundcloud.com/user-736114890/sport-data-analytics-in-football-kenneth-cortsen-talks-to-laurie-shaw-harvard-university) 
*    [Where Others Won't]() by [Cody Royle](https://open.spotify.com/show/13w1hFUG3jzoA0IrmSlc4m?si=gmYlfec-RyibIf7fC6QMMQ):
     +    [Rasmus Ankersen - Discovering Talent](https://open.spotify.com/episode/7lkkikNGL4F1cfZy1I4kPK?si=CYWpdhF9SFWr-v605Jb64w)   

## Notable Figures / Twitter Accounts
*    [2020 Analytics Twitter Top 1,000 Power Rankings](https://github.com/anenglishgoat/analyticsTwitterInteractions/blob/main/AnalyticsTwitterPageRank.csv), calculated by [Will Thomson](https://twitter.com/AnEnglishGoat). See the Twitter list created by [Luton Town Analytics](https://twitter.com/LutonAnalytics) [[link](https://twitter.com/i/lists/1341323211993182208)];
*    [Sports Analytics Twitter list](https://twitter.com/i/lists/831946455837446144) by Jan Van Haaren;
*    [Football Analyst Community Rankings dashboard](https://public.tableau.com/profile/grecian#!/vizhome/FootballAnalystCommunityRankings/Dashboard1) by Neil Charles; and
*    [Football data Analysts spreadsheet](https://docs.google.com/spreadsheets/d/1wjMVOpupmcF4hEG7PO4lY6l2mKsldGsnkyAULQwyAp8/) by [Dan Altman](https://twitter.com/NYAsports) (few years old now but lists the OGs of football analytics).

## Career Advice
*    [Getting into Sports Analytics](https://medium.com/@GregorydSam/getting-into-sports-analytics-ddf0e90c4cce) by [Sam Gregory](https://twitter.com/GregorydSam);
*    [Getting into Sports Analytics 2.0](https://medium.com/@GregorydSam/getting-into-sports-analytics-2-0-129dfb87f5be) by [Sam Gregory](https://twitter.com/GregorydSam);
*    [Best Football Analytics Pieces](https://medium.com/@GregorydSam/best-football-analytics-pieces-e532844b12e) by [Sam Gregory](https://twitter.com/GregorydSam);
*    [How to become a football data scientist – Friends of Tracking](https://www.youtube.com/watch?v=9J8CwOtjOiw) with Pascal Bauer, Javier Fernández, Suds Gopaladesikan, Fran Peralta, and David Sumpter;
*    [HANIC Panel "How to get into Sports Analytics & Media + Analytics"](https://www.youtube.com/watch?v=oUVISEJaEMM) with Alison Lukan, Sarah Bailey, Harman Dayal, Asmae Toumi Mike Johnson, Alison Lukan;
*    [You Want to be a Performance Analyst?](https://thevideoanalyst.com/want-performance-analyst/) by The Video Analyst;
*    [What do you need to learn to work in football analytics?](https://barcainnovationhub.com/what-do-you-need-to-learn-to-work-in-football-analytics/) by David Sumpter for Barca Innovation Hub;
*    [Careers in Sports Analytics](https://www.youtube.com/watch?v=0Y46KjeVsD0);
*    [Fanalytics](https://open.spotify.com/show/3G3LWoSWZdHW4Gg6igjIHU?si=9v83huJIR-GUxAnKRyXLRA) podcast with Mike Lewis - [Getting Your Foot in the Door](https://soundcloud.com/fanalytics/sports-analytics-getting-your-foot-in-the-door) with Sean Steffen;
*    [Tom Worville Twitter thread](https://twitter.com/Worville/status/1275732993819250688); and
*    [Will Spearman's Twitter thread](https://twitter.com/the_spearman/status/1260713785138073604).

## Events and Conferences
*    [OptaPro Analytics Forum](https://www.optasportspro.com/events/);
*    [StatsBomb Conference](https://statsbomb.com/conference/);
*    Barça [Sports Tomorrow](https://sportstomorrow.net/2020/en/virtual/), [Sports Analytics Summit](https://barcainnovationhub.com/event/barca-sports-analytics-summit-2019/), and [Sports Technology Symposium](https://www.fcbarcelona.com/club/sports-technology-symposium);
*    [MIT Sloan Sports Analytics Conference](http://www.sloansportsconference.com/);
*    [New England Symposium on Statistics in Sports (NESSIS](http://www.nessis.org/);
*    [Carnegie Mellon Sports Analytics Conference](http://www.cmusportsanalytics.com/conference2018.html);
*    [CASSIS](http://cascadiasports.com/);
*    [Tactical Insights 2020 Conference at King Power Stadium](https://www.lcfc.com/tacticalinsights);
*    [Workshop on Artificial Intelligence in Team Sports (AITS)](https://ai-teamsports.weebly.com/);
*    [Workshop on Machine Learning and Data Mining for Sports Analytics](https://dtai.cs.kuleuven.be/events/MLSA20/);
*    [International Workshop on Computer Vision in Sports](https://vap.aau.dk/cvsports/);
*    [Google Sports Analytics Meetup.](https://www.youtube.com/playlist?list=PLN61gcz35HB7enamPi8bG4bFJNsBPYW27);
*    [DFB Hackathon](https://www.dfb-akademie.de/hackathon-2-sts-akademie-eintracht/-/id-11009109);
*    [PSG Sports Analytics Challenge](https://www.agorize.com/fr/challenges/xpsg?lang=en);
*    [Football Data International Forum](https://eniit.es/football-data-international-forum/);
*    [Global Training Camp](http://gtc.analyticsinsport.com/);
*    [Great Lakes Analytics Conference](https://www.uwsp.edu/cols/Pages/GLAC/analyticsconference.aspx);
*    [MathSport International](http://www.mathsportinternational.com/);
*    [Sports Analytics World Series](https://www.analyticsinsport.com/); and
*    [Sportdata & Performance Forum](https://www.sportdataperformance.com/).

## Competitions
Includes non-football competitions.

*    [NFL Big Data Bowl](https://operations.nfl.com/gameday/analytics/big-data-bowl/) (American Football) - [2021](https://www.kaggle.com/c/nfl-big-data-bowl-2021) - annual;
*    [Big Data Cup](https://www.stathletes.com/big-data-cup/) (Hockey) - annual;
*    [Google Research Football with Manchester City F.C.](https://www.kaggle.com/c/google-football) - October 2020; and
*    [Liverpool Analytics Challenge](https://soccermatics.medium.com/entries-for-the-liverpool-analytics-challenge-807f5eee12fd) (Football) - May 2020. Challenge used [Last Row Tracking-like data](https://github.com/Friends-of-Tracking-Data-FoTD/Last-Row) kindly provided by [Ricardo Tavares](https://twitter.com/rjtavares).

## Courses
*    [Mathematical Modelling of Football by Uppsala University](https://uppsala.instructure.com/courses/28112);
*    [StatsBomb Academy](https://statsbomb.com/academy/); and
*    [Barça Innovation Hub](https://barcainnovationhub.com/).

## Jobs
*    [The Video Analyst](https://thevideoanalyst.com/jobs/) - Rob Carroll posts many of the jobs going in football on his own website. Make sure to also follow him on Twitter ([@thevideoanalyst](https://twitter.com/thevideoanalyst));
*    [City Football Insights](https://twitter.com/CFG_Insights):
*    [Opta](https://www.optasports.com/about/work-for-opta/);
*    [Stats Perform Job Opportunities](https://www.statsperform.com/stats-careers/) and [link](https://performacademy.csod.com/ux/ats/careersite/3/home?c=performacademy)
*    [Statsbomb](https://statsbomb.com/careers/);
*    [Wyscout](https://wyscout.com/careers/#job-openings) and careers@wyscout.com;
*    [Hudl](https://www.hudl.com/jobs#jobs);
*    [Metrica Sports](https://apply.workable.com/metrica-sports/);
*    [Second Spectrum](https://www.secondspectrum.com/careers/opportunities.html);
*    [SciSports](https://www.scisports.com/jobs/);
*    [Football Radar](https://www.footballradar.com/careers/);
*    [Genius Sports](https://www.geniussports.com/careers) and [link](https://geniussports.gr8people.com/index.gp?method=cappportal.showPortalSearch&sysLayoutID=123);
*    [Gracenote](https://www.gracenote.com/company/careers/) and [link](https://careers.nielsen.com/en-us/?s=&post_type=openings&regions=na&locations=ca-emeryville&teams=&types=&schedules=&orderby=&order=&North+America=na&ame=&asia-pacific=&europe=&greater-china=&india=&latam=&na=ca-emeryville);
*    [Global Sports](https://www.globalsportsjobs.com/jobs);
*    [Smart Odds](https://www.smartodds.co.uk/Careers/Vacancies); and
*    [FutbolJobs](https://futboljobs.com/en/search-football-jobs/).

## Key Concepts

### Expected Goals (xG)
[TO ADD]
*    David Sumpter's Expected Goals webinars for #FoT - [How to Build An Expected Goals Model 1: Data and Model](https://www.youtube.com/watch?v=bpjLyFyLlXs), [How to Build An Expected Goals Model 2: Statistical fitting](https://www.youtube.com/watch?v=wHOgINJ5g54), and [The Ultimate Guide to Expected Goals](https://www.youtube.com/watch?v=310_eW0hUqQ). See the following for code [3xGModel](https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython/blob/master/3xGModel.py), [4LinearRegression](https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython/blob/master/4LinearRegression.py), [5xGModelFit.py](https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython/blob/master/5xGModelFit.py), and [6MeasuresOfFit](https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython/blob/master/6MeasuresOfFit.py);
*    [Expected Goal literature](https://docs.google.com/document/d/1OY0dxqXIBgncj0UDgb97zOtczC-b6JUknPFWgD77ng4/edit)

### Tracking data
*    Laurie Shaw's Metrica Sports Tracking data series for #FoT - [Introduction](https://www.youtube.com/watch?v=8TrleFklEsE), [Measuring Physical Performance](https://www.youtube.com/watch?v=VX3T-4lB2o0), [Pitch Control modelling](https://www.youtube.com/watch?v=5X1cSehLg6s), and [Valuing Actions](https://www.youtube.com/watch?v=KXSLKwADXKI). See the following for code [[link](https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking)];

### Possession Value (PV) Frameworks

#### Expected Threat (xT)
[TO ADD]

#### Valuing Actions by Estimating Probabilities (VAEP) 
*    Lotte Bransen and Jan Van Haaren's 'Valuating Actions in Football' series for #FoT - [Valuing Actions in Football: Introduction](https://www.youtube.com/watch?v=xyyZLs_N1F0), [Valuing Actions in Football 1: From Wyscout Data to Rating Players](https://www.youtube.com/watch?v=0ol_eLLEQ64), [Valuing Actions in Football 2: Generating Features](https://www.youtube.com/watch?v=Ep9wXQgAFaE&t=42s), [Valuing Actions in Football 3: Training Machine Learning Models](https://www.youtube.com/watch?v=WlORqYIb-Gg), and [Valuing Actions in Football 4: Analyzing Models and Results](https://www.youtube.com/watch?v=w9G0z3eGCj8). See the following for code [[link](https://github.com/SciSports-Labs/fot-valuing-actions)];

#### Goals Added (g+)
*    [Goals Added: Introducing a New Way to Measure Soccer](https://www.americansocceranalysis.com/home/2020/4/22/37ucr0d5urxxtryn2cfhzormdziphq)

### Player Similarity Analysis
[TO ADD]

### Player Comparison and Similarity Analysis
[TO ADD]
*    [Paul Power: How to properly compare players](https://www.youtube.com/watch?v=lRg0BCLeitM)
*    [`PCA_Player_Finder`](https://github.com/parth1902/PCA_Player_Finder) by [Parth Athale](https://twitter.com/ParthAthale);

### Reinforceement Learning for Football Simulation
*    [Google Research Football: A Novel Reinforcement Learning Environment](https://arxiv.org/pdf/1907.11180.pdf) (2020) by Karol Kurach, Anton Raichuk, Piotr Stańczyk, Michał Zając, Olivier Bachem, Lasse Espeholt, Carlos Riquelme, Damien Vincent, Marcin Michalski, Olivier Bousquet, Sylvain Gelly;
*    [`Google Research Football`](https://github.com/google-research/football) GitHub repo;
*    [Google Research Football with Manchester City F.C.](https://www.kaggle.com/c/google-football) Kaggle Competition (ended October 2020)
*    [Karol Kurach - Google Research Football](https://www.youtube.com/watch?v=Va5dIxejqx0)
*    [Karol Kurach (Google Brain) "Google Research Football: Learning to Play Football with Deep RL](https://www.youtube.com/watch?v=lsN5y2frNig)
*    [Google Research Football](https://www.youtube.com/watch?v=esQvSg2qeS0) by Piotr Stanczyk;
*    [Google's AI Plays Football…For Science!](https://www.youtube.com/watch?v=Uk9p4Kk98_g) by Two Minute Papers

## Miscellaneous
*    [Club crests](https://drive.google.com/drive/folders/1R22tOjU-gjJ3QDzwUZ8JlXGjtO4O_XaJ) available to download, put together by [Ninad Barbadikar](https://twitter.com/NinadB_06);
*    [Association of Sports Analytics Professionals](https://www.sportsanalyticsprofessionals.com/);
*    [Expected Goal literature](https://docs.google.com/document/d/1OY0dxqXIBgncj0UDgb97zOtczC-b6JUknPFWgD77ng4/edit);
*    [FIFA EPTS (Electronic Performance and Tracking Systems)](https://football-technology.fifa.com/en/media-tiles/epts/);
*    [opensport (Google Group)](https://groups.google.com/forum/#!forum/opensport); and
*    [Technical Report - 2018 FIFA World Cup](https://img.fifa.com/image/upload/evdvpfdkueqrdlbbrrus.pdf).

## Credits
Credits to the [Soccer Analytics Handbook](https://github.com/devinpleuler/analytics-handbook) by [Devin Pleuler](https://twitter.com/devinpleuler), the [Awesome Soccer Analytics](https://github.com/matiasmascioto/awesome-soccer-analytics) by [Matias Mascioto](https://twitter.com/matiasmascioto), and [Jan Van Haaren](https://twitter.com/janvanhaaren)'s [Soccer Analytics 2020 Review](https://janvanhaaren.be/2020/12/30/soccer-analytics-review-2020.html) which were all used to plug gaps in the list once it was published.
