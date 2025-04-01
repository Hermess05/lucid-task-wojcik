from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from crud import delete_post_by_post_id
from models import Users
from utilities import get_db, validate_user

router = APIRouter()


@router.delete("/delete-post/")
async def delete_post(
    post_id: int, user: Users = Depends(validate_user), db: Session = Depends(get_db)
):
    # here we are not using the user directly, but we need it for the token validation
    # that could be able done by calling here the validate_token method,
    # but in the task description there was "dependency injection" mentioned, so I decided to
    # do it this way
    if delete_post_by_post_id(db, post_id):
        return {"Message": "Post deleted successfully!"}
    raise HTTPException(status_code=404, detail="Post not found")
