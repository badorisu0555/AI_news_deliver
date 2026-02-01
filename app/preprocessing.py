import pandas as pd
import json
import re
from pprint import pprint
import emoji

#JSONファイルの読み込み
def read_json(json_open):
    json_open = json.load(json_open)

    id = []
    text = []
    viewCount = []
    likeCount = []
    url = []

    for i in range(len(json_open)):
        id.append(json_open[i]["id"])
        text.append(json_open[i]["text"])
        viewCount.append(json_open[i]["viewCount"])
        likeCount.append(json_open[i]["likeCount"])
        url.append(json_open[i]["url"])

    df = pd.DataFrame({
        "id":id,
        "text":text,
        "viewCount":viewCount,
        "likeCount":likeCount,
        "url":url})
    
    return df

#ツイート本文からURLを削除
def remove_url(df):
    df["text"] = df["text"].str.replace("\n","")
    pattern = r'https?://[^\s]+'
    df["text"] = df["text"].apply(lambda x:re.sub(pattern,"",x))
    return df

#ツイート本文から絵文字の削除
def remove_emoji(text):
    return emoji.replace_emoji(text,replace='')

#データの読み込みと前処理の全体実行
def load_and_preprocess_data(file_path):
    json_open = open(file_path,"r",encoding="utf-8")
    df = read_json(json_open)
    df = remove_url(df)
    df["text"] = df["text"].apply(lambda x: remove_emoji(x))
    df_json = df.to_json(orient='records',force_ascii=False)

    return df_json

# 動作確認

if __name__ == "__main__":
    df_json = load_and_preprocess_data("nogizaka_tweets.json")
    pprint(df_json)