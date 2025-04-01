"""
This module imports and organizes the different routers for handling various API endpoints in the FastAPI application.

Key components:
- `add_post_router`: Router for adding a new post.
- `delete_post_router`: Router for deleting a post by its ID.
- `get_posts_router`: Router for fetching posts (either all posts or by user).
- `signup_router`: Router for user signup (registration).
- `login_router`: Router for user login (authentication).

`router_list` contains all the routers in the application, allowing them to be easily included into the
main FastAPI app.
"""

from .add_post import router as add_post_router
from .delete_post import router as delete_post_router
from .get_posts import router as get_posts_router
from .login import router as login_router
from .signup import router as signup_router

router_list = [
    add_post_router,
    delete_post_router,
    get_posts_router,
    signup_router,
    login_router,
]
