#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thur Jan 21 18:50:58 2021

Module for measuring player velocities, smoothed using a Savitzky-Golay filter, with Metrica Sport's tracking data.

GitHub repo for Laurie Shaw's code for Metrica Sport's data can be found here:
https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking

Data can be found at: https://github.com/Friends-of-Tracking-Data-FoTD/SoccermaticsForPython/blob/master/12GetSignalityAPI.py. The password required to use the Signality API is available in the Uppsala Mathematical Modelling of Football Slack Group: https://twitter.com/novosomsalvador/status/1290696029634002946. Email rsalvadords@gmail.com if you have any issues.

@author: This code is originally written by Laurie Shaw (@EightyFivePoint) with only slight amendments for Signality compatibility by Edd Webster (@eddwebster). All credit to Laurie Shaw.
"""
import numpy as np
import scipy.signal as signal
import Signality_Viz as sviz

# Adjusted Laurie Shaw's code, also adds acceleration & distance to goal
def calc_player_velocities(team, data_file_name, file_name, smoothing_v=True, smoothing_a=True, distance2goal=True, window=7, maxspeed = 12, pitch_length=106, pitch_width=68):
    # remove any velocity data already in the dataframe
    team = remove_player_velocities(team)
    
    # Get the player ids
    player_ids = np.unique( [ c[:-2] for c in team.columns if c[:4] in ['Home','Away'] ] )
   
    # Calculate the timestep from one frame to the next. Should always be 0.04 within the same half
    dt = 0.04 #team['Time [s]'].diff()
    
    # estimate velocities for players in team
    for player in player_ids: # cycle through players individually
        # difference player positions in timestep dt to get unsmoothed estimate of velocity
        vx = team[player+"_x"].diff() / dt
        vy = team[player+"_y"].diff() / dt
        #ax = vx.diff() / dt
        #ay = vy.diff() / dt
                
        if maxspeed>0:
            # remove unsmoothed data points that exceed the maximum speed (these are most likely position errors)
            raw_speed = np.sqrt( vx**2 + vy**2 )
            #acceleration = raw_speed.diff() / dt
            vx[ raw_speed>maxspeed ] = np.nan
            vy[ raw_speed>maxspeed ] = np.nan
        #if maxacc>0:
          #  ax[ raw_acc>maxacc ] = np.nan
           # ay[ raw_acc>maxacc ] = np.nan           
        if smoothing_v:
            ma_window = np.ones( window ) / window 
            vx = np.convolve( vx, ma_window, mode='same') 
            vy = np.convolve( vy, ma_window, mode='same')
#            speed = ( vx**2 + vy**2 )**.5
          #  acceleration = np.diff(speed) / dt
        #    ax = np.convolve( ax, ma_window, mode='same' ) 
         #   ay = np.convolve( ay, ma_window, mode='same' )              
        # put player speed in x,y direction, and total speed back in the data frame
        team[player + "_vx"] = vx
        team[player + "_vy"] = vy
        #team[player + "_ax"] = ax
        #team[player + "_ay"] = ay
        #team[player + "_rawspeed"] = raw_speed
        #team[player + "_rawacc"] = raw_acc
        team[player + "_speed"] = np.sqrt( vx**2 + vy**2 )
        # Calculate acceleration
        acceleration = team[player + "_speed"].diff() / dt
        team[player + "_acceleration"] = acceleration
        if smoothing_a:
            ma_window = np.ones( window ) / window 
            team[player + "_acceleration"] = np.convolve( acceleration, ma_window, mode='same' )        
        if distance2goal: 
            # Calculate distance to goal
            dy2goal = team[player+"_y"]
            # Mirror playing direction for both halves
            # Hammarby starts 1st half playing from right to left in all 3 matches so we don't have to adjust for different matches
            if data_file_name == file_name+'.1':              # 1st half
                dx2goal = (pitch_length/2) + team[player+"_x"]
            if  data_file_name == file_name+'.2':             # 2nd half
                dx2goal = (pitch_length/2) - team[player+"_x"]
            
            dist2goal = np.sqrt( dx2goal**2 + dy2goal**2 )
            team[player + "_dist2goal"] = dist2goal        
    return team


def remove_player_velocity_acceleration_distance(team):
    """
    Clean up function: removes velocities, acceleration, and distance to goal
    """
    # remove player velocities, acceleration, and distance to goal measures that are already in the 'team' dataframe
    # so that they can be cleanly re-calculated
    columns = [c for c in team.columns if c.split('_')[-1] in ['vx','vy','ax','ay','speed','acceleration','D']]
    team = team.drop(columns=columns)
    return team

def remove_player_velocities(team):
    # remove player velocoties and acceleeration measures that are already in the 'team' dataframe
    columns = [c for c in team.columns if c.split('_')[-1] in ['vx','vy','ax','ay','rawspeed','rawacc','speed','acceleration','dx','dy','dist2goal']] # Get the player ids
    team = team.drop(columns=columns)
    return team

def calc_opp_goal_position(shootingDirection, pitchLength):
    """
    Outputs either +1 or -1 if team shooting left-to-right or right-to-left, respectively.
    """
    
    # 1 = left-to-right
    if shootingDirection == 1:
        return (pitchLength/2, 0)
    # -1 = right-to-left
    else:
        return (-1*pitchLength/2, 0)

def compute_accelaration(df):
    """
    Function to determine's player accelaration from the tracking data and estimates the maximum rate of acceleration for each player
    """
    
    # Get the player ids
    v_columns = [i for i in df.columns if '_speed' in i]

    # Calculate the timestep from one frame to the next. Should always be 0.04 within the same half
    dt = df['Time [s]'].diff()
    

    for c in v_columns:
        player = '_'.join(c.split('_')[:2])
        
        ax = df[player+"_vx"].diff() / dt
        ay = df[player+"_vy"].diff() / dt
        
        # put player speed in x,y direction, and total speed back in the data frame
        df[player + "_ax"] = ax
        df[player + "_ay"] = ay
        df[player + "_acc"] = np.sqrt( ax**2 + ay**2 )

    return df
    
# for all players
def calc_distance_nearest_teammate(team,frame_number):
    team = sviz.calc_frame_coordinates(team,frame_number)
    dist = np.sqrt((team.x[:,None]-team.x[None,:])**2 + (team.y[:,None]-team.y[None,:])**2) # calculate distances to all players
    np.fill_diagonal(dist, np.nan)   # To avoid finding 0 distance to himself
    nearest_tm = np.nanmin(dist, axis=0) # Find the smallest distance 
    return nearest_tm

# For all players
def calc_distance_nearest_opponent(team,team_opp,frame_number):
    team = sviz.calc_frame_coordinates(team,frame_number)
    team_opp = sviz.calc_frame_coordinates(team_opp,frame_number)
    nearest_opp = []
    for player in range(11):    # loop over all 11 players
        team12=team_opp.append(team.iloc[player]) # Append player to 11 opponents
        dist = np.sqrt((team12.x[:,None]-team12.x[None,:])**2 + (team12.y[:,None]-team12.y[None,:])**2) # Calculate all distances from all opponents to each other and to the one player we are interested in, so very inefficient but didn't manage to code it in a different way
        np.fill_diagonal(dist, np.nan)
        temp = np.nanmin(dist, axis=0)
        nearest_opp = np.append(nearest_opp, temp[11])    # Filter the only result we are interested in
    return nearest_opp

# for 1 player
def calc_distance_nearest_opponent1player(team,team_opp,frame_number,requested_player):
    team = sviz.calc_frame_coordinates(team,frame_number)
    team_opp = sviz.calc_frame_coordinates(team_opp,frame_number)
    nearest_opp = []
    team12=team_opp.append(team.loc[f'Home_{requested_player}_x',:]) # Append player to 11 opponents,
    dist = np.sqrt((team12.x[:,None]-team12.x[None,:])**2 + (team12.y[:,None]-team12.y[None,:])**2) # Calculate all distances from all opponents to each other and to the one player we are interested in, so very inefficient but didn't manage to code it in a different way
    np.fill_diagonal(dist, np.nan)
    nearest_opp = np.nanmin(dist, axis=0)
    nearest_opp = nearest_opp[11]   # select only result we are interested in; the appended player
    return nearest_opp