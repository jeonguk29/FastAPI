from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# 미들웨어, 시크릿키 추가
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# 세션 정의 
@app.post("/set/")
async def set_session(request: Request):
    request.session["username"] = "john" #세션에 값을 설정
    return {"message": "Session value set"}
    #응답값에 setcookie로 클라이언트 id가 발급 받아서 전달이 된다고 보면 됨

# 세션 정보 가져오기
# 클라이언트 id가 포함되어서 서버에 전송이 되고 서버에서 해독을 해서 특정 세션 정보인지를 확인을하고
# 해당 세션 정보에 들어가있는 username(john)을 가져오는것임
@app.get("/get/")
async def get_session(request: Request):
    username = request.session.get("username", "Guest") #이름이 없으면 기본값 Guest
    return {"username": username}

'''
http는 한번 요청하고 그것에 대한 응답을 받는 형태로만 설계가 되어 있음
HTTP는 Stateless:통신이 끝나면 상태를 유지하지 않는다.

이를 보완하기 위해 쿠기와 세션이 나옴 (로그인 상태 유지 등)
쿠키는 비번과 아이디를 사용자에게 주면 사용자가 가지고 있다가 계속 비번 아이디를 같이 주면서 요청을 보내는 것임
다만 이러면 해커가 탈취할 위험이 있어서 세션이라는게 나왔음
'''