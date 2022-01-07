from ScraperFC.FBRef import FBRef
from ScraperFC.Understat import Understat
from ScraperFC.FiveThirtyEight import FiveThirtyEight
from IPython.display import clear_output
import pandas as pd
from ScraperFC.shared_functions import check_season


class ScraperFC:
    
    def __init__(self):
        self.fbref = FBRef()
        self.understat = Understat()
        self.fte = FiveThirtyEight()
        
        
    def close(self):
        self.fbref.close()
        self.understat.close()
        self.fte.close()
        
    
    def scrape_matches(self, year, league, save=False):
        if not check_season(year,league,'All'):
            return -1
        
#         print('Preparing to gather match data from Understat and FBRef.')
        season = str(year-1)+'-'+str(year)
#         num_matches = 380
#         # get FBREF links
#         fbref_links = self.fbref.get_match_links(year,league)
#         assert len(fbref_links) == num_matches
#         # get Understat links
#         understat_links = self.understat.get_match_links(year, league)
#         assert len(understat_links) == num_matches
#         clear_output()
        
#         fbref_cols = ['Date','Home Team','Away Team','Home Goals','Away Goals',
#                       'Home Ast','Away Ast','FBRef Home xG','FBRef Away xG','Home npxG',
#                       'Away npxG','FBRef Home xA','FBRef Away xA','Home psxG','Away psxG']
#         fbref_df = pd.DataFrame(columns=fbref_cols)
#         understat_cols = ['Date','Home Team','Away Team','Home Goals','Away Goals',
#                           'Home Ast','Away Ast','Understat Home xG','Understat Away xG',
#                           'Understat Home xA','Understat Away xA','Home xPts','Away xPts']
#         understat_df = pd.DataFrame(columns=understat_cols)

        print('Scraping match data from FiveThirtyEight for the '+season+" "+league+' season.')
        fte_df = self.fte.scrape_matches(year, league)
        clear_output()
        
        print('Scraping match data from FBRef for the '+season+" "+league+' season.')
        fbref_df = self.fbref.scrape_matches(year, league)
        clear_output()
        
        print('Scraping match data from Understat for the '+season+" "+league+' season.')
        understat_df = self.understat.scrape_matches(year,league)
        clear_output()
        
#         for i in range(num_matches):
#             print('Scraping match ' + str(i+1) + '/' + str(num_matches) + ' in the ' + season + ' EPL season.')
            
#             fbref_link = fbref_links[i]
#             understat_link = understat_links[i]
            
#             fbref_match = self.fbref.scrape_match(fbref_link,'EPL')
#             understat_match = self.understat.scrape_match(understat_link)
            
#             fbref_df = fbref_df.append(fbref_match, ignore_index=True)
#             understat_df = understat_df.append(understat_match, ignore_index=True)
            
#             clear_output()

        # merge dataframes
        df = fbref_df.merge(understat_df, how='outer',
                            left_index=True, right_index=True,
                            on=['Date','Home Team','Away Team',
                                'Home Goals','Away Goals',
                                'Home Ast','Away Ast'])
        df = df.merge(fte_df, how='outer',
                      left_index=True, right_index=True,
                      on=['Date','Home Team','Away Team'])
        
        # save to CSV if requested by user
        if save:
            filename = season+"_"+league+"_matches.csv"
            df.to_csv(path_or_buf=filename, index=False)
            print('Matches dataframe saved to ' + filename)
            return filename
        else:
            return df
        
            