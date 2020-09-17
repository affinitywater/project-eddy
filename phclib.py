"""Per Household Consumption daily trends modelling lib"""

import pandas as pd
import numpy as np
import os
import pickle

def save_obj(obj, name, full_path=False):
    """Pickle-save object to disk"""
    if full_path:
        with open(name, 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    else:
        with open('{}/'.format(os.getcwd()) + name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
			

def load_obj(name, full_path=False):
    """Load pickled object into memory"""
    if full_path:
        with open(name, 'rb') as f:
            return pickle.load(f)
    else:
        with open('{}/'.format(os.getcwd()) + name + '.pkl', 'rb') as f:
            return pickle.load(f)
			
def pythonify_cols(cols):
    """Make columns lower case and replace spaces with underscores as per Python PEP rules"""
    return ['_'.join(c.split()).lower().replace('-','_').replace('___','_').replace('__','_') for c in cols]
    
def compress_df(df, force_float32=True, verbose=False):
    """
    Improve storage requirements by converting columns to appropriate compressed data format without losing data
    """
    cols = df.columns.tolist()
    for i, col in enumerate(cols):
        # Shrink floats
        if df[col].dtype == 'float64':
            if force_float32:
                df[col] = df[col].astype('float32')
            else:
                if min((df[col].astype('float32').fillna(0) == df[col].astype('float64').fillna(0))) is True:
                    df[col] = df[col].astype('float32')
         # Shrink long ints
        if df[col].dtype == 'int64':
            if min((df[col].astype('int8').fillna(0) == df[col].astype('int64').fillna(0))) is True:
                df[col] = df[col].astype('int8')
            elif min((df[col].astype('int16').fillna(0) == df[col].astype('int64').fillna(0))) is True:
                df[col] = df[col].astype('int16')
            elif min((df[col].astype('int32').fillna(0) == df[col].astype('int64').fillna(0))) is True:
                df[col] = df[col].astype('int32')
        if df[col].dtype == 'int32':
            if min((df[col].astype('int8').fillna(0) == df[col].astype('int32').fillna(0))) is True:
                df[col] = df[col].astype('int8')
            elif min((df[col].astype('int16').fillna(0) == df[col].astype('int32').fillna(0))) is True:
                df[col] = df[col].astype('int16')
        if verbose:
            print("{}/{}/{}           ".format(i+1, len(cols), col), end='\r')
    return df
    
def chunks(sample, chunksize):
    '''Split a 1d collection into chunks'''
    res = [sample[x:x+chunksize] for x in range(0, len(sample), chunksize)]
    return res
    
def train_test_split_by_key(data, target, usecols, key, test_size):
    """
    Split a dataset into training and testing set by a certain category key.
    Returns the same output as sklearn's train_test_split
    """
    train = data[data[key].isin(pd.Series(data[key].unique()).sample(frac=1-test_size))][usecols+[target]+[key]]
    test = data[~data[key].isin(train[key].unique())][usecols+[target]+[key]]
    print('Test Size: ', test.shape[0] / data.shape[0])
    return train.drop([target, key], 1), test.drop([target, key], 1), train[target], test[target]