import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Imputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score

op = pd.read_csv('offensive_player_data.csv')
op.index =[op.date, op.player_id]

op['draft_round'] = op.draft_round.fillna('Null')
op['draft_position'] = op.draft_position.fillna('Null')

predictors = ['age','height', 'game_location', 'game_number', 'game_won', 'kick_return_attempts',
       'kick_return_touchdowns', 'kick_return_yards', 'opponent',
       'opponent_score', 'passing_attempts', 'passing_completions',
       'passing_interceptions', 'passing_rating', 'passing_sacks',
       'passing_sacks_yards_lost', 'passing_touchdowns', 'passing_yards',
       'player_team_score', 'punt_return_attempts', 'punt_return_touchdowns', 
       'punt_return_yards','receiving_receptions', 'receiving_targets', 'receiving_touchdowns',
       'receiving_yards', 'rushing_attempts', 'rushing_touchdowns',
       'rushing_yards', 'team', 'year', 'weight',]

targets = ['prev_year_td_leader', 'MVP_prev_year', 'prev_year_yards_leader']


x = op[predictors]
y = op[targets]
y= np.ravel(y)
x_hot=pd.get_dummies(x)
x_hot, y = make_classification(n_samples=1000, n_features=112,
                                                       n_informative=3, n_redundant=0,
                                                       random_state=0, shuffle=False, n_classes=3)



clf = make_pipeline(Imputer(), RandomForestClassifier(max_depth=2, random_state=0))
scores = cross_val_score(clf, x_hot, y, scoring='neg_mean_absolute_error')
print("Cross-val accuracy: %f" %scores.mean())
print(scores)
print('Mean Absolute Error %2f' %(-1 * scores.mean()))







