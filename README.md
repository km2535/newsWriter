# 뉴스 자동 수집기
- 뉴스를 자동으로 오전 5시, 오후 5시에 수집합니다.

## 개발 목적 
- 바쁜 현대인을 위한 뉴스 요약 블로그 글 자동 생성

## 차별점
- 모든 카테고리를 하나의 블로그에 압축 요약

## 개발 일정
- 2024.11.01 ~ 2024.11.30 (약 30일)

## 처리과정
- 파이썬 스케줄러를 통해 매일 오전 4시, 오후 4시에 뉴스를 파이썬 뷰티풀숩을 이용하여 스크랩핑
- Ollama api를 통하여 AI모델 Gemma를 이용해 섹션별 3줄 요약 하기 
- 세션별로 요약된 데이터로 하나의 변수로 만들기
- Medium API를 이용하여 글 작성하기
- 글 작성 완료 시 이메일로 블로그 등록 보내기

## 장점
- 자동으로 블로그 글을 작성할 수 있습니다.
- 전체 뉴스 기사를 한눈에 볼 수 있습니다.
- 뉴스의 영문판으로 확인 할 수 있습니다.

## 단점
- 사용자가 직접 조작할 수 있는 것이 없습니다.
  (모든 것은 자동으로 처리)

## 향후 계획
- 매일 오전, 오후 자동으로 뉴스를 요약해서 컨텐츠를 제공하기 때문에 뉴스를 통한 인사이트를 쉽게 얻을 수 있습니다. 또한 한국 뉴스를 한눈에 요약하고 영어로 번역에서 판매가 가능합니다. 

## 향후 계획
- 음성기술도 추가해서 요약된 뉴스를 읽어주는 기능도 추가
- 스크랩 대상 뉴스 컨텐츠 확장
- 다양한 언어로 번역

## 사용 방법
- git clone "https://github.com/km2535/newsWriter.git"
- .env 추가 
  - example.env --> 미디움 토큰으로 수정
  - 미디움 -> settings -> Security and apps -> Integration tokens
- ollama 다운
  - 해당 프로젝트에서 ai 모델은 gemma2:9b 사용 
- phython scheduler
- 도커로 실행시 
  ```bash
    sudo docker run -d --name batchpy_scheduler_container --add-host=host.docker.internal:host-gateway speech2/auto_news_summary:amd  
  ```