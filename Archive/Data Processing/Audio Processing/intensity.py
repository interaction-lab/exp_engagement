import os
import pandas as pd

def process_intensity(directory):
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as f:
            data = pd.read_fwf(f, sep=" ", header=None)
            data.columns = ["intensity"]
            data = data.round(3)
            data.to_csv(directory+'/'+filename.split('.Intensity')[0]+'_Intensity.csv',index = False)
            
            
if __name__ == '__main__':
    directory = ['P5','P7','P8','P9']
    for dirc in directory:
        print dirc
        process_intensity(dirc)