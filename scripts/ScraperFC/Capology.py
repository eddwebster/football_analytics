from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from IPython.display import clear_output

from ScraperFC.shared_functions import *

class Capology():

    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('window-size=700,600')
        # Use proxy
        # don't load images
        prefs = {'profile.managed_default_content_settings.images': 2}
        options.add_experimental_option('prefs', prefs)
        # create driver
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        clear_output()

        self.leagues = {
            'Bundesliga': 'de/1-bundesliga',
            '2.Bundesliga': '/de/2-bundesliga',
            'EPL': 'uk/premier-league',
            'EFL Championship': '/uk/championship',
            'Serie A': 'it/serie-a',
            'Serie B': 'it/serie-b',
            'La Liga': 'es/la-liga',
            'La Liga 2': 'es/la-liga-2',
            'Ligue 1': 'fr/ligue-1',
            'Ligue 2': 'fr/ligue-2',
            'Eredivisie': '/ne/eredivisie',
            'Primeira Liga': '/pt/primeira-liga',
            'Scottish PL': '/uk/scottish-premiership',
            'Super Lig': '/tr/super-lig',
            'Belgian 1st Division': 'be/first-division-a'
        }


    def close(self):
        self.driver.close()
        self.driver.quit()

    
    def scrape_salaries(self, year, league, currency):
        error, valid = check_season(year, league, 'Capology')
        if not valid:
            print(error)
            return -1
        elif currency not in ['eur', 'gbp', 'usd']:
            print('Currency must be one of "eur", "gbp", or "usd".')
            return -1

        
        league_url = 'https://www.capology.com/{}/salaries/{}-{}'.format(self.leagues[league], year-1, year)

        self.driver.get(league_url)

        # show all players on one page
        done = False
        while not done:
            try:
                all_btn = WebDriverWait(
                    self.driver, 
                    10,
                ).until(EC.element_to_be_clickable(
                    (By.LINK_TEXT, 'All')
                ))
                all_btn.click()
                done = True
            except StaleElementReferenceException:
                pass

        # select euros as currency
        euro_btn = WebDriverWait(
            self.driver, 
            10,
        ).until(EC.element_to_be_clickable(
            (By.ID, 'btn_{}'.format(currency))
        ))
        self.driver.execute_script('arguments[0].click()', euro_btn)

        # table to pandas df
        tbody_html = self.driver.find_element(By.ID, 'table')\
                .find_element(By.TAG_NAME, 'tbody')\
                .get_attribute('outerHTML')
        table_html = '<table>' + tbody_html + '</table>'
        df = pd.read_html(table_html)[0]
        if df.shape[1] == 13:
            df = df.drop(columns=[1])
            df.columns = [
                'Player', 'Weekly Gross', 'Annual Gross', 'Expiration', 'Length', 
                'Total Gross', 'Status', 'Pos. group', 'Pos.', 'Age', 'Country', 
                'Club'
            ]
        else:
            df.columns = [
                'Player', 'Weekly Gross', 'Annual Gross', 'Adj. Gross', 'Pos. group', 
                'Age', 'Country', 'Club'
            ]

        return df
