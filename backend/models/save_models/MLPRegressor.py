#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
import sklearn.metrics as sm
from sklearn.neural_network import MLPRegressor
from tqdm.autonotebook import tqdm


# ### Train Test split
# 
# Train 80% - Test 20%<br>
# Total number of rows = 25 million

# In[4]:


test_index = range(10_000_000,15_000_000+1)


# In[18]:


chunksize = 1000000
sliding_window_data = pd.read_csv("sliding_window_data.csv", chunksize=chunksize, iterator=True, skiprows=test_index)


# #### Setting Seed value

# In[6]:


seed = 3101
np.random.seed(3101)


# In[19]:


regression_model = MLPRegressor(random_state=seed, shuffle=True)
for batch in tqdm(sliding_window_data):
    drop_cols = ["date","time","station"]
    for i in range(1,7):
        for j in range(1,7):
            drop_cols.append(f"T{i}S{j}_station number")
    batch.drop(drop_cols, axis=1, inplace=True)
    batch.fillna(value=0, inplace=True)
    regression_model.partial_fit(batch.iloc[:,1:], batch.iloc[:,0])


# In[22]:


def display_metrics(y_pred,y_true):
    print(f'R2 score is : {sm.r2_score(y_true,y_pred)}')
    print(f'MAE is : {sm.mean_absolute_error(y_true,y_pred)}')
    print(f'MSE is : {sm.mean_squared_error(y_true,y_pred)}')
    
    threshold = 0.0
    result = pd.DataFrame({'predicted': y_pred, 'actual': y_true}, columns=['predicted', 'actual'])
    result
    fn = result[result['actual'] > threshold]
    fn = fn[round(fn['predicted'],1) <= threshold]
    fnr = len(fn)/len(result[result['actual'] > threshold])
    print(f'False negative rate is : {fnr}')

    fp = result[result['actual'] == threshold]
    fp = fp[round(fp['predicted'],1) > threshold]
    fpr = len(fp)/len(result[result['actual'] == threshold])
    print(f'False positive rate (FP/FP+TN) is : {fpr}')


# In[12]:


test_dataset = pd.read_csv("sliding_window_data.csv", header=0, nrows=5_000_000, skiprows=range(1,10_000_000))
drop_cols = ["date","time","station"]
for i in range(1,7):
    for j in range(1,7):
        drop_cols.append(f"T{i}S{j}_station number")
test_dataset.drop(drop_cols, axis=1, inplace=True)
test_dataset.fillna(value=0, inplace=True)


# In[23]:


prediction_base = regression_model.predict(test_dataset.iloc[:,1:])


# In[24]:


display_metrics(prediction_base,test_dataset.iloc[:,0])


# #### Hyper parameter tuning
# Training on a subset of the data for faster performance

# In[8]:


sample_size = 1000000
sample_data = pd.read_csv("sliding_window_data.csv", header=0, nrows=sample_size, skiprows=range(1,3101888))


# In[9]:


drop_cols = ["date","time","station"]
for i in range(1,7):
    for j in range(1,7):
        drop_cols.append(f"T{i}S{j}_station number")
sample_data.drop(drop_cols, axis=1, inplace=True)
sample_data.fillna(value=0, inplace=True)


# In[10]:


train, test = train_test_split(sample_data, test_size=0.2, random_state=seed, shuffle=True)


# In[11]:


train.iloc[:,1:].values


# In[12]:


mlpr = MLPRegressor(random_state=seed, shuffle=True)
param_list = {"hidden_layer_sizes": [(64,),(32,), (16,), (32,64), (16,32), (128,)], "activation": ["logistic", "relu"],
              "solver": ["sgd", "adam"]}

gridCV = GridSearchCV(estimator=mlpr, param_grid=param_list, verbose=10, return_train_score=True, n_jobs=3, refit=True)
gridCV.fit(train.iloc[:,1:].values, train.iloc[:,0].values)


# In[15]:


gridCV.cv_results_


# In[14]:


gridCV.best_params_


# #### Fitting a new MLPRegressor with the best params from hyperparamater tuning

# #### Re-generate train dataset iterator

# In[5]:


sliding_window_data = pd.read_csv("sliding_window_data.csv", chunksize=chunksize, iterator=True, skiprows=test_index)


# In[8]:


regression_model_hyper = MLPRegressor(activation="relu", hidden_layer_sizes=(32,), solver="adam", random_state=seed, shuffle=True)
for batch in tqdm(sliding_window_data):
    drop_cols = ["date","time","station"]
    for i in range(1,7):
        for j in range(1,7):
            drop_cols.append(f"T{i}S{j}_station number")
    batch.drop(drop_cols, axis=1, inplace=True)
    batch.fillna(value=0, inplace=True)
    regression_model_hyper.partial_fit(batch.iloc[:,1:], batch.iloc[:,0])


# In[17]:


prediction_hyper = regression_model_hyper.predict(test_dataset.iloc[:,1:])
display_metrics(prediction_hyper,test_dataset.iloc[:,0])

