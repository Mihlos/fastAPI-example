from fastapi import FastAPI


app_v2 = FastAPI(root_path="/v2")


@app_v2.get("/hello")
async def hello_world():
    return {"Hello FastAPI v2 world!"}
