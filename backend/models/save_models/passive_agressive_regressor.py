#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from sklearn.linear_model import PassiveAggressiveRegressor
from sklearn.model_selection import train_test_split
import sklearn.metrics as sm
from sklearn.model_selection import GridSearchCV
from tqdm.autonotebook import tqdm
import matplotlib.pyplot as plt


# #### Train Test split
# Total 25 million rows <br>
# Split 0.8 Train : 0.2 Test

# In[2]:


test_index = range(10_000_000,15_000_000+1)


# In[3]:


chunksize = 1000000
sliding_window_data = pd.read_csv("sliding_window_data.csv", chunksize=chunksize, iterator=True, skiprows=test_index)


# #### Setting Seed value

# In[4]:


seed = 3101
np.random.seed(3101)


# In[5]:


regression_model = PassiveAggressiveRegressor(random_state=seed, shuffle=True)
for batch in tqdm(sliding_window_data):
    drop_cols = ["date","time","station"]
    for i in range(1,7):
        for j in range(1,7):
            drop_cols.append(f"T{i}S{j}_station number")
    batch.drop(drop_cols, axis=1, inplace=True)
    batch.fillna(value=0, inplace=True)
    regression_model.partial_fit(batch.iloc[:,1:], batch.iloc[:,0])


# In[6]:


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


# In[7]:


test_dataset = pd.read_csv("sliding_window_data.csv", header=0, nrows=5_000_000, skiprows=range(1,10_000_000))
drop_cols = ["date","time","station"]
for i in range(1,7):
    for j in range(1,7):
        drop_cols.append(f"T{i}S{j}_station number")
test_dataset.drop(drop_cols, axis=1, inplace=True)
test_dataset.fillna(value=0, inplace=True)


# In[8]:


prediction_base = regression_model.predict(test_dataset.iloc[:,1:])


# In[9]:


display_metrics(prediction_base,test_dataset.iloc[:,0])


# #### Hyper parameter tuning

# In[46]:


sample_size = 2000000
sample_data = pd.read_csv("sliding_window_data.csv", header=0, nrows=sample_size, skiprows=range(1,3101888))


# In[47]:


drop_cols = ["date","time","station"]
for i in range(1,7):
    for j in range(1,7):
        drop_cols.append(f"T{i}S{j}_station number")
sample_data.drop(drop_cols, axis=1, inplace=True)
sample_data.fillna(value=0, inplace=True)


# In[48]:


train, test = train_test_split(sample_data, test_size=0.2, random_state=seed, shuffle=True)


# In[49]:


train.iloc[:,0].values


# In[50]:


par = PassiveAggressiveRegressor(random_state=seed, shuffle=True)
param_list = {"C":[0.01, 0.05, 0.1, 0.5, 1.0, 1.5, 2.0]}

gridCV = GridSearchCV(estimator=par, param_grid=param_list, verbose=10, return_train_score=True, n_jobs=10, refit=True)
gridCV.fit(train.iloc[:,1:].values, train.iloc[:,0].values)


# In[51]:


gridCV.cv_results_


# In[54]:


gridCV.best_params_


# #### Fitting a new Passive Aggressive Regressor with the best params from hyperparamater tuning

# #### Re-generate train dataset iterator

# In[10]:


sliding_window_data = pd.read_csv("sliding_window_data.csv", chunksize=chunksize, iterator=True, skiprows=test_index)


# In[11]:


regression_model_hyper = PassiveAggressiveRegressor(C=0.01,random_state=seed, shuffle=True)
for batch in tqdm(sliding_window_data):
    drop_cols = ["date","time","station"]
    for i in range(1,7):
        for j in range(1,7):
            drop_cols.append(f"T{i}S{j}_station number")
    batch.drop(drop_cols, axis=1, inplace=True)
    batch.fillna(value=0, inplace=True)
    regression_model_hyper.partial_fit(batch.iloc[:,1:], batch.iloc[:,0])


# In[12]:


prediction_hyper = regression_model_hyper.predict(test_dataset.iloc[:,1:])
display_metrics(prediction_hyper,test_dataset.iloc[:,0])


# #### Visualize Variable importance

# In[138]:


features = list(test_dataset.keys())
features.remove("value")


# In[139]:


hyper_model_coeffs = pd.DataFrame(regression_model_hyper.coef_,index=features,columns=["predict"])
# hyper_model_coeffs = hyper_model_coeffs[abs(hyper_model_coeffs["predict"])>= 0.001]
hyper_model_coeffs = hyper_model_coeffs[abs(hyper_model_coeffs["predict"])>= 0.005]
# hyper_model_coeffs = hyper_model_coeffs.apply(abs, axis=1)
hyper_model_coeffs = hyper_model_coeffs.sort_values(by=["predict"],ascending=True)

colors = 9*["red"] + 12*["green"]
# hyper_model_coeffs = hyper_model_coeffs.head(5)
x,y = zip(*hyper_model_coeffs["predict"].items())


# In[140]:


plt.figure(figsize=(5,5))
plt.barh(x,y,color=colors)
plt.yticks()
plt.title("Value of Coefficient in fitted model (| |>=0.005)")
plt.xlabel("Coefficient value in fitted model")
plt.ylabel("Feature")
plt.show()

