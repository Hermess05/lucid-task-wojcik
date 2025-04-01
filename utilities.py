"""
This module provides functionality for creating, verifying, and validating JWT tokens
for user authentication in the FastAPI application.

It contains utility functions for:
- Creating an access token with an expiration time.
- Verifying the validity of the token and decoding it.
- Validating the user's identity based on the token.

Key Functions:
- `get_db`: A dependency that provides a database session.
- `create_access_token`: Creates a new JWT token for a user with an expiration time.
- `verify_token`: Verifies and decodes a given JWT token, retrieving the user associated with the token.
- `validate_user`: Validates the user's identity by verifying the token and ensuring the user is authorized.
"""

from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.exceptions import HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from crud import get_user_by_email
from database import SessionLocal

SECRET_KEY = "secretkey"
ALGORITHM = "HS256"


def get_db():
    """
    Dependency function that provides a database session.

    This function can be used in FastAPI route handlers to obtain a database session.

    Yields:
        Session: A SQLAlchemy database session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    """
    Creates a JWT access token with the given data and expiration time.

    Args:
        data (dict): The payload data to encode in the token (typically user info).
        expires_delta (timedelta): The time duration after which the token will expire. Default is 15 minutes.

    Returns:
        str: The generated JWT token as a string.

    This function takes the user data, sets an expiration time for the token, and encodes it using the specified
    secret key and algorithm.
    """
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str, db: Session = Depends(get_db)):
    """
    Verifies and decodes the JWT token, returning the associated user if the token is valid.

    Args:
        token (str): The JWT token to verify and decode.
        db (Session): The database session, provided via dependency injection.

    Returns:
        user (User or None): The user object if the token is valid, otherwise None.

    This function decodes the JWT token, checks if the 'sub' field (user email) exists, and verifies the
    validity of the token. If valid, it retrieves the user from the database using the decoded email.
    """
    try:
        payload = jwt.decode(token.encode("utf-8"), SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if not user_email:
            return None
    except JWTError:
        return None

    if user := get_user_by_email(db, user_email):
        return user


def validate_user(token: str, db: Session = Depends(get_db)):
    """
    Validates the user based on the provided JWT token. If the token is invalid, raises an HTTPException.

    Args:
        token (str): The JWT token to validate.
        db (Session): The database session, provided via dependency injection.

    Returns:
        user (User): The validated user object.

    Raises:
        HTTPException: If the token is invalid or user cannot be found, raises a 401 Unauthorized error.
    """
    user = verify_token(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized access.")
    return user
