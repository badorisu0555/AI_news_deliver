from app.api import get_dynamod_data
from app.api import news_summary
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import decimal

def decimal_to_native(obj):
    if isinstance(obj, decimal.Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    if isinstance(obj, list):
        return [decimal_to_native(item) for item in obj]
    if isinstance(obj, dict):
        return {key: decimal_to_native(value) for key, value in obj.items()}
    return obj

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "AI news summary API healthy", "status": "healthy"}

@app.get("/predict")
def main(days=7,table_name='ai_news'):
    try:
        print("=======================ニュースデータの取得を開始します。=======================")
        news_data = get_dynamod_data.get_dynamo_data(days=days, table_name=table_name)
        news_data = decimal_to_native(news_data)
        print(f"=======================ニュースデータの取得が完了しました。=======================")
        print(news_data)
        print("=======================ニュースの要約を開始します。=======================")
        summary = news_summary.summarize_news_with_LLM(news_data)
        print("=======================ニュースの要約が完了しました。=======================")
        print(summary)
        return JSONResponse(content={"summary": summary})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
