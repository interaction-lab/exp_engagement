import os
import pandas as pd

def process_harmonicity(directory):
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as f:
            data = pd.read_fwf(f, sep=" ", header=None)
            data.columns = ["harmonicity"]
            data = data.round(3)
            data.to_csv(directory+'/'+filename.split('.Harmonicity')[0]+'_Harmonicity.csv',index = False)
            
            
if __name__ == '__main__':
    directory = ['P5','P7','P8','P9']
    for dirc in directory:
        print dirc
        process_harmonicity(dirc)