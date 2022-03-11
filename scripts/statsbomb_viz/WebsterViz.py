#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 20:52:19 2022

Module for visualising StatsBomb Event data.

StatsBomb's Open Data can be found at: https://github.com/statsbomb/open-data

A repository of analysis for EURO 2020, as part of the technical assignment for the
StatsBomb Pro Services Analyst role can be found at: https://github.com/eddwebster/statsbomb

The functions in this script have be designed to read Event data, with no data engineering required beforehand. These steps are all taken care of within the function.

This script of functions can be divided into the following subsections
1. Function to draw a pitch - draw_pitch()
2. Functions to draw shot maps - create_shot_map_team(), create_shot_map_player()
3. Function to draw an xG race chart - create_xg_race_chart()
4. Functions to create OBV charts - create_obv_teams_bar_chart(), create_obv_players_bar_chart()
5. Functions to create Expected Goals plots - create_xg_diff_bar_chart(), create_xg_bar_chart(), create_xg_bar_chart_player(), create_xga_bar_chart(), create_xg_diff_scatter_plot()
6. Functions to create Passing Networks - create_passing_network()
7. Functions to create Passing Maps - create_pass_map_team(), create_pass_map_single_player(), create_pass_map_multiple_players()
8. Functions to create Heat Maps - create_heat_map_team(), create_heat_map_player()
9. Functions to create combined Heat and Pass Maps - create_heat_and_pass_map_team(), create_heat_and_pass_map_player()
10. Functions to create OBV Maps - create_obv_carries_player() and create_obv_passes_player() 

@author: Edd Webster (@eddwebster)

