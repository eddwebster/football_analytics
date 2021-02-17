# Edd Webster Football Analytics
This repository is a public space for the football analytics projects by [Edd Webster](https://twitter.com/eddwebster).

<p align="center">
  <a href="https://www.twitter.com/eddwebster"><img src="img/fifa21eddwebsterbanner.png"></a>
</p>


I recently accidentally deleted what was quite a well written and cited README file for this repository, unfortunately without backup. Whilst this notice remains, I am currently rewriting it to include the full list with links of: data sources, libraries & webscrapers, and favourite papers and learning materials, all of which include links to credited sources. This should be done shortly - 07/02/2021.

## About this Repository and Author
Please note, all work produced in this repository is mine and/or credited to the publicly produced code and libraries used. and is in no way related to the work and analysis I produce for my employers.

For more information about this repository and the author, I'm available through all the following channels:
*    [eddwebster.com](https://www.eddwebster.com/);
*    edd.j.webster@gmail.com;
*    [@eddwebster](https://www.twitter.com/eddwebster);
*    [linkedin.com/in/eddwebster](https://www.linkedin.com/in/eddwebster/);
*    [github/eddwebster](https://github.com/eddwebster/);
*    [public.tableau.com/profile/edd.webster](https://public.tableau.com/profile/edd.webster);
*    [kaggle.com/eddwebster](https://www.kaggle.com/eddwebster); and
*    [hackerrank.com/eddwebster](https://www.hackerrank.com/eddwebster).

## Notebooks
For code, see the notebooks subfolder, in which the workflow is divided into the following:
1.    [Webscraping](https://github.com/eddwebster/football_analytics/tree/master/notebooks/1_data_scraping);
2.    [Data Parsing](https://github.com/eddwebster/football_analytics/tree/master/notebooks/2_data_parsing);
3.    [Data Engineering](https://github.com/eddwebster/football_analytics/tree/master/notebooks/3_data_engineering);
4.    [Machine Learning](https://github.com/eddwebster/football_analytics/tree/master/notebooks/4_machine_learning); and
5.    [Data Analysis](https://github.com/eddwebster/football_analytics/tree/master/notebooks/5_data_analysis_and_projects) - projects include working with [Tracking data](https://github.com/eddwebster/football_analytics/tree/master/notebooks/5_data_analysis_and_projects/tracking_data), constructing [VAEP models](https://github.com/eddwebster/football_analytics/tree/master/notebooks/5_data_analysis_and_projects/vaep) (as introduced by SciSports), building [xG models](https://github.com/eddwebster/football_analytics/tree/master/notebooks/5_data_analysis_and_projects/xg_modeling) using Logistic Regression, Decision Trees and XGBoost, and analysing [player similarity](https://github.com/eddwebster/football_analytics/tree/master/notebooks/5_data_analysis_and_projects/player_similarity) using PCA and Factor Analysis.

## Data Sources
Due to the 100mb file size limitation in GitHub, all engineered datasets prepared in this repository have been exported and made publicly available to view and download in Google Drive. Please see the following [[link](https://drive.google.com/drive/folders/1r2Rf3CPsKnxyxtmDRIHQ2eoW5WwCzBa0?usp=sharing)]. However, all code in this repository should enable you to scrape, parse, and engineer the datasets used in the data analysis and visualisation.

Data sources featured in this repository include:
*    DAVIES estimated player evaluation data by Sam Goldberg for American Soccer Analysis;
*    ELO club rankings;
*    FIFA 15-21 player rating data;
*    KPMG player valuation data;
*    Last Row Tracking-like data by Ricardo Tavares;
*    Metrica Sports Tracking data;
*    Opta Sports match-by-match aggregated player performance data for the 11/12 season and F24 Event data for a 11/12 match of Manchester City vs. Bolton Wanders as part of the [#mcfcanalytics](https://twitter.com/search?q=%23mcfcanalytics) initiative;
*    Signality Tracking data;
*    SkillCorner broadcast Tracking data;
*    StatsBomb Open Event data;
*    StatsBomb season-on-season aggregated player performance data scraped from FBref;
*    Stats Perform CPL Event data [[link](https://drive.google.com/drive/u/0/folders/1ktlkt6f6Ujami53YCS-Lbc9BGGL8BaYA)]
*    StrataBet Chance shooting data;
*    TransferMarket player bio and fiscal data scraped using the FCrStats webscraper (pull request submitted);
*    Understat shooting and meta data including player xG values; and
*    Wyscout Event data for the 17/18 season for the 'Big 5' European leagues, Euro 2016 Chanpionship, and 2018 World Cup made available by [Luca Pappalardo](https://twitter.com/lucpappalard?). See his paper [A public data set of spatio-temporal match events in soccer competitions](https://www.nature.com/articles/s41597-019-0247-7).
*    Reference data:
     -    League-wide xT values from the 2017-18 Premier League season (12x8 grid) by Karun's Singh [[link](https://twitter.com/karun1710/)]
     -    Zones on a pitch for Tableau visualisation by [Rob Carroll](https://twitter.com/thevideoanalyst) [[link](https://drive.google.com/drive/folders/1Se0DFtsjQWmnt-G9Ihn_w8EQE4EZiblD)]

## Data Visualisation and Tableau 
For Tableau dashboards produced using the data engineered in the notebooks in this repository, please see my Tableau Public profile: [public.tableau.com/profile/edd.webster](https://public.tableau.com/profile/edd.webster). 
*    WSL dashboards and analysis [[link](https://public.tableau.com/views/EddWebsterFAWSLAnalysisandDashboard/WSLxGAnalysisDashboard?:language=es&:display_count=y&:origin=viz_share_link)];
*    ‘Big 5’ European leagues dashboards and analysis [[link](https://public.tableau.com/views/EddWebsterBig5EuropeanLeagueAnalysisandDashboards/Big5WaffleChart?:language=es&:display_count=y&:origin=viz_share_link)];
*    EFL dashboards and analysis [[link](https://public.tableau.com/views/EddWebsterEFLAnalysisandDashboards/EFLFullBackRadarDashboard?:language=es&:display_count=y&:origin=viz_share_link)];
*    StrataBet Chance dashboards and analysis [[link](https://public.tableau.com/views/EddWebsterStrataBetChanceAnalysisandDashboards/StrataBetChanceShotMapDashboard?:language=es&:display_count=y&:origin=viz_share_link)]; and
*    Opta [#mcfcanalytics](https://twitter.com/search?q=%23mcfcanalytics) dashboards and analysis [[link](https://public.tableau.com/views/EddWebsterOptaMCFCAnalyticsPL1112AnalysisandDashboards/OptaPlayerDemographicsDashboard?:language=es&:display_count=y&:origin=viz_share_link)].

## Libaries
[TO REWRITE]

## Learning Resources
*    Tableau for Sport by [Rob Carroll](https://twitter.com/thevideoanalyst) [[link](https://thevideoanalyst.com/tableau-sport/)] - completely free tutorials for using football data in Tableau

## Papers and Blog Posts
[TO REWRITE]
