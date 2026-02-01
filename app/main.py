import nogi_tweet.app.preprocessing as preprocessing
import nogi_tweet.app.tweet_categorize as tweet_categorize
import nogi_tweet.app.tweet_api as tweet_api

def main(query, tweet_cnt):
    print("=======================ツイートの取得を開始します。=======================")
    save_file_path, all_tweets = tweet_api.get_tweet(query, tweet_cnt)
    print(f"=======================ツイートの取得が完了しました。前処理を開始します。=======================")
    df_json = preprocessing.load_and_preprocess_data(save_file_path)
    print("=======================前処理が完了しました。LLMツイート分類を開始します。=======================")
    answer = tweet_categorize.categorize_tweets_with_LLM(df_json)
    print("=======================ツイートの分類が完了しました=======================")
    print(answer)

if __name__ == "__main__":
    main()