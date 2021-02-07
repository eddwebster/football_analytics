#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thur Jan 21 18:50:58 2021

Module for reading in Signality sample data.

GitHub repo for Laurie Shaw's code for Metrica Sports data can be found here:
https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking

Data can be found at: https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython/blob/master/12GetSignalityAPI.py. The password required to use the Signality API is available in the Uppsala Mathematical Modelling of Football Slack Group: https://twitter.com/novosomsalvador/status/1290696029634002946. Email rsalvadords@gmail.com if you have any issues.

@author: This code is originally written by Laurie Shaw (@EightyFivePoint) with only slight amendments for Signality compatibility by Edd Webster (@eddwebster). All credit to Laurie Shaw.
"""

import pandas as pd
import csv as csv
import numpy as np
import glob
import os
from os.path import basename
import json
import datetime
from datetime import date
import time
import math
import pickle
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from copy import deepcopy

# Fran Peralta's custom libraries for working with Signality data
from Libraries import Functions_PreprocessTrackingData as funcs
from Libraries import Dictionaries as dicts

# Set up initial paths to subfolders
base_dir = os.path.join('..', '..', '..', '..')
data_dir = os.path.join(base_dir, 'data')
data_dir_signality = os.path.join(base_dir, 'data', 'signality')
data_dir_signality_tracking = os.path.join(base_dir, 'data', 'signality', 'raw', '2019', 'tracking_data')
scripts_dir = os.path.join(base_dir, 'scripts')
scripts_dir_signality = os.path.join(base_dir, 'scripts', 'signality')
scripts_dir_metrica = os.path.join(base_dir, 'scripts', 'metrica')

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 10:49:00 2020

@author: Fran Peralta
"""

"""============================================================================
===============================================================================

Script that contains all the necessary functions to run the main script
PreprocessTrackingData.py

===============================================================================
============================================================================"""

def initialise_dic_tracks(df_homePlayers, df_awayPlayers):
    """
    Initialises dictionaries for both home and away player locations
    """

    dic_home_tracks = {}
    dic_away_tracks = {}

    for homePlayer in df_homePlayers.playerIndex:
        for xy in ['x','y']:
            dic_home_tracks[f'Home_{homePlayer}_{xy}'] = []

    for awayPlayer in df_awayPlayers.playerIndex:
        for xy in ['x','y']:
            dic_away_tracks[f'Away_{awayPlayer}_{xy}'] = []
            
    return dic_home_tracks, dic_away_tracks

def populate_df_tracks(homeAway, homeAway_tracks, playersJerseyMapping, dic_tracks, df_players):
    """
    For a given team (home OR away), will transform the JSON track data to produce a dataframe just like Laurie's
    """
    
    lst_playerJerseys = df_players.jersey_number.values
    
    # iterating through frames for home/away team
    for n, frame in enumerate(homeAway_tracks):

        lst_playerJerseysPerFrame = []

        for player in frame:
            jersey_number = player.get('jersey_number')
            playerIndex = playersJerseyMapping[jersey_number]
            x,y = player.get('position', [np.nan, np.nan])

            # keeping track of jerseys that have a position for that frame
            lst_playerJerseysPerFrame.append(jersey_number)

            dic_tracks[f'{homeAway}_{playerIndex}_x'].append(x)
            # flipping the y axis to make the data sync with Laurie's plotting methods
            dic_tracks[f'{homeAway}_{playerIndex}_y'].append(-1*y)

        # list of jerseys that aren't in the frame
        lst_playerJerseysNotInFrame = list(set(lst_playerJerseys) - set(lst_playerJerseysPerFrame))

        # adding the jerseys that aren't in frame and providing an x,y position of nan, nan
        for jersey_number in lst_playerJerseysNotInFrame:
            playerIndex = playersJerseyMapping[jersey_number]
            x,y = [np.nan, np.nan]

            dic_tracks[f'{homeAway}_{playerIndex}_x'].append(x)
            dic_tracks[f'{homeAway}_{playerIndex}_y'].append(y)
    
    # transforming tracking dic to a tracking dataframe
    df_tracks = pd.DataFrame(dic_tracks)
    
    return df_tracks

def to_single_playing_direction(home,away):
    """
    Switches x and y co-ords with negative sign in the second half
    Requires the co-ords to be symmetric about 0,0 (i.e. going from roughly -60 to +60 in the x direction and -34 to +34 in the y direction)
    """
    for team in [home,away]:
        second_half_idx = team.Period.idxmax(2)
        columns = [c for c in team.columns if c[-1].lower() in ['x','y']]
        team.loc[second_half_idx:,columns] *= -1
    return home,away

