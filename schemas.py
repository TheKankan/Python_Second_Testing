from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


# what the api receives from the client
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


# what the api returns to the client (without the password for security reasons)
class UserOut(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
