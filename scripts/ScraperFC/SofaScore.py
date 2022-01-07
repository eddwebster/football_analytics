from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from ScraperFC.shared_functions import *
from IPython.display import clear_output
import time

class SofaScore:

    def __init__(self):
        options = Options()
        # options.headless = True
        options.add_argument("window-size=1400,600")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        clear_output()


    def close(self):
        self.driver.close()
        self.driver.quit()


    def scrape_team_stats(self, year, league, normalize=True):
        error, valid = check_season(year, league, "SofaScore")
        if not valid:
            print(error)
            return -1
        
        url = "https://www.sofascore.com/tournament/football/usa/usl-league-one/13362"
        self.driver.get(url)

        # Click button for right season
        for el in self.driver.find_elements_by_tag_name("li"):
            if str(year) in el.get_attribute("outerHTML"):
                button = el
                break
        self.driver.execute_script("arguments[0].click()",button)
        time.sleep(3)

        # Get links to the teams in the tables
        team_links = list()
        for el in self.driver.find_elements_by_tag_name("a"):
            href = el.get_attribute("href")
            if href and ("team" in href):
                team_links.append(href)

        # Scrape stats for each team
        for team_link in team_links[:1]:
            self.driver.get(team_link) # Go to team's page

            # Click to season stats for the chosen season
            buttons = list()
            for el in self.driver.find_elements_by_tag_name("li"):
                time.sleep(0.1)
                if str(year) in el.get_attribute("outerHTML"):
                    buttons.append(el)
            self.driver.execute_script("arguments[0].click()",buttons[1])

            matches = None
            team_stats = {
                "Team name": team_link.split("/")[-2].replace("-"," "),
                "Avg. rating": self.driver.find_element_by_xpath("/html/body/div[1]/main/div/div[2]/div[1]/div[2]/div/div[4]/div/div[2]/div[2]").text,
                "Matches": matches,
                "GF": None,
                "GA": None,
                "A": None,
                "Goal conversion": None,
                "PK goals": None,
                "FK goals": None,
                "Goals from inside the box": None,
                "Goals from outside the box": None,
                "Left foot goals": None,
                "Right foot goals": None,
                "Headed goals": None,
                "Big chances": round(None*matches),
                "Big chances missed": round(None*matches),
                "Shots": round(None*matches),
                "Shots on target": round(None*matches),
                "Shots off target": round(None*matches),
                "Succ. dribbles": round(None*matches),
                "Corners": round(None*matches),
                "Hit woodwork": None,
                "Counter attacks": None,
                "Avg. possession": None,
                "Acc. passes": round(None*matches),
                "Pass acc.": None,
                "Comp. passes own half": None,
                "Pass acc. own half": None,
                "Comp. passes opp. half": None,
                "Pass acc. opp. half": None,
                "Comp. long balls": None,
                "Long ball acc.": None,
                "Comp. crosses": None,
                "Cross acc.": None,
                "CS": None,
                "Tackles": round(None*matches),
                "Interceptions": round(None*matches),
                "Clearances": round(None*matches),
                "Saves": round(None*matches),
                "Err. leading to shot": None,
                "Err leading to goal": None,
                "PK conceded": None,
                "PK goals conceded": None,
                "Clearances off line": None,
                "Last man tackles": None,
                "Duels won": round(None*matches),
                "Duels win %": None,
                "Ground duels won": round(None*matches),
                "Ground duels win %": None,
                "Aerial duels won": round(None*matches),
                "Aerial duels win %": None,
                "Poss. lost": round(None*matches),
                "Offsides": round(None*matches),
                "Fouls": round(None*matches),
                "YC": round(None*matches),
                "RC": None,
                "Squad size": None
            }

        if normalize:
            pass

        return 999

