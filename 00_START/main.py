from fastapi import FastAPI, Body

app = FastAPI()

@app.post("/items/")
def create_item(item: dict = Body(...)): #보낼때 해당 바디에 이 값이 필수다라고 선언 스웨거에서도 확인 가능함
    return {"item": item}

#Body 클래스는 Post, Put 방식에 적합함 


@app.post("/advanced_items/")
def create_advanced_item(item: dict = Body(
    default=None, 
    example={"key": "value"}, 
    alias="item_alias", 
    title="Sample Item", 
    description="This is a sample item", 
    deprecated=False)):
    return {"item": item}


@app.post("/advanced_items_2para/")
def create_advanced_item(
    item: dict = Body(
        default=None,
        example={"key": "value"},
        alias="item_alias",
        title="Sample Item",
        description="This is a sample item",
        deprecated=False
    ),
    additional_info: dict = Body(
        default=None,
        example={"info_key": "info_value"},
        title="Additional Info",
        description="This is some additional information about the item",
        deprecated=False
    )
):
    return {
        "item_alias": item,
        "additional_info": additional_info
    }