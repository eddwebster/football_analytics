#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 16:41:01 2020

Module for exploring expected possession value (EPV) surfaces using MetricaSports's tracking & event data.

EPV is the probability that a possession will end with a goal given the current location of the ball. Multiplying by a
pitch control surface gives the expected value of moving the ball to any location, accounting for the probability that the 
ball move (pass/carry) is successful.

The EPV surface is saved in the FoT github repo and can be loaded using load_EPV_grid()

A detailed description of EPV can be found in the accompanying video tutorial here: 
    
GitHub repo for this code can be found here:
https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking

Data can be found at: https://github.com/metrica-sports/sample-data

Main Functions
----------

load_EPV_grid(): load pregenerated EPV surface from file. 
calculate_epv_added(): Calculates the expected possession value added by a pass
find_max_value_added_target(): Finds the *maximum* expected possession value that could have been achieved for a pass (defined by the event_id) by searching the entire field for the best target.
    

@author: Laurie Shaw (@EightyFivePoint)

"""

import numpy as np
import Metrica_PitchControl as mpc
import Metrica_IO as mio

def load_EPV_grid(fname='EPV_grid.csv'):
    """ load_EPV_grid(fname='EPV_grid.csv')
    
    # load pregenerated EPV surface from file. 
    
    Parameters
    -----------
        fname: filename & path of EPV grid (default is 'EPV_grid.csv' in the curernt directory)
        
    Returns
    -----------
        EPV: The EPV surface (default is a (32,50) grid)
    
    """
    epv = np.loadtxt(fname, delimiter=',')
    return epv
    
def get_EPV_at_location(position,EPV,attack_direction,field_dimen=(106.,68.)):
    """ get_EPV_at_location
    
    Returns the EPV value at a given (x,y) location
    
    Parameters
    -----------
        position: Tuple containing the (x,y) pitch position
        EPV: tuple Expected Possession value grid (loaded using load_EPV_grid() )
        attack_direction: Sets the attack direction (1: left->right, -1: right->left)
        field_dimen: tuple containing the length and width of the pitch in meters. Default is (106,68)
            
    Returrns
    -----------
        EPV value at input position
        
    """
    
    x,y = position
    if abs(x)>field_dimen[0]/2. or abs(y)>field_dimen[1]/2.:
        return 0.0 # Position is off the field, EPV is zero
    else:
        if attack_direction==-1:
            EPV = np.fliplr(EPV)
        ny,nx = EPV.shape
        dx = field_dimen[0]/float(nx)
        dy = field_dimen[1]/float(ny)
        ix = (x+field_dimen[0]/2.-0.0001)/dx
        iy = (y+field_dimen[1]/2.-0.0001)/dy
        return EPV[int(iy),int(ix)]
    
def calculate_epv_added( event_id, events, tracking_home, tracking_away, GK_numbers, EPV, params):
    """ calculate_epv_added
    
    Calculates the expected possession value added by a pass
    
    Parameters
    -----------
        event_id: Index (not row) of the pass event to calculate EPV-added score
        events: Dataframe containing the event data
        tracking_home: tracking DataFrame for the Home team
        tracking_away: tracking DataFrame for the Away team
        GK_numbers: tuple containing the player id of the goalkeepers for the (home team, away team)
        EPV: tuple Expected Possession value grid (loaded using load_EPV_grid() )
        params: Dictionary of pitch control model parameters (default model parameters can be generated using default_model_params() )
        
    Returrns
    -----------
        EEPV_added: Expected EPV value-added of pass defined by event_id
        EPV_difference: The raw change in EPV (ignoring pitch control) between end and start points of pass

    """
    # pull out pass details from the event data
    pass_start_pos = np.array([events.loc[event_id]['Start X'],events.loc[event_id]['Start Y']])
    pass_target_pos = np.array([events.loc[event_id]['End X'],events.loc[event_id]['End Y']])
    pass_frame = events.loc[event_id]['Start Frame']
    pass_team = events.loc[event_id].Team
    
    # direction of play for atacking team (so we know whether to flip the EPV grid)
    home_attack_direction = mio.find_playing_direction(tracking_home,'Home')
    if pass_team=='Home':
        attack_direction = home_attack_direction
        attacking_players = mpc.initialise_players(tracking_home.loc[pass_frame],'Home',params,GK_numbers[0])
        defending_players = mpc.initialise_players(tracking_away.loc[pass_frame],'Away',params,GK_numbers[1])
    elif pass_team=='Away':
        attack_direction = home_attack_direction*-1
        defending_players = mpc.initialise_players(tracking_home.loc[pass_frame],'Home',params,GK_numbers[0])
        attacking_players = mpc.initialise_players(tracking_away.loc[pass_frame],'Away',params,GK_numbers[1])    
    # flag any players that are offside
    attacking_players = mpc.check_offsides( attacking_players, defending_players, pass_start_pos, GK_numbers)
    # pitch control grid at pass start location
    Patt_start,_ = mpc.calculate_pitch_control_at_target(pass_start_pos, attacking_players, defending_players, pass_start_pos, params)
    # pitch control grid at pass end location
    Patt_target,_ = mpc.calculate_pitch_control_at_target(pass_target_pos, attacking_players, defending_players, pass_start_pos, params)
    
    # EPV at start location
    EPV_start = get_EPV_at_location(pass_start_pos, EPV, attack_direction=attack_direction)
    # EPV at end location
    EPV_target   = get_EPV_at_location(pass_target_pos,EPV,attack_direction=attack_direction)
    
    # 'Expected' EPV at target and start location
    EEPV_target = Patt_target*EPV_target
    EEPV_start = Patt_start*EPV_start
    
    # difference is the (expected) EPV added
    EEPV_added = EEPV_target - EEPV_start
    
    # Also calculate the straight up change in EPV
    EPV_difference = EPV_target - EPV_start

    return EEPV_added, EPV_difference

def find_max_value_added_target( event_id, events, tracking_home, tracking_away, GK_numbers, EPV, params ):
    """ find_max_value_added_target
    
    Finds the *maximum* expected possession value that could have been achieved for a pass (defined by the event_id) by searching the entire field for the best target.
    
    Parameters
    -----------
        event_id: Index (not row) of the pass event to calculate EPV-added score
        events: Dataframe containing the event data
        tracking_home: tracking DataFrame for the Home team
        tracking_away: tracking DataFrame for the Away team
        GK_numbers: tuple containing the player id of the goalkeepers for the (home team, away team)
        EPV: tuple Expected Possession value grid (loaded using load_EPV_grid() )
        params: Dictionary of pitch control model parameters (default model parameters can be generated using default_model_params() )
        
    Returrns
    -----------
        maxEPV_added: maximum EPV value-added that could be achieved at the current instant
        max_target_location: (x,y) location of the position of the maxEPV_added

    """
    # pull out pass details from the event data
    pass_start_pos = np.array([events.loc[event_id]['Start X'],events.loc[event_id]['Start Y']])
    pass_frame = events.loc[event_id]['Start Frame']
    pass_team = events.loc[event_id].Team
    
    # direction of play for atacking team (so we know whether to flip the EPV grid)
    home_attack_direction = mio.find_playing_direction(tracking_home,'Home')
    if pass_team=='Home':
        attack_direction = home_attack_direction
        attacking_players = mpc.initialise_players(tracking_home.loc[pass_frame],'Home',params,GK_numbers[0])
        defending_players = mpc.initialise_players(tracking_away.loc[pass_frame],'Away',params,GK_numbers[1])
    elif pass_team=='Away':
        attack_direction = home_attack_direction*-1
        defending_players = mpc.initialise_players(tracking_home.loc[pass_frame],'Home',params,GK_numbers[0])
        attacking_players = mpc.initialise_players(tracking_away.loc[pass_frame],'Away',params,GK_numbers[1])   
        
    # flag any players that are offside
    attacking_players = mpc.check_offsides( attacking_players, defending_players, pass_start_pos, GK_numbers)
    
    # pitch control grid at pass start location
    Patt_start,_ = mpc.calculate_pitch_control_at_target(pass_start_pos, attacking_players, defending_players, pass_start_pos, params)
    
    # EPV at start location
    EPV_start = get_EPV_at_location(pass_start_pos, EPV, attack_direction=attack_direction)

    # calculate pitch control surface at moment of the pass
    PPCF,xgrid,ygrid = mpc.generate_pitch_control_for_event(event_id, events, tracking_home, tracking_away, params, GK_numbers, field_dimen = (106.,68.,), n_grid_cells_x = 50, offsides=True)
    
    # EPV surface at instance of the pass
    if attack_direction == -1:
        EEPV = np.fliplr(EPV)*PPCF
    else:
        EEPV = EPV*PPCF
        
    # find indices of the maxEPV
    maxEPV_idx = np.unravel_index(EEPV.argmax(),EEPV.shape)
    
    # Expected EPV at current ball position   
    EEPV_start = Patt_start*EPV_start
    
    # maxEPV_added (difference between max location and current ball location)
    maxEPV_added = EEPV.max() - EEPV_start
    
    # location of maximum
    max_target_location = (xgrid[maxEPV_idx[1]], ygrid[maxEPV_idx[0]])

    return maxEPV_added, max_target_location