For more information about the author, I am available through the following channels:
- edd.j.webster@gmail.com
- https://www.eddwebster.com
- https://www.linkedin.com/in/eddwebster
- https://github.com/eddwebster/football_analytics
- https://public.tableau.com/app/profile/edd.webster
"""


# Import Libraries

## Python ≥3.5 (ideally)
import platform
import sys, getopt
assert sys.version_info >= (3, 5)
import csv

## Math Operations
import numpy as np
from math import pi

## Datetime
import datetime
from datetime import date
import time

## Data Preprocessing
import pandas as pd
import pandas_profiling as pp
import os
import re
import chardet
import random
from io import BytesIO
from pathlib import Path

## Reading Directories
import glob
import os

## Working with JSON
import json
from pandas import json_normalize

## Data Visualisation
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.patches import Arc
from matplotlib.colors import ListedColormap
import matplotlib.image as image
import matplotlib.gridspec as gridspec 
import matplotlib.patheffects as path_effects
import seaborn as sns
from PIL import Image
from highlight_text import htext
import missingno as msno
from mplsoccer.pitch import Pitch
import soccerplots
from soccerplots.radar_chart import Radar   # for custom radar visuals

## Requests and downloads
import tqdm
import requests

## Machine Learning
from scipy.spatial import ConvexHull
from scipy import stats


# Set up initial paths to subfolders
base_dir = os.path.join('..')
data_dir = os.path.join(base_dir, 'data')
img_dir = os.path.join(base_dir, 'img')
fig_dir = os.path.join(base_dir, 'img', 'fig')


#class WhoScored():
    
############################################################################
## 1) Function to draw a pitch
############################################################################
def draw_pitch(x_min=0,
                x_max=106,
                y_min=0,
                y_max=68,
                pitch_color="w",
                line_color="grey",
                line_thickness=1.5,
                point_size=20,
                orientation="horizontal",
                aspect="full",
                ax=None
                ):

    """
    Custom function to draw a football pitch in matplotlib by Peter McKeever.
    See: http://petermckeever.com/2020/10/how-to-draw-a-football-pitch/
    """

    if not ax:
        raise TypeError("This function is intended to be used with an existing fig and ax in order to allow flexibility in plotting of various sizes and in subplots.")


    if orientation.lower().startswith("h"):
        first = 0
        second = 1
        arc_angle = 0

        if aspect == "half":
            ax.set_xlim(x_max / 2, x_max + 5)

    elif orientation.lower().startswith("v"):
        first = 1
        second = 0
        arc_angle = 90

        if aspect == "half":
            ax.set_ylim(x_max / 2, x_max + 5)

    
    else:
        raise NameError("You must choose one of horizontal or vertical")

    
    ax.axis("off")

    rect = plt.Rectangle((x_min, y_min),
                        x_max, y_max,
                        facecolor=pitch_color,
                        edgecolor="none",
                        zorder=-2)

    ax.add_artist(rect)

    x_conversion = x_max / 100
    y_conversion = y_max / 100

    pitch_x = [0,5.8,11.5,17,50,83,88.5,94.2,100] # pitch x markings
    pitch_x = [x * x_conversion for x in pitch_x]

    pitch_y = [0, 21.1, 36.6, 50, 63.2, 78.9, 100] # pitch y markings
    pitch_y = [x * y_conversion for x in pitch_y]

    goal_y = [45.2, 54.8] # goal posts
    goal_y = [x * y_conversion for x in goal_y]

    # side and goal lines
    lx1 = [x_min, x_max, x_max, x_min, x_min]
    ly1 = [y_min, y_min, y_max, y_max, y_min]

    # outer boxed
    lx2 = [x_max, pitch_x[5], pitch_x[5], x_max]
    ly2 = [pitch_y[1], pitch_y[1], pitch_y[5], pitch_y[5]]

    lx3 = [0, pitch_x[3], pitch_x[3], 0]
    ly3 = [pitch_y[1], pitch_y[1], pitch_y[5], pitch_y[5]]

    # goals
    lx4 = [x_max, x_max+2, x_max+2, x_max]
    ly4 = [goal_y[0], goal_y[0], goal_y[1], goal_y[1]]

    lx5 = [0, -2, -2, 0]
    ly5 = [goal_y[0], goal_y[0], goal_y[1], goal_y[1]]

    # 6 yard boxes
    lx6 = [x_max, pitch_x[7], pitch_x[7], x_max]
    ly6 = [pitch_y[2],pitch_y[2], pitch_y[4], pitch_y[4]]

    lx7 = [0, pitch_x[1], pitch_x[1], 0]
    ly7 = [pitch_y[2],pitch_y[2], pitch_y[4], pitch_y[4]]


    # Halfway line, penalty spots, and kickoff spot
    lx8 = [pitch_x[4], pitch_x[4]]
    ly8 = [0, y_max]

    lines = [
        [lx1, ly1],
        [lx2, ly2],
        [lx3, ly3],
        [lx4, ly4],
        [lx5, ly5],
        [lx6, ly6],
        [lx7, ly7],
        [lx8, ly8],
        ]

    points = [
        [pitch_x[6], pitch_y[3]],
        [pitch_x[2], pitch_y[3]],
        [pitch_x[4], pitch_y[3]]
        ]

    circle_points = [pitch_x[4], pitch_y[3]]
    arc_points1 = [pitch_x[6], pitch_y[3]]
    arc_points2 = [pitch_x[2], pitch_y[3]]


    for line in lines:
        ax.plot(line[first], line[second],
                color=line_color,
                lw=line_thickness,
                zorder=-1)

    for point in points:
        ax.scatter(point[first], point[second],
                color=line_color,
                s=point_size,
                zorder=-1)

    circle = plt.Circle((circle_points[first], circle_points[second]),
                        x_max * 0.088,
                        lw=line_thickness,
                        color=line_color,
                        fill=False,
                        zorder=-1)

    ax.add_artist(circle)

    arc1 = Arc((arc_points1[first], arc_points1[second]),
            height=x_max * 0.088 * 2,
            width=x_max * 0.088 * 2,
            angle=arc_angle,
            theta1=128.75,
            theta2=231.25,
            color=line_color,
            lw=line_thickness,
            zorder=-1)

    ax.add_artist(arc1)

    arc2 = Arc((arc_points2[first], arc_points2[second]),
            height=x_max * 0.088 * 2,
            width=x_max * 0.088 * 2,
            angle=arc_angle,
            theta1=308.75,
            theta2=51.25,
            color=line_color,
            lw=line_thickness,
            zorder=-1)

    ax.add_artist(arc2)

    ax.set_aspect("equal")

    return ax


############################################################################
## 2) Functions to draw shot maps
############################################################################

## Define function for plotting a DataFrame of shots for a team
def create_shot_map_team(df,
                         team_name,
                         team_colour,
                         pitch_length_x,
                         pitch_length_y,
                         orientation,
                         aspect,
                         x_dimensions,
                         y_dimensions
                        ):

    """
    Function to create a shot map for an individual team, utilising the 'draw_pitch' function, created by Peter McKeever @petermckeever.
    """

    ## Data Engineering
    
    ### Exclude penalties
    df = df[df['shot_type_name'] != 'Penalty']
    
    ### Select only shots from the DataFrame if full events dataset passed through
    df_shots = df[(df['type_name'] == 'Shot') & (df['shot_outcome_name'] != 'Goal') & (df['team_name'] == team_name)]
    df_goals = df[(df['type_name'] == 'Shot') & (df['shot_outcome_name'] == 'Goal') & (df['team_name'] == team_name)]
    df_shots_and_goals = df[(df['type_name'] == 'Shot') & (df['team_name'] == team_name)]

    ### Determine the total number of shots
    total_shots = len(df_shots)
    total_goals = len(df_goals)

    ### Determine the total nxG
    total_xg = df_shots_and_goals['shot_statsbomb_xg'].sum().round(2)

    ### Define X and Y values
    y_shots = df_shots['location_x'].tolist()
    x_shots = df_shots['location_y'].tolist()
    y_goals = df_goals['location_x'].tolist()
    x_goals = df_goals['location_y'].tolist()


    ## Data Visualisation

    ### Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#F7F7F7'
    title_colour='black'
    text_colour='black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    ### Create figure 
    fig, ax = plt.subplots(figsize=(x_dimensions, y_dimensions))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)

    ### Set Gridlines 
    #ax.grid(lw=0.25, color='k', zorder=1)

    ### Draw the pitch using the 
    draw_pitch(x_min=0,
               x_max=pitch_length_x,
               y_min=0,
               y_max=pitch_length_y,
               orientation=orientation,
               aspect=aspect,
               pitch_color=background,
               line_color='#3B3B3B',
               ax=ax
              )

    ## Add Z variable for xG
    z1 = df_shots['shot_statsbomb_xg'].tolist()
    z1 = [1000 * i for i in z1]
    z2 = df_goals['shot_statsbomb_xg'].tolist()
    z2 = [1000 * i for i in z2]

    ### Define Z order
    zo = 12
    
    ## Add small legend in the bottom corner
    mSize = [0.05, 0.10, 0.2, 0.4, 0.6, 1]
    mSizeS = [1000 * i for i in mSize]
    mx = [1.5, 3.0, 5.0, 7.5, 10.625, 14.25]
    my = [115, 115, 115, 115, 115, 115]
    ax.text(7.875,
            110.5,
            'xG',
            color='#3B3B3B',
            ha='center',
            va='center',
            zorder=zo,
            fontsize=16
           )

    ### Create scatter plot of shots
    ax.scatter(x_shots,
               y_shots,
               marker='o',
               color='red',
               edgecolors='black',
              #linewidths=0.5,
               s=z1,
               alpha=0.7,
               zorder=zo,
               label='Shots'
              )

    ### Create scatter plot of goals
    ax.scatter(x_goals,
               y_goals,
               marker='*',
               color='green',
               edgecolors='black',
              #linewidths=0.5,
               s=z2,
               alpha=0.7,
               zorder=zo,
               label='Goals'
              )

    ### 
    ax.scatter(mx, my,s=mSizeS, facecolors='#3B3B3B', edgecolor='#3B3B3B', zorder=zo)
    ax.plot([1.5, 14.25], [112.25,112.25], color='#3B3B3B', lw=2, zorder=zo)

    ### 
    i = 0
    for i in range(len(mx)):
        ax.text(mx[i], my[i], mSize[i], fontsize=mSize[i]*14, color='white', zorder=zo, ha='center', va='center')


    ### Show Legend
    plt.legend()

    ### Add Plot Title
    s = '<{}>\'s Shot Map of {:,} shots and {:,} goals ({} xG)\n'
    htext.fig_htext(s.format(team_name, total_shots, total_goals, total_xg), 0.13, 0.945, highlight_colors=[team_colour], highlight_weights=['bold'], string_weight='bold', fontsize=23, fontfamily=title_font, color=text_colour)


    ### Add Plot Subtitle
    fig.text(0.13, 0.955, f'EURO 2020', fontweight='regular', fontsize=20, fontfamily=title_font, color=text_colour)


    ### Add UEFA EURO 2020 logo
    #ax2 = fig.add_axes([0.765, 0.769, 0.12, 0.12])
    ax2 = fig.add_axes([0.115, 0.035, 0.12, 0.12])
    ax2.axis('off')
    img = image.imread('../img/competitions/uefa_euro_2020.png')
    ax2.imshow(img)


    ### Add StatsBomb logo
    ax3 = fig.add_axes([0.63, -0.018, 0.15, 0.15])
    ax3.axis('off')
    img = image.imread('../img/logos/stats-bomb-logo.png')
    ax3.imshow(img)


    ### Add StatsBomb 360 logo
    ax4 = fig.add_axes([0.792, 0.0235, 0.07, 0.07])
    ax4.axis('off')
    img = image.imread('../img/logos/stats-bomb-360-logo.png')
    ax4.imshow(img)


    ### Footnote
    plt.figtext(0.13,
                -0.03,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb. Excluding penalties.\n',
                fontstyle='italic',
                fontsize=15, 
                fontfamily=main_font,
                color=text_colour
               )


    ### Save figure
    if not os.path.exists(fig_dir + f'/shots_{orientation}_{aspect}.png'):
        plt.savefig(fig_dir + f'/shots_{orientation}_{aspect}.png', bbox_inches='tight', dpi=300)
    else:
        pass


    ### Show plt
    plt.tight_layout()
    plt.show()


## Define function for plotting a DataFrame of shots
def create_shot_map_player(df,
                           player_name,
                           team_of_interest,
                           team_colour,
                           pitch_length_x,
                           pitch_length_y,
                           orientation,
                           aspect,
                           x_dimensions,
                           y_dimensions
                          ):

    """
    Function to create a shot map for individual players, utilising the 'draw_pitch' function, created by Peter McKeever @petermckeever.
    """

    ## Data Engineering
    
    ### Exclude penalties
    df = df[df['shot_type_name'] != 'Penalty']
    
    ### Select only shots from the DataFrame if full events dataset passed through
    df_shots = df[(df['type_name'] == 'Shot') & (df['shot_outcome_name'] != 'Goal') & (df['player_name'] == player_name)]
    df_goals = df[(df['type_name'] == 'Shot') & (df['shot_outcome_name'] == 'Goal') & (df['player_name'] == player_name)]
    df_shots_and_goals = df[(df['type_name'] == 'Shot') & (df['player_name'] == player_name)]

    ### Determine the total number of shots
    total_shots = len(df_shots)
    total_goals = len(df_goals)

    ### Determine the total nxG
    total_xg = df_shots_and_goals['shot_statsbomb_xg'].sum().round(2)

    ### Define X and Y values
    y_shots = df_shots['location_x'].tolist()
    x_shots = df_shots['location_y'].tolist()
    y_goals = df_goals['location_x'].tolist()
    x_goals = df_goals['location_y'].tolist()


    ## Data Visualisation

    ### Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#F7F7F7'
    title_colour='black'
    text_colour='black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    ### Create figure 
    fig, ax = plt.subplots(figsize=(x_dimensions, y_dimensions))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)

    ### Set Gridlines 
    #ax.grid(lw=0.25, color='k', zorder=1)

    ### Draw the pitch using the 
    draw_pitch(x_min=0,
               x_max=pitch_length_x,
               y_min=0,
               y_max=pitch_length_y,
               orientation=orientation,
               aspect=aspect,
               pitch_color=background,
               line_color='#3B3B3B',
               ax=ax
              )

    ## Add Z variable for xG
    z1 = df_shots['shot_statsbomb_xg'].tolist()
    z1 = [1000 * i for i in z1]
    z2 = df_goals['shot_statsbomb_xg'].tolist()
    z2 = [1000 * i for i in z2]

    ### Define Z order
    zo = 12
    
    ## Add small legend in the bottom corner
    mSize = [0.05, 0.10, 0.2, 0.4, 0.6, 1]
    mSizeS = [1000 * i for i in mSize]
    mx = [1.5, 3.0, 5.0, 7.5, 10.625, 14.25]
    my = [115, 115, 115, 115, 115, 115]
    ax.text(7.875,
            110.5,
            'xG',
            color='#3B3B3B',
            ha='center',
            va='center',
            zorder=zo,
            fontsize=16
           )

    ### Create scatter plot of shots
    ax.scatter(x_shots,
               y_shots,
               marker='o',
               color='red',
               edgecolors='black',
              #linewidths=0.5,
               s=z1,
               alpha=0.7,
               zorder=zo,
               label='Shots'
              )

    ### Create scatter plot of goals
    ax.scatter(x_goals,
               y_goals,
               marker='*',
               color='green',
               edgecolors='black',
              #linewidths=0.5,
               s=z2,
               alpha=0.7,
               zorder=zo,
               label='Goals'
              )

    ### 
    ax.scatter(mx, my,s=mSizeS, facecolors='#3B3B3B', edgecolor='#3B3B3B', zorder=zo)
    ax.plot([1.5, 14.25], [112.25,112.25], color='#3B3B3B', lw=2, zorder=zo)

    ### 
    i = 0
    for i in range(len(mx)):
        ax.text(mx[i], my[i], mSize[i], fontsize=mSize[i]*14, color='white', zorder=zo, ha='center', va='center')


    ### Show Legend
    plt.legend()

    ### Add Plot Title
    s = '{}\'s Shot Map of {:,} shots and {:,} goals for <{}> ({} xG)\n'
    htext.fig_htext(s.format(player_name, total_shots, total_goals, team_of_interest, total_xg), 0.13, 0.945, highlight_colors=[team_colour], highlight_weights=['bold'], string_weight='bold', fontsize=23, fontfamily=title_font, color=text_colour)


    ### Add Plot Subtitle
    fig.text(0.13, 0.955, f'EURO 2020', fontweight='regular', fontsize=20, fontfamily=title_font, color=text_colour)


    ### Add UEFA EURO 2020 logo
    #ax2 = fig.add_axes([0.765, 0.769, 0.12, 0.12])
    ax2 = fig.add_axes([0.115, 0.035, 0.12, 0.12])
    ax2.axis('off')
    img = image.imread('../img/competitions/uefa_euro_2020.png')
    ax2.imshow(img)


    ### Add StatsBomb logo
    ax3 = fig.add_axes([0.63, -0.018, 0.15, 0.15])
    ax3.axis('off')
    img = image.imread('../img/logos/stats-bomb-logo.png')
    ax3.imshow(img)


    ### Add StatsBomb 360 logo
    ax4 = fig.add_axes([0.792, 0.0235, 0.07, 0.07])
    ax4.axis('off')
    img = image.imread('../img/logos/stats-bomb-360-logo.png')
    ax4.imshow(img)


    ### Footnote
    plt.figtext(0.13,
                -0.03,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb. Excluding penalties.\n',
                fontstyle='italic',
                fontsize=15, 
                fontfamily=main_font,
                color=text_colour
               )


    ### Save figure
    if not os.path.exists(fig_dir + f'/shots_{orientation}_{aspect}.png'):
        plt.savefig(fig_dir + f'/shots_{orientation}_{aspect}.png', bbox_inches='tight', dpi=300)
    else:
        pass


    ### Show plt
    plt.tight_layout()
    plt.show()



############################################################################
## 3) Function to draw an xG race chart
############################################################################

## Define function for plotting a DataFrame of shots
def create_xg_race_chart(df,
                         home_team,
                         away_team,
                         home_colour,
                         away_colour,
                         mins_limit,
                         subtitle,
                         x_dimensions,
                         y_dimensions
                         ):

    """
    Function to create an xG race chart.
    """
    
    ## Data Engineering
    
    ### Sort DataFrame 
    df = df.sort_values(['match_id', 'index'], ascending=[True, True])

    
    ### Filter DataFrame

    #### Cut off data before penalties
    df = df[df['minute'] < mins_limit]

    #### Filter all Events for Shots and Goals
    df = df[(df['home_team_name'] == home_team) & (df['away_team_name'] == away_team)].reset_index(drop=True)
    df_shots = df[(df['type_name'] == 'Shot')].reset_index(drop=True)
    df_goals = df[(df['type_name'] == 'Shot') & (df['shot_outcome_name'] == 'Goal')].reset_index(drop=True)


    ### Create four lists to plot the different xG values - home, away, xG, and minutes. We start these with zero so our charts will start at 0
    h_xG = [0]
    a_xG = [0]
    h_min = [0]
    a_min = [0]
    h_min_goals = []
    a_min_goals = []

    ### Define team names from the DataFrame
    hteam = home_team
    ateam = away_team


    ### For loop to append the xG and minute for both the Home and Away teams
    for i in range(len(df_shots['shot_statsbomb_xg'])):
        if df_shots['team_name'][i]==hteam:
            h_xG.append(df_shots['shot_statsbomb_xg'][i])
            h_min.append(df_shots['minute'][i])
            if df_shots['shot_outcome_name'][i]=='Goal':
                h_min_goals.append(df_shots['minute'][i])
        if df_shots['team_name'][i]==ateam:
            a_xG.append(df_shots['shot_statsbomb_xg'][i])
            a_min.append(df_shots['minute'][i])
            if df_shots['shot_outcome_name'][i]=='Goal':
                a_min_goals.append(df_shots['minute'][i])


    ### Function cumulative add xG values xG. Goes through the list and adds the xG values together
    def nums_cumulative_sum(nums_list):
        return [sum(nums_list[:i+1]) for i in range(len(nums_list))]


    ### Apply defned nums_cumulative_sum function to the home and away xG lists
    h_cumulative = nums_cumulative_sum(h_xG)
    a_cumulative = nums_cumulative_sum(a_xG)


    ### Find the total xG. Create a new variable from the last item in the cumulative list
    #alast = round(a_cumulative[-1],2)
    #hlast = round(h_cumulative[-1],2)
    hlast = h_cumulative[-1]
    alast = a_cumulative[-1]


    ### Determine the final cumulative xG (used for the title)
    h_final_xg = round(float(hlast), 2)
    a_final_xg = round(float(alast), 2)

    ### Determine the last minute
    last_min = max(df['minute'])


    ### Append last minute to list
    h_min.append(last_min)
    a_min.append(last_min)


    ### Append last (final) xG to 
    h_cumulative.append(hlast)
    a_cumulative.append(alast)


    ### Determine the maximum xG (used to determine the height of the y-axis)
    xg_max = max(alast, hlast)


    ### Create lists of the time and cumulative xG at the time Away goals were scored

    #### Empty list for the indexes of Away goals
    a_goals_indexes = []

    #### Create list of the indexes for Away goals
    for i in range(len(a_min)):
        if a_min[i] in a_min_goals:
            a_goals_indexes.append(i)

    #### Empty list for the cumulative xG at the moment Away goals are scored
    a_cumulative_goals = []

    #### Create list of the cumulative xG at the moment Away goals are scored
    for i in a_goals_indexes:
        a_cumulative_goals.append(a_cumulative[i])


    ### Create lists of the time and cumulative xG at the time Home goals were scored

    #### Empty list for the indexes of Home goals
    h_goals_indexes = []

    #### Create list of the indexes for Home goals
    for i in range(len(h_min)):
        if h_min[i] in h_min_goals:
            h_goals_indexes.append(i)

    #### Empty list for the cumulative xG at the moment Home goals are scored
    h_cumulative_goals = []

    #### Create list of the cumulative xG at the moment Home goals are scored
    for i in h_goals_indexes:
        h_cumulative_goals.append(h_cumulative[i])



    ## Data Visualisation

    ### Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background = '#F7F7F7'
    title_colour = 'black'
    text_colour = 'black'
    filler = 'grey'
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams.update({'font.size':15})


    ### Create figure 
    fig, ax = plt.subplots(figsize=(x_dimensions, y_dimensions))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)


    ### Add a grid and set gridlines
    ax.grid(linestyle='dotted',
            linewidth=0.25,
            color='#3B3B3B',
            axis='y',
            zorder=1
        )

    ### Remove top and right spines, colour bttom and left
    spines = ['top', 'right', 'bottom', 'left']
    for s in spines:
        if s in ['top', 'right']:
            ax.spines[s].set_visible(False)
        else:
            ax.spines[s].set_color(text_colour)


    ### Plot xG Race Chart - step chart
    ax.step(x=h_min, y=h_cumulative, color=home_colour, label=hteam, linewidth=5, where='post')
    ax.step(x=a_min, y=a_cumulative, color=away_colour, label=ateam, linewidth=5, where='post')


    ### Plot goals - scatter plot
    ax.scatter(x=h_min_goals, y=h_cumulative_goals, s=1200, color=home_colour, edgecolors=background, marker='*', alpha=1, linewidth=0.5, zorder=2)
    ax.scatter(x=a_min_goals, y=a_cumulative_goals, s=1200, color=away_colour, edgecolors=background, marker='*', alpha=1, linewidth=0.5, zorder=2)


    ### Show Legend
    #plt.legend()     # commented out as colours of teams shown in the title


    ### Add Plot Title
    s = 'xG Race Chart for <{}> ({}) vs. <{}> ({})\n'
    htext.fig_htext(s.format(home_team, h_final_xg, away_team, a_final_xg), 0.04, 1.03, highlight_colors=[home_colour, away_colour], highlight_weights=['bold'], string_weight='bold', fontsize=25, fontfamily=title_font, color=text_colour)


    ### Add Plot Subtitle
    fig.text(0.04, 1.029, f'EURO 2020 {subtitle}', fontweight='regular', fontsize=20, fontfamily=title_font, color=text_colour)


    ### Add X and Y labels
    plt.xlabel('Minute', color=text_colour, fontsize=16)
    plt.ylabel('xG', color=text_colour, fontsize=16)
    plt.xticks([0, 15, 30, 45, 60, 75, 90])
    plt.xlim([0, last_min+2])
    plt.ylim([0, xg_max*1.1])    # Y axis goes to 10% greater than maximum xG


    ### Remove pips
    ax.tick_params(axis='both', length=0)


    ### Add UEFA EURO 2020 logo
    ax2 = fig.add_axes([0.89, 1.03, 0.12, 0.12])
    ax2.axis('off')
    img = image.imread('../img/competitions/uefa_euro_2020.png')
    ax2.imshow(img)


    ### Add StatsBomb logo
    ax3 = fig.add_axes([0.74, -0.090, 0.15, 0.15])
    ax3.axis('off')
    img = image.imread('../img/logos/stats-bomb-logo.png')
    ax3.imshow(img)


    ### Add StatsBomb 360 logo
    ax4 = fig.add_axes([0.905, -0.045, 0.07, 0.07])
    ax4.axis('off')
    img = image.imread('../img/logos/stats-bomb-360-logo.png')
    ax4.imshow(img)


    ### Footnote
    plt.figtext(0.04,
                -0.07,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb.\n',
                fontstyle='italic',
                fontsize=15, 
                fontfamily=main_font,
                color=text_colour
            )


    ### Save figure
    if not os.path.exists(fig_dir + f'/xg_race_map_{home_team}_{away_team}.png'):
        plt.savefig(fig_dir + f'/xg_race_map_{home_team}_{away_team}.png', bbox_inches='tight', dpi=300)
    else:
        pass

    ### Show plt
    plt.tight_layout()
    plt.show()


############################################################################
## 4) Functions to create OBV charts
############################################################################

## Define function to create a bar chart for the total OBV of teams
def create_obv_teams_bar_chart(df,
                               count_teams,
                               bar_colour,
                               games_limit,
                               selected_team_1,
                               selected_team_1_colour,
                               selected_team_2,
                               selected_team_2_colour,
                               x_dimensions,
                               y_dimensions
                              ):
    
    """
    Function to create a bar chart for the total OBV of teams.
    """
    
    ## Data Engineering
    
    ### Groupby and aggregate
    df_grouped_obv = (df
                          .groupby(['team_name'])
                          .agg({'match_id': pd.Series.nunique,
                                'obv_total_net': 'sum'})
                          .reset_index()
                     )

    ### Rename columns after groupby and aggregation
    df_grouped_obv.columns = ['team_name', 'games', 'total_obv']

    ### Calculate OBV per 90
    df_grouped_obv['obv_per_game'] = df_grouped_obv['total_obv'] / (df_grouped_obv['games'] / 90)

    ### Create a filter for a minimum number of minutes played
    df_grouped_obv = df_grouped_obv[df_grouped_obv['games'] >= games_limit]

    ### Sort by 'total_obv' decending
    df_grouped_obv = df_grouped_obv.sort_values(['obv_per_game'], ascending=[False])

    ### Reset index
    df_grouped_obv = df_grouped_obv.reset_index(drop=True)

    ### Filter DataFrame for top N team
    #df_grouped_obv = df_grouped_obv.head(count_teams)

    

    ## Data Visualisation

    ## Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background = '#f7f7f7'
    title_colour = 'black'
    text_colour = 'black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    ### Define labels and metrics
    team = df_grouped_obv['team_name']
    value = df_grouped_obv['obv_per_game']

    ### Create figure 
    fig, ax = plt.subplots(figsize =(16, 16))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)

    ### Create Horizontal Bar Plot
    bars = ax.barh(team,
                   value,
                   color=bar_colour,
                   alpha=0.75
                  )

    ### Select team of interest
    bars[selected_team_1].set_color(selected_team_1_colour)
    
    ### Select team of interest
    bars[selected_team_2].set_color(selected_team_2_colour)
    
    ### Add a grid and set gridlines
    ax.grid(linestyle='dotted',
            linewidth=0.25,
            color='#3B3B3B',
            axis='y',
            zorder=1
           )
    
    ### Remove top and right spines, colour bttom and left
    spines = ['top', 'right', 'bottom', 'left']
    for s in spines:
        if s in ['top', 'right', 'bottom', 'left']:
            ax.spines[s].set_visible(False)
        else:
            ax.spines[s].set_color(text_colour)

    ### Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    ### Add padding between axes and labels
    #ax.xaxis.set_tick_params(pad=2)
    #ax.yaxis.set_tick_params(pad=20)

    ### Add X, Y gridlines
    ax.grid(b=True,
            color='grey',
            linestyle='-.',
            linewidth=0.5,
            alpha=0.2
           )

    ### Show top values
    ax.invert_yaxis()

    ### Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+0.015, i.get_y()+0.4,
                 str(round((i.get_width()), 3)),
                 fontsize=18,
                 fontweight='regular',
                 color ='black'
                )
    
    ### Add Plot Title
    plt.figtext(0.045,
                0.99,
                f'Each Team\'s On-Ball Value Contribution ',
                fontsize=30,
                fontweight='bold', 
                color=text_colour
               )

    ### Add Plot Subtitle
    fig.text(0.045, 0.96, f'EURO 2020', fontweight='regular', fontsize=20, fontfamily=title_font, color=text_colour)
    
    ### Add UEFA EURO 2020 logo
    #ax2 = fig.add_axes([0.985, 1.03, 0.12, 0.12])
    #ax2.axis('off')
    #img = image.imread('../img/competitions/uefa_euro_2020.png')
    #ax2.imshow(img)

    ### Add StatsBomb logo
    ax3 = fig.add_axes([0.74, 0.005, 0.15, 0.15])
    ax3.axis('off')
    img = image.imread('../img/logos/stats-bomb-logo.png')
    ax3.imshow(img)

    ### Add StatsBomb 360 logo
    ax4 = fig.add_axes([0.905, 0.047, 0.07, 0.07])
    ax4.axis('off')
    img = image.imread('../img/logos/stats-bomb-360-logo.png')
    ax4.imshow(img)
    
    ### Footnote
    plt.figtext(0.045,
                -0.04,
                f'Created by Edd Webster / @eddwebster. OBV is a model that assigns a value to every action on the football pitch.\nData provided by StatsBomb.\n',
                fontstyle='italic',
                fontsize=15, 
                fontfamily=main_font,
                color=text_colour
               )

    ### Save figure
    if not os.path.exists(fig_dir + f'/total_obv_bar_chart.png'):
        plt.savefig(fig_dir + f'/total_obv_bar_chart.png', bbox_inches='tight', dpi=300)
    else:
        pass

    ### Show plt
    plt.tight_layout()
    plt.show()


## Define function to create a bar chart for the total OBV of players
def create_obv_players_bar_chart(df,
                                 lst_actions,
                                 count_players,
                                 bar_colour,
                                 mins_limit,
                                 selected_player_1,
                                 selected_player_1_colour,
                                 selected_player_2,
                                 selected_player_2_colour,
                                 x_dimensions,
                                 y_dimensions
                                ):
    
    """
    Function to create a bar chart for the total OBV of players.
    """
    
    ## Data Engineering
    
    ### 
    df = df[df['type_name'].isin(lst_actions)]
    
    ### Groupby and aggregate
    df_grouped_obv = (df
                          .groupby(['player_name', 'team_name', 'mins_total'])
                          .agg({'obv_total_net':'sum'})
                          .reset_index()
                     )

    ### Rename columns after groupby and aggregation
    df_grouped_obv.columns = ['player_name', 'country', 'mins_total', 'total_obv']

    ### Calculate OBV per 90
    df_grouped_obv['obv_p90'] = df_grouped_obv['total_obv'] / (df_grouped_obv['mins_total'] / 90)

    ### Remove players that played no minutes
    df_grouped_obv = df_grouped_obv[df_grouped_obv['mins_total'] != 0]

    ### Create a filter for a minimum number of minutes played
    df_grouped_obv = df_grouped_obv[df_grouped_obv['mins_total'] >= mins_limit]

    ### Sort by 'total_obv' decending
    df_grouped_obv = df_grouped_obv.sort_values(['obv_p90'], ascending=[False])

    ### Reset index
    df_grouped_obv = df_grouped_obv.reset_index(drop=True)

    ### Filter DataFrame for top N players
    df_grouped_obv = df_grouped_obv.head(count_players)

    

    ## Data Visualisation

    ## Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#f7f7f7'
    title_colour='black'
    text_colour='black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    ### Define labels and metrics
    player = df_grouped_obv['player_name']
    value = df_grouped_obv['obv_p90']

    ### Create figure 
    fig, ax = plt.subplots(figsize =(16, 16))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)

    ### Create Horizontal Bar Plot
    bars = ax.barh(player,
                   value,
                   color=bar_colour,
                   alpha=0.75
                  )

    ### Select team of interest
    bars[selected_player_1].set_color(selected_player_1_colour)
    
    ### Select team of interest
    bars[selected_player_2].set_color(selected_player_2_colour)
    
    ### Add a grid and set gridlines
    ax.grid(linestyle='dotted',
            linewidth=0.25,
            color='#3B3B3B',
            axis='y',
            zorder=1
           )
    
    ### Remove top and right spines, colour bttom and left
    spines = ['top', 'right', 'bottom', 'left']
    for s in spines:
        if s in ['top', 'right', 'bottom', 'left']:
            ax.spines[s].set_visible(False)
        else:
            ax.spines[s].set_color(text_colour)

    ### Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    ### Add padding between axes and labels
    #ax.xaxis.set_tick_params(pad=2)
    #ax.yaxis.set_tick_params(pad=20)

    ### Add X, Y gridlines
    ax.grid(b=True,
            color='grey',
            linestyle='-.',
            linewidth=0.5,
            alpha=0.2
           )

    ### Show top values
    ax.invert_yaxis()

    ### Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+0.015, i.get_y()+0.4,
                 str(round((i.get_width()), 3)),
                 fontsize=18,
                 fontweight='regular',
                 color ='black'
                )
    
    ### Add Plot Title
    plt.figtext(0.045,
                0.99,
                f'Top {count_players} Player\'s for On-Ball Value Contribution',
                fontsize=30,
                fontweight='bold', 
                color=text_colour
               )

    ### Add Plot Subtitle
    fig.text(0.045, 0.96, f'EURO 2020', fontweight='regular', fontsize=20, fontfamily=title_font, color=text_colour)
    
    ### Add UEFA EURO 2020 logo
    #ax2 = fig.add_axes([0.985, 1.03, 0.12, 0.12])
    #ax2.axis('off')
    #img = image.imread('../img/competitions/uefa_euro_2020.png')
    #ax2.imshow(img)

    ### Add StatsBomb logo
    ax3 = fig.add_axes([0.74, 0.005, 0.15, 0.15])
    ax3.axis('off')
    img = image.imread('../img/logos/stats-bomb-logo.png')
    ax3.imshow(img)

    ### Add StatsBomb 360 logo
    ax4 = fig.add_axes([0.905, 0.047, 0.07, 0.07])
    ax4.axis('off')
    img = image.imread('../img/logos/stats-bomb-360-logo.png')
    ax4.imshow(img)
    
    ### Footnote
    plt.figtext(0.045,
                -0.04,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb. OBV is a model that assigns a value to every action on the football pitch.\nOBV calculated for\n{lst_actions} events.\nEach player has played a minimum of {mins_limit} minutes and their OBV values are standardised per 90 minutes.\n',
                fontstyle='italic',
                fontsize=15, 
                fontfamily=main_font,
                color=text_colour
               )

    ### Save figure
    if not os.path.exists(fig_dir + f'/total_obv_bar_chart.png'):
        plt.savefig(fig_dir + f'/total_obv_bar_chart.png', bbox_inches='tight', dpi=300)
    else:
        pass

    ## Show plt
    plt.tight_layout()
    plt.show()


############################################################################
## 5) Functions to create Expected Goals plots
############################################################################

# Define function xG difference bar charts
def create_xg_diff_bar_chart(df,
                             bar_colour,
                             date_start,
                             date_end,
                             value,
                             selected_team_1,
                             selected_team_1_colour,
                             selected_team_2,
                             selected_team_2_colour,
                             subtitle,
                             x_dimensions,
                             y_dimensions
                            ):
    
    """
    Function to create a bar chart for the xG difference of each team per match.
    """
    
    ## Data Engineering

    ### Create an 'isGoal attribute'
    df['isGoal'] = np.where(((df['type_name'] == 'Shot') & (df['shot_outcome_name'] == 'Goal')), 1, 0)
    df['team'] = np.where(df['team_name'] == df['home_team_name'], df['home_team_name'], df['away_team_name'])
    df['opponent'] = np.where(df['team_name'] == df['away_team_name'], df['home_team_name'], df['away_team_name'])
    df['team_xg'] = np.where((df['team_name'] == df['team']), df['shot_statsbomb_xg'], 0)
    df['opponent_xg'] = np.where((df['team_name'] == df['opponent']), df['shot_statsbomb_xg'], 0)

    ### Filter out all goals scored from penalties
    df = df[df['minute'] < 120]
    df = df[df['shot_type_name'] != 'Penalty']

    ### Filter between two dates
    df['match_date'] = pd.to_datetime(df['match_date'])
    mask = (df['match_date'] > date_start) & (df['match_date'] <= date_end)
    df = df.loc[mask]
    
    ### Groupby and aggregate
    df_fixture_xg_1 = (df
                         .groupby(['team', 'opponent'])
                         .agg({'shot_statsbomb_xg':['sum'],
                               'isGoal':['sum'],
                               'minute':['max']
                              }
                             )
                         .reset_index() 
                      )

    ### Rename columns after groupby and aggregation
    df_fixture_xg_1.columns = ['team', 'opponent', 'team_xg', 'team_goals', 'minutes']

    ### Groupby and aggregate
    df_fixture_xg_2 = (df
                         .groupby(['opponent', 'team'])
                         .agg({'shot_statsbomb_xg':['sum'],
                               'isGoal':['sum'],
                               'minute':['max']
                              }
                             )
                         .reset_index() 
                      )

    ### Rename columns after groupby and aggregation
    df_fixture_xg_2.columns = ['opponent_2', 'team_2', 'opponent_xg', 'opponent_goals', 'minutes_2']

    ### Rearrange columns
    df_fixture_xg_2 = df_fixture_xg_2[['team_2', 'opponent_2', 'opponent_xg', 'opponent_goals', 'minutes_2']].drop_duplicates()

    ### Join the two xG DataFrames
    df_fixture_xg = df_fixture_xg_1.merge(df_fixture_xg_2, left_on=['team', 'opponent'], right_on=['opponent_2', 'team_2'], how='left')

    ### Groupby and aggregate
    df_team_grouped = (df_fixture_xg
                           .groupby(['team'])
                           .agg({'opponent':['count'],
                                 'minutes':['sum'],
                                 'team_xg':['sum'],
                                 'opponent_xg':['sum'],
                                 'team_goals':['sum'],
                                 'opponent_goals':['sum']
                                }
                               )
                           .reset_index() 
                      )

    ### Rename columns after groupby and aggregation
    df_team_grouped.columns = ['team', 'games_played', 'minutes_played', 'xg', 'xga', 'goals_scored', 'goals_conceded']

    ### Determine bespoke metrics
    df_team_grouped['xg_p90'] = df_team_grouped['xg'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['xg_per_game'] = df_team_grouped['xg'] / df_team_grouped['games_played']
    df_team_grouped['xga_p90'] = df_team_grouped['xga'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['xga_per_game'] = df_team_grouped['xga'] / df_team_grouped['games_played']
    df_team_grouped['goals_p90'] = df_team_grouped['goals_scored'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['goals_per_game'] = df_team_grouped['goals_scored'] / df_team_grouped['games_played']
    df_team_grouped['goals_conceded_p90'] = df_team_grouped['goals_conceded'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['goals_conceded_per_game'] = df_team_grouped['goals_conceded'] / df_team_grouped['games_played']
    df_team_grouped['goal_difference'] = df_team_grouped['goals_scored'] - df_team_grouped['goals_conceded']
    df_team_grouped['xg_diff'] = df_team_grouped['xg'] - df_team_grouped['xga']
    df_team_grouped['xg_diff_p90'] = df_team_grouped['xg_diff'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['xg_diff_per_game'] = df_team_grouped['xg_diff'] / df_team_grouped['games_played']

    ### Round the metrics to 2 or 3 decimal places
    df_team_grouped['xg'] = df_team_grouped['xg'].round(2)
    df_team_grouped['xga'] = df_team_grouped['xga'].round(2)
    df_team_grouped['xg_p90'] = df_team_grouped['xg_p90'].round(2)
    df_team_grouped['xg_per_game'] = df_team_grouped['xg_per_game'].round(2)
    df_team_grouped['xga_p90'] = df_team_grouped['xga_p90'].round(2)
    df_team_grouped['xga_per_game'] = df_team_grouped['xga_per_game'].round(2)
    df_team_grouped['goals_p90'] = df_team_grouped['goals_p90'].round(2)
    df_team_grouped['goals_per_game'] = df_team_grouped['goals_per_game'].round(2)
    df_team_grouped['goals_conceded_p90'] = df_team_grouped['goals_conceded_p90'].round(2)
    df_team_grouped['goals_conceded_per_game'] = df_team_grouped['goals_conceded_per_game'].round(2)
    df_team_grouped['xg_diff'] = df_team_grouped['xg_diff'].round(2)
    df_team_grouped['xg_diff_p90'] = df_team_grouped['xg_diff_p90'].round(3)
    df_team_grouped['xg_diff_per_game'] = df_team_grouped['xg_diff_per_game'].round(3)

    ### Sort by 'xg_per_game_diff' decending
    df_team_grouped = df_team_grouped.sort_values([value], ascending=[False])

    ### Reset index
    df_team_grouped = df_team_grouped.reset_index(drop=True)
    
    

    ## Data Visualisation

    ## Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#f7f7f7'    #'#313233'
    title_colour='black'
    text_colour='black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    ### Define labels and metrics
    player = df_team_grouped['team']
    value = df_team_grouped[value]

    ### Create figure 
    fig, ax = plt.subplots(figsize =(16, 16))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)
    
    ### Create Horizontal Bar Plot
    bars = ax.barh(player,
                   value,
                   color=bar_colour,
                   alpha=0.75
                  )
    
    ### Select team of interest
    bars[selected_team_1].set_color(selected_team_1_colour)

    ### Select team of interest
    bars[selected_team_2].set_color(selected_team_2_colour)
    
    ### Add a grid and set gridlines
    ax.grid(linestyle='dotted',
            linewidth=0.25,
            color='#3B3B3B',
            axis='y',
            zorder=1
           )
    
    ### Remove top and right spines, colour bttom and left
    spines = ['top', 'right', 'bottom', 'left']
    for s in spines:
        if s in ['top', 'right', 'bottom', 'left']:
            ax.spines[s].set_visible(False)
        else:
            ax.spines[s].set_color(text_colour)

    ### Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    ### Add padding between axes and labels
    ax.xaxis.set_tick_params(pad=2)
    ax.yaxis.set_tick_params(pad=20)

    ### Add X, Y gridlines
    ax.grid(b=True,
            color='grey',
            linestyle='-.',
            linewidth=0.5,
            alpha=0.2
           )

    ### Show top values
    ax.invert_yaxis()

    ### Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+0.015, i.get_y()+0.4,
                 str(round((i.get_width()), 3)),
                 fontsize=18,
                 fontweight='regular',
                 color ='black'
                )
        
    ### Add Plot Title
    plt.figtext(0.045,
                0.99,
                f'Each Country\'s xG Difference',
                fontsize=30,
                fontweight='bold', 
                color=text_colour
               )

    ### Add Plot Subtitle
    fig.text(0.045, 0.96, f'EURO 2020 - {subtitle}', fontweight='regular', fontsize=20, fontfamily=title_font, color=text_colour)

    ### Add UEFA EURO 2020 logo
    #ax2 = fig.add_axes([0.985, 1.03, 0.12, 0.12])
    #ax2.axis('off')
    #img = image.imread('../img/competitions/uefa_euro_2020.png')
    #ax2.imshow(img)

    ### Add StatsBomb logo
    ax3 = fig.add_axes([0.74, 0.005, 0.15, 0.15])
    ax3.axis('off')
    img = image.imread('../img/logos/stats-bomb-logo.png')
    ax3.imshow(img)

    ### Add StatsBomb 360 logo
    ax4 = fig.add_axes([0.905, 0.047, 0.07, 0.07])
    ax4.axis('off')
    img = image.imread('../img/logos/stats-bomb-360-logo.png')
    ax4.imshow(img)
    
    ### Footnote
    plt.figtext(0.045,
                -0.02,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb. A team\'s xG difference is their xG minus xG against. Penalties excluded.\nxG difference is standardised per 90 minutes.',
                fontstyle='italic',
                fontsize=15, 
                fontfamily=main_font,
                color=text_colour
               )
    
    ### Save figure
    if not os.path.exists(fig_dir + f'/xg_diff_bar_chart_teams.png'):
        plt.savefig(fig_dir + f'/xg_diff_bar_chart_teams.png', bbox_inches='tight', dpi=300)
    else:
        pass

    ### Show plt
    plt.tight_layout()
    plt.show()


# Define function to create an xG bar chart for teams
def create_xg_bar_chart(df,
                         bar_colour,
                         date_start,
                         date_end,
                         value,
                         selected_team_1,
                         selected_team_1_colour,
                         selected_team_2,
                         selected_team_2_colour,
                         title,
                         subtitle,
                         x_dimensions,
                         y_dimensions
                        ):
    
    """
    Function to create a bar chart for the xG of each team per match.
    """
    
    ## Data Engineering

    ### Create an 'isGoal attribute'
    df['isGoal'] = np.where(((df['type_name'] == 'Shot') & (df['shot_outcome_name'] == 'Goal')), 1, 0)
    df['team'] = np.where(df['team_name'] == df['home_team_name'], df['home_team_name'], df['away_team_name'])
    df['opponent'] = np.where(df['team_name'] == df['away_team_name'], df['home_team_name'], df['away_team_name'])
    df['team_xg'] = np.where((df['team_name'] == df['team']), df['shot_statsbomb_xg'], 0)
    df['opponent_xg'] = np.where((df['team_name'] == df['opponent']), df['shot_statsbomb_xg'], 0)

    ### Filter out all goals scored from penalties
    df = df[df['minute'] < 120]
    df = df[df['shot_type_name'] != 'Penalty']

    ### Filter between two dates
    df['match_date'] = pd.to_datetime(df['match_date'])
    mask = (df['match_date'] > date_start) & (df['match_date'] <= date_end)
    df = df.loc[mask]
    
    ### Groupby and aggregate
    df_fixture_xg_1 = (df
                         .groupby(['team', 'opponent'])
                         .agg({'shot_statsbomb_xg':['sum'],
                               'isGoal':['sum'],
                               'minute':['max']
                              }
                             )
                         .reset_index() 
                      )

    ### Rename columns after groupby and aggregation
    df_fixture_xg_1.columns = ['team', 'opponent', 'team_xg', 'team_goals', 'minutes']

    ### Groupby and aggregate
    df_fixture_xg_2 = (df
                         .groupby(['opponent', 'team'])
                         .agg({'shot_statsbomb_xg':['sum'],
                               'isGoal':['sum'],
                               'minute':['max']
                              }
                             )
                         .reset_index() 
                      )

    ### Rename columns after groupby and aggregation
    df_fixture_xg_2.columns = ['opponent_2', 'team_2', 'opponent_xg', 'opponent_goals', 'minutes_2']

    ### Rearrange columns
    df_fixture_xg_2 = df_fixture_xg_2[['team_2', 'opponent_2', 'opponent_xg', 'opponent_goals', 'minutes_2']].drop_duplicates()

    ### Join the two xG DataFrames
    df_fixture_xg = df_fixture_xg_1.merge(df_fixture_xg_2, left_on=['team', 'opponent'], right_on=['opponent_2', 'team_2'], how='left')

    ### Groupby and aggregate
    df_team_grouped = (df_fixture_xg
                           .groupby(['team'])
                           .agg({'opponent':['count'],
                                 'minutes':['sum'],
                                 'team_xg':['sum'],
                                 'opponent_xg':['sum'],
                                 'team_goals':['sum'],
                                 'opponent_goals':['sum']
                                }
                               )
                           .reset_index() 
                      )

    ### Rename columns after groupby and aggregation
    df_team_grouped.columns = ['team', 'games_played', 'minutes_played', 'xg', 'xga', 'goals_scored', 'goals_conceded']

    ### Determine bespoke metrics
    df_team_grouped['xg_p90'] = df_team_grouped['xg'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['xg_per_game'] = df_team_grouped['xg'] / df_team_grouped['games_played']
    df_team_grouped['xga_p90'] = df_team_grouped['xga'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['xga_per_game'] = df_team_grouped['xga'] / df_team_grouped['games_played']
    df_team_grouped['goals_p90'] = df_team_grouped['goals_scored'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['goals_per_game'] = df_team_grouped['goals_scored'] / df_team_grouped['games_played']
    df_team_grouped['goals_conceded_p90'] = df_team_grouped['goals_conceded'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['goals_conceded_per_game'] = df_team_grouped['goals_conceded'] / df_team_grouped['games_played']
    df_team_grouped['goal_difference'] = df_team_grouped['goals_scored'] - df_team_grouped['goals_conceded']
    df_team_grouped['xg_diff'] = df_team_grouped['xg'] - df_team_grouped['xga']
    df_team_grouped['xg_diff_p90'] = df_team_grouped['xg_diff'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['xg_diff_per_game'] = df_team_grouped['xg_diff'] / df_team_grouped['games_played']

    ### Round the metrics to 2 or 3 decimal places
    df_team_grouped['xg'] = df_team_grouped['xg'].round(2)
    df_team_grouped['xga'] = df_team_grouped['xga'].round(2)
    df_team_grouped['xg_p90'] = df_team_grouped['xg_p90'].round(2)
    df_team_grouped['xg_per_game'] = df_team_grouped['xg_per_game'].round(2)
    df_team_grouped['xga_p90'] = df_team_grouped['xga_p90'].round(2)
    df_team_grouped['xga_per_game'] = df_team_grouped['xga_per_game'].round(2)
    df_team_grouped['goals_p90'] = df_team_grouped['goals_p90'].round(2)
    df_team_grouped['goals_per_game'] = df_team_grouped['goals_per_game'].round(2)
    df_team_grouped['goals_conceded_p90'] = df_team_grouped['goals_conceded_p90'].round(2)
    df_team_grouped['goals_conceded_per_game'] = df_team_grouped['goals_conceded_per_game'].round(2)
    df_team_grouped['xg_diff'] = df_team_grouped['xg_diff'].round(2)
    df_team_grouped['xg_diff_p90'] = df_team_grouped['xg_diff_p90'].round(3)
    df_team_grouped['xg_diff_per_game'] = df_team_grouped['xg_diff_per_game'].round(3)

    ### Sort by 'xg_per_game_diff' decending
    df_team_grouped = df_team_grouped.sort_values([value], ascending=[False])

    ### Reset index
    df_team_grouped = df_team_grouped.reset_index(drop=True)
    
    

    ## Data Visualisation

    ## Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#f7f7f7'    #'#313233'
    title_colour='black'
    text_colour='black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    ### Define labels and metrics
    player = df_team_grouped['team']
    value = df_team_grouped[value]

    ### Create figure 
    fig, ax = plt.subplots(figsize =(16, 16))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)
    
    ### Create Horizontal Bar Plot
    bars = ax.barh(player,
                   value,
                   color=bar_colour,
                   alpha=0.75
                  )
    
    ### Select team of interest
    bars[selected_team_1].set_color(selected_team_1_colour)

    ### Select team of interest
    bars[selected_team_2].set_color(selected_team_2_colour)
    
    ### Add a grid and set gridlines
    ax.grid(linestyle='dotted',
            linewidth=0.25,
            color='#3B3B3B',
            axis='y',
            zorder=1
           )
    
    ### Remove top and right spines, colour bttom and left
    spines = ['top', 'right', 'bottom', 'left']
    for s in spines:
        if s in ['top', 'right', 'bottom', 'left']:
            ax.spines[s].set_visible(False)
        else:
            ax.spines[s].set_color(text_colour)

    ### Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    ### Add padding between axes and labels
    ax.xaxis.set_tick_params(pad=2)
    ax.yaxis.set_tick_params(pad=20)

    ### Add X, Y gridlines
    ax.grid(b=True,
            color='grey',
            linestyle='-.',
            linewidth=0.5,
            alpha=0.2
           )

    ### Show top values
    ax.invert_yaxis()

    ### Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+0.015, i.get_y()+0.4,
                 str(round((i.get_width()), 3)),
                 fontsize=18,
                 fontweight='regular',
                 color ='black'
                )
        
    ### Add Plot Title
    plt.figtext(0.045,
                0.99,
                f'Each Country\'s {title}',
                fontsize=30,
                fontweight='bold', 
                color=text_colour
               )

    ### Add Plot Subtitle
    fig.text(0.045, 0.96, f'EURO 2020 - {subtitle}', fontweight='regular', fontsize=20, fontfamily=title_font, color=text_colour)

    ### Add UEFA EURO 2020 logo
    #ax2 = fig.add_axes([0.985, 1.03, 0.12, 0.12])
    #ax2.axis('off')
    #img = image.imread('../img/competitions/uefa_euro_2020.png')
    #ax2.imshow(img)

    ### Add StatsBomb logo
    ax3 = fig.add_axes([0.74, 0.915, 0.15, 0.15])
    ax3.axis('off')
    img = image.imread('../img/logos/stats-bomb-logo.png')
    ax3.imshow(img)

    ### Add StatsBomb 360 logo
    ax4 = fig.add_axes([0.905, 0.957, 0.07, 0.07])
    ax4.axis('off')
    img = image.imread('../img/logos/stats-bomb-360-logo.png')
    ax4.imshow(img)
    
    ### Footnote
    plt.figtext(0.045,
                -0.04,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb. Penalties excluded.\n',
                fontstyle='italic',
                fontsize=15, 
                fontfamily=main_font,
                color=text_colour
               )
    
    ### Save figure
    if not os.path.exists(fig_dir + f'/xg_bar_chart_teams.png'):
        plt.savefig(fig_dir + f'/xg_bar_chart_teams.png', bbox_inches='tight', dpi=300)
    else:
        pass

    ## Show plt
    plt.tight_layout()
    plt.show()



# Define function to create an xG bar chart for teams
def create_xg_bar_chart_player(df,
                               bar_colour,
                               date_start,
                               date_end,
                               value,
                               count_players,
                               selected_player_1,
                               selected_player_1_colour,
                               selected_player_2,
                               selected_player_2_colour,
                               selected_player_3,
                               selected_player_3_colour,
                               title,
                               subtitle,
                               x_dimensions,
                               y_dimensions
                              ):
    
    """
    Function to create a bar chart for the xG of each team per match.
    """
    
    ## Data Engineering

    ### Create an 'isGoal attribute'
    df['isGoal'] = np.where(((df['type_name'] == 'Shot') & (df['shot_outcome_name'] == 'Goal')), 1, 0)
    df['team'] = np.where(df['team_name'] == df['home_team_name'], df['home_team_name'], df['away_team_name'])
    df['opponent'] = np.where(df['team_name'] == df['away_team_name'], df['home_team_name'], df['away_team_name'])
    df['xg'] = np.where((df['team_name'] == df['team']), df['shot_statsbomb_xg'], 0)
    df['opponent_xg'] = np.where((df['team_name'] == df['opponent']), df['shot_statsbomb_xg'], 0)

    ### Filter out all goals scored from penalties
    df = df[df['minute'] < 120]
    df = df[df['shot_type_name'] != 'Penalty']

    ### Filter between two dates
    df['match_date'] = pd.to_datetime(df['match_date'])
    mask = (df['match_date'] > date_start) & (df['match_date'] <= date_end)
    df = df.loc[mask]
    
    ### Groupby and aggregate
    df_player_grouped = (df
                         .groupby(['player_name'])
                         .agg({'shot_statsbomb_xg':['sum'],
                               'isGoal':['sum'],
                               'minute':['max']
                              }
                             )
                         .reset_index() 
                      )

    ### Rename columns after groupby and aggregation
    df_player_grouped.columns = ['player_name', 'xg', 'goals_scored', 'minutes_played']

    ### Determine bespoke metrics
    df_player_grouped['xg_p90'] = df_player_grouped['xg'] / (df_player_grouped['minutes_played'] / 90)
    df_player_grouped['goals_p90'] = df_player_grouped['goals_scored'] / (df_player_grouped['minutes_played'] / 90)

    ### Round the metrics to 2 or 3 decimal places
    df_player_grouped['xg'] = df_player_grouped['xg'].round(2)
    df_player_grouped['xg_p90'] = df_player_grouped['xg_p90'].round(2)
    df_player_grouped['goals_p90'] = df_player_grouped['goals_p90'].round(2)

    ### Sort by 'xg_p90' decending
    df_player_grouped = df_player_grouped.sort_values([value], ascending=[False])

    ### Reset index
    df_player_grouped = df_player_grouped.reset_index(drop=True)

    ### Filter DataFrame for top N players
    df_player_grouped = df_player_grouped.head(count_players)
    

    ## Data Visualisation

    ## Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#f7f7f7'    #'#313233'
    title_colour='black'
    text_colour='black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    ### Define labels and metrics
    player = df_player_grouped['player_name']
    value = df_player_grouped[value]

    ### Create figure 
    fig, ax = plt.subplots(figsize =(16, 16))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)
    
    ### Create Horizontal Bar Plot
    bars = ax.barh(player,
                   value,
                   color=bar_colour,
                   alpha=0.75
                  )
    
    ### Select team of interest
    bars[selected_player_1].set_color(selected_player_1_colour)

    ### Select team of interest
    bars[selected_player_2].set_color(selected_player_2_colour)
    
    ### Select team of interest
    bars[selected_player_3].set_color(selected_player_3_colour)
    
    ### Add a grid and set gridlines
    ax.grid(linestyle='dotted',
            linewidth=0.25,
            color='#3B3B3B',
            axis='y',
            zorder=1
           )
    
    ### Remove top and right spines, colour bttom and left
    spines = ['top', 'right', 'bottom', 'left']
    for s in spines:
        if s in ['top', 'right', 'bottom', 'left']:
            ax.spines[s].set_visible(False)
        else:
            ax.spines[s].set_color(text_colour)

    ### Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    ### Add padding between axes and labels
    ax.xaxis.set_tick_params(pad=2)
    ax.yaxis.set_tick_params(pad=20)

    ### Add X, Y gridlines
    ax.grid(b=True,
            color='grey',
            linestyle='-.',
            linewidth=0.5,
            alpha=0.2
           )

    ### Show top values
    ax.invert_yaxis()

    ### Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+0.015, i.get_y()+0.4,
                 str(round((i.get_width()), 3)),
                 fontsize=18,
                 fontweight='regular',
                 color ='black'
                )
        
    ### Add Plot Title
    plt.figtext(0.045,
                0.99,
                f'Each Player\'s {title}',
                fontsize=30,
                fontweight='bold', 
                color=text_colour
               )

    ### Add Plot Subtitle
    fig.text(0.045, 0.96, f'EURO 2020 - {subtitle}', fontweight='regular', fontsize=20, fontfamily=title_font, color=text_colour)

    ### Add UEFA EURO 2020 logo
    #ax2 = fig.add_axes([0.985, 1.03, 0.12, 0.12])
    #ax2.axis('off')
    #img = image.imread('../img/competitions/uefa_euro_2020.png')
    #ax2.imshow(img)

    ### Add StatsBomb logo
    ax3 = fig.add_axes([0.74, 0.915, 0.15, 0.15])
    ax3.axis('off')
    img = image.imread('../img/logos/stats-bomb-logo.png')
    ax3.imshow(img)

    ### Add StatsBomb 360 logo
    ax4 = fig.add_axes([0.905, 0.957, 0.07, 0.07])
    ax4.axis('off')
    img = image.imread('../img/logos/stats-bomb-360-logo.png')
    ax4.imshow(img)
    
    ### Footnote
    plt.figtext(0.045,
                -0.04,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb. Penalties excluded.\n',
                fontstyle='italic',
                fontsize=15, 
                fontfamily=main_font,
                color=text_colour
               )
    
    ### Save figure
    if not os.path.exists(fig_dir + f'/xg_bar_chart_teams.png'):
        plt.savefig(fig_dir + f'/xg_bar_chart_teams.png', bbox_inches='tight', dpi=300)
    else:
        pass

    ## Show plt
    plt.tight_layout()
    plt.show()



# Define function xGA bar charts
def create_xga_bar_chart(df,
                         bar_colour,
                         date_start,
                         date_end,
                         value,
                         selected_team_1,
                         selected_team_1_colour,
                         selected_team_2,
                         selected_team_2_colour,
                         subtitle,
                         x_dimensions,
                         y_dimensions
                        ):
    
    """
    Function to create a bar chart for the xGA of each team per match.
    """
    
    ## Data Engineering

    ### Create an 'isGoal attribute'
    df['isGoal'] = np.where(((df['type_name'] == 'Shot') & (df['shot_outcome_name'] == 'Goal')), 1, 0)
    df['team'] = np.where(df['team_name'] == df['home_team_name'], df['home_team_name'], df['away_team_name'])
    df['opponent'] = np.where(df['team_name'] == df['away_team_name'], df['home_team_name'], df['away_team_name'])
    df['team_xg'] = np.where((df['team_name'] == df['team']), df['shot_statsbomb_xg'], 0)
    df['opponent_xg'] = np.where((df['team_name'] == df['opponent']), df['shot_statsbomb_xg'], 0)

    ### Filter out all goals scored from penalties
    df = df[df['minute'] < 120]
    df = df[df['shot_type_name'] != 'Penalty']

    ### Filter between two dates
    df['match_date'] = pd.to_datetime(df['match_date'])
    mask = (df['match_date'] > date_start) & (df['match_date'] <= date_end)
    df = df.loc[mask]
    
    ### Groupby and aggregate
    df_fixture_xg_1 = (df
                         .groupby(['team', 'opponent'])
                         .agg({'shot_statsbomb_xg':['sum'],
                               'isGoal':['sum'],
                               'minute':['max']
                              }
                             )
                         .reset_index() 
                      )

    ### Rename columns after groupby and aggregation
    df_fixture_xg_1.columns = ['team', 'opponent', 'team_xg', 'team_goals', 'minutes']

    ### Groupby and aggregate
    df_fixture_xg_2 = (df
                         .groupby(['opponent', 'team'])
                         .agg({'shot_statsbomb_xg':['sum'],
                               'isGoal':['sum'],
                               'minute':['max']
                              }
                             )
                         .reset_index() 
                      )

    ### Rename columns after groupby and aggregation
    df_fixture_xg_2.columns = ['opponent_2', 'team_2', 'opponent_xg', 'opponent_goals', 'minutes_2']

    ### Rearrange columns
    df_fixture_xg_2 = df_fixture_xg_2[['team_2', 'opponent_2', 'opponent_xg', 'opponent_goals', 'minutes_2']].drop_duplicates()

    ### Join the two xG DataFrames
    df_fixture_xg = df_fixture_xg_1.merge(df_fixture_xg_2, left_on=['team', 'opponent'], right_on=['opponent_2', 'team_2'], how='left')

    ### Groupby and aggregate
    df_team_grouped = (df_fixture_xg
                           .groupby(['team'])
                           .agg({'opponent':['count'],
                                 'minutes':['sum'],
                                 'team_xg':['sum'],
                                 'opponent_xg':['sum'],
                                 'team_goals':['sum'],
                                 'opponent_goals':['sum']
                                }
                               )
                           .reset_index() 
                      )

    ### Rename columns after groupby and aggregation
    df_team_grouped.columns = ['team', 'games_played', 'minutes_played', 'xg', 'xga', 'goals_scored', 'goals_conceded']

    ### Determine bespoke metrics
    df_team_grouped['xg_p90'] = df_team_grouped['xg'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['xg_per_game'] = df_team_grouped['xg'] / df_team_grouped['games_played']
    df_team_grouped['xga_p90'] = df_team_grouped['xga'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['xga_per_game'] = df_team_grouped['xga'] / df_team_grouped['games_played']
    df_team_grouped['goals_p90'] = df_team_grouped['goals_scored'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['goals_per_game'] = df_team_grouped['goals_scored'] / df_team_grouped['games_played']
    df_team_grouped['goals_conceded_p90'] = df_team_grouped['goals_conceded'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['goals_conceded_per_game'] = df_team_grouped['goals_conceded'] / df_team_grouped['games_played']
    df_team_grouped['goal_difference'] = df_team_grouped['goals_scored'] - df_team_grouped['goals_conceded']
    df_team_grouped['xg_diff'] = df_team_grouped['xg'] - df_team_grouped['xga']
    df_team_grouped['xg_diff_p90'] = df_team_grouped['xg_diff'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['xg_diff_per_game'] = df_team_grouped['xg_diff'] / df_team_grouped['games_played']

    ### Round the metrics to 2 or 3 decimal places
    df_team_grouped['xg'] = df_team_grouped['xg'].round(2)
    df_team_grouped['xga'] = df_team_grouped['xga'].round(2)
    df_team_grouped['xg_p90'] = df_team_grouped['xg_p90'].round(2)
    df_team_grouped['xg_per_game'] = df_team_grouped['xg_per_game'].round(2)
    df_team_grouped['xga_p90'] = df_team_grouped['xga_p90'].round(2)
    df_team_grouped['xga_per_game'] = df_team_grouped['xga_per_game'].round(2)
    df_team_grouped['goals_p90'] = df_team_grouped['goals_p90'].round(2)
    df_team_grouped['goals_per_game'] = df_team_grouped['goals_per_game'].round(2)
    df_team_grouped['goals_conceded_p90'] = df_team_grouped['goals_conceded_p90'].round(2)
    df_team_grouped['goals_conceded_per_game'] = df_team_grouped['goals_conceded_per_game'].round(2)
    df_team_grouped['xg_diff'] = df_team_grouped['xg_diff'].round(2)
    df_team_grouped['xg_diff_p90'] = df_team_grouped['xg_diff_p90'].round(3)
    df_team_grouped['xg_diff_per_game'] = df_team_grouped['xg_diff_per_game'].round(3)

    ### Sort by 'xg_per_game_diff' decending
    df_team_grouped = df_team_grouped.sort_values([value], ascending=[True])

    ### Reset index
    df_team_grouped = df_team_grouped.reset_index(drop=True)
    
    

    ## Data Visualisation

    ## Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#f7f7f7'    #'#313233'
    title_colour='black'
    text_colour='black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    ### Define labels and metrics
    player = df_team_grouped['team']
    value = df_team_grouped[value]

    ### Create figure 
    fig, ax = plt.subplots(figsize =(16, 16))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)
    
    ### Create Horizontal Bar Plot
    bars = ax.barh(player,
                   value,
                   color=bar_colour,
                   alpha=0.75
                  )
    
    ### Select team of interest
    bars[selected_team_1].set_color(selected_team_1_colour)

    ### Select team of interest
    bars[selected_team_2].set_color(selected_team_2_colour)
    
    ### Add a grid and set gridlines
    ax.grid(linestyle='dotted',
            linewidth=0.25,
            color='#3B3B3B',
            axis='y',
            zorder=1
           )
    
    ### Remove top and right spines, colour bttom and left
    spines = ['top', 'right', 'bottom', 'left']
    for s in spines:
        if s in ['top', 'right', 'bottom', 'left']:
            ax.spines[s].set_visible(False)
        else:
            ax.spines[s].set_color(text_colour)

    ### Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    ### Add padding between axes and labels
    ax.xaxis.set_tick_params(pad=2)
    ax.yaxis.set_tick_params(pad=20)

    ### Add X, Y gridlines
    ax.grid(b=True,
            color='grey',
            linestyle='-.',
            linewidth=0.5,
            alpha=0.2
           )

    ### Show top values
    ax.invert_yaxis()

    ### Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+0.015, i.get_y()+0.4,
                 str(round((i.get_width()), 3)),
                 fontsize=18,
                 fontweight='regular',
                 color ='black'
                )
        
    ### Add Plot Title
    plt.figtext(0.045,
                0.99,
                f'Each Country\'s xG Conceded',
                fontsize=30,
                fontweight='bold', 
                color=text_colour
               )

    ### Add Plot Subtitle
    fig.text(0.045, 0.96, f'EURO 2020 - {subtitle}', fontweight='regular', fontsize=20, fontfamily=title_font, color=text_colour)

    ### Add UEFA EURO 2020 logo
    #ax2 = fig.add_axes([0.985, 1.03, 0.12, 0.12])
    #ax2.axis('off')
    #img = image.imread('../img/competitions/uefa_euro_2020.png')
    #ax2.imshow(img)

    ### Add StatsBomb logo
    ax3 = fig.add_axes([0.74, 0.915, 0.15, 0.15])
    ax3.axis('off')
    img = image.imread('../img/logos/stats-bomb-logo.png')
    ax3.imshow(img)

    ### Add StatsBomb 360 logo
    ax4 = fig.add_axes([0.905, 0.957, 0.07, 0.07])
    ax4.axis('off')
    img = image.imread('../img/logos/stats-bomb-360-logo.png')
    ax4.imshow(img)
    
    ### Footnote
    plt.figtext(0.045,
                -0.04,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb.\nA team\'s xG Conceded is the total xG of the chances of each country\'s opponents. Penalties excluded.\n',
                fontstyle='italic',
                fontsize=15, 
                fontfamily=main_font,
                color=text_colour
               )
    
    ### Save figure
    if not os.path.exists(fig_dir + f'/xga_bar_chart_teams.png'):
        plt.savefig(fig_dir + f'/xga_bar_chart_teams.png', bbox_inches='tight', dpi=300)
    else:
        pass

    ## Show plt
    plt.tight_layout()
    plt.show()


# Define function xG difference scatter plots
def create_xg_diff_scatter_plot(df,
                                colour_scale,
                                x_dimensions,
                                y_dimensions
                               ):
    
    """
    Function to create a scatter plot of the xG difference for each team.
    """

    ## Data Engineering

    ### Create an 'isGoal attribute'
    df['isGoal'] = np.where(((df['type_name'] == 'Shot') & (df['shot_outcome_name'] == 'Goal')), 1, 0)
    df['team'] = np.where(df['team_name'] == df['home_team_name'], df['home_team_name'], df['away_team_name'])
    df['opponent'] = np.where(df['team_name'] == df['away_team_name'], df['home_team_name'], df['away_team_name'])
    df['team_xg'] = np.where((df['team_name'] == df['team']), df['shot_statsbomb_xg'], 0)
    df['opponent_xg'] = np.where((df['team_name'] == df['opponent']), df['shot_statsbomb_xg'], 0)

    ### Filter out all goals scored from penalties
    df = df[df['minute'] < 120]
    df = df[df['shot_type_name'] != 'Penalty']

    ### Groupby and aggregate
    df_fixture_xg_1 = (df
                         .groupby(['team', 'opponent'])
                         .agg({'shot_statsbomb_xg':['sum'],
                               'isGoal':['sum'],
                               'minute':['max']
                              }
                             )
                         .reset_index() 
                      )

    ### Rename columns after groupby and aggregation
    df_fixture_xg_1.columns = ['team', 'opponent', 'team_xg', 'team_goals', 'minutes']

    ### Groupby and aggregate
    df_fixture_xg_2 = (df
                         .groupby(['opponent', 'team'])
                         .agg({'shot_statsbomb_xg':['sum'],
                               'isGoal':['sum'],
                               'minute':['max']
                              }
                             )
                         .reset_index() 
                      )

    ### Rename columns after groupby and aggregation
    df_fixture_xg_2.columns = ['opponent_2', 'team_2', 'opponent_xg', 'opponent_goals', 'minutes_2']

    ### Rearrange columns
    df_fixture_xg_2 = df_fixture_xg_2[['team_2', 'opponent_2', 'opponent_xg', 'opponent_goals', 'minutes_2']].drop_duplicates()

    ### Join the two xG DataFrames
    df_fixture_xg = df_fixture_xg_1.merge(df_fixture_xg_2, left_on=['team', 'opponent'], right_on=['opponent_2', 'team_2'], how='left')

    ### Groupby and aggregate
    df_team_grouped = (df_fixture_xg
                           .groupby(['team'])
                           .agg({'opponent':['count'],
                                 'minutes':['sum'],
                                 'team_xg':['sum'],
                                 'opponent_xg':['sum'],
                                 'team_goals':['sum'],
                                 'opponent_goals':['sum']
                                }
                               )
                           .reset_index() 
                      )

    ### Rename columns after groupby and aggregation
    df_team_grouped.columns = ['team', 'games_played', 'minutes_played', 'xg', 'xga', 'goals_scored', 'goals_conceded']

    ### Determine bespoke metrics
    df_team_grouped['xg_p90'] = df_team_grouped['xg'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['xg_per_game'] = df_team_grouped['xg'] / df_team_grouped['games_played']
    df_team_grouped['xga_p90'] = df_team_grouped['xga'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['xga_per_game'] = df_team_grouped['xga'] / df_team_grouped['games_played']
    df_team_grouped['goals_p90'] = df_team_grouped['goals_scored'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['goals_per_game'] = df_team_grouped['goals_scored'] / df_team_grouped['games_played']
    df_team_grouped['goals_conceded_p90'] = df_team_grouped['goals_conceded'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['goals_conceded_per_game'] = df_team_grouped['goals_conceded'] / df_team_grouped['games_played']
    df_team_grouped['goal_difference'] = df_team_grouped['goals_scored'] - df_team_grouped['goals_conceded']
    df_team_grouped['xg_diff'] = df_team_grouped['xg'] - df_team_grouped['xga']
    df_team_grouped['xg_diff_p90'] = df_team_grouped['xg_diff'] / (df_team_grouped['minutes_played'] / 90)
    df_team_grouped['xg_diff_per_game'] = df_team_grouped['xg_diff'] / df_team_grouped['games_played']

    ### Round the metrics to 2 or 3 decimal places
    df_team_grouped['xg'] = df_team_grouped['xg'].round(2)
    df_team_grouped['xga'] = df_team_grouped['xga'].round(2)
    df_team_grouped['xg_p90'] = df_team_grouped['xg_p90'].round(2)
    df_team_grouped['xg_per_game'] = df_team_grouped['xg_per_game'].round(2)
    df_team_grouped['xga_p90'] = df_team_grouped['xga_p90'].round(2)
    df_team_grouped['xga_per_game'] = df_team_grouped['xga_per_game'].round(2)
    df_team_grouped['goals_p90'] = df_team_grouped['goals_p90'].round(2)
    df_team_grouped['goals_per_game'] = df_team_grouped['goals_per_game'].round(2)
    df_team_grouped['goals_conceded_p90'] = df_team_grouped['goals_conceded_p90'].round(2)
    df_team_grouped['goals_conceded_per_game'] = df_team_grouped['goals_conceded_per_game'].round(2)
    df_team_grouped['xg_diff'] = df_team_grouped['xg_diff'].round(2)
    df_team_grouped['xg_diff_p90'] = df_team_grouped['xg_diff_p90'].round(3)
    df_team_grouped['xg_diff_per_game'] = df_team_grouped['xg_diff_per_game'].round(3)

    ### Sort by 'xg_per_game_diff' decending
    df_team_grouped = df_team_grouped.sort_values(['xg_diff_p90'], ascending=[False])

    ### Reset index
    df_team_grouped = df_team_grouped.reset_index(drop=True)



    ## Data Visualisation

    ### Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#F7F7F7'
    title_colour='black'
    text_colour='black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 15})


    ### Create figure 
    fig, ax = plt.subplots(figsize=(x_dimensions, y_dimensions))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)


    ### Add a grid and set gridlines
    ax.grid(linestyle='dotted',
            linewidth=0.25,
            color='#3B3B3B',
            axis='y',
            zorder=1
           )

    
    ### Remove top and right spines, colour bttom and left
    spines = ['top', 'right', 'bottom', 'left']
    for s in spines:
        if s in ['top', 'right', 'bottom', 'left']:
            ax.spines[s].set_visible(False)
        else:
            ax.spines[s].set_color(text_colour)

            
    ### Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    
    ### Add padding between axes and labels
    ax.xaxis.set_tick_params(pad=2)
    ax.yaxis.set_tick_params(pad=20)

    ### Add X, Y gridlines
    ax.grid(b=True,
            color='grey',
            linestyle='-.',
            linewidth=0.5,
            alpha=0.2
           )


    ### Define X and Y values
    xga_p90 = df_team_grouped['xga_p90'].tolist()
    xg_p90 = df_team_grouped['xg_p90'].tolist() 
    teams = df_team_grouped['team'].tolist()
    xg_diff_p90 = df_team_grouped['xg_diff_p90'].tolist()


    ### Label the nodes
    for i, label in enumerate(teams):
        plt.annotate(label,(xga_p90[i], xg_p90[i]))


    ### Define Z order
    zo = 12


    ### Create scatter plot of shots
    ax.scatter(xga_p90,
               xg_p90,
               marker='o',
              #color=point_colour,
               edgecolors='black',
               c=xg_diff_p90,
               cmap=colour_scale,
              #linewidths=0.5,
               s=200,
               alpha=0.7,
               zorder=zo
              )


    ### Show Legend
    #plt.legend(loc='upper left')     # commented out as not required

    ### Add Plot Title
    plt.figtext(0.045,
                1.04,
                f'Each Country\'s xG vs. xGA',
                fontsize=30,
                fontweight='bold', 
                color=text_colour
               )


    ### Add Plot Subtitle
    fig.text(0.045, 1.00, f'EURO 2020', fontweight='regular', fontsize=20, fontfamily=title_font, color=text_colour)

    
    ### Add X and Y labels
    plt.xlabel('xG Conceded', color=text_colour, fontsize=18)
    plt.ylabel('xG', color=text_colour, fontsize=18)
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2])
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6])
    plt.xlim([0.4, 2.6])
    plt.ylim([0, 2.2])
    
    
    ### Invert x axis - less xGA is better
    ax.invert_xaxis()

    
    ### Remove pips
    ax.tick_params(axis='both', length=0)
    
    
    ### Add UEFA EURO 2020 logo
    ax2 = fig.add_axes([0.90, 0.95, 0.12, 0.12])
    ax2.axis('off')
    img = image.imread('../img/competitions/uefa_euro_2020.png')
    ax2.imshow(img)


    ### Add StatsBomb logo
    ax3 = fig.add_axes([0.755, -0.0965, 0.15, 0.15])
    ax3.axis('off')
    img = image.imread('../img/logos/stats-bomb-logo.png')
    ax3.imshow(img)


    ### Add StatsBomb 360 logo
    ax4 = fig.add_axes([0.9175, -0.0535, 0.07, 0.07])
    ax4.axis('off')
    img = image.imread('../img/logos/stats-bomb-360-logo.png')
    ax4.imshow(img)


    ### Footnote
    plt.figtext(0.045,
                -0.05,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb.\nxG and xGA standardised per 90 minutes. Penalties excluded.\n',
                fontstyle='italic',
                fontsize=15, 
                fontfamily=main_font,
                color=text_colour
               )


    ### Save figure
    if not os.path.exists(fig_dir + f'/xg_diff_scatter_plot_teams.png'):
        plt.savefig(fig_dir + f'/xg_diff_scatter_plot_teams.png', bbox_inches='tight', dpi=300)
    else:
        pass


    ### Show plt
    plt.tight_layout()
    plt.show()    


############################################################################
## 6) Functions to create Passing Networks
############################################################################

## Define function for creating a passing network
def create_passing_network(df,
                           home_team,
                           away_team,
                           passing_network_team,
                           opponent,
                           passing_network_team_colour,
                           opponent_colour,
                           node_colour,
                           arrow_colour,
                           minute_start,
                           minute_end,
                           pitch_length_x,
                           pitch_length_y,
                           pass_threshold,
                           orientation,
                           aspect,
                           title,
                           players_to_exclude,
                           subtitle,
                           x_dimensions,
                           y_dimensions
                          ):
    
    """
    Function to create a passing network, originally made using the 
    'draw_pitch' function, created by Peter McKeever @petermckeever, however,
    due to some temporary technical issues, it's replaced with the pitch from mplsoccer
    """

    ## Data Engineering

    ### Filter DataFrame for a single match and then only select team of interest
    df = df[(df['home_team_name'] == home_team) & (df['away_team_name'] == away_team)].reset_index(drop=True)
    df = df[(df['team_name'] == passing_network_team)].reset_index(drop=True)


    ### Determine passers and recipients by ID and then filter for only passes
    df['passer'] = df['player_id']
    df['recipient'] = df['pass_recipient_id']


    ### Filter DataFrame for only passes and ind passes and then only look for the successful passes
    df_passes = df[df['type_name']=='Pass']
    df_successful = df_passes[df_passes['pass_outcome_name'].isnull()]


    ### Filter time
    #period_mask = (df_successful['period'] >= period_start) & (df_successful['period'] <= period_end)
    minute_mask = (df_successful['minute'] >= minute_start) & (df_successful['minute'] <= minute_end)
    #df_successful = df_successful.loc[(period_mask & minute_mask)]
    df_successful = df_successful.loc[minute_mask]


    ### Determine the first subsititution and filter the successful dataframe to be less than that minute
    #df_subs = df[df['next_event']=='Substitution']
    #df_subs = df_subs['minute']


    #### Determine when the first substitute took place
    #first_sub = df_subs.min()


    #### Filter DataFrame of successful pass for up until the first substitute takes place in the match
    #df_successful = df_successful[df_successful['minute'] < first_sub]


    ### Convert IDs of passer and recipients are floats
    pas = pd.to_numeric(df_successful['passer'], downcast='integer')
    rec = pd.to_numeric(df_successful['recipient'], downcast='integer')
    df_successful['passer'] = pas
    df_successful['recipient'] = rec
    df_successful['passer'] = df_successful['passer'].astype(float)
    df_successful['recipient'] = df_successful['recipient'].astype(float)

    ### Determine the average locations and counts of the passes
    df_average_locations = (df_successful
                                .groupby(['player_name', 'passer'])
                                .agg({'location_x':['mean'],
                                      'location_y':['mean','count']
                                     }
                                    )
                           )


    ### Rename columns after groupby and aggregation
    df_average_locations.columns = ['location_x', 'location_y', 'count']


    #### Reset index
    df_average_locations = df_average_locations.reset_index(drop=False)


    ### Groupby and aggregate the the number of passes between passers and recipients

    #### Now we need to find the number of passes between each player
    df_pass_between = (df_successful
                           .groupby(['player_name', 'passer', 'recipient'])
                           .id.count()
                           .reset_index()
                      )

    #### Rename columns
    df_pass_between = df_pass_between.rename({'player_name':'passer_name',
                                              'id':'pass_count'
                                             }, axis='columns')



    ### Merge the average location dataframe. We need to merge on the passer first then the recipient

    ####
    df_pass_between = df_pass_between.merge(df_average_locations, left_on='passer', right_on='passer')
    df_pass_between = df_pass_between.merge(df_average_locations, left_on='recipient', right_on='passer', suffixes=['', '_end'])

    #### Set minimum threshold of combinations
    df_pass_between = df_pass_between[df_pass_between['pass_count'] >= pass_threshold]

    #### Filter out any players to remove
    df_average_locations = df_average_locations[~df_average_locations['player_name'].isin(players_to_exclude)]
    df_pass_between = df_pass_between[~df_pass_between['player_name'].isin(players_to_exclude)]

    ### Select columns of interest
    df_unique_nodes = df_pass_between[['passer_name', 'passer', 'location_x', 'location_y']].drop_duplicates()
    df_unique_nodes['pass_surname'] = df_unique_nodes['passer_name'].str.split(' ').str[-1]
    
    
    
    ## Visualisation

    ### Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background = '#F7F7F7'
    title_colour = 'black'
    text_colour = 'black'
    filler = 'grey'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 17})


    """
    ### Draw the pitch using the Peter McKeever's 'draw_pitch function'
    pitch = draw_pitch(x_min=0,
                       x_max=pitch_length_x,
                       y_min=0,
                       y_max=pitch_length_y,
                       orientation=orientation,
                       aspect=aspect,
                       pitch_color=background,
                       line_color='#3B3B3B',
                       ax=ax
                      )

    """


    #### Plot the pitch
    pitch = Pitch(pitch_type='statsbomb',
                  orientation='horizontal',
                  pitch_color=background,
                  line_color='#3B3B3B',
                  figsize=(x_dimensions, y_dimensions),
                  constrained_layout=True,
                  tight_layout=False
                 )


    ### Create fixture 
    fig, ax = pitch.draw(figsize=(x_dimensions, y_dimensions))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)


    ### Plot the nodes
    nodes = pitch.scatter(df_average_locations['location_x'],
                          df_average_locations['location_y'],
                          s=1000,
                          color=node_colour,
                          edgecolors='black',
                          linewidth=2.5,
                          alpha=1,
                          zorder=1,
                          ax=ax
                         )    


    ### 
    x = df_unique_nodes['location_x'].tolist()
    y = df_unique_nodes['location_y'].tolist()
    players = df_unique_nodes['pass_surname'].tolist()


    ### Label the nodes
    for i, label in enumerate(players):
        plt.annotate(label,(x[i], y[i]))


    ### Plot the arrows
    arrows = pitch.arrows(df_pass_between['location_x'],
                          df_pass_between['location_y'],
                          df_pass_between['location_x_end'],
                          df_pass_between['location_y_end'],
                          width=7,
                         #width=df_pass_between['pass_count']*1000,
                         #headwidth=df_pass_between['pass_count']*1000,
                          headwidth=3,
                          color=arrow_colour,
                          zorder=1,
                          alpha=0.4,
                          ax=ax
                         )


    ### Add Plot Title
    s = '<{}>\'s Passing Network {} vs. <{}> at EURO 2020\n'
    htext.fig_htext(s.format(passing_network_team, title, opponent), 0.09, 0.915, highlight_colors=[passing_network_team_colour, opponent_colour], highlight_weights=['bold'], string_weight='bold', fontsize=22, fontfamily=title_font, color=text_colour)


    ### Add Plot Subtitle
    #fig.text(0.04, 1.029, f'EURO 2020 {subtitle}', fontweight='regular', fontsize=20, fontfamily=title_font, color=text_colour)


    ### Add UEFA EURO 2020 logo
    ax2 = fig.add_axes([0.81, 0.80, 0.12, 0.12])
    ax2.axis('off')
    img = image.imread('../img/competitions/uefa_euro_2020.png')
    ax2.imshow(img)


    ### Add StatsBomb logo
    ax3 = fig.add_axes([0.67, 0.02, 0.15, 0.15])
    ax3.axis('off')
    img = image.imread('../img/logos/stats-bomb-logo.png')
    ax3.imshow(img)


    ### Add StatsBomb 360 logo
    ax4 = fig.add_axes([0.83, 0.060, 0.075, 0.075])
    ax4.axis('off')
    img = image.imread('../img/logos/stats-bomb-360-logo.png')
    ax4.imshow(img)


    ### Footnote
    plt.figtext(0.09,
                0.010,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb.\n',
                fontstyle='italic',
                fontsize=15, 
                fontfamily=main_font,
                color=text_colour
               )

    """
    ### Save figure
    if not os.path.exists(fig_dir + f'/passing_network_{home_team}_{away_team}_{orientation}_{aspect}.png'):
        plt.savefig(fig_dir + f'/passing_network_{home_team}_{away_team}_{orientation}_{aspect}.png', bbox_inches='tight', dpi=300)
    else:
        pass
    """

    ### Show plt
    plt.tight_layout()
    plt.show()



############################################################################
## 7) Functions to create Passing Maps
#############################################################################

## Define function for creating a pass map for a team
def create_pass_map_team(df,
                         home_team,
                         away_team,
                         pass_map_team,
                         opponent,
                         pass_map_team_colour,
                         opponent_colour,
                         successful_pass_colour,
                         unsuccessful_pass_colour,
                         pitch_length_x,
                         pitch_length_y,
                         orientation,
                         aspect,
                         x_dimensions,
                         y_dimensions
                        ):
    
    """
    Function for creating a pass map for a team, utilising the 'create_passing_network' function, created by Peter McKeever @petermckeever.
    """
    
    ## Data Engineering
    
    ### Filter DataFrame for a single match and then only select team of interest
    df = df[(df['home_team_name'] == home_team) & (df['away_team_name'] == away_team)].reset_index(drop=True)
    df = df[(df['team_name'] == pass_map_team)].reset_index(drop=True)
    df_passes = df[df['type_name']=='Pass']
 
    
    
    ## Visualisation
    
    ### Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#F7F7F7'
    title_colour='black'
    text_colour='black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    
    ### Create figure 
    fig, ax = plt.subplots(figsize=(x_dimensions, y_dimensions))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)
    #ax.patch.set_facecolor('w')

    
    ### Set Gridlines 
    #ax.grid(lw=0.25, color='k', zorder=1)

    
    ### Draw the pitch using the 
    pitch = draw_pitch(x_min=0,
                       x_max=pitch_length_x,
                       y_min=0,
                       y_max=pitch_length_y,
                       orientation=orientation,
                       aspect=aspect,
                       pitch_color=background,
                       line_color='#3B3B3B',
                       ax=ax
                      )
    
    
    ### Define Z order
    zo = 12

    
    ### use a for loop to plot each pass
    for i in range(len(df_passes['location_x'])):
        try:
            if pd.isnull(df_passes['pass_outcome_name'][i]):
                plt.plot((df_passes['location_x'][i], df_passes['pass_end_location_x'][i]), (df_passes['location_y'][i], df_passes['pass_end_location_y'][i]), color='green')
                plt.scatter(df_passes['location_x'][i], df_passes['location_y'][i], color=successful_pass_colour)
            if pd.notnull(df_passes['pass_outcome_name'][i]):
                plt.plot((df_passes['location_x'][i], df_passes['pass_end_location_x'][i]), (df_passes['location_y'][i], df_passes['pass_end_location_y'][i]), color='red')
                plt.scatter(df_passes['location_x'][i], df_passes['location_y'][i], color=unsuccessful_pass_colour)
        except:
            pass
   
    
    ### Add Plot Title
    s = '<{}>\'s Pass Map vs. <{}> at EURO 2020\n'
    htext.fig_htext(s.format(pass_map_team, opponent), 0.09, 0.915, highlight_colors=[pass_map_team_colour, opponent_colour], highlight_weights=['bold'], string_weight='bold', fontsize=22, fontfamily=title_font, color=text_colour)


    ### Add Plot Subtitle
    #fig.text(0.04, 1.029, f'EURO 2020 {subtitle}', fontweight='regular', fontsize=20, fontfamily=title_font, color=text_colour)


    ### Add UEFA EURO 2020 logo
    ax2 = fig.add_axes([0.81, 0.80, 0.12, 0.12])
    ax2.axis('off')
    img = image.imread('../img/competitions/uefa_euro_2020.png')
    ax2.imshow(img)


    ### Add StatsBomb logo
    ax3 = fig.add_axes([0.67, 0.02, 0.15, 0.15])
    ax3.axis('off')
    img = image.imread('../img/logos/stats-bomb-logo.png')
    ax3.imshow(img)


    ### Add StatsBomb 360 logo
    ax4 = fig.add_axes([0.83, 0.060, 0.075, 0.075])
    ax4.axis('off')
    img = image.imread('../img/logos/stats-bomb-360-logo.png')
    ax4.imshow(img)


    ### Footnote
    plt.figtext(0.09,
                0.010,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb.\n',
                fontstyle='italic',
                fontsize=15, 
                fontfamily=main_font,
                color=text_colour
               )

    
    ### Save figure
    if not os.path.exists(fig_dir + f'/pass_map_{player_name}_{home_team}_{away_team}_{orientation}_{aspect}.png'):
        plt.savefig(fig_dir + f'/pass_map_{player_name}_{home_team}_{away_team}_{orientation}_{aspect}.png', bbox_inches='tight', dpi=300)
    else:
        pass


    ### Show plt
    plt.tight_layout()
    plt.show()



### Define function for creating a pass map for a single player
def create_pass_map_single_player(df,
                                  home_team,
                                  away_team,
                                  pass_map_team,
                                  opponent,
                                  player_name,
                                  pass_map_team_colour,
                                  opponent_colour,
                                  successful_pass_colour,
                                  unsuccessful_pass_colour,
                                  pitch_length_x,
                                  pitch_length_y,
                                  orientation,
                                  aspect,
                                  x_dimensions,
                                  y_dimensions
                                 ):

    """
    Function for creating a pass map for a single player, utilising the 'create_passing_network' function, created by Peter McKeever @petermckeever.
    """
    
    ## Data Engineering
    
    ### Filter DataFrame for a single match and then only select team of interest
    df = df[(df['home_team_name'] == home_team) & (df['away_team_name'] == away_team)].reset_index(drop=True)
    df = df[(df['player_name'] == player_name)].reset_index(drop=True)
    df_passes = df[df['type_name']=='Pass']
 
    
    
    ## Visualisation
    
    ### Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#F7F7F7'
    title_colour='black'
    text_colour='black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    
    ### Create figure 
    fig, ax = plt.subplots(figsize=(x_dimensions, y_dimensions))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)
    #ax.patch.set_facecolor('w')

    
    ### Set Gridlines 
    #ax.grid(lw=0.25, color='k', zorder=1)

    
    ### Draw the pitch using the 
    pitch = draw_pitch(x_min=0,
                       x_max=pitch_length_x,
                       y_min=0,
                       y_max=pitch_length_y,
                       orientation=orientation,
                       aspect=aspect,
                       pitch_color=background,
                       line_color='#3B3B3B',
                       ax=ax
                      )
    
    
    ### Define Z order
    zo = 12

    
    ### use a for loop to plot each pass
    for i in range(len(df_passes['location_x'])):
        try:
            if pd.isnull(df_passes['pass_outcome_name'][i]):
                plt.plot((df_passes['location_x'][i], df_passes['pass_end_location_x'][i]), (df_passes['location_y'][i], df_passes['pass_end_location_y'][i]), color='green')
                plt.scatter(df_passes['location_x'][i], df_passes['location_y'][i], color=successful_pass_colour)
            if pd.notnull(df_passes['pass_outcome_name'][i]):
                plt.plot((df_passes['location_x'][i], df_passes['pass_end_location_x'][i]), (df_passes['location_y'][i], df_passes['pass_end_location_y'][i]), color='red')
                plt.scatter(df_passes['location_x'][i], df_passes['location_y'][i], color=unsuccessful_pass_colour)
        except:
            pass
   
    
    ### Add Plot Title
    s = '{}\'s Pass Map for <{}> vs. <{}> at EURO 2020\n'
    htext.fig_htext(s.format(player_name, pass_map_team, opponent), 0.09, 0.915, highlight_colors=[pass_map_team_colour, opponent_colour], highlight_weights=['bold'], string_weight='bold', fontsize=22, fontfamily=title_font, color=text_colour)


    ### Add Plot Subtitle
    #fig.text(0.04, 1.029, f'EURO 2020 {subtitle}', fontweight='regular', fontsize=20, fontfamily=title_font, color=text_colour)


    ### Add UEFA EURO 2020 logo
    ax2 = fig.add_axes([0.81, 0.80, 0.12, 0.12])
    ax2.axis('off')
    img = image.imread('../img/competitions/uefa_euro_2020.png')
    ax2.imshow(img)


    ### Add StatsBomb logo
    ax3 = fig.add_axes([0.67, 0.02, 0.15, 0.15])
    ax3.axis('off')
    img = image.imread('../img/logos/stats-bomb-logo.png')
    ax3.imshow(img)


    ### Add StatsBomb 360 logo
    ax4 = fig.add_axes([0.83, 0.060, 0.075, 0.075])
    ax4.axis('off')
    img = image.imread('../img/logos/stats-bomb-360-logo.png')
    ax4.imshow(img)


    ### Footnote
    plt.figtext(0.09,
                0.010,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb.\n',
                fontstyle='italic',
                fontsize=15, 
                fontfamily=main_font,
                color=text_colour
               )

    
    ### Save figure
    if not os.path.exists(fig_dir + f'/pass_map_{player_name}_{home_team}_{away_team}_{orientation}_{aspect}.png'):
        plt.savefig(fig_dir + f'/pass_map_{player_name}_{home_team}_{away_team}_{orientation}_{aspect}.png', bbox_inches='tight', dpi=300)
    else:
        pass


    ### Show plt
    plt.tight_layout()
    plt.show()


## Define function for creating a pass map for multiple players
def create_pass_map_multiple_players(df,
                                     home_team,
                                     away_team,
                                     pass_map_team,
                                     opponent,
                                     player_names,
                                     pass_map_team_colour,
                                     opponent_colour,
                                     successful_pass_colour,
                                     unsuccessful_pass_colour,
                                     pitch_length_x,
                                     pitch_length_y,
                                     orientation,
                                     aspect,
                                     title,
                                     x_dimensions,
                                     y_dimensions
                                    ):
    
    """
    Function for creating a pass map for multiple players, utilising the 'create_passing_network' function, created by Peter McKeever @petermckeever.
    """
    
    ## Data Engineering
    
    ### Filter DataFrame for a single match and then only select team of interest
    df = df[(df['home_team_name'] == home_team) & (df['away_team_name'] == away_team)].reset_index(drop=True)
    df = df[df['player_name'].isin(player_names)].reset_index(drop=True)
    df_passes = df[df['type_name']=='Pass']
 
    
    
    ## Visualisation
    
    ### Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#F7F7F7'
    title_colour='black'
    text_colour='black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    
    ### Create figure 
    fig, ax = plt.subplots(figsize=(x_dimensions, y_dimensions))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)
    #ax.patch.set_facecolor('w')

    
    ### Set Gridlines 
    #ax.grid(lw=0.25, color='k', zorder=1)

    
    ### Draw the pitch using the 
    pitch = draw_pitch(x_min=0,
                       x_max=pitch_length_x,
                       y_min=0,
                       y_max=pitch_length_y,
                       orientation=orientation,
                       aspect=aspect,
                       pitch_color=background,
                       line_color='#3B3B3B',
                       ax=ax
                      )
    
    
    ### Define Z order
    zo = 12

    
    ### use a for loop to plot each pass
    for i in range(len(df_passes['location_x'])):
        try:
            if pd.isnull(df_passes['pass_outcome_name'][i]):
                plt.plot((df_passes['location_x'][i], df_passes['pass_end_location_x'][i]), (df_passes['location_y'][i], df_passes['pass_end_location_y'][i]), color='green')
                plt.scatter(df_passes['location_x'][i], df_passes['location_y'][i], color=successful_pass_colour)
            if pd.notnull(df_passes['pass_outcome_name'][i]):
                plt.plot((df_passes['location_x'][i], df_passes['pass_end_location_x'][i]), (df_passes['location_y'][i], df_passes['pass_end_location_y'][i]), color='red')
                plt.scatter(df_passes['location_x'][i], df_passes['location_y'][i], color=unsuccessful_pass_colour)
        except:
            pass
   
    
    ### Add Plot Title
    s = '{} Pass Map for <{}> vs. <{}> at EURO 2020\n'
    htext.fig_htext(s.format(title, pass_map_team, opponent), 0.09, 0.915, highlight_colors=[pass_map_team_colour, opponent_colour], highlight_weights=['bold'], string_weight='bold', fontsize=22, fontfamily=title_font, color=text_colour)


    ### Add Plot Subtitle
    #fig.text(0.04, 1.029, f'EURO 2020 {subtitle}', fontweight='regular', fontsize=20, fontfamily=title_font, color=text_colour)


    ### Add UEFA EURO 2020 logo
    ax2 = fig.add_axes([0.81, 0.80, 0.12, 0.12])
    ax2.axis('off')
    img = image.imread('../img/competitions/uefa_euro_2020.png')
    ax2.imshow(img)


    ### Add StatsBomb logo
    ax3 = fig.add_axes([0.67, 0.02, 0.15, 0.15])
    ax3.axis('off')
    img = image.imread('../img/logos/stats-bomb-logo.png')
    ax3.imshow(img)


    ### Add StatsBomb 360 logo
    ax4 = fig.add_axes([0.83, 0.060, 0.075, 0.075])
    ax4.axis('off')
    img = image.imread('../img/logos/stats-bomb-360-logo.png')
    ax4.imshow(img)


    ### Footnote
    plt.figtext(0.09,
                0.010,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb.\n',
                fontstyle='italic',
                fontsize=15, 
                fontfamily=main_font,
                color=text_colour
               )

    
    ### Save figure
    if not os.path.exists(fig_dir + f'/pass_map_{title}_{home_team}_{away_team}_{orientation}_{aspect}.png'):
        plt.savefig(fig_dir + f'/pass_map_{title}_{home_team}_{away_team}_{orientation}_{aspect}.png', bbox_inches='tight', dpi=300)
    else:
        pass


    ### Show plt
    plt.tight_layout()
    plt.show()





############################################################################
## 8) Functions to create Heat Maps
############################################################################

## Define function for creating a heat map of touches by a team
def create_heat_map_team(df,
                         home_team,
                         away_team,
                         heat_map_team,
                         pitch_length_x,
                         pitch_length_y,
                         orientation,
                         aspect,
                         gradient,
                         n_levels,
                         x_dimensions,
                         y_dimensions
                        ):
    
    """
    Function to create a heat map of touches by a team, utilising the 'create_passing_network' function, created by Peter McKeever @petermckeever.
    """
    
    ## Data Engineering
    
    ### Filter DataFrame for a single match and then only select team of interest
    df = df[(df['home_team_name'] == home_team) & (df['away_team_name'] == away_team)].reset_index(drop=True)
    df = df[(df['team_name'] == heat_map_team)].reset_index(drop=True)

    
    
    ## Visualisation
    
    ### Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#F7F7F7'
    title_colour='black'
    text_colour='black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    
    ### Create figure 
    fig, ax = plt.subplots(figsize=(x_dimensions, y_dimensions))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)
    #ax.patch.set_facecolor('w')

    
    ### Set Gridlines 
    #ax.grid(lw=0.25, color='k', zorder=1)

    
    ### Draw the pitch using the 
    pitch = draw_pitch(x_min=0,
                       x_max=pitch_length_x,
                       y_min=0,
                       y_max=pitch_length_y,
                       orientation=orientation,
                       aspect=aspect,
                       pitch_color=background,
                       line_color='#3B3B3B',
                       ax=ax
                      )
    
    
    ### Create the heatmap
    kde = sns.kdeplot(df['location_x'],
                      df['location_y'],
                      shade = True,
                      shade_lowest=False,
                      alpha=.5,
                      n_levels=n_levels,
                      cmap=gradient
                     )

    ### Define Z order
    zo = 12
  
    
    ### X and Y limits
    plt.xlim(0-5, pitch_length_x+5)
    plt.ylim(0-5, pitch_length_y+5)
    
    
    """
    ### Add Plot Title
    ax.set_title(f'Pass Map for {home_team} vs. {away_team} at EURO 2020',
                 loc='left',
                 fontsize=20,
                 fontweight='bold', 
                 color=text_colour
                )
    """
    
    
    ### Title v2
    plt.figtext(0.055,
                0.96,
                f'Heat Map for {home_team} vs. {away_team} at EURO 2020',
                fontsize=25,
                fontweight='bold', 
                color=text_colour
               )
    
    
    ### Footnote
    plt.figtext(0.055,
                -0.001,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb.\n',
                ha="left",
                fontsize=15
               )

    
    ### Save figure
    if not os.path.exists(fig_dir + f'/heat_map_{home_team}_{away_team}_{orientation}_{aspect}.png'):
        plt.savefig(fig_dir + f'/heat_map_{home_team}_{away_team}_{orientation}_{aspect}.png', bbox_inches='tight', dpi=300)
    else:
        pass


    ### Show plt
    plt.tight_layout()
    plt.show()



## Define function for creating a heat map of touches by a player
def create_heat_map_player(df,
                           home_team,
                           away_team,
                           player_name,
                           successful_pass_colour,
                           unsuccessful_pass_colour,
                           pitch_length_x,
                           pitch_length_y,
                           orientation,
                           aspect,
                           gradient,
                           n_levels,
                           x_dimensions,
                           y_dimensions
                          ):
    
    """
    Function to create a heat map of touches by a player, utilising the 'create_passing_network' function, created by Peter McKeever @petermckeever.
    """
    
    ## Data Engineering
    
    ### Filter DataFrame for a single match and then only select team of interest
    df = df[(df['home_team_name'] == home_team) & (df['away_team_name'] == away_team)].reset_index(drop=True)
    df = df[(df['player_name'] == player_name)].reset_index(drop=True)
    df_passes = df[df['type_name']=='Pass']
 
    
    
    ## Visualisation
    
    ### Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#F7F7F7'
    title_colour='black'
    text_colour='black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    
    ### Create figure 
    fig, ax = plt.subplots(figsize=(x_dimensions, y_dimensions))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)
    #ax.patch.set_facecolor('w')

    
    ### Set Gridlines 
    #ax.grid(lw=0.25, color='k', zorder=1)

    
    ### Draw the pitch using the 
    pitch = draw_pitch(x_min=0,
                       x_max=pitch_length_x,
                       y_min=0,
                       y_max=pitch_length_y,
                       orientation=orientation,
                       aspect=aspect,
                       pitch_color=background,
                       line_color='#3B3B3B',
                       ax=ax
                      )
    
    
    ### Create the heatmap
    kde = sns.kdeplot(
            df_passes['location_x'],
            df_passes['location_y'],
            shade = True,
            shade_lowest=False,
            alpha=.5,
            n_levels=n_levels,
            cmap=gradient
    )
    
    
    ### Define Z order
    zo = 12

    
    ### use a for loop to plot each pass
    for i in range(len(df_passes['location_x'])):
        try:
            if pd.isnull(df_passes['pass_outcome_name'][i]):
                plt.plot((df_passes['location_x'][i], df_passes['pass_end_location_x'][i]), (df_passes['location_y'][i], df_passes['pass_end_location_y'][i]), color='green')
                plt.scatter(df_passes['location_x'][i], df_passes['location_y'][i], color=successful_pass_colour)
            if pd.notnull(df_passes['pass_outcome_name'][i]):
                plt.plot((df_passes['location_x'][i], df_passes['pass_end_location_x'][i]), (df_passes['location_y'][i], df_passes['pass_end_location_y'][i]), color='red')
                plt.scatter(df_passes['location_x'][i], df_passes['location_y'][i], color=unsuccessful_pass_colour)
        except:
            pass
   

    ### X and Y limits
    plt.xlim(0-5, pitch_length_x+5)
    plt.ylim(0-5, pitch_length_y+5)

    """
    ### Add Plot Title
    ax.set_title(f'{player_name} Heat Map for {home_team} vs. {away_team} at EURO 2020',
                 loc='left',
                 fontsize=20,
                 fontweight='bold', 
                 color=text_colour
                )
    """
    
    
    ### Title v2
    plt.figtext(0.055,
                0.96,
                f'{player_name} Heat Map for {home_team} vs. {away_team} at EURO 2020',
                fontsize=25,
                fontweight='bold', 
                color=text_colour
               )
    
    
    ### Footnote
    plt.figtext(0.055,
                -0.001,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb.\n',
                ha="left",
                fontsize=15
               )

    
    ### Save figure
    if not os.path.exists(fig_dir + f'/heat_map_{player_name}_{home_team}_{away_team}_{orientation}_{aspect}.png'):
        plt.savefig(fig_dir + f'/heat_map_{player_name}_{home_team}_{away_team}_{orientation}_{aspect}.png', bbox_inches='tight', dpi=300)
    else:
        pass


    ### Show plt
    plt.tight_layout()
    plt.show()



############################################################################
## 9) Functions to create combined Heat and Pass Maps
############################################################################

## Define function for creating a heat map of touches by a team
def create_heat_and_pass_map_team(df,
                                  home_team,
                                  away_team,
                                  heat_map_team,
                                  successful_pass_colour,
                                  unsuccessful_pass_colour,
                                  pitch_length_x,
                                  pitch_length_y,
                                  orientation,
                                  aspect,
                                  gradient,
                                  n_levels,
                                  x_dimensions,
                                  y_dimensions
                                 ):
    
    """
    Function to create a combined heat and pass map of touches by a team, utilising the 'create_passing_network' function, created by Peter McKeever @petermckeever.
    """
    
    ## Data Engineering
    
    ### Filter DataFrame for a single match and then only select team of interest
    df = df[(df['home_team_name'] == home_team) & (df['away_team_name'] == away_team)].reset_index(drop=True)
    df = df[(df['team_name'] == heat_map_team)].reset_index(drop=True)
    df_passes = df[df['type_name']=='Pass']
 
    
    
    ## Visualisation
    
    ### Define fonts and colours
    #title_font = 'Alegreya Sans'
    #main_font = 'Open Sans'
    background='#F7F7F7'
    title_colour='black'
    text_colour='black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    
    ### Create figure 
    fig, ax = plt.subplots(figsize=(x_dimensions, y_dimensions))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)
    #ax.patch.set_facecolor('w')

    
    ### Set Gridlines 
    #ax.grid(lw=0.25, color='k', zorder=1)

    
    ### Draw the pitch using the 
    pitch = draw_pitch(x_min=0,
                       x_max=pitch_length_x,
                       y_min=0,
                       y_max=pitch_length_y,
                       orientation=orientation,
                       aspect=aspect,
                       pitch_color=background,
                       line_color='#3B3B3B',
                       ax=ax
                      )
    
    
    ### Create the heatmap
    kde = sns.kdeplot(df_passes['location_x'],
                      df_passes['location_y'],
                      shade = True,
                      shade_lowest=False,
                      alpha=.5,
                      n_levels=n_levels,
                      cmap=gradient
                     )

    ### Define Z order
    zo = 12

    
    ### use a for loop to plot each pass
    for i in range(len(df_passes['location_x'])):
        try:
            if pd.isnull(df_passes['pass_outcome_name'][i]):
                plt.plot((df_passes['location_x'][i], df_passes['pass_end_location_x'][i]), (df_passes['location_y'][i], df_passes['pass_end_location_y'][i]), color='green')
                plt.scatter(df_passes['location_x'][i], df_passes['location_y'][i], color=successful_pass_colour)
            if pd.notnull(df_passes['pass_outcome_name'][i]):
                plt.plot((df_passes['location_x'][i], df_passes['pass_end_location_x'][i]), (df_passes['location_y'][i], df_passes['pass_end_location_y'][i]), color='red')
                plt.scatter(df_passes['location_x'][i], df_passes['location_y'][i], color=unsuccessful_pass_colour)
        except:
            pass
   
    
    ### X and Y limits
    plt.xlim(0-5, pitch_length_x+5)
    plt.ylim(0-5, pitch_length_y+5)
    
    
    """
    ### Add Plot Title
    ax.set_title(f'Pass Map for {home_team} vs. {away_team} at EURO 2020',
                 loc='left',
                 fontsize=20,
                 fontweight='bold', 
                 color=text_colour
                )
    """
    
    
    ### Title v2
    plt.figtext(0.055,
                0.96,
                f'Combined Pass and Heat Map for {home_team} vs. {away_team} at EURO 2020',
                fontsize=25,
                fontweight='bold', 
                color=text_colour
               )
    
    
    ### Footnote
    plt.figtext(0.055,
                -0.001,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb.\n',
                ha="left",
                fontsize=15
               )

    
    ### Save figure
    if not os.path.exists(fig_dir + f'/heat_map_{home_team}_{away_team}_{orientation}_{aspect}.png'):
        plt.savefig(fig_dir + f'/heat_map_{home_team}_{away_team}_{orientation}_{aspect}.png', bbox_inches='tight', dpi=300)
    else:
        pass


    ### Show plt
    plt.tight_layout()
    plt.show()


## Define function for creating a heat map of touches by a player
def create_heat_and_pass_map_player(df,
                                    home_team,
                                    away_team,
                                    player_name,
                                    successful_pass_colour,
                                    unsuccessful_pass_colour,
                                    pitch_length_x,
                                    pitch_length_y,
                                    orientation,
                                    aspect,
                                    gradient,
                                    n_levels,
                                    x_dimensions,
                                    y_dimensions
                                   ):
    
    """
    Function to create a combined heat and pass map of touches by a player, utilising the 'create_passing_network' function, created by Peter McKeever @petermckeever.
    """
    
    ## Data Engineering
    
    ### Filter DataFrame for a single match and then only select team of interest
    df = df[(df['home_team_name'] == home_team) & (df['away_team_name'] == away_team)].reset_index(drop=True)
    df = df[(df['player_name'] == player_name)].reset_index(drop=True)
    df_passes = df[df['type_name']=='Pass']
 
    
    
    ## Visualisation
    
    ### Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#F7F7F7'
    title_colour='black'
    text_colour='black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    
    ### Create figure 
    fig, ax = plt.subplots(figsize=(x_dimensions, y_dimensions))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)
    #ax.patch.set_facecolor('w')

    
    ### Set Gridlines 
    #ax.grid(lw=0.25, color='k', zorder=1)

    
    ### Draw the pitch using the 
    pitch = draw_pitch(x_min=0,
                       x_max=pitch_length_x,
                       y_min=0,
                       y_max=pitch_length_y,
                       orientation=orientation,
                       aspect=aspect,
                       pitch_color=background,
                       line_color='#3B3B3B',
                       ax=ax
                      )
    
    
    ### Create the heatmap
    kde = sns.kdeplot(
            df_passes['location_x'],
            df_passes['location_y'],
            shade = True,
            shade_lowest=False,
            alpha=.5,
            n_levels=n_levels,
            cmap=gradient
    )
    
    
    ### Define Z order
    zo = 12

    
    ### use a for loop to plot each pass
    for i in range(len(df_passes['location_x'])):
        try:
            if pd.isnull(df_passes['pass_outcome_name'][i]):
                plt.plot((df_passes['location_x'][i], df_passes['pass_end_location_x'][i]), (df_passes['location_y'][i], df_passes['pass_end_location_y'][i]), color='green')
                plt.scatter(df_passes['location_x'][i], df_passes['location_y'][i], color=successful_pass_colour)
            if pd.notnull(df_passes['pass_outcome_name'][i]):
                plt.plot((df_passes['location_x'][i], df_passes['pass_end_location_x'][i]), (df_passes['location_y'][i], df_passes['pass_end_location_y'][i]), color='red')
                plt.scatter(df_passes['location_x'][i], df_passes['location_y'][i], color=unsuccessful_pass_colour)
        except:
            pass
   

    ### X and Y limits
    plt.xlim(0-5, pitch_length_x+5)
    plt.ylim(0-5, pitch_length_y+5)

    """
    ### Add Plot Title
    ax.set_title(f'{player_name} Heat Map for {home_team} vs. {away_team} at EURO 2020',
                 loc='left',
                 fontsize=20,
                 fontweight='bold', 
                 color=text_colour
                )
    """
    
    
    ### Title v2
    plt.figtext(0.055,
                0.96,
                f'{player_name} Combined Pass and Heat Map for {home_team} vs. {away_team} at EURO 2020',
                fontsize=25,
                fontweight='bold', 
                color=text_colour
               )
    
    
    ### Footnote
    plt.figtext(0.055,
                -0.001,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb.\n',
                ha="left",
                fontsize=15
               )

    
    ### Save figure
    if not os.path.exists(fig_dir + f'/heat_map_{player_name}_{home_team}_{away_team}_{orientation}_{aspect}.png'):
        plt.savefig(fig_dir + f'/heat_map_{player_name}_{home_team}_{away_team}_{orientation}_{aspect}.png', bbox_inches='tight', dpi=300)
    else:
        pass


    ### Show plt
    plt.tight_layout()
    plt.show()



############################################################################
## 10) OBV Maps
############################################################################

# Define function for creating map of highest OBV value carries for a single player
def create_obv_carries_player(df,
                              player_name,
                              team_colour,
                              successful_carry_colour,
                              unsuccessful_carry_colour,
                              pitch_length_x,
                              pitch_length_y,
                              orientation,
                              aspect,
                              n_carries,
                              x_dimensions,
                              y_dimensions
                             ):
    
    """
    Function to create a carry map of highest OBV value, utilising the 'create_passing_network' function, created by Peter McKeever @petermckeever.
    """
    
    ## Data Engineering
    
    ### Filter DataFrame for a single match and then only select team of interest
    df = df[(df['player_name'] == player_name)].reset_index(drop=True)
    df_carries = df[df['type_name']=='Carry']

    ### Sort DataFrame 
    df_carries = df_carries.sort_values(['obv_total_net'], ascending=[False])

    ### Filter for the top N carries
    df_carries = df_carries.nlargest(20, 'obv_total_net')

    ### Reset Index
    df_carries = df_carries.reset_index(drop=True)
 
    
    
    ## Visualisation
    
    ### Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#F7F7F7'
    title_colour='black'
    text_colour='black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    
    ### Create figure 
    fig, ax = plt.subplots(figsize=(8.5, 10.5))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)
    #ax.patch.set_facecolor('w')

    
    ### Set Gridlines 
    #ax.grid(lw=0.25, color='k', zorder=1)

    
    ### Draw the pitch using the 
    pitch = draw_pitch(x_min=0,
                       x_max=pitch_length_x,
                       y_min=0,
                       y_max=pitch_length_y,
                       orientation=orientation,
                       aspect=aspect,
                       pitch_color=background,
                       line_color='#3B3B3B',
                       ax=ax
                      )
    
    
    ### Define Z order
    zo = 12


    ### use a for loop to plot each pass
    for i in range(len(df_carries['location_x'])):
        try:
            if pd.isnull(df_carries['dribble_outcome_name'][i]):
                plt.plot((df_carries['location_y'][i], df_carries['endloc_y'][i]), (df_carries['location_x'][i], df_carries['endloc_x'][i]), color='green')
                plt.scatter(df_carries['location_y'][i], df_carries['location_x'][i], color=successful_carry_colour)
            if pd.notnull(df_carries['dribble_outcome_name'][i]):
                plt.plot((df_carries['location_y'][i], df_carries['endloc_y'][i]), (df_carries['location_x'][i], df_carries['endloc_x'][i]), color='red')
                plt.scatter(df_carries['location_y'][i], df_carries['location_x'][i], color=unsuccessful_carry_colour)
        except:
            pass
   
    
    ### Invert the Y axis - attacking from bottom to top
    ax.invert_yaxis()
    
    ### Add Plot Title
    s = '<{}>\'s Most Valuable Dribbles By OBV at EURO 2020\n'
    htext.fig_htext(s.format(player_name), 0.09, 0.915, highlight_colors=[team_colour], highlight_weights=['bold'], string_weight='bold', fontsize=15, fontfamily=title_font, color=text_colour)


    ### Add Plot Subtitle
    #fig.text(0.04, 1.029, f'EURO 2020 {subtitle}', fontweight='regular', fontsize=20, fontfamily=title_font, color=text_colour)


    ### Add UEFA EURO 2020 logo
    #ax2 = fig.add_axes([0.81, 0.80, 0.12, 0.12])
    #ax2.axis('off')
    #img = image.imread('../img/competitions/uefa_euro_2020.png')
    #ax2.imshow(img)


    ### Add StatsBomb logo
    #ax3 = fig.add_axes([0.67, 0.02, 0.15, 0.15])
    #ax3.axis('off')
    #img = image.imread('../img/logos/stats-bomb-logo.png')
    #ax3.imshow(img)


    ### Add StatsBomb 360 logo
    #ax4 = fig.add_axes([0.83, 0.060, 0.075, 0.075])
    #ax4.axis('off')
    #img = image.imread('../img/logos/stats-bomb-360-logo.png')
    #ax4.imshow(img)


    ### Footnote
    plt.figtext(0.09,
                0.010,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb.\n',
                fontstyle='italic',
                fontsize=11, 
                fontfamily=main_font,
                color=text_colour
               )

    
    ### Save figure
    if not os.path.exists(fig_dir + f'/{n_carries}_valuable_carries_{player_name}_{orientation}_{aspect}.png'):
        plt.savefig(fig_dir + f'/{n_carries}_valuable_carries_{player_name}_{orientation}_{aspect}.png', bbox_inches='tight', dpi=300)
    else:
        pass


    ### Show plt
    plt.tight_layout()
    plt.show()


# Define function for creating map of highest OBV value carries for a single player
def create_obv_passes_player(df,
                             player_name,
                             team_colour,
                             successful_pass_colour,
                             unsuccessful_pass_colour,
                             pitch_length_x,
                             pitch_length_y,
                             orientation,
                             aspect,
                             n_passes,
                             x_dimensions,
                             y_dimensions
                            ):
    
    """
    Function to create a pass map of highest OBV value, utilising the 'create_passing_network' function, created by Peter McKeever @petermckeever.
    """
    
    ## Data Engineering
    
    ### Filter DataFrame for a single match and then only select team of interest
    df = df[(df['player_name'] == player_name)].reset_index(drop=True)
    df_passes = df[df['type_name']=='Pass']

    ### Sort DataFrame 
    df_passes = df_passes.sort_values(['obv_total_net'], ascending=[False])

    ### Filter for the top N passes
    df_passes = df_passes.nlargest(20, 'obv_total_net')

    ### Reset Index
    df_passes = df_passes.reset_index(drop=True)
 
    
    
    ## Visualisation
    
    ### Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#F7F7F7'
    title_colour='black'
    text_colour='black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    
    ### Create figure 
    fig, ax = plt.subplots(figsize=(8.5, 10.5))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)
    #ax.patch.set_facecolor('w')

    
    ### Set Gridlines 
    #ax.grid(lw=0.25, color='k', zorder=1)

    
    ### Draw the pitch using the 
    pitch = draw_pitch(x_min=0,
                       x_max=pitch_length_x,
                       y_min=0,
                       y_max=pitch_length_y,
                       orientation=orientation,
                       aspect=aspect,
                       pitch_color=background,
                       line_color='#3B3B3B',
                       ax=ax
                      )
    
    
    ### Define Z order
    zo = 12


    ### use a for loop to plot each pass
    for i in range(len(df_passes['location_x'])):
        try:
            if pd.isnull(df_passes['pass_outcome_name'][i]):
                plt.plot((df_passes['location_y'][i], df_passes['endloc_y'][i]), (df_passes['location_x'][i], df_passes['endloc_x'][i]), color='green')
                plt.scatter(df_passes['location_y'][i], df_passes['location_x'][i], color=successful_pass_colour)
            if pd.notnull(df_passes['pass_outcome_name'][i]):
                plt.plot((df_passes['location_y'][i], df_passes['endloc_y'][i]), (df_passes['location_x'][i], df_passes['endloc_x'][i]), color='red')
                plt.scatter(df_passes['location_y'][i], df_passes['location_x'][i], color=unsuccessful_pass_colour)
        except:
            pass
   
    
    ### Invert the Y axis - attacking from bottom to top
    ax.invert_yaxis()
    
    ### Add Plot Title
    s = '<{}>\'s Most Valuable Passes By OBV at EURO 2020\n'
    htext.fig_htext(s.format(player_name), 0.09, 0.915, highlight_colors=[team_colour], highlight_weights=['bold'], string_weight='bold', fontsize=15, fontfamily=title_font, color=text_colour)


    ### Add Plot Subtitle
    #fig.text(0.04, 1.029, f'EURO 2020 {subtitle}', fontweight='regular', fontsize=20, fontfamily=title_font, color=text_colour)


    ### Add UEFA EURO 2020 logo
    #ax2 = fig.add_axes([0.81, 0.80, 0.12, 0.12])
    #ax2.axis('off')
    #img = image.imread('../img/competitions/uefa_euro_2020.png')
    #ax2.imshow(img)


    ### Add StatsBomb logo
    #ax3 = fig.add_axes([0.67, 0.02, 0.15, 0.15])
    #ax3.axis('off')
    #img = image.imread('../img/logos/stats-bomb-logo.png')
    #ax3.imshow(img)


    ### Add StatsBomb 360 logo
    #ax4 = fig.add_axes([0.83, 0.060, 0.075, 0.075])
    #ax4.axis('off')
    #img = image.imread('../img/logos/stats-bomb-360-logo.png')
    #ax4.imshow(img)


    ### Footnote
    plt.figtext(0.09,
                0.010,
                f'Created by Edd Webster / @eddwebster. Data provided by StatsBomb.\n',
                fontstyle='italic',
                fontsize=11, 
                fontfamily=main_font,
                color=text_colour
               )

    
    ### Save figure
    if not os.path.exists(fig_dir + f'/{n_passes}_valuable_passes_{player_name}_{orientation}_{aspect}.png'):
        plt.savefig(fig_dir + f'/{n_passes}_valuable_passes_{player_name}_{orientation}_{aspect}.png', bbox_inches='tight', dpi=300)
    else:
        pass


    ### Show plt
    plt.tight_layout()
    plt.show()