import os
import pandas as pd

def process_pitch(directory):
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as f:
            dicty = {}    
            flag = 0
            freq = 0
            strength = 0
            frame = 1
            nc = 0
            for line in f:
                if('nCandidates' in line):
                    nc = int(line.split(' = ')[-1])
                    continue
                if(nc == 1):
                    if('candidate [1]' in line):
                        flag = 1    
                        continue
                    if(flag == 1):
                        freq = round(float(line.split(' = ')[-1]),3)
                        flag = 2
                        continue
                    if(flag == 2):
                        strength = round(float(line.split(' = ')[-1]),3)
                        flag = 0
                        dicty[frame] = (freq,strength)
                        frame+=1
                else:
                    if('candidate [2]' in line):
                        flag = 1    
                        continue
                    if(flag == 1):
                        freq = round(float(line.split(' = ')[-1]),3)
                        flag = 2
                        continue
                    if(flag == 2):
                        strength = round(float(line.split(' = ')[-1]),3)
                        flag = 0
                        dicty[frame] = (freq,strength)
                        frame+=1
            df = pd.DataFrame.from_dict(dicty, orient='index', columns=['pitch_frequency', 'pitch_strength'])
            df.to_csv(directory+'/'+filename.split('.Pitch')[0]+'_Pitch.csv', index = False)

if __name__ == '__main__':
    directory = ['P5','P7','P8','P9']
    for dirc in directory:
        print dirc
        process_pitch(dirc)
