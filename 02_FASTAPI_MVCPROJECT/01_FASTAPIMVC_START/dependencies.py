from passlib.context import CryptContext
from database import AsyncSessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# password 해싱 처리, 유효성 검사 메서드
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 세션 자동 연결 및 해제 메서드 - 비동기 변환
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        await session.commit()

'''
보통 파일로 예를 들면 오픈, 처리, 닫기를 해줘야함 (명시적 처리)
with 파일 오픈
    파일 처리 

with 안에서 파일을 열고 파일 처리를 하면 닫기를 명시적으로 하지 않아도
블럭이 다 끝나면 파일을 닫아주는 문법이 with임
await session.close() 이 부분을 명시적으로 안써줘도 된다는 말임
'''