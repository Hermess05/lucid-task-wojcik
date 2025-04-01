"""
This module defines the FastAPI router for retrieving posts associated with an authenticated user.

Key components:
- `get_post`: Endpoint for fetching posts belonging to the authenticated user.
- The `validate_user` dependency is used to ensure the user is authenticated before retrieving posts.
- Uses `get_all_posts_by_user_id` from the `crud` module to fetch the posts from the database.

The `get-posts` route is mapped to the `/get-posts/` URL path and supports GET requests.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud import get_all_posts_by_user_id
from models import Users
from utilities import get_db, validate_user

router = APIRouter()


@router.get("/get-posts/")
async def get_post(user: Users = Depends(validate_user), db: Session = Depends(get_db)):
    """
    Endpoint for retrieving posts associated with the authenticated user.

    This function fetches all posts that belong to the authenticated user from the database.

    Args:
        user (Users): The authenticated user, provided by the `validate_user` dependency.
        db (Session): The database session, provided by the `get_db` dependency.

    Returns:
        dict: A dictionary containing a list of posts associated with the user.

    Example Response:
        {
            "posts": [
                {"post_id": 1, "text": "Sample post text", "user_id": 1},
                {"post_id": 2, "text": "Another post text", "user_id": 1}
            ]
        }
    """
    posts = get_all_posts_by_user_id(db, user.id)
    return {"posts": posts}
