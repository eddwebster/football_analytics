# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 17:05:14 2020

@author: gkgok
"""



import pandas as pd 
import numpy as np
import json
import os
import matplotlib.pyplot as plt


from FCPython import createPitch
# (fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','black')
# plt.show()

df = pd.read_json("ADD THE PATH TO STATSBOMB competitions.json file")

# Belgium World Cup
req_comp_id = 43
req_season_id = 3


pitchLengthX = 120
pitchWidthY=80
def statsbombXYtoPitch(x,y):
    x = x
    y = (pitchWidthY-y)    
    return (x,y)

# PATH TO THE GAME FILES
match_file_path = ["D:\\Football\\Data\\Statsbomb\\data\\matches\\43\\3.json"]

for i in range(len(match_file_path)):
    
    #Load the list of matches for this competition
    with open(match_file_path[i],encoding='utf-8') as f:
        val = json.load(f)
    
    matches = (pd.json_normalize(val))
    
    
    
    
    
belgium_matches = matches[(matches['home_team.home_team_name']=='Belgium') | (matches['away_team.away_team_name']=='Belgium')].sort_values(by='match_date')


events_path ='D:\\Football\\Data\\Statsbomb\\data\\events\\'

all_shots_list = {}
all_goals_list = {}
all_pass_list = {}
all_assists_list = {}

all_hazard_list = {}


for i in belgium_matches['match_id']:
    
    # print(events_path + '\\' + str(i) + '.json' )
    
    
    with open(events_path + '\\' + str(i) + '.json',encoding='utf-8') as f:
        event_json= json.load(f)
    
    match_event = pd.json_normalize(event_json)    
    match_event_columns = match_event.columns  
    
    # print(match_event.iloc[0,17:18])
    # print(match_event.iloc[1,17:18])
    
    
    
    
    # Space for Player Analysis
    
    # No Own Goals
    shot_event = match_event[(match_event['type.id']==16)]
    pass_event = match_event[(match_event['type.id']==30)]

    
    ### All Belgium Shots
    belgium_shot_event = shot_event[shot_event['possession_team.name']=='Belgium']
    
    #Filter Goals from Shots
    belgium_goal_event = belgium_shot_event[belgium_shot_event['shot.outcome.name']=='Goal']
    
    
    ### All Belgium Passes
    belgium_pass_event = pass_event[(pass_event['possession_team.name']=='Belgium') |
                                    (pass_event['team.name']=='Belgium')
                                    ]
    
    belgium_assist_event = belgium_pass_event[belgium_pass_event['pass.goal_assist']==True]
    
    all_shots_list[i] = belgium_shot_event
    all_goals_list[i] = belgium_goal_event
    all_pass_list[i] = belgium_pass_event
    all_assists_list[i] = belgium_assist_event
    
    all_hazard_list[i] = match_event[(match_event['player.name']=='Eden Hazard')
                         &
                         (
                             (match_event['type.name']=='Ball Receipt*')
                             |
                             (match_event['type.name']=='Carry')
                             |
                             (match_event['type.name']=='Pass'))
                         ]
    
    
    
    
    

all_shots = pd.concat(all_shots_list)
all_goals = pd.concat(all_goals_list)
all_passes = pd.concat(all_pass_list)
all_assists = pd.concat(all_assists_list) 




all_hazard = pd.concat(all_hazard_list)



match_event[(match_event['player.name']=='Axel Witsel')]
all_passes[(all_passes['player.name']=='Kevin De Bruyne')]


# OVERALL BELGIUM SHOTMAP 


for index,data in all_shots.iterrows():
    x,y = statsbombXYtoPitch(data['location'][0],data['location'][1])
    csize = np.sqrt(data['shot.statsbomb_xg']*7.5)
    # csize=1
    
    if(data['shot.outcome.name']=='Goal'):
        ax.add_patch(plt.Circle((x,y),csize,zorder=15,color='blue',alpha=0.4))
    else:
        ax.add_patch(plt.Circle((x,y),csize,zorder=15,color='red',alpha=0.4))



cmp = 0
incmp = 0

(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','black')

for index,data in all_assists.iterrows():
    
    fx,fy = statsbombXYtoPitch(data['location'][0],data['location'][1])
    tx,ty = statsbombXYtoPitch(data['pass.end_location'][0],data['pass.end_location'][1])
    
    

    # if((tx>90)):
        # if(data['pass.outcome.id']==9 or
        #                           data['pass.outcome.id']==75):
    ax.add_patch(plt.Arrow(fx,fy,tx-fx,ty-fy,width=1,zorder=15,color='black',alpha=0.4))
        #     if(tx>102):
        #         print(data['pass.recipient.name'],data['pass.outcome.name'])
        #     incmp+=1
        # else:
        #     ax.add_patch(plt.Arrow(fx,fy,tx-fx,ty-fy,width=1,zorder=15,color='red',alpha=0.7))
        #     cmp+=1
    # else:
    #     ax.add_patch(plt.Arrow(fx,fy,tx-fx,ty-fy,width=1,zorder=15,color='black',alpha=0.2))
    
        
# ax.add_patch(plt.Rectangle((80,0),40,80,alpha=0.1))

from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], marker='o', color='w', label='Completed',
                          markerfacecolor='r', markersize=10),
                    Line2D([0], [0], marker='o', color='w', label='Not Complete',
                          markerfacecolor='black', markersize=10)]
# plt.text(1,9,'Note: Radius denotes xG')

# plt.text(1,0.5,'xG')
# ax.add_patch(plt.Circle((7,5),np.sqrt(0.25*7.5),color='black',zorder=15,alpha=0.3))
# plt.text(4.5,0.5,'0.25')

# ax.add_patch(plt.Circle((12,5),np.sqrt(0.5*7.5),color='black',zorder=15,alpha=0.3))
# plt.text(10.5,0.5,'0.5')

# ax.add_patch(plt.Circle((18,5),np.sqrt(0.75*7.5),color='black',zorder=15,alpha=0.3))
# plt.text(16,0.5,'0.75')

ax.legend(handles=legend_elements,loc='upper right')
plt.title('KDB Final 3rd Passmap vs FRANCE')    
# fig.savefig('D:\\KDB-Final-3rd-Passmap-vs-FRANCE.png', format='png', dpi=800)
plt.show()

print(cmp,incmp)



# =============================================================================
#       SHOTMAP
# =============================================================================

(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','black')

for index,data in all_shots.iterrows():
    
    x,y = statsbombXYtoPitch(data['location'][0],data['location'][1])
    csize = np.sqrt(data['shot.statsbomb_xg']*7.5)
    # csize=5
    
    if(data['shot.outcome.name']=='Goal'):
        ax.add_patch(plt.Circle((x,y),csize,zorder=15,color='red',alpha=0.5))
    else:
        ax.add_patch(plt.Circle((x,y),csize,zorder=15,color='blue',alpha=0.4))
        print(data['shot.statsbomb_xg'])

from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], marker='o', color='w', label='Goal',
                          markerfacecolor='red', markersize=10),
                    Line2D([0], [0], marker='o', color='w', label='Shot',
                          markerfacecolor='blue', markersize=10)]
plt.text(1,9,'Note: Radius denotes xG')

plt.text(1,0.5,'xG')
ax.add_patch(plt.Circle((7,5),np.sqrt(0.25*7.5),color='black',zorder=15,alpha=0.3))
plt.text(4.5,0.5,'0.25')

ax.add_patch(plt.Circle((12,5),np.sqrt(0.5*7.5),color='black',zorder=15,alpha=0.3))
plt.text(10.5,0.5,'0.5')

ax.add_patch(plt.Circle((18,5),np.sqrt(0.75*7.5),color='black',zorder=15,alpha=0.3))
plt.text(16,0.5,'0.75')

ax.legend(handles=legend_elements,loc='upper right')
plt.title('BELGIUM Shotmap vs France')    
# fig.savefig('D:\\BELGIUM-Shotmap-vs-FRANCE.png', format='png', dpi=800)
plt.show()




# all_hazard = match_event[(match_event['player.name']=='Eden Hazard')
#                           &
#                            (
#                               (match_event['type.name']=='Pass'))
#                          ]


incmp=0
cmp=0

(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','black')

for index,data in all_hazard.iterrows():
    
    
    if (data['type.name']=='Carry'):
        fx,fy = statsbombXYtoPitch(data['location'][0],data['location'][1])
        tx,ty = statsbombXYtoPitch(data['carry.end_location'][0],data['carry.end_location'][1])
    
    
        ax.add_patch(plt.Arrow(fx,fy,tx-fx,ty-fy,width=1.2,zorder=15,color='black',alpha=0.5))
    
    
    else:
        if(data['ball_receipt.outcome.name']!='Incomplete'):
            x,y = statsbombXYtoPitch(data['location'][0],data['location'][1])
            ax.add_patch(plt.Circle((x,y),1.25,zorder=15,color='red',alpha=0.5))

        
# ax.add_patch(plt.Rectangle((80,0),40,80,alpha=0.1))
# Line2D([0], [0], color='red', lw=4, label='Unsuccessful Pass',alpha=0.9

from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], marker='o', color='w', label='Touch',
                          markerfacecolor='red', markersize=10),
                    Line2D([0], [0], color='black', label='Carry')]
# plt.text(1,9,'Note: Radius denotes xG')

# plt.text(1,0.5,'xG')
# ax.add_patch(plt.Circle((7,5),np.sqrt(0.25*7.5),color='black',zorder=15,alpha=0.3))
# plt.text(4.5,0.5,'0.25')

# ax.add_patch(plt.Circle((12,5),np.sqrt(0.5*7.5),color='black',zorder=15,alpha=0.3))
# plt.text(10.5,0.5,'0.5')

# ax.add_patch(plt.Circle((18,5),np.sqrt(0.75*7.5),color='black',zorder=15,alpha=0.3))
# plt.text(16,0.5,'0.75')

ax.legend(handles=legend_elements,loc='upper left')
plt.title('Hazard vs France')    
fig.savefig('D:\\Hazard-BallReceipts-FULL.png', format='png', dpi=800)
plt.show()

print(cmp,incmp)
