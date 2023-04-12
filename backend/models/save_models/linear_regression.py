#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import datetime
import numpy as np
from sklearn.linear_model import SGDRegressor, PassiveAggressiveRegressor
from sklearn.model_selection import train_test_split
import sklearn.metrics as sm
from sklearn.neural_network import MLPRegressor
from tqdm.autonotebook import tqdm


# In[4]:


chunksize = 1000000
sliding_window_data = pd.read_csv("sliding_window_data.csv", chunksize=chunksize, iterator=True)


# #### Setting Seed value

# In[5]:


seed = 3101
np.random.seed(3101)


# In[6]:


# train_data, test_data = train_test_split(sliding_window_data, test_size=0.2, random_state=seed)


# In[7]:


# sliding_window_data.dtypes


# In[8]:


drop_cols = ["date","time","station"]
for i in range(1,7):
    for j in range(1,7):
        drop_cols.append(f"T{i}S{j}_station number")


# In[9]:


regression_model = SGDRegressor(random_state=seed, shuffle=True)
for batch in tqdm(sliding_window_data):
    drop_cols = ["date","time","station"]
    for i in range(1,7):
        for j in range(1,7):
            drop_cols.append(f"T{i}S{j}_station number")
    batch.drop(drop_cols, axis=1, inplace=True)
    batch.fillna(value=0, inplace=True)
    regression_model.partial_fit(batch.iloc[:,1:], batch.iloc[:,0])


# In[10]:


random_skips = np.random.randint(1,chunksize,size=3101)
test_data = pd.read_csv("sliding_window_data.csv", header=0, nrows=chunksize, skiprows=random_skips)
drop_cols = ["date","time","station"]
for i in range(1,7):
    for j in range(1,7):
        drop_cols.append(f"T{i}S{j}_station number")
test_data.drop(drop_cols, axis=1, inplace=True)
test_data.fillna(value=0, inplace=True)


# In[11]:


prediction = regression_model.predict(test_data.iloc[:,1:])


# In[18]:


def display_metrics(y_pred,y_true):
    print(f'R2 score is : {sm.r2_score(y_true,y_pred)}')
    print(f'MAE is : {sm.mean_absolute_error(y_true,y_pred)}')
    print(f'MSE is : {sm.mean_squared_error(y_true,y_pred)}')
    
    threshold = 0.0
    temp = pd.concat([pd.DataFrame(prediction, columns=["predict"]),y_true], axis=1)
    temp["predict"].round(decimals=1)
    fn = temp[temp["value"] > threshold]
    fn = fn[fn["predict"] <= threshold ]
    p = y_true[y_true > threshold]
    fnr = len(fn)/len(p)
    recall = 1-fnr
    print(f'Recall is : {recall}')
    print(f'False negative rate is : {fnr}')

    tn = temp[temp["value"] <= threshold]
    tn = tn[tn["predict"] <= threshold ]
    fp = temp[temp["value"] <= threshold]
    fp = fp[fp["predict"] > threshold]
    fpr = len(tn)/(len(tn) + len(fp))
    print(f'False positive rate (FP/FP+TN) is : {fpr}')


# In[19]:


display_metrics(prediction,test_data.iloc[:,0])

