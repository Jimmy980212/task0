import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)  # 如果你在 .env 里放了 HF_TOKEN

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],   # 或直接写 "hf_xxx"
)

try:
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b:groq",
        messages=[
            {
                "role": "user",
                "content": "What is the capital of France?",
            },
        ],
    )
    print("✅ 调用成功：",  completion.choices[0].message.content)
except Exception as e:
    print("❌ 调用失败：", e)
