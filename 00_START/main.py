from fastapi import FastAPI, Query

app = FastAPI()
'''
요청 리퀘스트에 대해 url 즉 쿼리 파라미터를 세밀하게 제어 가능함
'''
@app.get("/users/")
def read_users(q: str = Query(None, max_length=50)): # 쿼리 파라미터를 제어 Pydantic 모델, Field 등과 유사한 기능을 가짐
    return {"q": q}

@app.get("/items/")
def read_items(internal_query: str = Query(None, alias="search")): #외부에서는 search로 보이게 됨 클라 사용 변수와 서버 내부 변수명을 분리하고 싶을때 사용
    return {"query_handled": internal_query}

@app.get("/usersDepre/") # 조만간 지원을 멈출것이라고 명시 (업데이트나 등등 추후 호완성을 위해 표시를 해주는 것)
def read_users(q: str = Query(None, deprecated=True)): # 주소가 없어진다는게 아님 해당 쿼리 파라미터가 없어질것이라고 알려주는 것임
    return {"q": q}