def shoot_direction(gk_x_position):
    """
    Produces either 1 (L2R) or -1 (R2L) based on GK position
    """
    if gk_x_position > 0:
        # shooting right-to-left
        return -1
    else:
        # shotting left-to-right
        return 1

def read_match_data(DATADIR,gameid):
    '''
    read_match_data(DATADIR,gameid):
    read all Signality match data (tracking data for home & away teams, and ecvent data)
    '''
    tracking_home = tracking_data(DATADIR,gameid,'Home')
    tracking_away = tracking_data(DATADIR,gameid,'Away')
    events = read_event_data(DATADIR,gameid)
    return tracking_home,tracking_away,events

def read_event_data(DATADIR,game_id):
    '''
    read_event_data(DATADIR,game_id):
    read Signality event data  for game_id and return as a DataFrame
    '''
    eventfile = '/Sample_Game_%d/Sample_Game_%d_RawEventsData.csv' % (game_id,game_id) # filename
    events = pd.read_csv('{}/{}'.format(DATADIR, eventfile)) # read data
    return events

def tracking_data(DATADIR,game_id,teamname):
    '''
    tracking_data(DATADIR,game_id,teamname):
    read Signality tracking data for game_id and return as a DataFrame. 
    teamname is the name of the team in the filename. For the sample data this is either 'Home' or 'Away'.
    '''
    teamfile = '/Sample_Game_%d/Sample_Game_%d_RawTrackingData_%s_Team.csv' % (game_id,game_id,teamname)
    # First:  deal with file headers so that we can get the player names correct
    csvfile =  open('{}/{}'.format(DATADIR, teamfile), 'r') # create a csv file reader
    reader = csv.reader(csvfile) 
    teamnamefull = next(reader)[3].lower()
    print("Reading team: %s" % teamnamefull)
    # construct column names
    jerseys = [x for x in next(reader) if x != ''] # extract player jersey numbers from second row
    columns = next(reader)
    for i, j in enumerate(jerseys): # create x & y position column headers for each player
        columns[i*2+3] = "{}_{}_x".format(teamname, j)
        columns[i*2+4] = "{}_{}_y".format(teamname, j)
    columns[-2] = "ball_x" # column headers for the x & y positions of the ball
    columns[-1] = "ball_y"
    # Second: read in tracking data and place into pandas Dataframe
    tracking = pd.read_csv('{}/{}'.format(DATADIR, teamfile), names=columns, index_col='Frame', skiprows=3)
    return tracking

def merge_tracking_data(home,away):
    '''
    merge home & away tracking data files into single data frame
    '''
    return home.drop(columns=['ball_x', 'ball_y']).merge( away, left_index=True, right_index=True )
    
def to_metric_coordinates(data,field_dimen=(106.,68.) ):
    '''
    Convert positions from Signality units to meters (with origin at centre circle)
    '''
    x_columns = [c for c in data.columns if c[-1].lower()=='x']
    y_columns = [c for c in data.columns if c[-1].lower()=='y']
    data[x_columns] = ( data[x_columns]-0.5 ) * field_dimen[0]
    data[y_columns] = -1 * ( data[y_columns]-0.5 ) * field_dimen[1]
    ''' 
    ------------ ***NOTE*** ------------
    Signality actually define the origin at the *top*-left of the field, not the bottom-left, as discussed in the YouTube video. 
    I've changed the line above to reflect this. It was originally:
    data[y_columns] = ( data[y_columns]-0.5 ) * field_dimen[1]
    ------------ ********** ------------
    '''
    return data

def shoot_direction(gk_x_position):
    """
    Produces either 1 (L2R) or -1 (R2L) based on GK position
    """
    if gk_x_position > 0:
        # shooting right-to-left
        return -1
    else:
        # shotting left-to-right
        return 1

def find_playing_direction(team,teamname):
    '''
    Find the direction of play for the team (based on where the goalkeepers are at kickoff). +1 is left->right and -1 is right->left
    '''    
    GK_column_x = teamname+"_"+find_goalkeeper(team)+"_x"
    # +ve is left->right, -ve is right->left
    return -np.sign(team.iloc[0][GK_column_x])
    
def find_goalkeeper(team):
    '''
    Find the goalkeeper in team, identifying him/her as the player closest to goal at kick off
    ''' 
    x_columns = [c for c in team.columns if c[-2:].lower()=='_x' and c[:4] in ['Home','Away']]
    GK_col = team.iloc[0][x_columns].abs().idxmax(axis=1)
    return GK_col.split('_')[1]

