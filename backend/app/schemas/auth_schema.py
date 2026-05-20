from pydantic import BaseModel
from EmailStr


class RegisterInput(
    BaseModel
):

    full_name:str

    email:EmailStr

    password:str