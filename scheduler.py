import datetime
import schedule
import time
import asyncio
from ollama_api import summarize_sections
from post_to_medium import post_to_medium
from scraper import NewsSummaryService

# 비동기 작업 함수
async def run_job(period):
    news_service = NewsSummaryService()
    news_data = news_service.scrape_news()  # 뉴스 스크래핑
    summarized_data = await summarize_sections(news_data)  # 뉴스 요약

    # 모든 요약된 내용을 하나의 문자열로 합치기
    combined_content = "\n\n".join(
        f"<h2>{item['title']}</h2>\n<p>{item['content']}</p>"
        for item in summarized_data
    )

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    # 시간대에 따른 제목 설정
    title = f"Daily News Summary ({current_date} - {period} 요약)"

    # Medium에 게시
    medium_post_link = post_to_medium(
        title=title,
        content=combined_content
    )

# 비동기 작업을 schedule로 등록하는 함수
def schedule_job():
    # asyncio.create_task()를 사용하여 비동기 작업을 실행
    schedule.every().day.at("05:00").do(lambda: asyncio.create_task(run_job("오전 5시")))
    schedule.every().day.at("17:00").do(lambda: asyncio.create_task(run_job("오후 5시")))

# 최초 1회 실행 (오전 5시 요약)
asyncio.run(run_job("오전 5시"))

# 스케줄 작업 등록
schedule_job()

# 스케줄 작업 실행 대기
while True:
    schedule.run_pending()
    time.sleep(1)
