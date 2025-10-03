from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

'''
static폴더를 등록을 해줘야 templates폴더에서 정적파일 등록해서 사용이 가능함
주로 static폴더 안에 정적 파일(이미지, js, CSS등)을 저장하고
templates 파일에 HTML 템플릿 파일들을 저장함

실무적 활용 및 이점
• 구조적 관리: 파일을 static 과 templates 로 구분하여 웹 애플리케이션의 구조를 명확하게 관리합니다.
• 성능 최적화: FastAPI의 정적 파일 처리 기능은 효율적인 브라우저 캐싱을 지원하여 페이지 로딩 시간을 단축합니다.
• 보안 강화: FastAPI는 정적 파일에 대한 안전한 접근 방식을 제공합니다.

FastAP를 활용하여 정적 파일과 HTML 페이지를 효과적으로 관리하면, 웹 애플리케이션의 성능, 유지보수성, 보안성을 향상시킬 수 있습니다. 
이를 통해 개발자는 웹 애플리케이션을 보다 효율적으로 개발하고 관리할 수 있게 됩니다.
'''
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})