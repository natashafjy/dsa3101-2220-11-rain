#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import PassiveAggressiveRegressor
from tqdm.autonotebook import tqdm


#Setting Seed value
seed = 3101
np.random.seed(3101)

def preprocess(df):
    """
    input: pandas dataframe
    output: pandas dataframe
    """
    #drop the date, time and station labels 
    drop_cols = ["date","time","station"]
    for i in range(1,7):
        for j in range(1,7):
            drop_cols.append(f"T{i}S{j}_station number")
    processed_df = df.drop(drop_cols, axis=1, inplace=False)
    processed_df.fillna(value=0, inplace=True)
    return processed_df

def train(df_iterator):
    """
    input : df_iterator, pandas iterator which gives batches of dataframe which includes the train_label in the 1st column and the remaining columns are feature variables
    """
    regression_model= PassiveAggressiveRegressor(C=0.01,random_state=seed, shuffle=True)
    for batch in tqdm(df_iterator):
        batch = preprocess(batch)
        regression_model.partial_fit(batch.iloc[:,1:], batch.iloc[:,0])
    return regression_model


def evaluate(y_pred,y_true):
    threshold = 0.0
    result = pd.DataFrame({'predicted': y_pred, 'actual': y_true}, columns=['predicted', 'actual'])
    fn = result[result['actual'] > threshold]
    fn = fn[round(fn['predicted'],1) <= threshold]
    fnr = len(fn)/len(result[result['actual'] > threshold])

    fp = result[result['actual'] == threshold]
    fp = fp[round(fp['predicted'],1) > threshold]
    fpr = len(fp)/len(result[result['actual'] == threshold])

    tp = result[result['actual'] > threshold]
    tp = tp[round(tp['predicted'],1) > threshold]
    tp = len(tp)

    f1 = tp/(tp+0.5*(len(fp)+len(fn)))
    print(f'False negative rate is : {fnr:.5f}')
    print(f'False positive rate (FP/FP+TN) is : {fpr:.5f}')
    print(f'F1 score is [ TP/(TP + 0.5(FP+FN)) ]: {f1:.5f}')
    return [fnr, fpr, f1]

def save(model, filename):
    """
    inputs: model, filename : saves model to filename location
    outputs: None
    """
    pickle.dump(model, open(filename, "wb"))


# Train Test split
# Train 80% - Test 20%
# Total number of rows = 25 million

test_index = range(10_000_000,15_000_000+1)

# Generate iterator for train dataset
chunksize = 1_000_000
sliding_window_data = pd.read_csv("sliding_window_data.csv", chunksize=chunksize, iterator=True, skiprows=test_index)

# Create test dataset
test_dataset = pd.read_csv("sliding_window_data.csv", header=0, nrows=5_000_000, skiprows=range(1,10_000_000))
test_dataset = preprocess(test_dataset)

# Train PassiveAggressiveRegressor model
PAR_model = train(sliding_window_data)

# Evaluate model performance and print some statistics
prediction = PAR_model.predict(test_dataset.iloc[:,1:])
evaluate(prediction,test_dataset.iloc[:,0])

# Save model into MLPRegressor.pkl in current directory
filename = "PassiveAggressiveRegressor.pkl"
save(PAR_model, filename)
