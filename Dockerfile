# Python 베이스 이미지 선택
FROM python:3.10

# 작업 디렉토리 설정
WORKDIR /app

# pip 업그레이드
RUN pip install --upgrade pip

# requirements.txt만 먼저 복사해서 의존성 설치
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt -v

# 나머지 코드 복사
COPY . /app

# FastAPI 애플리케이션 실행
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:6000"]
