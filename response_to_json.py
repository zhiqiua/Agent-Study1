import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from rich import print as rprint

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
)
response = client.chat.completions.create(
    model = os.getenv("MODEL_ID"),
    messages = [
        {"role": "system",
         "content": '''请把用户输入整理成 JSON
                       只输出 JSON，字段为 topic（字符串）和 keywords（字符串数组）。
                       示例：{"topic":"天气","keywords":["杭州","温度"]}'''
         },
        {"role": "user", "content": "你好，你能为我做什么？"},
    ],
    extra_body={
        "thinking":{
            "type": "enabled"
        }
    },
    response_format={"type": "json_object"},
)
result = response.choices[0].message.content
to_json_result = json.loads(result)
print(to_json_result)
