#!/usr/bin/env python
# coding: utf-8

# In[2]:


import datetime as dt
import os.path
import pickle
from datetime import date, datetime, timedelta

import jsm
import numpy as np
import pandas as pd
from pandas.core import common as com
from sklearn import preprocessing


def set_span(start=None, end=None, periods=None, freq='D'):
    """ 引数のstart, end, periodsに対して
    startとendの時間を返す。

    * start, end, periods合わせて2つの引数が指定されていなければエラー
    * start, endが指定されていたらそのまま返す
    * start, periodsが指定されていたら、endを計算する
    * end, periodsが指定されていたら、startを計算する
    """
    if com._count_not_none(start, end, periods) != 2:  # Like a pd.date_range Error
        raise ValueError('Must specify two of start, end, or periods')
    start = start if start else (pd.Period(end, freq) - periods).start_time
    end = end if end else (pd.Period(start, freq) + periods).start_time
    return start, end


def get_jstock(code, freq='D', start=None, end=None, periods=None):
    """get Japanese stock data using jsm
    Usage:
        `get_jstock(6502)`
        To get TOSHIBA daily from today back to 30days except holiday.

        `get_jstock(6502, 'W', start=pd.Timestamp('2016'), end=pd.Timestamp('2017'))`
        To get TOSHIBA weekly from 2016-01-01 to 2017-01-01.

        `get_jstock(6502, end=pd.Timestamp('20170201'), periods=50)`
        To get TOSHIBA daily from 2017-02-01 back to 50days except holiday.

        `get_jstock(6502, 'M', start='first', end='last')`
        To get TOSHIBA monthly from 2000-01-01 (the date of start recording) to today.
    """
    # Default args
    if com._count_not_none(start, end, periods) == 0:  # All of args is None
        end, periods = 'last', 30

    # Switch frequency Dayly, Weekly or Monthly
    freq_dict = {'D': jsm.DAILY, 'W': jsm.WEEKLY, 'M': jsm.MONTHLY}

    # 'first' means the start of recording date
    if start == 'first':
        data = jsm.Quotes().get_historical_prices(
            code, range_type=freq_dict[freq], all=True)
        start = [i.date for i in data][-1]
    else:
        data = None  # Temporaly defined

    # 'last' means last weekday (or today)
    if end == 'last':
        end = pd.datetime.today()

    # Return "start" and "end"
    start, end = (x.date() if hasattr(x, 'date')
                  else x for x in set_span(start, end, periods, freq))
    print('Get data from {} to {}'.format(start, end))

    data = jsm.Quotes().get_historical_prices(
        code, range_type=freq_dict[freq], start_date=start, end_date=end) if not data else data
    df = _convert_dataframe(data)
    return df[start:end]


def _convert_dataframe(target):
    """Convert <jsm.pricebase.PriceData> to <pandas.DataFrame>"""
    date = [_.date for _ in target]
    open = [_.open for _ in target]
    high = [_.high for _ in target]
    low = [_.low for _ in target]
    close = [_.close for _ in target]
    adj_close = [_._adj_close for _ in target]
    volume = [_.volume for _ in target]
    data = {'Open': open,
            'High': high,
            'Low': low,
            'Close': close,
            'Adj Close': adj_close,
            'Volume': volume}
    columns = *data.keys(),
    df = pd.DataFrame(data, index=date, columns=columns).sort_index()
    df.index.name = 'Date'
    return df

