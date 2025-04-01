"""
This module defines the FastAPI router for adding a new post to the application.

Key components:
- `add_post`: Endpoint for adding a new post. It expects post data (text) and ensures the user is
authenticated via JWT token.
- Uses `validate_user` to ensure the user is authenticated before allowing post creation.
- Relies on `create_post` from the `crud` module to create a post in the database.

The `add-post` route is mapped to the `/add-post/` URL path and supports POST requests.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud import create_post
from models import Users
from schemas import PostCreate
from utilities import get_db, validate_user

router = APIRouter()


@router.post("/add-post/")
async def add_post(
    post: PostCreate,
    user: Users = Depends(validate_user),
    db: Session = Depends(get_db),
):
    """
    Endpoint for creating a new post.

    This function creates a new post in the database, ensuring that the user is authenticated before proceeding.

    Args:
        post (PostCreate): The data for the new post, validated by the `PostCreate` Pydantic model.
        user (Users): The authenticated user, provided by the `validate_user` dependency.
        db (Session): The database session, provided by the `get_db` dependency.

    Returns:
        dict: A dictionary containing the `post_id` of the newly created post.

    Raises:
        HTTPException: If the user is not authenticated, an exception is raised by the `validate_user` function.

    Example Response:
        {
            "post_id": 123
        }
    """
    post_id = create_post(db, post, user)
    return {"post_id": post_id}
