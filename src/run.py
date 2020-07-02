from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED

from routes.v1 import app_v1
from routes.v2 import app_v2
from utils.security import check_jwt_token, authenticate_user, create_jwt_token
from utils.const import TOKEN_DESCRIPTION, TOKEN_SUMMARY
from models.jwt_user import JwtUser


app = FastAPI(
    title="Bookstore API Documentation", version="0.1", description="FastAPI example"
)

app.include_router(app_v1, prefix="/v1", dependencies=[Depends(check_jwt_token)])
app.include_router(app_v2, prefix="/v2", dependencies=[Depends(check_jwt_token)])


@app.post(
    "/token", description=TOKEN_DESCRIPTION, summary=TOKEN_SUMMARY,
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt_user_dict = {"username": form_data.username, "password": form_data.password}
    jwt_user = JwtUser(**jwt_user_dict)

    user = authenticate_user(jwt_user)

    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    jwt_token = create_jwt_token(user)
    # The name access_token is a rule ! (Required for Swagger)
    return {"access_token": jwt_token}


# In middleware frasing is not allowed
@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()
    # modify request
    if not any(word in str(request.url) for word in ["/token", "/docs", "/openapi"]):
        try:
            jwt_token = request.headers["Authorization"].split("Bearer ")[1]
            is_valid = check_jwt_token(jwt_token)
        except Exception as e:
            is_valid = False
        if not is_valid:
            return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)

    response = await call_next(request)
    # modify response
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["x-execution-time"] = str(execution_time)
    return response