def predictStock():

    Xcolumns1 = pickle.load(open("max_Xcolumns1.sav","rb"))
    Xcolumns2 = pickle.load(open("max_Xcolumns2.sav","rb"))
    Xcolumns3 = pickle.load(open("max_Xcolumns3.sav","rb"))

    columns_array = ['1321']

    for index in range(len(Xcolumns1)):
        columns_array.append(Xcolumns1[index][:4])

    for index in range(len(Xcolumns2)):
        columns_array.append(Xcolumns2[index][:4])

    for index in range(len(Xcolumns3)):
        columns_array.append(Xcolumns3[index][:4])

        
    columns_unique_array = list(set(columns_array))
    columns_unique_array


    #予想用
    Xcolumns1 = pickle.load(open("max_Xcolumns1.sav","rb"))
    Xcolumns2 = pickle.load(open("max_Xcolumns2.sav","rb"))
    Xcolumns3 = pickle.load(open("max_Xcolumns3.sav","rb"))

    columns_array = ['1321']

    for index in range(len(Xcolumns1)):
        columns_array.append(Xcolumns1[index][:4])

    for index in range(len(Xcolumns2)):
        columns_array.append(Xcolumns2[index][:4])

    for index in range(len(Xcolumns3)):
        columns_array.append(Xcolumns3[index][:4])

        
    columns_unique_array = list(set(columns_array))

    
    today = datetime.today()
    twoWeeksAgo = today - timedelta(days=14)
    twoWeeksAgo_str = datetime.strftime(twoWeeksAgo,'%Y-%m-%d')

    df_1321 = get_jstock(1321,start=pd.Timestamp(twoWeeksAgo_str),end=pd.Timestamp(today))

    df_1321.index[-1]
    one_str = datetime.strftime(df_1321.index[-1],'%Y-%m-%d')

    df_1321.index[-2]
    two_str = datetime.strftime(df_1321.index[-2],'%Y-%m-%d')

    errorStock_array = []
    for code in columns_unique_array :
        print("start:" + str(code))
        
        try:
            df_temp = get_jstock(code,start=pd.Timestamp(two_str),end=pd.Timestamp(one_str))
            df_temp.to_csv('PredictImportETF/' + str(code) + '.csv')
            print("end:" + str(code))
        except:
            df_temp = pd.DataFrame(np.zeros([2,6]), columns=['Open','High','Low','Close','Adj Close','Volume'],index=[two_str,one_str])
            df_temp.index.name = 'Date'

            df_temp.to_csv('PredictImportETF/' + str(code) + '.csv')
            errorStock_array.append(code)
            print("error")


    for code in columns_unique_array:
        print(code)
        
        path = "PredictImportETF/" + str(code) + ".csv"
        
        if os.path.exists(path):
            temp_df = pd.read_csv(path,engine = "python" ,encoding="utf8")
        else:
            errorStock_array.append(code)
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


    ETF_df = pd.DataFrame()

    for code in columns_unique_array:
        
        code = str(code)
        
        temp = pd.DataFrame()
        temp = pd.read_csv("PredictStockDataDif/" + code + "_dif.csv",encoding="utf8")
        
        if code == columns_unique_array[0]:
            #初回のみETF_dfにindexを設定
            ETF_df["Date"] = temp["Date"]
            ETF_df = ETF_df.set_index("Date")
            
        if code =="1321":
            for dateIndex in range(0,len(temp.index)-1):
                tempDate = temp.at[dateIndex,"Date"]
                    
                tempClose = temp.at[dateIndex+1,"Close"]
                if tempClose >= 0:
                    ETF_df.at[tempDate,"nextDay_HighLow"] = 1
                else:
                    ETF_df.at[tempDate,"nextDay_HighLow"] = -1
                    
        for dateIndex in temp.index:
            tempDate = temp.at[dateIndex,"Date"]
                
            ETF_df.at[tempDate,code + "Open"] = temp.at[dateIndex,"Open"]
            ETF_df.at[tempDate,code + "High"] = temp.at[dateIndex,"High"]
            ETF_df.at[tempDate,code + "Low"] = temp.at[dateIndex,"Low"]
            ETF_df.at[tempDate,code + "Close"] = temp.at[dateIndex,"Close"]
            ETF_df.at[tempDate,code + "Volume"] = temp.at[dateIndex,"Volume"]/10000
            
    ETF_df1 = ETF_df[Xcolumns1]
    ETF_df2 = ETF_df[Xcolumns2]
    ETF_df3 = ETF_df[Xcolumns3]

    ETF_df1 = ETF_df1.fillna(0)
    ETF_df2 = ETF_df2.fillna(0)
    ETF_df3 = ETF_df3.fillna(0)

    clf1 = pickle.load(open("max_clf1.sav","rb"))
    pred1 = clf1.predict(ETF_df1)

    clf2 = pickle.load(open("max_clf2.sav","rb"))
    pred2 = clf2.predict(ETF_df2)

    clf3 = pickle.load(open("max_clf3.sav","rb"))
    pred3 = clf3.predict(ETF_df3)

    pred = 0

    if pred1[1]+pred2[1]+pred3[1] > 0:
        pred = 1
    else:
        pred = -1

    return pred

