from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from model import TrainerImage
from sqlalchemy.future import select
from db_setup import engine, Base  # db_setup에서 engine과 Base 가져오기
import os

# 환경 변수 로드
load_dotenv()

# 비동기 세션 팩토리 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

# 데이터베이스 세션을 가져오는 종속성
async def get_db():
    async with SessionLocal() as session:
        yield session

# 트레이너 데이터를 가져오는 함수
async def fetch_trainers_data(trainer_numbers: list[int], db: AsyncSession):
    query = select(TrainerImage).where(TrainerImage.trainer_number.in_(trainer_numbers))
    result = await db.execute(query)
    trainers_data = result.scalars().all()

    # 필요한 데이터를 딕셔너리로 변환
    trainers_data_dict = [
        {"trainer_number": trainer.trainer_number, "name": trainer.name, "trainer_resume": trainer.resume}
        for trainer in trainers_data
    ]
    
    return trainers_data_dict
