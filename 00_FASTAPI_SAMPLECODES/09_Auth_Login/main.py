from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# 세션 미들웨어 추가, 'verysecret'는 실제 사용 시 안전한 키로 교체해야 합니다.
app.add_middleware(SessionMiddleware, secret_key="verysecret")

# 항상 세션 정보를 쓰거나 쓸 가능성이 있는 API는 무조건 Request를 붙여주는게 좋음
@app.post("/login/")
async def login(request: Request, username: str, password: str):
    if username == "john" and password == "1234": #실제 password는 암호화해서 DB에 저장 (해싱 기법등을 사용)
        request.session["username"] = username 
        # 이렇게 세션을 만듬 보이는건 메시지만 리턴해주지만
        # 내부적으로는 세션 ID가 Set Cookie를 통해 전달 되는 것임
        return {"message": "Successfully logged in"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/dashboard/")
async def dashboard(request: Request): # Request에 세션 ID정보가 있을것임 
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="Not authorized")
    return {"message": f"Welcome to the dashboard, {username}"}