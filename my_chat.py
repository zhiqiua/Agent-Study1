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
        {"role": "user", "content": "你好，你能为我做什么？"},
    ],
    extra_body={
        "thinking":{
            "type": "enabled"
        }
    }
)
print(response.choices[0].message.content)
#rprint(response)





