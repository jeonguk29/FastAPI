from passlib.context import CryptContext
from database import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# password 해싱 처리, 유효성 검사 메서드
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 세션 자동 연결 및 해제 메서드
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
