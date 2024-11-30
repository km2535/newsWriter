# 1. Python 이미지를 베이스로 사용 (필요한 Python 버전에 맞게 수정)
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    zlib1g-dev \
    libjpeg-dev \
    libxml2-dev \
    libxslt1-dev \
    libcurl4-openssl-dev \
    libicu-dev \
    libsqlite3-dev \
    locales \
    && rm -rf /var/lib/apt/lists/*


# 2. 작업 디렉터리 설정
WORKDIR /app

# 3. 현재 디렉터리의 모든 파일을 컨테이너로 복사
COPY . .

# 4. .env 파일을 복사하여 컨테이너 내의 /app 디렉토리로 전달
COPY .env /app/.env

# 5. 의존성 설치 (필요한 라이브러리를 requirements.txt에 명시)
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python", "batchpy.py"]
