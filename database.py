from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from model import TrainerImage, Trainer
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

async def fetch_trainers_by_keyword(keyword: str, db: AsyncSession):
    # trainer_image 테이블에서 resume 필드로만 키워드 조회
    query_image = select(TrainerImage).where(
        TrainerImage.resume.ilike(f"%{keyword}%")
    )
    result_image = await db.execute(query_image)
    trainers_from_image = result_image.scalars().all()

    # trainers 테이블에서 name과 gender 필드로 키워드 조회
    query_trainers = select(Trainer).where(
        Trainer.gender.ilike(f"%{keyword}%") | Trainer.name.ilike(f"%{keyword}%")
    )
    result_trainers = await db.execute(query_trainers)
    trainers_from_trainers = result_trainers.scalars().all()

    # 두 테이블에서 가져온 데이터를 하나로 합침
    trainers_data = [
        {
            "trainer_number": trainer.trainer_number,
            "resume": trainer.resume
        }
        for trainer in trainers_from_image
    ] + [
        {
            "trainer_number": trainer.trainer_number,
            "name": trainer.name,
            "gender": trainer.gender
        }
        for trainer in trainers_from_trainers
    ]
    
    return trainers_data