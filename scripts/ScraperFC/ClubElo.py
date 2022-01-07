from   datetime import datetime
from   io import StringIO
from   IPython.display import clear_output
import pandas as pd
import requests

class ClubElo:        
        
    def scrape_team_on_date(self, team, date):
        """
        Date must be passed in YYYY-MM-DD format as a string
        """
        date = datetime.strptime(date, '%Y-%m-%d')
        
        # use ClubElo API to get team data as Pandas DataFrame
        url = 'http://api.clubelo.com/{}'.format(team)
        r = requests.get(url)
        df = pd.read_csv(StringIO(r.text), sep=',')
        
        # find row that given date falls in
        for i in df.index:
            from_date = datetime.strptime(df.loc[i,'From'], '%Y-%m-%d')
            to_date = datetime.strptime(df.loc[i,'To'], '%Y-%m-%d')
            if (date>from_date and date<to_date) or date==from_date or date==to_date:
                return df.loc[i,'Elo']
        
        return -1 # return -1 if ELO not found for given date
        
