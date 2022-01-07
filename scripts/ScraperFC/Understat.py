import datetime
from IPython.display import clear_output
import json
import numpy as np
import pandas as pd
from ScraperFC.shared_functions import check_season
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager



class Understat:
    
    def __init__(self):
        options = Options()
        options.headless = True
        options.add_argument("window-size=1400,600")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        clear_output()
        
        
    def close(self):
        self.driver.close()
        self.driver.quit()
        
        
    def get_season_link(self, year, league):
        base_url = "https://understat.com/"
        lg = league.replace(" ","_")
        url = base_url+"league/"+lg+"/"+str(year-1)
        return url
        
        
    def get_match_links(self, year, league):
        if not check_season(year,league,'Understat'):
            return -1
        base_url = "https://understat.com/"
        lg = league.replace(" ","_")
        url = base_url+"league/"+lg+"/"+str(year-1)
        self.driver.get(url)
        btn = self.driver.find_element_by_class_name("calendar-prev")
        links = []
        for el in self.driver.find_elements_by_class_name("match-info"):
            links.append(el.get_attribute("href"))
        done = False
        while not done:
            btn.click()
            for el in self.driver.find_elements_by_class_name("match-info"):
                href = el.get_attribute("href")
                if href not in links:
                    links.append(href)
                else:
                    done = True
        return links
    
    
    def get_team_links(self, year, league):
        team_links = set()
        self.driver.get(self.get_season_link(year, league))
        for el in self.driver.find_elements_by_tag_name("a"):
            href = el.get_attribute("href")
            if href and "team" in href:
                team_links.add(href)
        return list(team_links)
    
    
    def remove_diff(self, string):
        string = string.split("-")[0]
        return float(string.split("+")[0])
        
        
    def scrape_matches(self, year, league, save=False):
        if not check_season(year,'EPL','Understat'):
            return -1
        
        season = str(year-1)+'-'+str(year)
        links = self.get_match_links(year, league)
        cols = ['Date','Match ID','Home Team','Away Team','Home Goals','Away Goals',
                'Home Ast','Away Ast','Understat Home xG','Understat Away xG',
                'Understat Home xA','Understat Away xA','Understat Home xPts','Understat Away xPts']
        matches = pd.DataFrame(columns=cols)
        
        for i,link in enumerate(links):
            print('Scraping match ' + str(i+1) + '/' + str(len(links)) + 
                  ' from Understat in the ' + season + ' ' + league + ' season.')
            match = self.scrape_match(link)
            matches = matches.append(match, ignore_index=True)
            clear_output()
        
        # save to CSV if requested by user
        if save:
            filename = season+"_"+league+"_Understat_matches.csv"
            matches.to_csv(path_or_buf=filename, index=False)
            print('Matches dataframe saved to ' + filename)
            return filename
        else:
            return matches
        
        
    def scrape_match(self, link):
        self.driver.get(link)
        elements = []
        for element in self.driver.find_elements_by_class_name('progress-value'):
            elements.append(element.get_attribute('innerHTML'))

        match = pd.Series()
        for element in self.driver.find_elements_by_class_name('breadcrumb'):
            date = element.find_elements_by_tag_name('li')[2]
            date = date.text
        date = datetime.datetime.strptime(date,'%b %d %Y').date()
        match['Date'] = date
        match['Match ID'] = link.split("/")[-1]
        match['Home Team'] = elements[0]
        match['Away Team'] = elements[1]
        
        for element in self.driver.find_elements_by_class_name('block-match-result'):
            score = element.get_attribute("innerHTML")
            score = score.split("</a>")[1]
            score = score.split("<a")[0].strip()
            score = score.split(" - ")
        assert len(score) == 2
        match['Home Goals'] = int(score[0])
        match['Away Goals'] = int(score[1])

        hxg = elements[7]
        axg = elements[8]

        ha = self.driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div[2]/table/tbody[2]/tr/td[8]')
        ha = int(ha[0].text)
        hxa = self.driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div[2]/table/tbody[2]/tr/td[10]')
        hxa = hxa[0].text.replace('+','-')
        # click button to away team stats
        button = self.driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div[1]/div/label[2]')
        button.click()
        aa = self.driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div[2]/table/tbody[2]/tr/td[8]')
        aa = int(aa[0].text)
        axa = self.driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div[2]/table/tbody[2]/tr/td[10]')
        axa = axa[0].text.replace('+','-')
        
        match['Home Ast'] = ha
        match['Away Ast'] = aa
        match['Understat Home xG'] = float(hxg.split('<')[0] + hxg.split('>')[1].split('<')[0])
        match['Understat Away xG'] = float(axg.split('<')[0] + axg.split('>')[1].split('<')[0])
        match['Understat Home xA'] = float(hxa.split('-')[0])
        match['Understat Away xA'] = float(axa.split('-')[0])

        string = elements[17]
        match['Home xPts'] = float(string.split('<')[0] + string.split('>')[1].split('<')[0])
        string = elements[18]
        match['Away xPts'] = float(string.split('<')[0] + string.split('>')[1].split('<')[0])
        
        return match
        
        
    def scrape_league_table(self, year, league, normalize=False):
        if not check_season(year,league,'Understat'):
            return -1
        
        url = self.get_season_link(year, league) # link to the selected league/season
        self.driver.get(url)
        
        # show all of the stats
        time.sleep(1)
        self.driver.find_elements_by_class_name("options-button")[0].click()
        time.sleep(1)
        # npxG
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]"+
            "/div/div[2]/div/div[2]/div[2]/div/div[11]/div[2]/label").click()
        time.sleep(1)
        # npxGA
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]"+
            "/div/div[2]/div/div[2]/div[2]/div/div[13]/div[2]/label").click()
        time.sleep(1)
        # npxGD
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]"+
            "/div/div[2]/div/div[2]/div[2]/div/div[14]/div[2]/label").click()
        time.sleep(1)
        # PPDA
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]"+
            "/div/div[2]/div/div[2]/div[2]/div/div[15]/div[2]/label").click()
        time.sleep(1)
        # OPPDA
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]"+
            "/div/div[2]/div/div[2]/div[2]/div/div[16]/div[2]/label").click()
        time.sleep(1)
        # DC
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]"+
            "/div/div[2]/div/div[2]/div[2]/div/div[17]/div[2]/label").click()
        time.sleep(1)
        # ODC
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]"+
            "/div/div[2]/div/div[2]/div[2]/div/div[18]/div[2]/label").click()
        time.sleep(1)

        self.driver.find_elements_by_class_name("button-apply")[0].click() # apply button
        time.sleep(1)

        # parse df out of HTML
        table = self.driver.find_elements_by_tag_name("table")[0].get_attribute("innerHTML")
        table = "<table>\n"+table+"</table>"
        df = pd.read_html(table)[0]
        
        # remove performance differential text from some columns
        for i in range(df.shape[0]):
            df.loc[i,"xG"] = self.remove_diff(df.loc[i,"xG"])
            df.loc[i,"xGA"] = self.remove_diff(df.loc[i,"xGA"])
            df.loc[i,"xPTS"] = self.remove_diff(df.loc[i,"xPTS"])
            
        if normalize:
            df.iloc[:,3:14] = df.iloc[:,3:14].divide(df["M"], axis="rows")
            df.iloc[:,16:] = df.iloc[:,16:].divide(df["M"], axis="rows")
        
        self.close()
        self.__init__()
        return df
    
    
    def scrape_home_away_tables(self, year, league, normalize=False):
        if not check_season(year,league,'Understat'):
            return -1
        
        url = self.get_season_link(year, league) # link to the selected league/season
        self.driver.get(url)

        # show all of the stats
        time.sleep(1)
        self.driver.find_elements_by_class_name("options-button")[0].click()
        time.sleep(1)
        # npxG
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]"+
            "/div/div[2]/div/div[2]/div[2]/div/div[11]/div[2]/label").click()
        time.sleep(1)
        # npxGA
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]"+
            "/div/div[2]/div/div[2]/div[2]/div/div[13]/div[2]/label").click()
        time.sleep(1)
        # npxGD
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]"+
            "/div/div[2]/div/div[2]/div[2]/div/div[14]/div[2]/label").click()
        time.sleep(1)
        # PPDA
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]"+
            "/div/div[2]/div/div[2]/div[2]/div/div[15]/div[2]/label").click()
        time.sleep(1)
        # OPPDA
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]"+
            "/div/div[2]/div/div[2]/div[2]/div/div[16]/div[2]/label").click()
        time.sleep(1)
        # DC
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]"+
            "/div/div[2]/div/div[2]/div[2]/div/div[17]/div[2]/label").click()
        time.sleep(1)
        # ODC
        self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]"+
            "/div/div[2]/div/div[2]/div[2]/div/div[18]/div[2]/label").click()
        time.sleep(1)

        self.driver.find_elements_by_class_name("button-apply")[0].click() # apply button
        time.sleep(1)
        
        # get home table
        labels = self.driver.find_elements_by_tag_name('label')
        [el for el in labels if el.text=='home'][0].click()
        table = self.driver.find_elements_by_tag_name('table')[0].get_attribute('outerHTML')
        home = pd.read_html(table)[0]
        
        
        # get away table
        [el for el in labels if el.text=='away'][0].click()
        table = self.driver.find_elements_by_tag_name('table')[0].get_attribute('outerHTML')
        away = pd.read_html(table)[0]
        
        # remove differentials from some columns
        for i in range(home.shape[0]):
            home.loc[i,"xG"] = self.remove_diff(home.loc[i,"xG"])
            home.loc[i,"xGA"] = self.remove_diff(home.loc[i,"xGA"])
            home.loc[i,"xPTS"] = self.remove_diff(home.loc[i,"xPTS"])
            away.loc[i,"xG"] = self.remove_diff(away.loc[i,"xG"])
            away.loc[i,"xGA"] = self.remove_diff(away.loc[i,"xGA"])
            away.loc[i,"xPTS"] = self.remove_diff(away.loc[i,"xPTS"])
        
        if normalize:
            home.iloc[:,3:14] = home.iloc[:,3:14].divide(home["M"], axis="rows")
            home.iloc[:,16:] = home.iloc[:,16:].divide(home["M"], axis="rows")
            away.iloc[:,3:14] = away.iloc[:,3:14].divide(away["M"], axis="rows")
            away.iloc[:,16:] = away.iloc[:,16:].divide(away["M"], axis="rows")
        
        self.close()
        self.__init__()
        return home, away
    
    
    def scrape_situations(self, year, league):
        if not check_season(year,league,'Understat'):
            return -1
        
        # Get links for teams in league that season
        team_links = self.get_team_links(year, league)
                
        mi = pd.MultiIndex.from_product(
            [
                ["Open play", "From corner", "Set piece", "Direct FK", "Penalty"],
                ["Sh", "G", "ShA", "GA", "xG", "xGA", "xGD", "xG/Sh", "xGA/Sh"]
            ]
        )
        mi = mi.insert(0, ("Team names", "Team"))
        situations = pd.DataFrame(columns=mi)
        
        for link in team_links:
            
            team_name = link.split("/")[-2]
            self.driver.get(link)
            table = self.driver.find_elements_by_tag_name("table")[0].get_attribute("outerHTML")
            df = pd.read_html(table)[0]
            
            for i in range(df.shape[0]):
                # remove performance differential text from some columns
                df.loc[i,"xG"] = self.remove_diff(df.loc[i,"xG"])
                df.loc[i,"xGA"] = self.remove_diff(df.loc[i,"xGA"])
            
            # reformat df to fit into a row
            df.drop(columns=["№","Situation"], inplace=True)
            row = df.to_numpy()
            row = np.insert(row, 0, team_name) # insert team name
            
            # append row
            situations = situations.append(
                pd.DataFrame(row.reshape(1,-1), columns=situations.columns),
                ignore_index=True
            )
        
        self.close()
        self.__init__()
        return situations
    
    
    def scrape_formations(self, year, league):
        if not check_season(year,league,'Understat'):
            return -1
        
        # Get links for teams in league that season
        team_links = self.get_team_links(year, league)
        
        formations = dict()
        
        for link in team_links:
            
            # Get team name to add to formations
            team_name = link.split("/")[-2]
            if team_name not in formations.keys():
                formations[team_name] = dict()
                
            # Got to team's link, click formations, and get table of formations used
            self.driver.get(link)
            self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div/div[1]/div/label[2]").click()
            table = self.driver.find_elements_by_tag_name("table")[0].get_attribute("outerHTML")
            df = pd.read_html(table)[0]
            df.drop(columns=["№"], inplace=True)
            
            # Remove performance differential text from some columns
            for i in range(df.shape[0]):
                df.loc[i,"xG"] = self.remove_diff(df.loc[i,"xG"])
                df.loc[i,"xGA"] = self.remove_diff(df.loc[i,"xGA"])
                
                formation = df.loc[i,"Formation"]
                
                if formation not in formations[team_name].keys():
                    formations[team_name][formation] = df.iloc[i,:].drop(columns=["№","Formation"])                
                
        self.close()
        self.__init__()
        return formations
    
    
    def scrape_game_states(self, year, league):
        if not check_season(year,league,'Understat'):
            return -1
        
        # Get links for teams in league that season
        team_links = self.get_team_links(year, league)
                
        mi = pd.MultiIndex.from_product(
            [
                ["Goal diff 0", "Goal diff -1", "Goal diff +1", "Goal diff < -1", "Goal diff > +1"],
                ["Min", "Sh", "G", "ShA", "GA", "xG", "xGA", "xGD", "xG90", "xGA90"]
            ]
        )
        mi = mi.insert(0, ("Team names", "Team"))
        game_states = pd.DataFrame(columns=mi)
        
        for link in team_links:
            
            team_name = link.split("/")[-2]
            self.driver.get(link)
            self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div/div[1]/div/label[3]").click()
            table = self.driver.find_elements_by_tag_name("table")[0].get_attribute("outerHTML")
            df = pd.read_html(table)[0]
            df.drop(columns=["№"], inplace=True)
            
            row = {
                "Goal diff 0": None,
                "Goal diff -1": None,
                "Goal diff +1": None,
                "Goal diff < -1": None,
                "Goal diff > +1": None
            }
            for i in range(df.shape[0]):
                # remove performance differential text from some columns
                df.loc[i,"xG"] = self.remove_diff(df.loc[i,"xG"])
                df.loc[i,"xGA"] = self.remove_diff(df.loc[i,"xGA"])
                
                game_state = df.loc[i,"Game state"]
                row[game_state] = df.loc[i,:].drop(labels=["Game state"])
                
            row_array = []
            for key in row.keys():
                row_array.append( row[key].to_numpy() )
            row_array = np.array(row_array)
            row_array = np.insert(row_array, 0, team_name) # insert team name
            
            # append row
            game_states = game_states.append(
                pd.DataFrame(row_array.reshape(1,-1), columns=game_states.columns),
                ignore_index=True
            )
            
        self.close()
        self.__init__()
        return game_states
    
    
    def scrape_timing(self, year, league):
        if not check_season(year,league,'Understat'):
            return -1
        
        # Get links for teams in league that season
        team_links = self.get_team_links(year, league)

        mi = pd.MultiIndex.from_product(
            [
                ["1-15", "16-30", "31-45", "46-60", "61-75", "76+"],
                ["Sh", "G", "ShA", "GA", "xG", "xGA", "xGD", "xG/Sh", "xGA/Sh"]
            ]
        )
        mi = mi.insert(0, ("Team names", "Team"))
        timing_df = pd.DataFrame(columns=mi)

        for link in team_links:
            
            team_name = link.split("/")[-2]
            self.driver.get(link)
            self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div/div[1]/div/label[4]").click()
            table = self.driver.find_elements_by_tag_name("table")[0].get_attribute("outerHTML")
            df = pd.read_html(table)[0]
            df.drop(columns=["№"], inplace=True)


            row = {
                "1-15": None,
                "16-30": None,
                "31-45": None,
                "46-60": None,
                "61-75": None,
                "76+": None
            }
            for i in range(df.shape[0]):
                # remove performance differential text from some columns
                df.loc[i,"xG"] = self.remove_diff(df.loc[i,"xG"])
                df.loc[i,"xGA"] = self.remove_diff(df.loc[i,"xGA"])

                timing = df.loc[i, "Timing"]
                row[timing] = df.loc[i,:].drop(labels=["Timing"])

            row_array = []
            for key in row.keys():
                row_array.append(row[key].to_numpy())
            row_array = np.array(row_array)
            row_array = np.insert(row_array, 0, team_name) # insert team name

            # append row
            timing_df = timing_df.append(
                pd.DataFrame(row_array.reshape(1,-1), columns=timing_df.columns),
                ignore_index=True
            )
            
        self.close()
        self.__init__()
        return timing_df
    
    
    def scrape_shot_zones(self, year, league):
        if not check_season(year,league,'Understat'):
            return -1
        
        # Get links for teams in league that season
        team_links = self.get_team_links(year, league)

        mi = pd.MultiIndex.from_product(
            [
                ["Own goals", "Out of box", "Penalty area", "Six-yard box"],
                ["Sh", "G", "ShA", "GA", "xG", "xGA", "xGD", "xG/Sh", "xGA/Sh"]
            ]
        )
        mi = mi.insert(0, ("Team names", "Team"))
        shot_zones_df = pd.DataFrame(columns=mi)

        for link in team_links:
            
            team_name = link.split("/")[-2]
            self.driver.get(link)
            self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div/div[1]/div/label[5]").click()
            table = self.driver.find_elements_by_tag_name("table")[0].get_attribute("outerHTML")
            df = pd.read_html(table)[0]
            df.drop(columns=["№"], inplace=True)


            row = {
                "Own goals": None,
                "Out of box": None,
                "Penalty area": None,
                "Six-yard box": None
            }
            for i in range(df.shape[0]):
                # remove performance differential text from some columns
                df.loc[i,"xG"] = self.remove_diff(df.loc[i,"xG"])
                df.loc[i,"xGA"] = self.remove_diff(df.loc[i,"xGA"])

                zone = df.loc[i, "Shot zones"]
                row[zone] = df.loc[i,:].drop(labels=["Shot zones"])

            row_array = []
            for key in row.keys():
                if row[key] is None:
                    row[key] = pd.Series(np.zeros((9)))
                row_array.append(row[key].to_numpy())
            row_array = np.array(row_array)
            row_array = np.insert(row_array, 0, team_name) # insert team name

            # append row
            shot_zones_df = shot_zones_df.append(
                pd.DataFrame(row_array.reshape(1,-1), columns=shot_zones_df.columns),
                ignore_index=True
            )
            
        self.close()
        self.__init__()
        return shot_zones_df
    
    
    def scrape_attack_speeds(self, year, league):
        if not check_season(year,league,'Understat'):
            return -1
        
        # Get links for teams in league that season
        team_links = self.get_team_links(year, league)

        mi = pd.MultiIndex.from_product(
            [
                ["Normal", "Standard", "Slow", "Fast"],
                ["Sh", "G", "ShA", "GA", "xG", "xGA", "xGD", "xG/Sh", "xGA/Sh"]
            ]
        )
        mi = mi.insert(0, ("Team names", "Team"))
        attack_speeds_df = pd.DataFrame(columns=mi)

        for link in team_links:
            
            team_name = link.split("/")[-2]
            self.driver.get(link)
            self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div/div[1]/div/label[6]").click()
            table = self.driver.find_elements_by_tag_name("table")[0].get_attribute("outerHTML")
            df = pd.read_html(table)[0]
            df.drop(columns=["№"], inplace=True)

            row = {
                "Normal": None,
                "Standard": None,
                "Slow": None,
                "Fast": None
            }
            for i in range(df.shape[0]):
                # remove performance differential text from some columns
                df.loc[i,"xG"] = self.remove_diff(df.loc[i,"xG"])
                df.loc[i,"xGA"] = self.remove_diff(df.loc[i,"xGA"])

                speed = df.loc[i, "Attack speed"]
                row[speed] = df.loc[i,:].drop(labels=["Attack speed"])

            row_array = []
            for key in row.keys():
                row_array.append(row[key].to_numpy())
            row_array = np.array(row_array)
            row_array = np.insert(row_array, 0, team_name) # insert team name

            # append row
            attack_speeds_df = attack_speeds_df.append(
                pd.DataFrame(row_array.reshape(1,-1), columns=attack_speeds_df.columns),
                ignore_index=True
            )
            
        self.close()
        self.__init__()
        return attack_speeds_df
    
    
    def scrape_shot_results(self, year, league):
        if not check_season(year,league,'Understat'):
            return -1
        
        # Get links for teams in league that season
        team_links = self.get_team_links(year, league)

        mi = pd.MultiIndex.from_product(
            [
                ["Missed shot", "Goal", "Saved shot", "Blocked shot", "Shot on post"],
                ["Sh", "G", "ShA", "GA", "xG", "xGA", "xGD", "xG/Sh", "xGA/Sh"]
            ]
        )
        mi = mi.insert(0, ("Team names", "Team"))
        shot_results_df = pd.DataFrame(columns=mi)

        for link in team_links:
            
            team_name = link.split("/")[-2]
            self.driver.get(link)
            self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div/div[1]/div/label[7]").click()
            table = self.driver.find_elements_by_tag_name("table")[0].get_attribute("outerHTML")
            df = pd.read_html(table)[0]
            df.drop(columns=["№"], inplace=True)

            row = {
                "Missed shot": None,
                "Goal": None,
                "Saved shot": None,
                "Blocked shot": None,
                "Shot on post": None
            }
            for i in range(df.shape[0]):
                # remove performance differential text from some columns
                df.loc[i,"xG"] = self.remove_diff(df.loc[i,"xG"])
                df.loc[i,"xGA"] = self.remove_diff(df.loc[i,"xGA"])

                result = df.loc[i, "Result"]
                row[result] = df.loc[i,:].drop(labels=["Result"])

            row_array = []
            for key in row.keys():
                row_array.append(row[key].to_numpy())
            row_array = np.array(row_array)
            row_array = np.insert(row_array, 0, team_name) # insert team name

            # append row
            shot_results_df = shot_results_df.append(
                pd.DataFrame(row_array.reshape(1,-1), columns=shot_results_df.columns),
                ignore_index=True
            )
            
        self.close()
        self.__init__()
        return shot_results_df
            

    def scrape_shot_xy(self, year, league, save=False):
        if not check_season(year,'EPL','Understat'):
            return -1
        
        season = str(year-1)+'-'+str(year)
        links = self.get_match_links(year, league)
        shots_data = dict()
        failures = list()

        i = 0
        for link in links:
            i += 1
            print(f"Scraping match {i}/{len(links)} in the {season} {league} season.")
            self.driver.get(link)
            match_id = link.split("/")[-1]
            try:
                game_shots_data = json.loads(\
                    self.driver.page_source\
                        .split("shotsData")[1]\
                        .split("JSON.parse(\'")[1]\
                        .split("\')")[0]\
                        .encode("latin-1")\
                        .decode("unicode-escape")
                )
                shots_data[match_id] = game_shots_data
            except:
                failures.append(match_id)
                shots_data[match_id] = "Error scraping"
            clear_output()
            
        self.close()
        self.__init__()

        # save to JSON file
        if save:
            filename = season+"_"+league+"_shot_xy.json"
            with open(filename, "w") as f:
                f.write(json.dumps(shots_data))
            print(f"Failed scraping matches {failures}.")
            print(f'Scraping saved to {filename}')
            return filename
        else:
            return shots_data
