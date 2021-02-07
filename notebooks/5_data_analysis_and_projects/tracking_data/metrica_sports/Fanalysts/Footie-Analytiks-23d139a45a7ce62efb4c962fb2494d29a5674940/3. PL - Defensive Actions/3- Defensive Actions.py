# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 12:10:43 2020

@author: gkgok
"""


import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('D:/Football/Data/FBref/PL/Defensive-Action-per90.csv')

df['Player']=df['Player'].apply(lambda x: x.split('\\')[0])


df['Pos'] = df['Pos'].apply(lambda x: x[:2]+'/'+x[2:] if len(x)>2 else x)

min_games = df[(df['90s']>20) & 
               (df['Pos']!='GK') &
               (df['Pos']!='FW') & 
               (
                   (df['Pos']=='DF')|
                   (
                       (df['Pos']=='MF') 
                        & 
                        ((df['Blocks.Blocks'] + df['Tackles.Tkl'] + df['Int']>4) | 
                         (df['Pressures.%']>22  )
                         ) 
                       )
                   )]


# Blocks/90 + Tackles/90  vs      Pressure %
PL_players = pd.read_csv('D:/Football/Data/FBref/PL/Player_name.csv')
PL_players[PL_players['Player'] == data['Player']]['Name']



fig,ax = plt.subplots(figsize=(15,18)) # create a figure 

for ind,data in min_games.iterrows():
    name = PL_players[PL_players['Player'] == data['Player']]['Name'].values[0]

    if(data['Pos']=='DF'):
        if name=='Chilwell' or name=='Tarkowski' or name=='PVA':
            ax.scatter(data['Blocks.Blocks']+data['Tackles.Tkl']+data['Int'],data['Pressures.%'],color='red')
            ax.annotate(name,(data['Blocks.Blocks']+data['Tackles.Tkl']+data['Int']-0.15,data['Pressures.%']-0.25))
        else:
            ax.scatter(data['Blocks.Blocks']+data['Tackles.Tkl']+data['Int'],data['Pressures.%'],color='red')
            ax.annotate(name,(data['Blocks.Blocks']+data['Tackles.Tkl']+data['Int']-0.1,data['Pressures.%']+0.1))
    else:        
        if name=='Milivojević' or name=='Maddison' or name=='Tielemans':
            ax.scatter(data['Blocks.Blocks']+ data['Tackles.Tkl']+data['Int'],data['Pressures.%'],color='blue')
            ax.annotate(name,(data['Blocks.Blocks']+data['Tackles.Tkl']+data['Int']-0.15,data['Pressures.%']+0.2))
        else:
            ax.scatter(data['Blocks.Blocks']+ data['Tackles.Tkl']+data['Int'],data['Pressures.%'],color='blue')
            ax.annotate(name,(data['Blocks.Blocks']+data['Tackles.Tkl']+data['Int']-0.15,data['Pressures.%']-0.3))

    # else:
        # ax.scatter(data['Blocks.Blocks']+ data['Tackles.Tkl'],data['Pressures.%'],color='green')
plt.xlabel('Blocks+Tackles+Interceptions per 90',size=15)
plt.ylabel('Successful Pressure %',size=15)

from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Midfielder', markerfacecolor='blue',markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Defender', markerfacecolor='red',markersize=10)
    ]


fig.text(0.89, 0.80, 'Gokul Krishna\n@gkgokul10',
         fontsize=20, color='black',
         ha='right', va='top', alpha=0.8)

ax.legend(handles=legend_elements,loc='best',prop={'size': 17})
plt.xticks(np.arange(2.0,10.5,0.5))
plt.yticks(np.arange(22,47,1))

plt.grid(color='gray',alpha=0.3)
plt.title('Defensive Actions (played > 1800 mins)',size=20)
plt.savefig('D:/BTI-Def1800Mins.png')
plt.show()




