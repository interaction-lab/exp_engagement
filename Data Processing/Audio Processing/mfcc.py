import os
import pandas as pd

def process_mfcc(directory):
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as f:
            dicty = {}    
            c0 = 0
            c1 = 0
            frame = 1
            for line in f:
                if('c0' in line):
                    c0 = round(float(line.split(' = ')[-1]),3)
                    continue
                if('c [1]' in line):
                    c1 = round(float(line.split(' = ')[-1]),3)
                    dicty[frame] = (c0,c1)
                    frame+=1        
                    continue
            df = pd.DataFrame.from_dict(dicty, orient='index', columns=['mfcc_0', 'mfcc_1'])
            df.to_csv(directory+'/'+filename.split('.MFCC')[0]+'_MFCC.csv', index = False)

if __name__ == '__main__':
    directory = ['P5','P7','P8','P9']
    for dirc in directory:
        print dirc
        process_mfcc(dirc)