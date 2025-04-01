"""
This module defines Pydantic models used for request validation and data serialization in the FastAPI application.

Key components:
- `UserSchema`: Pydantic model for validating and serializing user-related data, such as email and hashed password.
- `PostCreate`: Pydantic model for validating and serializing post creation data, specifically the content of the post (text).

Pydantic models are used by FastAPI to validate incoming request bodies and automatically generate API documentation.
"""

from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    """
    Pydantic model for user-related data used during user creation or authentication.

    Attributes:
        email (EmailStr): The email address of the user, validated as a proper email string.
        hashed_password (str): The hashed password of the user, validated with a minimum and maximum length constraint.

    This model is typically used for receiving user registration or login data in API endpoints.
    """
    email: EmailStr
    hashed_password: Annotated[str, Query(min_length=2, max_length=255)]


class PostCreate(BaseModel):
    """
    Pydantic model for post creation data.

    Attributes:
        text (str): The content of the post, which is a string with a maximum length of 1,000,000 characters.

    This model is used for receiving post creation data in API endpoints and ensures the post's text adheres to length constraints.
    """
    text: str = Field(..., max_length=1_000_000)
