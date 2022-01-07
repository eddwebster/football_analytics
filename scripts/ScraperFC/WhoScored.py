from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import datetime
from datetime import date
import time
from IPython.display import clear_output
from ScraperFC.shared_functions import *
import json
import os


class WhoScored():

    def __init__(self):
        options = Options()
#         options.add_argument('--headless')
        options.add_argument('window-size=700,600')
        # Use proxy
        proxy = get_proxy()
        options.add_argument('--proxy-server="http={};https={}"'.format(proxy, proxy))
        # don't load images
        prefs = {'profile.managed_default_content_settings.images': 2}
        options.add_experimental_option('prefs', prefs)
        # create driver
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        clear_output()

        
    ############################################################################
    def close(self):
        self.driver.close()
        self.driver.quit()

        
    ############################################################################
    def get_season_link(self, year, league):
        error, valid = check_season(year, league, 'WhoScored')
        if not valid:
            print(error)
            return -1
        
        links = {
            'EPL': 'https://www.whoscored.com/Regions/252/Tournaments/2/England-Premier-League',
            'La Liga': 'https://www.whoscored.com/Regions/206/Tournaments/4/Spain-LaLiga',
            'Bundesliga': 'https://www.whoscored.com/Regions/81/Tournaments/3/Germany-Bundesliga',
            'Serie A': 'https://www.whoscored.com/Regions/108/Tournaments/5/Italy-Serie-A',
            'Ligue 1': 'https://www.whoscored.com/Regions/74/Tournaments/22/France-Ligue-1',
            'Argentina Liga Profesional': 'https://www.whoscored.com/Regions/11/Tournaments/68/Argentina-Liga-Profesional',
            'EFL Championship': 'https://www.whoscored.com/Regions/252/Tournaments/7/England-Championship',
            'EFL1': 'https://www.whoscored.com/Regions/252/Tournaments/8/England-League-One',
            'EFL2': 'https://www.whoscored.com/Regions/252/Tournaments/9/England-League-Two'
        }
        
        if league == 'Argentina Liga Profesional' and year in [2016,2021]:
            year_str = str(year)
        else:
            year_str = '{}/{}'.format(year-1, year)
        
        # Repeatedly try to get the league's homepage
        done = False
        while not done:
            try:
                self.driver.get(links[league])
                done = True
            except:
                self.close()
                self.__init__()
                time.sleep(5)
        print('League page status: {}'.format(self.driver.execute_script('return document.readyState')))
        
        # Wait for season dropdown to be accessible, then find the link to the chosen season
        for el in self.driver.find_elements(By.TAG_NAME, 'select'):
            if el.get_attribute('id') == 'seasons':
                for subel in el.find_elements(By.TAG_NAME, 'option'):
                    if subel.text==year_str:
                        return 'https://www.whoscored.com'+subel.get_attribute('value')
        return -1


    ############################################################################
    def get_match_links(self, year, league):
        error, valid = check_season(year, league, 'WhoScored')
        if not valid:
            print(error)
            return -1
       
        # Go to season page
        season_link = self.get_season_link(year, league)
        if season_link == -1:
            print("Failed to get season link.")
            return -1
        
        # Repeatedly try to get to the season's homepage
        done = False
        while not done:
            try:
                self.driver.get(season_link)
                done = True
            except:
                self.close()
                self.__init__()
                time.sleep(5)
        print('Season page status: {}'.format(self.driver.execute_script('return document.readyState')))
        
        # Gather the links
        links = set()

        # Get the season stages and their URLs
        stage_dropdown_xpath = '//*[@id="stages"]'
        stage_elements = self.driver.find_elements(By.XPATH, '{}/{}'.format(stage_dropdown_xpath, 'option'))
        stage_urls = ['https://www.whoscored.com'+el.get_attribute('value') for el in stage_elements]
        if len(stage_urls) == 0: # if no stages in dropdown, then the current url is the only stage
            stage_urls = [self.driver.current_url, ]

        # Iterate through the stages
        for stage_url in stage_urls:

            # Go to the stage
            self.driver.get(stage_url)
            
            # Go to the fixtures
            fixtures_button = WebDriverWait(
                self.driver, 
                10, 
                ignored_exceptions=[TimeoutException]
            ).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#sub-navigation > ul:nth-child(1) > li:nth-child(2) > a:nth-child(1)")
            ))
            self.driver.execute_script('arguments[0].click()', fixtures_button)
        
            print('{} status: {}'.format(stage_url, 
                                         self.driver.execute_script('return document.readyState')))

            # Gather links for the stage
            done = False
            while not done:
                # Get match links from current month
                time.sleep(5)
                for el in self.driver.find_elements_by_tag_name('a'):
                    if el.get_attribute('class') == 'result-1 rc':
                        links.add(el.get_attribute('href'))
                
                # Determine if there is a previous or not
                prev_week_button = self.driver.find_element_by_css_selector('.previous')
                if 'No data for previous' in prev_week_button.get_attribute('title'):
                    done = True
                else:
                    self.driver.execute_script('arguments[0].click()', prev_week_button)
                    time.sleep(5)
                    prev_week_button = WebDriverWait(
                        self.driver, 
                        20
                    ).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.previous')))
        
        # Convert the set of links to a dict
        match_data_just_links = dict()
        for link in links:
            match_data_just_links[link] = ''
        
        # Save match data dict to json file
        save_filename = '{}_{}_match_data.json'.format(league, year).replace(' ','_')
        with open(save_filename, 'w') as f:
            f.write(json.dumps(match_data_just_links, indent=2))
        print('Match links saved to {}'.format(save_filename))
        
        return match_data_just_links


    ############################################################################
    def scrape_matches(self, year, league):
        error, valid = check_season(year, league, 'WhoScored')
        if not valid:
            print(error)
            return -1

        
        ## Create folders in which to save event, formation, and player data
        
        ### Define list of folders
        lst_folders = ['events', 'formations', 'players']

        ### Make the data directory structure
        for folder in lst_folders:
            path = os.path.join(folder)
            if not os.path.exists(path):
                os.mkdir(path)
        
        
        ## Read match links from file or get them with selenium
        save_filename = '{}_{}_match_data.json'.format(league, year).replace(' ','_')
        if os.path.exists(save_filename):
            with open(save_filename, 'r') as f:
                match_data = json.loads(f.read())
        else:
            match_data = self.get_match_links(year, league)
            if match_data == -1:
                return -1
        
        ## Scrape match data for each link
        i = 0
        
        
        ## Start timer
        tic = datetime.datetime.now()
                    
                    
        ## Print statement
        print(f'{tic}: Scraping, engineering, and saving of the data for the {league} league for the {year} season has now started...')
        
        
        ## Iterate through all the fixtures
        for link in match_data:
            i += 1
            try_count = 0
            while match_data[link] == '':
                try_count += 1
                if try_count > 10:
                    print('Failed to scrape match {}/{} from {}'.format(i, len(match_data), link))
                    return -1
                try:
                    print('{}\rScraping match data for match {}/{} in the {}-{} {} season from {}' \
                              .format(' '*500, i, len(match_data), year-1, year, league, link), end='\r')
                    match_data[link] = self.scrape_match(link)
                  
                    ## Edd's scraping code to save data as CSV files
                    
                    ### Assign JSON string to the item variable 
                    item = match_data[link]    # this part is the JSON string for the individual match
                    
                    ### Extract match detail data
                    matchId =  item['matchId']
                    timeStamp = item['matchCentreData']['timeStamp']
                    attendance = item['matchCentreData']['attendance']
                    venueName = item['matchCentreData']['venueName']
                    refereeName = item['matchCentreData']['referee']['name']
                    weatherCode = item['matchCentreData']['weatherCode']
                    startTime = item['matchCentreData']['startTime']
                    matchDate = startTime.rpartition('T')[0]
                    finalScore = item['matchCentreData']['score']
                    htScore = item['matchCentreData']['htScore']
                    ftScore = item['matchCentreData']['ftScore']
                    etScore = item['matchCentreData']['etScore']
                    pkScore = item['matchCentreData']['pkScore']
                    homeGoals = finalScore.rpartition(' :')[0]
                    awayGoals = finalScore.rpartition(': ')[-1]
                    statusCode = item['matchCentreData']['statusCode']
                    periodCode = item['matchCentreData']['periodCode']
                    homeTeamId = item['matchCentreData']['home']['teamId']
                    homeTeamName = item['matchCentreData']['home']['name']
                    awayTeamId = item['matchCentreData']['away']['teamId']
                    awayTeamName = item['matchCentreData']['away']['name']
                    fullFixture = matchDate + ': ' + homeTeamName + ' (' + homeGoals + ') vs. ' + awayTeamName + ' (' + awayGoals + ')'
                    
                    ###### Check is the match data has already been saved 
                    
                    ####### Define save filename
                    filename = f'{matchDate}_{league}_{homeTeamName}_{homeGoals}_{awayTeamName}_{awayGoals}'.replace(' ', '_').replace('(', '').replace(')', '').replace('-', '').replace(':', '').replace('.', '').replace('__', '_').replace('*', '').lower()

                    ####### Print statement
                    print(f'Checking if the data for {fullFixture} has already been saved...')
                    
                    ####### CSV file for the event data has already been saved for this match, skip
                    if os.path.exists('events/{filename}_event_data.csv'):
                        
                        ######## Print statement
                        print(f'The data for {fullFixture} has already been saved...')
                        pass
                    
                    
                    ####### File does not exist, begin extraction
                    else:
                        
                        ######## Print statement
                        print(f'The data for {fullFixture} has not been saved, scraping and extracting now starting...')
                    
                        
                        ### Extract formation data


                        #### Create empty dictionaries for home and away formations
                        home_formation, away_formation = dict(), dict()


                        #### Get the home formation details
                        for i in range(len(item['matchCentreData']['home']['formations'])):

                            ##### 
                            formation_no = i + 1

                            ##### 
                            home_formation[formation_no] = dict()

                            ##### 
                            for formation in item['matchCentreData']['home']['formations']:
                                home_formation[formation_no]['formationNo'] = i + 1
                                home_formation[formation_no]['formationId'] = item['matchCentreData']['home']['formations'][i]['formationId']
                                home_formation[formation_no]['formationName'] = item['matchCentreData']['home']['formations'][i]['formationName']
                                home_formation[formation_no]['period'] = item['matchCentreData']['home']['formations'][i]['period']
                                home_formation[formation_no]['startMinuteExpanded'] = item['matchCentreData']['home']['formations'][i]['startMinuteExpanded']
                                home_formation[formation_no]['endMinuteExpanded'] = item['matchCentreData']['home']['formations'][i]['endMinuteExpanded']            
                                home_formation[formation_no]['jerseyNumbers'] = item['matchCentreData']['home']['formations'][i]['jerseyNumbers']
                                home_formation[formation_no]['formationSlots'] = item['matchCentreData']['home']['formations'][i]['formationSlots']
                                home_formation[formation_no]['playerIds'] = item['matchCentreData']['home']['formations'][i]['playerIds']
                                home_formation[formation_no]['formationPositions'] = item['matchCentreData']['home']['formations'][i]['formationPositions']


                        #### Get the away formation details
                        for i in range(len(item['matchCentreData']['away']['formations'])):        

                            ##### 
                            formation_no = i + 1

                            ##### 
                            away_formation[formation_no] = dict()

                            ##### 
                            for formation in item['matchCentreData']['away']['formations']:
                                away_formation[formation_no]['formationNo'] = i + 1
                                away_formation[formation_no]['formationId'] = item['matchCentreData']['away']['formations'][i]['formationId']
                                away_formation[formation_no]['formationName'] = item['matchCentreData']['away']['formations'][i]['formationName']
                                away_formation[formation_no]['period'] = item['matchCentreData']['away']['formations'][i]['period']
                                away_formation[formation_no]['startMinuteExpanded'] = item['matchCentreData']['away']['formations'][i]['startMinuteExpanded']
                                away_formation[formation_no]['endMinuteExpanded'] = item['matchCentreData']['away']['formations'][i]['endMinuteExpanded']
                                away_formation[formation_no]['jerseyNumbers'] = item['matchCentreData']['away']['formations'][i]['jerseyNumbers']
                                away_formation[formation_no]['formationSlots'] = item['matchCentreData']['away']['formations'][i]['formationSlots']
                                away_formation[formation_no]['playerIds'] = item['matchCentreData']['away']['formations'][i]['playerIds']
                                away_formation[formation_no]['formationPositions'] = item['matchCentreData']['away']['formations'][i]['formationPositions']


                        #### Convert dictionaries to DataFrames
                        df_home_formations = pd.DataFrame.from_dict(home_formation)
                        df_away_formations = pd.DataFrame.from_dict(away_formation)


                        #### Transpose DataFrames and drop index
                        df_home_formations = pd.DataFrame.from_dict(home_formation).T.reset_index(drop=True)   # transposing the DataFrame to switch the x and y axis
                        df_away_formations = pd.DataFrame.from_dict(away_formation).T.reset_index(drop=True)


                        #### Create new columns from match details

                        ##### Home team 
                        df_home_formations['matchId'] = matchId
                        df_home_formations['homeTeamId'] = homeTeamId
                        df_home_formations['homeTeamName'] = homeTeamName

                        ##### Away team
                        df_away_formations['matchId'] = matchId
                        df_away_formations['awayTeamId'] = awayTeamId
                        df_away_formations['awayTeamName'] = awayTeamName


                        #### Rename formation DataFrame columns

                        ##### Home team 
                        ##df_home_formations['playerIds'] = df_home_formations['playerIds'].astype(str)
                        ##df_home_formations['playerIds'] = df_home_formations['playerIds'].str.replace('[','')
                        ##df_home_formations['playerIds'] = df_home_formations['playerIds'].str.replace(']','')
                        ##df_home_formations_formation_slots = df_home_formations['playerIds'].str.split(", ", expand=True)
                        #df_home_formations_formation_slots.columns = range(df_home_formations_formation_slots.columns.size)
                        #df_home_formations_formation_slots.columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
                        ##df_home_formations_formation_slots.columns = ['player_id_formation_slot_1', 'player_id_formation_slot_2', 'player_id_formation_slot_3', 'player_id_formation_slot_4', 'player_id_formation_slot_5', 'player_id_formation_slot_6', 'player_id_formation_slot_7', 'player_id_formation_slot_8', 'player_id_formation_slot_9', 'player_id_formation_slot_10', 'player_id_formation_slot_11', 'player_id_formation_slot_12', 'player_id_formation_slot_13', 'player_id_formation_slot_14', 'player_id_formation_slot_15', 'player_id_formation_slot_16', 'player_id_formation_slot_17', 'player_id_formation_slot_18', 'player_id_formation_slot_19', 'player_id_formation_slot_20']
                        #df_home_formations_formation_slots = df_home_formations_formation_slots.columns.add_prefix('player_id_formation_slot_')
                        ##df_home_formations = pd.concat([df_home_formations, df_home_formations_formation_slots], axis=1)

                        ##### Away team
                        ##df_away_formations['playerIds'] = df_away_formations['playerIds'].astype(str)
                        ##df_away_formations['playerIds'] = df_away_formations['playerIds'].str.replace('[','')
                        ##df_away_formations['playerIds'] = df_away_formations['playerIds'].str.replace(']','')
                        ##df_away_formations_formation_slots = df_away_formations['playerIds'].str.split(", ", expand=True)
                        #df_away_formations_formation_slots.columns = range(df_away_formations_formation_slots.columns.size)
                        #df_away_formations_formation_slots.columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
                        ##df_away_formations_formation_slots.columns = ['player_id_formation_slot_1', 'player_id_formation_slot_2', 'player_id_formation_slot_3', 'player_id_formation_slot_4', 'player_id_formation_slot_5', 'player_id_formation_slot_6', 'player_id_formation_slot_7', 'player_id_formation_slot_8', 'player_id_formation_slot_9', 'player_id_formation_slot_10', 'player_id_formation_slot_11', 'player_id_formation_slot_12', 'player_id_formation_slot_13', 'player_id_formation_slot_14', 'player_id_formation_slot_15', 'player_id_formation_slot_16', 'player_id_formation_slot_17', 'player_id_formation_slot_18', 'player_id_formation_slot_19', 'player_id_formation_slot_20']
                        #df_away_formations_formation_slots = df_away_formations_formation_slots.columns.add_prefix('player_id_formation_slot_')
                        ##df_away_formations = pd.concat([df_away_formations, df_away_formations_formation_slots], axis=1)


                        ##### Create minute-by-minute formations DataFrame

                        ###### Create minutes DataFrame

                        ####### Define empty minutes list
                        lst_mins = []

                        ####### Append values to minutes list
                        for i in range (130):
                            lst_mins.append(i)

                        ####### Convert minutes list to DataFrame
                        df_mins = pd.DataFrame({'min': lst_mins})


                        ###### Join Formation Changes DataFrame to minutes DataFrame
                        df_home_formations_minute_by_minute = pd.merge(df_mins, df_home_formations, left_on='min', right_on='startMinuteExpanded', how='left')
                        df_away_formations_minute_by_minute = pd.merge(df_mins, df_away_formations, left_on='min', right_on='startMinuteExpanded', how='left')


                        ###### Forward fill null values in the minute-by-minute formation DataFrames
                        df_home_formations_minute_by_minute = df_home_formations_minute_by_minute.ffill()
                        df_away_formations_minute_by_minute = df_away_formations_minute_by_minute.ffill()


                        ###### Determine the last minute of action for each team
                        maxHomeEndMinuteExpanded = df_home_formations_minute_by_minute['endMinuteExpanded'].max()
                        maxAwayEndMinuteExpanded = df_away_formations_minute_by_minute['endMinuteExpanded'].max()


                        ###### Cut the DataFrame of excess minutes
                        df_home_formations_minute_by_minute = df_home_formations_minute_by_minute.head(maxHomeEndMinuteExpanded+1)
                        df_away_formations_minute_by_minute = df_away_formations_minute_by_minute.head(maxAwayEndMinuteExpanded+1)



                        #### Extract player information

                        ##### Get the home and away player IDs
                        home_ids = [player['playerId'] for player in item['matchCentreData']['home']['players']]
                        away_ids = [player['playerId'] for player in item['matchCentreData']['away']['players']]



                        ##### Create dictionaries of players, including their Opta ID, shirt number, minute-by-minute ratings, and other statistics.

                        ###### Create empty dictionaries for home and away players
                        home, away = dict(), dict()


                        ###### Iterate through all home players
                        for i in range(len(item['matchCentreData']['home']['players'])):

                            ####### Get the home player's details
                            home_id = home_ids[i]
                            home[home_id] = dict()
                            for player in item['matchCentreData']['home']['players']:
                                if player['playerId'] == home_id:
                                    home[home_id]['playerId'] = player['playerId']
                                    home[home_id]['name'] = player['name']
                                    home[home_id]['number'] = player['shirtNo']
                                    home[home_id]['position'] = player['position']
                                    home[home_id]['height'] = player['height']
                                    home[home_id]['weight'] = player['weight']
                                    home[home_id]['age'] = player['age']
                                    try:
                                        home[home_id]['isStarter'] = player['isFirstEleven']
                                    except:
                                        home[home_id]['isStarter'] = False
                                    home[home_id]['isManOfTheMatch'] = player['isManOfTheMatch']
                                    home[home_id]['team'] = 'Home'
                                    try:
                                        home[home_id]['ratings'] = player['stats']['ratings']
                                    except:
                                        home[home_id]['ratings'] = np.nan


                        ###### Iterate through all away players
                        for i in range(len(item['matchCentreData']['away']['players'])):

                            ####### Get the away player's details
                            away_id = away_ids[i]
                            away[away_id] = dict()
                            for player in item['matchCentreData']['away']['players']:
                                if player['playerId'] == away_id:
                                    away[away_id]['playerId'] = player['playerId']
                                    away[away_id]['name'] = player['name']
                                    away[away_id]['number'] = player['shirtNo']
                                    away[away_id]['position'] = player['position']
                                    away[away_id]['height'] = player['height']
                                    away[away_id]['weight'] = player['weight']
                                    away[away_id]['age'] = player['age']
                                    try:
                                        away[away_id]['isStarter'] = player['isFirstEleven']
                                    except:
                                        away[away_id]['isStarter'] = False
                                    away[away_id]['isManOfTheMatch'] = player['isManOfTheMatch']
                                    away[away_id]['team'] = 'away'
                                    try:
                                        away[away_id]['ratings'] = player['stats']['ratings']
                                    except:
                                        away[away_id]['ratings'] = np.nan


                        ###### Transpose DataFrames and drop index
                        df_home_players = pd.DataFrame.from_dict(home).T.reset_index(drop=True)   # transposing the DataFrame to switch the x and y axis
                        df_away_players = pd.DataFrame.from_dict(away).T.reset_index(drop=True)


                        ###### Determine player ratings

                        ###### Extract final player reatings
                        df_home_players['finalPlayerRating'] = df_home_players['ratings'].astype(str).str[-5:-1]
                        df_away_players['finalPlayerRating'] = df_away_players['ratings'].astype(str).str[-5:-1]


                        ###### Convert final player ratings to floats
                        df_home_players['finalPlayerRating'] = pd.to_numeric(df_home_players['finalPlayerRating'], errors='coerce')
                        df_away_players['finalPlayerRating'] = pd.to_numeric(df_away_players['finalPlayerRating'], errors='coerce')


                        ###### Determine team final ratings
                        df_home_players['finalTeamRating'] = df_home_players['finalPlayerRating'].mean(skipna=True)
                        df_away_players['finalTeamRating'] = df_away_players['finalPlayerRating'].mean(skipna=True)


                        ###### Round team final ratings
                        df_home_players['finalTeamRating'] = df_home_players['finalTeamRating'].round(2)
                        df_away_players['finalTeamRating'] = df_away_players['finalTeamRating'].round(2)


                        ###### Add match details to Players DataFrame

                        ####### Home players
                        df_home_players['matchId'] = matchId
                        df_home_players['teamId'] = homeTeamId
                        df_home_players['teamName'] = homeTeamName

                        ####### Away players
                        df_away_players['matchId'] = matchId
                        df_away_players['teamId'] = awayTeamId
                        df_away_players['teamName'] = awayTeamName


                        ###### Union the two player datasets

                        ####### Define list of the DataFrame
                        lst_dfs_players = [df_home_players, df_away_players]

                        ####### Union the two DataFrames
                        df_players = pd.concat(lst_dfs_players)


                        ##### Extract Event data

                        ###### Create blank pandas DataFrame
                        df_events = pd.DataFrame(columns=['id',
                                                          'eventId',
                                                          'minute',
                                                          'second',
                                                          'teamId',
                                                          'x',
                                                          'y',
                                                          'expandedMinute',
                                                          'period',
                                                          'type',
                                                          'outcomeType',
                                                          'qualifiers',
                                                          'satisfiedEventsTypes',
                                                          'isTouch',
                                                          'playerId',
                                                          'endX',
                                                          'endY',
                                                          'blockedX',
                                                          'blockedY',
                                                          'goalMouthZ',
                                                          'goalMouthY',
                                                          'isShot',
                                                          'relatedEventId',
                                                          'relatedPlayerId',
                                                          'cardType',
                                                          'isGoal'
                                                         ]
                                                )



                        ###### Create empty list to append JSON
                        lst_events = list()



                        ###### Iterate through events
                        for event in item['matchCentreData']['events']:

                            ####### Append events to list of events
                            lst_events.append(event)


                            ####### Convert to float
                            new_row = pd.Series(dtype='float')


                            ####### Extract each event value

                            ####### Id
                            try:
                                new_row['id'] = int(event['id'])
                            except:
                                new_row['id'] = np.NaN

                            ####### eventId
                            try:
                                new_row['eventId'] = int(event['eventId'])
                            except:
                                new_row['eventId'] = np.NaN

                            ####### minute
                            try:
                                new_row['minute'] = int(event['minute'])
                            except:
                                new_row['minute'] = np.NaN

                            ####### second
                            try:
                                new_row['second'] = int(event['second'])
                            except:
                                new_row['second'] = np.NaN

                            ####### teamId  
                            try:
                                new_row['teamId'] = int(event['teamId'])
                            except:
                                new_row['teamId'] = np.NaN

                            ####### x
                            try:
                                new_row['x'] = int(event['x'])
                            except:
                                new_row['x'] = np.NaN

                            ####### y
                            try:
                                new_row['y'] = int(event['y'])
                            except:
                                new_row['y'] = np.NaN  

                            ####### expandedMinute
                            try:
                                new_row['expandedMinute'] = int(event['expandedMinute'])
                            except:
                                new_row['expandedMinute'] = np.NaN

                           ####### period
                            try:
                                new_row['period'] = str(event['period'])
                            except:
                                new_row['period'] = np.NaN

                            ####### type
                            try:
                                new_row['type'] = str(event['type'])
                            except:
                                new_row['type'] = np.NaN

                            ##### outcomeType
                            try:
                                new_row['outcomeType'] = str(event['outcomeType'])
                            except:
                                new_row['outcomeType'] = np.NaN

                            ##### qualifiers
                            try:
                                new_row['qualifiers'] = str(event['qualifiers'])
                            except:
                                new_row['qualifiers'] = np.NaN

                            ######## satisfiedEventsTypes
                            try:
                                new_row['satisfiedEventsTypes'] = str(event['satisfiedEventsTypes'])
                            except:
                                new_row['satisfiedEventsTypes'] = np.NaN

                            ####### isTouch
                            try:
                                new_row['isTouch'] = bool(event['isTouch'])
                            except:
                                new_row['isTouch'] = np.NaN

                            ####### playerId
                            try:
                                new_row['playerId'] = int(event['playerId'])
                            except:
                                new_row['playerId'] = np.NaN

                            ####### endX
                            try:
                                new_row['endX'] = float(event['endX'])
                            except:
                                new_row['endX'] = np.NaN

                            ####### endY
                            try:
                                new_row['endY'] = float(event['endY'])
                            except:
                                new_row['endY'] = np.NaN   

                            ####### blockedX
                            try:
                                new_row['blockedX'] = float(event['blockedX'])
                            except:
                                new_row['blockedX'] = np.NaN

                            ####### goalMouthZ
                            try:
                                new_row['goalMouthZ'] = float(event['goalMouthZ'])
                            except:
                                new_row['goalMouthZ'] = np.NaN   

                            ####### goalMouthY
                            try:
                                new_row['goalMouthY'] = float(event['goalMouthY'])
                            except:
                                new_row['goalMouthY'] = np.NaN

                            ####### isShot
                            try:
                                new_row['isShot'] = bool(event['isShot'])
                            except:
                                new_row['isShot'] = np.NaN

                            ####### relatedEventId
                            try:
                                new_row['relatedEventId'] = int(event['relatedEventId'])
                            except:
                                new_row['relatedEventId'] = np.NaN

                            ####### relatedPlayerId
                            try:
                                new_row['relatedPlayerId'] = int(event['relatedPlayerId'])
                            except:
                                new_row['relatedPlayerId'] = np.NaN

                            ####### cardType
                            try:
                                new_row['cardType'] = str(event['cardType'])
                            except:
                                new_row['cardType'] = np.NaN    

                            ####### isGoal
                            try:
                                new_row['isGoal'] = bool(event['isGoal'])
                            except:
                                new_row['isGoal'] = np.NaN    


                            ####### Data Engineering of the pandas DataFrame

                            ###### Convert columns to strings
                            df_events['period'] = df_events['period'].astype(str)
                            df_events['type'] = df_events['type'].astype(str)
                            df_events['outcomeType'] = df_events['outcomeType'].astype(str)
                            df_events['qualifiers'] = df_events['qualifiers'].astype(str)
                            df_events['satisfiedEventsTypes'] = df_events['satisfiedEventsTypes'].astype(str)

                            ###### Remove left brackets
                            df_events['period'] = df_events['period'].str.replace('[','')
                            df_events['type'] = df_events['type'].str.replace('[','')
                            df_events['outcomeType'] = df_events['outcomeType'].str.replace('[','')
                            df_events['qualifiers'] = df_events['qualifiers'].str.replace('[','')
                            df_events['satisfiedEventsTypes'] = df_events['satisfiedEventsTypes'].str.replace('[','')

                            ###### Remove right brackets
                            df_events['period'] = df_events['period'].str.replace(']','')
                            df_events['type'] = df_events['type'].str.replace(']','')
                            df_events['outcomeType'] = df_events['outcomeType'].str.replace(']','')
                            df_events['qualifiers'] = df_events['qualifiers'].str.replace(']','')
                            df_events['satisfiedEventsTypes'] = df_events['satisfiedEventsTypes'].str.replace(']','')

                            ###### Create 'Id' columns - extracting digits
                            df_events['periodId'] = df_events['period'].str.extract('(\d+)')
                            df_events['typeId'] = df_events['type'].str.extract('(\d+)')
                            df_events['outcomeTypeId'] = df_events['outcomeType'].str.extract('(\d+)')
                            #df_events['qualifiersId'] = df_events['qualifiers'].str.extract('(\d+)')

                            ###### Create 'TypeName' columns - varying logic
                            df_events['periodName'] = df_events['period'].str.rsplit("'displayName': '", 1).str[-1].str.rsplit("'", 1).str[0]
                            df_events['typeName'] = df_events['type'].str.rsplit("'displayName': '", 1).str[-1].str.rsplit("'", 1).str[0]
                            df_events['outcomeTypeName'] = df_events['outcomeType'].str.rsplit("'displayName': '", 1).str[-1].str.rsplit("'", 1).str[0]
                            #df_events['outcomeTypeName'] = np.where(df_events['outcomeTypeId'] == '1', True, False)    # alternative method


                            ####### Append data to row
                            df_events = df_events.append(new_row, ignore_index=True)



                        ###### Create new columns with match and team details
                        df_events['matchId'] = matchId
                        df_events['timeStamp'] = timeStamp
                        df_events['attendance'] = attendance
                        df_events['venueName'] = venueName
                        df_events['refereeName'] = refereeName
                        df_events['weatherCode'] = weatherCode
                        df_events['startTime'] = startTime
                        df_events['matchDate'] = matchDate
                        df_events['finalScore'] = finalScore
                        df_events['htScore'] = htScore
                        df_events['ftScore'] = ftScore
                        df_events['etScore'] = etScore
                        df_events['pkScore'] = pkScore
                        df_events['homeGoals'] = homeGoals
                        df_events['awayGoals'] = awayGoals
                        df_events['statusCode'] = statusCode
                        df_events['periodCode'] = periodCode
                        df_events['homeTeamId'] = homeTeamId
                        df_events['homeTeamName'] = homeTeamName 
                        df_events['awayTeamId'] = awayTeamId
                        df_events['awayTeamName'] = awayTeamName
                        df_events['fullFixture '] = fullFixture



                        ###### Streamline the formations DataFrames to only have important columns to be added to the Event data

                        ####### Define columns of interest
                        lst_cols_formations = ['min',
                                               'formationId',
                                               'formationName',
                                               'startMinuteExpanded'
                                              ]

                        ####### Select columns of interest for home and away formations
                        df_home_formations_minute_by_minute_select = df_home_formations_minute_by_minute[lst_cols_formations]
                        df_away_formations_minute_by_minute_select = df_away_formations_minute_by_minute[lst_cols_formations]



                        ###### Rename columns

                        ####### Home
                        df_home_formations_minute_by_minute_select = (df_home_formations_minute_by_minute_select
                                                                          .rename(columns={'min': 'homeMin',
                                                                                           'formationId': 'homeFormationId',
                                                                                           'formationName': 'homeFormationName',
                                                                                           'startMinuteExpanded': 'homeStartMinuteExpanded',
                                                                                         }
                                                                                )
                                                                     )

                        ####### Away
                        df_away_formations_minute_by_minute_select = (df_away_formations_minute_by_minute_select
                                                                          .rename(columns={'min': 'awayMin',
                                                                                           'formationId': 'awayFormationId',
                                                                                           'formationName': 'awayFormationName',
                                                                                           'startMinuteExpanded': 'awayStartMinuteExpanded',
                                                                                         }
                                                                                )
                                                                     )

                        ####### Join on formation data to the Event data

                        ####### Home
                        df_events = pd.merge(df_events, df_home_formations_minute_by_minute_select, left_on='minute', right_on='homeMin', how='left')


                        ####### Away
                        df_events = pd.merge(df_events, df_away_formations_minute_by_minute_select, left_on='minute', right_on='awayMin', how='left')


                        ####### Drop 'StartMinuteExpanded' columns
                        df_events = df_events.drop(['homeMin',
                                                    'awayMin',
                                                    'homeStartMinuteExpanded',
                                                    'awayStartMinuteExpanded'
                                                   ], axis=1
                                                  )


                        ####### Add columns for player details to the Event data

                        ####### Select player columns of interest

                        ######### Define columns of interest
                        lst_cols_players = ['playerId',
                                            'name',
                                            'number',
                                            'position',
                                            'isStarter',
                                            'isManOfTheMatch',
                                            'finalPlayerRating',
                                            'finalTeamRating'
                                           ]


                        ######### Select columns of interest for players
                        df_players_select = df_players[lst_cols_players]


                        ####### Join on player data to Event data
                        df_events = pd.merge(df_events, df_players_select, left_on='playerId', right_on='playerId', how='left')


                        ####### Select related player columns of interest

                        ######## Define columns of interest
                        lst_cols_related_players = ['playerId',
                                                    'name',
                                                    'number',
                                                    'position'
                                                   ]

                        ######## Select columns of interest for players
                        df_related_players_select = df_players_select[lst_cols_related_players]


                        ######## Rename columns
                        df_related_players_select = df_related_players_select.rename(columns={'playerId': 'relatedPlayerId',
                                                                                              'name': 'relatedPlayerName',
                                                                                              'number': 'relatedPlayerNumber',
                                                                                              'position': 'relatedPlayerPosition'
                                                                                             }
                                                                                    )

                        ######## Join on related player data to Event data
                        df_events = pd.merge(df_events, df_related_players_select , left_on='relatedPlayerId', right_on='relatedPlayerId', how='left')

                        ######## Fill blank values with NA
                        df_events['qualifiers'] = df_events['qualifiers'].fillna(np.nan)
                        df_events['satisfiedEventsTypes'] = df_events['satisfiedEventsTypes'].fillna(np.nan)



                        ###### Save to CSV

                        ####### Define save filename
                        save_filename = f'{matchDate}_{league}_{homeTeamName}_{homeGoals}_{awayTeamName}_{awayGoals}'.replace(' ', '_').replace('(', '').replace(')', '').replace('-', '').replace(':', '').replace('.', '').replace('__', '_').replace('*', '').lower()

                        ####### 
                        print(f'Saving data for {fullFixture} in the {league} league for the {year} season.')

                        ######## Home formation data 
                        print(f'>>> Saving home formation data...')
                        df_home_formations.to_csv(f'formations/{save_filename}_home_formation_data.csv', index=None, header=True)

                        ######## Away formation data 
                        print(f'>>> Saving away formation data...')
                        df_away_formations.to_csv(f'formations/{save_filename}_away_formation_data.csv', index=None, header=True)

                        ######## Home formation data 
                        #print(f'>>> Saving home formation minute-by-minute data...')
                        #df_home_formations_minute_by_minute.to_csv(f'formations/{save_filename}_home_formation_minute_by_minute_data.csv', index=None, header=True)

                        ######## Away formation data 
                        #print(f'>>> Saving away formation minute-by-minute data...')
                        #df_away_formations_minute_by_minute.to_csv(f'formations/{save_filename}_away_formation_minute_by_minute_data.csv', index=None, header=True)

                        ######## Player data 
                        print(f'>>> Saving player data...')
                        df_players.to_csv(f'players/{save_filename}_player_data.csv', index=None, header=True)

                        ######## Event data 
                        print(f'>>> Saving event data...')
                        df_events.to_csv(f'events/{save_filename}_event_data.csv', index=None, header=True)


                        ######## Print statement
                        print(f'Scraping, engineering, and saving of the data for the {league} league for the {year} season is now complete')
                    

                    
                except:
                    print('\n\nError encountered. Saving output and restarting webdriver.')
                    with open(save_filename, 'w') as f:
                        f.write(json.dumps(match_data))
                    self.close()
                    self.__init__()
                    time.sleep(5)
                    
                
                
        ### End timer
        toc = datetime.datetime.now()
        
        
        
        ### Print statement
        print(f'{toc}: Scraping, engineering, and saving of the data for the {league} league for the {year} season has now ended...')
        
        
        
        ### Save all output
        with open(save_filename, 'w') as f:
            f.write(json.dumps(match_data))
        return match_data


    ############################################################################
    def scrape_match(self, link):
        self.driver.get(link)
        scripts = list()
        
        for el in self.driver.find_elements_by_tag_name('script'):
            scripts.append(el.get_attribute('innerHTML'))
        
        for script in scripts:
            if 'require.config.params["args"]' in script:
                match_data_string = script
        
        match_data_string = match_data_string.split(' = ')[1] \
            .replace('matchId', '"matchId"') \
            .replace('matchCentreData', '"matchCentreData"') \
            .replace('matchCentreEventTypeJson', '"matchCentreEventTypeJson"') \
            .replace('formationIdNameMappings', '"formationIdNameMappings"') \
            .replace(';', '')
        match_data = json.loads(match_data_string)
        
        return match_data