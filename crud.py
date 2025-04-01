"""
This module contains functions for handling user and post management in the application.

Functions provided:
- `create_user`: Creates a new user and adds it to the database.
- `get_user_by_email`: Retrieves a user by their email.
- `create_post`: Creates a new post for a user and stores it in the database.
- `get_all_posts_by_user_id`: Retrieves all posts made by a user, using caching for performance.
- `delete_post_by_post_id`: Deletes a post from the database by its post ID.
"""

from argon2 import PasswordHasher
from cachetools import TTLCache
from sqlalchemy.exc import IntegrityError

from database import SessionLocal
from models import Posts, Users
from schemas import PostCreate, UserSchema

ph = PasswordHasher()
posts_cache = TTLCache(maxsize=1000, ttl=300)


def create_user(db: SessionLocal, user: UserSchema) -> None:
    """
    Create a new user in the database.

    Args:
        db (SessionLocal): The database session used to commit the transaction.
        user (UserSchema): The user schema containing the email and password data.

    Returns:
        None: The function does not return a value, but commits the user creation to the database.

    Raises:
        IntegrityError: If a user with the same email already exists in the database, an exception is raised.
    """
    new_user = Users(email=user.email, hashed_password=ph.hash(user.hashed_password))
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:  # Integrity Error will occur when given email is already in the database
        db.rollback()
        raise
    db.refresh(new_user)


def get_user_by_email(db: SessionLocal, email: str) -> Users:
    """
    Retrieve a user from the database using their email.

    Args:
        db (SessionLocal): The database session used to query the database.
        email (str): The email address of the user to be retrieved.

    Returns:
        Users: The user object if found, or None if no user with the given email exists.
    """
    return db.query(Users).filter_by(email=email).first()


def create_post(db: SessionLocal, post: PostCreate, user: Users) -> int:
    """
    Create a new post in the database associated with a specific user.

    Args:
        db (SessionLocal): The database session used to commit the transaction.
        post (PostCreate): The post data to be created, containing the post text.
        user (Users): The user object representing the user creating the post.

    Returns:
        int: The ID of the newly created post.

    This function commits the new post to the database and returns its unique post ID.
    """
    new_post = Posts(text=post.text, user_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post.post_id


def get_all_posts_by_user_id(db: SessionLocal, user_id: int) -> Posts:
    """
    Retrieve all posts made by a specific user, using cache to improve performance.

    Args:
        db (SessionLocal): The database session used to query the database.
        user_id (int): The ID of the user whose posts are to be retrieved.

    Returns:
        Posts: A list of posts made by the user.

    This function checks if the user's posts are cached. If not, it queries the database and caches the result.
    """
    if user_id in posts_cache:
        return posts_cache[user_id]
    posts = db.query(Posts).filter_by(user_id=user_id).all()
    posts_cache[user_id] = posts

    return posts


def delete_post_by_post_id(db: SessionLocal, post_id: int) -> bool:
    """
    Delete a post from the database by its post ID.

    Args:
        db (SessionLocal): The database session used to commit the transaction.
        post_id (int): The ID of the post to be deleted.

    Returns:
        bool: Returns True if the post was successfully deleted, otherwise False.

    If the post with the given ID exists, it will be deleted and the transaction committed.
    """
    if post := db.query(Posts).filter_by(post_id=post_id).first():
        db.delete(post)
        db.commit()
        return True
    return False
