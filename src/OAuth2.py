from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
import bcrypt
from dataclasses import dataclass

from . schemas import TokenData, UserInDB, User


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
#SECRET_KEY = "43e61b68530d3f034fff2ff95b9c697747db8db7495edf6aece88460dbed5964"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "Toxa": {
        "username": "Toxa",
        "full_name": "Toxa Kartoxa",
        "email": "Toxa@example.com",
        "hashed_password": "$2y$12$g7a144VcLEGwwmf7c91MTOM4nRXwVgG6O3kjg4GDliGSQB8HOqt62", # aboba
#        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#        "hashed_password": "$2y$12$ZQyuXctTJDIWOLmLVJQHCuizbhFNS611j2KYWHL/fYrfiyn98RWVS",
        "disabled": False,
    }
}

################################################################
#             Решение конфликта passlib с bcrypt 4.1.x

@dataclass
class SolveBugBcryptWarning:
 __version__: str = getattr(bcrypt, "__version__")

setattr(bcrypt, "__about__", SolveBugBcryptWarning())

################################################################

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

####################################################################################

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Check if the provided password matches the stored password (hashed)
# def verify_password(plain_password, hashed_password):
#     password_byte_enc = plain_password.encode('utf-8')
#     return bcrypt.checkpw(password = password_byte_enc, hashed_password = hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user