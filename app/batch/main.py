import app.batch.dynamo_write as dynamo_write
import app.batch.get_news as get_news
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

news_df = get_news.get_news()
dynamo_write.dynamo_batch_write(news_df, table_name='ai_news')
print(news_df)
print("DynamoDBへの書き込みが完了しました。")