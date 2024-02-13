#CSV utilities and parsing
import pandas as pd
import numpy as np
import traceback

BASE_METRICS = ['timestamp', 'EA', 'EL',
           'PI', 'PR', 'PG',
           'AX', 'AY', 'AZ',
           'GX', 'GY', 'GZ',
           'MX', 'MY', 'MZ',
           'SA', 'SR', 'SF',
           'T1', 'HR', 'BI']

IGNORED_METRICS = ['EM', 'B%', 'BV',
                   'RB', 'TL', 'AK',
                   'RS', 'RB', 'RD',
                   'DC']

def init_row():
    return {metric: np.nan for metric in BASE_METRICS}

def vectorize(source, 
              dest, 
              name,
              derive=True,   
              label='',
              note_labels=False,
              test_split=0.15, 
              cliphead=0, 
              cliptail=0,
              use_index=False,
              use_header=True):

    try:
        if note_labels:
            BASE_METRICS.append('UN')
        else:
            IGNORED_METRICS.append('UN') 

        raw = pd.read_csv(source, header=None, on_bad_lines='skip', skiprows=1, usecols=[3, 6, 7], index_col=False)
        raw = raw[~raw[3].str.contains('|'.join(IGNORED_METRICS))]

        if note_labels:
            labels = raw.loc[raw[3]=='UN', 7].tolist()
        
        list = []
        vec_row = init_row()

        for raw_row in raw.itertuples(index=True):
            if vec_row[raw_row[1]] is not np.nan:
                vec_row['timestamp'] = int(raw_row[0])
                list.append(vec_row)
                vec_row = init_row()
            if raw_row[1] == 'UN':
                vec_row[raw_row[1]] = raw_row[3]
            else:
                vec_row[raw_row[1]] = float(raw_row[2])

        vec = pd.DataFrame.from_dict(data=list)

        #Filling up 'holes' in data
        base_metrics = BASE_METRICS[:-1] if note_labels else BASE_METRICS
        for metric in base_metrics:
            indices = vec[vec[metric].notnull()].index
            for start, end in zip(indices,indices[1:]):
                if end-start > 1:
                    startval = float(vec.at[start, metric])
                    endval = float(vec.at[end, metric])
                    interpolated = np.linspace(start=startval, stop=endval, num=end-start+2)
                    vec.loc[start+1:end, metric] = interpolated[1:-1]
        
        labels = []
        dfs = []
        if note_labels:
            indices = vec[vec['UN'].notnull()].index.tolist()
            for i in indices:
                labels.append(vec.at[i, 'UN'])
            print(indices, labels)
            vec = vec.drop('UN', axis=1)

            for start, end in zip(indices,indices[1:]):
                dfs.append(vec[start:end-1])
            dfs.append(vec[end:])
        
        else:
            labels.append(label)
            dfs.append(vec)
        
        for vec, lab in zip(dfs, labels):

            vec.dropna(how='any', inplace=True)

            #Clipping Dataframe
            vec.drop(vec.head(cliphead).index, inplace=True)
            vec.drop(vec.tail(cliptail).index, inplace=True) 

            #Split into test and train
            test_vec = vec.sample(frac=test_split)
            train_vec = vec.drop(test_vec.index)

            #Adjust timestamps
            train_vec['timestamp'] -= train_vec['timestamp'].min()
            test_vec['timestamp'] -= test_vec['timestamp'].min()
            test_vec = test_vec.sort_values(by='timestamp')

            if(test_split > 0):
                test_vec.to_csv(f'{dest}/{(f"{lab}_", "")[lab!=""]}{name}_test.csv', index=use_index, header=use_header)
            train_vec.to_csv(f'{dest}/{(f"{lab}_", "")[lab!=""]}{name}_train.csv', index=use_index, header=use_header)
        
    except Exception as e:
        print(traceback.format_exc())
        return f'An error occured while parsing:\n{e}'

    return 'Success'

#useful for testing
if __name__ == "__main__":
    print(vectorize("C:/Users/thoma/Documents/WINTER24/SensorLab/Raw/2024-02-12_13-32-34-349344.csv", "C:/Users/thoma/Desktop", "test", note_labels=True))