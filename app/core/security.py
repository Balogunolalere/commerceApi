# auth.py
from datetime import datetime, timedelta
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from core.config import settings
from db import crud, base

# Define the secret key and algorithm for JWT encoding and decoding
JWT_SECRET = settings.secret_key
JWT_ALGORITHM = settings.algorithm

# Define the password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define the OAuth2 scheme for getting the token from the request header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Define a function to verify a password given a plain password and a hashed password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Define a function to hash a password given a plain password
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Define a function to generate an access token given a user id and an expiration time of  45 minutes
def create_access_token(user_id: str, expires_delta: timedelta = timedelta(minutes=settings.access_token_expire_minutes)):
    # Get the current time
    now = datetime.utcnow()
    # Create a payload with the user id and the expiration time (if any)
    payload = {"sub": user_id}
    if expires_delta:
        expire = now + expires_delta
        payload["exp"] = expire
    # Encode the payload with the secret key and algorithm and return it as a string
    encoded_jwt = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

# Define a function to authenticate a user given a username and a password
def authenticate_user(username: str, password: str):
    # Get the user from the database by username
    user = crud.get_user_by_username(username)
    # If the user is not found or the password is not verified, return False
    if not user or not verify_password(password, user.hashed_password):
        return False
    # Otherwise, return the user
    return user

# Define a function to get the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Try to decode the token and get the user id
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Get the user from the database by key
        user = crud.get_user(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Define a function to check if the current user is active
def get_current_active_user(current_user: base.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive")
    return current_user

# Define a function to check if the current user is an admin
def get_current_admin_user(current_user: base.User = Depends(get_current_active_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not an admin")
    return current_user

# Define a function to decode a token and get the user id
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        return user_id
    except jwt.JWTError:
        return None
    

