#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[2]:


from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd

# Load data
data = pd.read_csv('sliding_window_data.csv', nrows=1000000)


# In[3]:


#Fill the NA data with 0
data = data.fillna(0)


# In[4]:


data


# In[5]:


#Change the time variable as factor
data['T1S1_time'] = data['T1S1_time'].astype(object)
data['T1S2_time'] = data['T1S2_time'].astype(object)
data['T1S3_time'] = data['T1S3_time'].astype(object)
data['T1S4_time'] = data['T1S4_time'].astype(object)
data['T1S5_time'] = data['T1S5_time'].astype(object)
data['T1S6_time'] = data['T1S6_time'].astype(object)

data['T2S1_time'] = data['T2S1_time'].astype(object)
data['T2S2_time'] = data['T2S2_time'].astype(object)
data['T2S3_time'] = data['T2S3_time'].astype(object)
data['T2S4_time'] = data['T2S4_time'].astype(object)
data['T2S5_time'] = data['T2S5_time'].astype(object)
data['T2S6_time'] = data['T2S6_time'].astype(object)

data['T3S1_time'] = data['T3S1_time'].astype(object)
data['T3S2_time'] = data['T3S2_time'].astype(object)
data['T3S3_time'] = data['T3S3_time'].astype(object)
data['T3S4_time'] = data['T3S4_time'].astype(object)
data['T3S5_time'] = data['T3S5_time'].astype(object)
data['T3S6_time'] = data['T3S6_time'].astype(object)

data['T4S1_time'] = data['T4S1_time'].astype(object)
data['T4S2_time'] = data['T4S2_time'].astype(object)
data['T4S3_time'] = data['T4S3_time'].astype(object)
data['T4S4_time'] = data['T4S4_time'].astype(object)
data['T4S5_time'] = data['T4S5_time'].astype(object)
data['T4S6_time'] = data['T4S6_time'].astype(object)

data['T5S1_time'] = data['T5S1_time'].astype(object)
data['T5S2_time'] = data['T5S2_time'].astype(object)
data['T5S3_time'] = data['T5S3_time'].astype(object)
data['T5S4_time'] = data['T5S4_time'].astype(object)
data['T5S5_time'] = data['T5S5_time'].astype(object)
data['T5S6_time'] = data['T5S6_time'].astype(object)

data['T6S1_time'] = data['T6S1_time'].astype(object)
data['T6S2_time'] = data['T6S2_time'].astype(object)
data['T6S3_time'] = data['T6S3_time'].astype(object)
data['T6S4_time'] = data['T6S4_time'].astype(object)
data['T6S5_time'] = data['T6S5_time'].astype(object)
data['T6S6_time'] = data['T6S6_time'].astype(object)


# In[174]:


#Testing only with the raining data
X = data.drop(['date','time','station',
               'T1S1_station number', 'T1S2_station number', 'T1S3_station number','T1S4_station number','T1S5_station number','T1S6_station number',
              'T2S1_station number', 'T2S2_station number', 'T2S3_station number','T2S4_station number','T2S5_station number','T2S6_station number',
              'T3S1_station number', 'T3S2_station number', 'T3S3_station number','T3S4_station number','T3S5_station number','T3S6_station number',
              'T4S1_station number', 'T4S2_station number', 'T4S3_station number','T4S4_station number','T4S5_station number','T4S6_station number',
              'T5S1_station number', 'T5S2_station number', 'T5S3_station number','T5S4_station number','T5S5_station number','T5S6_station number',
              'T6S1_station number', 'T6S2_station number', 'T6S3_station number','T6S4_station number','T6S5_station number','T6S6_station number'], axis=1)
y = data['value'] # Target variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_test = X_test.loc[(X_test["value"]!=0)]
X_test = X_test.drop(['value'], axis=1)
y_test = y_test[y_test!=0]
X_train = X_train.drop(['value'], axis=1)


# In[169]:


#with the origin station data
X = data.drop(['date','time','station','value',
               'T1S1_station number', 'T1S2_station number', 'T1S3_station number','T1S4_station number','T1S5_station number','T1S6_station number',
              'T2S1_station number', 'T2S2_station number', 'T2S3_station number','T2S4_station number','T2S5_station number','T2S6_station number',
              'T3S1_station number', 'T3S2_station number', 'T3S3_station number','T3S4_station number','T3S5_station number','T3S6_station number',
              'T4S1_station number', 'T4S2_station number', 'T4S3_station number','T4S4_station number','T4S5_station number','T4S6_station number',
              'T5S1_station number', 'T5S2_station number', 'T5S3_station number','T5S4_station number','T5S5_station number','T5S6_station number',
              'T6S1_station number', 'T6S2_station number', 'T6S3_station number','T6S4_station number','T6S5_station number','T6S6_station number'], axis=1) # Input features
y = data['value'] # Target variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# In[ ]:





# In[1]:


# Train random forest model with full data
rf_full = RandomForestRegressor(n_estimators=500, random_state=42)
rf_full.fit(X_train, y_train)


# In[175]:


# Predict on test set
y_pred = rf_full.predict(X_test)

# Evaluate model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse:.2f}')


# In[172]:


(y_pred-y_test).sort_values(ascending=True)


# In[130]:


min((y_pred-y_test))


# In[176]:


#result = pd.concat([y_pred,y_test], axis=1)
#type(y_pred)
result = pd.DataFrame({'predicted': y_pred, 'actual': y_test}, columns=['predicted', 'actual'])
result


# In[177]:


#Worst case - predicted no rain but rain
result1 = result[result['actual'] >= 0.25]
result1 = result1[result1['predicted'] <= 0.25]
len(result1)/len(result)


# In[178]:


#second worst case - predicted rain but no rain
result2 = result[result['actual'] <= 0.25]
result2 = result2[result2['predicted'] >= 0.25]
len(result2)/len(result)


# In[173]:


len(abs(y_pred-y_test)[abs(y_pred-y_test)>=0.25])/len(abs(y_pred-y_test))


# In[147]:


len(abs(y_pred-y_test))


# In[148]:


#from sklearn import metrics
#metrics.confusion_matrix(y_test, y_pred)


# In[ ]:




