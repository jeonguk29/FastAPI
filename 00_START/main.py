from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/user/{username}")
def get_user(request: Request, username: str):
    return templates.TemplateResponse("index.html", {"request": request, "username": username})
  
@app.get("/safe")
def read_root_safe(request: Request):
    my_variable_with_html = "<h1>Hello, FastAPI!</h1>"
    return templates.TemplateResponse("index_with_safe.html", {"request": request, "my_variable_with_html": my_variable_with_html})

@app.get("/greet")
def greeting(request: Request, time_of_day: str):
    return templates.TemplateResponse("conditional.html", {"request": request, "time_of_day": time_of_day})

@app.get("/items")
def read_items(request: Request):
    my_items = ["apple", "banana", "cherry"]
    return templates.TemplateResponse("loop.html", {"request": request, "items": my_items})


# http://127.0.0.1:8000/dynamic_items/?item_list=사과,바나나,체리
@app.get("/dynamic_items/")
def dynamic_items(request: Request, item_list: str = ""):
    items = item_list.split(",")
    return templates.TemplateResponse("loop.html", {"request": request, "items": items})

@app.get("/inherit")
def template_inherit(request: Request):
    my_text = "FastAPI와 Jinja2를 이용한 예시입니다."
    return templates.TemplateResponse("inherit.html", {"request": request, "text": my_text})