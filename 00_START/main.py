from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

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
