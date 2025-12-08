import os
import time
import requests
import pandas as pd
from openai import OpenAI
from tqdm import tqdm  # ✅ 这样才能用 tqdm(...)
# 这是一个假的 token，请替换成你自己的正确token，并从environment中读取，而非硬编码
from dotenv import load_dotenv
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
#HF_TOKEN = "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"

client = OpenAI(
    api_key=HF_TOKEN,
    # 这里的 base_url 已经过时，请查阅文档改为正确的base_url
    base_url="https://router.huggingface.co/v1",
)

from tenacity import retry, stop_after_attempt, wait_exponential
@retry(stop=stop_after_attempt(3), 
       wait=wait_exponential(multiplier=1, min=4, max=10))
def translate_text(text):  # 用来调用API翻译传入的文本
    model_name = "openai/gpt-oss-120b:fastest"

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                 {"role": "system", "content": """你是一位专业的计算机视觉领域学术翻译专家。
                           请将下面的英文学术论文摘要翻译成中文，要求：
                         1. 保持学术严谨性和专业术语准确性
                         2. 语句流畅自然，符合中文表达习惯
                         3. 保留关键技术术语的英文原文（用括号标注）
                         4. 不要添加任何解释或评论，只输出翻译结果"""},
                 {"role": "user", "content": f"请翻译以下内容：\n\n{text}"}
             ],
            temperature=0.3,          #改：正常范围是 0-2，100 会导致输出完全随机（学术翻译需要稳定性）
            max_tokens=2048,            #改：只生成 20 个 token，根本翻译不完一个摘要
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        raise  # ✅ 重新抛出异常，触发 tenacity 重试机制

def main():
    df = pd.read_csv("papers.csv")
    
    # 修改1：检查 result.csv 是否存在，加载已翻译的 ID
    translated_ids = set()
    if os.path.exists("result.csv"):
        try:
            existing_df = pd.read_csv("result.csv")
            translated_ids = set(existing_df['id'])
            print(f"检测到已翻译 {len(translated_ids)} 篇，将跳过...")
        except:
            pass  # 文件损坏或为空，重新开始
    
    # 如果是第一次运行，写入表头
    if not translated_ids:
        with open("result.csv", "w", encoding="utf-8") as f:
            f.write("id,cn_abstract\n")

    # 修改2：添加 tqdm 进度条
    for index, row in tqdm(df.iterrows(), total=len(df), desc="翻译进度", unit="篇"):
        # 修改3：跳过已翻译的论文（断点续传）
        if row['id'] in translated_ids:
            continue
        
        abstract = row['abstract']
        print(f"Translating paper {index + 1}/{len(df)}: {row['id']}...")

        cn_abstract = translate_text(abstract)

        # 写入结果，处理特殊字符
        with open("result.csv", "a", encoding="utf-8") as f:
            safe_text = cn_abstract.replace('"', '""').replace('\n', ' ')
            f.write(f'{row["id"]},"{safe_text}"\n')
        
        time.sleep(3)
    
    # 修改4：添加完成提示
    print("\n✅ 翻译完成！")


if __name__ == "__main__":
    main()
