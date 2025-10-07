from fastapi import FastAPI
import asyncio

app = FastAPI()

async def fetch_data():
    await asyncio.sleep(2)
    return {"data": "some_data"}

@app.get("/")
async def read_root():
    data = await fetch_data() #비동기 함수 호출
    return {"message": "Hello, World!", "fetched_data": data}

# 10명이 동시에 접근시 동기 처리시 20초 걸림 (마지막 놈)
# 비동기 처리시 10명 동시에 접근 할때도 2초 걸림