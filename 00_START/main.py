from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from typing import List

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float

def get_item_from_db(id):
    # 매우 간단한 아이템 반환
    return {
        "name": "Simple Item", 
        "description": "A simple item description", 
        "price": 50.0,
        "dis_price": 45.0
    }
  
@app.get("/items/{item_id}", response_model=Item) # 반환 모델로 Item을 지정 그려면 반환값에 dis_price는 안들어감 
def read_item(item_id: int):
    item = get_item_from_db(item_id)
    return item



# 유니온 응답 모델 여러 가능한 모델 중 하나를 반환 할 수 있는 유니온 타입을 사용하는 모델

class Cat(BaseModel):
    name: str

class Dog(BaseModel):
    name: str

@app.get("/animal/", response_model=Union[Cat, Dog])
async def get_animal(animal: str): # 쿼리 파라미터를 받아서 알맞은 모델로 반환
    if animal == "cat":
        return Cat(name="Whiskers") #모델에 멤버 변수이름이랑 맞아야함 안맞으면 오류남
    else:
        return Dog(name="Fido")


# 리스트 응답 모델 예시

class Item(BaseModel):
    name: str

@app.get("/items/", response_model=List[Item])
async def get_items():
    return [{"name": "Item 1"}, {"name": "Item 2"}]
