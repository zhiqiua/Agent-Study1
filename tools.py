import json
from openai import OpenAI
import os
from dotenv import load_dotenv
from rich import print as rprint

load_dotenv()


client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
)

def get_weather(city: str) -> str:
    return f"{city} 晴，24°C"

def get_news(topic: str) -> str:
    return f"{topic}发射火箭"

TOOL_FUNCS = {"get_weather": get_weather, "get_news": get_news}

TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查询某个城市当前天气。用户问天气时使用。",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名，如 北京"}
            },
            "required": ["city"],
        },
    },
}, {
    "type": "function",
    "function": {
        "name": "get_news",
        "description": "查询某个主题的新闻。用户问新闻时使用。",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "主题名，如 科技"}
            },
            "required": ["topic"],
        },
    },
}]

def run(user_input: str, max_steps: int = 5) -> str:
    messages = [
        {"role": "system", "content": "你是一个简洁的助手。"},
        {"role": "user", "content": user_input},
    ]

    for _ in range(max_steps):                       # 死循环保护
        resp = client.chat.completions.create(
            model=os.getenv("MODEL_ID"),
            messages=messages,
            tools=TOOLS,
        )
        msg = resp.choices[0].message
        messages.append(msg)                         # ①
        rprint(msg)
        if not msg.tool_calls:                       # 不再调工具 → 收工
            return msg.content

        for call in msg.tool_calls:                  # ②
            fn = TOOL_FUNCS.get(call.function.name)
            if fn is None:
                content = f"错误：不存在名为 {call.function.name} 的工具"
            else:
                try:
                    content = str(fn(**json.loads(call.function.arguments)))
                except Exception as exc:             # 工具失败也要回话
                    content = f"工具执行失败：{exc}"
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,             # ③
                "content": content,
            })

    return "（达到最大步数，已中止）"

if __name__ == "__main__":
    print(run("北京今天天气怎么样？有哪些新闻？"))