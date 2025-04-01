"""
This module defines the SQLAlchemy ORM models for the application: `Users` and `Posts`.

The models are mapped to the `users` and `posts` tables in the database. They represent the structure of
the database tables and define relationships between users and their posts.

Key components:
- `Users` model: Represents a user, with fields for `id`, `email`, and `hashed_password`.
- `Posts` model: Represents a post, with fields for `post_id`, `text`, and a foreign key reference to the user (`user_id`).
- A one-to-many relationship is established between `Users` and `Posts`, meaning a user can have multiple posts.
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Users(Base):
    """
    User model representing the users of the application.

    Attributes:
        id (int): The unique identifier for the user (primary key).
        email (str): The user's email address, which must be unique.
        hashed_password (str): The user's hashed password for authentication.
        posts (relationship): A relationship to the `Posts` model that links the user to their posts.

    This model corresponds to the `users` table in the database.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(), unique=True, nullable=False, index=True)
    hashed_password = Column(String(), nullable=False)

    posts = relationship("Posts", back_populates="owner")


class Posts(Base):
    """
    Post model representing posts created by users.

    Attributes:
        post_id (int): The unique identifier for the post (primary key).
        text (str): The content of the post.
        user_id (int): A foreign key linking the post to a user, representing the author of the post.
        owner (relationship): A relationship to the `Users` model that links the post to its creator (the user).

    This model corresponds to the `posts` table in the database.
    """
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True)
    text = Column(String(), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="posts")
