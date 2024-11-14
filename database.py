from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 데이터베이스 URL 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")

# 비동기 엔진 생성
engine = create_async_engine(DATABASE_URL, echo=True)

# 비동기 세션 팩토리 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

# Base 클래스 생성
Base = declarative_base()

# 데이터베이스 세션을 가져오는 종속성
async def get_db():
    async with SessionLocal() as session:
        yield session
