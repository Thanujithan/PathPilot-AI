from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError

from utils.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(data: RegisterRequest):
    from main import db

    existing_user = db.users.find_one({"email": data.email})

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = {
        "name": data.name,
        "email": data.email,
        "password": hash_password(data.password)
    }

    try:
        result = db.users.insert_one(user)

        return {
            "message": "User registered successfully",
            "user_id": str(result.inserted_id)
        }

    except DuplicateKeyError:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )


@router.post("/login")
def login(data: LoginRequest):
    from main import db

    user = db.users.find_one({"email": data.email})

    if not user or not verify_password(
        data.password,
        user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(str(user["_id"]))

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }