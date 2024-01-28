#CSV utilities and parsing
import pandas as pd
import numpy as np

BASE_METRICS = ('EA', 'EL',
           'PI', 'PR', 'PG',
           'AX', 'AY', 'AZ',
           'GX', 'GY', 'GZ',
           'MX', 'MY', 'MZ',
           'SA', 'SR', 'SF',
           'T1', 'HR', 'BI')

IGNORED_METRICS = ('EM', 'B%', 'BV',
                   'RB', 'TL', 'AK',
                   'RS', 'RB', 'RD',
                   'DC')
return_msg = ''

def vectorize(source, 
              dest, 
              derive=True,   
              label='', 
              cliphead=0, 
              cliptail=0):

    try:    
        raw = pd.read_csv(source, header=None, on_bad_lines='skip', skiprows=2, usecols=[3, 6], index_col=False)
        raw = raw[~raw[3].str.contains('|'.join(IGNORED_METRICS))]
        
        list = []
        vec_row = {metric: np.nan for metric in BASE_METRICS}

        for raw_row in raw.itertuples(index=True):
            if vec_row[raw_row[1]] is not np.nan:
                list.append(vec_row)
                vec_row = {key: np.nan for key in vec_row.keys()}
            vec_row[raw_row[1]] = raw_row[2]

        vec = pd.DataFrame.from_dict(data=list)

        #Filling up 'holes' in data
        for metric in BASE_METRICS:
            indices = vec[vec[metric].notnull()].index
            for start, end in zip(indices,indices[1:]):
                if end-start > 1:
                    startval = float(vec.at[start, metric])
                    endval = float(vec.at[end, metric])
                    interpolated = np.linspace(start=startval, stop=endval, num=end-start+2)
                    vec.loc[start+1:end, metric] = interpolated[1:-1]

        #Clipping Dataframe
        vec.drop(vec.head(cliphead).index, inplace=True)
        vec.drop(vec.tail(cliptail).index, inplace=True) 
        vec.dropna(how='any', inplace=True)

        vec.to_csv(dest, index=False, header=True)
    
    except Exception as e:
        return f'An error occured while parsing:\n{e}'

    return 'Success'