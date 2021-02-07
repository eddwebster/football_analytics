# -*- coding: utf-8 -*-
"""
Created on Fri May 29 18:29:41 2020

@author: gkgok
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.animation as animation
from scipy.spatial import Delaunay



def plot_pitch( field_dimen = (106.0,68.0), field_color ='green', linewidth=2, markersize=20):
    """
    Parameters
    ----------
    field_dimen : TYPE, optional
        DESCRIPTION. The default is (106.0,68.0).
    field_color : TYPE, optional
        DESCRIPTION. The default is 'green'.
    linewidth : TYPE, optional
        DESCRIPTION. The default is 2.
    markersize : TYPE, optional
        DESCRIPTION. The default is 20.

    Returns
    -------
    fig,ax

    """

    fig,ax = plt.subplots(figsize=(12,8)) # create a figure 
    
    if field_color=='green':
        ax.set_facecolor('mediumseagreen')
        lc = 'whitesmoke' # line color
        pc = 'w' # 'spot' colors
    elif field_color=='white':
        lc = 'k'
        pc = 'k'

    # ALL DIMENSIONS IN m
    border_dimen = (3,3) # include a border arround of the field of width 3m
    meters_per_yard = 0.9144 # unit conversion from yards to meters
    half_pitch_length = field_dimen[0]/2. # length of half pitch
    half_pitch_width = field_dimen[1]/2. # width of half pitch
    signs = [-1,1] 
    
    # Soccer field dimensions typically defined in yards, so we need to convert to meters
    goal_line_width = 8*meters_per_yard
    box_width = 20*meters_per_yard
    box_length = 6*meters_per_yard
    area_width = 44*meters_per_yard
    area_length = 18*meters_per_yard
    penalty_spot = 12*meters_per_yard
    corner_radius = 1*meters_per_yard
    D_length = 8*meters_per_yard
    D_radius = 10*meters_per_yard
    D_pos = 12*meters_per_yard
    centre_circle_radius = 10*meters_per_yard
    
    # plot half way line # center circle
    ax.plot([0,0],[-half_pitch_width,half_pitch_width],lc,linewidth=linewidth)
    ax.scatter(0.0,0.0,marker='o',facecolor=lc,linewidth=0,s=markersize)
    
    y = np.linspace(-1,1,50)*centre_circle_radius
    x = np.sqrt(centre_circle_radius**2-y**2)
    
    ax.plot(x,y,lc,linewidth=linewidth)
    ax.plot(-x,y,lc,linewidth=linewidth)
    
    for s in signs: # plots each line seperately
        # plot pitch boundary
        ax.plot([-half_pitch_length,half_pitch_length],[s*half_pitch_width,s*half_pitch_width],lc,linewidth=linewidth)
        ax.plot([s*half_pitch_length,s*half_pitch_length],[-half_pitch_width,half_pitch_width],lc,linewidth=linewidth)
        # goal posts & line
        ax.plot( [s*half_pitch_length,s*half_pitch_length],[-goal_line_width/2.,goal_line_width/2.],pc+'s',markersize=6*markersize/20.,linewidth=linewidth)
        # 6 yard box
        ax.plot([s*half_pitch_length,s*half_pitch_length-s*box_length],[box_width/2.,box_width/2.],lc,linewidth=linewidth)
        ax.plot([s*half_pitch_length,s*half_pitch_length-s*box_length],[-box_width/2.,-box_width/2.],lc,linewidth=linewidth)
        ax.plot([s*half_pitch_length-s*box_length,s*half_pitch_length-s*box_length],[-box_width/2.,box_width/2.],lc,linewidth=linewidth)
        # penalty area
        ax.plot([s*half_pitch_length,s*half_pitch_length-s*area_length],[area_width/2.,area_width/2.],lc,linewidth=linewidth)
        ax.plot([s*half_pitch_length,s*half_pitch_length-s*area_length],[-area_width/2.,-area_width/2.],lc,linewidth=linewidth)
        ax.plot([s*half_pitch_length-s*area_length,s*half_pitch_length-s*area_length],[-area_width/2.,area_width/2.],lc,linewidth=linewidth)
        # penalty spot
        ax.scatter(s*half_pitch_length-s*penalty_spot,0.0,marker='o',facecolor=lc,linewidth=0,s=markersize)
        # corner flags
        y = np.linspace(0,1,50)*corner_radius
        x = np.sqrt(corner_radius**2-y**2)
        ax.plot(s*half_pitch_length-s*x,-half_pitch_width+y,lc,linewidth=linewidth)
        ax.plot(s*half_pitch_length-s*x,half_pitch_width-y,lc,linewidth=linewidth)
        # draw the D
        y = np.linspace(-1,1,50)*D_length # D_length is the chord of the circle that defines the D
        x = np.sqrt(D_radius**2-y**2)+D_pos
        ax.plot(s*half_pitch_length-s*x,y,lc,linewidth=linewidth)
        
    # remove axis labels and ticks
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])
    # set axis limits
    
    xmax = field_dimen[0]/2. + border_dimen[0]
    ymax = field_dimen[1]/2. + border_dimen[1]
    ax.set_xlim([-xmax,xmax])
    ax.set_ylim([-ymax,ymax])
    ax.set_axisbelow(True)
    
    return fig,ax


def shot_map(df, figax=None):
    '''
    Parameters
    ----------
    df -- all shots.
    fig -- figure.
    ax -- axis.
    
    Returns
    -------
    fig, ax 
    
    '''
    if figax is None:
        fig,ax = plot_pitch()
    else:
        fig, ax = figax
    
    ## iterating thorugh the shot dataframe
    for _, shot in df.iterrows():
        if '-GOAL' in shot['Subtype']:
            color = 'bo'
            label = 'Goal'
        else: 
            color = 'ro'
            label = 'No Goal'

            
        ## plotting the point where the shot took place                
        plt.plot(shot['Start X'], shot['Start Y'], color, label=label)
        
        ## adding an arrow to see the direction of the shot
        ax.annotate("", xy=shot[['End X', 'End Y']],
                    xytext=shot[['Start X', 'Start Y']], 
                    arrowprops=dict(arrowstyle='->', color=color[0]))
    
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='best', bbox_to_anchor=(0.97, 0.96, 0, 0), fontsize=12)
    
    
    return fig, ax
    

def plot_frame( home_team, away_team, figax=None, team_colors=('r','b'), field_dimen = (106.0,68.0), include_player_velocities=False, PlayerMarkerSize=10, PlayerAlpha=0.7, annotate=False ):
    """
    Parameters
    ----------
    hometeam : 
    awayteam : 
    figax : The default is None.
    team_colors : The default is ('r','b').
    field_dimen : The default is (106.0,68.0).
    include_player_velocities : The default is False.
    PlayerMarkerSize : The default is 10.
    PlayerAlpha : The default is 0.7.
    annotate : The default is False.

    Returns
    -------
    None.

    """
    
    if figax is None:
        fig,ax = plot_pitch()
    else:
        fig, ax = figax
    
    for team, color in zip([home_team, away_team], team_colors):
        # Columns names for player (x,y) positions
        x_columns = [ col for col in team.keys() if col[-2:].lower() == '_x' and col != 'ball_x' ]
        y_columns = [ col for col in team.keys() if col[-2:].lower() == '_y' and col != 'ball_y' ]
        
    
        ax.plot( team[x_columns], team[y_columns], color+'o', markersize = PlayerMarkerSize, alpha = PlayerAlpha)
    
        if include_player_velocities:
            # Column names for player velocity (x,y)
            vx_columns = [ '{}_vx'.format(col[:-2]) for col in x_columns ]
            vy_columns = [ '{}_vy'.format(col[:-2]) for col in y_columns ]
            
            ax.quiver( team[x_columns], team[y_columns], team[vx_columns], team[vy_columns], 
                      color=color, scale_units='inches', 
                      scale=10., width=0.0015, headlength=5, headwidth=3, alpha=PlayerAlpha)
    
    # plot the ball 
    ax.plot(home_team['ball_x'], home_team['ball_y'], 'ko', markersize=6, alpha=1.0, linewidth=0)
    
    return fig,ax



def plot_events( events, figax=None, field_dimen = (106.0,68), indicators = ['Marker','Arrow'], color='r', marker_style = 'o', alpha = 0.5, annotate=False):
    """ 
    Parameters
    -----------
        events : row (i.e. instant) of the home team tracking data frame
        fig,ax : Can be used to pass in the (fig,ax) objects of a previously generated pitch. Set to (fig,ax) to use an existing figure, or None (the default) to generate a new pitch plot, 
        field_dimen : tuple containing the length and width of the pitch in meters. Default is (106,68)
        indicators : List containing choices on how to plot the event. 'Marker' places a marker at the 'Start X/Y' location of the event; 'Arrow' draws an arrow from the start to end locations. Can choose one or both.
        color : color of indicator. Default is 'r' (red)
        marker_style : Marker type used to indicate the event position. Default is 'o' (filled ircle).
        alpha : alpha of event marker. Default is 0.5    
        annotate : Boolean determining whether text annotation from event data 'Type' and 'From' fields is shown on plot. Default is False.
        
    Returrns
    -----------
       fig,ax : figure and aixs objects (so that other data can be plotted onto the pitch)

    """
    
    if figax is None:
        fig,ax = plot_pitch()
    else:
        fig, ax = figax
        
    count = 1
    for i,row in events.iterrows():
        if 'Marker' in indicators:
            ax.plot( row['Start X'], row['Start Y'], color+marker_style, alpha=alpha )
        if 'Arrow' in indicators:
            ax.annotate("", xy=row[['End X','End Y']], xytext=row[['Start X','Start Y']], alpha=alpha, arrowprops=dict(alpha=alpha,arrowstyle="->",color=color),annotation_clip=False)
        if annotate:
            textstring = str(count) + ':' + row['Type']
            ax.text( row['Start X'] + 0.5, row['Start Y'] + 0.5, textstring, fontsize=10, color=color)
        count += 1
        
    return fig, ax
        


def save_match_clip(hometeam,awayteam, fpath, fname='clip_test',
                    figax=None, frames_per_second=25,
                    team_colors=('r','b'), field_dimen = (106.0,68.0),
                    include_player_velocities=False, PlayerMarkerSize=10, PlayerAlpha=0.7):
    
    # check that indices match first
    assert np.all( hometeam.index==awayteam.index ), "Home and away team Dataframe indices must be the same"
    # in which case use home team index
    index = hometeam.index
    
    if figax is None:
        fig,ax = plot_pitch(field_dimen=field_dimen)
    else:
        fig,ax = figax
    fig.set_tight_layout(True)
    
    # Set figure and movie settings
    FFMpegWriter = animation.writers['ffmpeg']
    metadata = dict(title='Tracking Data', artist='Matplotlib', comment='Metrica tracking data clip')
    writer = FFMpegWriter(fps=frames_per_second, metadata=metadata)
    fname = fpath + '/' +  fname + '.mp4' # path and filename
    
    print("Generating movie...",end='')
    
    
    with writer.saving(fig, fname, dpi=100):
        for i in index:
            # this is used to collect up all the axis objects so that they can be deleted after each iteration
            figobjs = [] 
            
            for team,color in zip( [hometeam.loc[i],awayteam.loc[i]], team_colors) :
                # column header for player x positions
                x_columns = [col for col in team.keys() if col[-2:].lower()=='_x' and col!='ball_x'] 
                # column header for player y positions
                y_columns = [col for col in team.keys() if col[-2:].lower()=='_y' and col!='ball_y']
               
                # Plot players
                objs, = ax.plot( team[x_columns], team[y_columns], color+'o', MarkerSize=PlayerMarkerSize, alpha=PlayerAlpha ) # plot player positions
                figobjs.append(objs)
                
                if include_player_velocities:
                    # column header for player x positions
                    vx_columns = [ '{}_vx'.format(col[:-2]) for col in x_columns] 
                    # column header for player y positions
                    vy_columns = [ '{}_vy'.format(col[:-2]) for col in y_columns] 
                    
                    # Plot player velocity arrow
                    objs = ax.quiver( team[x_columns], team[y_columns], team[vx_columns], team[vy_columns], color=color, scale_units='inches', scale=10.,width=0.0015,headlength=5,headwidth=3,alpha=PlayerAlpha)
                    figobjs.append(objs)
            # plot ball
            objs, = ax.plot( team['ball_x'], team['ball_y'], 'ko', MarkerSize=6, alpha=1.0, LineWidth=0)
            figobjs.append(objs)
            
            # include match time at the top
            frame_minute =  int( team['Time [s]']/60. )
            frame_second =  ( team['Time [s]']/60. - frame_minute ) * 60.
            timestring = "%d:%1.2f" % ( frame_minute, frame_second  )
            objs = ax.text(-2.5,field_dimen[1]/2.+1., timestring, fontsize=14 )
            figobjs.append(objs)
            
            writer.grab_frame()
            
            # Delete all axis objects (other than pitch lines) in preperation for next frame
            for figobj in figobjs:
                figobj.remove()
    
    print("done")
    plt.clf()
    plt.close(fig)  
    


def plot_pitchcontrol_for_event( event_id, events,  tracking_home, tracking_away, PPCF, xgrid, ygrid, alpha = 0.7, include_player_velocities=True, annotate=False, field_dimen = (106.0,68)):
    """ plot_pitchcontrol_for_event( event_id, events,  tracking_home, tracking_away, PPCF, xgrid, ygrid )
    
    Plots the pitch control surface at the instant of the event given by the event_id. Player and ball positions are overlaid.
    
    Parameters
    -----------
        event_id: Index (not row) of the event that describes the instant at which the pitch control surface should be calculated
        events: Dataframe containing the event data
        tracking_home: (entire) tracking DataFrame for the Home team
        tracking_away: (entire) tracking DataFrame for the Away team
        PPCF: Pitch control surface (dimen (n_grid_cells_x,n_grid_cells_y) ) containing pitch control probability for the attcking team (as returned by the generate_pitch_control_for_event in Metrica_PitchControl)
        xgrid: Positions of the pixels in the x-direction (field length) as returned by the generate_pitch_control_for_event in Metrica_PitchControl
        ygrid: Positions of the pixels in the y-direction (field width) as returned by the generate_pitch_control_for_event in Metrica_PitchControl
        alpha: alpha (transparency) of player markers. Default is 0.7
        include_player_velocities: Boolean variable that determines whether player velocities are also plotted (as quivers). Default is False
        annotate: Boolean variable that determines with player jersey numbers are added to the plot (default is False)
        field_dimen: tuple containing the length and width of the pitch in meters. Default is (106,68)
        
    Returrns
    -----------
       fig,ax : figure and aixs objects (so that other data can be plotted onto the pitch)

    """    

    # pick a pass at which to generate the pitch control surface
    pass_frame = events.loc[event_id]['Start Frame']
    pass_team = events.loc[event_id].Team
    
    # plot frame and event
    fig,ax = plot_pitch(field_color='white', field_dimen = field_dimen)
    plot_frame( tracking_home.loc[pass_frame], tracking_away.loc[pass_frame], figax=(fig,ax), PlayerAlpha=alpha, include_player_velocities=include_player_velocities, annotate=annotate )
    plot_events( events.loc[event_id:event_id], figax = (fig,ax), indicators = ['Marker','Arrow'], annotate=False, color= 'k', alpha=1 )
    
    # plot pitch control surface
    if pass_team=='Home':
        cmap = 'bwr'
    else:
        cmap = 'bwr_r'
    ax.imshow(np.flipud(PPCF), extent=(np.amin(xgrid), np.amax(xgrid), np.amin(ygrid), np.amax(ygrid)),interpolation='hanning',vmin=0.0,vmax=1.0,cmap=cmap,alpha=0.5)
    
    return fig,ax




def plot_pitchcontrol_for_frame( frame,  tracking_home, tracking_away, PPCF, xgrid, ygrid, alpha = 0.7, include_player_velocities=True, annotate=False, field_dimen = (106.0,68), team_pass='Home'):
    """ plot_pitchcontrol_for_frame( event_id, events,  tracking_home, tracking_away, PPCF, xgrid, ygrid )
    
    Plots the pitch control surface at the instant of the event given by the event_id. Player and ball positions are overlaid.
    
    Parameters
    -----------
        event_id: Index (not row) of the event that describes the instant at which the pitch control surface should be calculated
        events: Dataframe containing the event data
        tracking_home: (entire) tracking DataFrame for the Home team
        tracking_away: (entire) tracking DataFrame for the Away team
        PPCF: Pitch control surface (dimen (n_grid_cells_x,n_grid_cells_y) ) containing pitch control probability for the attcking team (as returned by the generate_pitch_control_for_event in Metrica_PitchControl)
        xgrid: Positions of the pixels in the x-direction (field length) as returned by the generate_pitch_control_for_event in Metrica_PitchControl
        ygrid: Positions of the pixels in the y-direction (field width) as returned by the generate_pitch_control_for_event in Metrica_PitchControl
        alpha: alpha (transparency) of player markers. Default is 0.7
        include_player_velocities: Boolean variable that determines whether player velocities are also plotted (as quivers). Default is False
        annotate: Boolean variable that determines with player jersey numbers are added to the plot (default is False)
        field_dimen: tuple containing the length and width of the pitch in meters. Default is (106,68)
        
    Returrns
    -----------
       fig,ax : figure and aixs objects (so that other data can be plotted onto the pitch)

    """    

    # pick a pass at which to generate the pitch control surface
    pass_frame = frame
    pass_team = team_pass
    
    # plot frame and event
    fig,ax = plot_pitch(field_color='white', field_dimen = field_dimen)
    plot_frame( tracking_home.loc[pass_frame], tracking_away.loc[pass_frame], figax=(fig,ax), PlayerAlpha=alpha, include_player_velocities=include_player_velocities, annotate=annotate )
    
    # plot pitch control surface
    if pass_team=='Home':
        cmap = 'bwr'
    else:
        cmap = 'bwr_r'
    ax.imshow(np.flipud(PPCF), extent=(np.amin(xgrid), np.amax(xgrid), np.amin(ygrid), np.amax(ygrid)),interpolation='hanning',vmin=0.0,vmax=1.0,cmap=cmap,alpha=0.5)
    
    return fig,ax




def plot_Delaunay_for_frame(frame, home_team, away_team, team, figax=None, include_player_velocities=False, field_dimen = (106.0,68)):

    if figax is None:
        fig,ax = plot_pitch(field_dimen=field_dimen)
    else:
        fig,ax = figax
        
    colors = ('r','b')

    if team == 'Home':
        select_color = 'r'
    else:
        select_color = 'b'
        
        
    for team, color in zip( [home_team.loc[frame], away_team.loc[frame] ], colors):
        
        x_columns = [ col for col in team.keys() if col[-2:].lower() == '_x' and col != 'ball_x' ]
        y_columns = [ col for col in team.keys() if col[-2:].lower() == '_y' and col != 'ball_y' ]
        
        ax.plot(team[x_columns], team[y_columns], color+'o', MarkerSize=12, alpha=0.7)

        x, y = np.array(team[x_columns][:]), np.array(team[y_columns][:])
        x, y = x[~np.isnan(x)], y[~np.isnan(y)]
        
        
        points = np.hstack([ x[:,np.newaxis], y[:,np.newaxis] ] )
        
        # Delaunay triangulation
        if color == select_color:
            tri = Delaunay(points)
            ax.triplot(x, y, tri.simplices.copy(), color='black')
            
        
        if include_player_velocities == True:
            vx_columns = [ '{}_vx'.format(cols[:-2]) for cols in x_columns ]
            vy_columns = [ '{}_vy'.format(cols[:-2]) for cols in y_columns ]

            # Plot the velocity vectors
            ax.quiver(team[x_columns], team[y_columns], team[vx_columns], team[vy_columns],
                  color=color, scale_units='inches', scale=10., width=0.0015, 
                  headlength=5, headwidth=3, alpha=0.7)
        
    # Plot the ball        
    ax.plot(team['ball_x'], team['ball_y'], 'ko', alpha=0.7)
    
    return fig,ax
            
        



    
    


    

