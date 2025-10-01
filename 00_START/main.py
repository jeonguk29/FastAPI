from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse, PlainTextResponse

app = FastAPI()

@app.get("/json", response_class=JSONResponse)
def read_json():
    return {"msg": "This is JSON"}


@app.get("/html", response_class=HTMLResponse)
def read_html():
    return "<h1>This is HTML</h1>"


@app.get("/text", response_class=PlainTextResponse)
def read_text():
    return "This is Plain Text"

@app.get("/redirect")
def read_redirect(): #해당 주소로 입력이 들어오면 아래 API로 이동해라 => 최종 보여지는건 /text에 해당하는 반환값
    # 기존 url을 최신 url로 바꿀때 등 다양한 목적으로 사용
    return RedirectResponse(url="/text")
