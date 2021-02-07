# -*- coding: utf-8 -*-
"""
Created on Fri May 29 18:29:29 2020

@author: gkgok
"""



import numpy as np
import pandas as pd
import csv


def read_event_data(data_dir, game_id):
    """
    Parameters
    ----------
    data_dir : string - The directory in which the data is present.
    game_dir : integer - The id of the game

    Returns
    -------
    event data

    """
    
    file_loc = '/Sample_Game_{0}/Sample_Game_{0}_RawEventsData.csv'.format(game_id)
    event_data = pd.read_csv(data_dir + file_loc)  
    
    return event_data



def convert_data(df):
    """
    Parameters
    ----------
    df : event_data 

    Returns
    -------
    event_data

    """
    
    field_dims = (105.0,68.0)
    
    x_cols = [col for col in df.columns if col[-1].lower() == 'x' ]
    y_cols = [col for col in df.columns if col[-1].lower() == 'y' ]
    
    
    df[x_cols] = (df[x_cols] - 0.5) * field_dims[0]
    df[y_cols] = -1 * (df[y_cols] - 0.5) * field_dims[1]
    
    return df

def to_single_half(home_data, away_data, events):
    """
    

    Parameters
    ----------
    home_data : home_data.
    away_data : away_data.
    events : events.

    Returns
    -------
    home_data, away_data, events after converting to a single half
    """
    
    for team in [home_data, away_data, events]:
        # Get the first frame of the second half
        second_half_id = team['Period'].idxmax(2)
        # Get the coordinates of both ball and players
        cols = [ col for col in team.columns if col[-1].lower() in ['x','y']]
        
        team.loc[second_half_id:, cols] *= -1
        
    return home_data, away_data, events
        

def read_tracking_data(data_dir, game_id, teamname):
    """
    Parameters
    ----------
    data_dir : string - The directory in which the data is present.
    game_dir : integer - The id of the game
    teamname : 'Home' or 'Away' team 

    Returns
    -------
    tracking data
    
    """
    
    teamfile = '/Sample_Game_%d/Sample_Game_%d_RawTrackingData_%s_Team.csv' % (game_id,game_id,teamname)


    # Create a CSV file reader
    csvfile =  open('{}/{}'.format(data_dir, teamfile), 'r')
    reader = csv.reader(csvfile) 
    
    # Extract team name home/away
    teamnamefull = next(reader)[3].lower()
    print("Reading team: %s" % teamnamefull)
    
    # extract player jersey numbers from second row
    jerseys = [x for x in next(reader) if x != ''] 
    columns = next(reader)
    
    
    # create x & y position column headers for each player
    for i, j in enumerate(jerseys):
        columns[i * 2 + 3] = "{}_{}_x".format(teamname, j)
        columns[i * 2 + 4] = "{}_{}_y".format(teamname, j)
        
    # column headers for the x & y positions of the ball
    columns[-2] = "ball_x"
    columns[-1] = "ball_y"
    

    tracking_data = pd.read_csv('{}/{}'.format(data_dir, teamfile), names=columns, index_col='Frame', skiprows=3)
    
    return tracking_data