def parse_raw_to_df(signalityRepo, rootFileName, frame_id, interpolate=True):
    """
    Takes raw root of a match string e.g. 20190930.Hammarby-Örebrö and transforms it into 4 dataframes:
    1) home players
    2) away players
    3) home tracking
    4) away tracking
    """ 
    
    lst_df_home = []
    lst_df_away = []
    
    for half in ['.1','.2']:
        
        # producing filename prefix (just need to add either "-info_live.json" or "-tracks.json")
        fileNamePrefix = rootFileName + half

        # load info
        ## looks like the info JSON is duplicated between the two halves
        with open(os.path.join(signalityRepo, f'{fileNamePrefix}-info_live.json')) as f:
            info = json.load(f)

        # load tracks
        with open(os.path.join(signalityRepo, f'{fileNamePrefix}-tracks.json')) as f:
            tracks = json.load(f)

        # unpacking info
        ## looks like .1 and .2 files are duplicated, so just looking at the .1 (first half file)
        if half == '.1':
            matchId = info.get('id')
            venueId = info.get('venueId')
            timeStart = info.get('time_start')
            pitchLength, pitchWidth = info.get('calibration').get('pitch_size')
            homeTeam = info.get('team_home_name')
            awayTeam = info.get('team_away_name')

            # unpacking players
            homePlayers = info.get('team_home_players')
            awayPlayers = info.get('team_away_players')
            homeLineup = info.get('team_home_lineup')
            awayLineup = info.get('team_away_lineup')
            homeLineupSwitch = {homeLineup[i]:i for i in homeLineup}
            awayLineupSwitch = {awayLineup[i]:i for i in awayLineup}

            # putting player metadata in dataframe
            df_homePlayers = pd.DataFrame(homePlayers)
            df_awayPlayers = pd.DataFrame(awayPlayers)
            df_homePlayers['teamName'] = homeTeam
            df_awayPlayers['teamName'] = awayTeam

            # adding matchId to the player dataframes
            df_homePlayers['matchId'] = matchId
            df_awayPlayers['matchId'] = matchId
            df_homePlayers['matchName'] = rootFileName
            df_awayPlayers['matchName'] = rootFileName

            # adding 1-11 + sub player indices (will probably use these for the final column names like Laurie in the tracks df)
            df_homePlayers['playerIndex'] = [int(homeLineupSwitch[i]) if i in homeLineupSwitch else np.nan for i in df_homePlayers.jersey_number.values]
            df_awayPlayers['playerIndex'] = [int(awayLineupSwitch[i]) if i in awayLineupSwitch else np.nan for i in df_awayPlayers.jersey_number.values]
            df_homePlayers.loc[pd.isna(df_homePlayers['playerIndex']) == True, 'playerIndex'] = np.arange(int(np.nanmax(df_homePlayers.playerIndex))+1, len(df_homePlayers)+1)
            df_awayPlayers.loc[pd.isna(df_awayPlayers['playerIndex']) == True, 'playerIndex'] = np.arange(int(np.nanmax(df_awayPlayers.playerIndex))+1, len(df_awayPlayers)+1)
            df_homePlayers['playerIndex'] = df_homePlayers.playerIndex.apply(lambda x: int(x))
            df_awayPlayers['playerIndex'] = df_awayPlayers.playerIndex.apply(lambda x: int(x))

            # re-jigging cols and re-ordering rows
            df_homePlayers = df_homePlayers[['matchId','matchName','teamName','playerIndex','jersey_number','name']].sort_values('playerIndex')
            df_awayPlayers = df_awayPlayers[['matchId','matchName','teamName','playerIndex','jersey_number','name']].sort_values('playerIndex')

            homePlayersJerseyMapping = {i:j for i, j in zip(df_homePlayers.jersey_number, df_homePlayers.playerIndex)}
            awayPlayersJerseyMapping = {i:j for i, j in zip(df_awayPlayers.jersey_number, df_awayPlayers.playerIndex)}

        ## parsing the track data
        phase = int(half[-1])

        # extracting home and away tracks
        home_tracks = [i.get('home_team') for i in tracks]
        away_tracks = [i.get('away_team') for i in tracks]

        # ball tracks
        ball_tracks = [i.get('ball') for i in tracks]
        ball_tracks_position = [(i.get('position')[0],i.get('position')[1],i.get('position')[2]) if i.get('position') != None else (np.nan, np.nan, np.nan) for i in ball_tracks]
        ball_x = [i[0] for i in ball_tracks_position]
        # flipping the y-coordinate
        ball_y = [-1*i[1] for i in ball_tracks_position]
        ball_z = [i[2] for i in ball_tracks_position]
        ball_jerseyPossession = [i.get('player') for i in ball_tracks]
        ball_jerseyPossession = [int(i) if pd.isna(i) == False else np.nan for i in ball_jerseyPossession]

        # match timestamps
        match_time = [i.get('match_time') for i in tracks]
        period = [i.get('phase') for i in tracks]
        timeStamp = pd.to_datetime([datetime.datetime.utcfromtimestamp(i.get('utc_time')/1000) for i in tracks])

        # unpacking tracks
        ## 1) initialising dictionaries for home and away teams
        dic_home_tracks, dic_away_tracks = initialise_dic_tracks(df_homePlayers, df_awayPlayers)
        ## 2) producing home tracking dataframe
        df_home_tracks = populate_df_tracks('Home', home_tracks, homePlayersJerseyMapping, dic_home_tracks, df_homePlayers)
        ## 3) producing away tracking dataframe
        df_away_tracks = populate_df_tracks('Away', away_tracks, awayPlayersJerseyMapping, dic_away_tracks, df_awayPlayers)

        # putting things together
        ## 1) home
        df_home_tracks['ball_x'] = ball_x
        df_home_tracks['ball_y'] = ball_y
        df_home_tracks['ball_z'] = ball_z
        
        # at this point we just have player and ball positions in the dataframe, so providing option now to interpolate
        # linearly interpolating (inside only) when there are enclosed NaNs - this is the shortest path, and will thus be the slowest in a set amount of time, so won't overestimate speed / acceleration when we're missing data
        if interpolate:
            df_home_tracks = df_home_tracks.interpolate(method='linear', limit_area='inside')
        
        # and now adding things where we wouldn't want there to be any interpolation (like the ball_jerseyPossession)
        df_home_tracks['halfIndex'] = df_home_tracks.index
        df_home_tracks['matchId'] = matchId
        df_home_tracks['matchName'] = rootFileName
        df_home_tracks['Period'] = period
        df_home_tracks['Time [s]'] = np.array(match_time) / 1000
        df_home_tracks['TimeStamp'] = timeStamp
        df_home_tracks['ball_jerseyPossession'] = ball_jerseyPossession

        ## 2) away
        df_away_tracks['ball_x'] = ball_x
        df_away_tracks['ball_y'] = ball_y
        df_away_tracks['ball_z'] = ball_z
        
        # option to interpolate, like with the home team
        if interpolate:
            df_away_tracks = df_away_tracks.interpolate(method='linear', limit_area='inside')
        
        df_away_tracks['halfIndex'] = df_away_tracks.index
        df_away_tracks['matchId'] = matchId
        df_away_tracks['matchName'] = rootFileName
        df_away_tracks['Period'] = period
        df_away_tracks['Time [s]'] = np.array(match_time) / 1000
        df_away_tracks['TimeStamp'] = timeStamp
        df_away_tracks['ball_jerseyPossession'] = ball_jerseyPossession
        
        lst_df_home.append(df_home_tracks)
        lst_df_away.append(df_away_tracks)
        
    # combining the first and second half data
    df_homeTracks = pd.concat(lst_df_home, ignore_index=True)
    df_awayTracks = pd.concat(lst_df_away, ignore_index=True)
    
    # getting a master index for the full game
    df_homeTracks['index'] = df_homeTracks.index
    df_awayTracks['index'] = df_awayTracks.index
    
    # forcing the second half of the match to follow the same direction as the first
    df_homeTracks, df_awayTracks = to_single_playing_direction(df_homeTracks, df_awayTracks)
    
    # use GK x position to know whether team is shooting right-to-left or left-to-right.
    avHomeGKxTrack = df_homeTracks.Home_1_x.mean()
    avAwayGKxTrack = df_awayTracks.Away_1_x.mean()
    
    # apply shooting direction to both home and away dataframes
    df_homeTracks['shootingDirection'] = shoot_direction(avHomeGKxTrack)
    df_awayTracks['shootingDirection'] = shoot_direction(avAwayGKxTrack)
    
    
    # Code added to make C Gilson's Data Engineering 
       
    ## Define year
    year = rootFileName[:4]
    
    ## First '.1' or second '.2' half of the match
    data_file_name=rootFileName+'.1'
    
    ## 
    [ball_position_not_transf, players_position_not_transf, players_team_id, events, players_jersey, info_match, names_of_players] = funcs.LoadDataHammarbyNewStructure2020(data_file_name, data_dir_signality_tracking + '/')
    
    ## 
    team_index = players_team_id[frame_id].astype(int).reshape(len(players_team_id[frame_id]),)
    players_in_play = funcs.GetPlayersInPlay(players_position_not_transf,frame_id)
    
    ## 
    [players_position, ball_position] = funcs.TransformCoords(players_position_not_transf, ball_position_not_transf)
    
    return df_homePlayers, df_awayPlayers, df_homeTracks, df_awayTracks, pitchLength, pitchWidth, homePlayersJerseyMapping, awayPlayersJerseyMapping, ball_position_not_transf, players_position_not_transf, players_team_id, events, players_jersey, info_match, names_of_players, team_index, players_in_play, players_position, ball_position