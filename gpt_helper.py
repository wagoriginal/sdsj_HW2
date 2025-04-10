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

    请根据天气给出合理的穿衣建议以及出行建议，简洁明了即可。
    """
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ 无法获取建议（API错误）：{e}"
