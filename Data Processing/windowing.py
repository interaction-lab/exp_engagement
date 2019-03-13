import pandas as pd
import numpy as np


p_path = 'p5'
file = p_path+'_master_smooth.csv'
data = pd.read_csv(file)

data = data.sort_values(['session_num', 'timestamp'], ascending=[True, True])

curr = 0
window_size = 29 
increment = 15

# Create Feature Dictionary for Each Window
checkpoint = 0
check_increment = 10000
print('Total', len(data))

to_add = []
while (curr+window_size < len(data)):
  if curr>=checkpoint:
    print(curr)
    checkpoint += check_increment

  # adjust window start if this window contains a session_change, ignore end of sessions 
  while data.loc[curr+window_size, 'session_num'] != data.loc[curr, 'session_num']:
    curr += 1
  
  window = data.loc[curr:curr+window_size]    
  append = {}
  for i in data.columns:
    if (window[i].isna().sum()) >= ((window_size+1)/2):
      append[i] = np.nan
      append[i+'_var'] = np.nan
    else:
      append[i] = np.nanmedian(window[i])
      append[i+'_var'] = np.nanvar(window[i])
  to_add.append(append)

  curr += increment

# Create DataFrame with Windows
cols = []
for i in data.columns:
  cols.append(i)
  cols.append(i+'_var')

answer = pd.DataFrame(columns=cols)
answer = answer.append(to_add, ignore_index=True, sort=True)

# Adjust, round some features
answer['timestamp'] = round(answer['timestamp'], 1)

# round_down features: features that are integers, if the median is not an integer round down
int_features = ['engagement', 'of_AU01_c', 'of_AU02_c', 'of_AU04_c', 'of_AU05_c',
       'of_AU06_c', 'of_AU07_c', 'of_AU09_c', 'of_AU10_c', 'of_AU12_c',
       'of_AU14_c', 'of_AU15_c', 'of_AU17_c', 'of_AU20_c', 'of_AU23_c',
       'of_AU25_c', 'of_AU26_c', 'of_AU28_c', 'of_AU45_c', 'of_success', 'op_num_people', 'p_diff_1', 'p_diff_2',
       'p_diff_3', 'p_diff_4', 'p_diff_5', 'p_games_session', 'p_games_total', 'p_mistakes_game', 'p_mistakes_session', 'p_mistakes_total',
       'p_no_game', 'p_skill_EM', 'p_skill_NC', 'p_skill_OS']

for i in int_features:
    answer[i] = np.floor(answer[i])

answer.to_csv(p_path+'_master_window.csv', index=False)
