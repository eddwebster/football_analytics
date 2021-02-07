# -*- coding: utf-8 -*-
"""
Created on Fri May 29 18:27:25 2020

@author: gkgok
"""


import metrica_io as io
import metrica_viz as viz
import metrica_velocity as mvelocity
import metrica_pitch_control as mpc

import matplotlib.pyplot as plt
import os


data_dir = 'D:\Football\Data\MetricaSports\data'
game_id = 2

# Read event data
event_data = io.read_event_data(data_dir, game_id)

# Store event columns
event_cols = list(event_data.columns)


# Convert from metrica data coordinate system to
# a sytem where the center of the pitch is 0,0
event_data = io.convert_data(event_data)


# Read and store home and away team events
home_team_events = event_data[ event_data['Team'] == 'Home']
away_team_events = event_data[ event_data['Team'] == 'Away']

home_team_events, away_team_events, event_data = io.to_single_half(home_team_events, away_team_events, event_data)

# All types of event
event_data['Type'].value_counts()


# Get shots
shots = event_data[ event_data['Type'] == 'SHOT']
home_shots = home_team_events[ event_data['Type'] == 'SHOT']
away_shots = away_team_events[ event_data['Type'] == 'SHOT']

# Plot pitch
fig, ax = viz.plot_pitch()

# Plot shots of home team
fig, ax = viz.shot_map(df=home_shots, figax=(fig,ax))

# Plot shots of away team
fig, ax = viz.shot_map(df=home_shots, figax=(fig,ax))

viz.plot_events( event_data.loc[190:198], indicators = ['Marker','Arrow'], annotate=True )

# TRACKING DATA

events = io.read_event_data(data_dir,game_id)

tracking_home = io.read_tracking_data(data_dir,game_id,'Home')
tracking_away = io.read_tracking_data(data_dir,game_id,'Away')

# Convert positions from metrica units to meters (note change in Metrica's coordinate system since the last lesson)
tracking_home = io.convert_data(tracking_home)
tracking_away = io.convert_data(tracking_away)
events = io.convert_data(events)


# Calculate player velocities
tracking_home = mvelocity.calc_player_velocities(tracking_home,smoothing=True)
tracking_away = mvelocity.calc_player_velocities(tracking_away,smoothing=True)

tracking_home, tracking_away, events = io.to_single_half(tracking_home, tracking_away, events)



# data_dir = 'D:\Football'
# viz.save_match_clip(tracking_home.iloc[73600:73600+500], tracking_away.iloc[73600:73600+500], data_dir, fname='home_goal_2', include_player_velocities=False)


# first get model parameters
params = mpc.default_model_params(3)


PPCF,xgrid,ygrid = mpc.generate_pitch_control_for_event(820, events, tracking_home, tracking_away, params, field_dimen = (106.,68.,), n_grid_cells_x = 50)
viz.plot_pitchcontrol_for_event( 820, events,  tracking_home, tracking_away, PPCF, xgrid, ygrid, annotate=True )



# viz.plot_frame( tracking_home.loc[800:801],tracking_away.loc[800:801], figax=None, team_colors=('r','b'), field_dimen = (106.0,68.0), include_player_velocities=False, PlayerMarkerSize=10, PlayerAlpha=0.7, annotate=False )

# viz.plot_Delaunay_for_frame(800, tracking_home, tracking_away, team='Away', include_player_velocities=False )


import moviepy.editor as mpy
from moviepy.video.io.bindings import mplfig_to_npimage
import math


starting_frame = 10715
end_frame = 12300
f = 25
    
def make_frame(t):
    t2 = int(math.ceil(t*f+0.0001)-1)
    #print(t ,t2+starting_frame, 'dscsd')
    
    fig, ax = viz.plot_Delaunay_for_frame(t2+starting_frame, tracking_home, tracking_away, team='Awat', include_player_velocities=False )

    image = mplfig_to_npimage(fig)
    return image # returns a 8-bit RGB array

clip = mpy.VideoClip(make_frame, duration=((end_frame-starting_frame)/f)).set_fps(f) # 2 seconds
clip.write_videofile("Goal-Delaunay-away.mp4")#video file is saved


