import pandas as pd
import numpy as np
import datetime
from time import time

start = time()
date = (datetime.datetime.now() + datetime.timedelta(microseconds = start/10)).strftime("%H:%M%p")
print("Running program:\nCurrent Time = "+ str(date))



#Load datasets
profiles = pd.read_json('profiles.json')
games = pd.read_json('games.json')
seasons = pd.read_csv('FDframe.csv')


#subset of seasons fromm 1970 to 2017 
games1970plus = pd.DataFrame(games[games['year'] >=1970])
del games

#check nan totals

# clean data
seasons.FantPos.fillna(value="Unknown", inplace =True)        
#remove white space from profiles and seasons
profiles.name = [i.strip() for i in profiles.name]
profiles.position = [i.strip() for i in profiles.position]
seasons.Name = [i.strip() for i in seasons.Name]
seasons.FantPos = [i.strip() for i in seasons.FantPos]


#change row value for Ty's position from WR/RB to RB
profiles.loc[profiles[profiles["name"] == 'Ty Montgomery'].index,'position'] = 'RB'



#sort values for row-wise concatentation 
games1970plus.sort_values(by='player_id', inplace=True)
profiles.sort_values(by='player_id', inplace=True)

games1970plus.index = games1970plus.player_id
profiles.index = profiles.player_id

#combine dfs
play_prof = pd.concat([games1970plus, profiles], axis = 1, join_axes=[games1970plus.index])



#define func that changes height from ft-in format to inches
def convert_ht(ht):

    h_ = str(ht).split("-")
    ft_ = float(h_[0])
    in_ = float(h_[1])
        
    return (12*ft_) + in_

#fill nans 
play_prof['height'] = play_prof.height.fillna('6-0')

#apply convert_height()
play_prof['height'] = [convert_ht(i) for i in play_prof.height]

# define func that changes age to year + days/year 
def convert_age(age):
    age_ = str(age).split("-")
    
    if len(age_) == 2:
        yr_ = float(age_[0])
        dy_ = float(age_[1])
        return yr_ + (dy_)/365


#apply convert_age()
play_prof['age'] = [convert_age(i) for i in play_prof.age]



#create column MVP_prev_year
play_prof['MVP_prev_year'] = np.repeat(0,len(play_prof))


#change col values to string type
play_prof['year'] = [str(i) for i in play_prof['year']]


#sort by descending year
play_prof.sort_values(by='year', ascending=False, inplace=True)
play_prof.index=[play_prof.name, play_prof.year]


mvpdf=pd.read_csv('MVPdf.csv')
mvpdf.index = [mvpdf.Player, mvpdf.Year] 
#MultiIndexes of MVP winner's followinig year

mvps=[(i[0], str(int(i[1]) + 1)) for i in mvpdf.index[1:50]]



#sets col value to True if player won MVP in the previous season. 
#Doesn't apply to players that retired the following season
for possible_mvp in play_prof.index:
   if possible_mvp in mvps:
       play_prof.loc[possible_mvp ,'MVP_prev_year'] = 1


#create columns noting previous season's Yards and TD leader
play_prof['prev_year_yards_leader'] = np.repeat(0,len(play_prof))
play_prof['prev_year_td_leader'] = np.repeat(0,len(play_prof))


#sort by year
seasons.sort_values(by='Year', inplace=True, ascending=False)
seasons.index=[seasons.Name, seasons.Year ]


#remove 2017 since there is no 2018 data yet
seasonsb = seasons[seasons['Year'] < 2017]


#subset of yards leaders
yards= seasonsb[seasonsb['Yards Leader'] == True]


#subset of yards leaders
td=seasonsb[seasonsb['TD Leader'] == True]

#stores indexes of players who led the league in TDs or yards the previous year
yrd_lead=[(i[0], str(int(i[1]) + 1)) for i in yards.index[1:]]
td_lead=[(i[0], str(int(i[1]) + 1)) for i in td.index[1:]]


#sets col values to True if a player was a yards leader/TD leader the previous year
for yleader in yrd_lead:
   if yleader in play_prof.index:
      play_prof.loc[yleader ,'prev_year_yards_leader'] = 1

for tleader in td_lead:
   if tleader in play_prof.index:
      play_prof.loc[tleader ,'prev_year_td_leader'] = 1



#save to csv
play_prof.to_csv('all_player_data.csv', index=False)


#subset offensive players
offensive =play_prof.loc[play_prof['position'].isin(['QB','RB','WR','TE']),:]


#save to csv
offensive.to_csv('offensive_player_data.csv',index=False)



total_elapsed = (time() - start)
date = (datetime.datetime.now() + datetime.timedelta(microseconds = start/10)).strftime("%H:%M%p")
print("\n\n\nTotal Time Elapsed: " + str(total_elapsed/60) +"[m]\nCurrent Time: " + str(date))