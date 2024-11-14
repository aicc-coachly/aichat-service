from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from model import UserInbody  # UserInbody 모델 가져오기

# 기존 코드 유지
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from db_setup import engine, Base
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

# 사용자 인바디 정보를 데이터베이스에서 조회하는 함수
async def get_user_inbody_from_db(user_id: int, db: AsyncSession):
    try:
        # user_id에 해당하는 인바디 정보를 UserInbody 테이블에서 조회
        query = select(UserInbody).where(UserInbody.user_number == user_id)
        result = await db.execute(query)
        user_inbody = result.scalars().first()

        # 인바디 정보가 없으면 None 반환
        if not user_inbody:
            print(f"사용자 {user_id}의 인바디 정보를 찾을 수 없습니다.")
            return None

        # 필요한 인바디 정보를 딕셔너리 형태로 반환
        return {
            "user_height": user_inbody.user_height,
            "user_weight": user_inbody.user_weight,
            "user_body_fat_percentage": user_inbody.user_body_fat_percentage,
            "user_body_fat_mass": user_inbody.user_body_fat_mass,
            "user_muscle_mass": user_inbody.user_muscle_mass,
            "user_metabolic_rate": user_inbody.user_metabolic_rate,
            "user_abdominal_fat_amount": user_inbody.user_abdominal_fat_amount,
            "user_visceral_fat_level": user_inbody.user_visceral_fat_level,
            "user_total_body_water": user_inbody.user_total_body_water,
            "user_protein": user_inbody.user_protein,
            "user_measurement_date": user_inbody.user_measurement_date
        }
    except Exception as e:
        print(f"데이터베이스에서 인바디 정보를 조회하는 중 오류 발생: {e}")
        return None
