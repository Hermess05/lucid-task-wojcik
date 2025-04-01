"""
This module defines the FastAPI router for user login functionality.

Key components:
- `log_in`: Endpoint for logging in a user by validating their email and password.
- Uses `get_user_by_email` to retrieve the user from the database.
- Uses the Argon2 password hashing library to verify the password.
- Generates an access token upon successful authentication using `create_access_token`.

The login route is mapped to the `/login` URL path and supports POST requests.
"""

from argon2.exceptions import VerifyMismatchError
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from crud import get_user_by_email, ph
from schemas import UserSchema
from utilities import create_access_token, get_db

router = APIRouter()


@router.post("/login")
def log_in(user: UserSchema = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint for logging in a user by verifying their email and password.

    This function retrieves the user from the database based on the provided email, verifies the password,
    and generates an access token if the credentials are correct.

    Args:
        user (UserSchema): The user's credentials, validated by the `UserSchema` Pydantic model.
        db (Session): The database session, provided by the `get_db` dependency.

    Returns:
        dict: A dictionary containing the generated access token and the token type.

    Raises:
        HTTPException:
            - If the user with the provided email does not exist, a 404 error is raised.
            - If the provided password doesn't match the stored hashed password, a 404 error is raised.

    Example Response:
        {
            "access_token": "your_access_token_here",
            "token_type": "bearer"
        }
    """
    user_from_db = get_user_by_email(db, user.email)
    if not user_from_db:
        raise HTTPException(
            status_code=404, detail="User with given email doesn't exists."
        )

    try:
        ph.verify(user_from_db.hashed_password, user.hashed_password)
    except VerifyMismatchError:
        raise HTTPException(
            status_code=404, detail="Given password doesn't match the email"
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
