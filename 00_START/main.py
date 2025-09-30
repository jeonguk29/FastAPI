from fastapi import FastAPI, Query
from typing import List, Dict

app = FastAPI()

'''
Query 는 쿼리 매개변수의 기본값 설정 및 유효성 검사에 사용됩니다. Query([) 는 매개변수가 필수가 아니며, 기본값 으로 빈 리스트를 설정합니다.
List 타입 힌트는 반드시 Query0 와 함께 사용해야 합니다

async를 씀으로서 비동기를 명시 await과 같이써야 비동기 작업이 가능함 이것만으로는 비동기 작업을 할 수 있는건 아님
관습적으로 쓰는 경우도 종종 있음
'''
@app.get("/items/")
async def read_items(q: List[int] = Query([])):
    return {"q": q}

@app.post("/create-item/")
async def create_item(item: Dict[str, int]):
    return item
