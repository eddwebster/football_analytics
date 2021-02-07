# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 10:59:01 2020

@author: Fran
"""

"""============================================================================
===============================================================================

Script that contains all the necessary functions to translate Opta names of 
teams and players into Signality names

===============================================================================
============================================================================"""

def OptaToSignality(opta_name):
    try:
        dictionary = {
                      # Teams
                      'AFC Eskilstuna':'Athletic Eskilstuna',
                      'AIK':'AIK',
                      'BK Häcken':'BK Häcken',
                      'IFK Norrköping':'IFK Norrköping FK',
                      'Helsingborgs IF':'Helsingborgs IF',
                      'Hammarby IF':'Hammarby',
                      'IF Elfsborg':'IF Elfsborg',
                      'Örebro SK':'Örebro',
                      'Falkenbergs FF':'Falkenbergs FF',
                      'IK Sirius':'IK Sirius FK',
                      'Kalmar FF':'Kalmar FF',
                      'Malmö FF':'Malmö FF',
                      'GIF Sundsvall':'GIF Sundsvall',
                      'Djurgårdens IF':'Djurgården',
                      'Östersunds FK':'Östersund',
                      'IFK Göteborg':'IFK Göteborg',
                      'Varbergs BoIS':'Varbergs BoIS FC',
                      'Mjällby AIF':'Mjällby AIF',
                      'Hammarby Dam':'Hammarby women',
                      'Sandvikens IF':'Sandvikens IF',
                      'IF Brommapojkarna':'IF Brommapojkarna'
                      
                      
                      # Players
                      
                      }
        return dictionary[opta_name]
    except:
        inv_dictionary = {v: k for k, v in dictionary.items()}
    
        return inv_dictionary[opta_name]

def OptaToAcronym(opta_name):
    dictionary = {
                  # Teams
                  'AFC Eskilstuna':'AFC',
                  'AIK':'AIK',
                  'BK Häcken':'BKH',
                  'IFK Norrköping':'NOR',
                  'Helsingborgs IF':'HEL',
                  'Hammarby IF':'HAM',
                  'IF Elfsborg':'ELF',
                  'Örebro SK':'ÖRE',
                  'Falkenbergs FF':'FFF',
                  'IK Sirius':'SIR',
                  'Kalmar FF':'KFF',
                  'Malmö FF':'MFF',
                  'GIF Sundsvall':'GIF',
                  'Djurgårdens IF':'DIF',
                  'Östersunds FK':'ÖFK',
                  'IFK Göteborg':'GBG',  
                  'Mjällby AIF':'MJÄ',
                  'Varbergs BoIS':'VAR',
                  'Hammarby Dam':'HAM',
                  'Sandvikens IF':'SIF',
                  'IF Brommapojkarna':'BP'
                  }
    
    return dictionary[opta_name]

def OptaToColor(opta_name):
    dictionary = {
                  # Teams
                  'AFC Eskilstuna':'y',
                  'AIK':'black',
                  'BK Häcken':'y',
                  'IFK Norrköping':'blue',
                  'Helsingborgs IF':'red',
                  'Hammarby IF':'green',
                  'IF Elfsborg':'y',
                  'Örebro SK':'red',
                  'Falkenbergs FF':'y',
                  'IK Sirius':'navy',
                  'Kalmar FF':'red',
                  'Malmö FF':'dodgerblue',
                  'GIF Sundsvall':'y',
                  'Djurgårdens IF':'navy',
                  'Östersunds FK':'red',
                  'IFK Göteborg':'dodgerblue',  
                  'Mjällby AIF':'y',
                  'Varbergs BoIS':'darkgreen',
                  'Hammarby Dam':'green',
                  'Sandvikens IF':'red'
                  }
    
    return dictionary[opta_name]