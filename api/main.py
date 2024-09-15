from typing import Optional

from bson import ObjectId
from fastapi import Depends, FastAPI, HTTPException, Query
from .models import Movie, User, Comment

from backend import MongoDBConfig, MongoDBConnection, settings

app = FastAPI()


# Dependency to get the MongoDB connection
async def get_mongo_connection() -> MongoDBConnection:
    config = MongoDBConfig(
        username=settings.USER,
        password=settings.PASS,
        host=settings.HOST,
        tls="true",
        tlsAllowInvalidCertificates="true",
    )
    mongo_connection = MongoDBConnection(config)
    await mongo_connection.client
    return mongo_connection


@app.get("/movies", response_model=list[Movie])
async def read_movies(
    _id: Optional[str] = Query(None, description="Filter by username"),
    title: Optional[str] = Query(None, description="Filter by title"),
    type: Optional[str] = Query(None, description="Filter by title"),
    limit: int = Query(
        10, description="Limit the number of results"
    ),  # Default limit to 10
    skip: int = Query(
        0, description="Number of records to skip"
    ),  # Default to skip 0 records
    mongo: MongoDBConnection = Depends(get_mongo_connection),
):
    filter_criteria = {}

    if _id:
        filter_criteria["_id"] = ObjectId(f"{_id}")
    if title:
        filter_criteria["title"] = title
    if type:
        filter_criteria["type"] = type

    movies = await mongo.fetch_documents(
        database_name="sample_mflix",
        collection_name="movies",
        filter_query=filter_criteria,
        limit=limit,
        skip=skip,
    )

    if not movies:
        raise HTTPException(status_code=404, detail="Movies not found")

    # Return only the first 1000 movies
    return [Movie.from_mongo(movie) for movie in movies]


@app.get("/comments", response_model=list[Comment])
async def read_movies(
    movie_id: Optional[str] = Query(None, description="Filter by username"),
    limit: int = Query(
        10, description="Limit the number of results"
    ),  # Default limit to 10
    skip: int = Query(
        0, description="Number of records to skip"
    ),  # Default to skip 0 records
    mongo: MongoDBConnection = Depends(get_mongo_connection),
):
    filter_criteria = {}

    if movie_id:
        filter_criteria["movie_id"] = ObjectId(f"{movie_id}")

    comments = await mongo.fetch_documents(
        database_name="sample_mflix",
        collection_name="comments",
        filter_query=filter_criteria,
        limit=limit,
        skip=skip,
    )

    if not comments:
        raise HTTPException(status_code=404, detail="Comments not found")

    # Return only the first 1000 movies
    return [Comment.from_mongo(comment) for comment in comments]


@app.post("/users/")
async def create_user(
    user: User, mongo_conn: MongoDBConnection = Depends(get_mongo_connection)
):
    try:
        # Check if the user with the same email already exists
        existing_users = await mongo_conn.fetch_documents(
            database_name="sample_mflix",
            collection_name="users",
            filter_query={"email": user.email},
        )

        if existing_users:
            raise HTTPException(
                status_code=400, detail="User with this email already exists"
            )

        # Insert the new user
        result = await mongo_conn.insert_documents(
            database_name="sample_mflix",
            collection_name="users",
            documents=user.model_dump(),
        )
        if result.inserted_id:
            return {"message": f"User created successfully: {result.inserted_id}"}
        else:
            raise HTTPException(status_code=500, detail="Failed to insert user")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users", response_model=list[User])
async def read_users(
    _id: Optional[str] = Query(None, description="Filter by username"),
    name: Optional[str] = Query(None, description="Filter by username"),
    email: Optional[str] = Query(None, description="Filter by email"),
    limit: int = Query(
        10, description="Limit the number of results"
    ),  # Default limit to 10
    skip: int = Query(
        0, description="Number of records to skip"
    ),  # Default to skip 0 records
    mongo: MongoDBConnection = Depends(get_mongo_connection),
):
    filter_criteria = {}

    if _id:
        filter_criteria["_id"] = ObjectId(f"{_id}")
    if name:
        filter_criteria["name"] = name
    if email:
        filter_criteria["email"] = email

    users = await mongo.fetch_documents(
        database_name="sample_mflix",
        collection_name="users",
        filter_query=filter_criteria,
        limit=limit,
        skip=skip,
    )

    if not users:
        raise HTTPException(status_code=404, detail="Users not found")

    return [User.from_mongo(user) for user in users]


# @app.put("/users/", response_model=dict)
# async def update_user(
#     user: User,
#     _id: Optional[str] = Query(None, description="Filter by email"),
#     name: Optional[str] = Query(None, description="Filter by email"),
#     email: Optional[str] = Query(None, description="Filter by email"),
#     mongo: MongoDBConnection = Depends(get_mongo_connection),
# ):
#     filter_criteria = {}
#     if _id:
#         filter_criteria["_id"] = ObjectId(f"{_id}")
#     if name:
#         filter_criteria["name"] = name
#     if email:
#         filter_criteria["email"] = email

#     result = await mongo.update_documents(
#         "sample_mflix", "users", filter_criteria, {"$set": user.model_dump()}
#     )
#     if result.matched_count == 0:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"message": "User updated successfully"}


# @app.delete("/users/", response_model=dict)
# async def delete_user(
#     _id: Optional[str] = Query(None, description="Filter by email"),
#     name: Optional[str] = Query(None, description="Filter by email"),
#     email: Optional[str] = Query(None, description="Filter by email"),
#     mongo: MongoDBConnection = Depends(get_mongo_connection),
# ):
#     filter_criteria = {}
#     if _id:
#         filter_criteria["_id"] = ObjectId(f"{_id}")
#     if name:
#         filter_criteria["name"] = name
#     if email:
#         filter_criteria["email"] = email

#     delete_result = await mongo.delete_documents(
#         "sample_mflix", "users", filter_criteria
#     )

#     if delete_result.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"message": "User deleted successfully"}
