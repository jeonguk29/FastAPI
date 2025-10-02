from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/info/")
def read_info(info: str = Query(None, description="정보를 입력해 주세요.")):
    return {"info": info}

@app.get("/items/")
def read_items(
    # regex는 지금 정규 표현식이 들어가있 맨앞부터 맨뒤는 알파뱃만 가능하고 +는 하나 이상을 의미함
    string_query: str = Query(default="default value", min_length=2, max_length=5, regex="^[a-zA-Z]+$", title="String Query", example="abc"),
    number_query: float = Query(default=1.0, ge=0.5, le=10.5, title="Number Query", example=5.5)
    # ge는 >= le는 <=를 이야기함 
):
    return {
        "string_query_handled": string_query,
        "number_query_handled": number_query
    }

'''
이렇게 요청에서 파라미터들을 제어 할 수 있는 것이 Query 클래스
HTTP Request
- Packet: header/body
- header options
 - URL parameters(in GET)

body
 - parameters(in Post)
'''