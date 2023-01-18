import pandas as pd
import os 
import glob

os.chdir('/Users/furkankarakaya/Desktop/billnius copy/charts')
print("Current working directory: {0}".format(os.getcwd()))

chartsYears = [str(i) for i in range(2020, 2023, 1)]

for currentYear in chartsYears:    
    csv_files = glob.glob('charts_' + currentYear + '_*.{}'.format('txt'))
    print('cvsFiles belong to ' + currentYear + ':', csv_files)

    df = pd.concat([pd.read_csv(f, sep=';', encoding='cp1252') for f in csv_files ], ignore_index=True)
    df['songs'] = df['artist'] + df['title']
    df.drop_duplicates(subset= 'songs', keep= 'first', inplace= True)
    df2 = (df.loc[:, ['artist', 'title']])
    print(df2)
    df2.to_csv('/Users/furkankarakaya/Desktop/billnius copy/combinedCharts/charts_' + currentYear + '_combined.txt')




