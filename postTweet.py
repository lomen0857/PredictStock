def postTweet(tweet):
    
    import sys
    import numpy as np
    import pandas as pd
    import notebookutil as nbu
    sys.meta_path.append(nbu.NotebookFinder())
    import json
    import config
    from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み

    CK = config.CONSUMER_KEY
    CS = config.CONSUMER_SECRET
    AT = config.ACCESS_TOKEN
    ATS = config.ACCESS_TOKEN_SECRET
    twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

    result = ""
    
    url = "https://api.twitter.com/1.1/statuses/update.json" #ツイートポストエンドポイント

    params = {"status" : tweet}

    res = twitter.post(url, params = params) #post送信

    if res.status_code == 200: #正常投稿出来た場合
        result = "Success."
    else: #正常投稿出来なかった場合
        result = "Failed. : %d"% res.status_code
    
    return result
