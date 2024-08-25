from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from backend import MongoDBConfig, MongoDBConnection
from backend import settings

app = FastAPI()


# Example Pydantic model for User
class User(BaseModel):
    name: str
    password: str
    email: Optional[EmailStr] = None


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
        result = await mongo_conn._client["sample_mflix"]["users"].insert_one(
            user.model_dump()
        )
        if result.inserted_id:
            return {"message": f"User created successfully: {result.inserted_id}"}
        else:
            raise HTTPException(status_code=500, detail="Failed to insert user")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users", response_model=list[User])
async def read_users(
    _id: Optional[str] = Query(None, description="Filter by ID"),
    name: Optional[str] = Query(None, description="Filter by username"),
    email: Optional[str] = Query(None, description="Filter by email"),
    mongo: MongoDBConnection = Depends(get_mongo_connection),
):
    filter_criteria = {}
    if _id:
        filter_criteria["_id"] = _id

    if name:
        filter_criteria["name"] = name

    if email:
        filter_criteria["email"] = email

    users = await mongo.fetch_documents(
        database_name="sample_mflix",
        collection_name="users",
        filter_query=filter_criteria,
    )

    if not users:
        raise HTTPException(status_code=404, detail="Users not found")

    return users


@app.put("/users/{name}", response_model=dict)
async def update_user(
    name: str, user: User, mongo: MongoDBConnection = Depends(get_mongo_connection)
):
    update_result = await mongo._client["sample_mflix"]["users"].update_one(
        {"name": name}, {"$set": user.model_dump()}
    )
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}


@app.delete("/users/{name}", response_model=dict)
async def delete_user(
    name: str, mongo: MongoDBConnection = Depends(get_mongo_connection)
):
    delete_result = await mongo._client["sample_mflix"]["users"].delete_one(
        {"name": name}
    )
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
