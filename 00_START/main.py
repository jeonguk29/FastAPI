from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}

# http://127.0.0.1:8000/items/
'''
1. 경로 매개변수 (Path Parameter)

URL 경로의 일부로 값을 전달

특정 리소스를 식별할 때 주로 사용
'''
@app.get("/items/{item_id}")
def read_item(item_id):
    return {"item_id": item_id}


# http://127.0.0.1:8000/items/?skip=5&limit=12
'''
2. 쿼리 파라미터 (Query Parameter)

URL 경로 끝에 ?key=value 형식으로 붙는 값

옵션/필터링/검색 등에 주로 사용
'''
@app.get("/items/")
def read_items(skip = 0, limit = 10):
    return {"skip": skip, "limit": limit}