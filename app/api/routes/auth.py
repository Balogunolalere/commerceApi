# auth.py
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from core.security import (
    authenticate_user,
    create_access_token,
    decode_access_token,
    get_current_user,
    get_password_hash,
)
from services.email import (
    send_verification_email,
    send_password_reset_email,
)
from db import crud, schemas

router = APIRouter()

# Define an endpoint for user registration
@router.post("/register", response_model=schemas.User)
def register(background_tasks: BackgroundTasks, user: schemas.UserCreate):
    # Check if the username or email already exists in the database
    if crud.get_user_by_username(user.username) or crud.get_user_by_email(user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already taken")
    # Hash the password using bcrypt
    hashed_password = get_password_hash(user.hashed_password)
    # Create a new user with the hashed password and default values for is_active and is_admin
    new_user = schemas.UserCreate(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=False,
        is_admin=False,
    )
    # Save the new user in the database
    user = crud.create_user(new_user)
    # Generate a verification token with the user key as the payload
    token = create_access_token(user.key)
    # Send a verification email to the user with the token as a link
    background_tasks.add_task(send_verification_email, user.email, token)
    # Return the user data
    return user

# Define an endpoint for user verification
@router.get("/verify/{token}")
def verify(token: str):
    # Decode the token and get the user key
    user_key = decode_access_token(token)
    if user_key is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    # Get the user from the database by key
    user = crud.get_user(user_key)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # Update the user's is_active attribute to True
    user = crud.update_user(user_key, schemas.UserUpdate(is_active=True))
    # Return a success message
    return {"message": "User verified successfully"}

# Define an endpoint for user login
@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authenticate the user with the username and password from the form data
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    # Check if the user is active
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive")
    # Generate an access token with the user key as the payload and a default expiration time
    access_token = create_access_token(user.key)
    # Return the access token and its type
    return {"access_token": access_token, "token_type": "bearer"}

# Define an endpoint for requesting a password reset
@router.post("/reset-password-request")
def reset_password_request(background_tasks: BackgroundTasks, email: str):
     # Get the user from the database by email 
     user = crud.get_user_by_email(email) 
     # If the user is not found, return a success message anyway (to avoid leaking information) 
     if not user: 
         return {"message": "Password reset request sent"} 
     # Generate a password reset token with the user key as the payload and a short expiration time 
     token = create_access_token(user.key, expires_delta=timedelta(minutes=15)) 
     # Send a password reset email to the user with the token as a link 
     background_tasks.add_task(send_password_reset_email, user.email, token)
     # Return a success message 
     return {"message": "Password reset request sent"}

# Define an endpoint for resetting a password 
@router.post("/reset-password/{token}") 
def reset_password(token: str, new_password: str): 
     # Decode the token and get the user key 
     user_key = decode_access_token(token) 
     if user_key is None: 
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") 
     # Get the user from the database by key 
     user = crud.get_user(user_key) 
     if user is None: 
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") 
     # Hash the new password using bcrypt 
     hashed_password = get_password_hash(new_password) 
     # Update the user's hashed_password attribute 
     user = crud.update_user(user_key, schemas.UserUpdate(hashed_password=hashed_password)) 
     # Return a success message 
     return {"message": "Password reset successfully"}

# get the current user
@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

# Refresh token endpoint
@router.post("/refresh-token", response_model=schemas.Token)
def refresh_token(current_user: schemas.User = Depends(get_current_user)):
    access_token = create_access_token(current_user.key)
    return {"access_token": access_token, "token_type": "bearer"}

# Update user endpoint 
@router.put("/update", response_model=schemas.User)
def update_user(user_update: schemas.UserUpdate, current_user: schemas.User = Depends(get_current_user)):
    user = crud.update_user(current_user.key, user_update)
    return user

# Delete account endpoint
@router.delete("/delete/me", response_model=schemas.User)
def delete_user(current_user: schemas.User = Depends(get_current_user)):
    user = crud.delete_user(current_user.key)
    return user

# List users endpoint - Returns a list of all users in the system. Requires admin privileges.
@router.get("/list", response_model=list[schemas.User])
def list_users(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not admin")
    users = crud.get_users()
    return users

# Promote user endpoint - Allows admins to promote a user to admin. Requires admin privileges.
@router.put("/promote/{user_key}", response_model=schemas.User)
def promote_user(user_key: str, current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not admin")
    user = crud.update_user(user_key, schemas.UserUpdate(is_admin=True))
    return user

# Demote user endpoint - Allows admins to demote a user from admin. Requires admin privileges.
@router.put("/demote/{user_key}", response_model=schemas.User)
def demote_user(user_key: str, current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not admin")
    user = crud.update_user(user_key, schemas.UserUpdate(is_admin=False))
    return user

