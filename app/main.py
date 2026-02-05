import app.dynamo_write as dynamo_write
import app.tweet_categorize as tweet_categorize
import app.get_news as get_news
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Nogizaka46 Related Tweet Categorization API", "status": "healthy"}

"""
@app.get("/predict")
def main(query,tweet_cnt :int = Query(10, ge=1, le=100)):
    try:
        print("=======================ツイートの取得を開始します。=======================")
        save_file_path, all_tweets = tweet_api.get_tweet(query, tweet_cnt)
        print(f"=======================ツイートの取得が完了しました。前処理を開始します。=======================")
        df_json = preprocessing.load_and_preprocess_data(save_file_path)
        print("=======================前処理が完了しました。LLMツイート分類を開始します。=======================")
        answer = tweet_categorize.categorize_tweets_with_LLM(df_json)
        print("=======================ツイートの分類が完了しました=======================")
        print(answer)
        return answer
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
"""