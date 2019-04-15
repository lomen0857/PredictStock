import predictStock
import postTweet
import pandas as pd
from datetime import datetime, date, timedelta

pred = predictStock.predictStock()

if pred > 0:
    tweet = "上昇"
else:
    tweet = "降下"


predDay = datetime.today()
predDayFormated = datetime.strftime(predDay,'%Y-%m-%d')
predDayAdd1 = predDay + timedelta(days=1)
predDayAdd1Formated = datetime.strftime(predDayAdd1,'%Y-%m-%d')
predDayAdd1DayOfTheWeek = datetime.strftime(predDayAdd1,'%a')

holiday_df = pd.read_csv("holiday.csv",encoding="utf8")
holiday_array = holiday_df.values

#土日休日判定
while predDayAdd1DayOfTheWeek == "Sat" or predDayAdd1DayOfTheWeek == "Sun" or predDayAdd1Formated in holiday_array:
    predDayAdd1 = predDayAdd1 + timedelta(days=1)
    predDayAdd1Formated = datetime.strftime(predDayAdd1,'%Y-%m-%d')
    predDayAdd1DayOfTheWeek = datetime.strftime(predDayAdd1,'%a')

tweet = predDayAdd1Formated + "の予想は「" + tweet + "」です。"

#ツイートメソッド呼び出し
tweetResult = postTweet.postTweet(tweet)

db = pd.read_csv("dataBase.csv",encoding="utf8",index_col='predictDate')
predDay = datetime.today()

predDayFormated = datetime.strftime(predDay,'%Y-%m-%d')
predDayDetail = datetime.strftime(predDay,'%Y-%m-%d %H:%M:%S')
db.loc[predDayFormated] = [pred,"","","","",predDayDetail]

db.to_csv("dataBase.csv")