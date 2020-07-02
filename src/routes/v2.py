from fastapi import APIRouter


app_v2 = APIRouter()


@app_v2.get("/hello")
async def hello_world():
    return {"Hello FastAPI v2 world!"}
