import logging
import requests
from bs4 import BeautifulSoup

# 로거 설정
logger = logging.getLogger(__name__)


class ArticleUrl:
    def __init__(self, url: str, title: str = None, content: str = None):
        self.url = url
        self.title = title
        self.content = content


class NewsSummaryService:
    CATEGORY_URLS = {
        "politics": "https://www.ytn.co.kr/news/list.php?mcd=0101",
        # "economy": "https://www.ytn.co.kr/news/list.php?mcd=0102",
        # "society": "https://www.ytn.co.kr/news/list.php?mcd=0103",
        # "international": "https://www.ytn.co.kr/news/list.php?mcd=0104",
        # "science": "https://www.ytn.co.kr/news/list.php?mcd=0105",
        # "culture": "https://www.ytn.co.kr/news/list.php?mcd=0106",
        # "sports": "https://www.ytn.co.kr/news/list.php?mcd=0107",
        # "nationwide": "https://www.ytn.co.kr/news/list.php?mcd=0115",
    }

    def scrape_news(self) -> list[ArticleUrl]:
        all_articles = []

        for url in self.CATEGORY_URLS.values():  # 모든 카테고리 URL을 순차적으로 처리
            logger.info(f"Scraping news from URL: {url}")
            try:
                response = requests.get(url)
                if response.status_code != 200:
                    raise ValueError(f"Failed to fetch data from {url}. HTTP Status: {response.status_code}")

                soup = BeautifulSoup(response.content, "html.parser")

                for item in soup.find_all("div", class_="title"):
                    a_tag = item.find("a")
                    if a_tag:
                        article_url = a_tag.get("href")
                        article_title = a_tag.get_text(strip=True)
                        article_content = self.fetch_article_content(article_url)  # 제목과 내용을 가져오는 메서드
                        all_articles.append(ArticleUrl(url=article_url, title=article_title, content=article_content))

                logger.info(f"Successfully scraped articles from {url}")

            except Exception as e:
                logger.error(f"Error scraping news from {url}: {str(e)}")

        logger.info(f"Total articles scraped: {len(all_articles)}")
        return all_articles

    def fetch_article_content(self, article_url: str) -> str:
        """기사의 URL을 통해 본문을 가져오는 함수"""
        try:
            response = requests.get(article_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                content = soup.find("div", class_="paragraph")  # 본문이 포함된 HTML 요소
                if content:
                    return content.get_text(strip=True)
            return "Content not available"
        except Exception as e:
            logger.error(f"Error fetching content from {article_url}: {str(e)}")
            return "Error fetching content"


# 사용 예시:
news_service = NewsSummaryService()
all_news_data = news_service.scrape_news()

# 결과 확인
for article in all_news_data:
    print(f"URL: {article.url}, Title: {article.title}, Content: {article.content}")
