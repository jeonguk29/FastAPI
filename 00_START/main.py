from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

class Item(BaseModel):
    # 각각의 속성 값에 대하여 세밀하게 지정
    name: str = Field(..., title="Item Name", min_length=2, max_length=50)
    description: str = Field(None, description="The description of the item", max_length=300)
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tag: List[str] = Field(default=[], alias="item-tags")
    '''
    description, title은 스웨거에서는 안보이지만 redoc에 가면 표시가 됨 
    필드 안에 ...는 반드시 있어야 하는 값을 말하며
    None은 없어도 된다, default는 빈리스트가 들어간다.

    숫자에서 gt, lt 숫자 필드 값 제안 초과, 미만 만약 이상 이하 쓸거면 gte, lte
    '''

@app.post("/items/")
async def create_item(item: Item):
    return {"item": item.dict()}

# 실행: uvicorn main:app --reload