# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 21:07:38 2020

@author: gkgok
"""



import pandas as pd 
import numpy as np
import json
import os
import matplotlib.pyplot as plt
from FCPython import createPitch


df = pd.read_json('ADD THE PATH TO STATSBOMB competitions.json file')

# France World Cup
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


# ENG,FRA,BELGIUM,CROATIA --> 7 games
# matches['home_team.home_team_name'].value_counts() + matches['away_team.away_team_name'].value_counts()


# Select France games alone
france_matches = matches[(matches['home_team.home_team_name']=='France') | (matches['away_team.away_team_name']=='France')].sort_values(by='match_date')

# ADD THE PATH TO STATSBOMB events folder
events_path ='D:\\Football\\Data\\Statsbomb\\data\\events\\'

all_shots_list = {}
all_goals_list = {}

all_pogba_data_list = {}

all_griez_recipts_list = {}
all_kylian_recipts_list = {}


for i in france_matches['match_id']:
    
    print(events_path + '\\' + str(i) + '.json' )
    
    
    with open(events_path + '\\' + str(i) + '.json',encoding='utf-8') as f:
        event_json= json.load(f)
    
    match_event = pd.json_normalize(event_json)    
    match_event_columns = match_event.columns    
    
    
    
    # Pogba data and analysis
    pogba_data = match_event[match_event['player.name']=='Moussa Sidi Yaya Dembélé']
    all_pogba_data_list[i] = pogba_data
    
    
    # Griezz ball recipts
    griez_receipts = match_event[(match_event['type.name']=='Shot')
                                 &
                                 (match_event['player.name']=='Antoine Griezmann')]
    
    
    # KYLIAN ball recipts
    kylian_receipts = match_event[(match_event['type.name']=='Ball Receipt*')
                                 &
                                 (match_event['player.name']=='Kylian Mbappé Lottin')]
    
    
    
    
    # No Own Goals
    shot_event = match_event[(match_event['type.id']==16)]
    
    france_shot_event = shot_event[shot_event['possession_team.name']=='France']
    
    #Filter Goals from Shots
    france_goal_event = france_shot_event[france_shot_event['shot.outcome.name']=='Goal']
    
    
    all_shots_list[i] = france_shot_event
    all_goals_list[i] = france_goal_event[france_goal_event['shot.outcome.name']=='Goal']
    
    all_griez_recipts_list[i] = griez_receipts
    all_kylian_recipts_list[i] = kylian_receipts

all_goals = pd.concat(all_goals_list)
all_shots = pd.concat(all_shots_list)

# POGBA STUFF
all_pogba = pd.concat(all_pogba_data_list)
all_pogba_pass = all_pogba[(all_pogba['type.name']=='Pass')]
                            # & 
                            # ((all_pogba['pass.recipient.id']==3009) |
                            #  (all_pogba['pass.recipient.id']==5487) |
                            #  (all_pogba['pass.recipient.id']==3604) |
                            #  (all_pogba['pass.recipient.id']==5477))] 
all_pogba_dispossessed = []




# KYLIANN

all_kylian = pd.concat(all_kylian_recipts_list)

(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','black')
for index,data in all_kylian.iterrows():
    x,y = statsbombXYtoPitch(data['location'][0],data['location'][1])
    
    if(data['ball_receipt.outcome.name']=='Incomplete'):
        ax.add_patch(plt.Circle((x,y),1.1,zorder=15,color='red',alpha=0.5))
    else:
        ax.add_patch(plt.Circle((x,y),1.1,zorder=15,color='blue',alpha=0.4))
    

from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], marker='o', color='w', label='Incomplete',
                          markerfacecolor='r', markersize=10),
                    Line2D([0], [0], marker='o', color='w', label='Successful',
                          markerfacecolor='b', markersize=10)]
ax.legend(handles=legend_elements,loc='upper right')
plt.title('Kylian - At the end of the pass')   
fig.savefig('D:\\Kylian_Receipt.png', format='png', dpi=800) 
plt.show()




# GRIEZZZZZZZZZZZZZZZZZ
all_griezz = pd.concat(all_griez_recipts_list)

(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','black')
for index,data in all_griezz.iterrows():
    x,y = statsbombXYtoPitch(data['location'][0],data['location'][1])
    csize = np.sqrt(data['shot.statsbomb_xg']*10)


    # BALL ReceiptS
    # if(data['ball_receipt.outcome.name']=='Incomplete'):
    #     ax.add_patch(plt.Circle((x,y),1.1,zorder=15,color='red',alpha=0.5))
    # else:
    #     ax.add_patch(plt.Circle((x,y),1.1,zorder=15,color='blue',alpha=0.4))
    
    
    # GOALS AND SHOTS
    if(data['shot.outcome.name']=='Goal'):
        ax.add_patch(plt.Circle((x,y),csize,zorder=15,color='blue',alpha=0.5))
    else:
        ax.add_patch(plt.Circle((x,y),csize,zorder=15,color='red',alpha=0.5))


from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], marker='o', color='w', label='Shot',
                          markerfacecolor='r', markersize=10),
                    Line2D([0], [0], marker='o', color='w', label='Goal',
                          markerfacecolor='b', markersize=10)]
plt.text(1,9,'Note: Radius denotes xG')

plt.text(1,0.5,'xG')
ax.add_patch(plt.Circle((7,5),np.sqrt(0.25*10),color='black',zorder=15,alpha=0.3))
plt.text(4.5,0.5,'0.25')

ax.add_patch(plt.Circle((12,5),np.sqrt(0.5*10),color='black',zorder=15,alpha=0.3))
plt.text(10.5,0.5,'0.5')

ax.add_patch(plt.Circle((18,5),np.sqrt(0.75*10),color='black',zorder=15,alpha=0.3))
plt.text(16,0.5,'0.75')

ax.legend(handles=legend_elements,loc='upper right')
    

from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], marker='o', color='w', label='Shot',
                          markerfacecolor='r', markersize=10),
                    Line2D([0], [0], marker='o', color='w', label='Goal',
                          markerfacecolor='b', markersize=10)]
ax.legend(handles=legend_elements,loc='upper right')
plt.title('Griezmann - ShotMap')   
fig.savefig('D:\\Griezz-ShotMap.png', format='png', dpi=800) 
plt.show()









for (x,y) in all_pogba[all_pogba['type.name']=='Dispossessed']['location']:
    all_pogba_dispossessed.append(statsbombXYtoPitch(x,y))
    
    

mb = 0
gz = 0
og = 0
od = 0


incp=0
cp=0
(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','black')

for index,data in all_pogba_pass.iterrows():
    fx,fy = statsbombXYtoPitch(data['location'][0],data['location'][1])
    tx,ty = statsbombXYtoPitch(data['pass.end_location'][0],data['pass.end_location'][1])
    if((data['pass.outcome.id']!=9) & (data['pass.outcome.id']!=74) & (data['pass.outcome.id']!=75) & (data['pass.outcome.id']!=77)):
        ax.add_patch(plt.Arrow(fx,fy,tx-fx,ty-fy,width=1,zorder=15,color='green',alpha=0.1))
        cp+=1
        # if((data['pass.recipient.id']==3009)):
        #     ax.add_patch(plt.Arrow(fx,fy,tx-fx,ty-fy,width=2,zorder=15,color='red',alpha=0.5))
        #     mb+=1
        # elif((data['pass.recipient.id']==5487)):
        #     ax.add_patch(plt.Arrow(fx,fy,tx-fx,ty-fy,width=2,zorder=15,color='blue',alpha=0.6))   
        #     gz+=1
        # elif((data['pass.recipient.id']==3604)):
        #     ax.add_patch(plt.Arrow(fx,fy,tx-fx,ty-fy,width=2,zorder=15,color='green',alpha=0.7))
        #     og+=1
    # else:
    #     ax.add_patch(plt.Arrow(fx,fy,tx-fx,ty-fy,width=2,zorder=15,color='yellow',alpha=0.8))
    #     od+=1
    else:
        incp+=1
        ax.add_patch(plt.Arrow(fx,fy,tx-fx,ty-fy,width=1,zorder=15,color='red',alpha=0.7))

for (x,y) in all_pogba_dispossessed:
    ax.add_patch(plt.Circle((x,y),1.5,zorder=15,color='blue',alpha=0.5))        
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

legend_elements = [Line2D([0], [0], color='red', lw=4, label='Unsuccessful Pass',alpha=0.9),
                    Line2D([0], [0], color='green', lw=4, label='Successful Pass',alpha=0.34),
                    Line2D([0], [0], marker='o', color='w', label='Dispossessed',
                          markerfacecolor='blue', markersize=13,alpha=0.5)]

ax.legend(handles=legend_elements, loc='best')
# 
# from matplotlib.lines import Line2D
# legend_elements = [Line2D([0], [0], color='red', lw=4, label='Mbappe',alpha=0.5),
#                     Line2D([0], [0], color='blue', lw=4, label='Griezmann',alpha=0.6),
#                     Line2D([0], [0], color='green', lw=4, label='Giroud',alpha=0.7),
#                     Line2D([0], [0], color='black', lw=4, label='Failed Pass',alpha=0.7)]

# ax.legend(handles=legend_elements, loc='best')

plt.title("Paul Pogba WC18 KO")
fig.savefig('D:\\pogba_wc18_KO.png', format='png', dpi=700)        
        
plt.show()
print(incp,cp)
print(mb,gz,og,od)




# OVERALL FRANCE SHOTMAP 

# (fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','black')

# for index,data in all_shots.iterrows():
#     x,y = statsbombXYtoPitch(data['location'][0],data['location'][1])
#     csize = np.sqrt(data['shot.statsbomb_xg']*10)
#     # csize=5
    
#     if(data['shot.outcome.name']=='Goal'):
#         ax.add_patch(plt.Circle((x,y),csize,zorder=15,color='blue',alpha=0.5))
#     else:
#         ax.add_patch(plt.Circle((x,y),csize,zorder=15,color='red',alpha=0.4))


# from matplotlib.lines import Line2D
# legend_elements = [Line2D([0], [0], marker='o', color='w', label='Shot',
#                           markerfacecolor='r', markersize=10),
#                     Line2D([0], [0], marker='o', color='w', label='Goal',
#                           markerfacecolor='b', markersize=10)]
# plt.text(1,9,'Note: Radius denotes xG')

# plt.text(1,0.5,'xG')
# ax.add_patch(plt.Circle((7,5),np.sqrt(0.25*10),color='black',zorder=15,alpha=0.3))
# plt.text(4.5,0.5,'0.25')

# ax.add_patch(plt.Circle((12,5),np.sqrt(0.5*10),color='black',zorder=15,alpha=0.3))
# plt.text(10.5,0.5,'0.5')

# ax.add_patch(plt.Circle((18,5),np.sqrt(0.75*10),color='black',zorder=15,alpha=0.3))
# plt.text(16,0.5,'0.75')

# ax.legend(handles=legend_elements,loc='upper right')
# plt.title('France WC18 Shotmap')    
# fig.savefig('D:\\FRA-shots&goals.png', format='png', dpi=800)
# plt.show()




