import os
import pandas as pd

p9_ref = {
'webcam_2018-06-07-14-01-26.mp4' : 's1' ,			
'webcam_2018-06-12-13-24-50.mp4' : 's3-1',			
'webcam_2018-06-12-18-24-01.mp4' : 's3-2',			
'webcam_2018-06-14-08-18-18.mp4' : 's4',			
'webcam_2018-06-26-15-27-45.mp4' : 's9',			
'webcam_2018-07-05-09-01-49.mp4' : 's13-3',			
'webcam_2018-07-07-07-37-52.mp4' : 's15',			
'webcam_2018-07-08-16-54-10.mp4' : 's16'		   
}

uniq = set()
op_dir = 'p9_audio'

def process(directory):
    for filename in os.listdir(directory):
        val = filename.split('_mp4')[0] #+ '.mp4'
        uniq.add(val)
    
    for item in uniq:
        df_h = pd.read_csv(directory+'/'+item+'_mp4_Harmonicity.csv')
        df_i = pd.read_csv(directory+'/'+item+'_mp4_Intensity.csv')
        df_m = pd.read_csv(directory+'/'+item+'_mp4_MFCC.csv')
        df_p = pd.read_csv(directory+'/'+item+'_mp4_Pitch.csv')
        
        df = pd.concat([df_h,df_i,df_m,df_p], axis=1)
        var = p9_ref[item+'.mp4']
        df.to_csv(op_dir+'/'+'p9_'+var+'_audio_feats.csv', index = False)
    
    #print len(uniq)
if __name__ == '__main__':
    directory = ['p9_feat']
    for dirc in directory:
        #print dirc
        process(dirc)