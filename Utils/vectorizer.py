#CSV utilities and parsing
import pandas as pd
import numpy as np
import os
import traceback

def vectorize(source, 
              dest, 
              name='',  
              label='',
              note_labels=False,
              append_data=True,
              test_split=0.15, 
              cliphead=0, 
              cliptail=0,
              use_index=False,
              use_header=True):
    
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

    if name=='' and label=='' and not note_labels:
        return 'Name and Label cannot both be empty if labels aren\'t inferred by notes in data.'

    try:
        if note_labels:
            BASE_METRICS.append('UN')
        else:
            IGNORED_METRICS.append('UN') 

        raw = pd.read_csv(source, header=None, on_bad_lines='skip', skiprows=1, usecols=[3, 6, 7], index_col=False)
        raw = raw[~raw[3].str.contains('|'.join(IGNORED_METRICS))]
        
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
            vec = vec.drop('UN', axis=1)

            for start, end in zip(indices,indices[1:]):
                dfs.append(vec[start:end-1])
            dfs.append(vec[end:])
        
        else:
            labels.append(label)
            dfs.append(vec)
        
        #Set Parameters for writing files
        #Create missing directories
        if(test_split > 0):
            if not os.path.isdir(f'{dest}/test'):
                os.makedirs(f'{dest}/test')
        if not os.path.isdir(f'{dest}/train'):
            os.makedirs(f'{dest}/train')

        #Set writing mode
        mode = 'a+' if append_data else 'w'
        
        for df, lab in zip(dfs, labels):

            df.dropna(how='any', inplace=True)

            #Clipping Dataframe
            df.drop(df.head(cliphead).index, inplace=True)
            df.drop(df.tail(cliptail).index, inplace=True)

            #Split into test and train, cannot use random indices due to the sequential nature of the data
            split_index = int((1-test_split)*len(df))
            test_df = df.iloc[split_index:, :]
            train_df = df.iloc[:split_index, :]

            #Adjust timestamps
            train_df['timestamp'] -= train_df['timestamp'].min()
            test_df['timestamp'] -= test_df['timestamp'].min()
            test_df = test_df.sort_values(by='timestamp')

            #Set filepaths
            test_path = f'{dest}/test/{("", lab.lower())[note_labels or label!=""]}{(".", "")[name==""]}{name}.csv'
            train_path = f'{dest}/train/{("", lab.lower())[note_labels or label!=""]}{(".", "")[name==""]}{name}.csv'

            #Set, changed below if necessary
            use_test_header = True
            use_train_header = True

            #Adjust timestamp if appending
            if os.path.isfile(test_path) and append_data:
                curr_test = pd.read_csv(test_path)
                #No need to include header if appending
                use_test_header = False
                test_df['timestamp'] += curr_test['timestamp'].max()+1

            if os.path.isfile(train_path) and append_data:
                curr_train = pd.read_csv(train_path)
                #No need to include header if appending
                use_train_header = False
                train_df['timestamp'] += curr_train['timestamp'].max()+1


            if(test_split > 0):
                test_df.to_csv(test_path, index=use_index, mode=mode, header=use_test_header)
            train_df.to_csv(train_path, index=use_index, mode=mode, header=use_train_header)
        
    except Exception as e:
        print(traceback.format_exc())
        return f'An error occured while parsing:\n{e}'

    return 'Success'

#useful for testing
if __name__ == "__main__":
    print(vectorize("C:/Users/thoma/Documents/WINTER24/SensorLab/Raw/2024-02-12_13-32-34-349344.csv", "C:/Users/thoma/Desktop", "test", note_labels=True))