# Python 베이스 이미지 선택
FROM python:3.10

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY . /app

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 애플리케이션 실행
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:6000"]
