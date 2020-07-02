from fastapi import Body, Header, File, APIRouter
from starlette.status import HTTP_201_CREATED
from starlette.responses import Response

from models.user import User
from models.author import Author
from models.book import Book


app_v1 = APIRouter()


@app_v1.get("/hello")
async def hello_world():
    return {"Hello FastAPI world!"}


# Return a choosen status
@app_v1.post("/user", status_code=HTTP_201_CREATED, tags=["User"])
async def post_user(user: User):
    return {"request body": user}


@app_v1.post("/userheader")
async def post_user_header(
    user: User, x_custom: str = Header("default"), tags=["User"]
):
    return {"request body": user, "custom header": x_custom}


# Parameters
@app_v1.get("/user", tags=["User"])
async def get_user_validation(password: str):
    return {"query parameter": password}


# Difference with previous param is:
# In this one is a value in the url.
@app_v1.get("/book/{isbn}", tags=["Book"])
async def get_book_with_isbn(isbn: str):
    return {"query changable param": isbn}


# Returning a model including or excluding parameters
@app_v1.get(
    "/bookmodel/{isbn}",
    response_model=Book,
    response_model_exclude=["author"],
    tags=["Book"],
)
async def get_book_model_with_isbn(isbn: str):
    author_dict = {"name": "Author1", "book": ["book10", "book20"]}
    author1 = Author(**author_dict)

    book_dict = {"isbn": "2", "name": "Libro de madre", "author": author1, "year": 2019}
    book1 = Book(**book_dict)

    return book1


@app_v1.get("/author/{id}/book", tags=["Book"])
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

