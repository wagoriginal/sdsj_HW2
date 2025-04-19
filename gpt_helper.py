from openai import OpenAI

# model="deepseek/deepseek-v3-base:free"

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)


def get_advice_from_openrouter(weather_text):
    prompt = f"""
    当前天气情况如下：
    {weather_text}

    请根据天气给出合理的穿衣建议以及运动建议，针对大学生。
    """
    try:
        response = client.chat.completions.create(
            model="qwen/qwen-2.5-vl-7b-instruct",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ 无法获取建议（API错误）：{e}"
