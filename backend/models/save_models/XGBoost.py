#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from sklearn.model_selection import train_test_split
import xgboost as xgb
from xgboost import plot_importance
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import recall_score
from sklearn.metrics import r2_score

import shap
import matplotlib.pyplot as plt
#from tqdm.auto import tqdm


# In[7]:


get_ipython().run_line_magic('cd', '"C:\\Users\\Angel\\Documents\\NUS\\Y3S2\\DSA3101 Data Science in Practice\\DSA3101\\project_backend\\sliding_window_data"')
get_ipython().run_line_magic('pwd', '')

# updated sliding window data dataset
df_sliding = pd.read_csv('sliding_window_data-full.csv', nrows=5000000)
df_sliding


#10min for 10mil rows
#~40s for 2mil rows
#3min for 5mil rows


# In[3]:


df_sliding['date'].nunique()


# In[4]:


df_clean = df_sliding.fillna(0.0)
df_clean

#3min for 10mil rows
#~10s for 2mil rows
#~1min for 5mil rows


# In[5]:


# use all rain related data (i.e. use also relative time, station distance for each of the nearest 5 stations)
X_all = df_clean.drop(['date','time','station','value', 
                   'T1S1_station number', 'T1S2_station number', 'T1S3_station number','T1S4_station number','T1S5_station number','T1S6_station number', 
                   'T2S1_station number', 'T2S2_station number', 'T2S3_station number','T2S4_station number','T2S5_station number','T2S6_station number', 
                   'T3S1_station number', 'T3S2_station number', 'T3S3_station number','T3S4_station number','T3S5_station number','T3S6_station number', 
                   'T4S1_station number', 'T4S2_station number', 'T4S3_station number','T4S4_station number','T4S5_station number','T4S6_station number', 
                   'T5S1_station number', 'T5S2_station number', 'T5S3_station number','T5S4_station number','T5S5_station number','T5S6_station number', 
                   'T6S1_station number', 'T6S2_station number', 'T6S3_station number','T6S4_station number','T6S5_station number','T6S6_station number'], 
                   axis = 1)

y_all = df_clean.loc[:, 'value']


# In[6]:


# to check
y_all.isna().any()


# ## Train the model

# In[7]:


X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=0.2, random_state=3101)


# In[8]:


model = xgb.XGBRegressor(
    n_estimators=500,
    max_depth=10,
    grow_policy="lossguide",
    learning_rate=0.01,
    objective="reg:squarederror",
    reg_alpha=0.5,
    reg_lambda=0.5,
    tree_method="hist",
    random_state=3101,
)
model.fit(X_train, y_train)

train_forecasts = model.predict(X_train)


# ## Testing the model

# In[9]:


test_forecasts = model.predict(X_test)


# In[10]:


result = pd.DataFrame({'actual':y_test, 'predicted':test_forecasts})
result


# In[33]:


# Metric: MSE
test_mse = mean_squared_error(y_test, test_forecasts, squared=True)

# Metric: MAE
test_mae = mean_absolute_error(y_test, test_forecasts)

threshold = 0.0
# Metric: FN rate --> Worst Case: Predicted no rain, but rained
fn = result[result['actual'] > threshold]  ## all actual positives
fn = fn[round(fn['predicted'], 1) <= threshold]
test_fnr = len(fn) / len(result[result['actual'] > threshold])

# Metric: FP rate --> 2nd Worst Case: Predicted rain, but no rain
fp = result[result['actual'] <= threshold]  ## all actual negatives
fp = fp[round(fp['predicted'], 1) > threshold]
test_fpr = len(fp) / len(result[result['actual'] <= threshold])

# Metric: R-squared score
test_r_squared = r2_score(y_test, test_forecasts)


# In[34]:


# Metrics output
print("MSE is: {}".format(test_mse))
print("MAE is: {}".format(test_mae))
print("FN Rate is: {}".format(test_fnr))
print("FP Rate is: {}".format(test_fpr))
print("R-squared Score is: {}".format(test_r_squared))


# ## Shapley Additive Explanation (SHAP) value
# Reference: https://www.analyticsvidhya.com/blog/2019/11/shapley-value-machine-learning-interpretability-game-theory/ \n
# Reference: https://www.kaggle.com/code/bryanb/xgboost-explainability-with-shap

# In[ ]:


# load JS visualization code to notebook
shap.initjs()


# In[ ]:


X_sampled = X_train.sample(50000, random_state=3101)


# In[ ]:


explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_sampled)

#~10min for 50000 samples from X_train


# In[ ]:


#shap.summary_plot(shap_values, features=X_sampled, feature_names=X_sampled.columns)


# In[ ]:


shap.summary_plot(shap_values, X_sampled, plot_type="bar")


# In[ ]:


# To save SHAP values summary
#shap.summary_plot(shap_values, X_sampled, plot_type="bar", show=False)
#plt.savefig("shap_summary.png",dpi=700)

