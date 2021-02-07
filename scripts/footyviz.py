from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.collections import PatchCollection
import matplotlib.patheffects as path_effects
import numpy as np

from scipy.spatial import Voronoi
from shapely.geometry import Polygon

X_SIZE = 105
Y_SIZE = 68

BOX_HEIGHT = (16.5*2 + 7.32)/Y_SIZE*100
BOX_WIDTH = 16.5/X_SIZE*100

GOAL = 7.32/Y_SIZE*100

GOAL_AREA_HEIGHT = 5.4864*2/Y_SIZE*100 + GOAL
GOAL_AREA_WIDTH = 5.4864/X_SIZE*100

SCALERS = np.array([X_SIZE/100, Y_SIZE/100])
pitch_polygon = Polygon(((0,0), (0,100), (100,100), (100,0)))

def draw_pitch(dpi=100, pitch_color='#a8bc95'):
    """Sets up field
    Returns matplotlib fig and axes objects.
    """
    fig = plt.figure(figsize=(12.8, 7.2), dpi=dpi)
    fig.patch.set_facecolor(pitch_color)

    axes = fig.add_subplot(1, 1, 1)
    axes.set_axis_off()
    axes.set_facecolor(pitch_color)
    axes.xaxis.set_visible(False)
    axes.yaxis.set_visible(False)

    axes.set_xlim(0,100)
    axes.set_ylim(0,100)

    plt.xlim([-13.32, 113.32])
    plt.ylim([-5, 105])

    fig.tight_layout(pad=3)

    draw_patches(axes)

    return fig, axes

def draw_patches(axes):
    """
    Draws basic field shapes on an axes
    """
    #pitch
    axes.add_patch(plt.Rectangle((0, 0), 100, 100,
                       edgecolor="white", facecolor="none"))

    #half-way line
    axes.add_line(plt.Line2D([50, 50], [100, 0],
                    c='w'))

    #penalty areas
    axes.add_patch(plt.Rectangle((100-BOX_WIDTH, (100-BOX_HEIGHT)/2),  BOX_WIDTH, BOX_HEIGHT,
                       ec='w', fc='none'))
    axes.add_patch(plt.Rectangle((0, (100-BOX_HEIGHT)/2),  BOX_WIDTH, BOX_HEIGHT,
                               ec='w', fc='none'))

    #goal areas
    axes.add_patch(plt.Rectangle((100-GOAL_AREA_WIDTH, (100-GOAL_AREA_HEIGHT)/2),  GOAL_AREA_WIDTH, GOAL_AREA_HEIGHT,
                       ec='w', fc='none'))
    axes.add_patch(plt.Rectangle((0, (100-GOAL_AREA_HEIGHT)/2),  GOAL_AREA_WIDTH, GOAL_AREA_HEIGHT,
                               ec='w', fc='none'))

    #goals
    axes.add_patch(plt.Rectangle((100, (100-GOAL)/2),  1, GOAL,
                       ec='w', fc='none'))
    axes.add_patch(plt.Rectangle((0, (100-GOAL)/2),  -1, GOAL,
                               ec='w', fc='none'))


    #halfway circle
    axes.add_patch(Ellipse((50, 50), 2*9.15/X_SIZE*100, 2*9.15/Y_SIZE*100,
                                    ec='w', fc='none'))

    return axes

def draw_frame(df, t, dpi=100, fps=20, display_num=False, display_time=False, show_players=True,
               highlight_color=None, highlight_player=None, shadow_player=None, text_color='white', flip=False, **anim_args):
    """
    Draws players from time t (in seconds) from a DataFrame df
    """
    fig, ax = draw_pitch(dpi=dpi)

    dfFrame = get_frame(df, t, fps=fps)
 
    if show_players:
        for pid in dfFrame.index:
            if pid==0:
                #se for bola
                try:
                    z = dfFrame.loc[pid]['z']
                except:
                    z = 0
                size = 1.2+z
                lw = 0.9
                color='black'
                edge='white'
                zorder = 100
            else:
                #se for jogador
                size = 3
                lw = 2
                edge = dfFrame.loc[pid]['edgecolor']

                if pid == highlight_player:
                    color = highlight_color
                else:
                    color = dfFrame.loc[pid]['bgcolor']
                if dfFrame.loc[pid]['team']=='attack':
                    zorder = 21
                else:
                    zorder = 20

            ax.add_artist(Ellipse((dfFrame.loc[pid]['x'],
                                dfFrame.loc[pid]['y']),
                                size/X_SIZE*100, size/Y_SIZE*100,
                                edgecolor=edge,
                                linewidth=lw,
                                facecolor=color,
                                alpha=0.8,
                                zorder=zorder))

            try:
                s = str(int(dfFrame.loc[pid]['player_num']))
            except ValueError:
                s = ''
            text = plt.text(dfFrame.loc[pid]['x'],dfFrame.loc[pid]['y'],s,
                            horizontalalignment='center', verticalalignment='center',
                            fontsize=8, color=text_color, zorder=22, alpha=0.8)

            text.set_path_effects([path_effects.Stroke(linewidth=1, foreground=text_color, alpha=0.8),
                                path_effects.Normal()])
            
    return fig, ax, dfFrame

def add_voronoi_to_fig(fig, ax, dfFrame):
    polygons = {}
    vor, dfVor = calculate_voronoi(dfFrame)
    for index, region in enumerate(vor.regions):
        if not -1 in region:
            if len(region)>0:
                try:
                    pl = dfVor[dfVor['region']==index]
                    polygon = Polygon([vor.vertices[i] for i in region]/SCALERS).intersection(pitch_polygon)
                    polygons[pl.index[0]] = polygon
                    color = pl['bgcolor'].values[0]
                    x, y = polygon.exterior.xy
                    plt.fill(x, y, c=color, alpha=0.30)
                except IndexError:
                    pass
                except AttributeError:
                    pass

    plt.scatter(dfVor['x'], dfVor['y'], c=dfVor['bgcolor'], alpha=0.2)

    return fig, ax, dfFrame

def calculate_voronoi(dfFrame):
    dfTemp = dfFrame.copy().drop(0, errors='ignore')

    values = np.vstack((dfTemp[['x', 'y']].values*SCALERS,
                        [-1000,-1000],
                        [+1000,+1000],
                        [+1000,-1000],
                        [-1000,+1000]
                       ))

    vor = Voronoi(values)

    dfTemp['region'] = vor.point_region[:-4]

    return vor, dfTemp

def get_frame(df, t, fps=20):
    dfFrame = df.loc[int(t*fps)].set_index('player')
    dfFrame.player_num = dfFrame.player_num.fillna('')
    return dfFrame