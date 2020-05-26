def get_day_of_week_jp(dt):
    w_list = ['月', '火', '水', '木', '金', '土', '日']
    return(w_list[dt.weekday()])

import predictStock
import resultStock
import sys
import postTweet
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta

db = pd.read_csv("dataBase.csv",encoding="utf8",index_col='predictDate')

#日付準備
thisDay = datetime.today()
#デバッグ用
# thisDay -= timedelta(days=2)

thisDay_Formated = datetime.strftime(thisDay,'%Y-%m-%d')
thisDay_OfTheWeek = get_day_of_week_jp(thisDay)

if not thisDay_Formated in db.index:
    #非営業日のため実行終了
    sys.exit()

nextDay = thisDay + timedelta(days=1)
nextDay_Formated = datetime.strftime(nextDay,'%Y-%m-%d')
nextDay_OfTheWeek = get_day_of_week_jp(nextDay)

previousDay_Formated = db.index[-2]

holiday_df = pd.read_csv("holiday.csv",encoding="utf8")
holiday_array = holiday_df.values

#次営業日
while nextDay_OfTheWeek == "土" or nextDay_OfTheWeek == "日" or nextDay_Formated in holiday_array:
    nextDay = nextDay + timedelta(days=1)
    nextDay_Formated = datetime.strftime(nextDay,'%Y-%m-%d')
    nextDay_OfTheWeek = get_day_of_week_jp(nextDay)

#前日した予想
thisDay_predict = db.loc[thisDay_Formated, 'predict']
if thisDay_predict == 1:
    thisDay_predict_str = "陽線"
else:
    thisDay_predict_str = "陰線"


#次の日の予想
nextDay_predict = predictStock.predictStock()
#今日の1321の結果
df_1321 = resultStock.resultStock()

if nextDay_predict > 0:
    nextDay_predicd_str = "陽線"
else:
    nextDay_predicd_str = "陰線"


#的中判定
closeValue = df_1321.loc[thisDay_Formated,"Close"]
openValue = df_1321.loc[thisDay_Formated,"Open"]
differenceValue = closeValue - openValue
if differenceValue >= 0:
    thisDay_predict_Result = "陽線"
else:
    thisDay_predict_Result = "陰線"

#的中回数
hitCount = sum(list(db["hit"].fillna(0)))

#総利益
sumValue = db.loc[previousDay_Formated,"sumValue"]

tempValue = (1000000//openValue)*differenceValue

if np.sign(differenceValue * thisDay_predict) == 1 or (differenceValue==0 and thisDay_predict==1):
    #的中
    hit = 1
    todayValue = abs(tempValue)
    thisDay_Predict_Result = "的中"
else:
    #ハズレ
    hit = 0
    todayValue = -1 * abs(tempValue)
    thisDay_Predict_Result = "ハズレ"

hitCount = hitCount + hit
count = len(db.index)
hitRate = 100*hitCount/count
sumValue = sumValue + todayValue
differenceHitRate = hitRate - db.loc[previousDay_Formated,"hitRate"]
hitRate_Formated = '{:.3f}'.format(hitRate) 

tweet = "◆" + nextDay_Formated +"("+ nextDay_OfTheWeek + ")の株価\n  「" + nextDay_predicd_str + "」と予想します。\n \n◆" + thisDay_Formated +"("+ thisDay_OfTheWeek + ")の株価\n   予想「" + thisDay_predict_str + "」、結果「"+ thisDay_predict_Result +"」のため" + thisDay_Predict_Result + "です。\n \n   的中率：" + hitRate_Formated + "%  (前回差：" + '{:+.3f}'.format(differenceHitRate) + "%)  (的中回数：" + '{:.0f}'.format(hitCount) + "/" + str(count) + "回)\n   総利益：" + '{:+,.0f}'.format(sumValue) + "円  (前回差：" + '{:+,.0f}'.format(todayValue) + "円)"

#ツイートメソッド呼び出し
tweetResult = postTweet.postTweet(tweet)
#print(tweet)

thisDay_Detail = datetime.strftime(thisDay,'%Y-%m-%d %H:%M:%S')

db.loc[thisDay_Formated,"hit":"sumValue"] = [hit,hitRate_Formated,differenceValue,sumValue]
db.loc[nextDay_Formated] = [nextDay_predict,"","","","",thisDay_Detail]


db.to_csv("dataBase.csv")