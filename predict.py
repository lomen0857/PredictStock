#!/usr/bin/env python
# coding: utf-8

# In[20]:


import datetime
import numpy as np
import pandas as pd
import pickle
import os.path
#pd.core.common.is_list_like = pd.api.types.is_list_like
#import pandas_datareader as web

from sklearn import preprocessing
#from keras.models import Sequential
#from keras.models import load_model


# In[21]:


Xcolumns = pickle.load(open("max_Xcolumns.sav","rb"))
columns_array = []


# In[22]:


for index in range(len(Xcolumns)):
    columns_array.append(Xcolumns[index][:4])
columns_unique_array = list(set(columns_array))
columns_unique_array.append(1321)


# In[23]:


for code in columns_unique_array:
    print(code)
    
    path = "importETF/" + str(code) + ".csv"
    
    if os.path.exists(path):
        temp_df = pd.read_csv(path,engine = "python" ,encoding="utf8")
    else:
        error_array.append(code)
        continue
        
    new_df = pd.DataFrame()
    new_df["Date"] = temp_df["Date"]
    
    #始値
    new_df["Open"] = 0
    
    for dateIndex in temp_df.index:
        
        #当日の始値
        openValue = temp_df.at[dateIndex,"Open"]
        
        new_df.at[dateIndex,"High"] = temp_df.at[dateIndex,"High"] - openValue
        new_df.at[dateIndex,"Low"] = temp_df.at[dateIndex,"Low"] - openValue
        new_df.at[dateIndex,"Close"] = temp_df.at[dateIndex,"Close"] - openValue
        
        if dateIndex != 0:
            new_df.at[dateIndex,"Volume"] = temp_df.at[dateIndex,"Volume"] - temp_df.at[dateIndex-1,"Volume"]
            new_df.at[dateIndex,"Open"] = openValue - temp_df.at[dateIndex-1,"Close"]
            
        else:
            new_df.at[0,"Volume"] = 0
    
    #csvファイル書き出し
    new_df.to_csv("PredictStockDataDif/" + str(code) + "_dif.csv")


# In[ ]:


ETF_df = pd.DataFrame()

startDate = "2010/01/01"

df = pd.read_csv("importETF.csv",encoding="utf8")

for code in df["code"]:
    
    if code not in error_array:
        code = str(code)
        
        temp = pd.DataFrame()
        temp = pd.read_csv("PredictStockDataDif/" + code + "_dif.csv",encoding="utf8")
        
        if code == "1305":
            #初回のみETF_dfにindexを設定
            ETF_df["Date"] = temp["Date"]
            ETF_df = ETF_df[ETF_df["Date"] > startDate]
            ETF_df = ETF_df.set_index("Date")
            
        if code =="1321":
            for dateIndex in range(0,len(temp.index)-1):
                tempDate = temp.at[dateIndex,"Date"]
                
                if tempDate <= startDate:
                    continue
                    
                tempClose = temp.at[dateIndex+1,"Close"]
                if tempClose >= 20:
                    ETF_df.at[tempDate,"nextDay_HighLow"] = 1
                elif tempClose >= 0:
                    ETF_df.at[tempDate,"nextDay_HighLow"] = 0
                elif tempClose > -20:
                    ETF_df.at[tempDate,"nextDay_HighLow"] = 0
                else:
                    ETF_df.at[tempDate,"nextDay_HighLow"] = -1
                    
        for dateIndex in temp.index:
            tempDate = temp.at[dateIndex,"Date"]
            
            if tempDate <= startDate:
                continue
                
            ETF_df.at[tempDate,code + "Open"] = temp.at[dateIndex,"Open"]
            ETF_df.at[tempDate,code + "High"] = temp.at[dateIndex,"High"]
            ETF_df.at[tempDate,code + "Low"] = temp.at[dateIndex,"Low"]
            ETF_df.at[tempDate,code + "Close"] = temp.at[dateIndex,"Close"]
            ETF_df.at[tempDate,code + "Volume"] = temp.at[dateIndex,"Volume"]/10000
            


# In[ ]:


path = "importETF/1321.csv"

if os.path.exists(path):
    nikkei1321_df = pd.read_csv(path,engine = "python" ,encoding="utf8")
else:
    error_array.append(code)


# In[52]:


df = pd.read_csv('nikkei_2001_2018.csv',encoding='SHIFT-JIS')


# In[53]:


model_open = Sequential()
model_open = load_model('model_open')

model_close = Sequential()
model_close = load_model('model_close')


# In[54]:


#modelのinput_shapeの要素数を取得
input_shape = model_open.layers[0].get_input_at(0).get_shape().as_list()[1]


# In[55]:


scaler = preprocessing.MinMaxScaler()
scaler.fit([[7200],[24790]])
scaler.fit([[1],[15]])


# In[56]:


df.head()


# In[57]:


input_data = input()

end_index = df.query('日付 == "' + str(input_data) + '"').index
start_index = end_index - input_shape

df = df[start_index.values[0]:end_index.values[0]]


# In[58]:


open_date = df.loc[:, ['始値']]
close_date = df.loc[:, ['終値']]


# In[59]:


open_date = np.array(open_date)
close_date = np.array(close_date)


# In[60]:


open_date = scaler.transform(open_date)
close_date = scaler.transform(close_date)

open_date = open_date.reshape(1,input_shape,1)
close_date = close_date.reshape(1,input_shape,1)


# In[61]:


predicted_open = model_open.predict(open_date)
predicted_close = model_close.predict(close_date)
print(predicted_open)
print(predicted_close)


# In[62]:


if predicted_open <= predicted_close:
    print('上昇')
else:
    print('降下')


# In[ ]:




