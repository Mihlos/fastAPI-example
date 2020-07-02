from fastapi import FastAPI, Body, Header, File, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm

from models.user import User
from models.author import Author
from models.book import Book
from models.jwt_user import JwtUser
from utils.security import authenticate_user, create_jwt_token, check_jwt_token


# Openapi_prefix deprecated. Use root_path, v2 with root_path
app_v1 = FastAPI(openapi_prefix="/v1")


@app_v1.get("/hello")
async def hello_world():
    return {"Hello FastAPI world!"}


# Return a choosen status
@app_v1.post("/user", status_code=HTTP_201_CREATED)
async def post_user(user: User):
    return {"request body": user}


@app_v1.post("/userheader")
async def post_user_header(user: User, x_custom: str = Header("default")):
    return {"request body": user, "custom header": x_custom}


# Parameters
@app_v1.get("/user")
async def get_user_validation(password: str):
    return {"query parameter": password}


# Difference with previous param is:
# In this one is a value in the url.
@app_v1.get("/book/{isbn}")
async def get_book_with_isbn(isbn: str):
    return {"query changable param": isbn}


# Returning a model including or excluding parameters
@app_v1.get("/bookmodel/{isbn}", response_model=Book, response_model_exclude=["author"])
async def get_book_model_with_isbn(isbn: str):
    author_dict = {"name": "Author1", "book": ["book10", "book20"]}
    author1 = Author(**author_dict)

    book_dict = {"isbn": "2", "name": "Libro de madre", "author": author1, "year": 2019}
    book1 = Book(**book_dict)

    return book1


@app_v1.get("/author/{id}/book")
async def get_authors_books(id: int, category: str, order: str = "asc"):

    return {"query params": order + category + str(id)}


# Passing values in body with JSON format
# embed= True required.
# If you want info in the body that isn't a class you need
# Body()
@app_v1.patch("/author/name")
async def patch_author_name(name: str = Body(..., embed=True)):
    return {"name in body": name}


# Multiple parameters
@app_v1.post("/user/author")
async def post_user_and_author(user: User, author: Author):
    return {"user": user, "author": author}


# Add headers to parameters
@app_v1.post("/user/photo")
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    response.headers["x-file-size"] = str(len(profile_photo))
    response.set_cookie(key="cookie-api", value="test")
    return {"file size": len(profile_photo)}


@app_v1.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt_user_dict = {"username": form_data.username, "password": form_data.password}
    jwt_user = JwtUser(**jwt_user_dict)

    user = authenticate_user(jwt_user)

    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    jwt_token = create_jwt_token(user)
    return {"token": jwt_token}
