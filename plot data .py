import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import parallel_coordinates

# Load Datasets nd sort by date
op = pd.read_csv('offensive_player_data.csv',low_memory=False)
op.sort_values(by='date', inplace=True)
op.index =op.date

op.plot()


# columns to plot
features = ['age','height', 'game_location', 'game_number', 'game_won', 'kick_return_attempts',
       'kick_return_touchdowns', 'kick_return_yards', 'opponent',
       'opponent_score', 'passing_attempts', 'passing_completions',
       'passing_interceptions', 'passing_rating', 'passing_sacks',
       'passing_sacks_yards_lost', 'passing_touchdowns', 'passing_yards',
       'player_id', 'player_team_score', 'punt_return_attempts', 'punt_return_touchdowns', 
       'punt_return_yards','receiving_receptions', 'receiving_targets', 'receiving_touchdowns',
       'receiving_yards', 'rushing_attempts', 'rushing_touchdowns',
       'rushing_yards', 'team', 'year','weight',
       'MVP_prev_year','position','prev_year_td_leader', 'prev_year_yards_leader']

pp = op[features]



# Subset by posistion
qb= pp.loc[pp['position'] == 'QB']
rb = pp.loc[pp['position']== 'RB']
wr = pp.loc[pp['position']== 'WR']


pph = pd.get_dummies(pp)


#Heat Maps tracking feature correllations for each position


qb_corr = (qb.loc[:, ['age','game_won', 'opponent_score','passing_attempts', 'passing_completions', 'opponent_score', 
                  'passing_interceptions', 'passing_rating', 'passing_sacks',
                  'passing_sacks_yards_lost', 'passing_touchdowns', 'passing_yards',
                  'weight','MVP_prev_year', 'prev_year_td_leader', 
                  'prev_year_yards_leader', 'height']]).corr()

fig, ax = plt.subplots(figsize=(17,17))
sns.heatmap(qb_corr, annot=True, linewidth=.5,
            ax=ax,cmap="BuPu")



rb_corr = (rb.loc[:, 
                  ['age', 'game_location', 'game_number', 'game_won','kick_return_attempts', 'kick_return_touchdowns',
                   'kick_return_yards', 'opponent','opponent_score','player_team_score', 'punt_return_attempts',
                   'punt_return_touchdowns', 'punt_return_yards','receiving_receptions', 'receiving_targets', 
                   'receiving_touchdowns', 'receiving_yards', 'rushing_attempts', 'rushing_touchdowns','rushing_yards',
                   'team', 'year','weight','MVP_prev_year','prev_year_td_leader', 
                   'prev_year_yards_leader']]
        
).corr()

fig, ax = plt.subplots(figsize=(17,17))
sns.heatmap(rb_corr, annot=True, linewidth=.5,
            ax=ax,cmap="YlGnBu")




wr_cprr = (wr.loc[:, 
                  ['age', 'game_location', 'game_number', 'game_won','prev_year_td_leader', 'prev_year_yards_leader'
                   'kick_return_attempts', 'kick_return_touchdowns', 'kick_return_yards', 'opponent',
                   'opponent_score','player_team_score', 'punt_return_attempts', 'punt_return_touchdowns',
                   'punt_return_yards','receiving_receptions', 'receiving_targets', 'receiving_touchdowns',
                   'receiving_yards', 'rushing_attempts', 'rushing_touchdowns','rushing_yards',
                   'team', 'year', 'weight','MVP_prev_year','prev_year_td_leader', 
                   'prev_year_yards_leader']]
        
).corr()

fig, ax = plt.subplots(figsize=(17,17))
sns.heatmap(rb_corr, annot=True, linewidth=.5,
            ax=ax,cmap="Greens")




kick_returns = (
    pp.loc[pp['position'].isin(['RB', 'WR'])]
    .loc[:, ['kick_return_attempts', 'kick_return_touchdowns', 'kick_return_yards',
             'punt_return_attempts', 'punt_return_touchdowns', 'punt_return_yards']]
    )


kick_returns['position'] = pp['position']
kick_returns = kick_returns.sample(200)

fig = plt.figure(figsize=(12,8))
fig, ax = plt.subplots(2,2)

parallel_coordinates(kick_returns, 'position', ax=ax)



