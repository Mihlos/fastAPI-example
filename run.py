from fastapi import FastAPI
from models.user import User
from models.book import Book


app = FastAPI()


@app.get("/hello")
async def hello_world():
    return {"Hello FastAPI world!"}


@app.post("/user")
async def post_user(user: User):
    return {"request body": user}


# Parameters
@app.get("/user")
async def get_user_validation(password: str):
    return {"query parameter": password}


# Difference with previous param is:
# In this one is a value in the url.
@app.get("/book/{isbn}")
async def get_book_with_isbn(isbn: str):
    return {"query changable param": isbn}