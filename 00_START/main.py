from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/jjk")
def read_jjkHi():
    return {"message": "Hello, jjk!"}