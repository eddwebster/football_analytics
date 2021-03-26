# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 14:37:48 2019

@author: Fran
"""

"""============================================================================
===============================================================================
Script that gets the live match data from Signality's API and stores it in the
format and folders needed for doing live analyses during matches.

The data is stored in the folders "Tracking Data/" and 
"Twelve-Analysis-Tools/Tracking Data/"
===============================================================================
============================================================================"""

#=============================================================================#
#------------------------------VARIABLES TO FILL IN---------------------------#
#Root of the name for the files
file_name = '20190722.Hammarby-IFElfsborg'
#file_name = '20191020.Hammarby-MalmöFF'
#file_name = '20190930.Hammarby-Örebrö'

#Names of the teams playing in OPTA format
home_team_name = 'Hammarby IF'
away_team_name = 'IF Elfsborg'

game_halves = ['.1','.2']
#=============================================================================#
#-----------------------------------------------------------------------------#

import json
import requests
import gzip
import shutil
import os

from Libraries import Dictionaries as dicts

# Credentials for Signality API
SIGNALITY_API = "https://api.signality.com"
USERNAME = 'allsvenskan2019'
PASSWORD = 'last-civet-verso'


year = file_name[:4]# Create the directories to save the data
save_dir1 = 'Signality/'+year+'/Tracking Data/'
if not os.path.exists(save_dir1):
        os.makedirs(save_dir1)

# Get access token
payload = json.dumps({"username": USERNAME, "password": PASSWORD})
headers = {"Content-Type": "application/json"}
response = requests.post(SIGNALITY_API + "/v3/users/login", data=payload, headers=headers)
response = response.json()
token = response["id"]
user_id = response["userId"]

# Get game id
header = {"Authorization": token, "Content-Type": "application/json"}
response = requests.get(SIGNALITY_API + f"/v3/users/{user_id}/games", headers=header)
available_games = response.json()

for game in available_games:
    if game['team_home_name']==dicts.OptaToSignality(home_team_name) and game['team_away_name']==dicts.OptaToSignality(away_team_name) and game['time_start'][:4]==year:
        game_id = game['id']
        date_of_game = game['time_start']
        break

# Get phase id
header = {"Authorization": token, "Content-Type": "application/json"}
response = requests.get(SIGNALITY_API+"/v3/games/"+game_id+'/phases', headers=header)
available_phases = response.json()
    
for game_half in game_halves:
    if game_half=='.1':
        phase_id = available_phases[0]['id']
    elif game_half=='.2':
        phase_id = available_phases[1]['id']
    
    # Download files
    response = requests.get(SIGNALITY_API+"/v3/games/"+game_id+'?filter=%7B%22include%22%3A%22calibration%22%7D', headers=header)
    info_live = response.json()
    datafile_name = save_dir1+file_name+game_half+'-info_live.json'
    with open(datafile_name, "w") as write_file:
        json.dump(info_live,write_file)
    
    
    files_list = ['events','tracks','stats']
    
    for file in files_list:
        response = requests.get(SIGNALITY_API+"/v3/games/"+game_id+'/phases/'+phase_id+'/'+file, headers=header)
        filename = file_name+game_half+'-'+file+'.json.gz'
        with open(filename, "wb") as f:
            f.write(response.content)
    
    # Extract files
    for file in files_list:
        filename = file_name+game_half+'-'+file+'.json.gz'
        with gzip.open(filename, 'rb') as f_in:
            filename_out = save_dir1+file_name+game_half+'-'+file+'.json'
            with open(filename_out, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    
            
    # Remove compressed files
    for file in files_list:
        filename = file_name+game_half+'-'+file+'.json.gz'
        os.remove(filename)

# Print the date of the fetched game to check for possible mistakes
print('Date of game: ',date_of_game)