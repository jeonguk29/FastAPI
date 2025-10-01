from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):  # Pydantic 모델 정의
    name: str
    price: float
    is_offer: bool = None

@app.post("/items/")
def create_item(item: Item):
    return {"item": item.dict()}  # Pydantic 모델을 API에 사용 
'''
반환 값을 사전 형식으로 리턴을 해줌
'''

class Item2(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 0.1

@app.post("/items2/")
async def create_item(item: Item2):
    return {"item": item.dict()}