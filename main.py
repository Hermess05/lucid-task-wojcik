"""
This module sets up the FastAPI application, includes routers, and creates the necessary database tables.

It imports FastAPI and related components to define API endpoints, as well as imports the SQLAlchemy
`Base` and `engine` to manage database connections and tables.

Key functionalities:
- Instantiates the FastAPI app.
- Includes all routers from `router_list` into the application.
- Creates the SQLAlchemy database tables based on models defined in `Base`.
"""

from fastapi import FastAPI, Request, Response

from database import Base, engine
from routers import router_list


app = FastAPI()

# Include all routers from the router_list into the FastAPI application
for router in router_list:
    app.include_router(router)

# Create all the tables in the database based on the SQLAlchemy models
Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_root(request: Request) -> Response:
    """
    Root endpoint for the FastAPI application.

    This default route responds with a simple JSON message when accessed.

    Args:
        request (Request): The FastAPI request object containing information about the incoming HTTP request.

    Returns:
        Response: A JSON response containing a simple greeting message.

    Example:
        {
            "Hello": "world!"
        }
    """
    return {"Hello": "world!"}
