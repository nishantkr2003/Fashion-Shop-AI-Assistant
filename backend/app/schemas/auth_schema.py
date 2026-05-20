from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class RegisterInput(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=100
    )
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128
    )

class LoginInput(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    is_verified: bool