import resultStock
import postTweet
import pandas as pd
from datetime import datetime, date, timedelta

result_df = resultStock.resultStock()

#

pred = ""
hitRate = ""
sumValue = ""

if pred > 0:
    pred = "当たり！"
else:
    pred = "ハズレ・・・"

    
db = pd.read_csv("dataBase.csv",encoding="utf8")
tweet = predDayMinus1 + "の予想は「" + pred + "」です。" + "正答率は「" + hitRate + "」です。" + "利益は「" + sumValue +"」です。"

#dataCount,predictDate,predict,hit,hitRate,differenceValue,sumValue,updateDate
#ツイートメソッド呼び出し
tweetResult = postTweet.postTweet(tweet)
