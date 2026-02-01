import os
import requests
import urllib.parse
import json
from dotenv import load_dotenv
import time

# 環境変数からAPIキーを読み込む関数
def load_api_key():
    load_dotenv(dotenv_path="./.env", override=True)
    api_key = os.getenv("tweet_API_Key")
    return api_key

# ツイートを検索してリストアップする関数
def tweet_search(query,tweet_count,api_key):
    url = "https://api.twitterapi.io/twitter/tweet/advanced_search"
    headers = {"X-API-Key": api_key}

    querystring = {
        "queryType": "Top",
        "query": query
    }

    all_tweets = []
    while len(all_tweets) < tweet_count+1:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        tweets = data.get("tweets", [])
        all_tweets.extend(tweets)
        # 次ページがなければ終了
        if not data.get("has_next_page"):
            break
        # next_cursor をセットして次ページ取得
        querystring["cursor"] = data["next_cursor"]
        # API制限回避
        time.sleep(7)
    return all_tweets

# ツイートをJSONファイルに保存する関数
def save_tweets_to_json(all_tweets):
    save_file_path = "nogizaka_tweets.json"
    with open(save_file_path,"w",encoding="utf-8") as f:
        json.dump(all_tweets,f,ensure_ascii=False,indent=2)
    return save_file_path

# ツイート検索から保存までのメインの処理を行う関数
def get_tweet(query, tweet_cnt):
    api_key = load_api_key()
    all_tweets = tweet_search(query, tweet_cnt,api_key)
    save_file_path = save_tweets_to_json(all_tweets)
    print(f"最終取得件数: {len(all_tweets)}")
    print(f"ツイートを{save_file_path}に保存しました。")
    return save_file_path, all_tweets

if __name__ == "__main__":
    get_tweet()