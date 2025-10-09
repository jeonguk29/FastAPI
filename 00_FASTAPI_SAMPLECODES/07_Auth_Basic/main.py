from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "alice" or credentials.password != "password":
        raise HTTPException(status_code=401, detail="Unauthorized") #인증 에러 처리 
    return credentials.username

 #어떤 API는 해당 라우팅 코드처럼 권한이 필요할것임 이때 Depends(get_current_username) 이렇게 해서 유효한지 검사를 할 수 있음
@app.get("/users/me")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}

'''
basic 64방법은 암호화 방법이 아니라서 민감한 정보를 보호하기에는 적합하지 않음, 따라서 현대에서는 많이 사용하지 않음
'''