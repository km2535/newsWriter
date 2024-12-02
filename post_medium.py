import os

import httpx
from dotenv import load_dotenv

load_dotenv()

MEDIUM_API_BASE_URL = os.getenv('MEDIUM_API_BASE_URL')
MEDIUM_INTEGRATION_TOKEN = os.getenv('MEDIUM_INTEGRATION_TOKEN')

def post_to_medium(title, content, tags=None, publish_status="public"):
    print("Posting to Medium...")
    headers = {
        "Authorization": f"Bearer {MEDIUM_INTEGRATION_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # 사용자 정보 가져오기
    response = httpx.get(f"{MEDIUM_API_BASE_URL}/me", headers=headers)
    response.raise_for_status()  # 요청 실패 시 예외 발생
    user_id = response.json()["data"]["id"]

    # 게시물 데이터 설정
    post_data = {
        "title": title,
        "contentFormat": "html",
        "content": content,
        "tags": tags or [],
        "publishStatus": publish_status,
    }

    # Medium에 게시 요청
    post_response = httpx.post(
        f"{MEDIUM_API_BASE_URL}/users/{user_id}/posts",
        json=post_data,
        headers=headers,
    )
    post_response.raise_for_status()

    return post_response.json()["data"]["url"]

