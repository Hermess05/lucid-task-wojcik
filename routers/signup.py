"""
This module defines the FastAPI router for user signup functionality.

Key components:
- `signup_create_user`: Endpoint for creating a new user account by validating email and password.
- Uses `create_user` to add the user to the database.
- Handles `IntegrityError` if the user already exists.
- Generates an access token upon successful signup using `create_access_token`.

The signup route is mapped to the `/signup` URL path and supports POST requests.
"""

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from crud import create_user
from schemas import UserSchema
from utilities import create_access_token, get_db

router = APIRouter()


@router.post("/signup")
def signup_create_user(
    user: UserSchema = Depends(), db: Session = Depends(get_db)
) -> dict:
    """
    Endpoint for creating a new user account.

    This function takes the user's email and password, creates a new user, and stores them in the database.
    If the user already exists, an error is raised. After successfully creating the user, an access token is generated.

    Args:
        user (UserSchema): The user's email and password, validated by the `UserSchema` Pydantic model.
        db (Session): The database session, provided by the `get_db` dependency.

    Returns:
        dict: A dictionary containing the generated access token and the token type.

    Raises:
        HTTPException:
            - If the user already exists in the database, a 403 error is raised due to a conflict
            (email already in use).

    Example Response:
        {
            "access_token": "your_access_token_here",
            "token_type": "bearer"
        }
    """
    new_user = UserSchema(email=user.email, hashed_password=user.hashed_password)
    try:
        create_user(db, new_user)
    except IntegrityError:
        raise HTTPException(
            status_code=403, detail="User with given email already exists."
        )
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
