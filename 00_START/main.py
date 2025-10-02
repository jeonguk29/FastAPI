from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    try:
        if item_id < 0:
            raise ValueError("음수는 허용되지 않습니다.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) #제일 중요한건 에러 코드와 에러 메시지임
    
@app.get("/items2/{item_id}")
def read_item(item_id: int):
    if item_id == 42:
        raise HTTPException(status_code=404, detail="Item not found") # try-except 없이 명시적으로 에러 처리, 에러를 보낼때는 raise를 붙임
    return {"item_id": item_id}
