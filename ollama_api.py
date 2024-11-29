import os

import requests
from dotenv import load_dotenv

load_dotenv()
OLLAMA_URL=os.getenv('OLLAMA_URL')

async def summarize_sections(news_data):
    summarized_data = []
    for item in news_data:
        response = requests.post(
            OLLAMA_URL,
            json={"model": "gemma2:9b", "prompt": "다음 기사의 내용을 3개의 한글 문장으로 요약해라, 요약 할 때는 뉴스의 내용 만 한글로 작성해라"
                                                  + item.content, "stream": False}
        )

        # 응답 JSON 데이터를 출력하여 확인
        response_data = response.json()
        print(response_data)  # 응답 데이터를 출력하여 확인

        # 'content' 키가 없으면 다른 키를 확인해야 합니다.
        if "response" in response_data:
            summary = response_data["response"]
        else:
            # content가 없으면 다른 처리를 할 수 있습니다.
            print("No 'content' in response:", response_data)
            summary = "No summary available"

        summarized_data.append({"title": item.title, "content": summary})

    return summarized_data
