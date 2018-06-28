import numpy as np
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
from time import time
from time import sleep
from random import randint
from IPython.core.display import clear_output



#seasons' range for fantasy stats
years_url = [str(i) for i in range(1970,2018)]

# to store scraped table data
header = []
players = []

start_time = time()

requests = 0

for year_url in years_url:
    
    
    # requests paced at 8-15 second intervals
    response = get('https://www.pro-football-reference.com/years/' + year_url + '/fantasy.htm')
    sleep(randint(8,15))
        
        
    # display request frequency
    requests += 1
    elapsed_time = time() - start_time
    print('Request:%d; Frequency: %f requests/s' %(requests, requests/elapsed_time))
    clear_output(wait = True)
    
    
    #Parse the content of the request with BeautifulSoup
    fntsy = BeautifulSoup(response.text, 'html.parser')
    
    
    #store rows values to players list of [year, season data]
    table =fntsy.find('table')
    tbody =fntsy.find('tbody')
    table_rows= tbody.find_all('tr')  
  
    for tr in table_rows:
        td = tr.find_all('td')
        player = [i.text for i in td]
        players.append([year_url,player])
        






#remove empty lists within players list    
for lsts in players:
    if len(lsts[1]) ==0:  
        players.remove(lsts)
     
        
    #remove extra characters from player names    
    elif len(lsts[1]) >0:
       lsts[1]= [i.replace("*", "",) for i in lsts[1]]
       lsts[1]=[i.replace("+", "",) for i in lsts[1]]
       


       
#Store header values to header list (year_url in response == 2017)
head = table.find('thead')
heads = head.find_all('tr') 
 
for head_row in heads:
    th = head_row.find_all('th')
    header = [i.text for i in th]

#Edit column names 
header.remove('Rk')
header[0] = 'Name'
header[8] = 'Pass Yards'
header[9] = 'Pass TDs'
header[12] = 'Rush Yards'
header[14] = 'Rush TDs'
header[17] = 'Rec Yards'
header[19] = 'Rec TDs'





#splits players list into two 
Years = []
fork = []
for items in players:
    Years.append(items[0])
    fork.append(list(items[1]))






#formats header and fork list into dataframe
FDframe = pd.DataFrame(fork, columns=header) 
FDframe['Year'] = Years
# Set multi index of (year, player name)
yr_nm_ind = pd.MultiIndex.from_arrays(np.array([FDframe['Year'].tolist(),
                                                FDframe['Name'].tolist()]), names=['Year', 'Name'])
FDframe.index = yr_nm_ind
#FDframe.sort_index(inplace=True)





#Scrape MVP table 
response2= get('https://www.pro-football-reference.com/awards/ap-nfl-mvp-award.htm')  
mvp_lister= BeautifulSoup(response2.text, 'html.parser')
mvp_table= mvp_lister.find('table')
mvp_rows= mvp_table.find_all('tr')                
mvp_head = mvp_table.find('thead')
mvp_heads = mvp_head.find_all('tr') 
MVPs= []
MVPyear= []


for tr_b in mvp_rows:
    td_b = tr_b.find_all('td')
    tr_b_h = tr_b.find_all('th')
    mvp = [i.text for i in td_b]
    MVPs.append(list(mvp))
    mvpyr = [i.text for i in tr_b_h]
    MVPyear.append(list(mvpyr))
    
for mvp_header in mvp_heads:
    th_b = mvp_header.find_all('th')
    year_list = [i.text for i in th_b] 
    



#extract mvp header values
MVPheader = list(MVPyear[0])
MVPyear = MVPyear[1:]
MVPs = MVPs[1:]
MVPheader = MVPheader[1:]
MVPyear = [int(j) for i in MVPyear for j in i]



#format MVP table data to pandas dataframe
MVPdf = pd.DataFrame(MVPs, columns=MVPheader)
MVPdf['Year'] = MVPyear


# Set multi index of (year, player name)
yr_nm_ind2 = pd.MultiIndex.from_arrays(np.array([MVPdf['Year'].tolist(),
                                                 MVPdf['Player'].tolist()]), names=['Year', 'Name'])
MVPdf.index = yr_nm_ind2
#MVPdf.sort_index(inplace=True)







##################################################

'''
The following adds 4 columns to FDframe:

Year - value corresponding to a respective season
MVP - boolean dependent on whether or not a player won MVP for a given year
Yards Leader - boolean dependent on whether or not a player was a yards leader for either of the three Yards columns
TD Leader -boolean dependent on whether or not a player was a touchdown leader for either of the three TD columnsr
'''


# New columns
FDframe['Year'] = Years
FDframe['MVP'] = pd.Series(np.repeat(0,len(FDframe)), index=FDframe.index)
FDframe['Yards Leader'] = pd.Series(np.repeat(0,len(FDframe)), index=FDframe.index)
FDframe['TD Leader'] = pd.Series(np.repeat(0,len(FDframe)), index=FDframe.index)


# turn string numeric data into float/ints
FDframe = FDframe.apply(pd.to_numeric, errors='ignore')


#checks if FDframe players appear on the MVPdf. If so, row value is set to True
for i in FDframe.index:
    if i in MVPdf.index:
        FDframe.loc[i,'MVP'] = 1



# set season subset range
for i in range(1970,2018):
    
    #store subsets each year
    frames = FDframe[FDframe['Year'] == i]
    
    #search players with the highest yard values for passing, rushng, receiving   
    y_leaders = frames.loc[frames[['Pass Yards', 'Rush Yards', 'Rec Yards']].idxmax()]
    
    #set corresponding player indices "Yards Leader' col to True
    FDframe.loc[y_leaders.index,'Yards Leader'] = 1
    
    
    
    #search players with the highest values for each yards column by season   
    td_leaders = frames.loc[frames[['Pass TDs', 'Rush TDs', 'Rec TDs']].idxmax()]
    
    #set 'Yards Leader'  to True if player was a yard leader for a given year
    FDframe.loc[td_leaders.index,'TD Leader'] = 1
  
    
    
    
FDframe.to_csv('FDframe.csv', index=False )
MVPdf.to_csv('MVPdf.csv', index=False)




