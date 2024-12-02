import datetime
import time
import asyncio
import schedule
import httpx
from ollama_api import summarize_sections
from post_medium import post_to_medium
from scraper import NewsSummaryService
from email_service import send_email


async def run_job(period):
    news_service = NewsSummaryService()
    news_data = news_service.scrape_news()  # 뉴스 스크래핑
    summarized_data = await summarize_sections(news_data)  # 뉴스 요약

    combined_content = "\n\n".join(
        f"<h2>{item['title']}</h2>\n<p>{item['content']}</p>"
        for item in summarized_data
    )

    first_summary = (
        f"<h2>{summarized_data[0]['title']}</h2>\n<p>{summarized_data[0]['content']}</p>"
        if summarized_data else "<p>No content available.</p>"
    )

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    title = f"일일 뉴스 요약 리포트 ({current_date} - {period} 요약)"

    try:
        # Medium에 게시
        medium_post_link = post_to_medium(title=title, content=combined_content)
        print(f"Post published: {medium_post_link}")

        # Medium 게시 성공 시 이메일 발송
        email_subject = f"{title} - Medium Post"
        email_body = f"""
        <html>
        <body>
            <h1>{title}</h1>
            <p>주인님! 다음 첫 번째 요약 글 입니다. :</p>
            {first_summary}
            <p> Medium 에서 확인 해주세요.: <a href="{medium_post_link}">{medium_post_link}</a></p>
        </body>
        </html>
        """
        send_email(email_subject, email_body)
        print("Email sent successfully")

    except httpx.HTTPStatusError as e:
        print(f"Failed to post to Medium: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print(f"Post published")

def run_async_job(period):
    asyncio.run(run_job(period))

def schedule_job_test():
    schedule.every().day.at("05:00").do(run_async_job, "오전 5시")
    schedule.every().day.at("17:00").do(run_async_job, "오후 5시")
    # schedule.every(10).seconds.do(run_async_job, "테스트 요약")  # 테스트 용 30초 간격

# 최초 1회 실행 (오전 5시 요약)
asyncio.run(run_job("오전 5시"))

# 스케줄 작업 등록
schedule_job_test()

# 스케줄 작업 실행 대기
while True:
    schedule.run_pending()
    time.sleep(1)
