import pandas as pd
import numpy as np

p_path = 'p8'
print(p_path)
file = p_path+'_master.csv'
data = pd.read_csv(file)

# Sort and Reset Index
data = data.sort_values(['session_num', 'timestamp'], ascending=[True, True])
data = data.reset_index(drop=True)

of_cols = ['of_gaze_0_x', 'of_gaze_0_y', 'of_gaze_0_z', 'of_gaze_1_x',
'of_gaze_1_y', 'of_gaze_1_z', 'of_gaze_angle_x', 'of_gaze_angle_y',
'of_gaze_distance', 'of_pose_Tx', 'of_pose_Ty', 'of_pose_Tz',
'of_pose_Rx', 'of_pose_Ry', 'of_pose_Rz', 'of_pose_distance',
'of_AU01_c', 'of_AU02_c', 'of_AU04_c', 'of_AU05_c', 'of_AU06_c',
'of_AU07_c', 'of_AU09_c', 'of_AU10_c', 'of_AU12_c', 'of_AU14_c',
'of_AU15_c', 'of_AU17_c', 'of_AU20_c', 'of_AU23_c', 'of_AU25_c',
'of_AU26_c', 'of_AU28_c', 'of_AU45_c']

of_smoothable = ['of_pose_Tx', 'of_pose_Ty', 'of_pose_Tz',
'of_pose_Rx', 'of_pose_Ry', 'of_pose_Rz', 'of_pose_distance',
'of_AU01_c', 'of_AU02_c', 'of_AU04_c', 'of_AU05_c', 'of_AU06_c',
'of_AU07_c', 'of_AU09_c', 'of_AU10_c', 'of_AU12_c', 'of_AU14_c',
'of_AU15_c', 'of_AU17_c', 'of_AU20_c', 'of_AU23_c', 'of_AU25_c',
'of_AU26_c', 'of_AU28_c', 'of_AU45_c']

of_not_smoothable = ['of_gaze_0_x', 'of_gaze_0_y', 'of_gaze_0_z', 'of_gaze_1_x',
'of_gaze_1_y', 'of_gaze_1_z', 'of_gaze_angle_x', 'of_gaze_angle_y',
'of_gaze_distance']


last_session = -1
last_success = -1

data['of_ts_success'] = 0

checkpoint = int(len(data)/20)

for i,r in data.iterrows():
    if i%checkpoint==0:
        print(i)
    # Check if new session started
    if last_session != r['session_num']:
        last_session = r['session_num']
        last_success = -1
    # 1 -- of success at this row, do nothing
    if r['of_success']==1:
        last_success = i
    # 2 -- no success this session -- everything np.nan
    elif (last_session == -1):
        data.loc[i, 'of_ts_success'] = -1
        for f in of_cols:
            data.loc[i, f] = np.nan   
    # 3 -- of success this session, last success <= 0.5 seconds 
    elif (last_success != -1) and (i-last_success <= 15):
        data.loc[i, 'of_ts_success'] = (i-last_success)*(0.1/3)
        # smoothable features: use last success
        for f in of_smoothable:
            data.loc[i, f] = data.loc[last_success, f]
        # non-smoothable => NaN 
        for f in of_not_smoothable:
            data.loc[i, f] = np.nan
    # 4 -- of success this session, last success > 0.5 seconds
    else:
        data.loc[i, 'of_ts_success'] = (i-last_success)*(0.1/3)
        for f in of_cols:
            data.loc[i, f] = np.nan    


data.to_csv(p_path+'_master_smooth.csv', index=False)

