from datetime import datetime, timedelta
import time

from passlib.context import CryptContext
from fastapi import Depends, HTTPException
import jwt
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED

from models.jwt_user import JwtUser
from utils.const import JWT_EXPIRATION_TIME_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"])
oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")

jwt_user1 = {
    "username": "user1",
    "password": "$2b$12$TRV.V62wIZQMTqM056DJBOT/OHR0Ze7EN7cO3Xm6ncAnon0AdzA0K",
    "disable": False,
    "role": "admin",
}
fake_jwt_user1 = JwtUser(**jwt_user1)


def get_hashed_password(password):
    return pwd_context.hash(password)


def verify_password(plain_pass, hashed_pass):
    try:
        return pwd_context.verify(plain_pass, hashed_pass)
    except Exception:
        return False


# Authenticate user
def authenticate_user(user: JwtUser):
    if fake_jwt_user1.username == user.username:
        if verify_password(user.password, fake_jwt_user1.password):
            user.role = "admin"
            return user

    return None


# Create access JWT token
def create_jwt_token(user: JwtUser):
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    jwt_payload = {"sub": user.username, "role": user.role, "exp": expiration}
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return jwt_token


# Check whether JWT token is correct
def check_jwt_token(token: str = Depends(oauth_schema)):
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        username = jwt_payload.get("sub")
        role = jwt_payload.get("role")
        expiration = jwt_payload.get("exp")

        if time.time() < expiration:
            if fake_jwt_user1.username == username:
                return final_checks(username, role)
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


#
def final_checks(username: str, role: str):
    if role == "admin":
        return True
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
