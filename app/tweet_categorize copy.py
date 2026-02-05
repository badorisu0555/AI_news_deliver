import pandas as pd
import boto3
import json
from botocore.exceptions import ClientError
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

def load_api_key():
    load_dotenv(dotenv_path="./.env", override=True)
    os.environ["AWS_BEARER_TOKEN_BEDROCK"] = os.getenv("Bedrock_API_Key")

def create_response(prompt_text,df_json):
    client = boto3.client(
        "bedrock-runtime",
        region_name="us-east-1"
    )

    prompt = PromptTemplate(
        input_variables=["tweet_data"],
        template = prompt_text)
    prompt = prompt.format(tweet_data=df_json)

    body = json.dumps({
        "messages":[
            {"role":"user","content":prompt}
        ],
        "max_tokens":1024,
        "temperature":0.5,
        "anthropic_version":"bedrock-2023-05-31"
        
    })

    model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    response = client.invoke_model(
        modelId=model_id,
        body=body
    )

    return response

# LLMを使ってツイートを分類する関数
def categorize_tweets_with_LLM(df_json):
    load_api_key()

    f = open("app/prompt.txt","r",encoding="utf-8")
    prompt_text = f.read()
    response = create_response(prompt_text,df_json)

    response_body = json.loads(response.get("body").read())
    answer = response_body["content"][0]["text"]
    return answer

